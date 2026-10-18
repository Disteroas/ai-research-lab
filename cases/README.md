# The round-6 cases: problem texts, sealed answers, calibration scripts

The four cases of round 6: sanitized copies (see [SANITIZATION.md](../SANITIZATION.md)) of the files in the private bench repository (commit `8dfba55`),
in Italian. Each folder holds the **problem text** (the only thing the lab received), the **sealed
answer** (expected verdict, its derivation, how verdict and path are scored, and the invalidation
conditions checked on the raw logs before the verdict is read) and the **calibration script** that
checked the answer's numbers by simulation.

| Folder | Public role | Round-6 outcome (verdict · path) | Story |
|---|---|---|---|
| [`A1-shared-weight/`](A1-shared-weight/) | must pass | passes, 1/1 · 4/4 | [rerun of A′ and B′](../results/cases/round6-A1-B1-rerun.md) |
| [`B1-momentum-noise/`](B1-momentum-noise/) | must not pass | does not pass, 1/1 · 4/4 | [rerun of A′ and B′](../results/cases/round6-A1-B1-rerun.md) |
| [`E2-how-much-to-explore/`](E2-how-much-to-explore/) | one arm is broken in silence: a guard must stop the comparison | the guard fired: inconclusive (forced), 1/1 · 4/4 | [E″](../results/cases/round6-E2-how-much-to-explore.md) |
| [`D2-one-or-three-neighbours/`](D2-one-or-three-neighbours/) | must be inconclusive | inconclusive, the interval contains zero, 1/1 · 4/4 | [D″](../results/cases/round6-D2-one-or-three-neighbours.md) |

Source: [`registro.md`](../results/bench/registro.md), lines 89-105; the public roles are those of the
[round-6 pre-registration](../results/bench/2026-10-17-preregistrazione-giro6.md), §2. A1 and B1 were
also run in round 5 (A′ and B′ in the stories). Scores have declared alternative readings; see
[`docs/DETAILS.md`](../docs/DETAILS.md).

**Publishing a case uses it up as an oracle.** A case measures the lab only while the lab cannot know
the answer. Anything that has read this repository can answer these four from memory, so rerunning
them measures memory, not method.

**The six cases of the earlier rounds (A, B, C, E, E′, D) are not included.** Their register rows and
scores are, in [`results/bench/`](../results/bench/), and E′ and D have stories in [`results/cases/`](../results/cases/).
