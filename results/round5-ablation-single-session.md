# Round 5 ablation — the same four cases, one session, no structure

| | |
|---|---|
| **Phase** | 5 of the roadmap, the control arm (run on 2026-10-17, after round 5 was closed) |
| **What was removed** | every role of the lab: no subagents, no critic, no checkpoints. One session per case, one prompt |
| **What was kept** | same four case texts, same model (`claude-opus-5-5`), same folder boundary, same two-axis rubric, fresh scoring sessions |
| **Single session** | verdict **3 / 4**, path **10 / 16**, ≈ 17 min in total (four runs of 3 to 5 min) |
| **Lab, round 5** | verdict **2 / 4**, path **15 / 16**, 36 to 75 min of work per case |
| **Where they differ on the verdict** | one case, D: the single session titled `INCONCLUSIVO`, the lab titled `PASSA` |
| **Where they differ on the path** | declared power (P1: 0 / 4 against 4 / 4) and, on one case more, the sanity gate (P2: 2 / 4 against 3 / 4) |
| **Human attention on content** | 0 min, all four |

Sources for the table: [REG-SUM]; [REG-A], [REG-B], [REG-E], [REG-D]; [SC-A] §10, [SC-B] §11,
[SC-E] §12, [SC-D] §11. All source keys are listed at the end. The source files are in Italian;
quotations are my translation. Numbers are copied as written, with the decimal comma turned into a
point; where I round, subtract, sum or divide, I say so.

The question of this phase is the one the whole project has to answer: what does a machine of six
roles add over one careful agent? The answer on these four cases is uncomfortable and clear. The
structure bought the **path**: power declared before measuring, gates that block on every arm, a
counter-verdict on the raw logs. It did not buy the **verdict**. On the one case built to test the
third state of the verdict, the structure did worse.

---

## The question in three lines

An ablation removes one part of a system and measures what changes. Here the removed part is the lab
itself: the scouts, the analyst, the critic, the validator, the counter-verdict, the checkpoints. What
is left is the model and the problem text.

The roadmap calls this "the most important missing experiment, and it is cheap", and fixes the rule
before any result: "if the single session draws level, it is a result that goes in the showcase all
the same — the cost of the structure is part of the story" ([ROUTE] §4, Fase 5).

