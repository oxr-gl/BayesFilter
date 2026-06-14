# P35 Phase 2 Zhao--Cui Highdim Squared Density And Transport Result

metadata_date: 2026-06-04

phase: Phase 2 squared density and KR transport

git_commit: `7ccb9c39883471c2d5ec2891cbf33b9ed436bada`

parent_plans:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-subplan-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md`

files_changed:
- `bayesfilter/highdim/__init__.py`
- `bayesfilter/highdim/squared_tt.py`
- `bayesfilter/highdim/transport.py`
- `tests/highdim/test_squared_tt_density.py`
- `tests/highdim/test_transport.py`
- `tests/highdim/test_failure_exits.py`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-result-2026-06-04.md`

evidence_contract:
- scientific_or_engineering_question: Can BayesFilter turn an existing
  square-root functional TT into a nonnegative normalized density, compute
  low-dimensional marginals and conditionals under the declared measure, and
  build deterministic grid KR CDF/inverse diagnostics?
- exact_baseline_or_comparator: analytic constant-density identities,
  paired-core mass contraction, dense two-dimensional trapezoid quadrature, and
  uniform-coordinate KR references on `[-1,1]`.
- primary_pass_criterion: Phase 0--2 tests pass under CPU-only TensorFlow with
  exact or stated low-dimensional tolerances.
- veto_diagnostics: `NORMALIZER_FLOOR_EXCEEDED`,
  `CONDITIONAL_DENOMINATOR_FLOOR_EXCEEDED`, `CDF_MONOTONICITY_FAILURE`,
  `INVERSE_BRACKET_FAILURE`, `MEASURE_MISMATCH`, nonfinite values, missing
  branch identity, public API regression, forbidden backend/source references,
  or `git diff --check` failure.
- explanatory_only_diagnostics: TensorFlow Probability deprecation warnings
  and TensorFlow CUDA plugin/init messages emitted despite CPU-hiding.
- what_will_not_be_concluded: This phase does not claim production adaptive KR
  transport accuracy, high-dimensional scaling, TT fitting correctness,
  filtering correctness, fixed-branch derivative correctness, or DSGE
  readiness.
- artifact: this result ledger plus the Phase 2 Claude review ledger.

commands_run:
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_failure_exits.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_failure_exits.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_failure_exits.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_failure_exits.py`
- `git diff --check -- bayesfilter/highdim/__init__.py bayesfilter/highdim/diagnostics.py bayesfilter/highdim/fixed_branch.py bayesfilter/highdim/validation.py bayesfilter/highdim/bases.py bayesfilter/highdim/tt.py bayesfilter/highdim/squared_tt.py bayesfilter/highdim/transport.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_failure_exits.py`
- `rg -n "import numpy|from numpy|import jax|from jax|import torch|from torch|matlab|octave|tensor-ssm-paper-demo|zhao_cui_tensor_ssm_p10" bayesfilter/highdim tests/highdim`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY' ... squared-density branch-hash diagnostic ... PY`
- `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-zhao-cui-phase2-impl-review-iter1 --model sonnet --effort high "<prompt>"`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_failure_exits.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_failure_exits.py`

run_manifest:
- git_commit: `7ccb9c39883471c2d5ec2891cbf33b9ed436bada`
- command_primary: `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_failure_exits.py`
- environment_or_conda_env: `tf-gpu`
- CPU/GPU status: CPU-only validation; `CUDA_VISIBLE_DEVICES=-1`
  intentionally hid GPUs before TensorFlow import for the authoritative Phase 2
  pytest gate.  TensorFlow emitted CUDA plugin/init messages in a branch-hash
  diagnostic; no GPU evidence is claimed.
- data_version: N/A.
- random_seeds: N/A.
- wall_time: `5.49s` for authoritative CPU-only Phase 0--2 pytest validation
  after Claude iteration-2b fixes.
- output_artifact_paths:
  - `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-result-2026-06-04.md`
  - `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-claude-review-ledger-2026-06-04.md`
- plan_file:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-subplan-2026-06-04.md`
- hardening_addendum:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md`
- result_file:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-result-2026-06-04.md`

tests_run:
- `tests/test_v1_public_api.py`
- `tests/highdim/test_phase0_contracts.py`
- `tests/highdim/test_bases.py`
- `tests/highdim/test_tt_algebra.py`
- `tests/highdim/test_squared_tt_density.py`
- `tests/highdim/test_transport.py`
- `tests/highdim/test_failure_exits.py`

test_outcome:
- Initial focused Phase 2 gate: `12 passed, 2 warnings in 3.61s`.
- Initial authoritative Phase 0--2 gate before Claude review:
  `47 passed, 2 warnings in 3.58s`.
- After Claude iteration-1 fixes, focused Phase 2 gate:
  `16 passed, 2 warnings in 7.81s`.
- After Claude iteration-1 fixes, authoritative Phase 0--2 gate:
  `51 passed, 2 warnings in 5.08s`.
- After Claude iteration-2b fixes, focused Phase 2 gate:
  `18 passed, 2 warnings in 5.40s`.
- After Claude iteration-2b fixes, authoritative Phase 0--2 gate:
  `53 passed, 2 warnings in 5.49s`.
- Warnings were TensorFlow Probability deprecation warnings about
  `distutils.version`.

fixtures_checked:
- constant square-root TT normalizes to one;
- paired-core squared normalizer matches dense two-dimensional trapezoid
  quadrature;
- measure-convention mismatch fails;
- defensive reference density rescues a zero square-root TT when `tau > 0`;
- marginal metadata carries contracted branch identity;
- conditional density integrates to one on the declared grid;
- conditional density integrates suffix coordinates by deterministic
  tensor-product trapezoid grids rather than freezing suffix coordinates at
  zero;
- a coupled two-dimensional conditional fixture verifies that suffix
  integration differs from a zero-suffix slice normalization;
- one-dimensional KR CDF/inverse round trip for uniform density;
- separable two-dimensional density gives independent coordinate maps;
- KR log-Jacobian equals the sum of conditional log densities on uniform
  examples;
- inverse bracket failure returns `INVERSE_BRACKET_FAILURE`;
- normalizer floor failure returns `NORMALIZER_FLOOR_EXCEEDED`.
- conditional denominator floor failure returns
  `CONDITIONAL_DENOMINATOR_FLOOR_EXCEEDED`;
- nonfinite density configuration/input paths return `NONFINITE_VALUE`;
- nonfinite transport forward input, inverse input, and CDF point paths return
  `NONFINITE_VALUE`;
- unrelated density branch identity returns `INVALID_BRANCH_MISMATCH`;
- non-natural coordinate order is rejected at transport construction.

tolerances_used:
- exact or `1e-12` tolerance for constant-density identities and normalizers;
- `3e-4` tolerance for dense two-dimensional trapezoid quadrature comparison;
- `2e-3` CDF tolerance and `2e-4` inverse tolerance for grid KR round trip.

clean_room_inputs:
- P35 Phase 2 subplan.
- P36 phase-specific hardened addendum.
- Phase 0--1 highdim contracts.
- Zhao--Cui/Cui--Dolgov equations as reconstructed in the project notes.

third_party_code_consulted:
- `none_for_implementation`

clean_room_attestation:
- No MATLAB, Octave, or third-party audit source was translated, copied, or
  ported.
- Production highdim Phase 2 modules do not import NumPy, JAX, PyTorch,
  MATLAB, or Octave.

backend_status:
- `PASS`
- Phase 2 production code uses TensorFlow tensors and defaults to `tf.float64`.

measure_convention_status:
- `PASS`
- Squared densities require the same measure convention as the square-root TT.
- Product reference density and conditionals use the declared mass measure.

branch_manifest_status:
- `PASS`
- `SquaredTTDensity.manifest_payload()` records square-root TT payload,
  defensive density payload, `tau`, floors, and measure convention.
- `SquaredTTDensity` validates the supplied `BranchIdentity` against the
  density manifest itself.
- Transport objects carry the density object, whose validated branch identity
  is required.

manifest_version:
- `squared_tt_density.v1`

branch_hash:
- Representative constant squared-density hash:
  `3c0b5f07e2aeb0883d0e00a414af1fb273fddf4b084c80feb5869e0bb2809d25`

replay_tape_hash_when_applicable:
- N/A.

exact_reference_status:
- `PASS_FOR_PHASE2_LOW_DIMENSIONAL_FIXTURES`

exact_reference_metrics:
- Constant density normalization exact.
- Paired-core squared normalizer agrees with dense trapezoid reference within
  `3e-4`.
- KR round-trip and Jacobian identities pass on constant/separable examples.

primary_pass_criterion_status:
- `PASS`

veto_diagnostics_status:
- `PASS`
- Public API guard passed.
- Phase 0--1 regression tests passed.
- Backend scan passed.
- `git diff --check` passed.

failure_exit_status:
- `PASS`
- Tests cover `MEASURE_MISMATCH`, `NORMALIZER_FLOOR_EXCEEDED`,
  `CONDITIONAL_DENOMINATOR_FLOOR_EXCEEDED`, `INVERSE_BRACKET_FAILURE`,
  `NONFINITE_VALUE`, and `INVALID_BRANCH_MISMATCH`.

termination_reason:
- `phase2_tests_and_claude_review_passed`

stop_condition_triggered:
- `none`

what_is_not_concluded:
- Phase 2 does not implement TT fitting, sequential filtering, retained-filter
  storage for filtering, fixed-branch derivative replay, high-dimensional
  performance validation, adaptive Zhao--Cui differentiability, or DSGE
  applications.
- Grid KR routines are deterministic low-dimensional diagnostics, not final
  production transport accuracy evidence.

decision:
- `PASS`
