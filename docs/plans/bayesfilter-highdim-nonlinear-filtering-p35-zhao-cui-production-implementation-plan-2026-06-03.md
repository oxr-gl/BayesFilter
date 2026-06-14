# P35 Zhao--Cui Production Implementation Plan

metadata_date: 2026-06-03

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- Gorodetsky, Karaman, and Marzouk, "A Continuous Analogue of the Tensor-Train
  Decomposition," Computer Methods in Applied Mechanics and Engineering, 2019.

source_artifacts:
- P30 Zhao--Cui expanded mathematical note:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
- P34 reference implementation audit:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p34-zhao-cui-reference-implementation-audit-result-2026-06-03.md`
- Fresh upstream clone:
  `third_party/audit/tensor-ssm-paper-demo`
- P10 reduced Octave-compatible audit snapshot:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source`

what_is_not_concluded:
- This plan does not claim the adaptive Zhao--Cui algorithm is globally
  differentiable.
- This plan does not claim the MATLAB repository is production BayesFilter code.
- This plan does not claim DSGE-scale accuracy or performance before the full
  validation ladder passes.
- This plan does not propose changing the existing v1 public API during the
  first implementation phases.
- This plan does not license-import or translate MATLAB files line by line.

## Evidence Contract

Question: can BayesFilter implement a production-quality, clean-room,
fixed-branch squared-TT sequential filter inspired by Zhao--Cui, with enough
tests to justify trying it on DSGE-style high-dimensional models later?

Baseline/comparator:

- exact analytic functions for basis, Gram, mass, marginalization, and
  normalization tests;
- exact Kalman filtering/evidence for small linear-Gaussian state-space models;
- finite differences for the declared fixed-branch scalar;
- P10 reduced Octave smoke for algorithm-stage sanity, not bitwise equality;
- Zhao--Cui paper examples as later stress tests.

Primary promotion criteria:

- value path matches exact small-model references within declared tolerances;
- fixed-branch derivative matches finite differences for the same deterministic
  scalar;
- every branch/failure exit is deterministic and tested;
- diagnostics prevent promotion when mass matrices, normalizers, CDF inversions,
  ranks, or residuals are invalid;
- memory and runtime scale according to declared dimension/rank/degree models
  on synthetic ladders before DSGE trials.

Veto diagnostics:

- any basis/transport path that lacks an explicit reference-measure convention;
- any fitted target evaluated under one measure while mass contractions use
  another;
- negative or NaN squared density normalizer;
- failed Gram/mass positive-definiteness after allowed stabilization;
- nonmonotone conditional CDF on declared grids;
- inverse-CDF round-trip failure;
- fixed-branch derivative finite-difference failure;
- hidden adaptive branch changes during derivative evaluation;
- finite-difference rows computed from different realized branch identities;
- exact score mismatch on small Kalman or dense-quadrature baselines;
- evidence or filtering marginal mismatch on exact Kalman tests;
- public API regression in existing tests.

Explanatory diagnostics:

- TT ranks, sweep residuals, condition numbers, fit/holdout residuals,
  enrichment deltas, ESS of correction samples, wall time, memory usage, and
  comparison with P10 smoke-stage outputs.

## Clean-Room And License Boundary

The authors' repository is an audit/reference artifact only.  It has an
LGPL/GPL-family boundary and MATLAB implementation details.  Production
BayesFilter code should be written from:

1. the mathematical P30 specification;
2. independently derived equations in the P30/P33 ledgers;
3. the observed high-level algorithm ordering in P34.

Do not copy MATLAB code, comments, class layouts, or helper implementations
into `bayesfilter/`.  When a design resembles the reference repository, record
the mathematical reason, not the source code line.

Operational provenance rules:

- implementation authors may inspect P30 and the project derivation ledgers
  while coding;
- the upstream MATLAB repository and P10 snapshot are read-only reference
  artifacts for planning, stage-order sanity, and post-hoc comparison, not
  coding templates;
- if a module's design is materially informed by direct inspection of upstream
  MATLAB internals, separate the roles: one person/agent writes a mathematical
  implementation brief from P30 notation, and a different person/agent authors
  the production module from that brief and tests;
