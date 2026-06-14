# P34 Zhao--Cui Reference Implementation Audit Result

metadata_date: 2026-06-03

## Question

Can `DeepTransport/tensor-ssm-paper-demo` serve as a reference implementation
for a future production-quality BayesFilter implementation of the Zhao--Cui
tensor-train sequential filter?

## Evidence Contract

- Scientific/engineering question: whether the authors' repository contains a
  runnable algorithmic reference for the basic and preconditioned TT state-space
  model methods.
- Baseline/comparator: Zhao and Cui, "Tensor-Train Methods for Sequential State
  and Parameter Learning in State-Space Models," JMLR 2024, plus the P30
  annotated mathematical contract.
- Primary criterion: a reproducible code path that implements the sequential
  TT/SIRT filter on at least a small model and exposes the algorithm objects
  needed for porting.
- Veto diagnostics: no runnable path, missing core dependencies, no mapping from
  code to algorithms, incompatible license boundary, or outputs that cannot be
  interpreted.
- Explanatory diagnostics: examples, model suite, tensor-train options,
  preconditioning code, sample/ESS outputs, and static code organization.
- Not concluded: production readiness of BayesFilter code, DSGE performance,
  statistical accuracy on large models, or differentiability of the adaptive
  Zhao--Cui algorithm.

## Source Snapshot

- Upstream repository:
  `https://github.com/DeepTransport/tensor-ssm-paper-demo`
- Fresh clone location:
  `third_party/audit/tensor-ssm-paper-demo`
- Fresh clone commit:
  `80034dccb99eb1d86284a1839b4a12067d13b9da`
- Existing pinned P10 audit snapshot:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source`
- Upstream license boundary: the repository carries LGPL/GPL-family license
  files.  It must remain an audit/reference input unless a separate clean-room
  and license decision is made.

## What Was Inspected

- `README.md`: states MATLAB 2021a/2023a support, four paper examples
  (`eg1_kalman`, `eg2_sv`, `eg3_sir`, `eg4_predatorprey`), and the bundled
  `deep-tensor.dev` dependency.
- `deep-tensor.dev/README.md`: documents the continuous TT/SIRT/DIRT library
  and its literature lineage.
- `models/full_sol.m`: basic sequential full TT/SIRT solver, including prior
  propagation, ESS diagnostics, weighted covariance preconditioning, TT/SIRT
  reapproximation, sampling, importance correction, log marginal likelihood,
  and smoothing.
- `models/pre_sol.m`: preconditioned solver path with Gaussian/tempered
  preconditioning variants and residual target construction.
- `models/ssmodel.m`: state-space-model shell with `complete` and
  `push_samples`.
- `deep-tensor.dev/src/@TTSIRT/TTSIRT.m`: squared inverse Rosenblatt transport
  wrapper around `TTFun`.
- `deep-tensor.dev/src/@TTFun/TTFun.m`: functional tensor-train approximation
  class and cross/round/evaluate/integrate surface.
- Example scripts for Kalman and stochastic-volatility models.

## Execution Results

Direct upstream Octave smoke:

```bash
octave --quiet --eval "cd('third_party/audit/tensor-ssm-paper-demo/deep-tensor.dev'); load_dir; dom=BoundedDomain([0,1]); bases=ApproxBases(Legendre(3), dom, 2); disp(class(bases));"
```

Result: failed before algorithm execution.  Octave rejected MATLAB class syntax
in `src/Domains/Domain.m` with:

```text
external methods are only allowed in @-folders
```

Interpretation: this is an Octave compatibility blocker, not evidence that the
authors' MATLAB-supported repository is broken.

Existing P10 patched Octave smoke:

```bash
timeout 60s octave-cli --quiet --no-gui \
  third_party/audit/zhao_cui_tensor_ssm_p10/source/octave_compat/p10_octave_kalman_smoke.m
