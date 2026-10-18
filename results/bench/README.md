# Bench files (evidence, Italian, sanitized copies)

Sanitized copies (see [SANITIZATION.md](../../SANITIZATION.md)) of the bench's own documents, taken from the bench repository at commit `16dfde6`
(2026-10-18, after round 6 was scored). They are **evidence**, not narrative: everything the English
stories and the top-level README cite lives here, with the line numbers they quote. The files are in
Italian; the stories translate what they quote and say so.

`SHA256SUMS.txt` lists the sha256 of the 23 sanitized copies and of `ROUTE-EXCERPT.md` (24 files). Check them with:

```bash
cd results/bench && shasum -a 256 -c SHA256SUMS.txt
```

Expected: 24 lines, all `OK`.

| File | What it is |
|---|---|
| [`2026-08-10-punteggio-giro2.md`](2026-08-10-punteggio-giro2.md) | round 2 scores (A, B), two-stage |
| [`2026-08-17-mappa-validazione.md`](2026-08-17-mappa-validazione.md) | validation map (what is verified, by which proof, on which system) as of round 4 |
| [`2026-08-17-punteggio-giro3-C.md`](2026-08-17-punteggio-giro3-C.md) | round 3 score (C): fallen oracle |
| [`2026-08-18-punteggio-giro4-E.md`](2026-08-18-punteggio-giro4-E.md) | round 4 score (E): verdict 1/1, path 2/4 |
| [`2026-10-17-FIX17-proposta.md`](2026-10-17-FIX17-proposta.md) | FIX 17 proposal: rules 18-19, self-refutations, inventory, burned cases |
| [`2026-10-17-preregistrazione-giro5.md`](2026-10-17-preregistrazione-giro5.md) | round 5 pre-registration (+ Amendment 1: ablation timing) |
| [`2026-10-17-preregistrazione-giro6.md`](2026-10-17-preregistrazione-giro6.md) | round 6 pre-registration (+ Amendments 1-2: cap, duplicate run) |
| [`2026-10-17-punteggio-ablation-A-primo-peso-condiviso.md`](2026-10-17-punteggio-ablation-A-primo-peso-condiviso.md) | ablation score (single session), two-stage |
| [`2026-10-17-punteggio-ablation-B-primo-momentum-e-rumore.md`](2026-10-17-punteggio-ablation-B-primo-momentum-e-rumore.md) | ablation score (single session), two-stage |
| [`2026-10-17-punteggio-ablation-D-orizzonte-finito.md`](2026-10-17-punteggio-ablation-D-orizzonte-finito.md) | ablation score (single session), two-stage |
| [`2026-10-17-punteggio-ablation-E-primo-premio-di-tappa.md`](2026-10-17-punteggio-ablation-E-primo-premio-di-tappa.md) | ablation score (single session), two-stage |
| [`2026-10-17-punteggio-giro5-A-primo-peso-condiviso.md`](2026-10-17-punteggio-giro5-A-primo-peso-condiviso.md) | round 5 score, two-stage |
| [`2026-10-17-punteggio-giro5-B-primo-momentum-e-rumore.md`](2026-10-17-punteggio-giro5-B-primo-momentum-e-rumore.md) | round 5 score, two-stage |
| [`2026-10-17-punteggio-giro5-D-orizzonte-finito.md`](2026-10-17-punteggio-giro5-D-orizzonte-finito.md) | round 5 score, two-stage |
| [`2026-10-17-punteggio-giro5-E-primo-premio-di-tappa.md`](2026-10-17-punteggio-giro5-E-primo-premio-di-tappa.md) | round 5 score, two-stage |
| [`2026-10-17-punteggio-giro6-A-primo-peso-condiviso.md`](2026-10-17-punteggio-giro6-A-primo-peso-condiviso.md) | round 6 score, two-stage |
| [`2026-10-17-punteggio-giro6-B-primo-momentum-e-rumore.md`](2026-10-17-punteggio-giro6-B-primo-momentum-e-rumore.md) | round 6 score, two-stage |
| [`2026-10-18-punteggio-giro6-D-secondo-tre-vicini.md`](2026-10-18-punteggio-giro6-D-secondo-tre-vicini.md) | round 6 score, two-stage |
| [`2026-10-18-punteggio-giro6-E-secondo-quanto-esplorare.md`](2026-10-18-punteggio-giro6-E-secondo-quanto-esplorare.md) | round 6 score, two-stage |
| [`MANDATO-PUNTEGGIO-ABLATION.md`](MANDATO-PUNTEGGIO-ABLATION.md) | scoring mandate for the single-session ablation |
| [`MANDATO-PUNTEGGIO-GIRO5.md`](MANDATO-PUNTEGGIO-GIRO5.md) | scoring mandate for rounds 5-6 (+ Amendments 1-3) |
| [`ROUTE-EXCERPT.md`](ROUTE-EXCERPT.md) | **not a bench copy**: an English excerpt of the route (goals §1, target sentence §2, the round cap, the passages the stories cite); the full route document is private |
| [`punteggio.md`](punteggio.md) | the two-axis rubric and its amendment history (verdict / path, P1-P4) |
| [`registro.md`](registro.md) | the round register: one row per round (1-6), ablation rows, errata — append-only |

Not copied (bench working files, quoted by the stories where needed): the surveillance diary
(`giro-auto/sorveglianza-diario.txt`), the single-session preamble (quoted in full in the ablation
story), the per-run `stato-`/`log-` files, and everything under `verita/` for cases that are still
sealed. The run repositories (`laboratorio-giro5-*`, `laboratorio-giro6-*`, `ablation-giro5-*`) are
not part of this showcase; the scores quote them.