- if role separation is not feasible, the result ledger must explicitly state
  that the project is using a single-author non-copy clean-room standard for
  that module, and a reviewer who did not author the code must perform the
  contamination audit before acceptance;
- each production module must carry a short provenance note in the plan/result
  ledger identifying the mathematical equations used and stating whether any
  upstream code was inspected during that module's implementation;
- no production implementation task should ask a worker to translate, port, or
  mimic a named MATLAB file;
- if a design decision is inspired by P34 static inspection, the implementation
  ledger must restate it as a mathematical operation from P30 before coding;
- a pre-merge audit must sample production functions and confirm that comments,
  names, and structure are not copied from the MATLAB source.

This boundary is not a claim that reading code is forbidden.  It is a claim
that production code must be justified by equations, tests, and BayesFilter
interfaces rather than by source-code inheritance.

## Measure Convention Gate

Every approximation path must declare its measure before fitting, mass
contraction, normalization, marginalization, transport construction, or
derivative evaluation.

Let \(r\) be physical coordinates and \(z\) be reference coordinates with
\(r=\Psi(z)\).  Let \(\lambda\) denote Lebesgue measure in \(z\), and let
\(\nu\) denote the declared reference measure with density \(\omega(z)\) with
respect to \(\lambda\):

```text
physical target density in r:          q_r(r) dr
Lebesgue pullback in z:                q_z^\lambda(z) dz
                                      = q_r(\Psi(z)) |det D\Psi(z)| dz
reference-measure target in z:         q_z^\nu(z) d\nu(z)
                                      = [q_z^\lambda(z)/omega(z)] d\nu(z)
```

Invariant:

- if basis mass matrices integrate against \(d\nu(z)=\omega(z)dz\), then the
  fitted square-root target must be a square root of \(q_z^\nu(z)\), not a
  square root of \(q_z^\lambda(z)\);
- if the fitted target is \(q_z^\lambda(z)\), then all mass contractions and
  normalizers must be Lebesgue contractions or must include the missing
  \(\omega\) factors explicitly;
- every density object must store `density_measure` as one of
  `PHYSICAL_LEBESGUE`, `REFERENCE_LEBESGUE`, or `REFERENCE_MEASURE`;
- every contraction must assert that its input density measure matches the
  mass convention.

Required gate tests:

- constant-density normalization under uniform reference;
- Gaussian pullback through a non-identity affine map, checked both as
  Lebesgue pullback and reference-measure target;
- non-uniform reference test where omitting the \(\omega\) factor produces a
  deliberately wrong normalizer that the gate catches;
- derivative of log normalizer under the same measure convention.

No value or derivative test may pass if the measure contract is absent.

## Implementation Scope

Initial scope: an optional internal high-dimensional module for fixed-branch
squared-TT filtering and derivative validation.

Proposed package layout:

```text
bayesfilter/highdim/
    __init__.py
    bases.py
    tt.py
    squared_tt.py
    transport.py
    fitting.py
    fixed_branch.py
    filtering.py
    diagnostics.py
    models.py
    derivatives.py
    validation.py
```

Proposed test layout:

```text
tests/highdim/
    test_bases.py
    test_tt_algebra.py
    test_squared_tt_density.py
    test_transport.py
    test_fixed_branch_fit.py
    test_filtering_kalman_exact.py
    test_fixed_branch_derivatives.py
    test_failure_exits.py
    test_scaling_smoke.py
```

Do not export new top-level `bayesfilter.__all__` symbols in Phases 0--6.
During Phases 1--6, users import from `bayesfilter.highdim` explicitly.  A
top-level public API decision is allowed only in Phase 7.

## Mathematical Objects To Implement

### Basis Layer

Objects:

- one-dimensional basis family;
- domain map;
- reference measure;
- explicit measure convention for basis mass and fitted target;
- quadrature or analytic mass matrix;
- basis value and derivative evaluation;
- Gram/mass stabilization diagnostics.

Minimum families:

- Legendre on bounded intervals;
- Hermite or Gaussian-weighted polynomial basis only after Legendre tests pass;
- optional Lagrange/interpolatory basis after core algebra is stable.

Required tests:

- shape and dtype invariants;
- measure-convention assertions before fitting or contraction;
- exact mass entries for low-degree Legendre bases;
- orthonormalization checks;
- derivative checks against finite differences;
- condition-number and ridge/floor diagnostics.

### Functional TT Layer

Objects:

- TT core list with ranks \(R_0=R_D=1\);
- coordinate ordering;
- basis index dimension per coordinate;
- evaluation contraction;
- integration/marginalization contraction;
- rank/shape invariants;
- deterministic serialization of a fixed branch.

Initial fitting:

- start with deterministic fixed-grid least squares and ridge regularization;
- postpone adaptive TT-cross/pivot/rank changes until after fixed-branch tests
  pass;
- store design matrices, sample points, row weights, ridge, ranks, and chosen
  solver.
- enforce early complexity caps before materializing design matrices:
  maximum rows, maximum columns, maximum dense matrix bytes, maximum condition
  number before ridge, and maximum rank budget.

Required tests:

- separable functions have rank-one representation;
- known low-rank bivariate and trivariate examples evaluate correctly;
- integrated TT matches analytic integrals on polynomial targets;
- marginalization preserves shape and normalization;
- saved branch reloads to identical evaluation;
- row/column/memory budget violations fail before allocation.

### Squared-TT Density Layer

Objects:

- square-root TT \(h(z)\);
- defensive/reference density term \(\tau q_0(z)\);
- nonnegative density \(q(z)\propto h(z)^2+\tau q_0(z)\);
- normalizer \(Z\);
- mass contractions;
- conditional marginal and conditional CDF builders.

Required tests:

- density is nonnegative on test grids;
- normalizer is positive and agrees with analytic examples;
- normalizer is computed under the declared measure convention;
- marginal densities integrate to one;
- defensive term prevents zero-mass failure in declared corner cases;
- error status is explicit when normalizer or mass matrix fails.

### Transport Layer

Objects:

- lower/upper triangular KR maps;
- conditional CDF evaluation;
- inverse conditional sampling;
- Jacobian determinant identity;
- CDF bracket/floor policy.

Required tests:

- monotonicity on declared grids;
- inverse-CDF round trip;
- uniform-to-target sampling on analytic Gaussian or beta-like examples;
- log-Jacobian equals sum of conditional log densities within tolerance;
- failure exits for nonmonotone CDFs and bracket failures.

### Filtering Value Path

Objects:

- state-space model protocol with transition density, observation density,
  initial density, parameter prior, simulator hooks, and dimensions;
- adjacent-state target builder;
- carried filter marginal;
- retained-state representation;
- fit configuration;
- correction-weight diagnostics;
- log normalizer/evidence accumulation.

Initial model suite:

1. one-step scalar linear-Gaussian model;
2. two-step scalar linear-Gaussian model;
3. small multivariate linear-Gaussian model;
4. nonlinear scalar observation model with dense quadrature oracle;
5. reduced Zhao--Cui Kalman-like model aligned with P10 smoke;
6. stochastic-volatility and SIR stress models;
7. predator-prey stress model only after positivity/state-domain issues are
   specified.

Promotion criteria:

- exact Kalman log evidence and filtering moments match within tolerance on
  the first three models;
- nonlinear scalar oracle agrees with dense quadrature;
- P10-aligned smoke reaches the same algorithm stages and finite diagnostics;
- no DSGE trial begins before these pass.

### Fixed-Branch Derivative Path

Objects:

- fixed branch record containing basis, ranks, sweep order, sample points,
  row weights, ridge, solver choices, mass matrices, normalizer floors,
  CDF/inversion settings, and retained-filter storage scheme;
- derivative of target evaluations;
- derivative of least-squares solution with fixed matrix or fixed design;
- derivative of TT core contractions;
- derivative of \(Z\), \(\log Z\), carried filter, and next target;
- total derivative of the declared scalar
  \(\widehat\ell_T(\theta;B,\mathcal F,y_{1:T})\).

Hard boundary:

- no derivative is claimed for adaptive branch selection, TT-cross pivot
  changes, rank changes, basis retraining, or data-dependent basis changes.

Required tests:

- unit finite differences for target evaluation derivatives;
- least-squares coefficient derivative checks;
- mass and normalizer derivative checks;
- carried-filter quotient derivative checks;
- two-step full scalar finite-difference table over \(h\);
- failure when branch object changes between value and derivative calls.

