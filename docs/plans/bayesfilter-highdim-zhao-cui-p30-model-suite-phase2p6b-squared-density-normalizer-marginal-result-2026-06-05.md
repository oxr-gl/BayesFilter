# P37-M2.6b Result: Squared-Density Normalizer And Retained Density For Scalar SV Adjacent Targets

metadata_date: 2026-06-06
phase: P37-M2.6b

## Decision

Decision: `PASS_M2P6B`.

M2.6b adds clean-room squared-density normalizer and scalar all-retained
normalized-density evidence for the fixed scalar stochastic-volatility adjacent
targets passed in M2.6a.  The new evidence checks the fitted square-root
functional TT against independent dense oracle quadrature on fresh M2.6b audit
grids.

This is not a sequential TT/SIRT filtering result.

## Source-Governance Status

- P30 anchors identified: `eq:p33-square-mass`, `eq:p33-mass-matrix`,
  `eq:p33-mass-recursion`, `eq:p33-mass-final`,
  `eq:p33-density-with-floor`, `eq:p33-full-normalizer`,
  `eq:p33-retained-marginal`, and `eq:p33-retained-normalized`.
- Zhao--Cui paper anchors identified: Eq. (13), Lemma 1, Proposition 2,
  Eq. (14), and Algorithm 1(c), as cross-checked through the P10 paper-code
  crosswalk.
- MATLAB behavioral anchors identified: `deep-tensor.dev/src/SIRT.m`,
  `deep-tensor.dev/src/@TTSIRT/TTSIRT.m`,
  `deep-tensor.dev/src/@TTSIRT/marginalise.m`, and
  `deep-tensor.dev/src/@TTIRT/marginalise.m`.
- BayesFilter code/test anchors identified:
  `bayesfilter/highdim/squared_tt.py`,
  `bayesfilter/highdim/__init__.py`,
  `tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py`,
  `tests/highdim/test_p30_sv_fixed_design_tt_target.py`, and
  `tests/highdim/test_squared_tt_density.py`.
- Deviations listed: yes.  This is a BayesFilter fixed-design scalar density
  check.  It is not MATLAB adaptive cross, not generic integrated-axis
  marginalization, and not full SIRT reproduction.
- Clean-room boundary respected: yes.  MATLAB code was used as audited
  behavioral reference only and was not copied or line-translated.
- Unsupported claims removed: yes.
- Reviewer verdict: `PASS_M2P6B_CODE_GOVERNANCE`.

## Evidence Contract Status

| Field | Status |
|---|---|
| Primary criterion | `PASS_LOCAL`; initial and transition square-mass normalizers match independent dense oracle quadrature on `p37.m2p6b.sv.normalizer-audit.gl257.v1`; scalar all-retained normalized density values match dense oracle values on `p37.m2p6b.sv.retained-density-audit.mid173.v1` |
| Veto diagnostics | `PASS_LOCAL`; no nonfinite values, M2.6a lineage drift, fixture drift, stale-grid promotion, tau/floor drift, metadata-only retained-density promotion, or guardrail regression was observed |
| Explanatory diagnostics | positive-tau auxiliary path checked at `tau_auxiliary=1e-12`; existing `conditional_density` and `marginal_density` remain non-promoted for M2.6b |
| Main uncertainty | the result is scalar and all-retained; integrated-axis marginal values and sequential recursion remain future gates |
| Next justified action | M2.6c short sequential SV TT/SIRT-like value path against dense oracle |
| What is not concluded | no sequential SV log evidence, adaptive TT-cross reproduction, paper-scale `T=1000`, SMC or real-data validation, derivative/HMC/DSGE/GPU readiness, or high-dimensional scalability claim |

## Implemented Behavior

New M2.6b helper:

```text
SquaredTTDensity.normalized_retained_density_values(keep_axes, points)
```

The helper is deliberately narrow:

- it evaluates the normalized retained density only when all axes are retained;
- it validates finite float64 point inputs;
- it raises `NotImplementedError` for genuine integrated-axis marginalization;
- it uses the existing squared-density normalizer rather than
  `conditional_density`, pointwise slice normalization, or metadata-only
  `marginal_density`.

New tests:

```text
tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py
```

The tests:

- reuse the exact M2.6a scalar SV fixture lineage;
- rebuild initial and transition adjacent targets with the reviewed degree-64
  basis and fixed rank `(1, 1)`;
- compare the TT square-mass normalizer with dense oracle quadrature on
  `p37.m2p6b.sv.normalizer-audit.gl257.v1`;
- compare normalized retained-density values with dense oracle values on
  `p37.m2p6b.sv.retained-density-audit.mid173.v1`;
- check the auxiliary positive-tau normalizer path at `tau=1e-12`;
- assert that metadata-only marginal output is not the promoted retained
  density path;
- assert that the helper rejects non-all-retained integrated-axis use.

## Fixture Lineage

M2.6b reused the passed M2.6a lineage:

```text
source_fixture_id = p37.m2p6a.sv.scalar.fixed-target.v1
source_fit_fixture_id = p37.m2p6a.sv.fixed-design-fit.degree64.v2
initial_target_id = p37.m2p6a.sv.initial.t0.v1
transition_target_id = p37.m2p6a.sv.transition.t1.v1
coordinate_map = AffineCoordinateMap(offset=[0.0], matrix=[[8.0]])
basis = normalized LegendreBasis1D(BoundedInterval(-1.0, 1.0), max_degree=64)
ranks = (1, 1)
defensive_density = TensorProductReferenceDensity(product_basis, convention)
tau_primary = 0.0
tau_auxiliary = 1e-12
normalizer_floor = 1e-12
denominator_floor = 1e-12
```

The transition target reused the M2.6a scalar dense retained filter after
`y_0`; the test checks the retained-filter hash at runtime.

## Failure And Repair Log

### Focused Attempt 1

Focused command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py \
  tests/highdim/test_p30_sv_fixed_design_tt_target.py \
  tests/highdim/test_squared_tt_density.py
```

result:

```text
3 failed, 12 passed, 2 warnings in 3.97s
```

Blocker classification:

```text
fixable test-contract/lineage assertion bug; scientific contract unchanged.
```

Observed issues:

- the lineage assertion used a hand-shaped partial product-basis dictionary
  rather than the actual emitted manifest schema;
- the substitute-rejection test compared against `conditional_density`,
  contradicting the reviewed M2.6b rule that `conditional_density` is not the
  promoted retained-density route.

Repair:

- assert strict product-basis manifest fields directly;
- assert that `marginal_density` remains metadata-only and that the promoted
  route is `normalized_retained_density_values`.

Process note:

```text
Codex applied this narrow repair before a separate Claude repair-plan review.
No M2.6b phase pass is claimed from the local repair alone.  Claude
code/governance review must accept or block this process deviation before the
phase may pass.
```

### Focused Attempt 2

result:

```text
15 passed, 2 warnings in 4.30s
```

## Run Manifest

git commit: `7ccb9c39883471c2d5ec2891cbf33b9ed436bada`

dirty/untracked status:

```text
dirty/untracked workspace; active M2.6b highdim files and P30 plan files are
untracked in this repository state.
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
p37-m2p6b-initial-target
p37-m2p6b-transition-target
p37-m2p6a-retained-t0
p37-m2p6b-initial-fit
p37-m2p6b-transition-fit
p37-m2p6b-substitute-rejection-fit
```

Focused command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py \
  tests/highdim/test_p30_sv_fixed_design_tt_target.py \
  tests/highdim/test_squared_tt_density.py
```

result:

```text
15 passed, 2 warnings in 4.30s
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
  tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py
```

result:

```text
138 passed, 2 warnings in 11.97s
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
git diff --check -- bayesfilter/highdim/squared_tt.py bayesfilter/highdim/__init__.py \
  tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py
```

result:

```text
passed
```

## Decision Table

| Field | Status |
|---|---|
| Decision | `PASS_M2P6B` |
| Primary criterion status | `PASS_LOCAL` |
| Veto diagnostic status | `PASS_LOCAL` |
| Strongest uncertainty | scalar all-retained evidence only; no integrated-axis or sequential evidence |
| Next justified action | M2.6c short sequential SV TT/SIRT-like value path |
| Non-claims | no sequential TT/SIRT, adaptive cross, paper-scale, SMC, real-data, derivative, HMC, DSGE, GPU, or scalability claim |

## Post-Run Red Team

Strongest alternative explanation:

- The result may only show that a degree-64 one-dimensional fixed-design TT
  fit is accurate enough for these two adjacent scalar targets, not that the
  full stochastic-volatility filtering recursion is validated.

What would overturn promotion:

- a fresh dense oracle grid finds normalizer or retained-density mismatch;
- the branch lineage drifts from M2.6a;
- Claude rejects the local repair process or finds the retained-density helper
  overclaims marginalization.

Weakest evidence:

- M2.6b validates all axes retained in a scalar case.  It deliberately does
  not validate integrated-axis marginalization.
