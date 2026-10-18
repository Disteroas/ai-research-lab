# The protocol

A research lab made of agents: you hand it a problem, and it carries it from "question" to
"validated result" — or to an honest "cannot measure" / "does not decide".

This directory describes the protocol **independently of any agent harness**. The reference
implementation, the one the benchmark numbers were measured on, is in
[`../harness/claude-code/`](../harness/claude-code/) (Italian; sanitized copies of the validated files, see [SANITIZATION.md](../SANITIZATION.md)).
A portable, unvalidated orchestrator is in [`../harness/openai-compatible/`](../harness/openai-compatible/).

| File | Content |
|---|---|
| [`roles/`](roles/) | the six role mandates (scout, analyst, critic, implementer, validator, coordinator) |
| [`rules.md`](rules.md) | the 19 numbered rules learned from real runs, each with its "why" |
| [`artifacts.md`](artifacts.md) | the schema of every artifact in a run |
| [`bench-method.md`](bench-method.md) | how the protocol itself is tested: sealed oracles, blind runs, two-axis rubric |

---

## The failure this protocol exists to prevent

Systems of this family have a **measured** failure mode. [Science](https://www.science.org/content/article/ai-agents-may-be-skilled-researchers-not-always-honest-ones)
reports that both [Agent Laboratory](https://arxiv.org/pdf/2501.04227) and AI Scientist v2
committed unacceptable acts in research: **inventing data** and **p-hacking** (repeating an
experiment and reporting only the best result).

Two distinct failures, two distinct structural defences:

| Failure | Cause | Structural defence |
|---|---|---|
| **p-hacking** | criteria chosen after seeing the results, or criteria that cannot fail | criteria **frozen before** implementation, with number of runs and seeds declared, vetted by the critic |
| **invented data** | whoever produces the result also narrates it | an **independent validator**, then a **counter-verdict** that rereads the raw logs |

Agent Laboratory has no independent validator: the *professor* writes the report on its
colleagues' results. Here that role is separated by construction.

## Shape: fan-out only in research, then a sequential chain

Multi-agent setups win on broad research along independent directions (the author's notes attribute a
large gain to parallel fan-out in broad research; the figure is not reproduced here) and **lose** on tasks with shared context and dense dependencies —
"like most coding". Analysis, implementation and validation are the second kind: **one agent at a time**.

```
problem
   │
   ├── scout ×1-4  (parallel — the only breadth-first phase)
   │      ↓ CHECKPOINT 1: the human chooses the sources
   ├── analyst     → 02_metodo.md + 03_criteri.md
   ├── critic (1)  → 03b_critica.md   "can this criterion fail? can it pass?"
   │      ↓ CHECKPOINT 2: the human FREEZES the criteria   ← dedicated commit
   ├── implementer → 04_impl/
   │      ↓ CHECKPOINT 3
   ├── validator   → 05_verdetto.md
   ├── critic (2)  → 05b_controverdetto.md   "do the raw logs support the verdict?"
   │      ↓ CHECKPOINT 4: outcome
   └── (optional) archive note, outside the protocol
```

## The six figures and their boundaries

| Figure | Instances | Model tier | Boundary |
|---|---|---|---|
| [Coordinator](roles/coordinator.md) | one (the session itself) | strong | Talks to the human, delegates, holds the checkpoints, **only committer**. **Never fetches content** (no papers, no pages, does not run the implementation) |
| [Scout](roles/scout.md) | 1-4, parallel | fast/cheap | Searches and catalogues. **Does not read full texts**, does not judge methods |
| [Analyst](roles/analyst.md) | one | strong | Reads in depth. Produces the method **and** falsifiable criteria. Writes no code |
| [Critic](roles/critic.md) | one, invoked twice | strong | Only criticises. **Read-only: does not write files, rewrite code or produce results** |
| [Implementer](roles/implementer.md) | one | strong | Writes **only** inside `04_impl/`. Never touches the criteria |
| [Validator](roles/validator.md) | one | strong | Measures against the frozen criteria. **Does not read the implementer's report or tests** |

Model allocation in the validated configuration: the strongest model where there is judgment
(analyst, critic, implementer, validator, coordinator), a faster one on the scouts, which do
extraction in parallel.

Workers **write to the filesystem and return only lightweight references** to the coordinator,
never the content. This avoids information loss and token overhead, and makes every artifact a
**resume checkpoint**: an interrupted run restarts from the last file written.

## The four checkpoints

1. **After the scouts** — the human chooses which candidate sources the analyst reads. The
   coordinator presents them in a compact table and does not choose.
2. **After analysis and critique** — the human **freezes** the criteria. The most important of the
   four. Immediately followed by the dedicated criteria commit. From here on nobody touches them.
3. **After implementation** — what was implemented, what was not, the non-obvious choices.
4. **After verdict and counter-verdict** — the outcome. Discrepancies found by the counter-verdict
   go to the human **unfiltered**.

At each checkpoint: present the **outcome, not the process**; one question with one
recommendation, not a menu; if something went wrong, say it **now**, when correcting it is cheapest.

In unattended mode (no human available) the coordinator decides at each checkpoint, writes the
decision and its motivation into the run, and continues. Nothing else changes.

## The artifact chain

`run/<YYYYMMDD>-<slug>/`

```
00_problema.md        coordinator   problem, questions, answers, boundaries, stop criteria
01_fonti__<dir>.md    each scout    one file per scout (parallel writers never share a file)
01_fonti.md           coordinator   merge of the scout files, deduplicated by DOI
02_metodo.md          analyst       the method, reproducible without reading the papers
03_criteri.md         analyst       falsifiable criteria + frozen aggregation rule
03b_critica.md        critic        "can it fail? can it pass?" (the coordinator writes the file)
04_impl/              implementer   code + come_eseguire.md; logs/ filled by the runs
05_verdetto.md        validator     per criterion: expected, measured, outcome. ALL runs
05b_controverdetto.md critic        do the raw logs support the verdict? (coordinator writes it)
```

File names stay in Italian, as in the validated system. Full schemas: [`artifacts.md`](artifacts.md).

## Non-negotiable rules

1. **Criteria frozen in a dedicated commit before `04_impl/`.** If `03_criteri.md` is not committed
   **before** the first commit touching `04_impl/`, the run is **invalid**. This is not a convention:
   it is checkable with
   `git log --diff-filter=A --format='%h %ad %s' --date=short -- "$RUN/03_criteri.md" "$RUN/04_impl"`
   (`03_criteri.md` must appear first). The commit contains `03_criteri.md` and nothing else, so the
   order reads at a glance.
2. **Raw logs committed before the counter-verdict.** As soon as the validator finishes, logs and
   verdict are committed together, before the critic is invoked. A verdict built on the best run is
   exposed two ways: a short table, and logs that contradict it. The first is dodged by lengthening
   the table; the second only by **deleting the inconvenient logs** — and after the commit every
   deletion is visible in `git log --diff-filter=D`. The same pair of commits also proves
   reproducibility: `git diff <implementation commit> <logs commit> -- "$RUN/04_impl/logs/"`.
3. **One committer: the coordinator**, and only at checkpoints. Workers get no git permissions and
   never touch the index: with parallel scouts there would be several writers on one index.
4. **The critic does not write.** Read-only access. It returns its text; the coordinator writes
   `03b_critica.md` and `05b_controverdetto.md`. A critic that produces becomes an interested party.
5. **The validator does not read the implementer's report** (nor its tests or reasoning notes). It
   reads the frozen criteria and `come_eseguire.md`; it may read code only to know how to run it or
   where a number ends up. A test written by the implementer measures what was implemented, not
   what the criteria asked.
6. **Criteria are not touched after the freeze.** If they must change, a new run is opened that cites
   the old one. If the implementer reports a criterion as impossible, it goes to the human at the
   checkpoint, unmodified: a criterion changed by whoever must satisfy it is no longer a criterion.
7. **The validator reports all runs**, never the best one, and never deletes a log file.
8. **Counter-verdict discrepancies are not "fixed" by re-measuring.** Asking the validator to redo
   the measurement until it matches is exactly the mechanism that produces p-hacking.
9. **Scouts: at most 4.** Scaling rule — a single obvious direction: 1; a comparison of known
   approaches: 2-3; open research with truly independent directions: 4; seems to need more: ask the
   human. Four scouts on a simple problem is a coordination error, not zeal.
10. **The critic loop on the criteria has at most two rounds.** If after that the criteria still do
    not hold, the problem goes to the human: it signals an ill-posed problem, not the need for
    another round.

## The feasibility gate

Between analysis and implementation the lab must answer by itself: **"what do we measure success
with, and do we have it on this machine?"**

If the criteria need a simulator, a dataset or hardware that is not available, the analyst opens
`03_criteri.md` with a `FEASIBILITY GATE NOT PASSED` block (what is missing, the evidence, the
options) and the run **stops there**. Stopping at the gate is a **successful** outcome: it is the
lab recognising that it cannot measure, instead of producing unmeasurable code — the most expensive
way of discovering the same thing.

## The verdict has three states

`PASSA` (passes), `NON PASSA` (does not pass), **`INCONCLUSIVO`** (inconclusive). Without the third,
"the experiment does not decide" always comes out as "does not pass" — a claim about the hypothesis
made without support. The verdict labels stay in Italian, as in the validated system.

The overall verdict is **not** a count of criteria: it applies the **aggregation rule frozen in
`03_criteri.md`**. If that rule is missing, the validator reports the count and does not title.
An outcome forced by arithmetic rather than by measurement gets its own label
(`NON PASSA (forzato)` — the run measures the bench, not the hypothesis), and the title carries
its qualifiers instead of leaving them to the body.

## Line caps

| Artifact | Cap |
|---|---|
| `02_metodo.md` | 400 lines |
| `03_criteri.md` | 500 lines |
| `05_verdetto.md` | 300 lines |

Measured with `wc -l` at delivery. An undeclared overflow goes back to the agent; one declared at
the top of the document is accepted and recorded. The cap is not aesthetics: in one early run,
4,095 lines of prose for 9.17 s of computation produced an analyst that died mid-document, two
false statements in a verdict nobody reread, and a contradiction between line 17 and line 307 of
the same file. What the cap must never compress: the falsifiability arguments and the failure
directions.

## Completeness check — at every delivery

**A file's existence is not its completeness.** A worker can die mid-write without its last
message saying so. Before accepting an artifact, four mechanical checks:

1. **mtime** — every declared file is newer than the worker's invocation.
2. **terminator** — every document ends with its closing line `<!-- FINE DOCUMENTO -->`
   (Italian for "end of document"; kept verbatim from the validated system).
3. **pending labels** — every label cited (`C3`, `G7`, …) is defined in the same document.
4. **consistency with the previous commit** — `git diff` of the file: did it grow while the tail
   stayed identical? A terminator inherited from a previous version proves nothing when the death
   happened mid-document. This check exists because checks 2 and 3 once **both passed** on a file
   whose middle had been half-rewritten.

If a check fails, do not try to resume the dead worker: start a fresh one that rereads from disk.
That works because every artifact lives on the filesystem.

## Resuming an interrupted run

The artifacts **are** the checkpoints. Look at which files exist in the run directory and restart
from the phase after the last one written. Do not start from scratch.

## Guardrails

- At most 4 scouts; beyond that, ask.
- One committer, only at checkpoints.
- The implementer writes only inside `04_impl/` — never in the user's own research code, never in
  personal notes.
- No agent touches the human's personal knowledge base.
- Heuristics, not rigid rules: start from short broad queries, then narrow; prefer authoritative
  sources (the bias of search agents towards SEO content is documented).

## Verifying the lab itself

**Every defence must be seen failing at least once**, otherwise it has been installed, not verified:

1. Break the implementation on purpose → the validator must notice.
2. Submit a non-falsifiable criterion (e.g. "the code runs without errors") → the critic must reject it.
3. Produce a verdict on one run when the criteria asked for N → the counter-verdict must flag it.
4. On a trivial problem, the coordinator must launch 1 scout, not 4.

The systematic version of this is the bench: [`bench-method.md`](bench-method.md).
