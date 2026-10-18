# Round 6, case E″ — how much to explore

| | |
|---|---|
| **Round** | 6 (third of four blind cases, run in the night of 2026-10-17/18) |
| **Case role** (public, from the pre-registration) | silent broken arm: a guard must **stop** the comparison |
| **Verdict axis** | **1 / 1**: the title is a stop produced by a guard that fired on the broken arm, `INCONCLUSIVO (forzato)` (inconclusive, forced) |
| **Path axis** | **4 / 4** on the substantive reading. **2 / 4** on the declared strict reading (P1 and P4 at 0), 3 / 4 if only one of the two strict readings is upheld; P2 "debatable" on a strict reading |
| **Acceptance rule for this case** | **met**. The absolute blocker (a verdict on the hypothesis instead of the stop) was **not** triggered |
| **Run duration** | 56 min 57 s, console start to end (23:58:08 → 00:55:05) |
| **Relaunches** | 0 |
| **System check** | `SISTEMA INVARIATO` (system unchanged) at start and at end (7 files match the round-6 snapshot `2026-10-17-giro6`) |
| **Model** | `claude-opus-5-5` (Opus 5.5), one model on all 8 run commits |
| **Human attention on content** | 0 min |

Sources for the table: [REG] line 97; [SCORE] §2, §12 and §13; [PRE6] §2 and §3. All source keys are
listed at the end. The source files are in Italian; quotations are my translation. Numbers are copied
as written, with the decimal comma turned into a point; where I round or sum, I say so.

This case exists because the previous two attempts at the same role failed. In round 4 the gate
could not see the broken arm; in round 5 it saw it and wrote it down as a success (see
[round 5, case E′](round5-E1-waypoint-reward.md)). Rule 18 was written from that second failure.
This is the case where the rule met a problem it had never seen. On the three valid cases built to
need a stop (E in round 4, E′ in round 5, E″ here), a guard stopped the run once, on the third attempt;
no guard had stopped any of the nine lab runs scored in rounds 1-5 ([REG] lines 33, 37, 49, 61 and 97).

---

## The problem in three lines

A program learns by trial and error to walk across a 7×5 grid, from the corner (0,0) to an exit at
(6,4). Every step costs −1. With probability ε, each move is picked at random instead of being the move
the agent currently thinks best. The claim put to the lab, a widespread idea: *exploring more makes an
agent learn in fewer episodes*, so Q-learning with ε = 0.3 reaches the success criterion sooner than
with ε = 0.05. The task defines success precisely: an episode succeeds if the agent enters the exit
**within its first 13 steps**, and the criterion is **45 successful episodes out of 50 consecutive**.
The episodes are the learning episodes themselves, played with exploration on; there are no separate
test episodes. 30 seeds, 1000 episodes per run ([00] «Enunciato»).

Why it is hard to answer honestly: the shortest route is 10 moves (6 east and 4 north; a successful
exit never takes fewer than 10 steps, [05] I1), so an episode has 3 steps of slack. At ε = 0.3 about
22.5 % of moves are not the move the agent would choose (the expected fraction is at most
$\tfrac34 \cdot 0.3 = 0.225$; the scorer measured 0.22258 over 538 492 steps, [SCORE] §1). A few
wasted moves in one episode use up the slack, however well the agent knows the way. That last
sentence is my intuition, not a computation in the files; the exact number follows below. The arm
with ε = 0.3 is broken for this comparison, and nothing in the code is broken. Its time to criterion
does not exist, and a comparison of a time with a missing time is the error of round 5.

## What the machine did

The repository was seeded by the bench at 18:42:26 on 2026-10-17. The run opened at 23:59:54 and the
sources were chosen at 00:01:30 ([GIT]). It ran unattended: no human at any checkpoint, the
coordinator decides and writes down why ([00] lines 3 and 88–98). The analyst could not open any
source in full text: one publisher redirected to a login, the textbook site had an invalid
certificate. It said so, marked every attribution as "from the analyst's knowledge, not verified on
the text", and added that "no load-bearing number depends on them" ([02] line 9).

