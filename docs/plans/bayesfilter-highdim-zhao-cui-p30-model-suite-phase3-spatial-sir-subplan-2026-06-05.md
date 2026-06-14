# P37-M3 Subplan: Spatial SIR High-Dimensional State Tests

metadata_date: 2026-06-05

parent_plan:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md`

## Purpose

Implement the P30 spatial SIR benchmark as the first source-governed test of
moderate-dimensional latent state filtering with partial observations.

M3 is split into an executable first gate and later ladder gates.  The first
gate may implement the P30 SIR model contract, deterministic RK4 transition,
observation likelihood, simulation fixtures, observed/unobserved RMSE
diagnostics, registry promotion from `REFERENCE_ONLY` only after
BayesFilter-native tests, and traceability/result ledgers.  It may not claim a
production TT/SIRT SIR filter, paper-scale accuracy, or high-dimensional
scalability.

## Mathematical Model

For compartments `j=1,...,J`, represent the state by

```text
x(t) = (S_1(t), I_1(t), ..., S_J(t), I_J(t)) in R^{2J}
```

with ODE dynamics

```text
dS_j/dt = -kappa_j S_j I_j + 1/2 sum_{i in I_j} (S_i - S_j)
dI_j/dt =  kappa_j S_j I_j - nu_j I_j + 1/2 sum_{i in I_j} (I_i - I_j)
dR_j/dt =  nu_j I_j + 1/2 sum_{i in I_j} (R_i - R_j)
```

and discrete transition

```text
X_k = X_{k-1} + integral_{(k-1)Delta}^{k Delta} G(x(s)) ds + eps_k^x
eps_k^x ~ N(0, Sigma_x)
Y_{k,j} = X_{k,2j} + eps_{k,j}^y,   eps_k^y ~ N(0, Sigma_y)
```

P30 paper-scale setting:

```text
J = 9, D = 18, T = 20
kappa_j = 0.1, nu_j = 18
Delta = 0.02
RK4 internal step = 0.005
Sigma_x = I_{2J}
Sigma_y = 100 I_J
S_j(0)=485+j, I_j(0)=15-j
X_0 ~ N(mu_0, I_18)
R in {10,20,40}
```

## Source-Governance Status

- P30 anchors: `eq:p27-sir1`--`eq:p27-sir13`.
- Paper anchor: spatial SIR benchmark section.
- MATLAB anchors: `eg3_sir/mainscript.m` and audited SIR likelihood helper
  paths recorded in the P34/P10 audit ledgers.
- BayesFilter current anchors: none for highdim SIR; starts as
  `REFERENCE_ONLY`.

## Evidence Contract

Question: can BayesFilter reproduce the P30 spatial SIR model contracts and
run partial-observation filtering tests from small `J` up to the paper-scale
`J=9` setting?

First-gate question: can BayesFilter implement and test the P30 SIR transition,
observation, simulation, domain policy, and observed/unobserved diagnostic
contracts on small deterministic rows without promoting a full nonlinear
filtering or scalability claim?

Decision table:

| Field | Contract |
|---|---|
| Baseline / comparator | RK4 hand-check/small-step transition reference; synthetic truth for observed and unobserved states |
| First-gate primary criterion | small `J` rows pass transition/domain/observation/likelihood/simulation checks and report observed plus unobserved RMSE diagnostics under a declared estimator baseline |
| Later-gate primary criterion | small filtering rows pass before any `J=5`/`J=9` paper-scale or rank-ladder row is promoted |
| Veto diagnostics | negative populations without policy, ODE-step mismatch, observed-only claim, nonfinite state/likelihood, unclassified resource failure |
| Explanatory only | ODE timing, rank growth, raw ESS, posterior plots, wall time |

Primary pass criteria:

- RK4 transition tests match hand-check or small-step reference rows;
- positivity/domain policy is explicit before stochastic perturbations;
- observed and unobserved component RMSE are reported separately;
- first-gate diagnostic rows use a declared estimator baseline, for example
  one-step transition mean versus synthetic truth, and must label it as a
  diagnostic rather than posterior filtering accuracy;
- memory, wall time, ranks, condition numbers, and ESS quantiles are recorded;
- paper-scale rows are promoted only after smaller `J` rows pass.

Vetoes:

- silent negative populations without a declared domain policy;
- using only observed infectious components as the accuracy claim;
- ODE step mismatch without a documented deviation;
- nonfinite ODE transition, likelihood, normalizer, or ESS;
- resource failure without classification;
- claiming all epidemic models have moderate TT rank.

## Fairness And Evidence Boundary

Fair comparison controls:

- all rows use the same spatial graph, neighbor convention, `Delta`, RK4
  internal step, initial condition, observation mask, noise covariance,
  observations, dtype, and seed ledger when comparing methods or ranks;
- observed and unobserved RMSE are both reported for the same synthetic truth;
- if a row changes graph size, rank, basis, or horizon, it is labeled as a
  ladder row rather than a direct method comparison.

BayesFilter-native evidence required for promotion:

- deterministic RK4 fixture tests;
- small `J` synthetic-truth diagnostic rows for the first gate;
- small `J` synthetic-truth filtering rows only in a later gate after a
  reviewed filter contract exists;
- explicit domain/positivity policy;
- resource and failure manifest.

MATLAB agreement can confirm source settings, but BayesFilter must supply its
own transition tests, likelihood tests, and synthetic filtering diagnostics.

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW_AFTER_SCOPE_HARDENING`.

The original M3 wording risked treating "small SIR rows" as if they already
implied a nonlinear posterior filtering implementation and a path toward
paper-scale `J=9` evidence.  That would be a wrong baseline and a proxy-metric
failure: RK4 transition tests, observation-mask tests, and one-step
synthetic-truth diagnostics are necessary model-contract evidence, but they are
not posterior filtering accuracy, TT/SIRT accuracy, or scalability evidence.

The hardened scope therefore makes the first gate a model-contract gate:
source equations, deterministic RK4 transition, Gaussian transition density,
infectious-only observation likelihood, simulation, domain policy, separate
observed/unobserved diagnostics, registry/traceability updates, and result
ledger.  Paper-scale rows, rank ladders, posterior filtering claims, and
high-dimensional scalability remain blocked until later reviewed subgates.

The hidden-assumption risk is population positivity.  P30 adds Gaussian process
noise after the RK4 transition, so stochastic samples can become negative even
when the deterministic RK4 mean is finite.  The first gate must declare this
as `diagnose_negative_after_noise` or an equivalent explicit policy; it may not
silently clip, project, or ignore negative states.

No material flaw remains in sending this narrowed M3 plan to Claude plan
review.  Implementation may not begin until `PASS_M3_PLAN`.

## Stop Conditions And Pre-Mortem

Stop before `J=9` if RK4 fixtures fail, state-domain policy is unresolved,
observed/unobserved RMSE cannot both be computed, or memory/rank budgets are
exceeded.

Misleading-pass risks:

- observed infectious components look accurate while susceptible components
  are poor;
- large observation noise masks dynamics errors;
- ODE solver cost dominates but is mistaken for TT scaling behavior;
- a single graph is overgeneralized to epidemic models broadly.

## Implementation Tasks

1. Implement SIR fixture generator for `J in {1,3}` before `J=5,9`.
2. Implement a TensorFlow `SpatialSIRSSM` model in `bayesfilter/highdim/models.py`
   with explicit `state_dim=2J`, `observation_dim=J`, `parameter_dim=0`, P30
   source equations in `manifest_payload`, deterministic RK4 mean transition,
   Gaussian transition log density, infectious-coordinate observation log
   density, and a simulation helper with seeded process and observation noise.
3. Add RK4 unit tests for one deterministic step with fixed parameters.  The
   tests must include an independent small-step or hand-check reference that is
   not a call to the production method under test.
4. Add observation-mask tests proving only infectious coordinates are observed.
5. Add finite likelihood, transition-density, and domain-policy tests.  The
   first gate may use the declared policy `diagnose_negative_after_noise`:
   deterministic RK4 means must remain finite, while stochastic Gaussian
   perturbations may leave the positive population domain and must be recorded
   as a diagnostic risk rather than silently clipped.
6. Add synthetic trajectory diagnostic tests reporting `RMSE_O` and `RMSE_U`
   separately for a declared baseline, such as deterministic one-step
   transition means.  These diagnostics must not be called posterior filtering
   accuracy.
7. Update the SIR registry and traceability rows only to the evidence boundary
   supported by the first gate, likely `BAYESFILTER_EXTENSION` with explicit
   non-claims.
8. Add dimension ladder `J in {3,5,9}` and rank ladder `R in {10,20,40}`
   only after small rows pass and a later filtering/rank-ladder subgate is
   reviewed.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/models.py
bayesfilter/highdim/validation.py
tests/highdim/test_p30_spatial_sir.py
docs/plans/*p37*phase3*claude-review-ledger*.md
docs/plans/*p37*phase3*result*.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

## Planned Commands

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_spatial_sir.py

git diff --check
```

Paper-scale or GPU rows require a separate experiment plan and run manifest.

## Exit Criteria

- first-gate small SIR rows pass with explicit observed/unobserved diagnostics;
- registry and traceability status state the exact evidence boundary;
- any later paper-scale row records exact `J,T,R,p`, RK4, and domain policy;
- result ledger classifies approximation, tuning, resource, and numerical
  failures separately;
- no overclaim beyond tested graphs and dimensions.
