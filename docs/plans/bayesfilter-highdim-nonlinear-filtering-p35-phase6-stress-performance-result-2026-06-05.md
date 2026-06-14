# P35 Phase 6 Result: Stress Models And Performance Ladder

metadata_date: 2026-06-05
phase: Phase 6 stress models and performance ladder
git_commit: 7ccb9c3

## Skeptical Plan Audit

Status: PASS_TO_EXECUTION.

The Phase 6 plan is valid only if it remains a bounded stress-smoke phase, not
a production scalability claim. The main audit risks are:

- wrong baseline: a TT artifact smoke cannot replace exact LGSSM references;
- proxy metric inflation: wall time and finite residuals cannot prove
  correctness;
- stale context: Phase 5 explicitly forbids claiming an end-to-end
  `FixedBranchSquaredTTFilter.score(...)` API;
- hidden environment mismatch: GPU use requires trusted execution, so this
  phase starts as deliberate CPU-only validation;
- artifact mismatch: a stress run without resource fields, replay status, and
  failure classification would not answer the Phase 6 question.

Resolution: execute only deterministic CPU smoke tests over validated internals.
Use exact LGSSM log-likelihood references where available; use scalar
TT-artifact replay as diagnostic evidence for fitting/squared-density branch
stability; record all resource and replay fields in a manifest. Do not claim
DSGE readiness, HMC readiness, GPU readiness, or score API readiness.

## Evidence Contract

Question: after Phase 0--5 value and derivative gates passed, can the
fixed-branch squared-TT implementation run a small Zhao--Cui-style stress smoke
with finite diagnostics, exact LGSSM references, resource budgets, replay
stability, and explicit failure classification?

Baseline/comparator:
- exact Kalman LGSSM log likelihood and retained moments for tiny dimensions;
- deterministic repeated run of the same fixed branch for replay stability.

Primary pass criteria:
- focused Phase 6 smoke tests pass;
- Phase 0--5 test suite remains green;
- each manifest includes resource budget, replay status, wall time,
  exact-reference status, branch hash, decision status, termination reason, and
  what is not concluded;
- failures classify separately as implementation, tuning, approximation,
  resource, or numerical-veto failures.

Veto diagnostics:
- any nonfinite log likelihood, fit residual, holdout residual, normalizer, or
  exact-reference error;
- missing branch hash or failed deterministic replay on selected smoke
  configurations;
- memory/resource budget missing from the manifest;
- Phase 0--5 regression;
- forbidden production backend/source reference in highdim code.

Explanatory-only diagnostics:
- wall time;
- small-grid rank/degree/horizon timing;
- fit residual magnitude in the scalar TT-artifact smoke;
- branch hash values themselves.

What will not be concluded:
- no DSGE readiness;
- no HMC readiness;
- no GPU production readiness;
- no adaptive Zhao--Cui derivative correctness;
- no end-to-end score API readiness;
- no claim that the small smoke establishes large-scale scalability.

Planned artifact:
- this result ledger;
- `tests/highdim/test_scaling_smoke.py`;
- Claude review ledger
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase6-stress-performance-claude-review-ledger-2026-06-05.md`.

## Run Manifest

command:
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_scaling_smoke.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_failure_exits.py tests/highdim/test_filtering_kalman_exact.py tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_scaling_smoke.py`
- `git diff --check`
- `rg -n "^\s*(import|from)\s+(numpy|jax|torch)\b|matlab|octave|tensor-ssm-paper-demo|zhao_cui_tensor_ssm_p10" bayesfilter/highdim tests/highdim`
environment: `/home/chakwong/anaconda3/envs/tf-gpu`, deliberate CPU-only pytest smoke
CPU/GPU status: CPU-only; `CUDA_VISIBLE_DEVICES=-1` set before TensorFlow import
random seeds: deterministic string branch seeds in tests
dtype: `tf.float64`
model equations:
- LGSSM:
  `x0 ~ N(m0,P0)`,
  `x_t = A x_{t-1} + b + eta_t`,
  `eta_t ~ N(0,Q)`,
  `y_t = H x_t + c + eps_t`,
  `eps_t ~ N(0,R)`.
dimension/rank/degree/horizon grid:
- exact LGSSM smoke: `state_dim in {1,2}`, `horizon in {1,2,3}`;
- scalar TT-artifact smoke: `rank=(1,1)`, `max_degree=4`,
  `horizon=2`.
row/column/normal-matrix budgets:
- exact LGSSM smoke with no TT artifacts: row/column/design/normal budgets `0`
  in the manifest because no dense TT design matrix is materialized;
- scalar TT-artifact smoke: `row_budget=256`, `column_budget=32`,
  `dense_matrix_byte_budget=100000`, `normal_matrix_byte_budget=10000`,
  `retained_storage_byte_budget=10000000`.
expected memory model: dense design and normal-matrix bytes from fit config
measured peak memory: not available in pytest smoke
wall time: recorded inside each runtime manifest object, not persisted outside pytest
exact-reference error:
- exact LGSSM smoke asserts `< 2e-12` for `state_dim in {1,2}`,
  `horizon in {1,2,3}`;
- scalar TT-artifact smoke compares the value path with the independent Kalman
  recurrence.
fit and holdout residuals:
- exact LGSSM smoke has no TT fit residual;
- scalar TT-artifact smoke asserts `max(fit_residuals) < 5e-2`;
- holdout residuals are `None` because this is a deterministic smoke, not a
  heldout accuracy ladder.
normalizer and CDF diagnostics:
- retained normalizers are finite in exact LGSSM smoke;
- scalar TT density normalizers are positive.
branch hash: nonempty result branch hash required by `StressRunManifest`
deterministic replay status: `PASS` required by `StressRunManifest`
decision status:
- `PASS_EXACT_REFERENCE` for exact/tiny smoke manifests;
- failure classifier tests cover resource, tuning, approximation, numerical
  veto, implementation, and phase-regression blocking statuses.
termination_reason: `finite_exact_reference_smoke`
stop_condition_triggered: `none`

## Clean-Room And Backend Attestation

clean_room_inputs:
- P35 Phase 6 subplan;
- P36 Phase 6 hardened addendum;
- Phase 0--5 implementation artifacts already accepted by Claude review.

third_party_code_consulted: none during this phase execution.
clean_room_attestation: Phase 6 tests and validation containers are written from
the project mathematical contract and existing BayesFilter highdim APIs.
backend_status: TensorFlow/TensorFlow Probability only for production highdim
code; no NumPy/JAX/PyTorch/MATLAB/Octave production backend.

## Results

Files changed:
- `bayesfilter/highdim/validation.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_scaling_smoke.py`
- this result ledger

Validation:
- Phase 6 focused smoke: `5 passed, 2 warnings in 5.46s`.
- Phase 0--6 CPU suite plus public API guardrail:
  `103 passed, 2 warnings in 5.99s`.
- `git diff --check`: pass, no output.
- forbidden backend/source scan over `bayesfilter/highdim tests/highdim`: pass,
  no matches.

Primary pass criterion status: PASS.

Veto diagnostics status:
- no nonfinite values observed in the smoke manifests;
- deterministic replay status is required to be `PASS`;
- stress manifest construction rejects missing resource/replay fields;
- Phase 0--5 gates did not regress;
- forbidden backend/source scan passed.

Failure exit status:
- `BLOCKED_BY_PHASE_REGRESSION` tested;
- `FAIL_RESOURCE`, `FAIL_TUNING`, `FAIL_APPROXIMATION`,
  `FAIL_NUMERICAL_VETO`, and `FAIL_IMPLEMENTATION` classification tested.

Termination reason: finite exact-reference and TT-artifact replay smoke passed.
Stop condition triggered: none.

Decision: PASS_TO_CLAUDE_REVIEW. Phase 6 has enough bounded evidence to support
the next reviewed implementation phase. It does not support DSGE trials,
GPU claims, HMC claims, adaptive-branch derivative claims, or score API claims.
