# Round 6, cases A′ and B′ — the same two questions, asked again

| Case | Round | System under test | Title label | Oracle check | Verdict | Path (substance · both strict readings) | Effective duration | Relaunches |
|---|---|---|---|---|---|---|---|---|
| A′ shared weight | 5 | FIX 1-16 | `PASSA (previsto in forma chiusa)` | $\tilde\rho$ = 11.0048 | 1 / 1 | 4 / 4 · 2 / 4 | 42 min 28 s | 0 |
| A′ shared weight | 6 | FIX 1-17 | `PASSA (previsto da 02_metodo §6-8 e confermato da C2, C3, C4, C6)` | $\tilde\rho$ = 11.0048 | 1 / 1 | 4 / 4 · 2 / 4 | 2 h 34 min 06 s, two runs | 4 automatic (failed) + 1 manual |
| B′ momentum | 5 | FIX 1-16 | `NON PASSA (pre-forzato …)` | $\hat R$ = 10.3086 | 1 / 1 | 4 / 4 · 2 / 4 | 36 min 26 s | 0 |
| B′ momentum | 6 | FIX 1-17 | `NON PASSA (forzato dall'algebra)` | $\hat R$ = 10.3086 | 1 / 1 | 4 / 4 · 3 / 4 | 44 min 20 s | 0 |

Sources for the table: [REG5] lines 41 and 45; [REG6] lines 89 and 93; [S5A] §1; [S6A] §1, §10, §12;
[S6B] §1, §11. All four runs: model `claude-opus-5-5`, `SISTEMA INVARIATO` at start and end, 0 min of
human attention on content ([REG5]; [REG6]). Source files are in Italian; quotations are my
translation, decimal commas turned into points.

---

## Why the same cases twice

Round 6 was the single repair round after round 5. Its system, FIX 1-17, adds rules 18 and 19 and
one line of the critic's checklist: 2 files out of 7 changed ([PRE6] §1). A′ and B′ were relaunched
"as they are", same text, same prompt checksum: no FIX 17 rule was born from them, so they were not
burned, and "a relaunch on a different system measures the system, not memory: the lab keeps nothing
between runs" ([PRE6] §2). Public roles: A′ must give `PASSA`, B′ must give `NON PASSA`.

The problems, told in full in [R5A] and [R5B]: **A′** asks whether TD's value error is at least 5
times Monte Carlo's where two exits share one weight (yes: 11, in closed form); **B′** asks whether
momentum $\beta = 0.9$ lowers the steady-state error of noisy gradient descent (no: about 10× higher).

## What did not change

**The label and the reason.** Both A′ runs titled `PASSA` for the reason the sealed answer requires:
TD's fixed point is distorted because the "stay" transition carries zero TD error and the only
informative one, the exit, bootstraps on the shared weight; ratio $1 + 1/(1-p) = 11$, derived before
any measurement ([REG5] line 41; [S6A] §8). Both B′ runs titled `NON PASSA` because the effect goes
the other way, momentum *worse*, 30 seeds out of 30, with the structural reason written in the method:
the filter has gain $1/(1-\beta) = 10$ and "accumulates, does not average" the noise ([REG5] line 45;
[S6B] §8). The scorer of round 6 found none of the sealed answers' "right verdict, wrong reason"
routes in either case ([S6A] §8; [S6B] §8).

**The oracle numbers, to the last printed digit.** For B′ this is by construction: the problem
statement fixes seeds 1–30 and `random.Random(s).gauss`, and both rounds report the same medians,
0.0047853522 and 0.0493304121, hence $\hat R$ = 10.3086 ([REG5] line 45; [S6B] §1, §8). For A′ it is
not: the statement leaves the episode-stream convention to the analyst (question D4 in [00-6A]).
Still, both rounds report median 11.0048, minimum 8.9653, maximum 11.1351 ([S5A] §1; [S6A] §1).
Reading the two episode logs for this story, I found the branch sequence identical on 30 seeds of 30,
2000 episodes each ([EP5], [EP6]): both rounds chose the same convention, so the same data.

**The optional "bonus".** A′: five of six elements both times, $\sqrt{11}$ missing ([REG5] line 41;
[S6A] §8). B′: the same three of four both times; round 6 calls it "full" because the answer accepts
any of them, a difference of wording, not of documents ([REG5] line 45; [S6B] §8).

## What changed in the documents

Same model, same text, same data, and the frozen criteria were nonetheless written differently.

**A′.**
- *Primary criterion.* Round 5 counted seeds: pass with at least 27 of 30 ratios $\ge 5$, fail with at
  most 15 ([S5A] §3). Round 6 used an order-statistic interval $[R_{(10)}; R_{(21)}]$, coverage
  0.9572: pass if $R_{(10)} > 5$, fail if $R_{(21)} < 5$, `INCONCLUSIVO` if it contains 5, "boundary
  from the statement, no equivalence margin (D3, rule 19)" ([S6A] §2). Measured $R_{(10)}$ = 10.8805
  ([S6A] §9).
- *Seeing a guard fire.* Round 5 ran a third arm, K, trained halfway by construction, on which the
  learning guard had to trip ([S5A] §4); it tripped 30 / 30 ([S5A] §9). Round 6 has two arms. Its
  guards were seen to fire on sabotaged copies of the logs, G3, G2a, G2d and G1 ([05-6A] «Le guardie
  possono scattare»); the learning guard G4 was not, and the criteria say why: G4 is read only after
  the replay guard G3 passes, and the bench failures G4 would catch are stopped by G3 first ([03-6A]
  note N2).