Why it is hard to answer honestly: the bench was built to judge the lab, and every rule of the rubric
was written from the lab's own failures. A single session is scored against obligations it was never
told about. That cuts against it on the path axis, and the scorers say so (see "What this ablation does
not say").

## What was run

### The protocol, frozen before round 5 was launched

The pre-registration of round 5 froze the ablation protocol in its §7 ([PRE] §7):

- the **same four cases**, same text, same model, same folder boundary, **one single session per
  case**, each in an empty repo `<workspace>/ablation-giro5-<case>` with one initial commit by `banco`;
- the prompt is a frozen **preamble** plus the case text. Preamble sha256 `e8e761ed313a4773…`; one
  prompt per case (D: `dfbe28b0774fcb8a…`);
- a **time cap**: a single session that runs longer than the lab did on the same case (or 4 h, if
  longer) without `VERDETTO.md` is stopped and scored as it is;
- the **same two-axis rubric**, a fresh scoring subagent, the invalidation check first, and a
  comparison table in the register: verdict, path, lines written, duration, commits, human attention.

Amendment 1 moved the ablation earlier: after the round-5 summary row and before round 6, in the order
A′ → B′ → E′ → D, with the prompts unchanged ([PRE] Emendamento 1). None of the four sessions came near
the time cap: the longest took 5 min 17 s ([REG-SUM]).

### The preamble, in full

This is everything the single session received besides the case text ([PRE-AMB]; sha256 of the file
recomputed by me: `e8e761ed313a477351fa78eece2a448d378282db150694c90d76b66fbb8c9575`, which matches
the prefix frozen in [PRE] §7):

> You are a single session, without structure: no subagents, no critic, no checkpoints. You receive a
> problem and must reach on your own a three-state verdict — `PASSA`, `NON PASSA`, `INCONCLUSIVO` — on
> the claim to be tested, working only in this repo (git already initialised).
>
> Minimal structure, needed only so that the result is readable:
> 1. **Before writing code** write `CRITERI.md`: success criteria with numerical thresholds, number of
>    seeds and parameters, and what would make each criterion fail or pass. Commit it **alone**, before
>    any other file.
> 2. Implement in `impl/`, save the raw logs in `impl/logs/` (at least one level below the aggregates)
>    and commit.
> 3. Write `VERDETTO.md`: first line = the title (`PASSA`, `NON PASSA` or `INCONCLUSIVO`, plus one
>    sentence); then, for each criterion, expected / measured / outcome, and all the runs made. Commit.
> 4. Stop when `VERDETTO.md` is committed.
>
> No human is available: you make the decisions and write them in the files. If files from a previous
> attempt already exist in the repo, **they are yours**: continue from there, do not start again.

The pre-registration says why this much and no more: the minimal structure "serves only to make the
result scoreable with the same rubric; **it is not a defence** and does not count as 'structure of the
lab'" ([PRE] §7).

### What the four sessions did

Each session wrote `CRITERI.md`, committed it alone, wrote and ran its code, and committed the
verdict: three commits per case, in that order, every time. The scorers checked the order with
`git log` on all four repos: criteria first, no deletions, one co-author trailer (Claude Opus 5.5)
([SC-A], [SC-B], [SC-E], [SC-D] §2; [REG-A], [REG-E]). The D repo, for example ([GIT-D]):

```
9b75b63 2026-10-17 18:47:55 +0200 VERDETTO: INCONCLUSIVO, IC95 di D contiene 0 su 30 semi
d3b1960 2026-10-17 18:47:00 +0200 impl: simulazione vettorizzata sui semi, analisi, log grezzi del giro 1
fd39d82 2026-10-17 18:45:05 +0200 CRITERI: affermazione, soglie, semi e regola di verdetto (pre-misura)
c6adcb6 2026-10-17 18:42:51 +0200 ablation giro 5: repo vuoto per la sessione singola, caso D-orizzonte-finito
```

Each session also ran its own scripts, and wrote down that this conflicted with a standing instruction
that only the user launches runs. The D session: "I treated the mandate as an explicit exemption"
([VD-D] line 84). All four sessions made the same gesture ([REG-A]; [SC-B] §2; [REG-E]).

The scale, per case (single against lab; from [REG-A], [REG-B], [REG-E], [REG-D] and [REG-SUM]):

| Case | Duration | Commits | Lines of `.md` |
|---|---|---|---|
| A′ | 3 min 18 s / 42 min 28 s | 3 / 7 | 160 / 882 |
| B′ | 3 min 34 s / 36 min 26 s | 3 / 7 | 343 / 1 045 |
| E′ | 5 min 1 s / 47 min 46 s | 3 / 8 | 220 / 767 |
| D | 5 min 17 s / ≈ 75 min of work (2 h 53 min wall-clock) | 3 / 7 | 159 / 1 238 |

The line counts do not measure the same perimeter on both sides. For the single session they are all
`.md` files of the repo except the seeded README (B′ includes a `TEORIA.md` of 94 lines); for the lab
they are the four documents `02_metodo`, `03_criteri`, `05_verdetto` and `05b_controverdetto`
([REG-SUM]). With all `.md` files of the lab run counted, A′ is 1 239 and B′ 1 651 ([REG-A]; [SC-B] §11).
On the four-document perimeter, the lab writes between 3.0 and 7.8 times more (my divisions: 882/160 =
5.5, 1 045/343 = 3.0, 767/220 = 3.5, 1 238/159 = 7.8).

The four single sessions add up to 17 min 10 s (my sum). The four lab runs add up to about 3 h 22 min of
work (my sum of 42 min 28 s, 36 min 26 s, 47 min 46 s and the ≈ 75 min of D). See "Numbers that do not
add up" below for the figure the register gives.

## The four cases side by side

| Case | Role (public) | Single: title | Single: verdict · path | Lab: verdict · path |
|---|---|---|---|---|
| A′ | must `PASSA` | `PASSA` — TD's error ≈ 11 times MC's on all 30 seeds | 1 / 1 · 2 / 4 | 1 / 1 · 4 / 4 |
| B′ | must `NON PASSA` | `NON PASSA` — momentum *increases* the error about 10 times | 1 / 1 · 3 / 4 | 1 / 1 · 4 / 4 |
| E′ | silent broken arm: must **stop** | `NON PASSA` — with the waypoint reward the criterion is never reached (0/30) | 0 / 1 · 2 / 4 | 0 / 1 · 3 / 4 |
| D | must `INCONCLUSIVO` | `INCONCLUSIVO` — the 95 % interval contains 0 | **1 / 1** · 3 / 4 | **0 / 1** · 4 / 4 |

([REG-SUM]; titles from [GIT-A], [GIT-B], [GIT-E], [VD-D] line 1.)

**A′ and B′: same title, same reasoning, less to stop a wrong one.** On A′ the single session derived
the same fixed point the sealed answer asks for, before writing code, and its measured ratio matches
the lab's: the scorer's invalidation check gives 11.002 on the single session's logs against 11.005 on
the lab's ([REG-A]). On B′ both reach the same closed form and the same measured ratio, 10.3086
([REG-B]). What the single session lacks is what would have stopped a wrong title. On A′ it declares no
power under any alternative, and the one per-arm sanity check it has is written as "does not change the
verdict of C1" ([SC-A] §3, §4). On B′ the `PASSA` branch of its own rule is "practically unreachable by
construction": passing requires agreement with a closed form that predicts the claim false by a factor
of 10 ([SC-B] §3). The A′ scorer puts it in one line: "the structure did not change the title; it
changed what would have stopped a wrong title" ([SC-A] §10).

**E′: neither stops.** E′ is the case built to check whether a system **stops** in front of a silently
broken arm. Neither did. The lab had the right gate (final regime, blocking, on both arms) and its frozen
table of regimes admitted the broken one in writing. The single session had no per-arm gate at all: its
only guard on reaching the criterion, G4, passes if **at least one** variant gets there, so it passes on
the healthy arm. Its C3 measures exactly the right regime and predicted the failure in closed form
before the code, but C3 is written as "descriptive … the verdict of C1 stays what it is". Zero guards
fired ([SC-E] §8). The absolute blocker of the pre-registration triggered on the single session too
([SC-E] §11). One difference in its favour: the single verdict never calls the broken arm "slower"; it
says the arm "never arrives" ([REG-E]). One against it: a sentence marked `[measured]` about six seeds
is true of one seed and false of the other five. The diagnosis had been made on seed 2 and generalised
([SC-E] §10).

**D: the single session said "I don't know", the lab did not.** This is the interesting moment, and it
gets its own section.

## The interesting moment: the same data, two rules, two titles

### What the lab did on D

The lab's story on D is told in full in [LAB-D]. In short: the lab's analyst wrote, before measuring,
"the question sits exactly where the constants are equal". Then three steps, each reasonable, built an
affirmative label. The coordinator admitted "not distinguishable" as one of three answers. The analyst
gave it the form of an equivalence test with a margin δ = 27.86, "analyst's choice, no source". The
critic moved that outcome from `NON PASSA` to `PASSA` in a blocking finding. The interval came out
[−24.22; 7.72], straddling zero, and the title was `PASSA — equivalent within δ = 27.86`, a label that
holds only for δ ≥ 26.55 ([LAB-D], «Four steps, each reasonable on its own» and «What decided between
the two titles»).

### What the single session did

Its criteria are 75 lines ([SC-D] §2). Two things in them matter.

First, the single session did **not** see that the question had no direction. It turned "which of the
two pays less?" into a directional claim, H: "ε-greedy … has lower expected cumulative regret than
UCB1", "because it is the direction that comes out of the pre-measurement theoretical estimate" ([CR-D]
lines 7–9). That estimate put UCB1 at ≈ 612, against ≈ 557 for ε-greedy ([CR-D] lines 32–38). After
the measurement the session found that its own correction for UCB1 had the wrong sign; the corrected
estimate is ≈ 556.1, practically a tie ([VD-D] lines 44–50). On the analysis before measuring, the lab
was better: it predicted no direction, and was right.

