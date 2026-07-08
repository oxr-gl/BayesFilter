# Phase 5 Result: Generic Backend Implementation

Date: 2026-07-01

Status: PASSED_TO_PHASE_6_ADAPTER_IMPLEMENTATION

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Advance to Phase 6 actual-SV adapter implementation after bounded Claude result review. |
| Primary criterion status | Met locally: generic factor-propagating SR-UKF backend exists, focused tests pass, static route guard passes the admitted backend, and negative guard tests reject forbidden route families. |
| Veto diagnostic status | No local veto remains.  Claude result review remains required before Phase 6 execution. |
| Main uncertainty | Backend is intentionally Phase-5 narrow: nonnegative covariance-weight branches and one-step generic fixtures only.  Actual-SV adapter correctness and multi-step leaderboard behavior remain Phase 6/7 obligations. |
| Next justified action | Run bounded Claude review of this Phase 5 result, then execute Phase 6 adapter implementation if review agrees. |
| Not concluded | No actual-SV readiness, no leaderboard admission, no HMC/GPU readiness, no exact actual-SV likelihood, and no same-target transformed-likelihood claim. |

## Evidence Contract Outcome

Question:

- Does the generic implementation follow the audited SR-UKF derivation and
  expose analytical score diagnostics?

Outcome:

- Yes for the focused Phase 5 generic backend.  The backend places sigma points
  from a declared factor, propagates explicit map derivatives, computes the
  Gaussian innovation score manually, hands off filtered factor derivatives,
  and reports factor/solve residual diagnostics.

## Code Artifacts

- `bayesfilter/nonlinear/srukf_factor_tf.py`
- `bayesfilter/nonlinear/srukf_route_guard.py`
- `bayesfilter/nonlinear/__init__.py`
- `tests/test_srukf_factor_tf.py`
- Refreshed Phase 6 subplan:
  `docs/plans/bayesfilter-srukf-actual-sv-score-phase6-actual-sv-adapter-implementation-subplan-2026-07-01.md`

## Exact Forbidden-Route Set Preserved

The Phase 5 result and refreshed Phase 6 subplan preserve the exact four-route
forbidden set:

- `GradientTape`
- `tf_svd_sigma_point_filter`
- historical SVD/eigenderivative derivatives
- strict-SPD principal-root derivative helpers

The admitted backend source `bayesfilter/nonlinear/srukf_factor_tf.py` passes
the static route guard.  The guard module and tests necessarily contain the
forbidden tokens so they can reject them.

## Local Checks Run

CPU-only choice:

- Focused unit tests were deliberately run with `CUDA_VISIBLE_DEVICES=-1`.
  These were CPU unit tests and are not GPU/XLA evidence.
- A non-CPU-hidden import check caused TensorFlow CUDA initialization warnings
  inside the sandbox.  This is recorded as sandbox/runtime noise, not GPU health
  evidence.

Commands:

- `python -m py_compile bayesfilter/nonlinear/srukf_factor_tf.py bayesfilter/nonlinear/srukf_route_guard.py`
- `python -m py_compile bayesfilter/nonlinear/srukf_factor_tf.py bayesfilter/nonlinear/srukf_route_guard.py bayesfilter/nonlinear/__init__.py tests/test_srukf_factor_tf.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_srukf_factor_tf.py -q`
- `git diff --check -- bayesfilter/nonlinear/srukf_factor_tf.py bayesfilter/nonlinear/srukf_route_guard.py bayesfilter/nonlinear/__init__.py tests/test_srukf_factor_tf.py`
- `rg` static scan confirming no forbidden route tokens appear in
  `bayesfilter/nonlinear/srukf_factor_tf.py`.

Focused test result:

- `9 passed` in `tests/test_srukf_factor_tf.py`.

Test coverage:

- Closed-form affine Gaussian value and score.
- Same-scalar finite-difference consistency on the fixed branch.
- Factor reconstruction residual diagnostics.
- Filtered-factor derivative residual diagnostics.
- Static route guard on the admitted backend source.
- Negative guard tests for `GradientTape`, `tf_svd_sigma_point_filter`,
  historical SVD/eigenderivative language, and strict-SPD principal-root
  derivative helper language.

## Implementation Boundary

Implemented:

- Generic one-step factor-propagating SR-UKF value/score primitive.
- Nonnegative covariance-weight sigma-point branches for the focused backend
  fixture.
- Explicit map derivative callbacks.
- Manual Gaussian innovation score.
- Filtered mean/factor/covariance derivative handoff.
- Route guard and negative guard tests.

Not implemented:

- Actual-SV adapter wiring.
- Long or batched filtering runner.
- GPU/XLA/HMC benchmark.
- Leaderboard regeneration.
- Exact actual-SV likelihood route.

## Handoff To Phase 6

Phase 6 must map audited actual-SV adapter labels to the new generic backend
API and preserve the exact four-route forbidden set in code, tests, result, and
Phase 7 handoff.  It must not wire the historical value-only diagnostic route
or any autodiff/principal-root/SVD score route into the admitted analytical
score path.
