#!/usr/bin/env python3
"""lab.py - portable orchestrator for the research-lab protocol.

One file, Python >= 3.10, standard library only. Talks to any endpoint that speaks
`POST {base_url}/v1/chat/completions` (Ollama, vLLM, LM Studio, ...).

The role mandates are NOT in this file: they are loaded as system prompts from
../../protocol/roles/*.md, so protocol and orchestrator stay separate.

NOT validated by the bench: the benchmark numbers were measured on the Claude Code
harness only. See README.md next to this file.
"""

import argparse
import itertools
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

TERMINATOR = "<!-- FINE DOCUMENTO -->"
ROLES_DIR = Path(__file__).resolve().parent.parent.parent / "protocol" / "roles"
ROLES = ("coordinator", "scout", "analyst", "critic", "implementer", "validator")
WORKERS = ("scout", "analyst", "critic", "implementer", "validator")
HTTP_TIMEOUT = 1800          # seconds per request; local models can be slow
MAX_FILE_CHARS = 30000       # per inlined file
MAX_LOG_CHARS = 120000       # all inlined logs together
LINE_CAPS = {"02_metodo.md": 400, "03_criteri.md": 500, "05_verdetto.md": 300}

FILE_BLOCK = re.compile(r"^<<<FILE[ \t]+([^\n>]+?)[ \t]*>>>[ \t]*\n(.*?)^<<<END>>>[ \t]*$",
                        re.M | re.S)
RUN_HEADING = re.compile(r"^#{2,3}\s+(run the full protocol|eseguire il protocollo completo)\s*$",
                         re.I)

# Appended to every role's system prompt: what this harness can and cannot do.
CONTRACT = """
---

# How this harness works (lab.py)

You are running inside lab.py, a text-only orchestrator. You have NO tools: no shell, no web,
no git, no file access. Everything you may read is pasted in the user message. Where your mandate
says "run", "search", "read the file" or "commit", the orchestrator does what it can on your
behalf, as stated below; never claim you did it yourself.

To write a file, put it in a block exactly like this, path relative to the run directory:

<<<FILE path/inside/the/run.md>>>
...full file content...
<<<END>>>

Write every file in full (no diffs, no placeholders). Every markdown document you write must end
with the line """ + TERMINATOR + """. Anything outside the blocks is your short report.
"""

ROLE_CONTRACT = {
    "coordinator": "You are consulted by the orchestrator, which itself delegates, writes files "
                   "and commits. Answer exactly what each message asks, in the format it asks.",
    "scout": "You cannot query any API or open any page. Catalogue only works you know, write "
             "'unverified (model memory)' in the citations column of every row and in the 'APIs "
             "queried' field. Write exactly the one file named in the message.",
    "analyst": "Write exactly two files: 02_metodo.md and 03_criteri.md. You cannot fetch papers: "
               "work from the catalogue and what you know, and list what you could not check in "
               "'What the paper does NOT say'.",
    "critic": "Do NOT use FILE blocks. Reply with the full text of the requested document and "
              "nothing else; the coordinator writes it to disk. It must end with " + TERMINATOR +
              ". You cannot run code: compute by hand and show the computation, or write the "
              "point as a suspicion to be verified.",
    "implementer": "Write files only under 04_impl/, never under 04_impl/logs/. You cannot run "
                   "anything. After you, the orchestrator executes the commands of the ```bash "
                   "block in the section '## Run the full protocol' of 04_impl/come_eseguire.md, "
                   "one command per line, from inside 04_impl/, each with a timeout. That block "
                   "must be self-sufficient (create any virtual environment there), and the code "
                   "must write every log under logs/ (that is, 04_impl/logs/).",
    "validator": "You cannot run anything: the orchestrator has already executed the full "
                 "protocol once, exactly as declared in come_eseguire.md; the console output of "
                 "each command and every file under 04_impl/logs/ are pasted below. Measure from "
                 "those. Write exactly one file: 05_verdetto.md.",
}


# ---------------------------------------------------------------- pure functions

def extract_files(text):
    """Return [(path, content)] for every <<<FILE path>>> ... <<<END>>> block in text."""
    return [(m.group(1).strip(), m.group(2)) for m in FILE_BLOCK.finditer(text)]


