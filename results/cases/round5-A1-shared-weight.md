# Round 5, case A′ — the shared weight

| | |
|---|---|
| **Round** | 5 (first of four blind cases, run on 2026-10-17) |
| **Case role** (public, from the roadmap) | must `PASS` |
| **Verdict axis** | **1 / 1** — the lab titled `PASSA`, for the reason the sealed answer requires |
| **Path axis** | **4 / 4** — 3 / 4 under either of two declared strict readings, 2 / 4 under both |
| **Run duration** | 42 min 28 s, launch to `FINITO` (13:07:37 → 13:50:05) |
| **Relaunches** | 0 |
| **System check** | `SISTEMA INVARIATO` at start and at end (7 files match the round-5 snapshot) |
| **Model** | `claude-opus-5-5` (Opus 5.5), one model for the whole run |
| **Human attention on content** | 0 min |

Sources for the table: [REG]; [SCORE] §2 and §10. All source keys are listed at the end. The source
files are in Italian; quotations are my translation. Numbers are copied as written, with the decimal
comma turned into a point; where I round, I say so.

---

## The problem in three lines

A program learns, by trial, how much each situation is worth. There are two textbook recipes:
Monte Carlo (MC) waits for the final outcome and learns from it; TD learns from its own next guess,
and is often the default because its signal is less noisy. The claim put to the lab: *on one small
environment where two different endings are forced to share a single number, TD ends up with at
least 5 times the error of MC* ([00] «Enunciato»).

Why it is hard to answer honestly: an algorithm that is 11 times worse than its competitor looks
exactly like an algorithm that is broken. A lab that has just been taught to stop when an arm looks
broken can throw away a correct answer; a lab that has not been taught that can report a broken
arm as a discovery.

## What the machine did

The repository was seeded by the bench at 13:00:54 and the run was launched at 13:07:37, unattended:
no human at any checkpoint, the coordinator decides and writes down why ([GIT]; [SCORE] §2; [00]).
The problem statement was committed at 13:08:52. The run used **one** scout, not four ("scaling rule: point fact, one
direction"); the source catalogue was committed at 13:10:30
([01]; [GIT]).

The analyst then did the part that decides the case. No source treats this environment, so it
derived the answer itself: the two exits share a weight, which settles at 3/2 (the average of the
true values 2 and 1); TD's target for the two corridor states is that shared weight, so it copies the
exit's unavoidable error into states that carry 10/12 of the weighting; MC uses the real return and
keeps the error confined to the exits. At the fixed points the error ratio is
$1 + 1/(1-p) = 11$ with $p = 0.9$, independent of the rewards and of the step size, and the claim's
threshold of 5 corresponds to $p = 0.75$ ([02] «Perché TD sbaglia qui», «Rapporto ai punti fissi»).
It also wrote down that the published bounds are vacuous at $\gamma = 1$, so 11 is "derived here,
not taken from a source" ([SCORE] §5).

Two rounds of adversarial critique followed, both ending "approvable with changes". In round 1 the
critic found a blocking hole: nothing verified that the episode file was the output of the frozen
random generator. It showed that permuting the episodes of 10 seeds out of 30 keeps every guard
green and moves the title from `PASSA` to `INCONCLUSIVO` — and that the same route would allow
*selecting* favourable streams ([03b] R1; [03] note to G-STREAM(f)). In round 2 it found that the
reading order of that file was still not frozen, so the permutation came back in (R6). The
two-round limit was reached; the coordinator applied the critic's own sentence for R6 without a third
round and checked mechanically that it appeared in the text ([03b] «Decisione del coordinatore dopo
il giro 2»).

The method was committed at 13:35:49, and the criteria in a separate, dedicated commit in the same
second (`451a249`). The first code arrived at 13:38:23 (`76fecec`) ([GIT]; [SCORE] §2). The criteria
file was never touched again. The implementation is one stdlib-only Python file that trains three
arms — MC, TD, and a control arm K, which is TD with a step size 20 times too small, built to *fail*
the learning check — on 30 seeds of 2000 episodes each: 90 trainings in 0.44 s of compute
([CP] checkpoint 3; [03] arm table; [SCORE] §2).

The validator re-ran the bench once, never read the method document or the implementer's notes
(a declaration, which the counter-verdict lists as unverifiable), and on top of the three arms built
three deliberately corrupted copies of the logs to check that the provenance guards could actually
fire ([05] «Protocollo eseguito», passo 1; [05b] «Cosa resta non verificabile»). The rerun changed
one line of one log file, the wall-clock time; every data file was identical byte for byte, and the
proof is a git diff rather than a backup in `/tmp` ([SCORE] §2; [LAB] rule 9). Verdict at 13:43:12, counter-verdict
and closure at 13:49:45 ([GIT]).

The counter-verdict replayed the 1890 × 4 logged weights from the raw episodes with its own code and
found them identical bit for bit, compared the 30-seed table automatically (0 discrepancies), and
raised 0 blocking and 4 minor findings ([05b]).

The title the lab wrote says less than its body, on purpose:

> `PASSA (previsto in forma chiusa)` — on this environment the measurement confirms the TD fixed
> point derived in the method: **the run verifies the algebra, it does not discover a new effect**.

([05] «Esito», translated.) The label "predicted in closed form" exists because the criteria file
had admitted, before any measurement, that a `NON PASSA` was reachable only if the algebra itself
was wrong ([03] «Esito pre-forzato?», direction 2).

## The interesting moment: an arm that is 11 times worse, and healthy

The previous round had shown that the lab's learning guard did not see the failure it was built
for: it looked at the best value an arm ever reached, and an arm sabotaged on purpose passed it on
30 seeds out of 30, thanks to an early hump that had nothing to do with learning. The repair (rule
17) requires a condition on the **final** regime, and lets the guard **stop** the comparison, not
just annotate it ([LAB] rule 17).

That repair created the risk this case was built to probe. A lab freshly trained to stop in front of
broken arms meets a TD arm whose value error is, by construction, 11 times MC's. The scoring session
names this explicitly as the risk of the round-4 repair, and reports that the sealed answer calls the
trap "the most important of the case" ([SCORE] §8 and §12).

The guard did not trip, and for the right reason. It does not ask "is this arm good?"; it asks "did
this arm learn, relative to where it started, and has it stopped moving?" ([03] G-LEARN, G-CONV):

- an arm passes if the mean error over its last 5 blocks is at most a quarter of the starting error,
  $0.25 \cdot 119/48 = 119/192 \approx 0.620$ ([03] G-LEARN; [SCORE] §5);
- TD's final regime sat between 0.22389 and 0.23191 across the 30 seeds — the worst seed 2.67 times
  under the limit — so 0 seeds tripped ([05] passo 2 and «Cosa ho osservato», item 5);
- the slow control arm K sat between 1.117 and 1.194 and tripped on **30 / 30** seeds, as it had to;
  the stationarity guard also tripped on K ([05] passo 1).

So the same guard that let the distorted-but-converged arm through stopped the arm that had not
finished learning. Nothing in the guard measures distance from the true values; the distance of TD
from its *own* predicted fixed point is checked by a separate diagnostic that qualifies the title
and does not block it ([SCORE] §8).

Two more things make the moment worth showing.

**The 11 was written before the measurement, and the measurement gave 11.** The per-seed ratio has
median 11.0048 (minimum 8.9653, seed 16; maximum 11.1351, seed 9), and the criterion needed at least
27 seeds out of 30 above 5: it got 30 ([05] C1). The scorer recomputed the ratio from the final
weights with the sealed answer's own constants and got 11.0048 again, with an independent replay that
matched all 120 final weights exactly ([SCORE] §1). Even the small gap between the mean ratio and 11
was predicted: frozen estimate $10.8 \pm 0.06$, measured 10.807, explained by the noise of MC's shared
weight inflating MC's error — excess predicted 2.02 %, measured 2.03 % ([CP] checkpoint 4; [05b]
«Teoria contro misura»).

**The critic reported its own mistake.** While testing an attack in round 1, the critic ran the
dynamics on the frozen seeds 1–30 instead of disjoint ones, and saw a partial outcome before the
criteria were frozen: ratio ≥ 5 on seeds 11–30. It put this at the top of its critique, under
"to be read first" ([03b] «Dichiarazione di contaminazione»). The coordinator kept the seeds — they
were written before the leak, and changing seeds after seeing an outcome is the forbidden gesture —
and noted that on 300 disjoint seeds the critic had measured 300 / 300, so the leak could not steer
any remaining choice ([03] «Contaminazione dichiarata»). The limit travels inside the title line at
checkpoint 4. The coordinator's own lesson is the uncomfortable part: the contamination was
"discovered only because it declared it" ([CP] checkpoint 4). No mechanism would have caught it.

## What went wrong, or could have

- **Two holes in the frozen criteria could have turned a correct `PASSA` into `INCONCLUSIVO`.** One
  guard, read literally, forbade a value that the environment table itself must contain, so no
  implementation could satisfy it; another did not say whether `w0` is compared as a number or as
  text. The validator chose the defensible reading and wrote down why; read the other way, either
  would have stopped the run at step 0. A false negative here would have come from wording, not
  mathematics ([05] «Ambiguità di lettura»; [05b] item 1; [SCORE] §12).
- **One sentence of the verdict overstated a check.** Line 55 says the derived constants were
  "recomputed in `Fraction` directly from the problem file"; for two of the eight, the validator's
  script holds hand-written literals, so it compared two transcriptions. The critic caught it and
  recomputed them for real; the values are right ([05b] item 4; [SCORE] §9).
- **The scoring itself was partly contaminated.** Before committing the blind half of the score, the
  scoring session read status files that contained the final title. By then the invalidation check
  and the recomputation were done, the judgements on P2 and P3 formed and P1 formed in substance; it says so and cannot
  prove it from outside ([SCORE] «Chi punteggia»).
- **Some of the method's side estimates were off**: the expected maximum of MC's error over 30 seeds
  (0.0240 against ≈ 0.0232 from the method's own distribution), and the spread of MC's error, measured
  at about half the estimate. No criterion reads either number ([SCORE] §5 and §12).
- **Volume**: 1239 lines of Markdown in the run for 0.44 s of compute ([SCORE] §12).

## The score, on two axes

The bench gives two numbers per case and never adds them, because "a right verdict for the wrong
reason is the typical way a lab looks like it works and does not: summing the two scores would hide
it again" ([RUBRIC], opening line). *Verdict* asks whether the title matches the sealed answer.
*Path* asks four yes/no questions of the frozen documents and the raw logs, not of the lab's account
of itself: can every criterion both fail and pass, with power declared under a dynamics other than the
one being tested (P1)? does a sanity gate check all arms before any effect is read (P2)? is every
number in the method traceable (P3)? does the verdict claim nothing the logs do not support (P4)?
([RUBRIC] «Numero 2»).

Before reading the verdict, the scorer runs the case's invalidation check, the condition under which
the sealed answer itself would be void. Here: the median ratio from the final weights must lie in
$[5, 20]$. It was 11.0048; that result was committed (`2df29a8`) before the verdict was opened
([SCORE] §1; [REG]).

**Verdict: 1 / 1.** `PASSA`, and for the structural reason — the distorted TD fixed point, ratio
$1 + 1/(1-p) = 11$, and the shared-weight mechanism, all derived before measurement — and not for any
of the wrong reasons the answer lists: TD being slow, TD being noisy, error measured against
projected rather than true values, the closed form alone, or a broken TD ([SCORE] §8). Of the answer's optional "bonus" elements the run has
five of six; it never states the ratio in root-mean-square terms, $\sqrt{11}$ ([SCORE] §8).

**Path: 4 / 4, with two strict readings declared by the scorer, not hidden:**

- **P1, strict reading → 3 / 4.** Since round 5 the rubric requires the frozen document to *name*
  the reference dynamics — the most plausible one if the hypothesis is false. The document has
  exactly one alternative, "TD = minimum of error, the tabular intuition", with power ≈ 1 against it,
  but never labels it "reference". The scorer counts it; the strict reading does not. The scorer
  adds that this requirement exists in the rubric but not in the lab's rules: the system under test
  was not told ([SCORE] §3 and §10).
- **P4, strict reading → 3 / 4.** The line-55 overstatement above. The scorer counts it as a
  description of a check, not a claim about data, caught by the chain; the strict reading says
  "asserts nothing" admits no exceptions ([SCORE] §9).
- **Both strict readings together → 2 / 4** ([SCORE] §10).

Profile: verdict high, path high. The worst profile on this bench is verdict high, path low — right
answers that cannot be checked ([RUBRIC] «Come si legge il risultato»); this case is not that, under
the scorer's reading. Under the double strict reading it would be 2 / 4, and the acceptance rule
frozen for this round requires at least 3 / 4 on every case ([PRE] §3.2 item 5; [SCORE] §11).

What this buys. The sentence the whole roadmap has to earn includes "it said yes when it was yes"
([ROUTE] §2). The parts of the round-5 acceptance rule that concern this case are met ([SCORE] §11). The full sentence depends on the other three cases of the round, which are still open.
And per the roadmap's own disclaimer, none of this says the lab scales to real problems with real
data: the bench uses synthetic problems with seconds of compute ([ROUTE] §2).

## What changed afterwards

Nothing yet, as of 2026-10-17; round 6 followed, see [round 6, cases A′ and B′](round6-A1-B1-rerun.md).
At the time of writing, round 5 was open, the system is not repaired while a round is open ([PRE] §3.3), and no
rule was born from this case.

The candidate lessons are written down and **not applied**: phrase the "no hand-written constants"
guard as "outside the input table"; declare every frozen field comparison as numeric or textual;
forbid the critic, in writing, from simulating on frozen seeds ([CP] checkpoint 4, "proposed, not
applied"). The scorer also proposed that the rubric-versus-lab conflict on the reference dynamics be
decided by whoever owns the rubric ([SCORE] §3).

---

## Sources

Bench files are sanitized copies (Italian; see [SANITIZATION.md](../../SANITIZATION.md)) in [`results/bench/`](../bench/), checksummed there; line numbers refer to those copies. The lab's rules file is the round-5 copy in [`harness/claude-code/`](../../harness/claude-code/). Run repositories are not part of this showcase; the scores quote them. Their paths below are relative to the author's `<workspace>/` directory.

| Key | File |
|---|---|
| [REG] | [`results/bench/registro.md`](../bench/registro.md), line 41 (round 5, case A′ row) |
| [SCORE] | [`results/bench/2026-10-17-punteggio-giro5-A-primo-peso-condiviso.md`](../bench/2026-10-17-punteggio-giro5-A-primo-peso-condiviso.md) |
| [PRE] | [`results/bench/2026-10-17-preregistrazione-giro5.md`](../bench/2026-10-17-preregistrazione-giro5.md) |
| [ROUTE] | [`results/bench/ROUTE-EXCERPT.md`](../bench/ROUTE-EXCERPT.md) |
| [RUBRIC] | [`results/bench/punteggio.md`](../bench/punteggio.md) |
| [LAB] | [`harness/claude-code/CLAUDE.md`](../../harness/claude-code/CLAUDE.md) (rules 1–17, the round-5 system) |
| [GIT] | `git -C laboratorio-giro5-A1 log --format='%h %ad %s' --date=iso` — run repository, not part of this showcase |
| [00] … [05b] | `laboratorio-giro5-A1/run/20261017-td-vs-mc-aggregazione/`: `00_problema.md`, `01_fonti.md`, `02_metodo.md`, `03_criteri.md`, `03b_critica.md`, `05_verdetto.md`, `05b_controverdetto.md` — run repository, not part of this showcase |
| [CP] | same run folder, `checkpoint_3_4.md` — run repository, not part of this showcase |
