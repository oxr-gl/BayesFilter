# Result scaffold: LEDH-PFPF-OT retained-teacher Phase 3 effectiveness rung

## Phase
Phase 3 — warm-start effectiveness rung

## Question
After passing semantic-preservation gates, does the retained-teacher warm-start arm reduce warm-call median time or effective correction burden on the real LEDH-PFPF-OT path relative to the frozen cold baseline?

## Master program reference
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-neural-ot-master-program-2026-06-25.md`

## Inherited advancement rule
Phase 3 is promotable only if the arm being evaluated already passed Phase 2 correctness.

## Run manifest
| Field | Value |
| --- | --- |
| Git commit | |
| Commands | |
| Environment | |
| GPU / device | |
| Precision mode | |
| JIT / compiled mode | |
| Seed(s) | |
| Particle count(s) | |
| Corrective budget | |
| Primary compared arms | |
| Output artifact(s) | |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-neural-ot-master-program-2026-06-25.md` |

## Primary metrics
| Metric | cold | heuristic | learned | Notes |
| --- | --- | --- | --- | --- |
| Warm-call median seconds | | | | |
| Warm-call mean seconds | | | | |
| Teacher-preservation discrepancy | | | | |
| Residual parity | | | | |
| Iteration burden | | | | |

## Veto diagnostics
- Any runtime gain with failed residual parity:
- Any teacher/object drift under the claimed winning arm:
- Any route mismatch:
- Any unfair budget difference:

## Explanatory-only diagnostics
- Compile + first-call time:
- Memory before/after:
- Timing distribution details:
- Descriptive TF32 notes if collected:

## Decision table
| Decision field | Status |
| --- | --- |
| Did Phase 3 pass for `learned`? | |
| Did heuristic match or beat learned? | |
| Main promotion criterion status | |
| Main veto status | |
| Allowed next phase | `Phase 4` or `Phase 6` depending on outcome |
| What is not concluded | No posterior/HMC/default claim |

## Interpretation
- Runtime or correction-burden improvement is promotable only if correctness parity still holds.
- If heuristic and learned are effectively tied, prefer the simpler route unless later evidence changes that judgment.

## Post-run red-team note
- Strongest alternative explanation for an apparent gain:
- Result that would overturn the effectiveness reading:
- Weakest part of the current evidence:
