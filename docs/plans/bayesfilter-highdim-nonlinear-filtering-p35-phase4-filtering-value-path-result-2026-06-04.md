# P35 Phase 4 Zhao--Cui Highdim Filtering Value Path Result

metadata_date: 2026-06-04

phase: Phase 4 filtering value path

git_commit: `7ccb9c39883471c2d5ec2891cbf33b9ed436bada`

parent_plans:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase4-filtering-value-path-subplan-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md`

## Pre-Implementation Skeptical Audit

status: `PASS_TO_IMPLEMENT_PHASE4_ONLY`

The Phase 4 plan has a valid value-path target if it is restricted to exact
small-model filtering fixtures, deterministic retained-filter contracts, and
explicit measure conventions.  The non-uniform-reference fixture is the highest
risk: it must verify the \(q_z^\nu=q_r(\Psi(z))|\det D\Psi|/\omega(z)\)
conversion explicitly and must not be approximated by a hidden uniform-measure
shortcut.  If this cannot be represented honestly with the current basis and
filtering contracts, Phase 4 must stop before Phase 5.

Wrong-baseline risk: Kalman fixtures are correctness gates for small linear
Gaussian models, not performance or DSGE evidence.

Proxy-metric risk: TT fit residuals are explanatory only; exact Kalman evidence
and retained marginal references are veto gates for Phase 4.

Environment risk: authoritative tests are CPU-only TensorFlow tests with
`CUDA_VISIBLE_DEVICES=-1`; no GPU performance conclusion is made.

## Evidence Contract

scientific_or_engineering_question: Can BayesFilter compute deterministic
fixed-branch filtering value-path objects on exact small models before
derivative or stress phases begin?

exact_baseline_or_comparator:
- pinned scalar one-step LGSSM evidence and posterior mean/variance;
- pinned scalar two-step LGSSM evidence and final filtering marginal;
- pinned two-dimensional LGSSM evidence and final filtering marginal;
- pinned affine/non-uniform reference-measure conversion fixture;
- dense scalar nonlinear quadrature oracle.

primary_pass_criterion:
- focused Phase 4 tests pass;
- full Phase 0--4 CPU-only validation passes;
- retained filters carry measure convention, axes/order, normalizer, and branch
  identity;
- deterministic replay reproduces branch hash, value, and retained marginal.

veto_diagnostics:
- `EXACT_REFERENCE_MISMATCH`;
- `RETAINED_MEASURE_MISMATCH`;
- `RETAINED_AXES_MISMATCH`;
- `RETAINED_STORAGE_BUDGET_EXCEEDED`;
- `NORMALIZER_FLOOR_EXCEEDED`;
- `NONFINITE_VALUE`;
- public API regression;
- forbidden backend/source scan failure;
- Claude Code blocker not resolved after at most five rounds.

explanatory_only_diagnostics:
- TT fit residuals and holdout residuals;
- branch hashes and normalizer diagnostics;
- P10-aligned stage sanity label.

what_will_not_be_concluded:
- analytical derivative correctness;
- adaptive Zhao--Cui TT-cross correctness;
- DSGE readiness;
- large-scale performance;
- public API readiness.

artifact:
- this result ledger;
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase4-filtering-value-path-claude-review-ledger-2026-06-04.md`.

