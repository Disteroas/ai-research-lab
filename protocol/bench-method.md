# The bench: how the lab is tested

The lab produces verdicts. The bench is how one knows whether those verdicts are right. It is a set
of problems whose **answer is already known**, rerun at every change of the lab. "The lab works"
means the bench says so.

Without known answers, *the lab got it wrong* and *that question was hard* feel identical from the
inside, and any modification will look like an improvement.

Reference texts (Italian; copies in `../results/bench/`): the bench README, `punteggio.md`
(the rubric) and the route document. Case texts are **not** in this file: consumed cases are
published separately, sealed ones never.

## Sealed oracles, outside the lab's repository

- Each case is a problem text plus a **truth** (expected verdict, its derivation, the conditions
  that would invalidate the case). Truths come from closed-form computation on a synthetic
  environment, from the literature, or from construction (e.g. a deliberately poisoned protocol),
  and when a number needs checking it is checked by a calibration script **run by the human**.
- The truths live in a directory **outside the lab's repository**. If they were inside, an agent
  could read them while working: the blind would fall without anyone noticing, and every later
  score would be worthless.
- The lab's repository contains **no reference to the bench**. If a run ever mentions the bench's
  location, that case is void.
- The bench covers every state of the verdict on purpose: a case that **must pass** (the one people
  forget to build, and the only way to catch false negatives — a lab that says `NON PASSA` to
  everything is indistinguishable from a rigorous one), a case that **must not pass** (the lab can
  contradict a plausible claim), a case that **must not conclude** (`INCONCLUSIVO` is the right
  answer), and a case with **an arm broken in silence** (a guard must stop the run). Which case plays
  which role is written only in the sealed truths.
- At least one truth is synthetic and reported by no paper: if the lab gets it wrong, the error is
  100 % the lab's.

## The blind rule

The lab **must not know it is being tested**. It receives the case text as its problem and nothing
else: no "this is a test", no "I already know the answer", no reaction at checkpoints that reveals
the expected direction. Truths are not opened before the case is finished.

The blind is proof against distraction, not against an adversary: an agent with a shell that left
its folder could find the truths. The defence is that it has no reason to look, plus an explicit
boundary in the launch prompt.

**Known limit**: as long as the same person builds and scores the cases, the operator can leak the
expected direction at checkpoints. Mitigations: at checkpoints, approve or reject **without
commenting on the merits**; better, launch unattended (no human checkpoints at all — the coordinator
decides and documents); best, cases written by one person and scored by another.

## Pre-registration before any launch

Before the first launch of a round, a pre-registration document is written and committed:
acceptance rules, **denominators** (verdict n/k, path n/4k), which system version is under test,
how outcomes are attributed. Then:

- **One system for the whole round.** The definitions (agents, coordinator, rules file) are
  snapshotted with their sha256 and the environment (harness version, pinned model, plugins, hooks);
  a verification script checks the live system against the snapshot **before and after** every run.
  A run during which the system drifted is not interpretable.
- **The model is pinned** and checked by a pre-flight request; a run that switches model halfway is
  not interpretable (it happened once, through an inherited default).
- **No modification of the lab between two cases of the same round.** Otherwise the scores belong to
  different systems and do not add up. Change one thing, rerun the whole bench, compare.
- If a case of a round reveals a new defect, the round is closed and scored anyway; the repair goes
  into the next round.

## The rubric: two numbers, never summed

A right verdict for the wrong reason is the typical way a lab looks like it works and does not:
summing the two scores would hide it again.

### Number 1 — Verdict (0-n)

One point per case if the final verdict matches the expected one. No partial credit. Borderline
cases are decided by the sealed truth of that case, not by eye.

### Number 2 — Path (0-4n)

Four binary checks per case, scored by reading `03_criteri.md`, `03b_critica.md`, `05_verdetto.md`
and the raw logs — **not** the story the lab tells about itself.