def strip_blocks(text):
    """The part of a reply outside the file blocks (the worker's report)."""
    return FILE_BLOCK.sub("", text).strip()


def safe_path(run_dir, rel):
    """Resolve rel inside run_dir; raise ValueError if it is empty, absolute or escapes."""
    rel = rel.strip()
    if not rel:
        raise ValueError("empty path")
    if rel.startswith(("/", "\\", "~")) or re.match(r"^[A-Za-z]:", rel):
        raise ValueError(f"absolute path refused: {rel}")
    if ".." in re.split(r"[\\/]", rel):
        raise ValueError(f"path with '..' refused: {rel}")
    root = Path(run_dir).resolve()
    target = (root / rel).resolve()
    if root not in target.parents:
        raise ValueError(f"path outside the run directory refused: {rel}")
    return target


def check_complete(path):
    """Minimal completeness check. Return None if ok, else the reason."""
    p = Path(path)
    if not p.is_file():
        return "missing"
    text = p.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        return "empty"
    if text.strip().splitlines()[-1].strip() != TERMINATOR:
        return f"does not end with {TERMINATOR}"
    return None


def parse_commands(md):
    """Commands of the ```bash block under '## Run the full protocol' in come_eseguire.md."""
    lines = md.splitlines()
    start = next((i for i, l in enumerate(lines) if RUN_HEADING.match(l.strip())), None)
    if start is None:
        return []
    level = len(lines[start].strip().split()[0])
    commands, inside = [], False
    for line in lines[start + 1:]:
        s = line.strip()
        if not inside:
            h = re.match(r"^(#{1,6})\s", s)
            if h and len(h.group(1)) <= level:
                break                               # next section: no block found
            if re.match(r"^```(bash|sh|shell)\b", s):
                inside = True
            continue
        if s.startswith("```"):
            break
        if s and not s.startswith("#"):
            commands.append(s)
    return commands


def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:40].strip("-") or "run"


def body_of(text):
    """Document text without its terminator line."""
    return text.rstrip().removesuffix(TERMINATOR).rstrip()


def load_role(name):
    path = ROLES_DIR / f"{name}.md"
    if not path.is_file():
        raise SystemExit(f"lab.py: role file missing: {path}\n"
                         "lab.py loads the role mandates from protocol/roles/ of the repository; "
                         "keep harness/openai-compatible/ inside the repository layout.")
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------- orchestrator

def say(msg):
    print(f"[lab] {msg}", flush=True)


def die(msg):
    raise SystemExit(f"lab.py: {msg}")


