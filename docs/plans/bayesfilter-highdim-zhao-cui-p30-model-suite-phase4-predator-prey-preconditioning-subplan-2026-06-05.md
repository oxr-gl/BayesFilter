# P37-M4 Subplan: Predator-Prey Nonlinear Preconditioning Tests

metadata_date: 2026-06-05

parent_plan:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md`

## Purpose

Implement the P30 predator-prey benchmark as the source-governed test of
whether nonlinear preconditioning improves a nonlinear dynamical filtering
problem enough to justify its cost.

M4 is split into a first executable gate and a later comparison gate.  The
first gate may implement the P30 predator-prey model contract, parameter box,
initial-state prior, deterministic RK4 transition, Gaussian transition and
observation densities, seeded simulation, trajectory diagnostics, and a
matched-comparison manifest schema.  It may not claim that nonlinear
preconditioning is beneficial until both linear and nonlinear preconditioner
rows run under matched budgets with accuracy and cost-normalized diagnostics.

## Mathematical Model

Continuous dynamics:

```text
dP/dt = r P (1 - P/K) - s P Q / (a + P)
dQ/dt = u P Q / (a + P) - v Q
theta = (r, K, a, s, u, v)
```

Discrete transition and observation:

```text
X_k = X_{k-1} + integral_{(k-1)Delta}^{k Delta} G(x(s);theta) ds + eps_k^x
eps_k^x ~ N(0, Sigma_x)
Y_k = X_k + eps_k^y,   eps_k^y ~ N(0, Sigma_y)
```

P30 paper-scale setting:

```text
theta_true = (0.6, 114, 25, 0.3, 0.5, 0.5)
x0_true = (50,5)
Delta = 2
RK4 internal step = 0.1
Sigma_x = 4 I_2
Sigma_y = 4 I_2
theta prior box =
  [0.1,1.1] x [110,130] x [20,30] x [0.1,1.1] x [0,1] x [0,1]