| # | Check | Passes if |
|---|---|---|
| P1 | **Two-direction criteria** | For every criterion there is a concrete, nameable outcome that would make it **fail**, *and* one that would make it **pass**, and power is declared under a dynamics **different** from the one the criterion puts to the test. A criterion that cannot fail scores 0. One that cannot pass scores 0. Also 0 if the critic approved it. **Exception (E-P1b)**: a criterion declared inert **before measurement**, with the derivation of its inertness, does not zero P1 — provided the load-bearing criterion remains two-directional. **Power threshold (E-P1c)**: the load-bearing criterion must have declared power **≥ 0.50 under the reference dynamics** (the one the frozen document identifies as the most plausible if the hypothesis is false), otherwise P1 = 0; from round 5, a document that does not identify the reference dynamics scores P1 = 0. |
| P2 | **Sanity gate** | The frozen criteria require that the manipulation worked on **all** arms before any effect is evaluated. |
| P3 | **Faithful method** | Every number and parameter in `02_metodo.md` is traceable to a source or a derivation. No number out of nowhere. |
| P4 | **Verdict within the data** | `05_verdetto.md` asserts nothing the raw logs do not support. Decided by the counter-verdict, reread by the scorer. |

P3 measures **provenance**, not truth: a wrong but declared derivation passes P3 by construction.
If a run fails because of a wrong derivation, the defect goes into the round notes, not the score.

A case built around a poisoned protocol weighs double on P2: if the gate is missing, P2 = 0 even if
the final verdict is correct.

**Why E-P1b and E-P1c exist.** E-P1b: a lab rule requires declaring pre-forced outcomes before
measurement, and the literal P1 punished that declaration — rewarding silence. E-P1c: one round
showed a load-bearing criterion with power 0.050 against a size of 0.05 under the dynamics the
document itself called dominant — it passed almost equally with the hypothesis true or false, and P1
had no tooth to see it. The threshold is read in the frozen document, not judged by the scorer.

### Changing the yardstick

Changing the rubric between two cases of the same round makes them incomparable. Every amendment is
made **between** rounds, recorded with its date, and comes with a **declared retroactive rescoring**
of the rounds it touches.

## Scoring in two times, separated by a commit

Scoring happens in a **fresh session**, distinct from whoever observed the run, one case per session:

1. **Invalidation first.** Before anything else, check the case's invalidation conditions (blind
   broken, system drift, model switch, sealed conditions in the truth).
2. **Path before verdict.** Score P1-P3 from the frozen documents and **commit** those scores
   **before opening the verdict**. Only then read `05_verdetto.md`, score the verdict and P4.

The commit makes it checkable that the path score was not influenced by knowing whether the verdict
was right.

## Consumed cases and the fallen oracle

- A case whose answer can be read from the lab's own instructions — because a rule was written from
  that case — is **consumed**: it no longer tests anything and is replaced. Consumed cases are
  recorded, and only consumed cases are ever published.
- **Fallen oracle** (verdict with denominator 0, any path): the invalidation check voided the case,
  so the bench can no longer answer on it. The verdict is **not scored** — neither merit nor blame:
  looking at the verdict first, a coincidence of titles could be mistaken for merit (it happened
  once: `INCONCLUSIVO` titled for a reason unrelated to the expected one). The path stays informative
  and is scored in full. The case is consumed and must be replaced; if the same truth falls twice,
  the defect is in the design of the truths, not in the case.

## How to read the result

- **Verdict perfect on the first round**: suspicious, not a triumph. Look at the path: if it is low,
  the lab guessed.
- **Verdict low, path high**: the lab is rigorous and wrong. The best place to be — the error is
  localised and repairable.
- **Verdict high, path low**: the worst case, because it is invisible without the bench. The next
  runs will give credible, unverifiable answers.
- **The must-pass case wrong** (false negative): absolute priority. A lab that cannot say yes is
  useless, and this defect never surfaces in real runs, where a `NON PASSA` always looks like prudence.

## When the bench must be thrown away

- A case that gives the expected outcome **three rounds in a row without ever coming close to
  missing it** no longer discriminates: replace it.
- A poisoned-protocol case that stops biting (faster machine, more efficient implementation) must be
  re-budgeted and its truth rebuilt.
- A "literature" truth that turns out to be contested is no longer an oracle: downgrade it or
  replace it with a synthetic one.

## Human attention

Not part of the score, but recorded for every case: an estimate, declared by the human at the end
of the run, of the minutes of real reading the case cost, checkpoints included. It answers the
question that decides whether the lab is worth having — whether it frees more time than it costs —
and it cannot be reconstructed afterwards. It is written as an estimate, not a measurement.
