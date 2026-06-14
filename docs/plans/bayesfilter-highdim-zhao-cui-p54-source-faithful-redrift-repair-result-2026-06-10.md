# P54 Result: Source-Faithful Redrift Repair

metadata_date: 2026-06-10
program: P54-source-faithful-redrift-recovery
status: COMPLETE_FOR_GUARDRAIL_REPAIR
supervisor: Codex
reviewer: Claude Code read-only

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Accept the P54 source-route guardrail repair. |
| Primary criterion status | PASS.  Required source-route operation coverage now includes previous retained object / marginalization, and drift markers now explicitly include pairwise-grid, all-grid, retained-grid-only, local-neighborhood, and rank-width route drift. |
| Veto diagnostic status | PASS.  The fixed-gradient branch remains separate, no MATLAB source was copied, and no artifact claims the full adaptive TT/SIRT Zhao--Cui filter is complete. |
| Main uncertainty | The executable source-faithful sequential filter remains incomplete because adaptive TT/SIRT transport fit, previous retained-object marginalization, inverse-transport retained sampling, and integrated proposal correction are still future work. |
| Next justified action | Start the next clean-room implementation phase for one-step source reapproximation and transport-fit boundary tests before retrying spatial SIR or predator-prey source-route ladders. |
| What is not concluded | No d=18 spatial SIR readiness, no high-dimensional production readiness, no HMC readiness, no smoothing readiness, and no claim that helper-level tests certify the full Zhao--Cui filter. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `2648501` |
| CPU/GPU status | CPU-only validation; `CUDA_VISIBLE_DEVICES=-1` set intentionally. |
| Environment | Existing repo Python environment; TensorFlow Probability emitted two deprecation warnings. |
| Random seeds | N/A; deterministic unit/contract tests only. |
| Plan files | `docs/plans/bayesfilter-highdim-zhao-cui-p54-source-faithful-redrift-audit-2026-06-10.md`; `docs/plans/bayesfilter-highdim-zhao-cui-p54-source-faithful-repair-plan-2026-06-10.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p54-source-faithful-redrift-repair-result-2026-06-10.md` |

## Implemented Repairs

1. `bayesfilter/highdim/source_route.py`
   - Added `previous_retained_object_marginalization` to
     `SOURCE_ROUTE_REQUIRED_OPERATION_IDS`.
   - Broadened `SOURCE_ROUTE_FORBIDDEN_DRIFT_MARKERS` with explicit
     retained-grid and all-grid storage markers in addition to pairwise-grid and
     local-neighborhood markers.
2. `tests/highdim/test_p54_source_route_drift_audit.py`
   - Added coverage that the previous retained-object / marginalization
     operation is required.
   - Added pairwise-grid, all-grid, retained-grid-only, and local-neighborhood
     markers to the source-route drift-blocking test.
3. P54 audit and repair-plan artifacts
   - Added a distinct source-operation row for prior or previous retained object
     / marginalization.
   - Added critical findings for the missing marginalization operation and the
     too-narrow drift marker vocabulary.
   - Added close criteria that block completion if pairwise-grid, all-grid, or
     retained-grid-only routes can satisfy source-faithful audit vocabulary.

## Validation

Focused pytest:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p54_source_route_drift_audit.py \
  tests/highdim/test_p49_source_route_sample_proposal.py \
  tests/highdim/test_p49_source_route_recenter_normalizer.py \
  tests/highdim/test_p49_source_route_retained_object.py \
  tests/highdim/test_p49_source_route_preconditioned_predator_prey.py \
  tests/highdim/test_p49_source_route_smoothing_boundary.py \
  tests/highdim/test_p49_gradient_lane_boundary.py \
  tests/highdim/test_public_api_highdim.py
```

Result: `55 passed, 2 warnings in 5.52s`.

Compile check:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p54_source_route_drift_audit.py \
  tests/highdim/test_p49_source_route_sample_proposal.py \
  tests/highdim/test_p49_source_route_recenter_normalizer.py
```

Result: pass.

Static diff check:

```bash
git diff --check -- \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p54_source_route_drift_audit.py \
  tests/highdim/test_p49_source_route_sample_proposal.py \
  tests/highdim/test_p49_source_route_recenter_normalizer.py \
  docs/plans/bayesfilter-highdim-zhao-cui-p54-source-faithful-redrift-audit-2026-06-10.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p54-source-faithful-repair-plan-2026-06-10.md
```

Result: pass.

## Claude Review Loop

| Iteration | Verdict | Action |
| --- | --- | --- |
| 1 | `VERDICT: REVISE` | Claude agreed the previous retained-object / marginalization blocker was resolved, but found pairwise-grid drift was not explicitly tested or documented enough. |
| 2 | `VERDICT: AGREE` | After adding pairwise-grid coverage to tests and docs, Claude accepted the repair. |

## Post-Run Red Team

Strongest alternative explanation: these repairs prevent relabeling drift as
source-faithful progress, but they do not yet implement the missing source
operations.  A later agent could still overclaim if it treats the operation
audit as functional evidence rather than governance evidence.

What would overturn the decision: a reviewed source-code audit showing that
previous retained object marginalization is not a required source-route
operation, or that pairwise/all-grid retained propagation is equivalent to the
source route under the target high-dimensional setting.  Current P48/P49
evidence supports the opposite.

Weakest part of the evidence: no executable source TT/SIRT reapproximation is
available yet, so this result is guardrail completion only.
