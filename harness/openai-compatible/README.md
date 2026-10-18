# Harness: OpenAI-compatible endpoints (portable, unvalidated)

**NOT validated by the bench: the benchmark numbers were measured on the Claude Code harness only.**
This orchestrator runs the same protocol on any model served behind an OpenAI-compatible
`/v1/chat/completions` endpoint — Ollama, vLLM, LM Studio, or a hosted provider — so the lab can be
tried with local models. Whether a given model follows the protocol well enough is exactly what has
not been measured.

## What it is

- **One file**, [`lab.py`](lab.py): Python ≥ 3.10, standard library only, no dependencies.
- **The roles are not in the code.** `lab.py` loads the six mandates from
  [`../../protocol/roles/`](../../protocol/roles/) and uses them as system prompts, appending a short
  "how this harness works" contract (no tools, how to write files). Keep the repository layout.
- **The same chain and the same files** as the protocol: `00_problema.md` → parallel scouts
  (`01_fonti__*.md`, merged into `01_fonti.md`) → analyst (`02_metodo.md`, `03_criteri.md`) →
  critic on the criteria (`03b_critica.md`, at most `--max-critic-rounds` rounds) → **dedicated
  commit of `03_criteri.md`** → implementer (`04_impl/`, `come_eseguire.md`) → the orchestrator runs
  the declared commands (`04_impl/logs/`) → **commit of the raw logs** → validator (`05_verdetto.md`)
  → critic on the verdict (`05b_controverdetto.md`) → final commit.
- **The orchestrator is the only committer**, with fixed commit messages, and prints the order check
  at the end (`03_criteri.md` must be older than anything in `04_impl/`). If the run directory is not
  inside a git repository, one is initialised there; `--no-git` skips git (and loses the proof).
- **Completeness check** on every artifact: the file exists, is not empty, and ends with
  `<!-- FINE DOCUMENTO -->`; line caps (400/500/300) produce a warning.
- **Checkpoint decisions** are appended to `checkpoints.md` in the run (human or, with
  `--unattended`, the coordinator model with its motivation). Raw model replies are kept in
  `<run>/.transcripts/` for inspection; they are not committed and never passed to another role.

How the models write files: they answer with blocks

```
<<<FILE 04_impl/run.py>>>
...content...
<<<END>>>
```

which the orchestrator writes **inside the run directory only** (absolute paths and `..` are
refused), and only where the role is allowed to write (scout: its own `01_fonti__<slug>.md`;
analyst: `02_metodo.md`, `03_criteri.md`; implementer: `04_impl/` but not `04_impl/logs/`;
validator: `05_verdetto.md`). The critic writes nothing: its reply is the document, and the
orchestrator writes it, as the protocol requires.

The validator receives `03_criteri.md`, `come_eseguire.md` and the logs — **not** the implementer's
report.

## Run it

```bash
# Ollama (default endpoint http://localhost:11434)
ollama pull qwen2.5-coder:32b          # any instruction-following model you like
python3 lab.py --problem example-problem.md --model qwen2.5-coder:32b

# vLLM
python3 lab.py --problem example-problem.md --base-url http://localhost:8000 --model <served-name>

# LM Studio (local server)
python3 lab.py --problem example-problem.md --base-url http://localhost:1234 --model <model-id>

# a stronger model for the judgment roles, a smaller one for the scouts, no human at checkpoints
python3 lab.py --problem example-problem.md --model big-model --model-scout small-model --unattended
```

The run is created in `run/<YYYYMMDD>-<slug>/` under the current directory (`--run-dir` to choose).

## Configuration

| Option | Env | Default | Meaning |
|---|---|---|---|
| `--problem FILE` | | required | markdown problem statement, copied verbatim into `00_problema.md` |
| `--base-url URL` | `LAB_BASE_URL` | `http://localhost:11434` | endpoint root; `/v1/chat/completions` is appended (a trailing `/v1` is accepted) |
| `--api-key KEY` | `LAB_API_KEY` | none | sent as `Authorization: Bearer KEY` |
| `--model NAME` | `LAB_MODEL` | none | model for every role, coordinator included |
| `--model-scout`, `--model-analyst`, `--model-critic`, `--model-implementer`, `--model-validator` | | `--model` | per-role override |
| `--run-dir DIR` | | `run/<YYYYMMDD>-<slug>` | must not exist or be empty (no resume) |
| `--scouts N` | | 2 | parallel scouts, 1-4 |
| `--max-critic-rounds N` | | 2 | analyst/critic rounds before checkpoint 2 |
| `--cmd-timeout S` | | 600 | timeout of each command from `come_eseguire.md` |
| `--unattended` | | off | checkpoints decided by the coordinator model instead of `input()` |
| `--no-git` | | off | no commits |

Offline tests of the pure functions (file-block extraction, path refusal, terminator check, command
parsing): `python3 -m unittest -v test_lab_offline`.

## Limits — read before running

- **Not validated.** No round of the bench has been run on this harness.
- **It executes model-written shell commands** on your machine (the `bash` block under
  `## Run the full protocol` in `come_eseguire.md`, from inside `04_impl/`). In attended mode you
  see them at checkpoint 3 and must answer `RUN`; with `--unattended` they run without asking.
  Use a container or a throwaway VM.
- **No tools for the models.** Scouts cannot query OpenAlex/arXiv/Crossref: they catalogue from
  memory and must mark every entry as unverified. The analyst cannot read papers. The implementer
  cannot run its code before delivering, and there is **no fix loop**: if the commands fail, the
  failure is logged and the validator measures that. The validator does not re-execute the protocol:
  the orchestrator runs it once.
- **Simplified coordinator.** Merging of scout files is plain concatenation (no DOI deduplication);
  the number of scouts is fixed by `--scouts`, not chosen by the scaling rule; the completeness check
  is the minimal one (no mtime, pending-label or diff checks); there is no resume of an interrupted run.
- **Context windows.** System prompts are long (the analyst's and the critic's are ~3-4k tokens) and
  documents and logs are inlined (each file truncated at 30,000 characters, logs at 120,000 in
  total). Small default contexts truncate silently: with Ollama, raise the context length
  (e.g. `OLLAMA_CONTEXT_LENGTH=32768`, or `num_ctx` in a Modelfile).
- **No streaming, one retry.** One retry after an HTTP or network error, then a clear failure.
  Each request has a 30-minute timeout.
