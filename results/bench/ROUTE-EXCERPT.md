# The route: an excerpt

**This is not a copy of a bench file.** The bench's route document (`OBIETTIVO-E-ROTTA.md`, written on
2026-08-18 and amended twice on 2026-10-17) fixes the project's goal, the sentence that must be honestly
sayable at the end, the phases and the cap on rounds. The full document is **private**, because it
contains the author's strategy and the author's own words. This file reproduces only what the stories
and [`docs/DETAILS.md`](../../docs/DETAILS.md) cite. Translations are mine; omissions are marked […].
The Italian bench files in this folder still refer to the original by its file name.

## §1. The goals (three)

1. Show a multi-agent framework that works on small experiments, with a three-state verdict
   (`INCONCLUSIVO` included), and that could be extended to a larger scale.
2. Show a way to check with AI what AI produces: the bench, frozen criteria, sealed oracles, the two-axis score.
3. Extract the agents (critic, counter-verdict, validator, the discipline of frozen criteria) for the
   author's real projects, with the author coordinating; the whole lab is not used and stays on display.

## §2. The final sentence

In the original Italian:

> Ho costruito un laboratorio di ricerca multi-agente e, separatamente, il banco per non fidarmene.
> Il banco ha trovato due difetti reali nel laboratorio — un oracolo morto e una guardia che non
> scattava — e li ho riparati. **Una sola versione** del sistema riparato ha poi superato cinque
> profili alla cieca: ha detto sì quando era sì, no quando era no, «non lo so» quando i dati non
> decidevano, si è **fermata** davanti a un braccio rotto in silenzio, e l'ha fatto meglio di una
> sessione singola senza struttura, misurata sugli stessi casi.

Translated:

> I built a multi-agent research lab and, separately, the bench not to trust it. The bench found two
> real defects in the lab — a dead oracle and a guard that did not fire — and I repaired them. **One
> single version** of the repaired system then passed five blind profiles: it said yes when it was yes,
> no when it was no, "I don't know" when the data did not decide, it **stopped** in front of an arm
> broken in silence, and it did so better than a single session without structure, measured on the
> same cases.

**What is not claimed** («Cosa NON si rivendica», §2, written at the same time): that the system scales
to real problems with real data (the bench covers synthetic problems, seconds of compute); that the
ratio of prose to computation survives outside small problems; that the lab serves the author's own
research (it will never touch it).

## The cap on rounds

Amendment 1, point 2 (2026-10-17): if round 5 does not buy the §2 sentence, **one repair round** (round 6), then stop.
Amendment 2 (2026-10-17 evening, round 6 already open, round 6 unchanged): **cap at round 8, stop at the first round that buys the sentence**.

## Other passages cited

- **§4, Phase 3** (new sealed cases E′, A′, B′), on E′: "The break stays in the specification, not in a bug."
- **§4, Phase 5** (ablation): the question is how much the six-role machine adds over a single careful
  agent, "the most important missing experiment, and it is cheap"; and "if the single session draws
  level, it is a result that goes in the showcase all the same — the cost of the structure is part of
  the story".
- **§7, progress log** (append-only; line numbers are those of the private original):
  - line 244, 2026-08-18, phase 2 closed: "FIX 16 in the lab's CLAUDE.md (rules 12-17, commit 7598fa5)" […]
  - line 246, 2026-10-17, phase 3, sealed answers complete: A′ and B′ "written by two isolated Opus
    agents", `CALIBRAZIONE OK` committed (7cc34f7, 2d22d4d) […]
  - line 249, 2026-10-17, phase 5 closed (ablation on the round-5 cases): "single session verdict 3/4 ·
    path 10/16 in ≈17 min, against lab 2/4 · 15/16 in ≈2 h 41 min. The structure buys the path (power,
    gates, counter-verdict), not the verdict; on D the single session titles INCONCLUSIVO for the right
    reason and the lab does not." […] "FIX 17 installed in the lab (128634d, rules 18-19 + critic row),
    snapshot 2026-10-17-giro6, round-6 repos seeded" […]
  - line 250, 2026-10-17, erratum to the phase-5 row: "the lab's time is ≈ 3 h 21 min, not 2 h 41
    (wrong sum by the main session)" […]
  - line 251, 2026-10-18, round 6 closed, "§2 sentence BOUGHT": "verdict 4/4, path 16/16 (substantive
    reading; strict 10/16, `<domanda aperta 7>`)" […] "The cap at round 8 (Amendment 2) was not needed."
