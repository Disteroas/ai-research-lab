# Harness: Claude Code (reference implementation)

**This is the harness on which the benchmark numbers were measured.** The files here are the
validated system of round 5 of the bench, taken from the snapshot of 2026-10-17 as **sanitized copies**
(see [SANITIZATION.md](../../SANITIZATION.md)): author-specific paths, note-system names and plugin names
were replaced by placeholders, nothing else. They are in **Italian** (the language the lab works in). English renderings of the
same mandates, without Claude Code specifics, are in [`../../protocol/`](../../protocol/).

| Path | What it is |
|---|---|
| `agents/lab-scout.md`, `lab-analista.md`, `lab-critic.md`, `lab-implementatore.md`, `lab-validatore.md` | the five worker subagents (scout, analyst, critic, implementer, validator), with Claude Code frontmatter (`model`, `tools`) |
| `skills/laboratorio/SKILL.md` | the coordinator, as a skill invoked with `/laboratorio` |
| `CLAUDE.md` | the lab's rules file (rules 1-17 and the structure of a run; rules 18-19 are in `giro6/CLAUDE.md`) |
| `SHA256SUMS.txt` | sha256 of the seven shipped (sanitized) files, in the snapshot's format; the sha256 of the validated originals stay in the author's private bench |
| `scripts/` | the launch, surveillance and verification scripts used by the bench (see [`scripts/README.md`](scripts/README.md)) |
| [`giro6/`](giro6/) | the system of round 6 (**FIX 1-17**): only the 2 files that differ from round 5, `CLAUDE.md` and `agents/lab-critic.md`, plus a `SHA256SUMS.txt` for the seven round-6 files (sanitized copies) |

## Verify the shipped copies

`SHA256SUMS.txt` uses the snapshot's flat file names. From this directory:

```bash
sed -e 's#  laboratorio-CLAUDE.md$#  CLAUDE.md#' \
    -e 's#  skill-laboratorio-SKILL.md$#  skills/laboratorio/SKILL.md#' \
    -e 's#  lab-#  agents/lab-#' SHA256SUMS.txt | shasum -a 256 -c
```

Seven `OK` lines expected.

## Round 5 and round 6: two systems, two files apart

The files at the top of this directory are the system of **round 5 = FIX 1-16** (snapshot
`2026-10-17-giro5`, lab commit `8958eb7`). Round 6 ran **FIX 1-17** (snapshot `2026-10-17-giro6`, lab
commit `128634d`), which changes **2 of the 7 files**: `CLAUDE.md` gains rules 18 and 19 (section
"Le due regole del giro 5 del banco (FIX 17)"), and `lab-critic.md` gains one row in the table of its
criteria mode ("Esito non risolto con etichetta affermativa"). The other 5 files are identical, so
[`giro6/`](giro6/) holds only the two changed files; its `SHA256SUMS.txt` lists all 7 files of
the round-6 system (sanitized copies). To install the round-6 system, copy the round-5 files and then overwrite
`CLAUDE.md` and `agents/lab-critic.md` with the ones in `giro6/`. From `giro6/`:

```bash
sed -E -e 's#  laboratorio-CLAUDE\.md$#  CLAUDE.md#' \
       -e 's#  lab-critic\.md$#  agents/lab-critic.md#' \
       -e 's#  skill-laboratorio-SKILL\.md$#  ../skills/laboratorio/SKILL.md#' \
       -e 's#  lab-(analista|implementatore|scout|validatore)\.md$#  ../agents/lab-\1.md#' \
       SHA256SUMS.txt | shasum -a 256 -c
```

Seven `OK` lines expected: two against `giro6/`, five against the round-5 files above.

**Which numbers were measured on which files.** The round-6 numbers (verdict 4/4, path 16/16) were
measured on the system in [`giro6/`](giro6/) plus the five unchanged files (FIX 1-17); the round-5
numbers (verdict 2/4, path 15/16) on the seven files at the top of this directory, `agents/`,
`skills/` and `CLAUDE.md` (FIX 1-16) ([`registro.md`](../../results/bench/registro.md), lines 61
and 105).

## Install into a run repository

The definitions are **project-scoped**: they live inside the repository where runs are created, not
in `~/.claude`. Copies in `~/.claude` would be loaded by every session on the machine and must be
absent.

```bash
REPO=~/my-lab                       # any git repository; runs go in $REPO/run/
mkdir -p "$REPO/.claude/agents" "$REPO/.claude/skills/laboratorio"
cp agents/lab-*.md               "$REPO/.claude/agents/"
cp skills/laboratorio/SKILL.md   "$REPO/.claude/skills/laboratorio/SKILL.md"
cp CLAUDE.md                     "$REPO/CLAUDE.md"
cd "$REPO" && git init           # if it is not a repository yet
```

Before the first run, edit `lab-scout.md`: the OpenAlex and Crossref queries carry a `mailto=`
parameter set to the placeholder `<your-email>`; put your own.

The Italian files mention `<note dell'autore>` (the author's personal notes) and "l'agente che aggiorna le note"
(an agent of the author's that updates those notes) in `CLAUDE.md` and `skills/laboratorio/SKILL.md`,
here optionally after checkpoint 4 ("se l'utente vuole", `SKILL.md`). Neither is in this
repository, and neither is needed to run the lab.

## Run it — attended

```bash
cd "$REPO"
claude --model <model-id>
> /laboratorio <your problem, in plain words>
```

The coordinator asks a few questions, then stops at the four checkpoints for your decisions.

**Pin the model with `--model`.** The machine default is not a guarantee: once the settings file
declared one model and a detached process committed as another, and a run that switches model
halfway is not interpretable. Subagents declare their own tier in the frontmatter (`model: sonnet`
for scouts, `model: opus` for the others).

## Run it — unattended (how the bench was run)

The bench launches each case as a **detached** `claude -p` process with no human at the checkpoints:

- the prompt is `/laboratorio ` + the problem text + `scripts/prompt-NOTA-NON-PRESIDIATA.txt` (the
  "unattended mode" note: the coordinator decides at checkpoints and documents why; everything else
  is unchanged); `scripts/genera-prompt.sh` builds it from a case file;
- `scripts/stacca.sh <case>` runs a **pre-flight** request to check that the pinned model really
  answers, then detaches the run (survives closing the terminal), with
  `--model "$MODELLO"` (variable `MODELLO`, default the model of round 5),
  `--permission-mode bypassPermissions`, and an appended system prompt that confines the session to
  its repository. At start and end it records `verifica-sistema.sh` output and the
  `Co-Authored-By` trailers of the run's commits (there must be exactly one model);
- `scripts/sorveglia.sh` watches the running cases, relaunches a case that stopped before the
  counter-verdict (up to a cap), and exits only on what needs human judgment: system drift, relaunch
  cap reached, all cases done, time cap;
- `scripts/verifica-sistema.sh <snapshot> [repo]` compares the definitions in the run repository
  with a snapshot (sha256) and prints the live environment; `scripts/istantanea.sh <name>` takes a
  snapshot (definitions, sha256, Claude Code version, declared models, plugins, hooks).

`bypassPermissions` gives the session unrestricted tool use inside the run: launch unattended runs
only in a disposable environment.

## Other models through an Anthropic-compatible proxy

Claude Code talks to the endpoint in `ANTHROPIC_BASE_URL`. Pointing it at a proxy that exposes the
Anthropic Messages API in front of another provider (including a local model server) is a way to run
this same harness on non-Claude models; the frontmatter aliases (`sonnet`, `opus`) and `--model`
must then map to models the proxy knows.

**Not tested by the author.** The benchmark numbers hold only for the configuration recorded in the
snapshot (Claude Code 2.1.291, coordinator pinned to `claude-opus-5-5`). For a harness that does not
need Claude Code at all, see [`../openai-compatible/`](../openai-compatible/) — also not validated.

## How the shipped copies differ from the validated files

The shipped files are **not byte-identical** to the ones the bench measured. Two kinds of change, both
string substitutions that leave every rule, threshold and instruction as it was:

- `agents/lab-scout.md`: the author's e-mail address was removed from the two API examples (OpenAlex and
  Crossref "polite pool" parameters) and replaced by `<your-email>`, which you should fill in before running;
- the sanitization described in [SANITIZATION.md](../../SANITIZATION.md): workspace paths, the name of the
  author's note system and of a plugin replaced by placeholders, in `CLAUDE.md`, `giro6/CLAUDE.md`,
  `skills/laboratorio/SKILL.md`, `agents/lab-analista.md`, `agents/lab-implementatore.md`,
  `agents/lab-scout.md` and the scripts.

`agents/lab-critic.md`, `giro6/agents/lab-critic.md` and `agents/lab-validatore.md` are unchanged. Both
`SHA256SUMS.txt` files in this folder list the sha256 of the shipped copies. The sha256 of the validated
originals (quoted by prefix in the bench files, e.g. `f50666f66633d9b9…` for the round-5 `CLAUDE.md` and
`8dfe7fcb7696381e…` for the round-6 one) stay in the bench snapshots of the author's private repository.
