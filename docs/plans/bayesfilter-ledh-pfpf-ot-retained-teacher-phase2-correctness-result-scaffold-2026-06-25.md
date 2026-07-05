# Result scaffold: LEDH-PFPF-OT retained-teacher Phase 2 correctness rung

## Phase
Phase 2 — warm-start correctness rung

## Question
Under the frozen whole-program contract, do the `cold`, `heuristic`, and `learned` retained-teacher arms preserve the exact same transport semantics, teacher-preservation envelope, and residual contract before any runtime comparison is interpreted?

## Master program reference
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-neural-ot-master-program-2026-06-25.md`

## Inherited evidence contract
This phase inherits the same frozen baseline and exact-route contract. The only allowed comparison is between same-route arms under matched device, precision, seed, particle count, and corrective budget.

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
| Arms run | `cold`, `heuristic`, `learned` |
| Output artifact(s) | |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-neural-ot-master-program-2026-06-25.md` |

## Hard-gate checks by arm
| Arm | Finite outputs | Residual parity | Teacher/object drift | Same route | Same barycentric semantics | Pass? |
| --- | --- | --- | --- | --- | --- | --- |
| cold | | | | | | |
| heuristic | | | | | | |
| learned | | | | | | |

## Primary correctness diagnostics
- Teacher-preservation discrepancy / RMSE:
- Residual summary by arm:
- Any route or output-semantic mismatch:

## Secondary diagnostics
- Compile + first-call time:
- Warm-call timing summaries:
- Memory snapshots:
- Latent/state loss if relevant:

## Decision table
| Decision field | Status |
| --- | --- |
| Did Phase 2 pass? | |
| Which arms preserved semantics? | |
| Which arm failed first, if any? | |
| Allowed next phase | `Phase 3 — warm-start effectiveness rung` only if the compared arm(s) pass |
| What is not concluded | No speed or effectiveness promotion yet |

## Interpretation
- If an arm fails semantic preservation, it is excluded from effectiveness reading.
- If all compared arms pass, Phase 3 may interpret runtime differences.

## Post-run red-team note
- Strongest alternative explanation for a correctness failure:
- Smallest discriminating follow-up check:
- What would force a return to Phase 1:
