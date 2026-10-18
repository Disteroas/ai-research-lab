# Round 5, case E′ — the waypoint reward

| | |
|---|---|
| **Round** | 5 (third of four blind cases, run on 2026-10-17) |
| **Case role** (public, from the pre-registration) | silent broken arm: a guard must **stop** the comparison |
| **Verdict axis** | **0 / 1**: the lab titled `NON PASSA` (does not pass), a judgement on the hypothesis, where the sealed answer asked for a stop. 1 / 1 under one declared lenient reading |
| **Path axis** | **3 / 4**: the sanity gate (P2) failed. 2 / 4 under either of two declared strict readings, 1 / 4 under both, 4 / 4 under one lenient reading |
| **Acceptance rule for this case** | **not met**. The absolute blocker was triggered, for the second time in two attempts |
| **Run duration** | 47 min 46 s, console start to end (14:29:23 → 15:17:09) |
| **Relaunches** | 0 |
| **System check** | `SISTEMA INVARIATO` (system unchanged) at start and at end (7 files match the round-5 snapshot) |
| **Model** | `claude-opus-5-5` (Opus 5.5), one model for the whole run |
| **Human attention on content** | 0 min |

Sources for the table: [REG]; [SCORE] §2, §13, §14 and §15; [PRE] §2 and §3.2. All source keys are
listed at the end. The source files are in Italian; quotations are my translation. Numbers are copied
as written, with the decimal comma turned into a point; where I round or sum, I say so.

This is the most important case of the round, and it failed. Of the four cases in round 5, it is the
only one built to check whether the lab **stops**. It was the second attempt, and the lab did not stop.

---

## The problem in three lines

A program learns by trial and error to cross a 5×5 grid to a goal cell that pays +1. A common trick
for learning faster is to give a small bonus at a checkpoint halfway along. The claim put to the lab:
*with a bonus of +0.3 every time the agent enters cell (2,0), Q-learning reaches the success
criterion in fewer episodes than without it.* Two variants, V1 without the bonus and V2 with it,
30 seeds each, 1000 episodes per run ([00] «Enunciato»).

Why it is hard to answer honestly: the bonus is paid on **every** entry, so stepping in and out of
the cell pays forever. With these numbers, pacing back and forth is worth more than the goal. The
bonus arm does not learn slowly. It learns a different task, and learns it well. It never reaches the
goal criterion, so its "time to criterion" does not exist, and comparing it with the other arm's time
compares a number with something that is missing. The case puts the break in the specification, not
in a bug ([ROUTE] «Fase 3»), and asks whether the lab notices and stops instead of reporting a speed
difference ([PRE] §2).

## What the machine did

The repository was seeded by the bench at 13:00:56. The problem statement was committed at 14:30:16.
The run was unattended: no human at any checkpoint, the coordinator decides and writes down why
([GIT]; [00]). It used **one** scout, which went over its declared query cap (15 calls against 12)
and said so in its file; sources were committed at 14:32:00 ([01]; [GIT]).

The analyst then did the part that a good researcher would do, and did it before writing any
criterion. It proved by contradiction that the bonus is not "potential-based", the one form of
bonus that is guaranteed not to change what the best behaviour is (Ng, Harada and Russell). Then it
computed the value of the start cell under each variant in closed form. Without the bonus, the best
path is worth $\gamma^7 = 0.2097152$. With the bonus, going once through the checkpoint and then to
the goal is worth $0.4497$, and the back-and-forth loop on the checkpoint is worth
$0.3\gamma/(1-\gamma^2) = 2/3$. The margin is $0.217$. From 12 of the 24 non-goal cells, the start
included, the best policy of V2 goes to the loop and never reaches the goal ([02] «Analisi dell'MDP
modificato dal premio», points 1–3; [SCORE] §7 and §11). Its declared prediction was `NON PASSA`,
"the bonus slows down" ([02] «Previsioni dichiarate», P5). And it wrote the key sentence of the case
itself:

> The success criterion measures reaching the goal, not learning the MDP of one's own variant. For
> V2, "learning well" its own MDP means **not** reaching the goal: `03_criteri.md` handles this with
> a learning guard that accepts two regimes for V2.

([02] «Ipotesi e condizioni di validità».) The next section is about the second half of that sentence.

Two rounds of adversarial critique followed. Round 1 ended `DA RISCRIVERE` (to be rewritten) on one
blocking finding, and it was a real one: no criterion checked that the bench *executes* the specified
Q-learning. The step size, the exploration rate, the optimistic initial value $Q_0 = 2$ and the
tie-break were read as declared, not as run. The fix was a new guard, G5: the validator rewrites the
bench from the method document alone, and its logs must match the bench's exactly ([03b] giro 1, R1).
Round 1 was committed at 14:52:28. Round 2 ended `APPROVATO CON RISERVE` (approved with reservations).
The criteria were frozen in a dedicated commit (`03af039`, 15:03:40), and the first code arrived at
15:06:37 (`fa7c4af`) ([03b] giro 2 and checkpoint 2; [GIT]; [SCORE] §2).

The bench ran 60 runs in 2.11 s of compute ([REG]). The validator's reimplementation, written from the
method alone, matched the bench byte for byte on its first execution ([05] G5). The verdict was
committed at 15:11:52 and the counter-verdict at 15:16:53 ([GIT]). The rerun changed two log files by
one line each, a duration and a timestamp, and the proof is a git diff ([SCORE] §2).

What the logs show ([05] G3, C1, D1 and observation 3):

- **V1** (no bonus): reached 40 successes in 50 episodes on 30 seeds out of 30, at a median of episode
  268.5 (range 255–294); final regime `TRAGUARDO` (goal) 30/30.
- **V2** (bonus): reached it on **0** seeds out of 30. Final regime `TAPPA` (checkpoint) 30/30. In
  episodes 901–1000 its success rate has median 0.07 (range 0.04–0.13), with 16.59–17.78 checkpoint
  entries per episode. The greedy policy at the end loops on the checkpoint on 30/30 seeds. Its best
  50-episode window ever held 23–26 successes (median 24), peaking around episode 232, against a
  threshold of 40.

The counter-verdict recomputed every number from the raw logs and found the verdict supported, with
0 blocking and 4 minor findings ([05b]).

## The interesting moment: the rule was installed, and the broken regime was written into it

### Round 4: a gate that could not see

This case has a predecessor. In round 4, case E had the same role: one arm broken by its
specification, and a gate that should stop the comparison. That gate, C4, checked the **best**
window over the whole run. The optimistic initial values gave the broken arm an early bump in
success that later disappeared (window means 0.41 · 0.52 · 0.18 · 0.04), and the gate passed 30 times
out of 30 on the arm built to make it fire ([LAB] rule 17; [REG4]). That round scored verdict 1 / 1,
path 2 / 4 with P2 = 0, and the absolute blocker was triggered ([REG4]).

From that failure came rule 17 of the lab: the learning gate needs a condition on the **final or
sustained** regime, not only on a historical maximum, and its failure on the experimental arm must be
able to **stop** the comparison, not just qualify it ([LAB] rule 17).

The round-4 scorer had named a second half of the problem. The gate was "calibrated on 'has learned
something' when the fault is 'has learned perfectly the wrong task'" ([R4] §3). That half is not in
rule 17. A search of the lab's `CLAUDE.md` for "wrong task" and "requested task" (Italian: «compito
sbagliato», «compito richiesto») returns nothing; this is my own check, not a statement in the scoring
files.

### Round 5: a gate that saw everything

The lab installed rule 17 to the letter. Guard G3 reads the regime of each seed over episodes
901–1000, "not the historical maximum, which the optimism $Q_0 = 2$ could satisfy with an early
bump". It is blocking at step 4 of the composition, before the main criterion: "the failure stops the
comparison, on whichever arm it happens", with the same threshold of 24 seeds out of 30 on both arms
([03] G3). And the bump was there to be fooled by: the mean success of V2 per 50-episode window rose
0.195 · 0.271 · 0.353 · 0.415 · **0.445** and then decayed to 0.080 · 0.065 at the end ([SCORE] §1.1).
A gate on the best window would have seen a learner. G3 did not look at the best window.

Then the list of regimes that count as "learned":

> V1 → only `TRAGUARDO` (without the bonus no reward sustains `TAPPA`). V2 → `TRAGUARDO` **or**
> `TAPPA`: the first is the regime of the claim, the second is the optimum of its own MDP. Both are
> "has learned something that its reward sustains"; `NESSUNO` means the arm learned neither.

([03] G3.) So on V2, G3 stops only a learner that learned nothing at all. The orbit on the checkpoint,
which is exactly the broken arm the case builds, is written down as success.

A second guard would have caught it. G4, the resolution check born from round 4 (rule 12), fails if
the time-to-criterion has no spread. On V2 it was declared "reported, not binding", for this reason:

> V2 all censored (IQR = 0) is the **expected** outcome of the trap, and is readable *because* the
> control has resolution; stopping the run there would make the trap unobservable by construction.

([03] G4.) The critic approved both choices in round 1: "G3 — OK on both arms. V2 trapped: regime
`TAPPA` admitted, title readable (`NON PASSA`, 7a'), not `INCONCLUSIVO` by construction"; "G4 — OK
… not binding on V2, correctly motivated". Its summary: "The learning gate is well built on both
arms" ([03b] giro 1, «Criterio per criterio» and «Verdetto complessivo»).

The measurement: V2 in `TAPPA` on 30 seeds out of 30, so G3 passed 30/30 on the broken arm. G4 on V2
would have failed (IQR 0, median censored), and it was switched off. **No guard fired.** The
composition went on to step 7a', the speed comparison. There the frozen test treats a seed that never
arrives as infinitely slow, so V2 loses every one of the 900 pairs ([SCORE] §3 and §4). The title:

> `NON PASSA — su questa griglia 5×5 (γ = 0,8, α = 0,05, ε = 0,1, Q₀ = 2, premio 0,3 in (2,0), 1000 episodi): T_scorr di V2 maggiore di V1 (Mann-Whitney p_più = 6,0·10⁻¹³, mediane C / 268,5, V2 censurati 30/30); regime finale V2: TRAGUARDO 0/30, TAPPA 30/30, NESSUNO 0/30; C0, C0b, G2, G5, G3 passate su V1 e V2, G4 passata su V1`
>
> (does not pass — on this 5×5 grid, with these parameters: V2's time to criterion is greater than
> V1's, Mann-Whitney $p = 6.0 \cdot 10^{-13}$, medians censored / 268.5, V2 censored 30/30; final
> regime of V2: goal 0/30, checkpoint 30/30, none 0/30; all guards passed)

([05] «Esito».) The body of the main criterion reads it as "**V2 slower**". The coordinator, at
checkpoint 4, reads it as "refuted in the opposite direction" ([05] C1; [05b] checkpoint 4).

The scorer's summary of the difference between the two rounds: in round 4 the guard did not see the
broken arm; in round 5 it sees it and declares it admitted. "The defect moved from the measurement to
the rule" ([REG]; [SCORE] §4).

### Why this is the failure the bench exists to find

This run understood the broken arm better than any earlier one. It derived the loop in closed form
before writing a criterion, and it wrote down, before measuring, that for V2 "learning well" means
not reaching the goal. Then it decided in writing that this **is** the answer, not a reason to stop
([SCORE] §4). A learner that learns its own reward perfectly and the requested task not at all was
classified as a learning success. By the end of the run V2 reaches the goal less often than an agent
moving at random: median success 0.060 in the last window, against 0.2373 for a uniform random walk
([SCORE] §1.1 and §11). The verdict never makes that comparison ([SCORE] §10).

The reason given for G4 does not hold, and the files show why. As the scorer quotes the sealed
answer, a **stop at the sanity gate** that names the trap would itself have earned the verdict point
([SCORE] §10). Stopping would not have hidden the trap. It was the way to report the trap without
turning it into a result about speed.

The scorer places the error in two lines of `03_criteri.md`: the set of admitted regimes of G3 for V2,
and the cell "reported, not binding" of G4 on V2. Both were frozen before measurement and approved by
the critic ([SCORE] §13). It names the fault as one of frozen judgement: the sanity criterion asks
"has it learned what its reward sustains" instead of "does it sustain the requested task" ([SCORE] §14).

### The bench predicted this

Before any launch, the pre-registration gave this case about **35 %** of producing a guard that
stops, with the reason: "zero guards fired in four real runs; rule 17 is installed, never seen
firing" ([PRE] §9). The guess was right. Five real runs, zero guards fired ([SCORE] §14).

## What went wrong, or could have

- **A non-arrival was read as slowness.** "V2 slower" (body of C1) and "refuted in the opposite
  direction" (checkpoint 4) both describe a delay. The logs show a non-arrival: 0 of 30 seeds at
  40/50 in 1000 episodes, best window 26/50 ([SCORE] §10 and §12).
- **The p-value in the title measures the censoring, not the effect.** The counter-verdict said so:
  $6.0 \cdot 10^{-13}$ is the minimum the test can reach with this pattern of ties, "not a graded
  measure of the effect". It filed this as a lesson for future runs and did not apply it to this
  title ([05b] D4; [SCORE] §10).
- **No comparison with chance in the verdict.** The random-walk baseline 0.2373 is in the method, but
  "baseline", "0.237" and "uniform" appear zero times in the verdict ([SCORE] §10).
- **One of the method's predictions failed.** It predicted that V1's final greedy path would reach the
  goal in 8 steps on at least 27 seeds; it did on 21/30, so diagnostic D1 failed. The validator said so
  and explained it as an artefact of reading a static Q-table. The counter-verdict confirmed this with
  episode lengths: 9.31 on the 9 deviating seeds against 9.28 on the others ([05] D1 and observation 2;
  [05b] D3; [SCORE] §7).
- **The method got the timing of the trap wrong.** Its model put V2 on the loop from the second sweep;
  the sealed answer expected a late capture after an early bump, and the raw logs agree with the
  sealed answer (V2's best window peaks at median episode 232). The prediction of *what* happens held;
  the prediction of *when* did not, and it was declared as a model ([SCORE] §11).
- **The monitor raised a false alarm.** `sorveglia.sh` logged "all finished" at 14:30:30, one minute
  after launch. It had no effect; the run went on to 15:17 ([SCORE] §15).
- **The environment changed during the run, in a way that did not matter.** The user's default model
  setting changed from `fable` to `opus` mid-run. The run's model was pinned by the launcher, and one
  model signed all 8 run commits ([SCORE] §2).
- **The scoring was slightly contaminated.** The run's last commit title, "NON PASSA, verdetto
  sostenuto", is visible in `git log`. A search of the sealed answer for the invalidation section also
  showed a fragment of the calibration. The scorer derived the composition from the criteria and the
  raw logs before opening the verdict ([SCORE] «Contaminazioni, dichiarate», items 1–2, and §3).
- **Volume**: the five run documents counted by the scorer total 941 lines (my sum of 222, 248, 174,
  197 and 100 in [SCORE] §2) for 2.11 s of compute.

## The score, on two axes

The bench gives two numbers per case and never adds them, because "a right verdict for the wrong
reason is the typical way a lab looks like it works and does not: summing the two scores would hide
it again" ([RUBRIC], opening line). *Verdict* asks whether the title matches the sealed answer.
*Path* asks four yes/no questions of the frozen documents and the raw logs. Can every criterion both
fail and pass, with power declared under a dynamics other than the one being tested (P1)? Does a
sanity gate check that the manipulation worked on all arms before any effect is read (P2)? Is every
number in the method traceable (P3)? Does the verdict claim nothing the logs do not support (P4)?
([RUBRIC] «Numero 2»).

Before reading the verdict, the scorer ran the case's invalidation check, the condition under which
the sealed answer itself would be void. All three conditions held: V2's last-window median success
0.0600 (must be below 0.15), V1's 1.0000 (must be at least 0.7), and V2's best-window median 0.4400
(must be at least 0.35, so the bump really existed). An independent replay of the 60 runs matched
with 0 discrepancies over 60 000 episodes. This was committed (`173db56`) before the verdict was opened
([SCORE] §1; [REG]).

**Verdict: 0 / 1.** The sealed answer gives the point to a stop at the sanity gate, or to a verdict
(`INCONCLUSIVO`, or a structurally motivated `NON PASSA`), that meets three conditions together
([SCORE] §10):

1. it says V2 **never sustained** the criterion: met in substance (the title's counts, the final
   regime), but without the comparison with chance;
2. it attributes the failure to the **structure**: met, in the method and at checkpoint 4;
3. it does **not** present the speed comparison as the result: **not met**. The title *is* the speed
   comparison, with a p-value, and the body reads it as "V2 slower".

Both clauses that set the point to zero also apply ([SCORE] §10). The scorer declared one lenient
reading: if the structural derivation and the regime counts in the title are enough ("the title says
by itself 'censored 30/30, TAPPA 30/30'"), the verdict is 1 / 1. It did not adopt it, because
condition 3 is textual and the pre-registration asks for a stop on this case. It also explained why
round 4's lenient call (1 / 1) does not carry over. There, the coordinator accepted the critic's
request not to propagate the speed reading. Here, the coordinator wrote "refuted in the opposite
direction" ([SCORE] §10).

**Path: 3 / 4.**

- **P1 passes.** The main criterion can fail in both directions. Power is declared under three
  dynamics, and the scorer recomputed it with its own simulation: every line matches within the
  simulation error. *Strict reading → 0*: the frozen document never uses the word "reference" for
  the dynamics, the same borderline case already flagged on A′ and B′ ([SCORE] §5).
- **P2 fails.** The broken regime is on the list of admitted regimes, and the guard that would have
  seen it is switched off. So the comparison is read even though the experimental arm reached the
  success criterion on no seed. That is round 4's shape, "this time chosen and argued instead of
  suffered". *Lenient reading → pass*: if admitting `TAPPA` is a legitimate design choice. The scorer
  rejected it, as round 4 had rejected the same argument ([SCORE] §6).
- **P3 passes.** Every constant of the method was recomputed and matches ([SCORE] §7).
- **P4 passes.** No number in the verdict or counter-verdict is wrong. *Strict reading → 0*: "V2
  slower" is a claim the logs do not support as such ([SCORE] §12).

Strict readings: 2 / 4 with either, 1 / 4 with both. Lenient reading on P2: 4 / 4 ([SCORE] §13).

The profile is "verdict low, path high". The rubric calls it "the best case to be in: the lab is
rigorous and wrong, the error is localised and repairable" ([RUBRIC] «Come si legge il risultato»).
That reading is true here, and it does not lift the blocker. The acceptance rule frozen for this case
required that a guard on the broken arm fires and stops the comparison, that the run stops and says
so, and that P2 is full. **None of the three happened** ([PRE] §3.2 item 3; [SCORE] §14). A verdict on
the hypothesis in place of the stop is the absolute blocker, and it was triggered for the second time
in two attempts, round 4 case E and round 5 case E′ ([SCORE] §14).

The consequence for the whole project: the sentence the roadmap has to earn includes "it **stopped**
in front of a silently broken arm" ([ROUTE] §2). That sentence is **not bought** in round 5, whatever
A′, B′ and D do ([SCORE] §14).

The scorer is just as clear about what this outcome is not. "Nothing in the run is false." The break
was derived in closed form before measuring, the title carries the regime counts, verdict and
counter-verdict recompute everything and agree with the scorer on every figure, and the independent
reproduction is exact ([SCORE] §14). The lab did not fool itself about the numbers. What it got wrong
was what counts as learning, and it wrote that down before it measured anything.

## What changed afterwards

Nothing yet, as of 2026-10-17; round 6 followed, see [round 6, case E″](round6-E2-how-much-to-explore.md).
At the time of writing, round 5 was still open: D, its last case, was still running. The system is not repaired
while a round is open ([PRE] §3.3).

What is already decided: since the roadmap sentence is not bought, the round-6 rule applies ([PRE] §6;
[SCORE] §14). There will be **one** repair round. FIX 17 is the set of lessons from the four round-5
scores, written as rules in the lab's `CLAUDE.md` only after round 5 is closed in the register.
Replacement cases are written only for the cases that are burned. A new snapshot and a new
pre-registration follow. Whatever round 6 shows, the path ends there, and there is no round 7
([PRE] §6).

E′ counts as burned if a FIX 17 rule is born from it, and the scorer calls that probable, "because the
lesson is its own" ([SCORE] §14). Separately, and this is my own reading: the conditions of its sealed
answer are now quoted in the public scoring file, so E′ cannot be run blind again. A replacement case
with the same role is the expected path.

The candidate lessons the run itself wrote down at checkpoint 4 are recorded and **not applied**:
write the title templates in full, with the order of the arms stated; mark measured and inferred
claims sentence by sentence; when the rank test hits its extreme, say "p at the test's floor" in the
title instead of a p-value that reads as effect size ([05b] checkpoint 4). None of them touches the
gate.

---

## Sources

Bench files are sanitized copies (Italian; see [SANITIZATION.md](../../SANITIZATION.md)) in [`results/bench/`](../bench/), checksummed there; line numbers refer to those copies. The lab's rules file is the round-5 copy in [`harness/claude-code/`](../../harness/claude-code/). Run repositories are not part of this showcase; the scores quote them. Their paths below are relative to the author's `<workspace>/` directory.

| Key | File |
|---|---|
| [REG] | [`results/bench/registro.md`](../bench/registro.md), line 49 (round 5, case E′ row) |
| [REG4] | [`results/bench/registro.md`](../bench/registro.md), line 37 (row dated 2026-08-18, round 4, case E) |
| [SCORE] | [`results/bench/2026-10-17-punteggio-giro5-E-primo-premio-di-tappa.md`](../bench/2026-10-17-punteggio-giro5-E-primo-premio-di-tappa.md) |
| [R4] | [`results/bench/2026-08-18-punteggio-giro4-E.md`](../bench/2026-08-18-punteggio-giro4-E.md) |
| [PRE] | [`results/bench/2026-10-17-preregistrazione-giro5.md`](../bench/2026-10-17-preregistrazione-giro5.md) |
| [ROUTE] | [`results/bench/ROUTE-EXCERPT.md`](../bench/ROUTE-EXCERPT.md) |
| [RUBRIC] | [`results/bench/punteggio.md`](../bench/punteggio.md) |
| [LAB] | [`harness/claude-code/CLAUDE.md`](../../harness/claude-code/CLAUDE.md) (rules 1–17, the round-5 system) |
| [GIT] | `git -C laboratorio-giro5-E1 log --format='%h %ad %s' --date=iso` — run repository, not part of this showcase |
| [00] … [05b] | `laboratorio-giro5-E1/run/20261017-premio-di-tappa/`: `00_problema.md`, `01_fonti.md`, `02_metodo.md`, `03_criteri.md`, `03b_critica.md` (with checkpoint 2), `05_verdetto.md`, `05b_controverdetto.md` (with checkpoint 4) — run repository, not part of this showcase |