Exact score baselines:

- one-step scalar linear-Gaussian score against exact Kalman derivative;
- two-step scalar linear-Gaussian score against exact Kalman derivative;
- dense-quadrature nonlinear scalar score against finite-difference or
  automatic-differentiation oracle outside the TT code path;
- local neighborhood test around \(\theta_0\): for each finite-difference
  perturbation, verify the realized branch identity is unchanged before using
  the finite-difference row as evidence.

These tests certify the fixed-branch surrogate only.  They do not certify the
adaptive Zhao--Cui algorithm or exact nonlinear likelihood.

## Realized Branch Identity Contract

A branch is not just a nominal configuration.  It is the complete realized
sequence of numerical choices that define the deterministic scalar.

The branch identity record must include:

- basis family, degrees, domains, domain maps, reference measures, and measure
  convention;
- coordinate ordering, retained-coordinate layout, and physical/reference
  coordinate maps;
- preconditioners, shifts, scales, affine maps, nonlinear maps, and their
  fitted parameters;
- TT ranks, sweep order, selected rows, sample points, row weights, pivots if
  any, ridge values, solver choices, truncation decisions, and stopping
  reasons;
- defensive density family, \(\tau\), floors, normalizer floors, CDF brackets,
  inverse-CDF tolerances, and monotonicity repairs;
- mass matrices, Cholesky/square-root factors, stabilization constants, and
  branch-level condition diagnostics;
- retained-filter storage scheme and every normalizer passed to the next time
  step;
- random seeds or quasi-random generator states used to build the branch;
- code version and configuration hash.

The value path, derivative path, and finite-difference validation path must
all report a realized branch manifest and hash.  The hash must be computed
over a canonical serialization of the full manifest listed above, including
all numeric arrays through declared stable serialization rules.  A selective
or hand-curated subset hash is not sufficient evidence that the same scalar
was evaluated.

A finite-difference row is marked `INVALID_BRANCH_MISMATCH`, not failed
derivative evidence, if either \(+h\) or \(-h\) changes the realized branch
hash.

The fixed-branch derivative is accepted only for rows with identical realized
branch hashes and finite value diagnostics.

## Phase Plan

### Phase 0: Design Contract And Non-Public Skeleton

Deliverables:

- `bayesfilter/highdim/` package skeleton;
- dataclasses/protocols for basis, TT branch, fit config, diagnostics, model;
- measure convention enums and assertions;
- realized branch identity dataclass, full-manifest canonical serializer, and
  hash;
- backend policy note: production algorithmic implementation uses
  TensorFlow/TensorFlow Probability by default; NumPy is limited to independent
  reference solutions, comparison fixtures, closed-form sanity checks,
  serialization/reporting, and explicitly reviewed exceptions; JAX/PyTorch are
  non-default and require a separate reviewed exception before use;
- no top-level public API export;
- tests for import isolation and public API non-regression.

Exit criteria:

- existing test subset for public API passes;
- no external MATLAB code is imported;
- highdim module imports without TensorFlow GPU assumptions.
- branch identity and measure convention objects are required by constructors.
- no NumPy-backed BayesFilter-owned algorithmic path is introduced as the
  implementation default.

### Phase 1: Basis, Mass, And TT Algebra

Deliverables:

- Legendre basis on bounded domains;
- analytic or quadrature mass matrices;
- TT core evaluation/integration/marginalization;
- deterministic fixed-rank branch record.
- first memory/shape budget gate for design and contraction arrays.

Exit criteria:

- all basis and TT algebra tests pass;
- analytic polynomial examples match exact values/integrals;
- shape/rank diagnostics are explicit.
- non-uniform reference measure tests catch missing density-ratio factors.
- matrix-size and rank-budget gates fail before large allocation.

### Phase 2: Squared Density And Transport

Deliverables:

- squared-TT density object;
- normalizer and marginal contractions;
- conditional CDF and inverse-CDF sampler;
- defensive/reference density policy.

Exit criteria:

- nonnegativity, normalization, marginal, CDF monotonicity, inverse round-trip,
  and Jacobian tests pass;
- failure exits are covered by tests.
- all normalizer and marginalization tests run under the measure convention
  gate.

