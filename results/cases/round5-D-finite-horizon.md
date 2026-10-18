# Round 5, case D — the finite horizon

| | |
|---|---|
| **Round** | 5 (fourth and last of four blind cases, run on 2026-10-17) |
| **Case role** (public, from the pre-registration) | must give `INCONCLUSIVO` (inconclusive), for the reason the sealed answer expects |
| **Verdict axis** | **0 / 1**: the lab titled `PASSA` (passes) with the answer "equivalent within δ = 27.86". 1 / 1 under one declared lenient reading |
| **Path axis** | **4 / 4**: 3 / 4 under any one of the declared strict readings, 1 / 4 under all of them |
| **Acceptance rule for this case** | **not met** (§3.2 item 4). The third state of the verdict has still never been shown on a valid oracle |
| **Run duration** | ≈ 75 min of work (15:18:01 → 15:34:16, then 17:12:00 → 18:11:06); 2 h 53 min wall-clock, of which 1 h 38 min waiting for the usage limit |
| **Relaunches** | 6 automatic (1 started and died on the usage limit, 5 refused at the model pre-flight) + 1 manual, at 17:12 |
| **System check** | `SISTEMA INVARIATO` (system unchanged) at start, at the resume (pre-flight of 17:12:00) and at end |
| **Model** | `claude-opus-5-5` (Opus 5.5), one co-author trailer on all 7 run commits |
| **Human attention on content** | 0 min |

Sources for the table: [REG-D]; [SCORE] §2, §2.1, §11, §12 and §13; [PRE] §2 and §3.2. All source
keys are listed at the end. The source files are in Italian; quotations are my translation. Numbers
are copied as written, with the decimal comma turned into a point; where I round, subtract or sum,
I say so.

This case was built so that the right answer is "I don't know". The lab worked out, before measuring,
that the question sits exactly where the data cannot decide. Then it gave "I don't know" the name of an
answer and titled it a pass. The failure is in one label. The body of the verdict has the right
diagnosis.

---

## The problem in three lines

A slot machine with 10 arms, each paying 1 with a fixed probability; arm 0 is the best (0.8). Two
classic strategies decide which arm to pull next: UCB1, which pulls the arm with the best optimistic
estimate, and ε-greedy, which mostly pulls the best-looking arm and explores at random with a
probability that shrinks as $236/t$. Theory puts both in the same class: the total cost of not always
pulling the best arm ("regret") grows like $\log T$. The question put to the lab: *on this machine, after
$T = 100\,000$ pulls, which of the two has the lower expected regret?* ([00] «Enunciato»).

Why it is hard to answer honestly: the asymptotic class says nothing about the constants, and at a
fixed horizon the constants decide. Here they were chosen to come out almost equal. With 30 seeds the
difference is inside the noise. A lab that always produces an answer will produce one here too. The case
role in the pre-registration is to give `INCONCLUSIVO`, and only for the reason the sealed answer
expects ([PRE] §2 and §3.2 item 4).

The case is older than the round. Its sealed answer is the only one on the bench that stayed sealed
from 2026-08-11 to this round; this scoring session was the first to open it ([SCORE], opening lines).
The bench put D last in the order of launch because it was "the only old oracle still blind and the
most expensive to replace" ([PRE] §2).

## What the machine did

### A run interrupted by the usage limit

D is the only run of the round with a story about the environment. The other three cases finished
with no relaunches between 13:07 and 15:17 ([REG-R5]). D's monitor started at 15:18:07. The problem
statement was committed at 15:19:12 and the sources at 15:21:23 ([DIARY]; [GIT]). Then the account's
usage limit hit. The monitor logged at 15:32:08 "stopped without counter-verdict, relaunch no. 1", and
at 15:34:16 "dead from usage limit, retry in 30 min" ([DIARY]).

Relaunches no. 2 to 6 (16:04, 16:20, 16:36, 16:52, 17:08) all ended with "relaunch FAILED (pre-flight
or other)" ([DIARY]). The pre-flight is the launcher's check that the pinned model answers before a run
starts. During the limit it refused, so none of these five relaunches got as far as starting a run.
At 17:12 the main session relaunched the case by hand, with the same prompt (sha256 `eb1c2f74165bffdb…`,
the one in the pre-registration). The diary does not record the manual relaunch. The scorer confirmed
it from two file timestamps: the system-check file at 17:12:00 and the console file at 17:11:59. The
pre-flight of the resume says `SISTEMA INVARIATO` ([SCORE] §2, §2.1 and §13).

