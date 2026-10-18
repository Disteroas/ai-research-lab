# Sanitization

The files in this repository come from the author's private workspace: the lab's definitions and
scripts, the bench's records, the round-6 cases. Before publication every tracked file was sanitized:
whatever belonged to the author's own setup (the layout of the workspace, absolute paths, the name of
the author's note system and of its files, the names of plugins and hooks, the time zone, the git
handle, private documents) was replaced by a placeholder or removed. Nothing else was changed: no rule,
threshold, number, verdict or score. The Italian files were edited only by string substitution, line
by line, so **every line number quoted by the stories and by [`docs/DETAILS.md`](docs/DETAILS.md) still
points to the same line**.

## The shipped copies are not byte-identical to the originals

Because of these substitutions, the shipped copies are **no longer byte-identical** to the originals
in the bench. The three `SHA256SUMS.txt` files of this repository
([`results/bench/`](results/bench/SHA256SUMS.txt), [`harness/claude-code/`](harness/claude-code/SHA256SUMS.txt),
[`harness/claude-code/giro6/`](harness/claude-code/giro6/SHA256SUMS.txt)) list the sha256 of the
**sanitized copies**. The sha256 values quoted inside the bench files, the register and the
pre-registrations (for example the rules-file prefixes `f50666f66633d9b9…` and `8dfe7fcb7696381e…`)
identify the **validated originals**; those originals and their full sha256 stay in the author's
private bench repository.

Tracked files that do not appear in the table below were not modified: among them the four case
statements (`cases/*/…-*.md` other than the sealed answers), the four calibration scripts,
`agents/lab-critic.md`, `giro6/agents/lab-critic.md`, `agents/lab-validatore.md`, `protocol/` except
its README, and the OpenAI-compatible harness.

## Substitution rules applied

The original strings are deliberately not repeated here. Placeholders are the same in Italian and
English text unless noted.

| Rule | What was replaced | Replacement |
|---|---|---|
| R1 | absolute and relative paths of the author's workspace (home-directory paths of the workspace root, its tools category folder and its archive folder), in prose, code blocks and scripts | `<workspace>/` (`<workspace>` when it stood alone). Names of the lab, bench and run repositories (`laboratorio`, `banco-laboratorio`, `laboratorio-giro5-A1`, `ablation-giro5-*`, …) were kept |
| R2 | the name of the author's note system, its folders, index pages and project-note paths | `<note dell'autore>` in Italian text (articles adjusted: «nelle», «delle», «le …»), `<author's notes>` in English text; «indici» for the index pages |
| R2 | the author's open-questions file (any path or form of its name) | `<open-questions file>` |
| R2 | the entries of that file, keyed by a bracketed tag with a number | `<domanda aperta n>`, number kept (entry 7 → `<domanda aperta 7>`) |
| R2 | the name of the author's notes-updating agent | «l'agente che aggiorna le note» (Italian), "the notes-updating agent" (English) |
| R3 | names of plugins installed on the author's machine (three names, five substitutions) | `` `<plugin>` `` |
| R4 | the time zone and clock time in a quoted quota message | «resets at `<time>`» |
| R5 | the author's git handle in commit-attribution tables | `` `<autore>` `` |
| R6 | the private route document: deleted and replaced by [`results/bench/ROUTE-EXCERPT.md`](results/bench/ROUTE-EXCERPT.md); every link and `[ROUTE]` key pointing to it now points to the excerpt; one phrase naming the author's research tool generalized; the private publication-gate document untracked (kept on disk, listed in `.gitignore`) and its link replaced by a one-line note in `docs/DETAILS.md` | — |
| R7 | statements that the shipped files are byte-for-byte or identical copies (READMEs, `docs/DETAILS.md`, stories) | "sanitized copies (see SANITIZATION.md)"; the harness README section on the differences from the validated files rewritten accordingly |

Hook-key lists and the sha256 of the user-level CLAUDE.md were also in scope (placeholders `<hooks>`,
`<sha>`), but no tracked file contained them.

## Files deleted, created, untracked