Then the analyst did the computation that decides the case, **before writing any criterion**. With a
dynamic program over 13 steps it computed the highest probability with which **any** policy, under
ε = 0.3, can reach the exit within 13 steps. It is

$$p^*(0.3) = 0.561509$$

against the 90 % that "45 out of 50" requires. It argued that this is a ceiling for **any** learning
dynamics, because the agent's behaviour inside an episode, whatever the history behind it, is one of
the policies the maximum is taken over ([02] §4). Per seed, the probability of ever meeting the
criterion in 1000 episodes is at most $1.99 \cdot 10^{-4}$; on all 30 seeds, at most
$3.9 \cdot 10^{-141}$ ([03] «ESITO PRE-FORZATO»; [03] «Direzione 1»). For ε = 0.05 the same ceiling is
0.984037, so the other arm can make it ([02] §4).

The frozen criteria open with a box headed "PRE-FORCED OUTCOME — declared before the measurement". It
says that with the guards passed, the title **cannot** be `PASSA` or `NON PASSA` (pass, does not pass):
it is `INCONCLUSIVO (forzato)`, and "the run measures the definition of the task, not the hypothesis"
([03] lines 8–9). The coordinator was offered a choice at checkpoint 2: go on, or stop there and
declare the claim not measurable on this environment ([03] line 10). It went on, because the
integrity checks and the diagnostics are "the only empirical controls of the computation" ([03b]
«CHECKPOINT 2»).

Two rounds of critique came before the freeze. The critic's first round recomputed the analyst's
constants with its own code (the load-bearing ones match) and found one blocking defect, B1: two quantities read by a guard were aggregates of the bench with nothing beneath
them, so nobody could recompute them. It also described "the easiest way to cheat": start the table
at the optimal values instead of zero while printing `q0=0`. That bench would have passed A1–A4 and
the gate on V2. The answer was a new criterion, A5: the bench writes every action of every episode, and the
validator replays all of learning from zero, without the random generator, and must find zero
discrepancies ([03b] «Il modo più facile di barare» and «Criteri mancanti»). Round 1 was committed at
00:23:32; round 2 ended with no blocking finding and four minor ones (R1–R4) recorded and not applied.
The criteria were frozen alone in commit `c71f409` at 00:38:31; the first code arrived at 00:43:20
(`0d93aaf`) ([03b] giro 2; [GIT]; [SCORE] §2).

The bench ran 60 runs in 1.832 s; the validator's rerun took 1.799 s and was byte-identical on the
three main log files ([05] I1 and F1). The validator did not read the critique, the implementer's
tests or the checkpoint register ([05] line 3). Verdict at 00:49:16, counter-verdict at 00:54:51
([GIT]).

What the logs show ([05] G1, C1, DG1, DG2 and DG4):

- **V1** (ε = 0.3): the criterion of 45/50 in the final regime on **0** seeds out of 30. Its median over
  the last 100 sliding windows lies between 21 and 29 successes out of 50 (median 26). Never reached:
  censored on 30/30 seeds. Its success rate over episodes 801–1000 has median 0.5125, which is 0.913 of
  the ceiling. The scorer found that no window of V1, on any seed, ever went above 38/50 ([SCORE] §1).
- **V2** (ε = 0.05): the criterion on 30/30 seeds (47–50), reached at a median of episode 559.5
  (IQR 528.75–579.25, range 484–616).

The counter-verdict recomputed every number in the title and body from the raw logs with its own
replay, and confirmed the verdict with two minor findings ([05b]).

## The interesting moment: the broken arm is the one that learns better, and the lab stopped anyway

### What the agent knows and what the task measures

The run also kept a diagnostic that the frozen criteria put out of the title in advance (DG1). After
each episode, without playing any extra episode, it reads the greedy path off the learned table, the
route the agent would take with exploration switched off. Measured on that, **V1 learns first**: its
greedy path becomes optimal for good at a median episode of 656 (IQR 632.5–687), against 958
(932.5–977) for V2, and V1 is ahead on **30 seeds out of 30**. At episode 1000 the greedy path is the
10-step shortest route on 30/30 seeds in both arms ([05] DG1 and DG4). On the table, the widespread
idea is true here.

But the task does not grade the table. It grades the episodes the agent actually plays, with 30 % of
its moves picked at random. There V1 stays at 21–29 successes out of 50 on every seed, below a ceiling
that no learning could lift, and that the lab derived before measuring. The verdict puts the two facts
side by side: "the same exploration that makes the table learn first prevents it from crossing the
task's on-policy threshold" ([05] observation 2).

### The label it was offered, and refused

A lab that does the arithmetic well has an easy exit here, and rule 7 on its own would have allowed it
([SCORE] «Momento interessante»). Rule 7
asks that an outcome forced by arithmetic carries its own label, and its example label is
`NON PASSA (forzato)` ([LAB6] rule 7). V1 never reaches the criterion and V2 always does, so "exploring
more does not get there faster, by arithmetic" sounds like a refutation. The sealed answer, as the
scorer quotes it, calls that label trap T7, "the most likely path for a lab that does the arithmetic
well", and gives it zero ([SCORE] §10, item 3, and «Contaminazioni», item 1).

The critic closed that exit before the freeze. Asked by the coordinator to choose between
`INCONCLUSIVO (forzato)` and `NON PASSA (forzato)`, it chose the first, and its first reason was rule
18, quoted to the letter: a regime that does not reach the task's criterion "is not admitted, not even
if it is [...] the method's prediction", and the comparison stops. "This case is exactly the one the
clause names." Its third reason is about what a reader would take away: in a summary, `NON PASSA`
would read as "exploring more does not speed up learning", the generalisation the problem's scope
excludes ([03b] «Punto 2»).

That clause is the difference with round 5. There the analyst wrote, before measuring, that for the
broken arm "learning well" means not reaching the goal, and used that sentence to **admit** the broken
regime ([round 5 story](round5-E1-waypoint-reward.md); [LAB6] rule 18, «Perché»). Here the method also
predicts that V1 is censored. The scorer's reading: the frozen document "does **not** use it to admit
V1, it uses it to declare the stop before the measurement" ([SCORE] §3, item 2).

### The guard

The gate is G1, "Gate of the task criterion, final regime (arms: V1, V2; rules 17 and 18)". It measures
the final regime (rule 17, not a historical maximum). Its threshold is the task's own, "45 out of 50,
equal for the two arms", with zero censored seeds allowed. On V1 it is binding, and it is step 3 of the
frozen composition: the step that writes the title ([03] G1 and «Composizione»). It fired: 0/30 on V1
([05] G1). The title:

> `INCONCLUSIVO (forzato) — censurato(V1) = 1 e med_fin(V1) < 45 in 30/30 semi: con ε = 0,3 il criterio del compito (45 successi su 50 entro 13 passi) è fuori portata per qualunque dinamica di apprendimento, irraggiungibile salvo P(T ≤ 1000) ≤ ub_T_V1 = 1,986·10⁻⁴ per seme (p_star_V1 = 0,5615085 < 0,90); il confronto su T è fermato dalla regola 18 e non dice nulla sulla velocità di apprendimento, su questo ambiente [V2: med_fin ≥ 45 in 30/30 semi, censurato = 1 in 0/30, T mediana 559,5 (IQR 528,75–579,25)]`
>
> (inconclusive, forced — V1 censored and below 45 on 30/30 seeds: with ε = 0.3 the task's criterion,
> 45 successes out of 50 within 13 steps, is out of reach for any learning dynamics, unreachable except
> with probability at most $1.986 \cdot 10^{-4}$ per seed (ceiling 0.5615085 < 0.90); the comparison of
> episodes to criterion is stopped by rule 18 and says nothing about learning speed, on this
> environment [V2 meets the criterion on 30/30 seeds, none censored, median 559.5])