### Phase 3: Fixed-Branch Fitting

Deliverables:

- deterministic fixed-grid or supplied-sample least-squares TT fit;
- ridge and rank policy;
- holdout residual diagnostics;
- branch serialization/reload.
- row-count, dense-matrix-byte, rank-saturation, and coordinate-order
  sensitivity diagnostics.

Exit criteria:

- separable and low-rank analytic fits pass;
- branch reload is bitwise or tolerance-identical;
- fit diagnostics veto intentionally bad basis/rank choices.
- fixed-rank fitting refuses to proceed when complexity gates are exceeded.
- coordinate-order sensitivity is reported on at least one coupled analytic
  example.

### Phase 4: Filtering Value Path

Deliverables:

- model protocol and adjacent-state target builder;
- one-step and multi-step fixed-branch squared-TT filter;
- retained-filter storage for scalar and small vector retained states;
- log-evidence accumulation and diagnostic object.
- exact Kalman score fixtures for later derivative tests.

Exit criteria:

- exact Kalman one-step/two-step/multivariate tests pass;
- dense quadrature scalar nonlinear oracle test passes;
- P10-reduced smoke-stage comparison is documented;
- no public API export yet.
- P10 comparison is explicitly labeled `STAGE_SANITY_ONLY`, not correctness
  evidence.

### Phase 5: Fixed-Branch Derivative Path

Deliverables:

- derivative recursions for target values, LS coefficients, TT contractions,
  normalizers, carried filters, and next-step targets;
- finite-difference validation harness;
- same-branch enforcement.

Exit criteria:

- finite-difference tables pass for component and end-to-end scalars;
- exact small-model score baselines pass;
- branch-change tests fail loudly;
- finite-difference rows with branch mismatch are invalidated rather than
  counted as failures or successes;
- diagnostics clearly state `FIXED_BRANCH_ONLY`.

### Phase 6: Stress Models And Performance Ladder

Deliverables:

- Zhao--Cui-style Kalman, stochastic-volatility, SIR, and predator-prey
  configurations;
- memory/time scaling reports over dimension, rank, degree, and horizon;
- GPU/TFP performance memo if acceleration is needed;
- separate reviewed backend-exception memo before any JAX/PyTorch experiment is
  allowed to influence production implementation.

Exit criteria:

- stress models run with bounded memory and finite diagnostics;
- accuracy comparison against available references is recorded;
- performance ladder identifies bottlenecks and feasible DSGE trial size.

### Phase 7: Public API Decision

Deliverables:

- final audit result;
- API proposal if Phases 1--6 pass;
- documentation of limitations and fixed-branch derivative scope.

Exit criteria:

- existing `tests/test_v1_public_api.py` remains valid or is intentionally
  updated with review;
- public symbols are minimal and stable;
- no DSGE model integration occurs before public/internal readiness decision.

## Claude Review Procedure

Claude Code should review this plan before implementation.  Use Claude as a
hostile reviewer with veto power over the plan, not as the final authority over
production code.

Review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p35-zhao-cui-implementation-plan-review-iter<N> \
  --model sonnet \
  --effort high \
  "<prompt>"
```

Claude prompt requirements:

- read this P35 plan, P30 mathematical note, P34 reference audit, and P10
  paper-code crosswalk ledger;
- review as three personas: numerical analyst, production engineer, and
  HMC/statistical inference user;
- identify missing gates, hidden adaptive-branch assumptions, wrong baselines,
  license risks, performance blind spots, and tests that would not answer the
  stated question;
- classify each finding as blocker/major/minor;
- state whether the plan should pass, pass with required edits, or fail.

Codex audit of Claude findings:

- `ACCEPT`: patch plan.
- `PARTIAL`: patch narrower or different issue.
- `DISPUTE`: write rebuttal with file/section evidence.
- `CLARIFY`: gather evidence or ask human direction.

Maximum plan-review iterations: 5.

## Final Acceptance Criteria For This Plan

This plan is ready to execute only if:

- Claude review has no unresolved blocker;
- accepted findings are patched;
- disputed findings are recorded with evidence;
- the implementation scope remains clean-room and non-public until tests pass;
- the test ladder begins with exact small models, not DSGE;
- derivative claims remain fixed-branch only.
