# Result scaffold: LEDH-PFPF-OT retained-teacher Phase 1 baseline rung

## Phase
Phase 1 — exact-route baseline rung

## Question
Did the exact same-route cold / zero-init batched streaming LEDH-PFPF-OT reference lane execute successfully under the frozen whole-program contract, and did it produce a trusted baseline artifact for later retained-teacher comparison?

## Master program reference
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-neural-ot-master-program-2026-06-25.md`

## Inherited evidence contract
This result note inherits the master program's frozen baseline and evidence contract:
- same GPU device,
- same JIT/compiled mode,
- same precision mode,
- same seeds,
- same particle counts,
- same transport settings,
- same cost definition,
- same barycentric output rule.

This phase is not promotable. Its job is only to certify the reference rung used by later phases.

## Run manifest
| Field | Value |
| --- | --- |
| Git commit | |
| Command | |
| Environment | |
| GPU / device | |
| Precision mode | |
| JIT / compiled mode | |
| Seed(s) | |
| Particle count(s) | |
| Transport route | |
| Output artifact(s) | |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-neural-ot-master-program-2026-06-25.md` |

## Baseline artifact summary
- Cold / zero-init arm artifact path:
- JSON summary:
- Markdown summary:

## Hard-gate checks
| Check | Status | Notes |
| --- | --- | --- |
| Finite outputs | | |
| Trusted requested device execution | | |
| Memory growth applied before execution | | |
| Same declared transport route | | |
| Residual contract satisfied | | |
| Same barycentric semantics preserved | | |
| No fallback off intended GPU/JIT path | | |

## Primary diagnostics
- Warm-call median seconds:
- Compile + first-call seconds:
- Residual summary:
- Finite-output flag:
- Route metadata:

## Secondary diagnostics
- Warm-call timing list:
- GPU memory snapshots before/after:
- Shape / transport settings echo:
- Any descriptive precision notes:

## Decision table
| Decision field | Status |
| --- | --- |
| Did Phase 1 pass? | |
| Main pass reason | |
| Main unresolved issue | |
| Allowed next phase | `Phase 2 — warm-start correctness rung` only if all hard gates pass |
| What is not concluded | No effectiveness, no speed claim, no retained-teacher benefit claim |

## Interpretation
- If all hard gates pass, this baseline rung is certified as the reference comparator for later retained-teacher phases.
- If any hard gate fails, the master program must not advance to retained-teacher comparison until the baseline route is repaired and rerun.

## Post-run red-team note
- Strongest alternative explanation if this rung looks unusually good or bad:
- Smallest follow-up check if there is any route/device ambiguity:
- What would invalidate the baseline as a later comparator:
