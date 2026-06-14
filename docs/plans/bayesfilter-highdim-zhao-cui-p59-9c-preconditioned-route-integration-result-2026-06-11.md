# P59-9c Result: Preconditioned Route Integration

metadata_date: 2026-06-11
status: PASS_P59_9C_PRECONDITIONED_ROUTE_INTEGRATION

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Does the author Austria SIR Phase-9 row use the full source route or the preconditioned route, and can later phases fail closed on that decision? |
| Baseline/comparator | Zhao-Cui `eg3_sir/mainscript.m`, `models/full_sol.m`, `models/pre_sol.m`, `models/tensordot/precond.m`, P57-M8 preconditioned surface, and P59 master ordering. |
| Primary criterion | Emit an executable source-cited route-decision artifact before P59-9b and P59-9d. |
| Veto diagnostics | Missing source files, `eg3_sir/mainscript.m` not selecting `full_sol`, contradictory `pre_sol` selection for this row, unverified `full_sol`/`pre_sol`/`precond` boundaries, UKF as route substitute, or P57-M8 algebra promoted when the row does not select `pre_sol`. |
| Explanatory diagnostics | Source-substring checks, route manifest, fail-closed missing-source tests, contradictory-source tests, focused CPU-only pytest. |
| Not concluded | No Phase-9 validation launch, no d=18 filtering accuracy, no same-route rank convergence, no d=50/d=100 scaling, no HMC production readiness, no adaptive Zhao-Cui parity. |

## Source Anchors Checked

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:53-56`
  constructs `full_sol(myModel, sqr, poly2, opt, lowopt, N, 4)` and solves it.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:9-18`
  constructs the full route and allocates `model.d + 2*model.m` samples.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-38`
  pushes samples, augments `[theta, x_t, x_{t-1}]`, fits the full-route SIRT,
  samples through `eval_irt`, and corrects with `eval_pdf`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m:1-10`
  is a separate subclass route with a `precond` object.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/tensordot/precond.m:43-56`
  defines the linear preconditioner boundary used only when a row selects the
  preconditioned route.

## Implementation

Changed code:

- `bayesfilter/highdim/source_route.py`
  - Added P59-9c status and route-decision constants.
  - Added `P59AuthorSIRRouteDecisionResult`.
  - Added `p59_author_sir_route_decision(...)`, which reads the local author
    MATLAB source files and fails closed when source evidence is missing or
    contradictory.
  - Added `_p59_9c_block_result(...)`.
- `bayesfilter/highdim/__init__.py`
  - Exported the P59-9c constants, result class, and helper.
- `tests/highdim/test_p59_author_sir_route_decision.py`
  - Added tests for source-selected `full_sol`, fail-closed downstream gating,
    missing-source blocking, contradictory-source blocking, and incoherent
    result-payload rejection.

## Artifact Manifest

Key emitted values from `p59_author_sir_route_decision()`:

| Field | Value |
| --- | --- |
| Status | `PASS_P59_9C_PRECONDITIONED_ROUTE_INTEGRATION` |
| Target id | `zhao_cui_sir_austria_d18` |
| Route decision | `full_route_selected` |
| Source-selected MATLAB constructor | `full_sol` |
| Preconditioned route required | `False` |
| Preconditioned route status | `not_required_author_sir_mainscript_selects_full_sol` |
| Unlocks after consumed by | `P59-9b`, `P59-9d` |

Source evidence flags:

```text
mainscript_selects_full_sol: True
mainscript_selects_pre_sol: False
full_sol_source_boundary_verified: True
pre_sol_boundary_verified: True
precond_boundary_verified: True
```

## Commands Run

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_route_decision.py tests/highdim/test_p59_author_sir_36d_target_fit.py tests/highdim/test_p58_m9_source_route_pipeline_readiness.py tests/highdim/test_p57_m8_preconditioned_algorithm5.py
```

Result: `19 passed, 2 warnings`.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p59_author_sir_route_decision.py
```

Result: passed.

```text
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p59_author_sir_route_decision.py
```

Result: passed.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -c '... p59_author_sir_route_decision() ...'
```

Result: emitted the manifest values above. TensorFlow printed CUDA plugin import
warnings even with `CUDA_VISIBLE_DEVICES=-1`; this was not a GPU run and is not
used as GPU evidence.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| Working tree | Dirty before and after; P59 changes are local/uncommitted and unrelated prior artifacts remain present. |
| Python | `Python 3.11.14` |
| CPU/GPU status | CPU-only intended via `CUDA_VISIBLE_DEVICES=-1`; no GPU benchmark or GPU initialization claim. |
| Seeds | N/A; no stochastic run. |
| Wall time | Focused tests completed in under 10 seconds. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9c-preconditioned-route-integration-subplan-2026-06-11.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9c-preconditioned-route-integration-result-2026-06-11.md` |

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass P59-9c route decision. | Met: source-cited artifact selects `full_route_selected` for author SIR and exposes fail-closed gating for P59-9b/P59-9d. | No missing source, contradictory route evidence, UKF substitution, or preconditioned-route overclaim in tests/artifact. | This is a route gate only; it does not assemble step specs or run validation. | Execute P59-9b: source-route step-spec assembly, consuming this route-decision artifact first. | No d=18 filtering accuracy, no rank convergence, no paper-scale validation. |

## Token

`PASS_P59_9C_PRECONDITIONED_ROUTE_INTEGRATION`