- *Where the strict readings bite.* Round 5: the reference dynamics is not labelled as such, and one
  sentence claims a recomputation "in `Fraction`" that used literals ([REG5] line 41). Round 6: three
  side criteria (C3, C5, C6) declare that they can fail but give no numeric power under an
  alternative; and the verdict body states a false mechanism (it explains MC's extra spread by the sign
  of the sample's deviations, while that error depends only on their size) and writes "disagrees" on
  diagnostics frozen as not judged ([S6A] §9, §10). Different faults, same total: 2 / 4 under both readings.

**B′.**
- *Primary criterion.* Round 5: zones on the per-seed ratio, measured in zone C with $k_> = 30$ and
  $M_R$ = 10.1998 ([S5B] §3, §7). Round 6: the paired difference $D_s = E_{V2} - E_{V1}$ with a
  95 % $t$ interval, [0.043744; 0.045967], 0 seeds of 30 below zero, ratio of means 10.274 ([S6B]
  §1-bis). Per-seed ratios span 8.34 to 12.63 in both ([REG5] line 45; [S6B] §1-bis).
- *The trap.* Under the damped form $v \leftarrow \beta v + (1-\beta) g$ the claim becomes true, by
  0.47 %. Round 5 anticipated it and declared it out of domain ([REG5] line 45). Round 6 turned it
  into a power check: under that dynamics the primary test lands in "supports" with probability 0.81,
  which shows that the instrument can say yes ([S6B] §3, §8).
- *Strict readings.* Round 5: 2 / 4 ([REG5] line 45). Round 6: 3 / 4; only P1 bites, partly because
  the reference dynamics is still not named, partly because a protocol whose primary can never title
  `PASSA` on this fixed environment meets the rubric's "a criterion that cannot pass counts 0" head-on.
  The scorer found no strict reading of P4 it could defend ([S6B] §3, §9, §11).

Rules 18 and 19 appear in both runs without work to do: A′ cites rule 19 to exclude an equivalence
margin ([S6A] §2); B′ finds no task success criterion for rule 18 to gate on ([S6B] §4).

## Moment 1 — A′ did the whole job twice and refused to look at the first attempt

The first launch started at 19:19:26 (a time from the launch mandate; no file keeps it) and froze
its criteria in a dedicated commit at 20:53:15 (`13fa6d8`, 497 lines). At 20:53:49 the session died
on the usage quota; no implementation existed.
Four automatic relaunches, at 21:11:48, 21:27:56, 21:44:02 and 22:00:08, each failed at pre-flight
within seconds. A manual relaunch at 22:11:48, with the same prompt, did not resume the run: it opened
a new one ([S6A] §6, §12; [GIT-6A]).

The new coordinator found its own predecessor's frozen criteria in `run/` and wrote, at line 5 of the
new problem file: "In `run/` there is `20261017-mc-vs-td-aggregazione`, on a similar question,
stopped at frozen criteria and without implementation. By the user's instruction **it is not this
question** […] no agent of this run reads the files of that run […]. The instruction would allow
reusing its method and code with a citation; we decline, because the method can be derived from the
statement in a few lines and independence is worth more than the time saved" ([00-6A] line 5). The
"instruction" is a note in the prompt, written for a different run seeded on 2026-08-02: "if `run/`
holds a previous run on a similar question, it is not this question" ([S6A] §6; [PRE6] Amendment 2).
Applied to the lab's own interrupted run, the clause turned against the run itself.

The second run redid sources, method, two rounds of critique and the freeze, and reached the
counter-verdict at 23:11:14. The scorer checked for copying: 14 of 250 non-empty lines of the criteria
and 7 of 186 of the method are identical, all of them section headings, table separators and one fixed
sentence of the lab's template; the log schemas differ. And the primary criterion is the same: per-seed
paired ratio, pass if $r_{(10)} > 5$, `INCONCLUSIVO` if the order interval contains 5 ([S6A] §6). The
scorer reads this as "compatible with two independent derivations", and names what would falsify it:
a transcript of the second run opening a file of the first ([S6A] §6).

So, by accident, the lab ran a reproducibility test on its own design: two coordinators blind to each
other, the same criterion. The price, from the scorer's arithmetic: the abandoned run cost 1 h 34 min
23 s, more than the complete one (59 min 43 s); 2 h 34 min 06 s of effective work, 3 h 52 min 05 s
wall clock, 1546 extra lines of Markdown ([S6A] §12). Round 5 had done the same case in 42 min 28 s
([REG5] line 41).

## Moment 2 — B′: a `replace` pasted the coordinator into the critic's sentence

To append its checkpoint-2 section to the critique file, the B′ coordinator ran in Python
`s.replace('<!-- FINE DOCUMENTO -->', section + terminator)` with no occurrence limit. The critic's
text quoted that terminator between backticks, in a sentence about document endings. Both occurrences
were replaced: the coordinator's section appeared twice, once at the end and once inside the critic's
sentence ([05b-6B] «CHECKPOINT 4», N1). The file at commit `7cc0029` has 199 lines and two copies; the
repaired one 189 lines and one ([S6B] §2-bis).

The coordinator's integrity check looked only at the last line (`tail -1`), and passed. The
counter-verdict found the defect, as N1: "exactly the case 'the existence of an artifact is not its
completeness' [one of the lab's hygiene rules, [LAB6]]: the terminator check passed, because the
terminator was there, twice over" ([05b-6B] N1). The defect dated from `7cc0029`,
committed in the same second as the criteria freeze (23:41:43); it was repaired after the verdict in
`d905e15` (−11 / +1 lines), and the frozen criteria file has a single commit, `2d32434`, untouched
by both ([S6B] §2-bis; [GIT-6B]). The coordinator adopted a process fix inside the same file: append
only at the end, and count the lines that *start* with the terminator, expected 1 ([05b-6B]
«CHECKPOINT 4»).

The scorer, too, first wrote "the first occurrence" and corrected it to "all" in an errata ([S6B]
§7). Effect on the score: declared, not punished; the critique's content is the same in both versions
([S6B] §2-bis).

## The score, on two axes

