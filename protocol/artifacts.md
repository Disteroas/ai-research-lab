# Artifacts of a run

Every run lives in `run/<YYYYMMDD>-<slug>/`. File names are kept in Italian, as in the validated
system, so that runs produced by either harness have the same shape. The full section templates are
in the role files; this page is the index.

**Terminator.** Every markdown document ends with the line

```
<!-- FINE DOCUMENTO -->
```

("end of document"). It is the cheapest signal between "finished" and "interrupted"; it only
covers deaths at the tail, which is why the completeness check also diffs against the last commit
(see [`README.md`](README.md#completeness-check--at-every-delivery)).

| # | Artifact | Written by | Contains | Committed in |
|---|---|---|---|---|
| 0 | `00_problema.md` | coordinator | `Statement` (the human's words, verbatim) · `Questions and answers` · `Boundaries` (in/out) · `Known constraints` · `Stop criteria` | COMMIT 1 |
| 1a | `01_fonti__<direction>.md` | one scout each | direction, queries run, APIs queried · candidates table (title, year, DOI/URL, citations, why relevant) · what was NOT found · queries list | COMMIT 2 |
| 1b | `01_fonti.md` | coordinator | merge of the scout files, deduplicated by DOI | COMMIT 2 |
| 2 | `02_metodo.md` | analyst | in one sentence · how it works · assumptions and validity conditions · parameters table · what is needed to reproduce it · what the paper does NOT say. Cap 400 lines | before or with COMMIT 4 (never in COMMIT 3) |
| 3 | `03_criteri.md` | analyst | optional `FEASIBILITY GATE NOT PASSED` block at the top · experimental protocol (N runs, seeds, all runs reported, statistic) · criteria `C1…` (measure, threshold, passes if, fails if, origin, declared power) · guards with consequences, per arm · frozen aggregation rule (failure directions, load-bearing vs diagnostic, pre-forced outcomes, uncovered profile) · log field schemas · what is NOT measured · how the experiment can fail. Cap 500 lines | **COMMIT 3, dedicated, alone** |
| 3b | `03b_critica.md` | critic (text) → coordinator (file) | overall verdict `ACCEPTABLE` / `TO BE REWRITTEN (n)` · criterion by criterion `OK` / `DEFECTIVE` with fix · missing criteria · the easiest way to cheat | before or with COMMIT 4 |
| 4 | `04_impl/` | implementer | code (deterministic, seed in input), optional venv, `logs/` (one file per run, at least one level below the aggregates) | COMMIT 4 |
| 4a | `04_impl/come_eseguire.md` | implementer | prerequisites · run a single run · run the full protocol · where results go and which field maps to which criterion · choices made · what was NOT implemented. **Commands and schemas, never outcomes** | COMMIT 4 |
| 5 | `05_verdetto.md` | validator | outcome `PASSA` / `NON PASSA` / `INCONCLUSIVO` (+ own label if pre-forced) with "(n of N)" and the aggregation rule applied · protocol executed (N required, M run, seeds) · criterion by criterion with **all** runs and log paths · full runs table · what the criteria did not capture · how to redo the measurement. Cap 300 lines | logs COMMIT, **with `04_impl/logs/`, before the critic** |
| 5b | `05b_controverdetto.md` | critic (text) → coordinator (file) | is the verdict supported? `YES` / `NO` / `PARTIALLY` · spot checks against the logs · discrepancies · what remains unverifiable | COMMIT 5 |
| — | checkpoint decisions | coordinator | at each of the four checkpoints, the decision and its motivation (mandatory in unattended mode). The validated harness writes them in the run's own files; the portable harness writes them to `checkpoints.md` | with the phase they close |

## The order that git must show

```
COMMIT 1  00_problema.md
COMMIT 2  01_fonti__*.md, 01_fonti.md
          02_metodo.md, 03b_critica.md        (may share a commit, never COMMIT 3)
COMMIT 3  03_criteri.md                       ← alone
COMMIT 4  04_impl/ (code, come_eseguire.md)
COMMIT    04_impl/logs/ + 05_verdetto.md      ← before the critic reads them
COMMIT 5  05b_controverdetto.md
```

Check: `git log --diff-filter=A --format='%h %ad %s' --date=short -- "$RUN/03_criteri.md" "$RUN/04_impl"`
must list `03_criteri.md` first; `git log --diff-filter=D -- "$RUN/04_impl/logs/"` must be empty.