class Lab:
    def __init__(self, args):
        self.args = args
        self.roles = {r: load_role(r) for r in ROLES}
        self.models = {r: getattr(args, f"model_{r}", None) or args.model for r in ROLES}
        missing = [r for r, m in self.models.items() if not m]
        if missing:
            die(f"no model for {', '.join(missing)}: set --model (or LAB_MODEL)")
        url = args.base_url.rstrip("/")
        self.url = (url if url.endswith("/v1") else url + "/v1") + "/chat/completions"
        self.problem = Path(args.problem).read_text(encoding="utf-8").strip()
        if not self.problem:
            die(f"problem file is empty: {args.problem}")
        first = next(l for l in self.problem.splitlines() if l.strip())
        name = f"{date.today():%Y%m%d}-{slugify(first.lstrip('# '))}"
        self.run_dir = Path(args.run_dir or Path("run") / name).resolve()
        if self.run_dir.exists() and any(self.run_dir.iterdir()):
            die(f"run directory exists and is not empty: {self.run_dir} (lab.py does not resume)")
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.name = self.run_dir.name
        self.counter = itertools.count(1)
        self.repo, self.git_env = None, None
        if not args.no_git:
            self.setup_git()

    # ---- model calls

    def chat(self, role, user):
        system = self.roles[role] + CONTRACT + "\n" + ROLE_CONTRACT[role] + "\n"
        body = json.dumps({"model": self.models[role], "stream": False,
                           "messages": [{"role": "system", "content": system},
                                        {"role": "user", "content": user}]}).encode()
        headers = {"Content-Type": "application/json"}
        if self.args.api_key:
            headers["Authorization"] = f"Bearer {self.args.api_key}"
        for attempt in (1, 2):
            try:
                req = urllib.request.Request(self.url, data=body, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                    reply = json.load(r)["choices"][0]["message"]["content"] or ""
                break
            except urllib.error.HTTPError as e:
                err = f"HTTP {e.code}: {e.read()[:500].decode(errors='replace')}"
            except (urllib.error.URLError, OSError) as e:
                err = str(e)
            except (KeyError, IndexError, TypeError, ValueError) as e:
                die(f"{role}: unexpected response from {self.url}: {e!r}")
            if attempt == 2:
                die(f"{role}: request to {self.url} failed twice: {err}")
            say(f"{role}: request failed ({err}); retrying once in 5 s")
            time.sleep(5)
        # Raw replies are kept for inspection; they are never passed to another role.
        tdir = self.run_dir / ".transcripts"
        tdir.mkdir(exist_ok=True)
        (tdir / f"{next(self.counter):02d}-{role}.md").write_text(reply, encoding="utf-8")
        return reply

    def document(self, role, user, rel):
        """Ask a role for a plain-text document (coordinator, critic) and write it to rel."""
        text = self.chat(role, user)
        path = safe_path(self.run_dir, rel)
        path.write_text(text.strip() + "\n", encoding="utf-8")
        self.require_complete(rel)
        return text

    def write_blocks(self, role, reply, allowed):
        """Write the file blocks of reply whose path satisfies allowed(path)."""
        written = []
        for rel, content in extract_files(reply):
            try:
                path = safe_path(self.run_dir, rel)
            except ValueError as e:
                say(f"{role}: {e}")
                continue
            rel = path.relative_to(self.run_dir.resolve()).as_posix()
            if not allowed(rel):
                say(f"{role}: refused to write {rel} (outside its mandate)")
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            written.append(rel)
        say(f"{role} wrote: {', '.join(written) or 'nothing'}")
        return written

    def require_complete(self, rel):
        reason = check_complete(self.run_dir / rel)
        if reason:
            die(f"{rel}: {reason}. Completeness check failed; raw replies in "
                f"{self.run_dir / '.transcripts'}")
        cap = LINE_CAPS.get(rel)
        n = len((self.run_dir / rel).read_text(encoding="utf-8").splitlines())
        if cap and n > cap:
            say(f"WARNING: {rel} has {n} lines, cap {cap} (accepted only if declared at the top)")

    def inline(self, *rels):
        parts = []
        for rel in rels:
            text = (self.run_dir / rel).read_text(encoding="utf-8", errors="replace")
            if len(text) > MAX_FILE_CHARS:
                text = text[:MAX_FILE_CHARS] + f"\n[... truncated by lab.py, {len(text)} chars]\n"
            parts.append(f"===== {rel} =====\n{text}")
        return "\n\n".join(parts)

    def inline_logs(self):
        logs = self.run_dir / "04_impl" / "logs"
        files = sorted(p for p in logs.rglob("*") if p.is_file())
        parts, used, skipped = [f"Files under 04_impl/logs/: {len(files)}"], 0, []
        for p in files:
            rel = p.relative_to(self.run_dir).as_posix()
            try:
                text = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                skipped.append(rel + " (binary)")
                continue
            text = text[:MAX_FILE_CHARS]
            if used + len(text) > MAX_LOG_CHARS:
                skipped.append(rel)
                continue
            used += len(text)
            parts.append(f"===== {rel} =====\n{text}")
        if skipped:
            parts.append("Not inlined (size cap or binary): " + ", ".join(skipped))
        return "\n\n".join(parts)

    # ---- git: the orchestrator is the only committer

    def git(self, *a, check=True):
        return subprocess.run(["git", "-C", str(self.repo), *a], capture_output=True, text=True,
                              check=check, env=self.git_env)

    def setup_git(self):
        r = subprocess.run(["git", "-C", str(self.run_dir), "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True)
        if r.returncode == 0:
            self.repo = Path(r.stdout.strip()).resolve()
        else:
            subprocess.run(["git", "init", "-q", str(self.run_dir)], check=True)
            self.repo = self.run_dir
            say(f"initialised a git repository in {self.run_dir}")
        if not self.git("config", "user.email", check=False).stdout.strip():
            self.git_env = dict(os.environ, GIT_AUTHOR_NAME="lab.py", GIT_COMMITTER_NAME="lab.py",
                                GIT_AUTHOR_EMAIL="lab.py@localhost",
                                GIT_COMMITTER_EMAIL="lab.py@localhost")

    def commit(self, msg, rels):
        if self.repo is None:
            return
        paths = [str((self.run_dir / r).resolve().relative_to(self.repo))
                 for r in rels if (self.run_dir / r).exists()]
        if not paths:
            return
        self.git("add", "--", *paths)
        r = self.git("commit", "-q", "-m", msg, "--", *paths, check=False)
        if r.returncode:
            die(f"commit '{msg}' failed: {r.stderr.strip() or r.stdout.strip()}")
        say(f"committed: {msg}")

    # ---- checkpoints

    def checkpoint(self, n, title, summary, question, options=None, default="", context=""):
        """Human decides (attended) or coordinator decides (--unattended). Recorded in the run.
        options=None means a free-text decision; context is shown to the model only."""
        print(f"\n===== CHECKPOINT {n} - {title} =====\n{summary}\n", flush=True)
        if self.args.unattended:
            fmt = (f"First line exactly 'DECISION: <one of {'|'.join(options)}>', then the "
                   "motivation in a few lines." if options else
                   "First line 'DECISION: <your decision>', then the motivation in a few lines.")
            reply = self.chat("coordinator", f"CHECKPOINT {n} - {title}\n\n{summary}\n\n{context}"
                                             f"\n\n{question}\nNo human is available: you decide. "
                                             f"{fmt}")
            m = re.search(r"DECISION:\s*\**\s*(.+)", reply)
            decision = m.group(1).strip().strip("*").strip() if m else ""
            if options:
                decision = next((o for o in options if decision.upper().startswith(o)), options[-1])
            who, why = "coordinator (unattended)", reply.strip()
        else:
            prompt = f"{question} [{'/'.join(options)}]: " if options else f"{question}: "
            decision = input(prompt).strip()
            if options:      # empty or unknown answer = the last (most conservative) option
                decision = next((o for o in options if decision and o.startswith(decision.upper())),
                                options[-1])
            who, why = "human", ""
        decision = decision or default
        say(f"checkpoint {n}: {decision}")
        self.last_checkpoint = f"**Decision:** {decision}\n\n{why}".strip()
        with open(self.run_dir / "checkpoints.md", "a", encoding="utf-8") as f:
            f.write(f"## Checkpoint {n} - {title}\n\nDecided by: {who}\n\n"
                    f"{self.last_checkpoint}\n\n")
        return decision

    # ---- phases

    def phase0_problem(self):
        say(f"run directory: {self.run_dir}")
        reply = self.chat("coordinator", "PHASE 0. The human's problem:\n\n" + self.problem +
                          "\n\nAsk 1-4 targeted clarifying questions (what success means, "
                          "boundaries, known constraints). One per line, each starting with 'Q: '.")
        questions = [m.group(1).strip() for m in
                     re.finditer(r"^[\s\-*\d.)]*\**Q\d*\**\s*:\**\s*(.+)$", reply, re.M)]
        if not questions:
            qa = "(no questions asked)"
        elif self.args.unattended:
            qa = self.chat("coordinator", "Problem:\n\n" + self.problem + "\n\nQuestions:\n" +
                           "\n".join(f"- {q}" for q in questions) + "\n\nNo human is available. "
                           "Answer each question yourself, conservatively, from the problem text; "
                           "mark every answer that is your assumption. Format, for each question: "
                           "'**Q:** ...' on one line, '**A (coordinator, unattended):** ...' on the next.")
        else:
            qa = ""
            for q in questions:
                a = input(f"\nQ: {q}\nA: ").strip() or "(no answer)"
                qa += f"**Q:** {q}\n**A:** {a}\n\n"
        rest = self.chat("coordinator", "Problem:\n\n" + self.problem + "\n\nQuestions and answers:"
                         "\n\n" + qa + "\n\nWrite ONLY these three sections of 00_problema.md: "
                         "'## Boundaries' (in / out), '## Known constraints', '## Stop criteria' "
                         f"(when to stop even without success). End with the line {TERMINATOR}.")
        text = (f"# Problem\n\n## Statement\n\n{self.problem}\n\n## Questions and answers\n\n"
                f"{qa.strip()}\n\n{rest.strip()}\n")
        (self.run_dir / "00_problema.md").write_text(text, encoding="utf-8")
        self.require_complete("00_problema.md")
        self.commit(f"problem: {self.name}", ["00_problema.md"])

    def phase1_scouts(self):
        n = self.args.scouts
        reply = self.chat("coordinator", self.inline("00_problema.md") + f"\n\nPHASE 1. Propose "
                          f"exactly {n} DISJOINT research directions for {n} scout(s). One per "
                          "line: '<slug>: <direction>', slug in lowercase-with-dashes.")
        dirs = []
        for line in reply.splitlines():
            m = re.match(r"^\s*(?:[-*]|\d+[.)])?\s*`?([a-z0-9][a-z0-9-]*)`?\s*:\s*(.+)$", line)
            if m and m.group(1) not in dict(dirs):
                dirs.append((m.group(1), m.group(2).strip()))
        if not dirs:
            die("the coordinator proposed no parseable scout direction")
        dirs = dirs[:n]
        say("scout directions: " + "; ".join(f"{s}: {d}" for s, d in dirs))

        def scout(sd):
            slug, direction = sd
            rel = f"01_fonti__{slug}.md"
            r = self.chat("scout", f"Direction: {direction}\nRun path: {self.run_dir}\n"
                          f"Write exactly one file: {rel}\n\n" + self.inline("00_problema.md"))
            self.write_blocks("scout", r, lambda p: p == rel)
            return rel

        with ThreadPoolExecutor(max_workers=len(dirs)) as pool:
            files = list(pool.map(scout, dirs))
        for rel in files:
            self.require_complete(rel)
        merged = "# Sources - merged catalogue\n\nMerged by lab.py by concatenation of the scout " \
                 "files (not deduplicated by DOI).\n\n"
        for rel in files:
            merged += body_of((self.run_dir / rel).read_text(encoding="utf-8")) + "\n\n"
        (self.run_dir / "01_fonti.md").write_text(merged + TERMINATOR + "\n", encoding="utf-8")
        self.checkpoint(1, "sources", f"Candidate sources: {self.run_dir / '01_fonti.md'}",
                        "Which candidates should the analyst read? (free text; empty = all)",
                        default="all candidates", context=self.inline("01_fonti.md"))
        self.sources_choice = self.last_checkpoint
        self.commit(f"sources: {self.name}", files + ["01_fonti.md", "checkpoints.md"])

    def phase2_analysis(self):
        critique = ""
        for rnd in range(1, self.args.max_critic_rounds + 1):
            user = self.inline("00_problema.md", "01_fonti.md") + \
                "\n\nCheckpoint 1 - sources chosen for analysis:\n" + self.sources_choice
            if critique:
                user += "\n\nThe critic asked for a rewrite. Rewrite BOTH files addressing every " \
                        "finding.\n\n" + self.inline("02_metodo.md", "03_criteri.md", "03b_critica.md")
            r = self.chat("analyst", user)
            self.write_blocks("analyst", r, lambda p: p in ("02_metodo.md", "03_criteri.md"))
            for rel in ("02_metodo.md", "03_criteri.md"):
                self.require_complete(rel)
            head = "\n".join((self.run_dir / "03_criteri.md").read_text().splitlines()[:30]).upper()
            if "FEASIBILITY GATE NOT PASSED" in head or \
                    ("CANCELLO DI FATTIBILIT" in head and "NON SUPERATO" in head):
                say("FEASIBILITY GATE NOT PASSED: the run stops here (a successful outcome)")
                self.checkpoint(2, "feasibility gate not passed",
                                f"See the top of {self.run_dir / '03_criteri.md'}",
                                "Acknowledge the stop", ["STOP"])
                self.commit(f"analysis: feasibility gate not passed, {self.name}",
                            ["02_metodo.md", "03_criteri.md", "checkpoints.md"])
                return False
            critique = self.document("critic", "CRITERIA mode, round " + str(rnd) + ". Write the "
                                     "text of 03b_critica.md.\n\n" +
                                     self.inline("00_problema.md", "02_metodo.md", "03_criteri.md"),
                                     "03b_critica.md")
            head = "\n".join(critique.splitlines()[:15]).upper()
            if "TO BE REWRITTEN" not in head and "DA RISCRIVERE" not in head:
                break
            say(f"critic round {rnd}: TO BE REWRITTEN")
        verdict = next((l for l in critique.splitlines() if re.search(
            r"ACCEPTABLE|TO BE REWRITTEN|ACCETTABILI|DA RISCRIVERE", l, re.I)), "(not found)")
        decision = self.checkpoint(
            2, "freeze the criteria",
            f"Criteria: {self.run_dir / '03_criteri.md'}\nCritique: {self.run_dir / '03b_critica.md'}"
            f"\nCritique verdict line: {verdict.strip()}",
            "Freeze the criteria and proceed to implementation?", ["FREEZE", "STOP"],
            context=self.inline("03_criteri.md", "03b_critica.md"))
        self.commit(f"analysis: method and critique, {self.name}",
                    ["02_metodo.md", "03b_critica.md", "checkpoints.md"])
        if decision != "FREEZE":
            say("stopped at checkpoint 2: criteria not frozen")
            return False
        self.commit(f"criteria: frozen for {self.name}", ["03_criteri.md"])   # dedicated commit
        return True

    def phase3_implementation(self):
        r = self.chat("implementer", f"Run path: {self.run_dir}\n\n" +
                      self.inline("02_metodo.md", "03_criteri.md", "03b_critica.md"))
        written = self.write_blocks("implementer", r, lambda p: p.startswith("04_impl/")
                                    and not p.startswith("04_impl/logs/"))
        self.require_complete("04_impl/come_eseguire.md")
        self.commands = parse_commands((self.run_dir / "04_impl/come_eseguire.md").read_text())
        if not self.commands:
            die("04_impl/come_eseguire.md has no ```bash block under '## Run the full protocol'")
        decision = self.checkpoint(
            3, "implementation",
            "Implementer's report:\n" + (strip_blocks(r) or "(none)") + "\n\nCommands the "
            "orchestrator will run in 04_impl/:\n" + "\n".join(f"  {c}" for c in self.commands),
            "Run these commands on this machine?", ["RUN", "STOP"])
        self.commit(f"implementation: {self.name}", written + ["checkpoints.md"])
        if decision != "RUN":
            say("stopped at checkpoint 3: protocol not executed")
            return False
        return True

    def execute(self):
        impl = self.run_dir / "04_impl"
        logs = impl / "logs"
        logs.mkdir(exist_ok=True)
        for i, cmd in enumerate(self.commands, 1):
            say(f"$ {cmd}")
            try:
                p = subprocess.run(cmd, shell=True, cwd=impl, capture_output=True, text=True,
                                   timeout=self.args.cmd_timeout)
                code, out, err = p.returncode, p.stdout, p.stderr
            except subprocess.TimeoutExpired as e:
                code = f"TIMEOUT after {self.args.cmd_timeout} s"
                out = e.stdout.decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
                err = e.stderr.decode(errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
            say(f"  exit: {code}")
            (logs / f"_orchestrator_cmd_{i:02d}.log").write_text(
                f"$ {cmd}\nexit: {code}\n--- stdout ---\n{out}\n--- stderr ---\n{err}\n",
                encoding="utf-8")
        # Raw logs committed BEFORE the validator and the counter-verdict read them.
        self.commit(f"execution: raw logs of {self.name}", ["04_impl/logs"])

    def phase4_validation(self):
        r = self.chat("validator", f"Run path: {self.run_dir}\n\n" +
                      self.inline("03_criteri.md", "04_impl/come_eseguire.md") + "\n\n" +
                      self.inline_logs())
        self.write_blocks("validator", r, lambda p: p == "05_verdetto.md")
        self.require_complete("05_verdetto.md")
        self.commit(f"validation: verdict of {self.name}", ["05_verdetto.md"])
        deleted = "(no git)"
        if self.repo is not None:
            logs_rel = str((self.run_dir / "04_impl/logs").relative_to(self.repo))
            deleted = self.git("log", "--diff-filter=D", "--oneline", "--", logs_rel,
                               check=False).stdout.strip() or "(none)"
        self.document("critic", "VERDICT mode. Write the text of 05b_controverdetto.md.\n"
                      f"Deletions recorded by git under 04_impl/logs/: {deleted}\n\n" +
                      self.inline("03_criteri.md", "05_verdetto.md") + "\n\n" + self.inline_logs(),
                      "05b_controverdetto.md")
        outcome = next((l for l in (self.run_dir / "05_verdetto.md").read_text().splitlines()
                        if re.search(r"PASSA|INCONCLUSIVO", l)), "(outcome line not found)")
        self.checkpoint(4, "outcome", f"Verdict: {outcome.strip()}\nVerdict file: "
                        f"{self.run_dir / '05_verdetto.md'}\nCounter-verdict: "
                        f"{self.run_dir / '05b_controverdetto.md'}",
                        "Close the run", ["CLOSE"])
        self.commit(f"counter-verdict: {self.name}", ["05b_controverdetto.md", "checkpoints.md"])

    def run(self):
        self.phase0_problem()
        self.phase1_scouts()
        if self.phase2_analysis() and self.phase3_implementation():
            self.execute()
            self.phase4_validation()
        if self.repo is not None:
            rel = lambda p: str((self.run_dir / p).relative_to(self.repo))
            order = self.git("log", "--diff-filter=A", "--format=%h %s", "--",
                             rel("03_criteri.md"), rel("04_impl"), check=False).stdout
            print("\nOrder check (03_criteri.md must be the OLDEST, i.e. last line):\n" + order)
        say(f"done: {self.run_dir}")


def main(argv=None):
    env = os.environ.get
    p = argparse.ArgumentParser(
        description="Run the research-lab protocol on an OpenAI-compatible endpoint "
                    "(Ollama, vLLM, LM Studio, ...). NOT validated by the bench.")
    p.add_argument("--problem", required=True, help="markdown file with the problem statement")
    p.add_argument("--base-url", default=env("LAB_BASE_URL", "http://localhost:11434"),
                   help="endpoint root; /v1/chat/completions is appended "
                        "(env LAB_BASE_URL, default %(default)s = Ollama)")
    p.add_argument("--api-key", default=env("LAB_API_KEY"),
                   help="optional, sent as 'Authorization: Bearer' (env LAB_API_KEY)")
    p.add_argument("--model", default=env("LAB_MODEL"),
                   help="model for every role, coordinator included (env LAB_MODEL)")
    for role in WORKERS:
        p.add_argument(f"--model-{role}", help=f"override --model for the {role}")
    p.add_argument("--run-dir", help="default: run/<YYYYMMDD>-<slug of the problem's first line>")
    p.add_argument("--scouts", type=int, default=2, choices=range(1, 5), metavar="N",
                   help="parallel scouts, 1-4 (default %(default)s)")
    p.add_argument("--max-critic-rounds", type=int, default=2,
                   help="analyst/critic rounds on the criteria (default %(default)s)")
    p.add_argument("--cmd-timeout", type=int, default=600,
                   help="seconds per command of come_eseguire.md (default %(default)s)")
    p.add_argument("--unattended", action="store_true",
                   help="checkpoints decided by the coordinator model instead of input()")
    p.add_argument("--no-git", action="store_true", help="do not commit (the order proof is lost)")
    args = p.parse_args(argv)
    if args.max_critic_rounds < 1:
        p.error("--max-critic-rounds must be >= 1")
    Lab(args).run()


if __name__ == "__main__":
    sys.exit(main())