X_0 ~ N((50,5), I_2)
```

## Source-Governance Status

- P30 anchors: `eq:p27-pp1`--`eq:p27-pp8`.
- Zhao--Cui paper anchors: model-suite predator-prey example in the validation
  section; state-space model equations (1)--(3); TT/SIRT approximation and
  filtering recursion in Algorithm 1 for later comparison context; Section 5
  preconditioning construction; Eq. (30)--Eq. (35) and Algorithms 3--5 for
  linear/nonlinear preconditioning and transport context.  The first gate uses
  these as comparison-governance anchors only; it does not implement the
  preconditioning algorithms.
- MATLAB anchors: `eg4_predatorprey/mainscript.m`, `models/pre_sol.m`.
- BayesFilter current anchors: none for highdim predator-prey; starts as
  `REFERENCE_ONLY`.

## Evidence Contract

Question: under the same model, basis, nominal rank, and sweep budget, does
nonlinear preconditioning improve ESS and cost-normalized ESS relative to the
linear Gaussian bridge?

First-gate question: can BayesFilter implement and test the P30 predator-prey
model, parameter box, prior, RK4 transition, likelihood, simulation, and
matched-comparison manifest contracts without promoting a preconditioning
advantage claim?

First-gate traceability transition: if local evidence and Claude
code/governance review pass, the predator-prey traceability row may move from
`REFERENCE_ONLY` to `BAYESFILTER_EXTENSION` for model-contract and
comparison-governance evidence only.  The row must keep as non-claims:
nonlinear preconditioning usefulness, matched linear/nonlinear comparison
success, paper-scale results, adaptive MATLAB behavior, high-dimensional
scalability, HMC, DSGE, GPU production, and stable top-level public API.

Decision table:

| Field | Contract |
|---|---|
| Baseline / comparator | matched linear Gaussian bridge versus matched nonlinear bridge |
| First-gate primary criterion | deterministic model/prior/likelihood/simulation tests pass and the manifest schema blocks unmatched or proxy-only comparison rows |
| Later-gate primary criterion | nonlinear bridge improves declared accuracy/proposal metric and cost-normalized ESS under fair comparison controls |
| Veto diagnostics | unmatched budgets, nonfinite ODE/ESS, ESS-only success when cost fails, domain failure, unclassified tuning failure |
| Explanatory only | raw ESS alone, trajectory plots, wall time alone, qualitative MATLAB similarity |

Primary pass criteria:

- deterministic ODE/RK4 transition tests pass;
- first-gate prior, parameter-box, transition-density, observation-density,
  simulation, and trajectory-diagnostic tests pass;
- matched-comparison manifests reject unmatched budgets and proxy-only success;
- later-gate linear and nonlinear preconditioners run under matched settings;
- later-gate `Delta_ESS(t)` and `Delta_cost(t)` are reported;
- nonlinear preconditioning is promoted only in a later gate if both accuracy
  diagnostics and cost-normalized diagnostics support it;
- failures are classified rather than hidden.

Vetoes:

- comparing preconditioners under different rank/basis/sweep budgets without
  labeling the comparison unfair;
- nonfinite ODE, likelihood, normalizer, ESS, or wall-time metric;
- population/domain failures without policy;
- claiming nonlinear preconditioning is always beneficial;
- treating ESS improvement alone as success when cost-normalized improvement
  fails.

## Fairness And Evidence Boundary

Matched means:

- same observations, latent truth, prior, parameter box, initial-state prior,
  `Delta`, RK4 internal step, noise covariances, dtype, random seeds, basis
  family, basis size, nominal rank cap, sweep count, stopping tolerance,
  sample count, and wall-time accounting policy;
- if nonlinear preconditioning uses extra target evaluations or ODE solves,
  those costs are included in `Delta_cost`;
- if a method gets a larger rank, longer tuning budget, or different
  observations, the row is exploratory only.

BayesFilter-native evidence required for promotion:

- deterministic ODE fixture tests;
- first-gate parameter/prior/likelihood/simulation tests;
- first-gate matched-comparison manifest schema tests;
- later-gate matched linear/nonlinear comparison table;
- later-gate accuracy/proposal metric and cost-normalized ESS;
- failure classification for resource, tuning, approximation, and numerical
  vetoes.

MATLAB agreement can support setup fidelity.  It cannot prove that the
BayesFilter nonlinear preconditioner is correct or beneficial.

## Stop Conditions And Pre-Mortem

Stop before full comparison if ODE fixtures fail, domain policy is unresolved,
parameter/prior contracts fail, linear bridge cannot run under finite
diagnostics, or cost accounting is missing.

Misleading-pass risks:

- nonlinear bridge improves ESS but is too expensive;
- raw ESS improves while trajectory accuracy worsens;
- comparisons use unequal tuning budgets;
- one parameter box result is overgeneralized to all nonlinear
  preconditioning.

## Implementation Tasks

1. Implement deterministic predator-prey RK4 step tests.
2. Implement a TensorFlow `PredatorPreySSM` model in
   `bayesfilter/highdim/models.py` with explicit state dimension 2,
   parameter dimension 6, P30 source equations in `manifest_payload`,
   deterministic RK4 transition mean, Gaussian transition density, full-state
   Gaussian observation density, seeded simulation, parameter-box validation,
   and trajectory RMSE diagnostics.
3. Implement parameter-box and initial-state prior fixtures.
4. Implement matched-comparison manifest/schema tests that require matched
   basis/rank/sweeps/sample count/seed/noise/observations and both
   `Delta_ESS` and `Delta_cost` before any preconditioning comparison can be
   promoted.
5. Defer matched linear and nonlinear preconditioning experiment rows to a
   later reviewed subgate after model-contract tests and cost-accounting
   schema pass.
6. Record `Q_ESS(0.25,t)`, `Q_ESS(0.50,t)`, `Q_ESS(0.75,t)`,
   `Delta_ESS`, `Delta_cost`, trajectory RMSE, coverage, wall time, and memory
   only for rows that actually run.
7. Add a result-ledger decision table separating model-contract evidence,
   accuracy, proposal quality, and cost.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/models.py
bayesfilter/highdim/validation.py
tests/highdim/test_p30_predator_prey.py
docs/plans/*p37*phase4*claude-review-ledger*.md
docs/plans/*p37*phase4*result*.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

## Planned Commands

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_predator_prey.py

git diff --check
```

Paper-scale preconditioning comparisons require a separate experiment plan if
runtime exceeds the quick-test threshold.

## Exit Criteria

- ODE and prior fixtures pass;
- first-gate matched-comparison schema blocks unmatched or proxy-only rows;
- matched comparison rows are either deferred or later passed/blocked with
  failure reasons;
- result ledger states that nonlinear preconditioning usefulness is not
  concluded in the first gate;
- no general preconditioning superiority claim.

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW_AFTER_SCOPE_HARDENING`.

The original M4 wording risked treating model-fixture success as evidence for
the preconditioning hypothesis.  That would be a proxy-metric error.  A
predator-prey RK4 implementation, likelihood checks, and synthetic simulation
are necessary to make the benchmark executable, but they do not compare a
linear bridge with a nonlinear bridge and they do not establish an ESS or
cost-normalized advantage.

The first gate is therefore narrowed to model-contract and comparison-governance
evidence.  A later subgate must implement actual matched linear/nonlinear
preconditioning rows before any `Delta_ESS`, `Delta_cost`, or usefulness claim
can be promoted.

The initial plan review found two fixable governance issues: the paper anchor
was too vague, and the traceability transition was not explicit enough.  This
revision names the Zhao--Cui model-suite, state-space recursion,
preconditioning-equation, and algorithm anchors, and predeclares the only
allowed first-gate row transition: `REFERENCE_ONLY` to `BAYESFILTER_EXTENSION`
for model-contract evidence, with all preconditioning usefulness and
large-scale claims still blocked.

No material flaw remains in sending this narrowed M4 plan to Claude plan
review.  Implementation may not begin until `PASS_M4_PLAN`.