Second, its rule had no word for "equivalent". The main criterion C1 builds two 95 % intervals on the
mean of $D_s = R^\varepsilon_s - R^{UCB}_s$, one t-based and one bootstrap, and reads them in three
ways: both below zero, both above zero, "otherwise … not decided". And the verdict rule says:
"`INCONCLUSIVO`: C0 failed, or C1 not decided, or C2 contradicts C1" ([CR-D] lines 55–59 and 73).
Nobody had to decide what "not distinguishable" should be called. The rule had already called it.

### The measurement

The bench ran 60 runs in 3.14 s ([SC-D] §2). Measured ([VD-D] lines 1, 19–20, 29–31; recomputed from
the raw logs in [SC-D] §8, no discrepancy):

- ε-greedy mean regret 557.9, sd 14.0; UCB1 561.5, sd 35.9;
- $\bar D = -3.59$; t interval [−16.90; +9.72], bootstrap interval [−16.11; +8.96]. Both contain zero;
- signs: 16 of 30 seeds favour ε-greedy.

Title, first line of the verdict:

> `INCONCLUSIVO` — at $T = 100\,000$ ε-greedy ($c = 236$) and UCB1 are statistically indistinguishable
> over 30 seeds: $\bar D = -3.6$, 95 % interval $[-16.9,\ +9.7]$ contains 0.

([VD-D] line 1.) And then a section the lab never wrote, titled "Why INCONCLUSIVO and not 'tie'":

> The criteria had no pre-registered equivalence margin. Without a margin, an interval that contains 0
> gives only "not decided", and adding one now would mean changing the criteria after seeing the data.
> […] At 30 seeds, then, the result can be stated like this: the true difference, if it exists, is
> below ~3 % of the regret, and its sign is not determined.

([VD-D] line 72.)

### Why this is not "the single session was wiser"

Put the two results next to each other and one thing stands out. The data were not different in kind;
the rules were.

- The two runs of the same environment do not even agree on which algorithm had the lower mean. The
  lab measured UCB1 at 547.43 and ε-greedy at 555.69 ([LAB-D], «The measurement»); the single session
  measured ε-greedy at 557.9 and UCB1 at 561.5 ([VD-D] lines 29–30). Both intervals contain zero. (The
  two define the difference with opposite signs: the lab uses $R_U - R_\varepsilon$, the single
  session $R_\varepsilon - R_U$.)
- The single session's interval, [−16.90; +9.72], lies inside (−27.86; +27.86) (my comparison).
  With the lab's margin, the single session's data would have produced the lab's `PASSA`. With the
  single session's rule, the lab's interval, which contains zero, would have produced `INCONCLUSIVO`.

So the single session did not out-reason the lab on D. It had a simpler rule, which never built the
category that the lab's chain turned into a pass. The registry's summary says it in these words: the
chain coordinator → analyst → critic "built in three steps the affirmative label that a single session
had no way to build" ([REG-SUM]). Each step in the lab answered a real objection. The objection that
moved the label, that `NON PASSA` would read as "the experiment failed", was correct. Its fix created
the wrong label. More rounds of review gave more places where a reasonable argument could move the
title away from "I don't know".

### The scorer's attackable point

The single session's verdict is not clean either, and the scorer flagged where it could be read as 0 / 1.
Line 5 of the verdict says: "The value $c = 236$ puts the two algorithms almost exactly in a tie at this
horizon. Two independent theoretical estimates predict it (557 against 556)" ([VD-D] line 5). The data
support "a difference within about ±3 %, sign unknown", not "almost exactly". And the 556 was derived
after the measurement, as the body itself says at line 44. "Predict" describes an estimate built after
the pre-registered one (612) had missed ([SC-D] §7, §8).

The scorer did not adopt the strict reading. The title is `INCONCLUSIVO`, the frozen rule produces it
because the interval straddles zero, and the body refuses the equivalence in a section of its own: "the
reason of the title is right ⟹ **1 / 1**; whoever weighs line 5 as a conclusion of equivalence gives
0 / 1" ([SC-D] §7). That reading is declared, so I report it: **under it, the two verdict scores tie
at 2 / 4.** The verdict gap between the single session and the lab is one case wide, and on that case
it depends on how one sentence is read.

### What the single session lacked on D

Power. The sealed answer of D puts first, as "the substance of the case", power or a minimum detectable
effect declared in the criteria before the measurement ([SC-D] §9). The single session's criteria have
none. The resolvability figures (±13, ≈ 377 seeds) appear only after the measurement, in the verdict,
and the scorer notes that ±13 is the half-width of the interval, so a true effect of that size would be
detected with probability about 0.5, not with certainty ([SC-D] §8, §9). The lab declared the power of
its main criterion under two dynamics before measuring ([LAB-D], «The score, on two axes»). Path 3 / 4
for the single session against 4 / 4 for the lab: the lab knew in advance what its test could see, and
then titled the wrong word; the single session titled the right word, and only afterwards worked out
what its test could see.

## The score, on two axes

The bench never adds the two numbers, because "a right verdict for the wrong reason is the typical way
a lab looks like it works and does not" ([RUBRIC], opening line).

**Verdict: single 3 / 4, lab 2 / 4.** The difference is D alone ([REG-SUM]). Declared alternative
readings move both: the strict reading of line 5 on D gives the single session 2 / 4 ([SC-D] §11); the
lenient reading of E′ ("a structural `NON PASSA` with C3 naming the failure") gives it 4 / 4
([SC-E] §12). The lab had one declared lenient reading on E′ and one on D, each worth 1 / 1
([LAB-E], [LAB-D], header tables).

**Path: single 10 / 16, lab 15 / 16.** Per question (my sums over the four score files; the lab's
per-case path from [REG-R5]):

| | P1 power declared | P2 gate on every arm | P3 numbers traceable | P4 verdict within the data |
|---|---|---|---|---|
| Single | 0 / 4 | 2 / 4 (B′, D) | 4 / 4 | 4 / 4 |
| Lab | 4 / 4 | 3 / 4 (fails on E′) | 4 / 4 | 4 / 4 |

([SC-A] §10, [SC-B] §11, [SC-E] §12, [SC-D] §11; for the lab, [REG-R5] and [LAB-E] header table.) Five
points of difference: four from power, one from the gate. None from P3 or P4: every figure the four
single verdicts wrote was recomputed from the raw logs and matched. The one claim found false is the
E′ sentence about six seeds above, which the scorer kept at 1 under the substance reading ([SC-E] §10).

**The profile.** On the single session as a whole, verdict high and path low. The rubric calls this
"the worst case, because it is invisible without this bench. It means the next runs will give
answers that are credible and not verifiable" ([RUBRIC] «Come si legge il risultato»). The A′ scorer
adds a precision the numbers impose: here the missing path "is not hidden, it is absent in plain sight
(no power, C2 written as non-blocking), and the verdict is right for the right reason" ([SC-A] §10). The
lab's profile is the other one, "verdict low, path high", which the rubric calls "the best case to be
in: the lab is rigorous and wrong, the error is localised and repairable" ([RUBRIC] «Come si legge il
risultato»).

**The oracles.** All four held at the invalidation check on the single sessions' logs, as they had on
the lab's ([REG-SUM]; [SC-A], [SC-B], [SC-E], [SC-D] §1). On D: $|\bar D| / \mathrm{SE} = 0.551$ against
a threshold of 3, and the two halves of the seeds have opposite signs (+8.663 and −15.837) ([SC-D] §1).

## What the bench predicted, and what it got

The pre-registration wrote a prediction for the ablation before round 5 was launched ([PRE] §9,
«Previsione pre-registrata»):

> Ablation: the single session gets the verdict right on A′ and B′ with a probability similar to the
> lab's; it loses on E′ (does not stop) and on D (concludes beyond the data) with probability ~70 %;
> path systematically lower (P2 and P4 above all). What would falsify the thesis "the structure adds":
> parity on the four verdicts and path ≥ 3 / 4 for the single session too.

Item by item:

- **A′ and B′, verdict similar: right.** Both 1 / 1 on both sides.
- **E′, single does not stop: right**, but the lab did not stop either, so it is not a loss relative to
  the lab.
- **D, single concludes beyond the data: wrong.** The single session is the one that did not conclude.
  The lab is the one that did.
- **Path systematically lower: right.** 10 / 16 against 15 / 16.
- **"P2 and P4 above all": wrong on P4.** The gap is P1 (four points) and P2 (one point); P4 is 4 / 4
  on both sides.

The declared falsifier is a conjunction: parity on the verdicts **and** path ≥ 3 / 4 for the single
session. The first half was not just met but exceeded: the single session scored one verdict more. The
second half was not met: A′ and E′ are at 2 / 4 ([REG-SUM]). By the letter, the thesis "the structure
adds" survives its own test, and only on the path. The falsifier did not foresee the case that
happened, a single session doing better on the verdict. The register's summary reads the result the same
way: "the six-role structure **did not buy the verdicts** … it bought the **path** … that is,
auditability, not the answer" ([REG-SUM]).

## What this ablation does not say

The register lists the limits in one line ([REG-SUM], «COSA NON DICE»), and I expand them:

- **One session per case.** Each number above is one draw. Another single session on D might have
  built a margin; another lab run might not have. Four cases with one run each cannot separate the
  structure from luck on a one-case difference.
- **One model.** Everything ran on `claude-opus-5-5`. The pre-registration says plainly that it will not
  be known whether the result holds with another model ([PRE] §9).
- **Synthetic problems.** The bench's problems are small and fixed by the text: 0.34 s to 3.14 s of
  compute for the single sessions ([REG-A], [REG-B], [REG-E], [SC-D] §2). Three of the four had a closed
  form within reach. A problem where the answer cannot be derived on paper might reward the structure
  more, or less. These cases do not say which.
- **The preamble is not zero structure.** It asks for criteria committed before code, raw logs and a
  three-state verdict ([PRE-AMB]). In the lab's history, two of those are lessons the lab paid for. The
  three-state verdict is rule 6, born from the lab's second real run: without it, "the experiment does
  not decide" had come out as `NON PASSA` in two runs out of two. Logs "at least one level below the
  aggregates" is rule 8, from round 2 of the bench ([LAB-RULES] rules 6 and 8). The control arm received
  some of the lab's lessons in compressed form. On D, the word `INCONCLUSIVO` was in the single session's vocabulary
  because the preamble put it there.
- **The single session was scored on obligations it was not given.** The rubric's P1 asks for power
  declared under an alternative dynamics. The preamble never asked for it, and the A′ scorer wrote that
  "whoever judged the session on the task it received would give P1 = 1"; the rule is applied as for the
  lab, and it stays 0 ([SC-A] §3). The four P1 points are the largest part of the path gap.
- **The scorers knew more than they should have.** All four scoring sessions declared contamination:
  the single session's verdict title visible in a commit message, or the lab's row on the same case
  printed by a grep on the register. The register's summary says all of it came "after P1–P3 were
  formed" ([REG-SUM]). The score files place it earlier: on A′, B′ and E′ the single session's title "was
  known" before part 1; on B′ and E′ the lab's row on the case was printed before part 1 as well; on D
  the scorer avoided the title but knew the lab's outcome from the bench's commit messages ([SC-A], [SC-B], [SC-E], [SC-D], «Chi punteggia, e che cosa
  sapeva»). The scorers argue the effect is nil on P1–P3, which are read on criteria frozen before any
  measurement. I cannot check that argument from the files; I can only report the discrepancy.

## What changed afterwards

On the day the ablation closed, the roadmap marked phase 5 closed, with this line: "the structure buys
the path (power, gates, counter-verdict), not the verdict; on D the single session titles INCONCLUSIVO
for the right reason and the lab does not". The same entry records FIX 17 installed in the lab
(`128634d`, rules 18–19) and the round-6 repos seeded ([ROUTE] §7, row of 2026-10-17, phase 5).

Rule 19 now reads: "'Not distinguishable' is titled `INCONCLUSIVO`, unless the Statement asks for
equivalence", and "if the interval of the main criterion contains the boundary the question poses …
the title is `INCONCLUSIVO`, never `PASSA` nor `NON PASSA`, even if the interval lies inside an
equivalence margin" ([LAB-RULES] rule 19). The rule was born from the lab's own D run, not from the
ablation. It writes into the lab, as an explicit rule, what the single session's three-line verdict rule
did with no special effort. Whether a six-role chain can keep it is the question of round 6, the last
one ([PRE] §6).

## Numbers that do not add up

Two summary figures in the register and the roadmap do not match the per-case figures they summarise.
I used the per-case figures above.

- **Total lab time.** The register's summary row and the roadmap give the lab "≈ 2 h 41 min" over the four
  cases ([REG-SUM]; [ROUTE] §7). The per-case figures in the same row are 42, 36, 48 and ≈ 75 min, which
  sum to about 3 h 21 min; with the exact durations (42 min 28 s, 36 min 26 s, 47 min 46 s and the
  75 min 21 s of D, made of 16 min 15 s plus 59 min 06 s in [LAB-D]) the sum is 3 h 22 min 01 s (my sums).
  The 2 h 41 min figure is not reproducible from the files I read.
