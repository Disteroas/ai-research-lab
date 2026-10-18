# The 19 rules

Reference texts (Italian), numbered as in the original: rules 1-17 in
[`harness/claude-code/CLAUDE.md`](../harness/claude-code/CLAUDE.md), the system of round 5 (FIX 1-16);
rules 1-19 in [`harness/claude-code/giro6/CLAUDE.md`](../harness/claude-code/giro6/CLAUDE.md), the
system of round 6 (FIX 1-17). Each rule was written after a real failure: rules 1-3 come from the
first real run, 4-6 from the second, 7-11 from round 2 of the bench, 12-17 from round 4, 18-19 from
round 5. Rules 18 and 19 have been through one scored round, round 6: rule 18's gate fired on the
broken arm of E″ and the run stopped with a declared `INCONCLUSIVO (forzato)`; rule 19 titled D″
`INCONCLUSIVO`, with no equivalence margin; both cases scored verdict 1/1, path 4/4 on the substantive
reading (2/4 and 3/4 on the strict one) ([registro.md](../results/bench/registro.md), line 105). Each "why" below is one line; the full
story is in the reference text.

The structural rules that are not numbered (dedicated criteria commit, one committer, independent
validator, read-only critic) are in [`README.md`](README.md#non-negotiable-rules).

## From the first real run

**1. A guard on one arm is asked of all arms.** Mechanical end-of-draft check: arms on the rows,
guards on the columns, every empty cell is a question. Watch for guards that open by themselves
(`a ≤ b + δ` holds when `a` and `b` are both zero).
*Why:* the run guarded "the control arm must have learned" but not the experimental arm, which then
learned nothing — and the run, completed and validated, established nothing.

**2. Frozen constants are produced by the bench code.** Never by a script written for the occasion.
*Why:* a baseline frozen at 0.6835 from a side script was 0.72 on the real bench, so every derived
threshold was calibrated on a bench that did not exist — and it survived two rounds of critique.

**3. "Can it pass?" is asked together with "can it fail?".** Power is declared, not merely
assumed: "if the true effect is X, this criterion passes with probability Y".
*Why:* a criterion had probability 0.12 of passing with the hypothesis true (0.00 with the metric's
ceiling), and nobody noticed — a refutation produced by calibration is p-hacking with the sign reversed.

## From the second real run

**4. A list of criteria is not a verdict.** `03_criteri.md` contains a frozen aggregation rule:
for each criterion both failure directions and what they imply, which criteria are load-bearing,
and what is titled when a load-bearing one fails in the direction that *strengthens* the hypothesis.
Without it the validator reports the count and does not title.
*Why:* the correct reading was frozen before measurement, the verdict wrote it four lines below the
title, and still titled `NON PASSA` by counting "7 out of 8".

**5. Power is not asked of the model under test.** Declared under at least two dynamics: the assumed
model and a concrete alternative it excludes. Check the "clock" (rate-to-duration conversion) separately.
*Why:* a clock off by 1/ε = 200× made a criterion impossible to pass, and it survived two critique
rounds because both asked the same source.

**6. The verdict has three states.** `PASSA`, `NON PASSA`, `INCONCLUSIVO`.
*Why:* without the third, "the experiment does not decide" always came out as `NON PASSA` — two
runs out of two titled more strongly than their body.

## From round 2 of the bench

**7. A pre-forced outcome deserves its own label.** If `03_criteri.md` declares before measurement
that an outcome of the load-bearing criterion is forced by arithmetic, the composition rule does not
map it to an ordinary label: `NON PASSA (forzato) — the run measures the bench, not the hypothesis`,
or the scope qualifier inside the title.
*Why:* the qualification was done well in the body and lost in the title, which is the only line
that survives the first summary.

**8. A channel is independent only down to the level at which logs exist.** The bench produces at
least one level below the aggregates (raw samples of one parameter/seed pair, or a hash of the
sample vector).
*Why:* a validator truthfully believed it had "recomputed from raw data" what were in fact the
bench's own aggregates — nothing existed below them.

**9. Reproducibility is proven with git, not with `/tmp`.** Logs are committed after implementation
and again after validation; `git diff <impl> <valid> -- logs/` is the permanent proof.
*Why:* a verdict cited a backup in `/tmp` that evaporated before the counter-verdict, while the git
diff that proved the same thing was already there for free.

**10. Common-mode error between method and bench is declared.** A line in `03_criteri.md` checks the
environment constants printed by the bench against `00_problema.md`, or states that nobody does.
*Why:* if analyst and bench transcribe the same wrong environment, every guard passes; the hole was
once closed only by the critic's manual diligence, which is not a defence of the system.

**11. A failed guard is qualified per arm, in the composition rule.** Every line that says "guards
passed" says on which arms.
*Why:* a guard failed, as pre-registered, on a non-load-bearing arm; read literally the composition
fired no line, and the correct `PASSA` rested on an act of interpretation instead of on the text.

## From round 4 of the bench

**12. The power clause is conditioned on the observed resolution of the metric**, not only on effect
size and sample size. The guard `IQR > 0` on the load-bearing scale, on the control arm, is a
**step of the composition before the title** — not a diagnostic.
*Why:* an effect size of 1.00 obtained by total censoring of an arm made the sign test measure the
censoring, and the frozen power clause reached the title as a guarantee the logs contradicted.

**13. "Pre-forced outcome?" is checked in both directions, and redone at measurement.** "Was the
titled outcome reachable?" *and* "was the other one?" — at drafting and again on the data.
*Why:* the correct answer existed in the body while the header checked only the convenient direction.

**14. Frozen clause texts name the measured quantity, never a metaphor.** A clause naming the log
column is checked by reading the log; one naming a metaphor is checked by interpreting.
*Why:* "abandons the goal" was true for one meaning of "goal" and false for another — the
title-vs-body split happened in three cases out of five.

**15. `come_eseguire.md` contains commands and file schemas, never outcomes.**
*Why:* result numbers in that file reach the validator before measurement — a channel that pierces
independence exactly where it matters.

**16. The schema of every log field read by a criterion is frozen in `03_criteri.md`.** Alphabets,
allowed values, units.
*Why:* an implementer added a third symbol outside the method's two-letter alphabet; harmless, but
no criterion prescribed the alphabet — a specification hole found by luck.

**17. The learning gate cannot rest only on a historical maximum.** It needs a condition on the
final or sustained regime (last window, or median of the last k), and its failure on the
**experimental** arm must be able to **stop** the comparison, not only qualify it.
*Why:* optimistic initialisation gives a non-learning arm an early bump that satisfied a max-based
gate 30/30 on the arm sabotaged on purpose — "ever looked alive" is not "has learned".

## From round 5 of the bench (FIX 17)

Both come from runs with clean measurement and the right diagnosis in the body, where the title had
already been written by frozen criteria the critic had approved: **an unresolved outcome given an
affirmative label**, justified by the fact that the outcome had been predicted.

**18. The gate asks for the task's success criterion, the same for every arm.** When the main
quantity exists only for runs that reach the success criterion (time to criterion, performance
after it), the gate of rule 17 asks **every** arm for the criterion **of the task**: the definition
of success in `00_problema.md`, with the same threshold and the same censoring cap for all arms,
never an arm's own objective. A regime that does not reach that criterion is not admitted, not even
when it is the optimum of that arm's reward or what the method predicts: there the main quantity
has no value, only a censoring, and the comparison stops (`INCONCLUSIVO — <arm> does not sustain the
task's success criterion, k/N seeds`). For the same reason the resolution guard (rule 12) binds every
arm that enters the main criterion: "non-binding because censoring is the expected outcome" is
exactly the case that must stop. If the task fixes no criterion, or if the main criterion is reaching
it, not reaching it is the measurement and rule 17 applies as it is.
*Why:* on case E′ the final-regime gate followed rule 17 to the letter and saw the experimental arm
orbit the waypoint on 30 seeds out of 30, but it admitted that regime for that arm ("learning its own
MDP well means *not* reaching the goal"), and the IQR guard that would have fired was non-binding on
that arm, approved by the critic. Zero guards fired, and the run titled `NON PASSA` on an arm censored
30/30: the defect moved from the measurement into the rule.

**19. "Not distinguishable" is titled `INCONCLUSIVO`, unless the Statement asks for equivalence.**
If the interval of the main criterion contains the boundary the question poses (zero difference, or
the effect threshold of the Statement), the title is `INCONCLUSIVO`, never `PASSA` nor `NON PASSA`,
even if the interval lies inside an equivalence margin. Sole exception: the **Statement** of
`00_problema.md` (the user's words, not the coordinator's answers in phase 0) asks for equivalence and
fixes its margin or the margin's source. Otherwise the margin is a choice of whoever writes the
criteria, and moving it a little changes the label: the equivalence test is reported as a qualifier
of the `INCONCLUSIVO` ("CI ⊂ (−δ, δ), δ without a source"), not as the answer. And rule 6 is not
satisfied because `INCONCLUSIVO` is reachable somewhere: it is satisfied if the outcome that does not
decide gets it.
*Why:* on case D ("which of the two pays less?") phase 0 admitted "not distinguishable" as an answer,
the analyst turned it into an equivalence test with a margin "chosen by the analyst, no source", and
the critic moved that outcome from `NON PASSA` to `PASSA`. The interval [−24.22, 7.72] straddled zero;
the title `PASSA — equivalent within δ = 27.86` holds only for δ ≥ 26.55, and with δ = 25 it would
have been `INCONCLUSIVO`. The body knew it did not know; the title turned "I don't know" into an answer.

The same FIX 17 adds one row to the critic's table for criteria review ("unresolved outcome with an
affirmative label"), so that the critic looks for both defects before the freeze
([`harness/claude-code/giro6/agents/lab-critic.md`](../harness/claude-code/giro6/agents/lab-critic.md)).

## Two hygiene rules (unnumbered in the original, same weight)

**A file's existence is not its completeness.** Check mtime, terminator, pending labels **and the
diff against the last commit**.
*Why:* a worker killed mid-document leaves a file that looks finished, and an inherited terminator
proves nothing.

**A document nobody rereads is an installed defence, not a verified one.** Caps: `02_metodo.md`
≤ 400 lines, `03_criteri.md` ≤ 500, `05_verdetto.md` ≤ 300.
*Why:* one run produced 4,095 lines of prose for 9.17 s of computation.
