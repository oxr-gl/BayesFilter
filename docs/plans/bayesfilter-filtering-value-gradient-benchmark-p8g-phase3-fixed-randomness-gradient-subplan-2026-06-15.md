# P8g-G3 Subplan: Fixed-Randomness LEDH Gradient Objective

Date: 2026-06-15

Status: `READY_FOR_G3_AFTER_G2B_REVIEW`

## Phase Objective

Define and validate the no-resampling fixed-randomness LEDH objective needed for
gradient-bearing and diagnostic-HMC work, starting only with the actual scalar
SV row covered by the reviewed G2b graph route.

## Entry Conditions

- G2 vectorized route did not pass speed; do not use it as the serious G3
  entry route.
- G2b scalar-SV graph route passed result review and is cited:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-repair-result-2026-06-15.md`.
- G0 GPU manifest is cited.
- P8e raw-correction/flow-surrogate boundary remains intact.
- G3 initial scope is `zhao_cui_sv_actual_nongaussian_T1000` only. Generalized
  SV and other rows require their own graph route or a reviewed amendment.

## Required Artifacts

- Fixed-randomness seed/salt contract artifact.
- Canonical per-row optimization/HMC coordinate declaration.
- New runner entry point for fixed-randomness gradient checks; it does not exist
  at G3 entry and must be implemented before any gradient-validation command is
  cited as executed.
- G3-specific tests for repeatability, seed/salt contract, canonical-coordinate
  parity, and directional finite-difference checks; the existing value-route
  tests are not sufficient evidence for these claims.
- Gradient validation JSON/CSV/Markdown summary.
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-result-2026-06-15.md`
- refreshed G4 particle-count tuning subplan if G3 passes.

## Required Checks/Tests/Reviews

- Gradient non-None/finite/shape checks.
- Repeatability checks with same fixed randomness.
- CPU/GPU gradient parity in canonical coordinate.
- Directional finite-difference checks in canonical coordinate.
- Common-random-number seed-variation diagnostics.
- Focused pytest additions.
- `git diff --check`
- Claude read-only review.

## Planned Command And Artifact Contract

Repository root: `/home/chakwong/BayesFilter`.

Environment assumptions:

- G2 route identifiers are available and cited;
- the target is fixed-randomness/no-resampling LEDH conditional surrogate only;
- the initial target row is actual scalar SV through route variant
  `p8g_sv_scalar_graph`;
- canonical optimization/HMC coordinate and Jacobian convention are declared
  before gradient promotion.

Exact planned commands. The gradient-check command and the G3-specific tests
are implementation targets for this phase, not entry evidence:

- compile check, non-GPU:
  `python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py`
- gradient-focused CPU tests, deliberate CPU:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py -q -k "p8g or fixed or gradient or ledh"`
- trusted GPU gradient validation entry point, to be implemented or confirmed in
  G3 before use:
  `python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8g-fixed-randomness-gradient-check --rows actual_sv --horizon 50 --particles 32 --seeds 81120,81121,81122,81123,81124 --route-variant p8g_sv_scalar_graph --coordinate canonical_unconstrained --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-2026-06-15.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-2026-06-15.csv`
- formatting check, non-GPU:
  `git diff --check`

If the gradient check entry point or focused tests do not exist, G3 must create
them before any gradient claim, then rerun compile, focused tests, trusted GPU
gradient validation, and `git diff --check`.

Current known missing surfaces at G3 entry:

- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py` does not yet
  expose `--p8g-fixed-randomness-gradient-check`, `--route-variant`, or
  `--coordinate`;
- no reviewed G3-specific assertion yet proves fixed-randomness repeatability,
  seed/salt contract, canonical-coordinate CPU/GPU parity, or directional
  finite-difference behavior for the `p8g_sv_scalar_graph` route.

Phase-local output paths:

- required phase result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-result-2026-06-15.md`;
- gradient JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-2026-06-15.json`;
- gradient CSV:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-2026-06-15.csv`;
- seed/coordinate note:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-contract-2026-06-15.md`.

Approval boundary:

- trusted GPU gradient validation requires explicit approval;
- no stochastic PF marginal gradient, resampling gradient, or HMC chain run is
  authorized in G3.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the fixed-randomness/no-resampling LEDH surrogate objective provide stable, finite, coordinate-consistent gradients? |
| Baseline/comparator | Reviewed G2b scalar-SV graph value path and generic CPU/reference route on short horizons. |
| Primary criterion | Finite stable gradients pass CPU/GPU parity and directional checks in the declared canonical coordinate. |
| Veto diagnostics | Gradient through resampling/transport branch; missing seed/salt contract; parameterization mismatch; finite value treated as gradient correctness; non-finite or unstable gradients. |
| Explanatory diagnostics | Gradient norms, finite-difference residuals, seed-variation spread. |
| Not concluded | Stochastic PF target gradient correctness, production HMC readiness, or final filter ranking. |

## Forbidden Claims/Actions

- Do not call the objective the stochastic PF marginal likelihood.
- Do not promote gradients that only pass in a non-HMC coordinate.
- Do not include resampling gradients in this phase.
- Do not claim generalized-SV, high-dimensional, or generic Algorithm 1
  gradient readiness from the scalar-SV graph route.
- Do not cite the planned G3 gradient command or tests as passing until G3 has
  implemented and rerun them.

## Next-Phase Handoff Conditions

Advance to G4 if value and gradient paths are finite, reproducible, and
coordinate-consistent with artifacts for the actual scalar SV row, and the G4
subplan is refreshed to use only the reviewed gradient route.

## Stop Conditions

- Missing reproducible seed/salt schedule.
- Non-finite or unstable gradient.
- Coordinate transform/Jacobian convention unclear.
