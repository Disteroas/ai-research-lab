# Details, caveats and provenance

This was the repository's README until 2026-10-18. The short version is [`../README.md`](../README.md);
this file keeps every number with its source, the alternative readings, the errata and the provenance.

**I built a multi-agent research lab and, separately, the bench not to trust it. The bench found a
defect in the lab in each of five scored rounds. In the sixth, one repaired version of the lab got all
four blind cases right, on the substantive reading of the bench's rubric.**

The lab is a chain of agents that takes a question to a three-state verdict (`PASSA`, `NON PASSA`,
`INCONCLUSIVO`: passes, does not pass, inconclusive), with criteria frozen in git before any code
exists. The bench is a set of problems whose answers are sealed outside the lab's reach. It is
pre-registered before every round and scored on two axes that are never added together. In rounds 1
to 5 the bench found a defect in the lab every time. It also found a defect in one of its own oracles,
and in the tool that said which version of the lab had run.

Round 6 ran one version of the repaired system (FIX 1-17) on four blind cases and scored **verdict
4/4, path 16/16** ([register](../results/bench/registro.md), line 105). By the bench's own acceptance
rule, that buys the sentence the route fixed on 2026-08-18 as the end point of the project
([route §2](../results/bench/ROUTE-EXCERPT.md); progress log, [route §7](../results/bench/ROUTE-EXCERPT.md),
line 251). In my translation from the Italian:

> I built a multi-agent research lab and, separately, the bench not to trust it. The bench found two
> real defects in the lab — a dead oracle and a guard that did not fire — and I repaired them. **One
> single version** of the repaired system then passed five profiles blind: it said yes when it was yes,
> no when it was no, "I don't know" when the data did not decide, it **stopped** in front of a silently
> broken arm, and it did so better than a single session without structure, measured on the same
> cases.

Four facts stand next to that result:

- **It holds on the substantive reading of the rubric.** Under the strict reading, declared in every
  score, the round-6 path is **10/16** (A′ 2/4, B′ 3/4, E″ 2/4, D″ 3/4), and A′ and E″ fall below the
  3/4 per case that the acceptance rule asks for. Which reading is right is an open question that
  belongs to the author (`<domanda aperta 7>`), not to the scorers ([register](../results/bench/registro.md), line
  105; [round-6 pre-registration §3 and §4](../results/bench/2026-10-17-preregistrazione-giro6.md)).
- **"Better than a single session" holds for the path, not for the verdict.** The single-session
  ablation ran on the four round-5 cases: single session verdict 3/4 · path 10/16, lab 2/4 · 15/16
  ([register](../results/bench/registro.md), line 81, with the errata of line 85; [below](#ablation-the-same-four-cases-one-session-no-structure)).
  Four of the lab's five points of path advantage are P1 (declared power), an obligation the single
  session's preamble did not contain; outside P1 the gap is one point, P2 on A′
  ([register](../results/bench/registro.md), line 85; [ablation story](../results/round5-ablation-single-session.md),
  «What this ablation does not say»).
  It was not repeated on round 6, and the round-6 acceptance rule does not include it
  ([round-6 pre-registration §4](../results/bench/2026-10-17-preregistrazione-giro6.md), item 5).
- **The sentence says five profiles; round 6 had four cases**, and its pre-registration speaks of four
  profiles ([§5](../results/bench/2026-10-17-preregistrazione-giro6.md)). I quote the sentence as written
  and leave the mismatch visible.
- **The sentence counts the dead oracle among the lab's defects and says both were repaired.** The
  oracle was the bench's (case C, fallen in round 3), not the lab's, and it was not repaired: case C is
  void and its rebuilding is suspended, not planned ([register](../results/bench/registro.md), line 14,
  table «Casi consumati»). Here too the sentence stays as written and the mismatch stays visible.

This repository holds the protocol, sanitized copies of the files that were measured (see [SANITIZATION.md](../SANITIZATION.md)), the four round-6 cases with their
answers, and the bench's own records, so that every number below can be checked against a file.

Every number in this README links to the file it comes from. The bench's files are Italian, as sanitized
copies (see [SANITIZATION.md](../SANITIZATION.md)), in [`results/bench/`](../results/bench/). Where a figure is mine (a sum, a ratio), I say so.

## Repository map

| Path | What is there |
|---|---|
| [`protocol/`](../protocol/) | the protocol, harness-agnostic, in English: the six roles, the 19 rules, the artifact chain, the bench method |
| [`harness/claude-code/`](../harness/claude-code/) | the reference implementation for Claude Code: sanitized copies (see [SANITIZATION.md](../SANITIZATION.md)) of the measured files (Italian), with checksums and launch scripts; [`giro6/`](../harness/claude-code/giro6/) holds the 2 files that changed for round 6. **The benchmark was measured here** |
| [`harness/openai-compatible/`](../harness/openai-compatible/) | `lab.py`, a one-file, stdlib-only orchestrator for Ollama / vLLM / LM Studio. **Not validated by the bench** |
| [`cases/`](../cases/) | the four round-6 cases (A′, B′, E″, D″): problem text, sealed answer, calibration script (Italian; sanitized copies, see [SANITIZATION.md](../SANITIZATION.md)). The six earlier cases are not included: their register rows and scores are in [`results/bench/`](../results/bench/), and E′ and D also have stories in [`results/cases/`](../results/cases/) |
| [`results/`](../results/) | eight stories (four round-5 cases, the ablation, and three on round 6), in English |
| [`results/bench/`](../results/bench/) | the bench's register, rubric, pre-registrations and scores: sanitized copies (Italian; see [SANITIZATION.md](../SANITIZATION.md)), with checksums, plus an English excerpt of the route |

## What this is, and what it is not

What it is, in the words of the goal written on 2026-08-18
([route §1](../results/bench/ROUTE-EXCERPT.md)), three things. First, a demonstration of a
multi-agent framework that works on small experiments, with a three-state verdict. Second, a
demonstration of a way to check with AI what AI produces: frozen criteria, sealed oracles, a two-axis
score. Third, extracting the agents (critic, counter-verdict, validator, the discipline of frozen
criteria) for the author's real projects, with the author coordinating; the whole lab is not used and
stays on display.

What it is not:

- **It does not scale to real problems, as far as anyone knows.** Every bench problem is synthetic,
  fixed by its text, and computed in seconds: the four round-5 runs used 0.44 s, 1.40 s, 2.11 s and
  3.34 s of compute ([register](../results/bench/registro.md), lines 41, 45, 49, 53). The route lists
  this among the things it does not claim, together with the ratio of prose to computation surviving
  outside small problems ([route §2](../results/bench/ROUTE-EXCERPT.md), «Cosa NON si rivendica»).
- **It has never served the author's real research.** The lab's rules file opens by saying it is not
  an assistant for the user's real research ([`CLAUDE.md`](../harness/claude-code/CLAUDE.md), line 5), and
  the route says it will never touch the author's own research
  ([route §2](../results/bench/ROUTE-EXCERPT.md)).
- **It is not a statistic.** Each round is one run per case, four cases at most. Round 6 bought the
  route's sentence on four runs; the register closes with "no round 7"
  ([register](../results/bench/registro.md), line 105).

## The lab in one picture

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

Two structural defences carry the design ([`protocol/README.md`](../protocol/README.md)). Against
p-hacking: criteria committed **before** the first commit in `04_impl/`, checkable with `git log`.
Against invented data: a validator that has not seen the implementer's tests, then a counter-verdict
that rereads the raw logs. From round 2 on, every bench run was unattended: the coordinator decided
at the checkpoints and wrote down why ([`harness/claude-code/README.md`](../harness/claude-code/README.md)).
In round 1 the author approved at the checkpoints without reading the content
([register](../results/bench/registro.md), line 25).

## The bench

The bench is to the lab what an oracle is to a program under test. Its method is in
[`protocol/bench-method.md`](../protocol/bench-method.md). Its working parts:

- **Two axes, never added.** *Verdict*: one point per case if the title matches the sealed answer.
  *Path*: four binary checks per case, read on the frozen criteria, the critique, the verdict and the
  raw logs, not on what the lab says about itself. P1 asks whether criteria can fail and can pass, with
  power declared. P2 asks for a sanity gate on every arm. P3 asks that every number be traceable. P4
  asks that the verdict stay within the data. "A right verdict for the wrong reason is the typical way a
  lab looks like it works and does not: adding the two scores would hide it again"
  ([rubric](../results/bench/punteggio.md), opening line).
- **Blind.** The lab receives the case text and nothing else. The answers live outside its repository,
  and a run that mentions the bench is void.
- **Pre-registered.** Before every round: composition, acceptance rule, attribution, deviations and a
  numeric prediction, frozen and only amended at the end with a date
  ([round 5](../results/bench/2026-10-17-preregistrazione-giro5.md),
  [round 6](../results/bench/2026-10-17-preregistrazione-giro6.md)).
- **Invalidation first.** Every scorer first runs the sealed answer's invalidation condition on the
  raw logs, and commits its outcome **before** opening the lab's verdict. Then P1-P3, a commit, then
  verdict and P4.
- **Consumed cases.** When a rule of the lab is born from a case, the case is burned and replaced. The
  lab's rules file now tells its story, and rerunning it would measure memory, not method
  ([register](../results/bench/registro.md), table "Casi consumati"). The burned and void ones (A, B, C, E, E′, D) are
  not in this repository; their register rows and scores are in [`results/bench/`](../results/bench/).
- **The oracle can fall.** In round 3 the invalidation check voided case C before anyone looked at the
  verdict. Both arms had learned, so the poisoned protocol no longer bit. The lab had titled
  `INCONCLUSIVO`, the expected answer, for an unrelated reason. Read verdict-first, that would have been
  scored as merit ([register](../results/bench/registro.md), line 33). Since then the rubric has a profile
  for it: verdict with denominator 0, path scored in full, case replaced
  ([rubric](../results/bench/punteggio.md), «Come si legge il risultato»).

## Results

One row per scored round, from the register. "System" is the set of fixes the run's own copy of the
rules file contained. Verdict and path are on the round's own denominators: rounds differ in size and
are not summed.

| Round | Date | System | Cases | Verdict | Path | What the bench found | Source |
|---|---|---|---|---|---|---|---|
| 1 | 2026-08-03 | lab `8d27db5`: rules 1-3, before FIX 1 | A | 0/1 | 3/4 (2/4 under the rubric amended on 2026-08-05) | a **false negative**: the measurement matched the closed form, but the lab titled `NON PASSA` after writing that the failing criterion failed in the direction *opposite* to a refutation. There was no rule for composing criteria into a verdict. The path had been self-scored 4/4 and was corrected on rescoring | [register](../results/bench/registro.md), lines 25, 58 |
| 2 | 2026-08-10 | `a7b22b1`, FIX 1-8 | A, B (C deferred by the author) | 2/2 | 8/8 (7/8 if one P1 change made after opening the answer is judged lenient) | the false negative is closed on the same case. Two attackable points, stated in the register: a P1 changed after opening the answer (hence 7/8), and A's `PASSA` rested on an interpretive act, because the run's aggregation rule R4 asked for "guards passed" without naming the arm, so "R4 must be rewritten" ("guards passed on the load-bearing arms"). Five true things the score cannot see become rules 7-11. Both cases had huge effects (≥ 26× and 1357×), so `INCONCLUSIVO` stays **installed, not verified** | [register](../results/bench/registro.md), line 29; [score](../results/bench/2026-08-10-punteggio-giro2.md) |
| 3 | 2026-08-17 | `a7b22b1`, FIX 1-8 (first recorded as FIX 9-15, corrected) | C | not scored: **oracle fell** (denominator 0) | 3/4 (2/4 after the 2026-08-18 rescoring) | the poison no longer bit: both arms learned (medians 0.1430 and 0.0948 against frozen thresholds 0.0321 and 0.0368). The lab's `INCONCLUSIVO` came by a route unrelated to the poison: the guard meant to catch it never fired. An erratum the same day found that route sound on its own (the effect was neither detected nor excluded), so the third state was seen working, on a dead oracle. Also: the system check compared the live rules file, which no run reads. All of A, B and C had run on FIX 1-8, and FIX 9-15 had **never run**. Tool repaired the same day | [register](../results/bench/registro.md), line 33; [score](../results/bench/2026-08-17-punteggio-giro3-C.md); [validation map](../results/bench/2026-08-17-mappa-validazione.md) |
| 4 | 2026-08-18 | `bece2ac`, FIX 1-15 | E | 1/1 (0/1 if the title's first clause, a paired speed comparison, is judged to weigh more than the synthesis) | 2/4 (3/4 if the non-blocking branch (3) of the gate is judged a legitimate design choice) | the **absolute blocker** of the pre-registration tripped. The sanity gate passed **30/30 on the arm built to be broken**: it took the maximum over all windows, and optimistic initialisation gave the broken arm an early bump (window means 0.41 · 0.52 · 0.18 · 0.04). Zero guards had fired in "4 real runs", in the route's count | [register](../results/bench/registro.md), line 37; [score](../results/bench/2026-08-18-punteggio-giro4-E.md); [route §3](../results/bench/ROUTE-EXCERPT.md), line 70 |
| 5 | 2026-10-17 | `8958eb7`, FIX 1-16 | A′, B′, E′, D | 2/4 | 15/16 | zero oracles fell, a first. A′ and B′ right for the right reason. **E′**: the final-regime gate existed and was blocking, but the frozen criteria admitted the broken regime for the experimental arm, and zero guards fired for the fifth real run in a row. **D**: titled `PASSA` as "equivalent within δ = 27.86", a margin with no source. The interval [−24.22, 7.72] straddles zero, the title holds only for δ ≥ 26.55, and with δ = 25 it would have been `INCONCLUSIVO` | [register](../results/bench/registro.md), lines 41-61; [scores](#the-stories) |
| 6 | 2026-10-17/18 | `128634d`, FIX 1-17 | A′, B′ (rerun as they were), E″, D″ | 4/4 | 16/16 (strict reading 10/16) | zero oracles fell, again. A′ `PASSA` and B′ `NON PASSA` again, for the right reason. **E″**: the gate on the task's own success criterion (rule 18) was blocking and **fired** on the broken arm (criterion reached by 0/30 seeds, censored 30/30); the title is a declared stop, `INCONCLUSIVO (forzato)`: **a guard stopped a run**. On the three valid cases built to need a stop (E in round 4, E′ in round 5, E″ here), a guard stopped the run once, on the third attempt; no guard had stopped any of the nine lab runs scored in rounds 1-5 (1 + 2 + 1 + 1 + 4 in the rows above; register lines 33, 37, 49 and 61, «zero guardie scattate»; E″ on line 97). **D″**: titled `INCONCLUSIVO` because the 95 % interval of the main quantity, [−0.010041, 0.010374], contains zero, with no equivalence margin and no extra seeds (rule 19): **the third state for the right reason, on a valid oracle, for the first time**. Also: two runs died on the usage limit, A′ ran twice, the critic's new row was never put to the test, and the scorer of D″ recorded a design debt in its oracle ([Honesty notes](#honesty-notes)) | [register](../results/bench/registro.md), lines 89-105; [scores](#the-stories) |

**Round 6 was the repair round.** It was pre-registered as the only one: "no round 7, written here
before knowing how it goes" ([round-6 pre-registration §0](../results/bench/2026-10-17-preregistrazione-giro6.md)).
A′ and B′ were rerun as they were, because no rule of FIX 17 was born from them; E″ and D″ replaced
the two cases burned by rules 18 and 19, and their texts and answers were sealed during the round (§2); they are now published in
[`cases/`](../cases/). The
pre-registration gave the whole sentence ~25 %, a guard stopping on E″ ~45 %, and D″ `INCONCLUSIVO` for
the right reason ~55 % (§5). On the evening of 2026-10-17, while round 6 was running, the author raised
the cap to round 8 with a stop at the first round that buys the sentence (route, Amendment 2, in
[`results/bench/ROUTE-EXCERPT.md`](../results/bench/ROUTE-EXCERPT.md)), and wrote that every round,
failed ones included, stays in the register and here. The cap was not needed
([route §7](../results/bench/ROUTE-EXCERPT.md), line 251).

**What round 6 bought.** All five acceptance conditions of the pre-registration were met, the fifth
(path ≥ 3/4 on every case) on the substantive reading only
([pre-registration §3](../results/bench/2026-10-17-preregistrazione-giro6.md);
[register](../results/bench/registro.md), line 105). By the falsifiers written with FIX 17, rule 18 was
applied on E″ and rule 19 on D″ (§3.bis; register, lines 97 and 101). All four oracles held at the
invalidation check: A′ ρ̃ = 11.0048, B′ R̂ = 10.3086, none of E″'s four invalidation conditions fired,
D″ |t| = 0.033 against a threshold of 3 (register, line 105). The four runs took ≈ 5 h 26 min of
effective work, the register's sum of 2 h 34 min, 44 min, 57 min and 1 h 11 min (line 105).

**What round 5 did not buy.** Round 5 met three of the five acceptance conditions of the same sentence.
It failed the one on E′ (a guard must stop) and the one on D (`INCONCLUSIVO` for the right reason)
([register](../results/bench/registro.md), line 61). The pre-registration had given the full sentence
30-40 % on the first attempt
([§9](../results/bench/2026-10-17-preregistrazione-giro5.md)).

**Strict readings.** Each score names the readings it did not adopt. Under the strict reading of the
power threshold (the frozen documents never use the word "reference" for the dynamics they identify)
and of some sentences in the titles, round 5's path drops to 2/4 on A′ and B′ and to 1/4 on E′ and D
([register](../results/bench/registro.md), line 61). Round 6's drops from 16/16 to 10/16: A′ 2/4, B′
3/4, E″ 2/4, D″ 3/4, every strict loss going through the power check read literally or through single
sentences of commentary (line 105). The question is open and belongs to the author, not to the
scorers (`<domanda aperta 7>`; [round-6 pre-registration §4](../results/bench/2026-10-17-preregistrazione-giro6.md),
item 1).

## Ablation: the same four cases, one session, no structure

After round 5, the same four case texts went to a single session with the same model, the same folder
boundary and a short preamble. That preamble asks for criteria committed before code, raw logs and a
three-state verdict, and is quoted in full in the
[ablation story](../results/round5-ablation-single-session.md). There were no subagents, no critic and
no checkpoints. Fresh sessions scored it with the same rubric
([register](../results/bench/registro.md), line 81).

| Case | Single: verdict · path | Lab: verdict · path | Single: time | Lab: time | `.md` lines, single / lab |
|---|---|---|---|---|---|
| A′ | 1/1 · 2/4 | 1/1 · 4/4 | 3 min 18 s | 42 min 28 s | 160 / 882 |
| B′ | 1/1 · 3/4 | 1/1 · 4/4 | 3 min 34 s | 36 min 26 s | 343 / 1045 |
| E′ | 0/1 · 2/4 | 0/1 · 3/4 | 5 min 01 s | 47 min 46 s | 220 / 767 |
| D | **1/1** · 3/4 | **0/1** · 4/4 | 5 min 17 s | ≈ 75 min of work (2 h 53 min wall-clock) | 159 / 1238 |
| **Total** | **3/4 · 10/16** | **2/4 · 15/16** | ≈ 17 min | ≈ 3 h 21 min (see errata) | |

Sources: [register](../results/bench/registro.md), lines 65, 69, 73, 77 (per case), 81 (summary) and 85
(errata); lab times from lines 41, 45, 49, 53.

The structure bought the **path**, not the verdict. The whole path gap is P1 (declared power: single
0/4, lab 4/4) and P2 (gate on every arm: single 2/4, lab 3/4). P3 and P4 are 4/4 on both sides
([ablation story](../results/round5-ablation-single-session.md), «The score, on two axes»). Four of the
five points of difference are P1, and the single session's preamble never asked for declared power
(nor for a gate on every arm): the A′ scorer wrote that, judged on the task the session received, it
would get P1 = 1 ([register](../results/bench/registro.md), line 65). Outside P1, the path gap is one
point, P2 on A′ (line 85). The ablation story says it plainly: "The single session was scored on
obligations it was not given … The four P1 points are the largest part of the path gap". Whether a
longer preamble would buy the same path is untested
([ablation story](../results/round5-ablation-single-session.md), «What this ablation does not say»). On the one
case built to test the third state, D, the single session titled `INCONCLUSIVO` for the right reason.
The lab titled `PASSA`: its coordinator, analyst and critic had built, in three steps, the affirmative
label that a single session had no occasion to build
([register](../results/bench/registro.md), line 81). Neither system stopped on E′.

**Errata of 2026-10-17, appended to the register on the same day and not written over the summary
row** ([register](../results/bench/registro.md), line 85):

1. The lab's total time is ≈ 3 h 21 min, not the "≈ 2 h 41 min" of the summary row: that was a wrong
   sum.
2. The ratio of lines goes from 3.0 (B′: 1045 / 343) to 7.8 (D), not "from 3.5". The perimeters also
   differ between rows: the A′ ablation row counts 1239 lines for the lab, the summary row 882.
3. The summary said the reading was "pre-declared in the pre-registration §9". **False.** §9 predicted
   that the single session would lose on E′ and on D (~70 %), and that its path would be lower "P2 and
   P4 above all". It went the other way on D, and there is no gap on P4. The prediction is
   **falsified on D and on P4**.
4. "Contaminations, all after P1-P3 were formed" was too strong. The scores declare that the single
   sessions' titles (A′, B′, E′) and the lab's rows (B′, E′) were seen **before** part 1.

The overall scores stand. Under the strict reading of one line of the single session's verdict on D,
the verdicts tie at 2/4 ([register](../results/bench/registro.md), line 85). Under the declared lenient
readings, the single session reaches 4/4 (E′, "a structural `NON PASSA` with C3 naming the failure")
and the lab 4/4 (E′ and D) ([register](../results/bench/registro.md), lines 49, 53 and 73; the
[ablation story](../results/round5-ablation-single-session.md), «The score, on two axes», reports all of
them).

## The stories

Each story retells one case for a reader who has not seen the bench, with a source table at the end
pointing into [`results/bench/`](../results/bench/). The texts and sealed answers of the four round-6
cases are in [`cases/`](../cases/).

| Story | Case role | Verdict · path |
|---|---|---|
| [Round 5, case A′ — the shared weight](../results/cases/round5-A1-shared-weight.md) | must `PASSA` | 1/1 · 4/4 |
| [Round 5, case B′ — momentum and gradient noise](../results/cases/round5-B1-momentum-noise.md) | must `NON PASSA` | 1/1 · 4/4 |
| [Round 5, case E′ — the waypoint reward](../results/cases/round5-E1-waypoint-reward.md) | silent broken arm: a guard must stop | 0/1 · 3/4 |
| [Round 5, case D — the finite horizon](../results/cases/round5-D-finite-horizon.md) | must `INCONCLUSIVO` | 0/1 · 4/4 |
| [Round 5 ablation — one session, no structure](../results/round5-ablation-single-session.md) | control arm on the four cases | single 3/4 · 10/16 |
| [Round 6, cases A′ and B′ — the same two questions, asked again](../results/cases/round6-A1-B1-rerun.md) | must `PASSA`; must `NON PASSA` (rerun as they were) | A′ 1/1 · 4/4 (strict 2/4); B′ 1/1 · 4/4 (strict 3/4) |
| [Round 6, case E″ — how much to explore](../results/cases/round6-E2-how-much-to-explore.md) | silent broken arm: a guard must stop | 1/1 · 4/4 (strict 2/4) |
| [Round 6, case D″ — one neighbour or three](../results/cases/round6-D2-one-or-three-neighbours.md) | must `INCONCLUSIVO` | 1/1 · 4/4 (strict 3/4) |

The scores behind them: round 5
[A′](../results/bench/2026-10-17-punteggio-giro5-A-primo-peso-condiviso.md),
[B′](../results/bench/2026-10-17-punteggio-giro5-B-primo-momentum-e-rumore.md),
[E′](../results/bench/2026-10-17-punteggio-giro5-E-primo-premio-di-tappa.md),
[D](../results/bench/2026-10-17-punteggio-giro5-D-orizzonte-finito.md); ablation
[A′](../results/bench/2026-10-17-punteggio-ablation-A-primo-peso-condiviso.md),
[B′](../results/bench/2026-10-17-punteggio-ablation-B-primo-momentum-e-rumore.md),
[E′](../results/bench/2026-10-17-punteggio-ablation-E-primo-premio-di-tappa.md),
[D](../results/bench/2026-10-17-punteggio-ablation-D-orizzonte-finito.md); round 6
[A′](../results/bench/2026-10-17-punteggio-giro6-A-primo-peso-condiviso.md),
[B′](../results/bench/2026-10-17-punteggio-giro6-B-primo-momentum-e-rumore.md),
[E″](../results/bench/2026-10-18-punteggio-giro6-E-secondo-quanto-esplorare.md),
[D″](../results/bench/2026-10-18-punteggio-giro6-D-secondo-tre-vicini.md).

## Timeline of fixes

Every numbered rule of the lab was written after a failure. English renderings with their "why" are in
[`protocol/rules.md`](../protocol/rules.md). The Italian texts (sanitized copies) are in
[`harness/claude-code/CLAUDE.md`](../harness/claude-code/CLAUDE.md) (rules 1-17) and
[`harness/claude-code/giro6/CLAUDE.md`](../harness/claude-code/giro6/CLAUDE.md) (rules 1-19).

| Fix | Lab commit | Born from | What it added, in one line |
|---|---|---|---|
| rules 1-3 (before the bench) | in `8d27db5` | the first real run, `20260802-generalizzazione-labirinti`: completed, validated, and it established nothing | guards on every arm; frozen constants produced by the bench code; "can it pass?" asked together with "can it fail?" |
| FIX 1-8 | `ed14a98` (2026-08-04, seven fixes), `fc63219` (2026-08-05, the eighth) | round 1, case A (run `20260803-bandit-esplorazione`, the false negative) | among them rules 4-6: a frozen aggregation rule, power not asked of the model under test, the three-state verdict; FIX 8 is the line caps on the three main documents |
| FIX 9-15 | `fc7f812` | round 2: case B, whose critic wrote four of them, and the round-2 score, which produced the fifth | rules 7-11: a label for pre-forced outcomes, logs one level below the aggregates, reproducibility proven with git, common-mode error declared, failed guards qualified per arm. First executed in round 4 |
| FIX 16 | `7598fa5` (2026-08-18) | round 4, case E: five lessons written by the run itself, the sixth from the score | rules 12-17: power conditioned on the observed resolution of the metric, pre-forced outcomes checked both ways and again at measurement, clause texts that name the measured quantity, no outcomes in `come_eseguire.md`, frozen log schemas, a learning gate on the final regime that can stop the comparison |
| FIX 17 | `128634d` (2026-10-17) | round 5: case E′ (rule 18) and case D (rule 19) | rule 18: the gate asks every arm for the task's own success criterion; rule 19: "not distinguishable" is titled `INCONCLUSIVO` unless the Statement asks for equivalence; one row added to the critic's checklist ("outcome not resolved, with an affirmative label"). First run in round 6: rule 18 applied on E″, rule 19 on D″; the critic's row used in substance, never put to the test |

Sources: [register](../results/bench/registro.md), lines 33, 58 and 105; [route §7](../results/bench/ROUTE-EXCERPT.md),
lines 244 and 249; [round-6 pre-registration §1](../results/bench/2026-10-17-preregistrazione-giro6.md); the
section headings of the two rules files.

## Reproduce / reuse

- [`protocol/`](../protocol/): the roles, rules, artifacts and bench method in English, independent of
  any agent harness.
- [`harness/claude-code/`](../harness/claude-code/): sanitized copies of the measured files, with checksum verification,
  installation into a run repository, the attended and unattended launch, and the round-6 variant.
- [`harness/openai-compatible/`](../harness/openai-compatible/): a portable one-file orchestrator for any
  OpenAI-compatible endpoint, local models included.
- [`cases/`](../cases/): the four round-6 cases, to see what a sealed answer and an invalidation condition
  look like. Now that they are public they cannot be used as oracles anymore.

**The numbers in this repository were measured only on the Claude Code harness**, with Claude Code
2.1.291 and the coordinator pinned to `claude-opus-5-5` in rounds 5 and 6 (`claude-opus-5` in rounds
2-4). The OpenAI-compatible orchestrator and any other model are untested by the bench
([round-5 pre-registration §4](../results/bench/2026-10-17-preregistrazione-giro5.md), line 103;
[round-6 pre-registration §1](../results/bench/2026-10-17-preregistrazione-giro6.md);
[`harness/claude-code/README.md`](../harness/claude-code/README.md)).

## What this does not claim

- That the lab scales to real problems with real data, or that its ratio of prose to computation
  survives outside small problems ([route §2](../results/bench/ROUTE-EXCERPT.md)).
- That the result holds for a model other than Opus 5.5
  ([round-5 pre-registration §9](../results/bench/2026-10-17-preregistrazione-giro5.md)).
- That the lab works in general. The sentence of [route §2](../results/bench/ROUTE-EXCERPT.md) was
  bought in round 6 on four synthetic cases, one run each, on the substantive reading of the rubric;
  on the strict reading two of the four cases fall below the acceptance threshold
  ([register](../results/bench/registro.md), line 105).
- That the structure beats a single careful session on the verdict. On the four round-5 cases it did
  not (3/4 against 2/4), and the comparison was not repeated on round 6. Each case is one run per arm,
  so a one-case difference cannot separate structure from luck
  ([ablation story](../results/round5-ablation-single-session.md), «What this ablation does not say»).
- That the guards reliably stop a broken arm. One guard has stopped one run: E″ in round 6. On the
  three valid cases built to need a stop (E in round 4, E′ in round 5, E″ in round 6), a guard stopped
  the run once, on the third attempt, and no guard had stopped any of the nine lab runs scored in
  rounds 1-5 ([register](../results/bench/registro.md), lines 33, 37, 49, 61 and 97).
- That the third state is reliable. It has been verified on a valid oracle once, D″ in round 6; before
  that it was seen only in round 3, on the oracle that fell ([register](../results/bench/registro.md),
  lines 33, 101 and 105).

## Honesty notes

- **Contaminations are declared, not avoided.** Every round-5, ablation and round-6 score has a
  section on what its scorer knew too early. In round 5, on A′ the scorer read the coordinator's
  summary, title included, before committing part 1; on D the title was in the checkpoint register of
  `00_problema.md`, a file the scoring mandate makes it read
  ([register](../results/bench/registro.md), lines 41 and 53). In round 6, titles were seen in `git log`
  or through searches that printed too much, always after the invalidation check; on E″ a search the
  mandate prescribes printed the title (a defect of the mandate), and the scorer of D″ read the
  register rows of the other three cases (lines 89-105). Each scorer argues why the effect is nil.
  The argument is in the file, for the reader to judge.
- **The same family of model plays every role, separated by role and by context, not by person.** In
  round 5 the coordinator was pinned to `claude-opus-5-5`, and the worker subagents declare their own
  tier (Sonnet for scouts, Opus for the others). Two isolated Opus agents wrote the sealed answers of
  A′ and B′ ([route §7](../results/bench/ROUTE-EXCERPT.md)). The scores were written by fresh
  subagents of the orchestrating session; each declares that it did not coordinate or watch the run
  (each score's opening section). The FIX 17 proposal was written by a subagent of the main session
  ([proposal](../results/bench/2026-10-17-FIX17-proposta.md), opening lines). The score files do not
  record the scorer's model. The bench method names the strong version: cases written by one person and
  scored by another ([`protocol/bench-method.md`](../protocol/bench-method.md)). This bench does not have
  it.
- **Every figure can be rederived from the logs.** Each scorer recomputes the counter-verdict's
  numbers from the raw logs, not by rereading them
  ([round-5 pre-registration §3.1](../results/bench/2026-10-17-preregistrazione-giro5.md)). The scores
  list those recomputations; in round 5 none of the counter-verdicts' figures was found wrong
  ([register](../results/bench/registro.md), lines 41-53). The run logs live in
  the private run repositories, so here that check can be read, not repeated. In round 6 the scorers
  again recomputed the counter-verdicts' figures from the raw logs (lines 89-101). One sentence of E″'s
  verdict is false on the logs: its observation 4 says that no exact tie moved, and 27 did. It concerns
  a probe, and no figure of the verdict depends on it (line 97).
- **The bench corrects itself in the open.** Round 1's self-scored path was corrected, and round 3's
  attribution was corrected the same day. Round 3's path was rescored retroactively after a rubric change
  declared in advance. The ablation summary got an errata on the day it was written. Corrections are
  appended; the corrected line stays ([register](../results/bench/registro.md), lines 25, 33, 85;
  [rubric](../results/bench/punteggio.md), «Storia del metro»).
- **Human attention on content was zero in rounds 5 and 6**, for all eight runs. In round 5 the author
  seeded the repositories, launched one case, and authorised the sandbox, without reading criteria,
  method or verdicts ([register](../results/bench/registro.md), line 61). In round 6 every launch came
  from the autonomous session, plus two manual relaunches (line 105). The blind held, and nobody
  corroborated the path by hand.
- **Two round-6 runs died on the usage limit and were relaunched.** A′ died at 20:53:49 with its
  criteria already frozen, D″ at 01:53:05 after its implementation. Each time, four automatic
  relaunches failed at the pre-flight check while the limit lasted, and a manual relaunch went through
  ([register](../results/bench/registro.md), lines 89, 101 and 105). D″'s relaunch resumed the same run:
  the implementation folder differs only in a timing file, and the frozen criteria were never touched
  (line 101).
- **A′ ran twice in round 6.** Its manual relaunch opened a second run instead of resuming the first,
  because of a clause in the frozen prompt for unattended runs: "if a previous run on a similar question
  exists in `run/`, it is not this question", written for an older seeded run and turned here against
  the run's own interrupted attempt. Under a rule written before the score, the run that reached the
  counter-verdict was scored and the abandoned one declared. The scorer found no copying (14 of 250
  and 7 of 186 lines identical, schema only). The cost: 2 h 34 min 06 s of effective work, of which
  1 h 34 min 23 s thrown away ([register](../results/bench/registro.md), line 89;
  [round-6 pre-registration](../results/bench/2026-10-17-preregistrazione-giro6.md), Amendment 2).
- **B′ has a commit after its counter-verdict.** A `replace` without a limit, run by the coordinator on
  a terminator string that the critic had quoted, duplicated checkpoint 2 inside a sentence of
  `03b_critica.md`. The counter-verdict found it, and commit `d905e15`, after the verdict, repairs that
  file only. `03_criteri.md` was committed once and never touched
  ([register](../results/bench/registro.md), lines 93 and 105).
- **The strict readings are a conflict between the yardstick and the system, still open.** Read to
  the letter, the rubric's power check also punishes a run that stops as E″ asks (its main comparison
  is pre-forced, so it has no power by construction) and B′'s main measure, which as a protocol cannot
  title `PASSA`; the scorers record both next to `<domanda aperta 7>` ([register](../results/bench/registro.md),
  lines 93 and 97). The rubric was not amended between rounds, because the decision belongs to the
  author ([round-6 pre-registration §4](../results/bench/2026-10-17-preregistrazione-giro6.md), item 1).
  Until it is taken, 16/16 and 10/16 stand side by side.
- **D″'s oracle has a design debt.** Its sealed answer assumes that no derivation gives the sign of
  the effect. The run's own finite-sample theory gives E[d] = −0.000500 (the answer's Monte Carlo:
  −0.000597 ± 0.00014), and the scorer's finer grids give −0.00051 and −0.00059: with grids 2-4 times
  finer, the sign would be resolved (the scorer's hypothesis). The case's defence rests on its 60 s cap
  in pure Python, not on the computation being impossible. The scorer records it as a debt, not an
  invalidation ([register](../results/bench/registro.md), lines 101 and 105).
- **The critic's new row was never put to the test.** In both E″ and D″ it was used in substance, but
  the defect it targets never reached the freezing of the criteria, so these cases cannot tell "the
  critic used the row" from "the analyst never produced the defect"
  ([register](../results/bench/registro.md), line 105).

## Provenance

| What | Where | Identity |
|---|---|---|
| system of round 5 (FIX 1-16) | [`harness/claude-code/`](../harness/claude-code/) | snapshot `2026-10-17-giro5`, lab `8958eb7`; `SHA256SUMS.txt` sha256 `69357b4e2650fdd3…` (computed from the committed file) |
| system of round 6 (FIX 1-17) | [`harness/claude-code/giro6/`](../harness/claude-code/giro6/) (2 files) + the 5 unchanged files of round 5 | snapshot `2026-10-17-giro6`, lab `128634d`; `SHA256SUMS.txt` sha256 `f22fb2e8c63564bb…`, as quoted in [the round-6 pre-registration §1](../results/bench/2026-10-17-preregistrazione-giro6.md); rules file sha256 `8dfe7fcb7696381e…` in all four run repositories ([register](../results/bench/registro.md), lines 89-101) |
| bench records | [`results/bench/`](../results/bench/) | copied at bench commit `349bba1` (2026-10-17), then refreshed on 2026-10-18 with round 6's register rows, scores and the scoring mandates, at bench commit `16dfde6` (2026-10-18), as recorded in [`results/bench/README.md`](../results/bench/README.md); 23 sanitized copies plus the route excerpt, [`SHA256SUMS.txt`](../results/bench/SHA256SUMS.txt) |
| round-6 cases | [`cases/`](../cases/) | bench commit `8dfba55` (2026-10-18); sanitized copies (see [SANITIZATION.md](../SANITIZATION.md)) |

The sha256 values quoted in this table and in the bench files identify the **validated originals**, kept in the
author's private bench. The shipped files are sanitized copies (see [SANITIZATION.md](../SANITIZATION.md)): they
are not byte-identical to those originals, and the `SHA256SUMS.txt` files in this repository list the sha256 of
the sanitized copies.

A run was attributable only if the system check said `SISTEMA INVARIATO` against the snapshot, on the
copy inside the run's own repository, at start and at end, and if the run's commits carried exactly
one model in their `Co-Authored-By` trailers. All four round-5 runs did, and all four round-6 runs did
([register](../results/bench/registro.md), lines 61 and 105). For A′ and D″ in round 6 the start-of-run
check of the first launch was overwritten by the relaunch; the register replaces it with an empty
`git diff` from seeding to the last commit on the 7 system files (line 105).

## License

To be chosen by the author before publication.

The publication gate was judged by an independent session; its verdict is kept privately.