Verdict asks whether the title matches the sealed answer; path asks four yes/no questions of the
frozen documents and the raw logs ([RUBRIC]). Both cases score 1 / 1 and 4 / 4 in both rounds. The
strict readings are where the rounds differ: A′ stays at 2 / 4, for different faults; B′ moves from
2 / 4 to 3 / 4 ([REG5]; [REG6] lines 89, 93). They hinge on the open entry `<domanda aperta 7>`: the rubric
requires naming the reference dynamics, the lab's rules do not ([REG5] line 41; [PRE6] §4 item 1).

Round 6 as a whole: verdict 4 / 4, path 16 / 16 (10 / 16 strict), and the roadmap sentence it had to
earn recorded as bought ([REG6] line 105); the other two cases are told elsewhere.

## What changed afterwards

No rule was born from round 6 and no round 7 is planned ([REG6] line 105). The "similar run" clause
was left in the prompts with the round open, its risk declared ([PRE6] Amendment 2); the files I read
record no later change. B′'s process fix lives only in that run's file ([05b-6B] «CHECKPOINT 4»).

---

## Sources

Bench files are sanitized copies (Italian; see [SANITIZATION.md](../../SANITIZATION.md)) in [`results/bench/`](../bench/); the two round-6
scores were copied for this story and are checksummed in `SHA256SUMS.txt`. Paths without links are
relative to the author's `<workspace>/` directory and are not part of this showcase.

| Key | File |
|---|---|
| [REG5] | [`results/bench/registro.md`](../bench/registro.md), lines 41 (A′) and 45 (B′), round 5 |
| [REG6] | [`results/bench/registro.md`](../bench/registro.md), lines 89 (A′), 93 (B′), 105 (round-6 summary) |
| [S5A] | [`results/bench/2026-10-17-punteggio-giro5-A-primo-peso-condiviso.md`](../bench/2026-10-17-punteggio-giro5-A-primo-peso-condiviso.md) |
| [S5B] | [`results/bench/2026-10-17-punteggio-giro5-B-primo-momentum-e-rumore.md`](../bench/2026-10-17-punteggio-giro5-B-primo-momentum-e-rumore.md) |
| [S6A] | [`results/bench/2026-10-17-punteggio-giro6-A-primo-peso-condiviso.md`](../bench/2026-10-17-punteggio-giro6-A-primo-peso-condiviso.md) |
| [S6B] | [`results/bench/2026-10-17-punteggio-giro6-B-primo-momentum-e-rumore.md`](../bench/2026-10-17-punteggio-giro6-B-primo-momentum-e-rumore.md) |
| [PRE6] | [`results/bench/2026-10-17-preregistrazione-giro6.md`](../bench/2026-10-17-preregistrazione-giro6.md), §1-§4 and Amendment 2 |
| [RUBRIC] | [`results/bench/punteggio.md`](../bench/punteggio.md) |
| [LAB6] | [`harness/claude-code/giro6/CLAUDE.md`](../../harness/claude-code/giro6/CLAUDE.md) (rules 1–19, the round-6 system) |
| [R5A], [R5B] | [`round5-A1-shared-weight.md`](round5-A1-shared-weight.md), [`round5-B1-momentum-noise.md`](round5-B1-momentum-noise.md) |
| [GIT-6A], [GIT-6B] | `git -C laboratorio-giro6-A1 log --format='%h %ad %s' --date=iso`, same for `laboratorio-giro6-B1` |
| [00-6A], [03-6A], [05-6A] | `laboratorio-giro6-A1/run/20261017-td-vs-mc-rapporto-ve/`: `00_problema.md`, `03_criteri.md`, `05_verdetto.md` |
| [05b-6B] | `laboratorio-giro6-B1/run/20261017-momentum-sgd-regime/05b_controverdetto.md` |
| [EP5], [EP6] | `episodi.csv` in `04_impl/logs/` of `laboratorio-giro5-A1/run/20261017-td-vs-mc-aggregazione/` and of the [00-6A] folder |
