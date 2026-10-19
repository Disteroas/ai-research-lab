# AI research lab, and the bench that scores it

![The six roles](docs/agents.png)

This repository contains a research lab made of six AI agents and the bench used to test it. The lab
takes a question from hypothesis to verdict, with the pass/fail criteria frozen in a git commit before
anything is measured. The bench gives the lab problems whose answers are sealed out of its reach.

The latest version of the lab got 4 blind cases out of 4, including one where the right answer was
"I don't know" and one where the right move was to stop. Run again, unchanged, on a second batch of
four new cases, it got 4 out of 4 again. In the five earlier rounds, run on four earlier versions, the
bench found a defect every time.

## What the lab does

```
question
  ├─ scouts (1-4, in parallel) → sources            ◆ 1  sources chosen
  ├─ analyst                   → method + criteria
  ├─ critic                    → "can it fail? can it pass?"
  │                                                  ◆ 2  criteria frozen, own commit
  ├─ implementer               → code + raw logs     ◆ 3  build accepted
  ├─ validator                 → verdict
  └─ critic, second pass       → counter-verdict from the raw logs
                                                     ◆ 4  outcome
```

A sixth agent, the coordinator, runs the chain and is the only one that commits. Each ◆ is a
checkpoint where a human decides; on the bench nobody watched, so the coordinator decided and wrote
down why. The rules that carry the design ([`protocol/README.md`](protocol/README.md)):

- The criteria are committed on their own before the first line of code. `git log` shows the order.
- Raw logs and verdict are committed before the counter-verdict, so a deleted log stays in the history.
- The critic has read-only access. It returns objections and writes no file.
- The verdict has three states: passes, does not pass, inconclusive.

Each of the 19 numbered rules was written after a failure; [`protocol/rules.md`](protocol/rules.md)
lists them with the failure behind each one.

## Why it exists, and its limits

The lab was built for fun, as a side project, to find out whether a research lab made of AI agents was
feasible at all: could a chain of agents take a question to a measured verdict without inventing data
or moving the goalposts? The bench exists because the first real run looked rigorous and had measured
the wrong thing. What came out is a verification protocol with a worked example, not a research tool.
Its limits are the ones a reviewer would list first:

- **Sample.** Four cases per round, seven rounds, synthetic problems that compute in seconds. A
  benchmark would need dozens of cases and at least one problem with real data.
- **Circularity.** The cases, the scores and the repairs come from the same model family, in separate
  roles with separate contexts. Role separation is an argument, not a proof; human-written answers
  and a second model on the scoring side would be the next step.
- **Iteration until success.** Six rounds, the last one passed. Every failed round is in the register
  and consumed cases were replaced, which answers the p-hacking objection but not this one: how many
  versions would a fresh batch of cases take? A seventh round answered it: four new cases, never seen,
  run on the byte-identical system with no repairs in between, passed again, 4/4 verdicts and 16/16
  path. One fresh batch is still a small sample, and one of the four cases barely discriminated.
- **The ablation.** A single session with a ten-line preamble got 3 verdicts out of 4 in about 17
  minutes; the lab got 2 out of 4 in about 3 h 21 min on the same cases. Most of the lab's path
  advantage is declared statistical power, which that preamble did not ask for. The structure buys
  auditability; whether it buys verdicts is not shown here.
- **The metric.** Each score declares a substantive and a strict reading of the rubric; on round 6
  they give 16/16 and 10/16. A rubric with that degree of freedom needs several independent scorers
  and an agreement measure before its totals mean much.
- **Scale.** One harness, one vendor, one machine, two runs killed by usage limits and relaunched.
  Nothing here says how the protocol behaves on problems that take hours instead of seconds.

## How it is tested

Each case is a small problem with a known answer. The answer is sealed outside the lab's repository,
and the lab receives the problem text as an ordinary task. A run that mentions the bench is void.
Two scores are kept apart and never added. The verdict score asks whether the title matches the sealed
answer. The path score runs four checks on the frozen criteria and the raw logs: the criteria can fail
and can pass, every arm has a sanity gate, every number is traceable, the verdict stays within the data.
When a case gives rise to a new lab rule, the case is consumed and replaced. Each round is
pre-registered, with its acceptance rule, before the first launch ([method](protocol/bench-method.md)).

## Results

One run per case, on cases the lab had never seen. Versions differ between rounds, so the scores are
not summed.

| Round | Lab version | Cases | Verdicts | Path | What the bench found |
|---|---|---|---|---|---|
| 1 | `8d27db5`, rules 1-3 | 1 | 0/1 | 2/4 | A false negative: the measurement matched the theory, the title said "does not pass". No rule combined several criteria into one verdict ([register](results/bench/registro.md), line 25) |
| 2 | `a7b22b1`, rules 1-6 | 2 | 2/2 | 8/8 | Both verdicts right. One pass leaned on a vague rule for combining criteria, and "inconclusive" was never exercised: both effects were large ([register](results/bench/registro.md), line 29) |
| 3 | `a7b22b1`, rules 1-6 | 1 | not scored | 2/4 | The case itself broke (its built-in flaw no longer bit) and was voided. The tool that checked which lab version had run read the wrong file ([register](results/bench/registro.md), line 33) |
| 4 | `bece2ac`, rules 1-11 | 1 | 1/1 | 2/4 | Right title, blind gate: the sanity check passed 30/30 on the arm built to be broken, because it looked at the best stretch of learning, not the final one ([register](results/bench/registro.md), line 37) |
| 5 | `8958eb7`, rules 1-17 | 4 | 2/4 | 15/16 | No gate stopped a silently broken arm. On the case whose answer was "I don't know", the title was "pass, equivalent", within a margin nobody had asked for ([register](results/bench/registro.md), line 61) |
| 6 | `128634d`, rules 1-19 | 4 | 4/4 | 16/16 | A gate stopped the broken run, and "inconclusive" came for the right reason. No new rule came out of the round ([register](results/bench/registro.md), line 105) |

Paths for rounds 1 and 3 are as rescored on the current rubric in the round-6 entry of the register.

Round 5 failed on two cases, and each failure became a rule ([`protocol/rules.md`](protocol/rules.md)).
Rule 18: the sanity gate asks every arm to reach the task's own success criterion, not the arm's own
objective. Rule 19: when the interval of the main quantity contains the boundary the question poses,
the title is "inconclusive", unless the problem statement asks for equivalence and fixes the margin.
Round 6 reran the two cases that had passed and replaced the two that had produced the rules. Rule 18
fired and stopped the broken run; rule 19 produced the "inconclusive" title
([register](results/bench/registro.md), lines 97 and 101). The four runs took about 5 h 26 min of agent
work, with no human reading the content (line 105).

After round 5 the same four cases also went to a single session of the same model. A short preamble
asked for criteria before code, raw logs and a three-state verdict; there were no sub-agents, no critic
and no checkpoints ([story](results/round5-ablation-single-session.md)).

| Round-5 cases (4) | Verdicts | Path | Time |
|---|---|---|---|
| Lab (round-5 version) | 2/4 | 15/16 | ≈ 3 h 21 min |
| Single session | 3/4 | 10/16 | ≈ 17 min |

Sources: [register](results/bench/registro.md), line 81, with the corrected lab time on line 85.
The structure raises the path score (criteria, gates, checks on the logs), not the verdict score. Most
of the path gap is declared statistical power, which the preamble did not ask for. The comparison was
not repeated on round 6.

Each score file declares its alternative readings; see [docs/DETAILS.md](docs/DETAILS.md).

## Two cases worth opening

**The gate that stopped the run** (round 6). Claim: Q-learning with exploration ε = 0.3 reaches the
task's success criterion sooner than with ε = 0.05. With ε = 0.3 the criterion is reached on 0 seeds out
of 30, so the gate fired and the title was "inconclusive, forced": the comparison is void, not negative.
In round 5 the same kind of case went through unstopped. [Story](results/cases/round6-E2-how-much-to-explore.md).

**"I don't know", for the right reason** (round 6). Claim: three nearest neighbours beat one on this
problem. Over 30 seeds the mean difference in error is 0.000167, 95 % interval [−0.010041, 0.010374].
The title is "inconclusive", with "no effect" and "equivalent" excluded in writing; in round 5 a similar
case was titled "pass, equivalent". [Story](results/cases/round6-D2-one-or-three-neighbours.md).

## Contents

| Path | Contents |
|---|---|
| [`protocol/`](protocol/) | the six roles, the 19 rules, the artifacts of a run, the bench method; independent of any tool |
| [`harness/claude-code/`](harness/claude-code/) | sanitized copies of the files the numbers were measured on (Italian), with checksums and launch scripts; `giro6/` holds the two files changed for round 6 |
| [`harness/openai-compatible/`](harness/openai-compatible/) | `lab.py`, a one-file orchestrator for OpenAI-compatible endpoints (Ollama, vLLM, LM Studio); not tested by the bench |
| [`results/`](results/) | case stories for rounds 5 and 6 and the single-session comparison, in English |
| [`results/bench/`](results/bench/) | register, rubric, pre-registrations and score files (Italian), with checksums |
| [`cases/`](cases/) | the four round-6 cases with sealed answers and calibration scripts; public now, so no longer blind |
| [`docs/`](docs/) | [`DETAILS.md`](docs/DETAILS.md): every number with its source, alternative readings, errata, provenance |
| [`SANITIZATION.md`](SANITIZATION.md) | what was replaced before publication, and why the checksums differ from the originals |

## Scope

Every case is synthetic; a round-5 run used between 0.44 s and 3.34 s of compute
([register](results/bench/registro.md), lines 41 and 53). Each round is one run per case, four cases at
most. **All numbers were measured only with Claude Code, with Opus 5.5 in rounds 5-6 and Opus 5 in
rounds 2-4** ([round-5 pre-registration](results/bench/2026-10-17-preregistrazione-giro5.md), lines
37-38). The lab has not been used on real research ([rules file](harness/claude-code/CLAUDE.md), line 5).
The numbers hold for this setup and no other.

License: [MIT](LICENSE).
Details, caveats, errata and provenance: [docs/DETAILS.md](docs/DETAILS.md).