## Preflight Baseline

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_failure_exits.py
```

Outcome: `69 passed, 2 warnings in 5.63s`.

## Implementation Notes

Implemented a Phase 4 exact small-model value gate and retained-filter contract
layer:

- `bayesfilter/highdim/models.py`
  - `TFHighDimStateSpaceModel` protocol.
  - `LinearGaussianSSM` with TensorFlow/TFP float64 log-density methods.
- `bayesfilter/highdim/filtering.py`
  - coordinate-map contracts and identity/affine maps;
  - `FixedBranchFilterConfig`, `RetainedFilter`, `AdjacentTargetBatch`,
    `FixedBranchFilterStepResult`, `FixedBranchFilterResult`;
  - `FixedBranchSquaredTTFilter` exact LGSSM value path;
  - retained Gaussian moment storage with branch identity, measure convention,
    axes/order, storage budget, and normalizer checks;
  - affine non-uniform reference-measure fixture;
  - dense scalar nonlinear quadrature oracle.
- `bayesfilter/highdim/__init__.py`
  - subpackage-only Phase 4 exports.
- `tests/highdim/test_filtering_kalman_exact.py`
  - pinned Phase 4 exact fixtures and replay/failure-exit checks.
- `tests/highdim/test_phase0_contracts.py`
  - backend scan extended to Phase 4 modules.

Claude Code review iter2 blocked the first implementation because it was only
an exact-reference Kalman gate.  The remediation adds an opt-in real
fixed-branch TT artifact lane: when `FixedBranchFilterConfig` includes a
`product_basis` and `FixedTTFitConfig`, each filtering step now builds a sampled
reference-measure target, calls `FixedTTFitter.fit(...)`, constructs a
`SquaredTTDensity`, and stores the real `fit_result`/`density` artifacts in the
step result and retained filter.  The exact Kalman recursion remains the pinned
value oracle for small LGSSM fixtures.

## Commands Run

Focused Phase 4 validation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_kalman_exact.py tests/highdim/test_failure_exits.py
```

First outcome: `19 passed, 2 warnings in 7.14s`.

Post-remediation outcome: `20 passed, 2 warnings in 3.80s`.

Full Phase 0--4 CPU validation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_failure_exits.py tests/highdim/test_filtering_kalman_exact.py
```

First outcome: `80 passed, 2 warnings in 6.92s`.

Post-remediation outcome: `81 passed, 2 warnings in 6.54s`.

Whitespace check:

```bash
git diff --check -- bayesfilter/highdim tests/highdim docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase4-filtering-value-path-result-2026-06-04.md
```

Outcome: passed.

Backend/source scan:

```bash
rg -n "^\s*(import|from)\s+(numpy|jax|torch)\b|matlab|octave|tensor-ssm-paper-demo|zhao_cui_tensor_ssm_p10" bayesfilter/highdim tests/highdim
```

Outcome: no matches.  A broader literal scan matched only the strings inside
`tests/highdim/test_phase0_contracts.py`, where the backend scan itself asserts
that NumPy imports are absent.

## Fixtures Checked

Pinned scalar one-step LGSSM:

- expected log evidence: `-0.980376005178410`;
- expected filter mean: `0.183486238532110`;
- expected filter variance: `0.082568807339450`;
- tolerance used: `2e-10`.
- status: pass.

Pinned scalar two-step LGSSM:

- expected log evidence: `-1.484707421612687`;
- expected final filter mean: `-0.045960935616108`;
- expected final filter variance: `0.068709910778876`;
- tolerance used: `2e-10`.
- status: pass.

Pinned two-dimensional LGSSM:

- expected first increment: `-1.070896331885871`;
- expected total log evidence: `-1.550790276990481`;
- expected final mean: `[0.05354198, -0.14118922]`;
- expected final covariance:
  `[[0.10101319, -0.05495946], [-0.05495946, 0.29692253]]`;
- tolerances used: `2e-10` for log evidence, `1e-8` for moments.
- status: pass.

Pinned affine/non-uniform reference-measure fixture:

- map: `r = 0.5 + 2 z`;
- reference density: `omega(z) = (1 + 0.25 z) / 2`;
- target conversion: `gamma_nu(z) = gamma_r(0.5 + 2z) * 2 / omega(z)`;
- expected truncated log evidence: `-0.980376007510876`;
- expected truncated mean: `0.183486242567321`;
- expected truncated variance: `0.082568800546224`;
- tolerance used: `5e-10`.
- status: pass.

Dense scalar nonlinear oracle:

- model: `x ~ N(0,1)`, `y | x ~ N(x^2, 0.25)`;
- observation: `0.7`;
- diagnostic: Gauss-Legendre quadrature order 128 agrees with order 192 to
  `2e-10`.
- status: pass.

## Required Addendum Fields

files_changed:
- `bayesfilter/highdim/__init__.py`
- `bayesfilter/highdim/filtering.py`
- `bayesfilter/highdim/models.py`
- `tests/highdim/test_filtering_kalman_exact.py`
- `tests/highdim/test_phase0_contracts.py`
- this result ledger

clean_room_inputs:
- P35 Phase 4 subplan;
- P36 Phase 4 addendum;
- local Phase 0--3 highdim contracts.

third_party_code_consulted: none during implementation.

clean_room_attestation: no MATLAB/Octave/P10 source was ported, translated, or
used as an implementation template for Phase 4.

backend_status: TensorFlow/TensorFlow Probability only in `bayesfilter/highdim`
Phase 4 production code; no NumPy/JAX/PyTorch imports.

measure_convention_status: retained filters and adjacent target batches carry
and validate `MeasureConvention`; tests cover retained-measure and retained-axis
mismatch exits.

branch_manifest_status: deterministic branch manifests are generated for
retained filters, steps, and full results; replay test checks stable hashes for
fixed seed/config/observations.

manifest_version:
- `retained_filter_gaussian.v1`
- `fixed_branch_filter_step.v1`
- `fixed_branch_filter_result.v1`

branch_hash: generated deterministically per test fixture; replay test confirms
stable full-result and retained-filter hashes.

replay_tape_hash_when_applicable: N/A; replay tape is a Phase 5 derivative
artifact.

exact_reference_status: pass for pinned scalar, multivariate, affine/reference,
and dense nonlinear oracle fixtures listed above.

tt_artifact_status:
- `tests/highdim/test_filtering_kalman_exact.py` now includes
  `test_one_step_scalar_builds_real_fixed_branch_tt_density_artifacts`.
- The test verifies that a configured Phase 4 step returns a real
  `FixedTTFitResult`, a real `SquaredTTDensity`, an `AdjacentTargetBatch`, and a
  retained filter whose density is the step density.
- Targeted scan after remediation:
  `bayesfilter/highdim/filtering.py:520` calls `FixedTTFitter().fit(...)`;
  `bayesfilter/highdim/filtering.py:549` constructs `SquaredTTDensity(...)`.

exact_reference_metrics: see `Fixtures Checked`.

primary_pass_criterion_status: pass.  Tests pass for exact-reference value
gate, retained-filter contracts, and the remediated real fixed-branch TT density
artifact lane.  Claude iter4 returned `PASS_TO_PHASE5`.

veto_diagnostics_status:
- `EXACT_REFERENCE_MISMATCH`: not triggered;
- `RETAINED_MEASURE_MISMATCH`: deterministic failure exit tested;
- `RETAINED_AXES_MISMATCH`: deterministic failure exit tested;
- `RETAINED_STORAGE_BUDGET_EXCEEDED`: deterministic failure exit tested;
- `NORMALIZER_FLOOR_EXCEEDED`: existing failure-exit test still passes;
- `NONFINITE_VALUE`: existing failure-exit tests still pass;
- public API regression: not triggered;
- forbidden backend/source scan: no anchored matches.

failure_exit_status: pass for retained storage, retained measure, retained axes,
normalizer floor, conditional denominator floor, branch mismatch, complexity
gates, condition-number veto, and measure mismatch.

termination_reason: Phase 4 implementation and internal validation completed;
Claude iter2 blocked the first reference-only implementation; remediation and
internal validation completed; Claude iter4 passed the Phase 4 gate.

stop_condition_triggered: `BLOCKER_BEFORE_PHASE5` in Claude iter2, remediated by
adding per-step fixed-branch TT fitting and squared-TT density artifacts.

decision: `PASS_TO_PHASE5`