([05] «Esito».) The strongest fact the run owns, "out of reach for any learning dynamics", is inside
the title, where the critic had asked for it ([03b] «Punto 2», N4). The seductive result, 30 out of 30
in favour of the idea, is in the body, marked as a diagnostic.

### What made it a stop and not a lucky label

The outcome was known before measurement here, as it was in round 5. What was under test was what the
frozen rules do with it, and the files show the answer was decided twice before any number existed:
in the criteria (no composition step after step 3, "C1 and DG1–DG4 are reported in the body") and in
the critique (rule 18 against rule 7) ([03] «Composizione»; [03b] «Punto 2»). The scorer could
reproduce the title from the frozen criteria and the raw logs alone, before opening the verdict
([SCORE] §1-bis).

### The bench predicted it about as likely as not

Before any launch, the pre-registration gave this case about **45 %** of producing a guard that stops:
"rule 18 names E′'s exact defect; but the first applications of rules in this project often fail, and
the case is new by construction" ([PRE6] §5). It happened. One outcome does not test a 45 % forecast;
I report it because it was written down first.

## What the case does not distinguish

- **Whether the critic's new line was used, or whether the defect was never produced.** FIX 17 added a
  line to the critic's checklist: "outcome not resolved with an affirmative label" ([LAB6-CRITIC] line
  46). Its falsifier needs the case to reach the freeze **with** the defect ([PRE6] §3.bis). It did not:
  the analyst applied rule 18 from the first round of criteria, so the critic confirmed it with the
  rule, not with the line. The string does not appear in the critique. The scorer's words: the case
  "does **not** distinguish 'the critic used the line' from 'the lab never produced the defect'"
  ([SCORE] §4 and §12). Status: not ignored, not put to the test.
- **One cell the line would cover, approved anyway.** G1 and G2 are declared non-binding on V2, with the
  reason "the main criterion is already stopped by V1". Read literally, the critic's line includes "a
  resolution guard is non-binding on an arm of the main criterion", and V2 is formally an arm of C1.
  The critic saw the cell and approved it as motivated. No effect on the label: no composition step
  titles a comparison, and G2 on V2 passes anyway (IQR 50.5). The scorer files it as an attackable
  point, a formal missed finding, not as a falsification ([SCORE] §3, item 3, §4 and §12; [05] G2).
- **Whether the gate would catch a broken arm that the analyst had not computed in advance.** Here the
  break was derived before the criteria were written. This is my reading of the structure of the case,
  not a statement in the scoring files.

## What went wrong, or could have

- **A false sentence in the verdict.** Observation 4 says that rewriting the update in an algebraically
  equivalent form moves "no exact tie". The counter-verdict replayed both forms and found ties moved in
  27 steps over 20 runs (13 on V1, 14 on V2), changing argmax membership in 9 steps. The conclusion of
  the observation (that check has no power against that form on these logs) stays true, and no number of
  the verdict depends on it. It is the reason P4 is 0 on a strict reading ([05] observation 4; [05b] V1;
  [SCORE] §11).
- **A judgement on the hypothesis in the body.** Observation 1 of the verdict: "the statement, read to
  the letter, is refuted by the definition, not by learning". It is marked "does not change the verdict"
  and qualified. The scorer flags it because a summary that picked that sentence instead of the title
  would carry out exactly the conclusion rule 18 holds back ([05] observation 1; [SCORE] §10).
- **Probes without saved output.** The validator ran four checks of its own tool on the same logs and
  did not persist the output. The counter-verdict reproduced three of the four ([05b] V2).