```

Result: completed the reduced Kalman TT/SIRT path and printed:

```text
P10_OCTAVE_SMOKE_DONE
```

Observed output included an FTT approximation at time 1, ALS rank diagnostics,
total ESS `7.34 / 64`, and a finite log-marginal-like scalar `-4.8422`.

Interpretation: after local compatibility patching and severe problem-size
reduction (`T=1`, `N=64`, rank `4`, one ALS pass), the core sequential TT/SIRT
path can execute in the local environment.  This validates the presence of a
real algorithmic path, not paper-level accuracy or production readiness.

## Static Findings

The repository is useful as a reference for:

- the object decomposition of the paper method:
  `ssmodel`, `full_sol`, `pre_sol`, `TTSIRT`, `TTFun`, model folders, and
  tensor-dot utilities;
- the sequence of operations in the basic filter:
  prior sampling, transition/likelihood update, ESS trigger, weighted
  linear map, target recentering, squared-TT fit, inverse Rosenblatt sampling,
  proposal correction, and smoothing;
- the preconditioning path:
  partial target construction, preconditioner fit, transformed residual fit,
  and sample push-forward/backward maps;
- the four model examples in the paper: Kalman, stochastic volatility, SIR,
  and predator-prey.

The repository is not sufficient by itself as production code because:

- upstream support is MATLAB, not Python;
- examples are scripts, not automated unit/regression tests;
- default examples are relatively large and plotting-oriented;
- deterministic seeds are not uniformly enforced;
- no DSGE-style model is included;
- at least one helper, `models/tensordot/ftt_sqrconv.m`, appears incomplete or
  stale in the fresh upstream clone because it references undefined variables
  such as `ftt1`, `core1`, and `core1_exp`;
- adaptive TT-cross/rank/pivot behavior is not a differentiable scalar
  contract for HMC gradients.

## Reference-Implementation Decision

Decision: use the authors' repository as a mathematical and algorithmic
reference, not as production BayesFilter code.

Recommended use:

1. Treat `third_party/audit/tensor-ssm-paper-demo` as the fresh upstream
   reference snapshot.
2. Treat `third_party/audit/zhao_cui_tensor_ssm_p10/source` as the local
   reduced-execution audit snapshot.
3. Build BayesFilter production code by clean-room translation from the P30
   mathematical specification and the inspected algorithmic sequence, not by
   importing MATLAB files.
4. Start with a minimal fixed-branch squared-TT filter on a tiny linear-Gaussian
   model where Kalman evidence/filtering moments are available exactly.
5. Add regression tests against the reduced P10 smoke at the level of algorithm
   stages and diagnostics, not bitwise equality.
6. Only after exact small-model tests pass, add stochastic-volatility, SIR, and
   predator-prey-style tests as stress cases.

## Minimal Production Test Ladder Suggested Next

1. Basis and mass tests: one-dimensional polynomial basis values, Gram matrices,
   mass contractions, and normalization on analytic functions.
2. TT algebra tests: evaluation, integration, marginalization, rank-shape
   invariants, and nonnegative squared density reconstruction.
3. Transport tests: triangular conditional CDF monotonicity, inverse-CDF
   round-trip, KR Jacobian identity, and sample moment checks.
4. Filtering tests: one-step and two-step linear-Gaussian models against exact
   Kalman evidence and filtering marginals.
5. Fixed-branch derivative tests: finite differences for target evaluations,
   least-squares coefficients, normalizers, carried filters, and total
   log-likelihood.
6. Robustness tests: rank ladder failure exits, ill-conditioned mass matrices,
   defensive-density floor, negative/NaN target handling, and ESS collapse.
7. Performance tests: memory and wall-time scaling in dimension, rank, basis
   degree, time horizon, and retained-state dimension.
8. Paper-model tests: Kalman, stochastic volatility, SIR, and predator-prey
   models configured to match Zhao--Cui as closely as practical.

## What Is Not Concluded

- The upstream repository has not been run in MATLAB in this audit.
- The paper figures have not been reproduced.
- No claim is made that the upstream adaptive implementation is globally
  differentiable.
- No claim is made that the reduced Octave smoke is statistically accurate.
- No claim is made that a DSGE-scale BayesFilter implementation will be fast,
  stable, or accurate without the production test ladder above.