- Deleted: `results/bench/OBIETTIVO-E-ROTTA.md` (the route; private).
- Created: `results/bench/ROUTE-EXCERPT.md` (English excerpt), `SANITIZATION.md` (this file), `.gitignore`.
- Untracked, kept on the author's disk: `PUBBLICAZIONE.md` (the publication gate's criteria and verdict).
- Regenerated: the three `SHA256SUMS.txt` files. `results/bench/SHA256SUMS.txt` now lists the 23
  sanitized bench copies plus `ROUTE-EXCERPT.md` (24 lines).

## Files touched, with the number of substitutions

Counts are substitutions, per rule. R6 and R7 count edited link targets and sentences.

| File | R1 | R2 | R3 | R4 | R5 | R6 | R7 | Total |
|---|---|---|---|---|---|---|---|---|
| `README.md` |  |  |  |  |  |  | 1 | 1 |
| `cases/A1-shared-weight/A-primo.md` | 1 | 3 |  |  |  |  |  | 4 |
| `cases/B1-momentum-noise/B-primo.md` | 2 | 3 |  |  |  |  |  | 5 |
| `cases/D2-one-or-three-neighbours/D-secondo.md` | 3 | 1 |  |  |  |  |  | 4 |
| `cases/E2-how-much-to-explore/E-secondo.md` | 2 | 1 |  |  |  |  |  | 3 |
| `cases/README.md` |  |  |  |  |  |  | 1 | 1 |
| `docs/DETAILS.md` |  | 3 |  |  |  | 15 | 10 | 28 |
| `harness/claude-code/CLAUDE.md` |  | 7 | 1 |  |  |  |  | 8 |
| `harness/claude-code/README.md` |  | 1 |  |  |  |  | 7 | 8 |
| `harness/claude-code/agents/lab-analista.md` |  | 1 |  |  |  |  |  | 1 |
| `harness/claude-code/agents/lab-implementatore.md` |  | 2 |  |  |  |  |  | 2 |
| `harness/claude-code/agents/lab-scout.md` |  | 1 |  |  |  |  |  | 1 |
| `harness/claude-code/giro6/CLAUDE.md` |  | 7 | 1 |  |  |  |  | 8 |
| `harness/claude-code/scripts/README.md` | 1 |  |  |  |  |  | 3 | 4 |
| `harness/claude-code/scripts/istantanea.sh` | 5 |  |  |  |  |  |  | 5 |
| `harness/claude-code/scripts/sorveglia.sh` | 9 |  |  |  |  |  |  | 9 |
| `harness/claude-code/scripts/stacca.sh` | 11 | 1 |  |  |  |  |  | 12 |
| `harness/claude-code/scripts/verifica-sistema.sh` | 5 | 2 |  |  |  |  |  | 7 |
| `harness/claude-code/skills/laboratorio/SKILL.md` |  | 6 | 1 |  |  |  |  | 7 |
| `protocol/README.md` |  |  |  |  |  |  | 1 | 1 |
| `results/bench/2026-08-10-punteggio-giro2.md` |  | 3 |  |  |  |  |  | 3 |
| `results/bench/2026-08-17-mappa-validazione.md` | 5 | 1 |  |  |  |  |  | 6 |
| `results/bench/2026-08-17-punteggio-giro3-C.md` | 1 | 4 |  |  |  |  |  | 5 |
| `results/bench/2026-08-18-punteggio-giro4-E.md` | 1 | 6 | 1 |  |  |  |  | 8 |
| `results/bench/2026-10-17-FIX17-proposta.md` | 5 | 7 |  |  |  |  |  | 12 |
| `results/bench/2026-10-17-preregistrazione-giro5.md` | 8 | 3 |  |  |  |  |  | 11 |
| `results/bench/2026-10-17-preregistrazione-giro6.md` |  | 3 |  |  |  |  |  | 3 |
| `results/bench/2026-10-17-punteggio-ablation-A-primo-peso-condiviso.md` | 1 | 1 |  |  | 1 |  |  | 3 |
| `results/bench/2026-10-17-punteggio-ablation-B-primo-momentum-e-rumore.md` | 1 | 1 |  |  | 1 |  |  | 3 |
| `results/bench/2026-10-17-punteggio-ablation-D-orizzonte-finito.md` | 1 |  |  |  | 1 |  |  | 2 |
| `results/bench/2026-10-17-punteggio-ablation-E-primo-premio-di-tappa.md` | 1 |  |  |  | 1 |  |  | 2 |
| `results/bench/2026-10-17-punteggio-giro5-A-primo-peso-condiviso.md` | 1 | 4 |  |  |  |  |  | 5 |
| `results/bench/2026-10-17-punteggio-giro5-B-primo-momentum-e-rumore.md` | 1 | 2 |  |  | 2 |  |  | 5 |
| `results/bench/2026-10-17-punteggio-giro5-D-orizzonte-finito.md` | 3 | 3 |  |  |  |  |  | 6 |
| `results/bench/2026-10-17-punteggio-giro5-E-primo-premio-di-tappa.md` | 1 | 2 |  |  |  |  |  | 3 |
| `results/bench/2026-10-17-punteggio-giro6-A-primo-peso-condiviso.md` | 1 | 4 |  | 1 |  |  |  | 6 |
| `results/bench/2026-10-17-punteggio-giro6-B-primo-momentum-e-rumore.md` | 1 | 11 |  |  |  |  |  | 12 |
| `results/bench/2026-10-18-punteggio-giro6-D-secondo-tre-vicini.md` | 1 | 5 |  |  |  |  |  | 6 |
| `results/bench/2026-10-18-punteggio-giro6-E-secondo-quanto-esplorare.md` | 1 | 2 |  |  |  |  |  | 3 |
| `results/bench/MANDATO-PUNTEGGIO-ABLATION.md` | 2 |  |  |  |  |  |  | 2 |
| `results/bench/MANDATO-PUNTEGGIO-GIRO5.md` | 1 | 1 |  |  |  |  |  | 2 |
| `results/bench/README.md` |  |  |  |  |  | 1 | 3 | 4 |
| `results/bench/punteggio.md` |  | 1 |  |  |  |  |  | 1 |
| `results/bench/registro.md` | 6 | 32 | 1 |  |  |  |  | 39 |
| `results/cases/round5-A1-shared-weight.md` | 1 |  |  |  |  | 2 | 1 | 4 |
| `results/cases/round5-B1-momentum-noise.md` | 1 |  |  |  |  | 2 | 1 | 4 |
| `results/cases/round5-D-finite-horizon.md` | 1 | 1 |  |  |  | 2 | 1 | 5 |
| `results/cases/round5-E1-waypoint-reward.md` | 1 |  |  |  |  | 2 | 1 | 4 |
| `results/cases/round6-A1-B1-rerun.md` | 1 | 1 |  |  |  |  | 1 | 3 |
| `results/cases/round6-D2-one-or-three-neighbours.md` | 1 | 1 |  |  |  |  | 1 | 3 |
| `results/cases/round6-E2-how-much-to-explore.md` | 1 | 2 |  |  |  | 2 | 1 | 6 |
| `results/round5-ablation-single-session.md` | 2 |  |  |  |  | 2 | 1 | 5 |
| **Total** | 91 | 140 | 5 | 1 | 6 | 28 | 34 | **305** |

## Left as is, on purpose

- The Italian bench files still mention the route by its original file name and cite other bench
  working files that are not shipped (as they did before); those references are not links.
- Two quotations of the author's own working rules stay in the bench files, because they are evidence
  for a measured effect or part of the lab's design: the rule that only the user launches runs (from
  which the lab's rules file declares an explicit exemption) and, in the round-4 score, a style rule on
  writing explanations in full, cited as a cause of a line-cap overrun.
- Where a sentence contrasted an old and a new path of the same file, both now read `<workspace>/…`.
- The scripts keep running syntax (`bash -n` passes), but `<workspace>` is a literal placeholder: the
  paths must be adapted before use, as [`harness/claude-code/scripts/README.md`](harness/claude-code/scripts/README.md) says.