The resumed coordinator continued the same run directory. It did not open a second one: there is
exactly one `run/20261017-*` folder ([SCORE] §2). It started again from the analysis. Of the first life
(15:19–15:34) only the problem file and the sources survive. The method, the critique and the criteria
were all born on disk after the resume, from 17:40:37 on ([SCORE] §2). So the criteria the run was
judged by were written entirely after the interruption. They were committed once (`506f0db`, 17:50:53),
before the first code (`e37ed82`, 17:54:32). The validation was committed at 18:02:28 and the
counter-verdict at 18:10:49 ([GIT]). The run ended at 18:11:06 ([SCORE] §2).

The scorer's accounting: 16 min 15 s before the limit plus 59 min 06 s after it, ≈ 75 min of work;
2 h 53 min wall-clock, with 1 h 38 min of waiting; 3.34 s of compute ([SCORE] §13). The pre-registration
amendment written the same day speaks of the limit stopping D "for 97 minutes" ([PRE] Emendamento 1).
From 15:34:16 to 17:12:00 is 97 min 44 s (my subtraction), so the two figures are the same interval
rounded differently.

### The analysis

Two scouts searched the theory and the empirical comparisons, and found 17 distinct candidate sources
([01] opening line). The analyst read the main paper (Auer, Cesa-Bianchi and Fischer, 2002) in full and
derived a closed-form prediction for each strategy before any simulation ([02], header and «Previsione
teorica»):

- ε-greedy: ≈ 567, band [557, 600];
- UCB1: ≈ 555.6 from a fixed-point estimate, ≈ 573 with a convexity correction;
- the difference $E[D] = E[R_U] - E[R_\varepsilon]$: between about −11 and +6, inside a band of
  [−128, +110]. "Theory does not predict the direction" ([02] «Previsione sulla domanda»).

It also noticed why. The two predictions almost coincide over the whole last decade of the horizon:
372.6 against 375.1 at $10^4$ pulls, 555.6 against 557.1 at $10^5$. Its sentence, written before the
measurement:

> The question sits exactly where the constants are equal.

([02] «Previsione sulla domanda».) That is the diagnosis the case was built to elicit.

### The criteria, and the critique

The main criterion, C1, builds a 95 % confidence interval on the paired difference $D_s$ over 30 seeds
and reads it in four regions ([03] C1):

- **U**: the interval is below zero, so UCB1 has lower regret;
- **E**: the interval is above zero, so ε-greedy has lower regret;
- **Q**: the interval contains zero and lies inside $(-\delta, +\delta)$: "equivalent within δ";
- **N**: the interval contains zero and does not lie inside $(-\delta, +\delta)$: "not resolved".

The margin δ = 27.857 is 5 % of the exact expected exploration regret of ε-greedy, "the only exact
number available before measuring: differences below 5 % of the regret are declared practically
irrelevant". Its origin is written next to it: "**analyst's choice**, no source" ([03] C1, «Origine di
δ»).

Two rounds of critique followed. Round 1 ended `DA RISCRIVERE` (to be rewritten) with two blocking
findings. The second was a real hole: a tie-break tolerance that would have let a wrong implementation
pass the replay guard. The first is the one this story is about. The first draft titled Q as `NON PASSA`
(does not pass), against a hypothesis "the regrets are different". The critic blocked it, with three
reasons. A point hypothesis "different" is true a priori and Q does not refute it. Q is the most likely
outcome. And the reader of the <author's notes> would read `NON PASSA` as "the experiment failed" when it confirms
the analyst's central prediction: "D1 says explicitly that 'not distinguishable' is not a failure". Its
recommended rewrite titles every outcome with the **answer**, and maps Q to
`PASSA — risposta: equivalenti entro δ = 27,86` ([03b] giro 1, R1). Round 2 ended
`APPROVABILE CON RILIEVI` (approvable with findings), with no blocking finding ([03b] giro 2).

The same critic also wrote, as a non-blocking finding, that δ "moves the title between Q and N, and moves
it a lot". At a true difference of zero, with the expected spread, Q comes out with probability 0.385 if
δ = 20, 0.745 if δ = 25, **0.867** if δ = 27.86, 0.924 if δ = 30. The frozen document carries the
sentence: "at zero effect, the Q/N boundary depends on δ more than on the data" ([03b] giro 1, R3;
[03] C1).

### The measurement

The bench ran the 60 runs in 3.34 s ([05] G9). The validator replayed all 60 from the specification
alone and matched every action and every reward ([05] G3). All nine guards passed. Two of them apply to one strategy each, by design, with the gap
covered by another guard ([05] «Guardie»; [SCORE] §4). Then the main criterion ([05] C1 and «Tabella completa dei run»; [SCORE] §2-bis):

- UCB1: mean regret 547.43, sd 39.80. ε-greedy: 555.69, sd 12.74.
- $\bar D = -8.25$, interval **[−24.22; 7.72]**. It contains zero. UCB1 was lower on 16 seeds and
  ε-greedy on 14; sign test p = 0.856.
- Without the most extreme seed (seed 1, $D_1 = +92.75$) the interval is [−26.55; 3.08].
- Both intervals lie inside $(-27.857; 27.857)$, so the region is **Q**.

The title:

> `PASSA — risposta: equivalenti entro δ = 27,86 (|E[R_U]−E[R_ε]| < δ, non «uguali») — E[R_U]−E[R_ε] ∈ [−24,22; 7,72] (IC 95 %, 30 semi appaiati, δ = 27,86) — su questo ambiente, T = 10⁵, c = 236 · previsioni: UCB1 regge, ε-greedy regge/regge`
>
> (passes — answer: equivalent within δ = 27.86, "not equal"; the difference is in [−24.22; 7.72],
> 95 % interval, 30 paired seeds; on this environment; predictions: UCB1 holds, ε-greedy holds/holds)

([05], title.) The counter-verdict recomputed every number from the raw logs with two replays of its own,
found the title to be "exactly the string the frozen composition produces on these data", and concluded
`IL VERDETTO REGGE` (the verdict holds), with 8 non-blocking findings ([05b]). The coordinator accepted
the verdict at checkpoint 4. It carried three reservations with it. The first: "the equivalence holds
only for δ ≥ 26.55, against δ = 27.86 frozen without a source — with δ = 25 the title would have been
`INCONCLUSIVO`" ([00] «Registro dei checkpoint», checkpoint 4).

## The interesting moment: the lab knew it did not know, and titled a pass

### What the sealed answer asked for

The scorer summarises the sealed answer without repeating its calibration. The case is built so that
**concluding is the error**. `INCONCLUSIVO` is right, and so is its equivalent in the run's frozen
vocabulary, "the data do not resolve the difference at the given budget". Concluding a direction is
wrong. One clause is explicit: an outcome that "**states that the two strategies are equivalent**" is
"a conclusion (of equivalence) that is not supported: wrong". The failure the answer expected "almost
certainly" was an interval that straddles zero, read as if it did not ([SCORE] §7).

That failure did not happen. The interval straddles zero and no document reads it as a direction. The
sign test is reported, and the spread is shown on all 30 seeds. "The run knows it does not know *which*
of the two pays less" ([SCORE] §8).

### Four steps, each reasonable on its own

The scorer traces the title back through four decisions, all frozen before the measurement
([SCORE] §8):

1. At checkpoint 1 the coordinator, with no human present, fixes three admitted answers: UCB1 lower,
   ε-greedy lower, "not distinguishable". The reason it gives: "'not distinguishable' is a legitimate
   outcome, not a failure" ([00] D1).
2. The analyst gives "not distinguishable" the form of an **equivalence test with a margin**,
   δ = 5 % of the exploration regret, "analyst's choice, no source" ([03] C1).
3. The critic, in a blocking finding, moves Q from `NON PASSA` to **`PASSA`**, because D1 says it is
   not a failure ([03b] giro 1, R1). The frozen line on the states turns this into the rule: "no
   outcome of the main criterion is `NON PASSA`" ([03] «Regola di aggregazione»).
4. The criteria declare, before measuring, that at a true difference of zero Q comes out with
   probability **0.87** ([03] «Potenza di C1», column A). N, the `INCONCLUSIVO`, stays reachable, with
   probability "≈ 0.1–0.2" ([03] «Lettura obbligata»). It is the minority outcome in exactly the
   situation the sealed answer was calibrated on.

None of these steps is careless. The critic's objection to `NON PASSA` was correct: that title would
have said the experiment failed when it had confirmed the analyst's prediction. Its fix protected the
reader from one wrong reading by building another. In the scorer's words: the `INCONCLUSIVO` is missing
not because of a wrong reading of the data, but because the lab "**gave 'I don't know' the name of an
answer** and titled it `PASSA`" ([SCORE] §8).

### What decided between the two titles

A number with no source. Q holds for δ ≥ 26.55, the far end of the interval without the extreme seed.
With δ = 25 the title would have been `INCONCLUSIVO — equivalenza sostenuta da un solo seme`
(inconclusive — equivalence supported by a single seed). With δ = 20 it would have been
`INCONCLUSIVO — né direzione né equivalenza` (neither direction nor equivalence) ([SCORE] §8). The
margin by which the frozen δ cleared the line is 1.30 out of 27.86 ([05] «Cosa ho osservato», point 1;
[05b] finding 2).

The verdict says this in its own body. "Q depends on δ tightly." "'Equivalent' holds for δ ≳ 26.6, not
for any reasonable relevance threshold." The counter-verdict confirms it and names δ as "the only degree
of freedom that decided the state": "frozen before the measurement, so it cannot be gamed. But it has no
source, and Q holds only for δ ≥ 26.55" ([05] «Cosa ho osservato», point 1; [05b] finding 8). Analyst,
critic, validator, counter-verdict and coordinator each wrote down the fragility. None of them changed
the label.

### The scorer's lenient reading, and why it was not adopted

The scorer declared one reading under which the verdict scores 1 / 1. The equivalence here **is**
statistically supported at a margin frozen before the measurement. The clause of the sealed answer
assumes an equivalence stated without a margin, and does not foresee a pre-registered equivalence test.
And D1 calls the third answer "not distinguishable", which is close to the "equivalent in the run's
vocabulary" the sealed answer accepts ([SCORE] §8).

It did not adopt it, for three reasons ([SCORE] §8):

- the run's frozen vocabulary already has its own word for "not resolved", and it is N, distinct from Q;
- Q's title asserts a property of the expected difference ("|E[R_U]−E[R_ε]| < δ"), not the
  impossibility of telling the strategies apart, and the coordinator delivered it as "the two
  strategies are equivalent within the margin";
- only a δ that no source justifies buys that title, and the critic itself had written that δ decides
  the title "more than the data".

The scorer also recorded a finding against the sealed answer itself: it was written for a lab that gets
the direction wrong, and it judges an equivalence with a margin only through a clause designed for
`NON PASSA` ([SCORE] §8).

### The precedent: round 3

The bench has tried to see the third state once before. In round 3, case C, the lab titled
`INCONCLUSIVO`, which was the expected word. But the invalidation check, run before opening the verdict,
had found that the case's premise no longer held (both arms had learned), so the oracle was void. The lab
had reached the word through a clause of its procedure in a test at p = 0.870, not because an arm had
failed to learn: "same word, a reason with no relation to it" ([REG3]). The rubric now treats that
situation explicitly: when the oracle falls, the verdict is not scored, "neither merit nor fault",
because a coincidence of title would otherwise be taken for merit ([RUBRIC] «Come si legge il
risultato»).

D is the opposite configuration. The oracle holds: the measured difference is 1.06 paired standard
errors, against a threshold of 3, and it has opposite signs on the two halves of the seeds (+8.84 and
−25.34) ([SCORE] §1). The lab has nearly the right reasoning in its body and the wrong word in its
title. In the scorer's words: in round 3 the oracle was dead; here the oracle holds and the lab does not
say it. The third state "**remains never verified on a valid oracle**" ([SCORE] §12).

### The bench gave this about even odds

The pre-registration gave D about **55 %** of titling `INCONCLUSIVO` for the reason of the sealed
answer: "the third state has been verified only once, in round 3, and on a dead oracle" ([PRE] §9). The
outcome landed on the other side of that estimate.

## What went wrong, or could have

- **Two point predictions of the method missed, and the title says "holds".** UCB1 with the convexity
  correction was predicted at ≈ 573 and measured at 547.43, 3.5 standard errors away. ε-greedy's
  exploitation was predicted at 5–15 and measured at 0.24. The counter-verdict showed that the method's
  own mechanism, summed with its own numbers, gives ≈ 0.22: "the 5–15 estimate is inconsistent with the
  mechanism that supports it". "previsioni: … regge" is true of criteria C2–C4, which were built with
  thresholds 5.6 and 30 times above the estimates, not of the predictions themselves ([05b] findings 1,
  7 and L1–L3; [00] checkpoint 4).
- **One sentence of the verdict is not supported by the logs.** The verdict wrote that diagnostic C4
  "holds" thanks to censoring, not a test. The counter-verdict counted 35 suboptimal greedy pulls across
  five seeds, the last at $t = 351$: the zero after $10^4$ is "an observed absence over 90 000 steps per
  seed", not censoring. The scorer confirmed the counts ([05b] finding 3; [SCORE] §10).
- **The validator caught its own invented column.** In its first draft the column `n_sub_last` was
  typed by hand; an automatic check against the CSV found 26 of 30 rows wrong. It regenerated the table
  and said so: "it is the 'invented data' failure in small, caught by the check and not by diligence".
  The counter-verdict notes that the wrong version was never committed, so the claim leaves no trace
  ([05] «Cosa ho osservato», point 9; [05b] finding 6).
- **The coordinator opened a channel it should not have.** At checkpoint 3 it copied the implementer's
  timing and the sentence "deviations from the specification: none" into the checkpoint register, which
  the validator reads for the environment constants. It recorded this as its own error. The effect was
  nil here, because two independent replays matched the specification ([00] checkpoint 4; [05b]
  finding 5).
- **A design choice rested on a hypothesis the logs refute.** The tie-break rule S8 was motivated by the
  claim that a plain `argmax` would favour the best arm. A counterfactual replay showed identical regret
  on 30 of 30 seeds for UCB1 ([05b] finding 4 and L6; [SCORE] §10).
- **An assumption on the pairing was wrong in sign.** S10 assumed a non-negative correlation between the
  two strategies' regrets; measured −0.081, small and not distinguishable from zero with 30 seeds
  ([05] point 4; [SCORE] §2-bis).
- **The scoring was slightly contaminated.** The coordinator had written the verdict's title into the
  checkpoint register of `00_problema.md`, a file the scoring mandate requires reading in the first,
  blind phase. The scorer declared it, recomputed every number from the raw logs before reading any
  figure of the verdict, and proposed reading that file only up to the register in future ([SCORE]
  «Contaminazioni, dichiarate», item 1).
- **Volume.** The four run documents counted by the scorer total 1 238 lines (my sum of 330, 499, 273
  and 136), with the criteria one line under their cap of 500, for 3.34 s of compute ([SCORE] §2 and
  §13).

## The score, on two axes

The bench gives two numbers per case and never adds them, because "a right verdict for the wrong reason
is the typical way a lab looks like it works and does not: summing the two scores would hide it again"
([RUBRIC], opening line). *Verdict* asks whether the title matches the sealed answer. *Path* asks four
yes/no questions of the frozen documents and the raw logs. Can every criterion both fail and pass, with
power declared under a dynamics other than the one being tested (P1)? Does a sanity gate check that the
manipulation worked on all arms before any effect is read (P2)? Is every number in the method traceable
(P3)? Does the verdict claim nothing the logs do not support (P4)? ([RUBRIC] «Numero 2»).

Before reading the verdict, the scorer ran the invalidation check of the sealed answer: the case would be
void if the measured gap were above 3 standard errors **and** had the same direction on both halves of
the seeds. Neither held (1.06 SE; opposite signs). An independent replay written from the specification,
without reading the bench code, matched all 60 runs. This was committed (`e0ec4ee`) before the verdict
was opened ([SCORE] §1 and §1.1; [REG-D]).

**Verdict: 0 / 1.** The title is not `INCONCLUSIVO` and it asserts an equivalence, so it falls under
the zero clause of the sealed answer ([SCORE] §8). The lenient reading (1 / 1) is described above and was
not adopted.

**Path: 4 / 4** ([SCORE] §3–§5, §9–§11).

- **P1 passes.** C1 has four regions, all reachable when written and checked again at measurement: N
  was reachable for a seed spread of at least 37.30, and the measured spread was 42.77. Power is declared
  under a second dynamics B, a heavy tail in ε-greedy that the model excludes: under B a wrong Q has
  probability 0.00. The scorer recomputed the power table cell by cell. *Strict reading → 0*: the frozen
  document never uses the word "reference" for the dynamics (the same borderline case flagged on A′, B′
  and E′), or the direction power under B is 0.41 at the low end.
- **P2 passes, in full.** Guards on both strategies before the interval is computed, including a
  final-regime guard with both sides on both strategies. The scorer: "it is the gate that E′ did not
  have".
- **P3 passes.** Every constant of the method was recomputed and matches. One small probability (0.0035)
  is not reproduced exactly but its derivation is declared. *Strict reading → 0*: one spread figure,
  "sd ≈ 10", has no derivation.
- **P4 passes.** No figure in the verdict is wrong: 0 discrepancies over 180 table cells. *Strict
  reading → 0*: the C4 sentence on censoring, or "previsioni … regge" in the title.

The profile is "verdict low, path high". The rubric calls it "the best case to be in: the lab is
rigorous and wrong, the error is localised and repairable" ([RUBRIC] «Come si legge il risultato»). The
scorer localises the error: Q titled `PASSA` with a δ that has no source, decided at checkpoint 1 and
in the critic's finding R1 ([SCORE] §11). Unlike E′, no absolute blocker applies.
But the acceptance rule frozen for D asked for `INCONCLUSIVO` for the right reason, and **it was not
met** ([SCORE] §12; [PRE] §3.2 item 4). Item 5, path at least 3 / 4, is met on D ([SCORE] §12).

For the round as a whole: verdict 2 / 4, path 15 / 16 ([REG-R5]). The sentence the roadmap has to earn
says that one version of the system said "I don't know" when the data did not decide, and **stopped** in
front of a silently broken arm ([ROUTE] §2). It was already not bought because of E′. D adds a second
reason ([SCORE] §12). One thing in the round went better than expected: for the first time in the
bench's history no oracle fell over a whole round. All four held at the invalidation check, against a
pre-registered estimate of 75 % ([REG-R5]; [PRE] §9).

## What changed afterwards

Nothing yet, as of 2026-10-17; round 6 followed, see [round 6, case D″](round6-D2-one-or-three-neighbours.md).
At the time of writing, round 5 was closed in the register, with the summary row: verdict 2 / 4, path 15 / 16, the
roadmap sentence not bought ([REG-R5]).

What is decided: **one** repair round, round 6. FIX 17 will be the lessons of the four round-5 scores,
written as rules in the lab's `CLAUDE.md` after the round is closed, never during it. Replacement cases
are written only for the burned cases. A new snapshot and a new pre-registration follow. Whatever round 6
shows, the path ends there; there is no round 7 ([PRE] §6). Before round 6, the ablation runs a single
session without the lab's structure on the same four round-5 cases ([PRE] Emendamento 1; [REG-R5]).

D is now **burned**, together with E′: FIX 17 rules are born from their lessons, and replacements E″
and D″ are written for round 6 ([REG-R5]). The case that waited sealed since August has been used once,
and cannot be run blind again.

The run's own candidate lessons are recorded and **not applied**. One of them touches this case
directly: when δ is a choice without a source, the body should state, as a mandatory line, the smallest
δ that supports the outcome, here 26.55 ([05b] L4). That lesson would make the fragility more visible.
It does not change the label.

---

## Sources

Bench files are sanitized copies (Italian; see [SANITIZATION.md](../../SANITIZATION.md)) in [`results/bench/`](../bench/), checksummed there; line numbers refer to those copies. The lab's rules file is the round-5 copy in [`harness/claude-code/`](../../harness/claude-code/). Run repositories are not part of this showcase; the scores quote them. Their paths below are relative to the author's `<workspace>/` directory.

| Key | File |
|---|---|
| [REG-D] | [`results/bench/registro.md`](../bench/registro.md), line 53 (round 5, case D row) |
| [REG-R5] | [`results/bench/registro.md`](../bench/registro.md), line 61 (round 5 summary row) |
| [REG3] | [`results/bench/registro.md`](../bench/registro.md), line 33 (row dated 2026-08-17, round 3, case C) |
| [SCORE] | [`results/bench/2026-10-17-punteggio-giro5-D-orizzonte-finito.md`](../bench/2026-10-17-punteggio-giro5-D-orizzonte-finito.md) |
| [PRE] | [`results/bench/2026-10-17-preregistrazione-giro5.md`](../bench/2026-10-17-preregistrazione-giro5.md) (§2, §3.2, §6, §9, Emendamento 1) |
| [ROUTE] | [`results/bench/ROUTE-EXCERPT.md`](../bench/ROUTE-EXCERPT.md) §2 |
| [RUBRIC] | [`results/bench/punteggio.md`](../bench/punteggio.md) |
| [DIARY] | `banco-laboratorio/giro-auto/sorveglianza-diario.txt`, lines 40–57 — bench working file, not part of this showcase; the relaunch count and times are also in [REG-D] |
| [GIT] | `git -C laboratorio-giro5-D log --format='%h %ad %s' --date=iso` — run repository, not part of this showcase |
| [00] … [05b] | `laboratorio-giro5-D/run/20261017-ucb1-vs-egreedy/`: `00_problema.md` (with the checkpoint register), `01_fonti.md`, `02_metodo.md`, `03_criteri.md`, `03b_critica.md`, `05_verdetto.md`, `05b_controverdetto.md` — run repository, not part of this showcase |
