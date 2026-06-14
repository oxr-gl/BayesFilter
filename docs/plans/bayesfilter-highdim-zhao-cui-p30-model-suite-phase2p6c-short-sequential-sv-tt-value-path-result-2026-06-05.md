# P37-M2.6c Result: Short Sequential Scalar SV TT Value Path

metadata_date: 2026-06-06
phase: P37-M2.6c

## Decision

Decision: `PASS_M2P6C`.

M2.6c adds a TT-only two-observation scalar stochastic-volatility value path.
It composes the M2.6a fixed-design adjacent-target fitting and M2.6b
squared-density normalizer/retained-density helper, then compares per-step log
normalizers, total log evidence, retained means, and retained variances against
the pinned dense scalar M2/M2.5 oracle.

This is not paper-scale Zhao--Cui reproduction.

## Source-Governance Status

- P30 anchors identified: `eq:p27-sv1`--`eq:p27-sv10`,
  `eq:p25-bridge-1`--`eq:p25-bridge-3`, `eq:p33-square-mass`,
  `eq:p33-full-normalizer`, `eq:p33-retained-marginal`, and
  `eq:p33-retained-normalized`.
- Zhao--Cui paper anchors identified: SSM equations (1)--(3), filtering and
  posterior marginals (5)--(8), recursive update (9)--(11), Algorithm 1(a),
  Eq. (12), Algorithm 1(b), Algorithm 1(c), Eq. (13), Lemma 1, Proposition 2,
  Eq. (14), and Algorithm 2.
- MATLAB behavioral anchors identified: `eg2_sv/mainscript.m`,
  `deep-tensor.dev/src/SIRT.m`, `deep-tensor.dev/src/@TTSIRT/TTSIRT.m`, and
  `deep-tensor.dev/src/@TTFun/cross.m`.
- BayesFilter code/test anchors identified:
  `bayesfilter/highdim/filtering.py`,
  `bayesfilter/highdim/fitting.py`,
  `bayesfilter/highdim/squared_tt.py`,
  `bayesfilter/highdim/__init__.py`,
  `tests/highdim/test_p30_sv_short_sequential_tt_value_path.py`,
  `tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py`, and
  `tests/highdim/test_p30_stochastic_volatility.py`.
- Deviations listed: yes.  This is a fixed-design scalar BayesFilter extension
  with a pinned two-observation horizon, not MATLAB adaptive cross.
- Clean-room boundary respected: yes.  MATLAB code was not copied or
  line-translated.
- Unsupported claims removed: yes.
- Reviewer verdict: `PASS_M2P6C_CODE_GOVERNANCE`.

## Evidence Contract Status

| Field | Status |
|---|---|
| Primary criterion | `PASS_LOCAL`; per-step log normalizers, total log evidence, retained means, and retained variances pass against the dense GL321 comparator under reviewed M2.6c tolerances |
| Veto diagnostics | `PASS_LOCAL`; no nonfinite values, missing TT artifacts, dense-route promotion, missing density hash, replay mismatch, fixture drift, or guardrail regression observed |
| Explanatory diagnostics | chunked retained-density evaluation used to respect existing fitted-TT complexity budgets on GL257/GL321 retained grids |
| Main uncertainty | scalar two-observation evidence only; longer horizons and higher dimensions remain unvalidated |
| Next justified action | M2.6d SV TT lane closeout |
| What is not concluded | no adaptive TT-cross/MATLAB reproduction, paper-scale `T=1000`, SMC or real-data validation, derivative/HMC/DSGE/GPU readiness, or high-dimensional scalability claim |

## Implemented Behavior

New M2.6c entry point:

```text
scalar_nonlinear_fixed_design_tt_value_path(...)
```

The entry point:

- requires a nonlinear scalar model, exactly two observations, non-null
  `fit_config`, and non-null `product_basis`;
- leaves `FixedBranchSquaredTTFilter.log_likelihood()` unchanged for nonlinear
  scalar models, so the existing method still dispatches to the dense value
  path and rejects TT artifact requests;
- builds the initial adjacent target, fits a fixed-design square-root TT,
  constructs a `SquaredTTDensity`, and computes
  `log(density.normalizer()) + target.log_scale_shift`;
- builds a TT-generated retained grid with `storage_kind = scalar_tt_grid` and
  a required density hash;
- builds the transition adjacent target from the TT-generated retained grid,
  not from the dense M2.5 retained filter;
- dispatches `scalar_tt_grid` transition propagation through a TT-specific
  helper that validates the retained density object and density-hash replay
  before using the retained grid fields;
- records target, fit, density, retained-filter, and step branch hashes.

New retained-grid constructor:

```text
scalar_tt_grid_retained_filter(...)
```

This constructor records the physical/reference grid, raw propagation weights,
reconstructed physical log density, retained moments, and required density
hash.  Transition target construction accepts `scalar_tt_grid` only when the
density hash is present.

New tests:

```text
tests/highdim/test_p30_sv_short_sequential_tt_value_path.py
```

The tests:

- use fixture `p37.m2p6c.sv.short-sequential-tt-value-path.v1`;
- use dense comparator `p37.m2p6c.sv.dense-sequential-comparator.gl321.v1`;
- use retained-moment grid `p37.m2p6c.sv.tt-retained-moment.gl257.v1`;
- use retained-propagation grid `p37.m2p6c.sv.tt-retained-propagation.gl321.v1`;
- assert every promoted step has non-null fitted TT and density artifacts;
- assert every promoted step uses
  `value_path = scalar_nonlinear_fixed_design_tt_value_path`;
- assert the old `FixedBranchSquaredTTFilter.log_likelihood()` nonlinear
  scalar dispatcher still rejects TT artifact requests rather than silently
  promoting the dense path;
- monkeypatch the dense retained propagation helper to fail and verify the
  TT path still runs through the TT-specific propagation helper;
- assert deterministic replay of result, step, and retained-filter hashes.

## Failure And Repair Log

### Focused Attempt 1

result:

```text
6 failed, 11 passed, 2 warnings in 9.51s
```

Blocker classification:

```text
fixable implementation bug with unchanged mathematical/evidence contract.
```

Observed issue:

- `_coordinate_map_for_config` was called from the new TT path and dense-path
  refactor but had not been added.

Repair:

- added `_coordinate_map_for_config(config, dimension)`.

### Focused Attempt 2

result:

```text
3 failed, 14 passed, 2 warnings in 9.80s
```

Blocker classification:

```text
fixable complexity-budget implementation issue with unchanged grids,
tolerances, and scientific contract.
```

Observed issue:

- M2.6c retained grids GL257 and GL321 exceeded the fitted TT's per-call
  evaluation budget, which was inherited from the 161-point fit config.

Repair:

- added chunked normalized retained-density evaluation so each chunk respects
  the existing fitted-TT budget.  The reviewed GL257 and GL321 grids were not
  changed.

### Focused Attempt 3

result:

```text
17 passed, 2 warnings in 10.39s
```

### Claude Code/Governance Blocker 1

result:

```text
BLOCKED_M2P6C_CODE_GOVERNANCE
```

Accepted blocker:

- the `t=1` transition path required `scalar_tt_grid`, but still reused the
  generic dense retained propagation helper after the storage-kind check.
  Claude required a TT-specific propagation routine with density-object and
  density-hash replay validation, plus a negative test that would fail if the
  TT path silently called the dense helper.

Repair:

- split scalar retained propagation into
  `_scalar_tt_predictive_log_density_from_retained` and the existing dense
  helper;
- made the TT helper validate `storage_kind = scalar_tt_grid`, the retained
  `SquaredTTDensity` object, and the density hash before using the retained
  grid fields;
- added a monkeypatch negative test that makes the dense helper raise and
  confirms the promoted TT path still runs.

Rerun result:

```text
Focused M2.6c repair evidence:
18 passed, 2 warnings in 10.73s.

Broad highdim guardrail:
144 passed, 2 warnings in 12.87s.
```

## Run Manifest

git commit: `7ccb9c39883471c2d5ec2891cbf33b9ed436bada`

dirty/untracked status:

```text
dirty/untracked workspace; active highdim code, tests, and P30 plan files are
untracked in this repository state, so empty git diff summaries do not imply
no local changes.
```

environment: `/home/chakwong/anaconda3/envs/tf-gpu`

CPU/GPU status:

```text
deliberate CPU-only tests; CUDA_VISIBLE_DEVICES=-1 set in pytest commands.
No GPU claim is made.
```

dtype: `tf.float64`

random seeds:

```text
p37-m2p6c-sv-short-tt
p37-m2p6c-sv-short-tt-replay
p37-m2p6c-retained-hash
```

Focused command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_sv_short_sequential_tt_value_path.py \
  tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py \
  tests/highdim/test_p30_stochastic_volatility.py
```

result:

```text
18 passed, 2 warnings in 10.73s
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
  tests/highdim/test_p30_sv_fixed_design_tt_target.py \
  tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py \
  tests/highdim/test_p30_sv_short_sequential_tt_value_path.py
```

result:

```text
144 passed, 2 warnings in 12.87s
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
  tests/highdim/test_p30_sv_short_sequential_tt_value_path.py \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6c-short-sequential-sv-tt-value-path-subplan-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6c-short-sequential-sv-tt-value-path-claude-review-ledger-2026-06-05.md
```

result:

```text
passed
```

## Decision Table

| Field | Status |
|---|---|
| Decision | `PASS_M2P6C` |
| Primary criterion status | `PASS_LOCAL` |
| Veto diagnostic status | `PASS_LOCAL` |
| Strongest uncertainty | two-observation scalar fixed-design bridge only |
| Next justified action | M2.6d SV TT lane closeout |
| Non-claims | no adaptive TT-cross, paper-scale, SMC, real-data, derivative, HMC, DSGE, GPU, or high-dimensional scalability claim |

## Post-Run Red Team

Strongest alternative explanation:

- The result may show that a one-dimensional degree-64 fixed-design TT is
  adequate for two adjacent scalar SV updates, not that the method scales to
  long horizons or high dimensions.

What would overturn promotion:

- Claude finds that the transition target still depends on the dense retained
  path as promoted evidence;
- a fresh dense comparator detects larger retained-moment or log-normalizer
  error than the reviewed tolerances allow;
- branch replay or density-hash checks fail after code review.

Weakest evidence:

- The promoted horizon is exactly two observations.  Longer sequential
  propagation remains M2.6d/M5+ work.
