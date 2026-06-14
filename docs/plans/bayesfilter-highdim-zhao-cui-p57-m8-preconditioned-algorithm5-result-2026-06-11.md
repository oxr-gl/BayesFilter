# P57-M8 Result: Preconditioned Algorithm 5 Route

metadata_date: 2026-06-11
status: PASS_P57_M8_PRECONDITIONED_ALGORITHM5

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can BayesFilter implement the paper/source preconditioned route surface needed before spatial SIR validation? |
| Baseline/comparator | Zhao-Cui author `pre_sol.m:187-255` and `models/tensordot/precond.m:43-56`. |
| Primary pass criterion | Fixed-HMC source-surface code preserves the author linear preconditioner construction, `Tu2x`/`Tx2u` maps, residual/proposal density composition, and proposal correction algebra. |
| Veto diagnostics | No unanchored local/operator substitute was promoted; no UKF/rank proxy was promoted; no spatial SIR success was claimed from the preconditioned surface test. |
| Not concluded | This does not certify TT/SIRT fitting quality, d=18 spatial SIR success, d=50/d=100 scaling, HMC readiness, adaptive parity, smoothing, or S&P 500 reproduction. |

## Skeptical Audit

Status: `PASS`.

- Wrong-baseline risk checked: M8 uses the author preconditioned-route source
  anchors, not the earlier P49 target-identity-only helper.
- Proxy-risk checked: the analytic tests prove source algebra and shape
  contracts only; they do not promote to spatial SIR correctness.
- Missing-stop risk checked: the phase did not stop at map scaffolding; it also
  added the author linear preconditioner and proposal-correction helper.
- Artifact-risk checked: this result emits the required M8 token and preserves
  source anchors and nonclaims.

## Source Anchors Reopened

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m:187-213`
  for preconditioner SIRT setup and `Tu2x`/`Tx2u`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m:222-255`
  for residual target fitting, residual sampling, full target evaluation, and
  proposal correction.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/tensordot/precond.m:43-56`
  for the linear preconditioner matrix `C` and diagonal `Sigmak`.

## Implementation

Changed code:

- `bayesfilter/highdim/source_route.py`
  - Added `SourceRouteLinearPreconditionerResult`.
  - Added `source_route_linear_preconditioner_from_covariances(...)` as a
    TensorFlow transcription of author `precond.m:43-56`.
  - Added `SourceRoutePreconditionedMap` with source map labels `Tu2x` and
    `Tx2u`.
  - Added `SourceRoutePreconditionedProposalResult`.
  - Added `source_route_preconditioned_proposal_correction(...)`, enforcing
    the author density identity:
    `proposal = residual_log_density + preconditioner_log_density -
    reference_log_density`, `target = -full_negative_log_density`, and
    `correction = target - proposal`.
- `bayesfilter/highdim/__init__.py`
  - Exported the M8 source-route preconditioner/map/proposal symbols.
- `tests/highdim/test_p57_m8_preconditioned_algorithm5.py`
  - Added focused source-surface tests for linear preconditioner invariants,
    `Tu2x`/`Tx2u` roundtrip, proposal-correction algebra, and shape/route
    rejection.

## Commands Run

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m8_preconditioned_algorithm5.py tests/highdim/test_p49_source_route_preconditioned_predator_prey.py tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py
```

Result:

```text
14 passed, 2 warnings
```

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m8_preconditioned_algorithm5.py
```

Result: passed.

```text
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m8_preconditioned_algorithm5.py
```

Result: passed.

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass M8 pending Claude read-only review. | Met for the fixed-HMC Algorithm 5 source surface: linear preconditioner, maps, and proposal correction are implemented and tested. | No route drift, proxy promotion, or unearned spatial SIR claim observed. | Full d=18 spatial SIR still needs the M9 validation ladder with source-route comparator evidence. | Advance to M9 after Claude review agrees. | No paper-scale filtering success, rank success, or HMC readiness. |

## Token

`PASS_P57_M8_PRECONDITIONED_ALGORITHM5`
