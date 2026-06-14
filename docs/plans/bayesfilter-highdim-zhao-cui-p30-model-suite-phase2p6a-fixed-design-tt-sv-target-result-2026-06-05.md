# P37-M2.6a Result: Fixed-Design TT Fitting For Scalar SV Adjacent Targets

metadata_date: 2026-06-05
phase: P37-M2.6a

## Decision

Decision: `PASS_M2P6A`.

M2.6a adds clean-room fixed-design functional TT target-fitting evidence for
the P30 scalar synthetic stochastic-volatility model.  It validates initial
and transition adjacent square-root targets against dense oracle values using
the reviewed degree-64 fixture and a fresh audit holdout grid.

This is not a sequential TT/SIRT filtering result.

## Evidence Contract Status

| Field | Status |
|---|---|
| Primary criterion | `PASS`; train RMS, audit RMS, and audit relative target errors pass for initial and transition targets |
| Veto diagnostics | `PASS`; no nonfinite values, branch replay mismatch, coordinate-map mismatch, or guardrail regression |
| Main uncertainty | 1D fixed-design TT fitting is only a bridge toward M2.6b/M2.6c |
| Next justified action | M2.6b squared-density normalizer and retained marginalization for fitted adjacent targets |
| What is not concluded | no squared-density normalizer/marginalization, sequential TT/SIRT evidence, adaptive TT-cross reproduction, `T=1000`, SMC, real-data, derivative, HMC, DSGE, GPU, or high-dimensional scalability claim |

## Source-Governance Status

- P30 anchors identified: `eq:p27-sv1`--`eq:p27-sv10`,
  `eq:p25-bridge-1`--`eq:p25-bridge-3`,
  `eq:p24-p22-o3`--`eq:p24-p22-o8`,
  `eq:p33-pullback-leb`--`eq:p33-pullback-nu`,
  `eq:p33-density-with-floor`, `eq:p33-full-normalizer`.
- Zhao--Cui paper anchors identified: stochastic-volatility benchmark,
  functional TT approximation, and squared-density/SIRT construction sections.
- MATLAB behavioral anchors identified: `eg2_sv/mainscript.m`,
  `deep-tensor.dev/src/@TTFun/TTFun.m`,
  `deep-tensor.dev/src/@TTFun/cross.m`,
  `deep-tensor.dev/src/SIRT.m`,
  `deep-tensor.dev/src/@TTSIRT/TTSIRT.m`.
- BayesFilter code/test anchors identified:
  `bayesfilter/highdim/filtering.py`,
  `bayesfilter/highdim/fitting.py`,
  `tests/highdim/test_p30_sv_fixed_design_tt_target.py`.
- Deviations listed: yes.  Fixed-design degree-64 fitting is a
  `BAYESFILTER_EXTENSION`, not MATLAB adaptive cross reproduction.
- Clean-room boundary respected: yes.  MATLAB code was not copied or
  line-translated.
- Unsupported claims removed: yes.
- Reviewer verdict: `PASS_M2P6A_CODE_GOVERNANCE`.

## Files Changed

```text
bayesfilter/highdim/filtering.py
bayesfilter/highdim/__init__.py
tests/highdim/test_p30_sv_fixed_design_tt_target.py
docs/plans/bayesfilter-highdim-zhao-cui-p30-remaining-phases-gated-execution-master-plan-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-subplan-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-claude-review-ledger-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-result-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

## Implemented Behavior

New M2.6a target-building objects:

```text
ScalarAdjacentTargetBuildResult
scalar_nonlinear_initial_adjacent_target_batch
scalar_nonlinear_transition_adjacent_target_batch
```

The builders:

- construct scalar initial and transition SV adjacent targets in reference
  measure coordinates;
- include the coordinate-map Jacobian and reference-density correction;
- use the M2.5 scalar dense retained filter for the transition target;
- record fixture ID, target ID, target kind, coordinate-map payload,
  reference convention, max-log scale shift, retained-filter hash, and
  non-claims;
- produce replayable branch identities for target construction.

New tests:

```text
tests/highdim/test_p30_sv_fixed_design_tt_target.py
```

The tests:

- fit initial and transition square-root adjacent targets with
  `FixedTTFitter`;
- use revised fitting fixture
  `p37.m2p6a.sv.fixed-design-fit.degree64.v2`;
- record failed original fixture
  `p37.m2p6a.sv.fixed-design-fit.degree12.v1`;
- demote the consulted Gauss-Legendre order-121 holdout to tuning evidence;
- promote only on a fresh deterministic 149-point midpoint audit grid;
- verify deterministic target-builder and fitter branch replay;
- reject transition target construction from non-scalar-dense retained filters.

## Fixture Revision

Initial implementation against the reviewed degree-12 fitting fixture failed:

```text
initial train RMS:    0.006158834878663081 > 2e-5
transition train RMS: 0.006376784097517419 > 2e-5
```

A bounded tuning diagnostic over the same target and original holdout showed
degree 64 cleared the target approximation gate.  Claude then blocked reuse of
that holdout for promotion.  The final reviewed correction:

- assigns the degree-64 fit its own fixture ID;
- records the failed degree-12 fixture ID;
- uses the consulted order-121 holdout only as tuning evidence;
- uses a fresh untouched 149-point midpoint audit grid for promotion.

Claude fixture-revision status:

```text
PASS_M2P6A_FIXTURE_REVISION
```

Claude implementation/governance status:

```text
PASS_M2P6A_CODE_GOVERNANCE
```

## Run Manifest

git commit: `N/A dirty/untracked workspace`

environment: `/home/chakwong/anaconda3/envs/tf-gpu`

CPU/GPU status:

```text
deliberate CPU-only tests; CUDA_VISIBLE_DEVICES=-1 set in pytest commands.
```

dtype: `tf.float64`

random seeds:

```text
p37-m2p6a-initial-target
p37-m2p6a-transition-target
p37-m2p6a-retained-t0
p37-m2p6a-initial-fit
p37-m2p6a-transition-fit
p37-m2p6a-transition-replay
```

Focused command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_sv_fixed_design_tt_target.py \
  tests/highdim/test_p30_stochastic_volatility.py \
  tests/highdim/test_p30_model_suite_contracts.py
```

result:

```text
23 passed, 2 warnings in 9.82s
```

Broad highdim guardrail:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py \
  tests/highdim/test_phase0_contracts.py \
  tests/highdim/test_bases.py \
  tests/highdim/test_tt_algebra.py \
  tests/highdim/test_squared_tt_density.py \
  tests/highdim/test_transport.py \
  tests/highdim/test_fixed_branch_fit.py \
  tests/highdim/test_failure_exits.py \
  tests/highdim/test_filtering_kalman_exact.py \
  tests/highdim/test_fixed_branch_derivatives.py \
  tests/highdim/test_scaling_smoke.py \
  tests/highdim/test_public_api_highdim.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/highdim/test_p30_lgssm_exact_reference.py \
  tests/highdim/test_p30_stochastic_volatility.py \
  tests/highdim/test_p30_sv_fixed_design_tt_target.py
```

result:

```text
134 passed, 2 warnings in 11.09s
```

Compile:

```bash
python -m compileall -q bayesfilter/highdim tests/highdim
```

result:

```text
passed
```

Whitespace:

```bash
git diff --check -- bayesfilter/highdim/filtering.py bayesfilter/highdim/__init__.py \
  tests/highdim/test_p30_sv_fixed_design_tt_target.py \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-remaining-phases-gated-execution-master-plan-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-subplan-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-claude-review-ledger-2026-06-05.md
```

result:

```text
passed
```

## Post-Run Red Team

Strongest alternative explanation:

- The result may show that a degree-64 one-dimensional polynomial can fit this
  particular scalar target, not that high-dimensional SV filtering has low TT
  rank.

What would overturn promotion:

- a fresh audit grid or dense oracle detects large target reconstruction error;
- branch replay fails after code review;
- M2.6b fails to turn the fitted target into a correct squared-density
  normalizer and retained marginal.

Weakest evidence:

- M2.6a is target fitting only; it does not yet test normalizer, marginal, or
  sequential evidence recursion.
