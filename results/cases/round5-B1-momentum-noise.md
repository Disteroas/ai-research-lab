# Round 5, case B′ — momentum and gradient noise

| | |
|---|---|
| **Round** | 5 (second of four blind cases, run on 2026-10-17) |
| **Case role** (public, from the pre-registration) | must give `NON PASSA` (does not pass) |
| **Verdict axis** | **1 / 1**: the lab titled `NON PASSA (pre-forzato …)` ("pre-forced"), for the reason the sealed answer requires |
| **Path axis** | **4 / 4**: 3 / 4 under either of two declared strict readings, 2 / 4 under both |
| **Run duration** | 36 min 26 s, launch to `FINITO` (13:52:20 → 14:28:46) |
| **Relaunches** | 0 |
| **System check** | `SISTEMA INVARIATO` at start and at end (7 files match the round-5 snapshot) |
| **Model** | `claude-opus-5-5` (Opus 5.5), one model for the whole run |
| **Human attention on content** | 0 min |

Sources for the table: [REG]; [SCORE] §2 and §12; [PRE] §2. All source keys are listed at the end.
The source files are in Italian; quotations are my translation. Numbers are copied as written, with
the decimal comma turned into a point; where I round or sum, I say so.

---

## The problem in three lines

A program looks for the lowest point of a function, but every step uses a noisy estimate of the
slope, so it never settles: it keeps jittering around the minimum. A widespread idea is that
*momentum* (carrying over part of the previous steps) averages the noise out. The claim put to the
lab: *at the same step size $\alpha$, adding momentum with $\beta = 0.9$ reduces the steady-state
squared error of stochastic gradient descent* on one fully specified one-dimensional problem, 30
seeds, 20 000 steps per run ([00] «Enunciato»).

Why it is hard to answer honestly: on this problem the answer follows from algebra before any code
runs. A lab can confirm the folklore with its own numbers, or it can run a measurement whose outcome
was decided in advance and present it as a discovery. The honest answer is a `NON PASSA` that also
says, in the title, how little the measurement adds.

## What the machine did

The repository was seeded by the bench at 13:00:55 and the run was launched at 13:52:20, unattended:
no human at any checkpoint, the coordinator decides and writes down why ([GIT]; [SCORE] §12; [00]).
The problem statement was committed at 13:52:58. The run used **one** scout, by the scaling rule
("point fact, one direction"); sources were committed at 13:54:38 ([CP] checkpoint 1; [GIT]).

The analyst derived the answer itself; the sources are declared not read in full, and "no number is
taken from the sources" ([02] «Confronto con le fonti scelte»). The stationary variance of the iterate
has a closed form, and its ratio between the two variants is $3781/379 = 9.976$. The reading the
analyst wrote down: for small steps momentum behaves like plain stochastic gradient descent with an
*effective* step $\alpha/(1-\beta)$, so at fixed $\alpha$ it multiplies the steady-state error by about
$1/(1-\beta) = 10$; "the noise enters $x$ amplified, not attenuated". The prediction was written
before any simulation: the claim is false on this environment ([02] «Lettura»). The analyst also
noted, and placed outside the claim, the one thing momentum does better here: it forgets the
starting point about 5 times faster ([02], note on the transient; [03] «Cosa NON viene misurato»).

Two rounds of adversarial critique followed. Round 1 ended `DA RISCRIVERE` (to be rewritten), on one
blocking finding that is the subject of the next section. Round 2 ended "approved with minor
findings"; the last two fixes were applied before freezing without a third round, and the
coordinator checked with a `diff` that they touched no threshold, zone or composition step ([03b];
[CP] checkpoint 2). The critic also corrected a physical claim in the method's motivation: even the
"normalised" form of momentum, which the problem excludes, would reduce the error by only 0.5 %
($R \approx 0.995$), not by the large factor the motivation suggested ([03b] R2).

The method and the critique were committed at 14:18:16, and the criteria in a separate, dedicated
commit in the same second (`369e334`). The first code arrived at 14:20:29 (`c3d96e3`) ([GIT]; [SCORE]
§2). The implementation is one stdlib-only Python file of 174 lines that runs both variants on the
same noise for each seed: 60 runs in 1.40 s of compute ([CP] checkpoint 3; [SCORE] §12).

The validator re-ran the bench once and re-simulated all 60 runs with its own code. The verdict was
committed at 14:24:18 and the counter-verdict at 14:28:31 ([GIT]). On every seed, momentum made the
error **larger**: the per-seed ratio $R_s$ ran from 8.3399 (seed 21) to 12.6306 (seed 24), median
10.1998, 30 seeds out of 30 above 1 ([05] C1). Simulation and theory agreed within the frozen
tolerance on both arms, at −1.46 and −0.77 standard deviations ([05] C2). The rerun changed one line
of one log file, the wall-clock time, and the proof is a git diff ([05b] «Integrità dei log»; [LAB]
rule 9).

The counter-verdict found the verdict supported, with 0 blocking and 3 minor findings ([05b]).

## The interesting moment: a defence that holds one level up

### The guard that could have failed an honest bench

The frozen criteria include a guard, G4f, that recomputes every summary statistic from the raw CSV
files and requires it to match the logged value **bit for bit** ([03] G4f). In round 1 the critic
showed why that is dangerous as written. The protocol fixed the function for the standard deviation
but not for the mean, so the implementer could write `math.fsum(xs)/30` and the validator
`statistics.mean(xs)`. On 20 000 synthetic vectors, with a seed outside the frozen ones and without
the bench, the two disagree in the last bit in 26.9 % of cases; with two means in the summary, the
chance of a false failure is about $1 - 0.731^2 \approx 0.47$. A false failure of G4f maps, by the
frozen composition, to `INCONCLUSIVO — simulazione non verificata`: a false statement about an
honest bench ([03b] R1; [03] step P2).

The fix was one line: name the function for every statistic, the same for bench and validator
(`statistics.mean`, `median`, `stdev`, fixed quartile method) ([03] «Funzioni fissate»). In round 2
the critic checked it and found the same failure class elsewhere: a hash of re-simulated values
differs between two legitimate ways of writing the same process in 80 cases out of 80, so it
accepted keeping that hash only where it is computed from logged values, and leaving the
re-simulation to numeric tolerances ([03b] giro 2, R6). Its argument for why the fix works: those functions round once on an exact
result, so "if bench and validator use the same functions, the bit-for-bit recomputation is
deterministic" ([03b] giro 2, R1).

### The scorer's replay

The scorer replayed the run on Python 3.10; the run had used Python 3.14.6 ([SCORE] §1.2; [05]
«Protocollo eseguito»). The 60 values of the error metric came out bit-identical, and so did the
noise hashes ([SCORE] §1.2). Then it rechecked the counter-verdict's claim that the per-arm
statistics are "identical to 17 digits":

- on Python 3.14.6, 14 statistics out of 14 match bit for bit;
- on Python 3.10, **one** differs by 1 ulp (one unit in the last place): the standard deviation of
  the momentum arm. The logged value is the correctly rounded one, checked with exact arithmetic
  ([SCORE] §9 and §12).

So the failure the critic predicted does exist, one level below where it was closed: the function
was fixed, the interpreter version was not ([SCORE] §12). It had no effect on this run, because
bench and validator ran on the same machine with the same interpreter ([SCORE] §12). My own reading
of the frozen text, not stated in the files: anyone applying G4f literally to the committed logs from
Python 3.10 would see that one number fail, and step P2 turns any G4f failure into `INCONCLUSIVO`
([03] G4f and step P2). The files record the 1-ulp difference; they do not say what in the
interpreter causes it, and I do not either.

What makes this worth showing is not the bit. The critic reasoned correctly that a bit-for-bit check
depends on how the code is written, and repaired it at the level it could see. The scorer, by
changing one thing the run did not control, found the next level down. Neither the run's lessons nor
the score turn it into a proposed rule yet ([CP] checkpoint 4; [SCORE] §12).

### A `NON PASSA` declared before the measurement

The second thread is the title. The criteria file asked, before any measurement, whether the
outcome was forced, in both directions ([03] «Esito pre-forzato»; [LAB] rule 13). Its answer: if the
theory–simulation check C2 passes on both arms, the main criterion C1 must land in the zone
"momentum increases the error by at least 10 %", so the outcome is decided by the algebra. `PASSA`
stays reachable, but only along the path in which the simulation contradicts the theory. In the
forced case the title must carry its own label, and the file says what the run then establishes: that
the bench realises the environment and agrees with the algebra, "not evidence on the claim beyond
the algebra itself" ([03] «Conseguenza per il titolo»).

That is exactly the title the lab produced:

> `NON PASSA (pre-forzato: con C2 passato su b0 e b09 l'esito è determinato dall'algebra di 02_metodo; la misura verifica l'algebra) — su questo ambiente, α = 0,01`
>
> (does not pass, pre-forced: with C2 passed on both arms the outcome is determined by the algebra
> of the method; the measurement verifies the algebra; on this environment, $\alpha = 0.01$)

([05] «Esito».) The counter-verdict checked that it is the frozen line character for character
([05b] «Esito»). The label exists because of rule 7, born in round 2 of the bench from the earlier
case B, which had qualified its forced result correctly in the body and badly in the title; the
qualification left to the body "survives until the first summary and no further" ([LAB] rule 7).
Here it sits in the one line that travels.

At measurement time the validator repeated the reachability check on the data, as rule 13 requires:
21 seeds would have to flip sign to reach the zones where momentum reduces the error, `PASSA`
among them, and 10 to reach "sign not resolved" ([05]
«Regola 13 alla misura»). One count was off, as the next section says.

## What went wrong, or could have

- **A count in the verdict is not the minimum.** For the "no reduction" zone the verdict says "at
  least 15 (16 suffice)" values below 1.10. The counter-verdict and the scorer both find that 16 is
  the exact minimum and 15 is never enough. The statement is true as a condition on values, not the
  minimum number of seeds that rule 13 asks for ([05] «Regola 13 alla misura»; [05b] R1; [SCORE] §9).
- **Two numbers marked "measured" had no line in any log.** A standard deviation and a correlation in
  the verdict's observations are correct (the critic and the scorer recomputed them) but no file of
  the validator contains them. The counter-verdict calls it "exactly the signature the counter-verdict
  must look for" ([05b] R2; [SCORE] §9).
- **The validator's independent re-simulation was not very independent.** It ran the same operations
  in the same order as the bench, so it matched with error exactly 0 and its tolerances were never
  tested by any rounding difference. The validator wrote this itself; the counter-verdict closed the
  gap by re-simulating in a different algebraic form, with deviations of $1.3 \cdot 10^{-15}$ and
  $1.4 \cdot 10^{-14}$ ([05] «Cosa ho osservato», item 3; [05b] «Indipendenza del canale»).
- **The closing of the `PASSA` path was argued incompletely.** The verdict closed it from C2 passing;
  it should also have used C1's own data, where 0 seeds out of 30 point the other way ([05b] R3).
- **The shared reading of the problem is not checked by anything.** Bench, validator and critic read
  the problem text the same way (window indexing, noise timing, update order). The arithmetic is
  verified three ways, the interpretation is not. The checkpoint adds that the factor of about 10
  would not change with a one-step shift of the window ([03] «Cosa NON viene misurato»; [CP]
  checkpoint 4).
- **The scoring was slightly contaminated.** To find the invalidation section, the scorer ran a grep
  of the sealed answer's headings and saw the expected title and the closed-form 9.976. Both were
  already public: the role in the pre-registration, the number derived by the run itself
  ([SCORE] «Contaminazioni dichiarate», item 1).
- **The sealed answer and the rubric disagree on one definition.** For the power requirement E-P1c,
  the sealed answer describes the reference dynamics as the one "if the hypothesis were **true**";
  the rubric defines it as the most plausible one "if the hypothesis is **false**". The scorer
  followed the rubric and flagged the sentence for alignment outside the round ([SCORE] §8; [REG]).
- **Volume**: the seven run documents counted by the scorer add up to 1480 lines (my sum of the
  counts in [SCORE] §12) for 1.40 s of compute.

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
the sealed answer itself would be void. Here: the ratio of the median errors with and without
momentum must be at least 5. It was $0.0493304121 / 0.0047853522 = 10.3086$, the implementation was
checked against the literal rule, and an independent replay of the 60 runs matched with 0
discrepancies; that result was committed (`e3f223d`) before the verdict was opened ([SCORE] §1;
[REG]).

**Verdict: 1 / 1.** `NON PASSA`, and for the direction the answer requires: momentum makes the error
*larger* by about an order of magnitude, not merely "not smaller" ([SCORE] §7). None of the wrong
reasons the answer lists applies: not absence of effect, not "momentum is slower" (the run says the
opposite and puts it outside the claim), not divergence, not literature alone. The normalised form of
momentum, a listed trap, was derived and declared out of domain before measurement. Of the answer's
optional "bonus" elements the run has three of four; it lacks a proof that the error grows for
**every** $\beta$, giving only the approximate reading "about $1/(1-\beta)$" ([SCORE] §7).

**Path: 4 / 4, with two strict readings declared by the scorer, not hidden:**

- **P1, strict reading → 3 / 4.** Since round 5 the rubric requires the frozen document to *identify*
  the reference dynamics. The document names the dynamics under which the claim is false as "the
  dynamics predicted by the method", and writes the falsity of the claim as a prediction, but never
  uses the word "reference". The scorer counts it, calling it "the strongest case possible without
  the word"; the strict reading does not. As on A′, the requirement is in the rubric and not in the
  lab's rules ([SCORE] §3).
- **P4, strict reading → 3 / 4.** The two "measured" numbers without a log line. The scorer counts them
  as a traceability defect, since the raw logs support them; the strict reading treats the label as
  a claim the logs do not show. The scorer calls this weaker than A′'s point, where a sentence was
  false about the code ([SCORE] §9).
- **Both strict readings together → 2 / 4** ([SCORE] §10).

P2 passes in full: every guard is checked on both arms and is blocking before the main criterion,
"including the experimental arm alone" ([SCORE] §4). P3 passes: the scorer recomputed every number in
the method and all match ([SCORE] §5).

Profile: verdict high, path high. The worst profile on this bench is verdict high, path low: right
answers that cannot be checked ([RUBRIC] «Come si legge il risultato»). Under the scorer's reading
this case is not that. Under the double strict reading it would be 2 / 4, and the acceptance rule
frozen for this round requires at least 3 / 4 on every case ([PRE] §3.2 item 5; [SCORE] §11).

What this buys. The sentence the whole roadmap has to earn includes "no when it was no" ([ROUTE]
§2). The parts of the round-5 acceptance rule that concern this case are met: items 2 and 5 ([SCORE]
§11). The full sentence depends on the rest of the round: A′ already scored, E′ and D still open.
And per the roadmap's own disclaimer, none of this says the lab scales to real problems with real
data: the bench uses synthetic problems with seconds of compute ([ROUTE] §2).

## What changed afterwards

Nothing yet, as of 2026-10-17; round 6 followed, see [round 6, cases A′ and B′](round6-A1-B1-rerun.md).
At the time of writing, round 5 was open, the system is not repaired while a round is open ([PRE] §3.3), and no
rule was born from this case.

The candidate lessons are written down and **not applied**: every value marked "measured" in a
verdict must have a line in one of the validator's log files; the frozen schema must cover every
file that a guard reads bit for bit, not only the CSVs ([CP] checkpoint 4, "not applied here"). The
scorer also flagged the sealed answer's sentence on the reference dynamics for whoever maintains
the sealed answers ([SCORE] §8). The interpreter-version gap behind the 1-ulp difference is recorded
as a finding, not yet as a proposal ([SCORE] §12).

---

## Sources

Bench files are sanitized copies (Italian; see [SANITIZATION.md](../../SANITIZATION.md)) in [`results/bench/`](../bench/), checksummed there; line numbers refer to those copies. The lab's rules file is the round-5 copy in [`harness/claude-code/`](../../harness/claude-code/). Run repositories are not part of this showcase; the scores quote them. Their paths below are relative to the author's `<workspace>/` directory.

| Key | File |
|---|---|
| [REG] | [`results/bench/registro.md`](../bench/registro.md), line 45 (round 5, case B′ row) |
| [SCORE] | [`results/bench/2026-10-17-punteggio-giro5-B-primo-momentum-e-rumore.md`](../bench/2026-10-17-punteggio-giro5-B-primo-momentum-e-rumore.md) |
| [PRE] | [`results/bench/2026-10-17-preregistrazione-giro5.md`](../bench/2026-10-17-preregistrazione-giro5.md) |
| [ROUTE] | [`results/bench/ROUTE-EXCERPT.md`](../bench/ROUTE-EXCERPT.md) |
| [RUBRIC] | [`results/bench/punteggio.md`](../bench/punteggio.md) |
| [LAB] | [`harness/claude-code/CLAUDE.md`](../../harness/claude-code/CLAUDE.md) (rules 1–17, the round-5 system) |
| [GIT] | `git -C laboratorio-giro5-B1 log --format='%h %ad %s' --date=iso` — run repository, not part of this showcase |
| [00] … [05b] | `laboratorio-giro5-B1/run/20261017-momentum-sgd-regime/`: `00_problema.md`, `02_metodo.md`, `03_criteri.md`, `03b_critica.md`, `05_verdetto.md`, `05b_controverdetto.md` — run repository, not part of this showcase |
| [CP] | same run folder, `checkpoint.md` — run repository, not part of this showcase |
