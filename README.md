# A research lab made of AI agents, and the bench I built not to trust it

The lab is a chain of AI agents that takes a research question from "hypothesis" to a measured
verdict, with the pass/fail criteria frozen in git before anything is measured. The bench is a set of
problems with known answers, sealed where the lab cannot see them, built to catch the lab fooling
itself.

On the latest version the lab got 4 blind cases out of 4: it said yes, it said no, it said "I don't
know", and it stopped in front of a broken experiment. Before that, the bench had caught it out five
times in a row.

## Results

Each round runs one version of the lab, once per case, on cases it has never seen. Two scores, never
added together: **verdict** (does the lab's title match the sealed answer?) and **path** (four checks
per case, read on the frozen criteria and the raw logs: can the criteria fail, is every arm
sanity-checked, is every number traceable, does the verdict stay within the data).

| Round | Lab version | Cases | Right verdicts | Path | What the bench found | Source |
|---|---|---|---|---|---|---|
| 1 | `8d27db5`, rules 1-3 | 1 | 0/1 | 2/4 | A false negative: the measurement matched the theory, but the lab titled "does not pass". It had no rule for turning several criteria into one verdict. | [register](results/bench/registro.md), line 25 |
| 2 | `a7b22b1`, rules 1-6 | 2 | 2/2 | 8/8 | Both right, but one "pass" leaned on a vague rule for combining criteria, and "inconclusive" was never exercised: both effects were huge. | [register](results/bench/registro.md), line 29 |
| 3 | `a7b22b1`, rules 1-6 | 1 | not scored | 2/4 | The bench's own test case broke (its built-in flaw no longer bit: both arms learned) and was voided. The tool that checked which lab version had run was reading the wrong file. | [register](results/bench/registro.md), line 33 |
| 4 | `bece2ac`, rules 1-11 | 1 | 1/1 | 2/4 | Right title, blind guard: the sanity check passed 30/30 on the arm built to be broken, because it looked at the best stretch of learning, not the final one. | [register](results/bench/registro.md), line 37 |
| 5 | `8958eb7`, rules 1-17 | 4 | 2/4 | 15/16 | No guard stopped a silently broken arm. On a case whose right answer was "I don't know", the lab titled "pass, equivalent", with a margin nobody had asked for. | [register](results/bench/registro.md), line 61 |
| 6 | `128634d`, rules 1-19 | 4 | 4/4 | 16/16 | A guard stopped the broken run, and "I don't know" came for the right reason. No new rule was needed. | [register](results/bench/registro.md), line 105 |

Every rule of the lab was written after one of these failures; the full list, each with the failure
behind it, is in [`protocol/rules.md`](protocol/rules.md). Paths are as listed in the register's
round-6 summary (line 105), which rescores rounds 1 and 3 on the current rubric. Round 6 took about
5 h 26 min of agent work for the four cases and zero minutes of human attention on content (same line).

Scores have declared alternative readings; see [docs/DETAILS.md](docs/DETAILS.md).

### The lab against a single session

After round 5, the same four cases went to a single session of the same model, with a short preamble
asking for criteria before code, raw logs and a three-state verdict. No sub-agents, no critic, no
checkpoints.

| Round-5 cases (4) | Right verdicts | Path | Time |
|---|---|---|---|
| Lab (round-5 version) | 2/4 | 15/16 | ≈ 3 h 21 min |
| Single session | 3/4 | 10/16 | ≈ 17 min |

Sources: [register](results/bench/registro.md), line 81, with the corrected lab time on line 85.

The structure paid in auditability, not in verdicts. On the "I don't know" case the single session was
right and the lab was not. The comparison was not repeated on round 6
([story](results/round5-ablation-single-session.md)).

## Two moments worth reading

**The guard that stopped the run.** The claim: an agent that explores more (ε = 0.3 instead of 0.05)
reaches the task's success criterion sooner. With ε = 0.3 the criterion is out of reach, on 0 seeds out
of 30. The tempting title was "does not pass"; instead the guard on the task's own criterion fired, and
the lab titled "inconclusive, forced": the comparison is void, not negative. In rounds 4 and 5 the same
kind of case went through unstopped. [Story](results/cases/round6-E2-how-much-to-explore.md).

**"I don't know", for the right reason.** The claim: three nearest neighbours beat one on this problem.
Over 30 seeds the mean difference in error was 0.000167, with a 95 % interval of [−0.010041, 0.010374].
The lab titled "inconclusive" and wrote that this means neither "no effect" nor "equivalent". The
previous version had titled a similar case "pass, equivalent".
[Story](results/cases/round6-D2-one-or-three-neighbours.md).

## How it works

```
question
  ├─ scouts (1-4, in parallel) → sources        ◆ 1: choose the sources
  ├─ analyst                   → method + criteria
  ├─ critic                    → "can it fail? can it pass?"
  │                                              ◆ 2: freeze the criteria (own commit)
  ├─ implementer               → code + logs    ◆ 3: what was built
  ├─ validator                 → verdict
  └─ critic again              → counter-verdict, from the raw logs
                                                 ◆ 4: outcome
```

Each ◆ is a checkpoint where a human decides; on the bench nobody was watching, so the coordinating
agent decided and wrote down why. Three rules are not negotiable:

- the criteria are frozen in their own commit before the first line of code, and `git log` proves it;
- the raw logs are committed before the counter-verdict, so a deleted log shows in the history;
- the critic does not write: it reads and returns its objections, nothing else.

The bench: the answers live outside the lab's repository, and a run that mentions them is void; the
lab gets the problem text and nothing else, and each round is pre-registered with its acceptance rule;
verdict and path are scored separately, so a right answer for the wrong reason stays visible.

## Try it / reuse

- [`protocol/`](protocol/): the six roles, the 19 rules, the artifacts and the bench method, independent
  of any tool.
- [`harness/claude-code/`](harness/claude-code/): sanitized copies of the files that were measured (see [SANITIZATION.md](SANITIZATION.md)), with checksums
  and launch scripts.
- [`harness/openai-compatible/lab.py`](harness/openai-compatible/lab.py): a one-file orchestrator for any
  OpenAI-compatible endpoint (Ollama, vLLM, LM Studio). Portable, not measured.
- [`cases/`](cases/): the four round-6 cases with their sealed answers, now public. Whoever reruns them
  measures memory, not method.

**All the numbers were measured only on Claude Code, with Opus 5.5 in rounds 5 and 6 (Opus 5 in rounds
2-4).** Nothing else has been tested by the bench
([round-5 pre-registration](results/bench/2026-10-17-preregistrazione-giro5.md), lines 37-38).

## What this is not

- Not real-sized: every case is synthetic, and a round-5 run used 0.44 s to 3.34 s of compute
  ([register](results/bench/registro.md), lines 41 and 53).
- Not general: one model family, one harness, one run per case.
- Not a statistic: the best result rests on four runs.
- Not used for real work: it has never served my actual research
  ([rules file](harness/claude-code/CLAUDE.md), line 5).

Details, caveats, errata and provenance: [docs/DETAILS.md](docs/DETAILS.md).
License: to be chosen before the repo goes public.