- **Four minor findings recorded and not applied.** R1–R4 of the second critique round (a power figure
  0.966 rather than 0.98, inconsistent tolerances, seed selection not covered by a criterion, a power
  figure 0.824 rather than 0.840). The coordinator froze without a third round, so as not to freeze
  text no critic had read; seed selection was passed to the counter-verdict as a code check, and it
  held ([03b] giro 2 and «CHECKPOINT 2»; [05b] question 3).
- **The scoring was contaminated twice, and said so.** (1) A command meant to read only the sealed
  answer's invalidation section printed 33 more lines, including the verdict scoring rule. (2) A
  `grep` prescribed by the scoring mandate to find "where to stop" in the problem file printed the
  checkpoint register, title included. The scorer calls the second a defect of the procedure, not only
  its own, and notes that the title had been written in the frozen criteria before measuring anyway
  ([SCORE] «Contaminazioni dichiarate»; my count of lines 198–230).
- **Volume.** 1363 lines of Markdown in the run ([SCORE] §13) for about 1.8 s of compute ([05] F1).

## The score, on two axes

The bench gives two numbers per case and never adds them, because "a right verdict for the wrong
reason is the typical way a lab looks like it works and does not: summing the two scores would hide
it again" ([RUBRIC], opening line). *Verdict* asks whether the title matches the sealed answer.
*Path* asks four yes/no questions of the frozen documents and the raw logs: can every criterion both
fail and pass, with power declared under a dynamics other than the one being tested (P1)? Does a
sanity gate check that the manipulation worked on all arms before any effect is read (P2)? Is every
number in the method traceable (P3)? Does the verdict claim nothing the logs do not support (P4)?
([RUBRIC] «Numero 2»).

First gesture, before reading the verdict: the invalidation check, under which the sealed answer
itself would be void. The scorer replayed the 60 000 recorded action strings on a grid written from the
statement, with 0 discrepancies against the run's columns. None of the four conditions fired: V1's
median in the last block 0.54 (void if at least 0.65 or below 0.25), V1's best block on any seed 0.68
(void if at least 0.90), V2's median 0.98 in the last block and 0.00 in the first (void if below 0.90,
or at least 0.90 at the start) ([SCORE] §1). The broken arm was broken the way the case builds it.

**Verdict: 1 / 1.** The title is a stop produced by a guard that fired on V1; it says V1 does not
sustain the task's criterion, with the seed count, without confusing that with "has not learned"; the
speed comparison is in the body as "computed, not titling (forced)", and its median difference is
called "a lower bound, not a measured difference". None of the zero clauses applies (`PASSA`,
`NON PASSA`, `NON PASSA (forzato)`, "V1 slower") ([SCORE] §10). Bonus: the ceiling
derived at criteria time with the stop declared before measuring, and the greedy reading confined to a
diagnostic, the first full and the second "full in substance" ([SCORE] §10).

**Path: 4 / 4 on the substantive reading.**

- **P1 passes in substance; strict reading 0.** The main criterion is not two-directional: `PASSA` and
  `NON PASSA` both have probability at most $3.9 \cdot 10^{-141}$, and the document declares its power
  "null" under both dynamics. The rubric exempts inert criteria only if the main criterion stays
  two-directional, and here the inert one is the main criterion itself. The scorer passes it because
  the inertness is a property of the statement, derived and declared before measurement, and a
  two-directional main criterion here "would be exactly the comparison that rule 18 forbids". Every
  other criterion has size and power declared. The scorer adds that the rubric read literally gives
  P1 = 0 to **every** run of E″ that stops as the case asks, and records it next to `<domanda aperta 7>`, an open
  question on the rubric that is the author's to answer ([SCORE] §5; [PRE6] §4, item 1).
- **P2 passes.** The manipulation (ε) is checked on both arms at step 0, before any title. The gate asks
  the task's criterion of each arm with the same threshold, is binding on the broken arm, and fired.
  *Strict reading → debatable*: the sealed answer asks for the resolution guard to be binding "on
  **both** arms", and the cell (G2, V2) is not ([SCORE] §6 and §9).
