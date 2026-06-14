# P35 Phase 1 Zhao--Cui Highdim Basis And TT Algebra Result

metadata_date: 2026-06-04

phase: Phase 1 basis, mass, and TT algebra

git_commit: `7ccb9c39883471c2d5ec2891cbf33b9ed436bada`

parent_plans:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-subplan-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Gorodetsky, Karaman, and Marzouk, "A Continuous Analogue of the
  Tensor-Train Decomposition," Computer Methods in Applied Mechanics and
  Engineering, 2019.

files_changed:
- `bayesfilter/highdim/__init__.py`
- `bayesfilter/highdim/bases.py`
- `bayesfilter/highdim/tt.py`
- `tests/highdim/test_bases.py`
- `tests/highdim/test_tt_algebra.py`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-result-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-claude-review-ledger-2026-06-04.md`

commands_run:
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py`
- `git diff --check -- bayesfilter/highdim/__init__.py bayesfilter/highdim/diagnostics.py bayesfilter/highdim/fixed_branch.py bayesfilter/highdim/validation.py bayesfilter/highdim/bases.py bayesfilter/highdim/tt.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py`
- `rg -n "import numpy|from numpy|import jax|from jax|import torch|from torch|matlab|octave|tensor-ssm-paper-demo|zhao_cui_tensor_ssm_p10" bayesfilter/highdim tests/highdim`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY' ... branch-hash diagnostic ... PY`
- `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-zhao-cui-phase1-impl-review-iter1 --model sonnet --effort high "<prompt>"`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_tt_algebra.py tests/highdim/test_bases.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_tt_algebra.py tests/highdim/test_bases.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py`

run_manifest:
- git_commit: `7ccb9c39883471c2d5ec2891cbf33b9ed436bada`
- command_primary: `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py`
- command_secondary:
  - `git diff --check -- bayesfilter/highdim/__init__.py bayesfilter/highdim/diagnostics.py bayesfilter/highdim/fixed_branch.py bayesfilter/highdim/validation.py bayesfilter/highdim/bases.py bayesfilter/highdim/tt.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py`
  - `rg -n "import numpy|from numpy|import jax|from jax|import torch|from torch|matlab|octave|tensor-ssm-paper-demo|zhao_cui_tensor_ssm_p10" bayesfilter/highdim tests/highdim`
- environment_or_conda_env: `tf-gpu`
- CPU/GPU status: CPU-only validation; `CUDA_VISIBLE_DEVICES=-1`
  intentionally hid GPUs before TensorFlow import for the authoritative Phase 1
  pytest gate.  TensorFlow still emitted CUDA plugin/init messages in one
  branch-hash diagnostic; no GPU correctness or availability evidence is
  claimed from Phase 1.
- data_version: N/A.
- random_seeds: N/A.
- wall_time: `3.29s` for authoritative CPU-only pytest validation after the
  Claude iteration-2 fixes.
- output_artifact_paths:
  - `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-result-2026-06-04.md`
  - `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-claude-review-ledger-2026-06-04.md`
- plan_file:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-subplan-2026-06-04.md`
- hardening_addendum:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md`
- result_file:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-result-2026-06-04.md`

tests_run:
- `tests/test_v1_public_api.py`
- `tests/highdim/test_phase0_contracts.py`
- `tests/highdim/test_bases.py`
- `tests/highdim/test_tt_algebra.py`

test_outcome:
- Initial local gate before Claude review: `29 passed, 2 warnings in 2.98s`.
- After Claude iteration-1 fixes, local gate:
  `33 passed, 2 warnings in 3.55s`.
- After Claude iteration-2 fixes, authoritative local gate:
  `35 passed, 2 warnings in 3.29s`.
- Warnings were TensorFlow Probability deprecation warnings about
  `distutils.version`; they are unrelated to Phase 1 highdim contracts.

fixtures_checked:
- normalized Legendre basis dimension;
- normalized reference-measure mass matrix identity for degrees 0--5;
- reference-Lebesgue mass matrix interval-length factor;
- reference-measure integral vector for the constant basis;
- Legendre derivative recurrence against centered finite differences;
- mixed density/mass convention rejection;
- invalid bounded interval and invalid degree rejection;
- product-basis axis evaluation shape;
- rank-one separable TT evaluation;
- low-rank bivariate TT evaluation;
- trivariate TT rank, basis shape, and exact integral;
- declared mass measure use in `integrate_all`;
- rejection of a `FunctionalTT` whose measure convention differs from its
  `ProductBasis` convention;
- true integrated-axis contraction into retained TT cores;
- full-axis contraction as an explicit scalar contracted representation with no
  fake retained core;
- contracted-representation branch identity over contracted payload;
- retained-basis metadata sensitivity in contracted-representation branch
  identity;
- branch manifest hash sensitivity to core values and basis-domain fields;
- complexity gate status before dense allocation;
- complexity gate enforcement on `evaluate`, `integrate_all`, and
  `contract_axes`.
- contraction-complexity estimates accounting for retained-rank growth after
  integrated axes.

tolerances_used:
- exact equality for analytically constructed mass and integral tensors;
- `1e-5` absolute tolerance for finite-difference derivative checks with
  centered step `1e-6`;
- `1e-12` absolute tolerance for TT evaluation, integration, and contraction
  examples.

clean_room_inputs:
- P35 Phase 1 subplan.
- P36 phase-specific hardened addendum.
- Existing Phase 0 highdim contracts.
- Existing BayesFilter TensorFlow style.
- Standard Legendre recurrence and tensor-train contraction equations from the
  project mathematical notes.

third_party_code_consulted:
- `none_for_implementation`

clean_room_attestation:
- No MATLAB, Octave, or third-party audit source was translated, copied, or
  ported.
- `third_party/audit/tensor-ssm-paper-demo/**` and
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/**` were not used for
  class layouts, helper names, comments, or implementation details.
- Production highdim Phase 1 modules do not import NumPy, JAX, PyTorch,
  MATLAB, or Octave.

backend_status:
- `PASS`
- Phase 1 production code uses TensorFlow tensors and defaults to `tf.float64`.
- The focused forbidden-backend scan found no NumPy/JAX/PyTorch/MATLAB/Octave
  imports or forbidden third-party source references in production highdim
  code.  It only found the Phase 0 test that asserts NumPy is not imported.

measure_convention_status:
- `PASS`
- `ProductBasis` requires a `MeasureConvention`.
- Mixed reference-measure density and reference-Lebesgue mass are rejected.
- Pinned normalized Legendre convention:
  `psi_n(x)=sqrt(2n+1) P_n(2(x-a)/(b-a)-1)`.
- Under uniform reference probability measure `dnu=dx/(b-a)`, the mass matrix
  is identity and the constant-basis integral is one.
- Under reference Lebesgue measure, the mass matrix and integral vector carry
  the interval-length factor.

branch_manifest_status:
- `PASS`
- `FunctionalTT.manifest_payload()` records rank tuple, basis dimensions,
- complexity budget, measure convention fields, basis family/domain/dtype/
  reference-measure/degree/normalization, and all core tensors.
- `TTContractedRepresentation.manifest_payload()` records kept axes,
  integrated axes, measure convention, retained basis family/domain/dtype/
  reference-measure/degree/normalization, retained cores, scalar contracted
  value when applicable, and contraction diagnostics.
- Hash tests verify sensitivity to core values and basis-domain fields.

manifest_version:
- `functional_tt.v1`

branch_hash:
- Representative one-core constant TT hash:
  `49cdae87ca27e8b6536694dae1c1eea5f67f88ac3a4bb0f14089afd2c745a037`

replay_tape_hash_when_applicable:
- N/A.

exact_reference_status:
- `PASS_FOR_PHASE1_EXACT_FIXTURES`

exact_reference_metrics:
- Legendre mass and integral exact-construction tests passed.
- TT evaluation and integration low-dimensional exact examples passed within
  pinned tolerances.
- Derivative finite-difference test passed at `1e-5` absolute tolerance.

primary_pass_criterion_status:
- `PASS`
- Phase 1 now represents bounded normalized Legendre bases, reference mass and
  integral vectors, fixed-rank functional TT evaluation, full integration,
  integrated-axis contraction, scalar full contraction, manifest payloads, and
  enforced pre-allocation complexity status on dense Phase 1 paths.

veto_diagnostics_status:
- `PASS`
- Public API guard passed; no top-level `bayesfilter` API exposure was added.
- Phase 0 regression tests passed.
- Backend scan passed.
- `git diff --check` passed for Phase 0/1 scoped files.
- Complexity budget failure returns `COMPLEXITY_GATE` and dense paths raise
  before work when the declared budget is exceeded.
- The contraction gate simulates the actual pending-rank flow used by
  `contract_axes()` and rejects retained-rank growth before constructing the
  retained cores.

failure_exit_status:
- `PASS`
- Tests cover `MEASURE_MISMATCH`, `INVALID_SHAPE`, `COMPLEXITY_GATE`, and
  Phase 0 failure exits that remain inherited gates for Phase 1.

termination_reason:
- `phase1_tests_and_claude_review_passed`

stop_condition_triggered:
- `none`

what_is_not_concluded:
- Phase 1 does not implement squared TT densities, normalizers for squared
  density objects, KR transport, TT fitting, sequential filtering, fixed-branch
  replay, derivatives, finite-difference gradient diagnostics, performance
  stress tests, DSGE applications, or public API exposure.
- Phase 1 exact fixtures do not certify Zhao--Cui production numerical
  accuracy.
- Phase 1 does not claim adaptive Zhao--Cui differentiability.

decision:
- `PASS`

next_step_if_review_passes:
- Begin Phase 2 only after Codex performs the Phase 2 skeptical plan audit and
  records the Phase 2 evidence contract.