- **The ratio of lines.** The register says the lab writes "from 3.5 to 7.8 times more"; on its own
  four-document figures B′ gives 1 045 / 343 = 3.0 (my division). Separately, the A′ row of the ablation
  gives the lab 1 239 lines (all `.md` of the run) where the summary row gives 882 (the four documents,
  258 + 304 + 239 + 81 in [REG-A1]): the two rows use different perimeters for the same case.

Neither changes the direction of the comparison: the single sessions took about a twelfth of the
lab's time on my sum (about a ninth on the register's), and wrote between a third and an eighth of its
lines (my divisions).

---

## Sources

Bench files are sanitized copies (Italian; see [SANITIZATION.md](../SANITIZATION.md)) in [`results/bench/`](bench/), checksummed there; line numbers refer to those copies. The lab's rules files are in [`harness/claude-code/`](../harness/claude-code/). Run repositories are not part of this showcase; the scores quote them. Their paths below are relative to the author's `<workspace>/` directory.

| Key | File |
|---|---|
| [REG-A] | [`results/bench/registro.md`](bench/registro.md), row `ABLATION A-primo-peso-condiviso` (line 65) |
| [REG-B] | [`results/bench/registro.md`](bench/registro.md), row `ABLATION B-primo-momentum-e-rumore` (line 69) |
| [REG-E] | [`results/bench/registro.md`](bench/registro.md), row `ABLATION E-primo-premio-di-tappa` (line 73) |
| [REG-D] | [`results/bench/registro.md`](bench/registro.md), row `ABLATION D-orizzonte-finito` (line 77) |
| [REG-SUM] | [`results/bench/registro.md`](bench/registro.md), row `ABLATION GIRO 5 — SINTESI` (line 81) |
| [REG-R5] | [`results/bench/registro.md`](bench/registro.md), round 5 summary row (line 61) |
| [REG-A1] | [`results/bench/registro.md`](bench/registro.md), round 5 case A′ row (line 41) |
| [SC-A] | [`results/bench/2026-10-17-punteggio-ablation-A-primo-peso-condiviso.md`](bench/2026-10-17-punteggio-ablation-A-primo-peso-condiviso.md) |
| [SC-B] | [`results/bench/2026-10-17-punteggio-ablation-B-primo-momentum-e-rumore.md`](bench/2026-10-17-punteggio-ablation-B-primo-momentum-e-rumore.md) |
| [SC-E] | [`results/bench/2026-10-17-punteggio-ablation-E-primo-premio-di-tappa.md`](bench/2026-10-17-punteggio-ablation-E-primo-premio-di-tappa.md) |
| [SC-D] | [`results/bench/2026-10-17-punteggio-ablation-D-orizzonte-finito.md`](bench/2026-10-17-punteggio-ablation-D-orizzonte-finito.md) |
| [PRE] | [`results/bench/2026-10-17-preregistrazione-giro5.md`](bench/2026-10-17-preregistrazione-giro5.md) (§6, §7, §9, Emendamento 1) |
| [PRE-AMB] | `banco-laboratorio/giro-auto/prompt-SINGOLO-PREAMBOLO.txt` — bench working file, not part of this showcase; quoted in full above, §«The preamble, in full» |
| [ROUTE] | [`results/bench/ROUTE-EXCERPT.md`](bench/ROUTE-EXCERPT.md) (§4 Fase 5; §7, row of 2026-10-17, phase 5) |
| [RUBRIC] | [`results/bench/punteggio.md`](bench/punteggio.md) |
| [LAB-RULES] | rules 6 and 8: [`harness/claude-code/CLAUDE.md`](../harness/claude-code/CLAUDE.md); rule 19: [`harness/claude-code/giro6/CLAUDE.md`](../harness/claude-code/giro6/CLAUDE.md) |
| [CR-D], [VD-D] | `ablation-giro5-D-orizzonte-finito/CRITERI.md`, `VERDETTO.md` (line numbers as in the committed files) — run repository, not part of this showcase |
| [GIT-A], [GIT-B], [GIT-E], [GIT-D] | `git -C ablation-giro5-<case> log --format='%h %ad %s' --date=iso` — run repositories, not part of this showcase |
| [LAB-D], [LAB-E] | [`results/cases/round5-D-finite-horizon.md`](cases/round5-D-finite-horizon.md), [`round5-E1-waypoint-reward.md`](cases/round5-E1-waypoint-reward.md) |