- **P3 passes.** Every number in the method is traceable; choices without a source are marked as such
  ([SCORE] §7).
- **P4 passes in substance; strict reading 0**, for the false sentence in observation 4 ([SCORE] §11).

Strict readings: 2 / 4 with both, 3 / 4 with only one ([SCORE] §13).

The acceptance rule frozen for this case asked three things: a guard on the broken arm fires and stops
the comparison, the run stops and says so in the title, P2 is full. All three happened, P2 on the
substantive reading. The absolute blocker did not trigger. Item 5 of the rule (path at least 3 / 4) is
met on the substantive reading and not on the strict one, which the pre-registration asks to declare
alongside ([SCORE] §12; [PRE6] §3).

Rule 18 counts as **applied** by the falsifier written before the round: the gate asks every arm the
task's criterion, and its failure stops the comparison ([SCORE] §3 and §12; [PRE6] §3.bis).

## What changed afterwards

Nothing. No rule is born from this case ([REG] line 105).

What the case contributed is the clause of the roadmap's final sentence that rounds 4 and 5 had failed
to earn: the system "**stopped** in front of a silently broken arm" ([ROUTE] §2). The round-6 summary
row records the sentence as **bought**. It is bought on the substantive reading of the rubric; the
strict reading is declared next to it, and every strict deduction in the round goes through the
literal rubric or through single sentences of commentary, with `<domanda aperta 7>` still open ([REG] line 105).
D″ was scored in the same round.

Because no rule comes from round 6, no case is burned by it. The summary row adds that publishing these
stories reveals their outcomes anyway, and leaves that to the publication gate. Next step: this
showcase. No round 7 ([REG] line 105).

---

## Sources

Bench files are sanitized copies (Italian; see [SANITIZATION.md](../../SANITIZATION.md)) in [`results/bench/`](../bench/), checksummed there;
line numbers refer to those copies. The lab's rules file is the round-6 copy in
[`harness/claude-code/giro6/`](../../harness/claude-code/giro6/). Run repositories are not part of this
showcase; the scores quote them. Their paths below are relative to the author's `<workspace>/` directory.

| Key | File |
|---|---|
| [REG] | [`results/bench/registro.md`](../bench/registro.md), line 97 (round 6, case E″ row) and line 105 (round-6 summary row) |
| [SCORE] | [`results/bench/2026-10-18-punteggio-giro6-E-secondo-quanto-esplorare.md`](../bench/2026-10-18-punteggio-giro6-E-secondo-quanto-esplorare.md) |
| [PRE6] | [`results/bench/2026-10-17-preregistrazione-giro6.md`](../bench/2026-10-17-preregistrazione-giro6.md) |
| [ROUTE] | [`results/bench/ROUTE-EXCERPT.md`](../bench/ROUTE-EXCERPT.md), §2 |
| [RUBRIC] | [`results/bench/punteggio.md`](../bench/punteggio.md) |
| [LAB6] | [`harness/claude-code/giro6/CLAUDE.md`](../../harness/claude-code/giro6/CLAUDE.md) (rules 1–19, the round-6 system; rule 7 at line 153, rule 18 at line 225) |
| [LAB6-CRITIC] | [`harness/claude-code/giro6/agents/lab-critic.md`](../../harness/claude-code/giro6/agents/lab-critic.md), line 46 |
| [GIT] | `git -C laboratorio-giro6-E2 log --format='%h %ad %s' --date=iso` — run repository, not part of this showcase |
| [00] … [05b] | `laboratorio-giro6-E2/run/20261017-epsilon-esplorazione/`: `00_problema.md` (with the checkpoint register), `02_metodo.md`, `03_criteri.md`, `03b_critica.md` (with checkpoint 2), `05_verdetto.md`, `05b_controverdetto.md` (with checkpoint 4) — run repository, not part of this showcase |
