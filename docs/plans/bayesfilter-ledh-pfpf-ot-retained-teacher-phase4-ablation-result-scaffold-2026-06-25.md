# Result scaffold: LEDH-PFPF-OT retained-teacher Phase 4 within-family ablation rung

## Phase
Phase 4 — within-family ablation rung

## Question
Among already-supported retained-teacher variants (for example `learned_base` vs `learned_wide`), is there any explanatory evidence that one learned arm is preferable, conditional on the frozen baseline contract?

## Master program reference
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-neural-ot-master-program-2026-06-25.md`

## Status note
This phase is explanatory unless a variant is explicitly compared back to the frozen cold baseline under the same contract.

## Run manifest
| Field | Value |
| --- | --- |
| Git commit | |
| Commands | |
| Environment | |
| Compared variants | |
| Device / precision / budget | |
| Output artifact(s) | |

## Variant comparison
| Metric | Variant A | Variant B | Notes |
| --- | --- | --- | --- |
| Warm-call median seconds | | | |
| Teacher-preservation discrepancy | | | |
| Residual parity | | | |
| Latent/state loss | | | |
| Iteration burden | | | |

## Interpretation boundary
- Explanatory-only unless variant performance is tied back to the frozen cold baseline.
- No promotion claim from within-family comparison alone.

## Decision table
| Decision field | Status |
| --- | --- |
| Did a variant dominate descriptively? | |
| Is any conclusion promotable? | |
| Allowed next phase | `Phase 5` or `Phase 6` |
| What is not concluded | No broad superiority claim from ablation alone |

## Post-run red-team note
- What could make the apparent variant difference spurious:
- Smallest additional baseline-linked check if needed:
