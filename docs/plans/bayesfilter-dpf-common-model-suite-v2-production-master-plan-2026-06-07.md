# DPF Common Model Suite V2 Production Master Plan

metadata_date: 2026-06-07
status: REVIEWED_READY_FOR_P0_EXECUTION

## Purpose

Upgrade `experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py`
from the closed v1 smoke/common-sense suite into the production-level common
model contract for BayesFilter/FilterFlow tie-outs.

This is a new v2 evidence program.  It must not mutate, overwrite, or reinterpret
the closed 2026-06-06/2026-06-07 v1 artifacts:

- `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_tieout_2026-06-06.json`
- `experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_noresampling_2026-06-06.json`
- `experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_fixed_resampling_2026-06-06.json`
- `experiments/dpf_implementation/reports/outputs/dpf_common_fixed_branch_gradient_2026-06-06.json`
- `experiments/dpf_implementation/reports/outputs/dpf_cross_impl_closed_fixture_manifest_2026-06-07.json`

## Core Decision

V2 becomes the production common model suite.  The standalone fixture modules

- `experiments/dpf_implementation/tf_tfp/fixtures/lgssm_tf.py`
- `experiments/dpf_implementation/tf_tfp/fixtures/stochastic_volatility_tf.py`
- `experiments/dpf_implementation/tf_tfp/fixtures/range_bearing_tf.py`

are transitional sources only.  They may be retired after v2 absorbs their model
definitions, simulated observations, checksums, and density/path semantics into
`common_model_suite_tf.py` and after the v2 evidence ladder passes.

Retirement means no production runner imports these three standalone modules and
new evidence points to v2 artifacts.  Physical deletion is a final cleanup step
after review, not a precondition for v2 testing.

## V2 Model Coverage

V2 must include these production contract rows:

| V2 model id | Source surface | Required coverage |
|---|---|---|
| `lgssm_2d_h25_rich` | current `lgssm_tf.py` fixture semantics | 2D linear Gaussian dynamics, simulated horizon-25 observations, density, fixed-noise paths, fixed-ancestor paths, physical gradients |
| `sv_1d_h18_rich` | current `stochastic_volatility_tf.py` fixture semantics | 1D stochastic volatility with `mu`, `phi`, `sigma`, simulated horizon-18 observations, density, fixed-noise paths, fixed-ancestor paths, physical gradients |
| `range_bearing_4d_h20_rich` | current `range_bearing_tf.py` fixture semantics | 4D constant-velocity range-bearing with angle wrapping, simulated horizon-20 observations, density, fixed-noise paths, fixed-ancestor paths, physical gradients |
| `structural_ar1_quadratic_h16` | current `structural_ar1_quadratic_tf.py` fixture semantics | structural AR(1) stochastic state plus deterministic quadratic completion, simulated horizon-16 observations, density, fixed-noise paths, fixed-ancestor paths, physical gradients |
| `spatial_sir_j3_rk4` | `bayesfilter.highdim.SpatialSIRSSM` | 3-node spatial SIR RK4 transition, infectious-coordinate observation, density and fixed-path value tie-out; gradients only for declared differentiable physical knobs after contract review |
| `predator_prey_rk4` | `bayesfilter.highdim.PredatorPreySSM` | RK4 predator-prey transition with parameter box, Gaussian state/observation noise, density, fixed-path value tie-out, fixed-branch gradients for declared physical knobs |

The old v1 rows may remain as regression rows but cannot be called the
production suite after v2 passes.

## V2 Isolation And Preflight Gates

The v2 program must fail closed unless all of the following are true:

- the P1 manifest contains exactly the six declared v2 model ids and no silent
  omissions;
- P2--P5 use new v2 runners and new v2 artifact names with prefix
  `dpf_common_model_suite_v2_`;
- no v2 runner writes any `dpf_common_*_2026-06-06.json` artifact;
- no v2 runner calls the old three-row `common_model_specs()` API except in
  explicit v1 validation-only checks;
- old v1 runners remain validation-only evidence for closed v1 artifacts and
  cannot be reused as v2 execution;
- closed v1 fixture payloads and checksums remain byte-for-byte stable under
  validation-only commands.

Any violation is a material blocker, not a warning.

## SIR And Predator-Prey Adapter Contract

SIR and predator-prey may only enter BF/FF tie-out execution after a frozen
no-lookup adapter contract certifies exact equality of the FilterFlow
subprocess adapter to the v2 declared semantics.  If this cannot be certified
without mutating `.localsource/filterflow`, the row is classified
`CONTRACT_BLOCKED` before execution.

For `spatial_sir_j3_rk4`, the contract must record:

- state-coordinate convention `(S_1,I_1,...,S_J,I_J)`;
- infectious-only observation route;
- `domain_policy="diagnose_negative_after_noise"`;
- RK4 `delta`, `rk4_internal_step`, and substep count;
- graph/neighbor sets and neighbor Laplacian semantics;
- process, observation, and initial covariance;
- gradient inclusion or exclusion reason.

For `predator_prey_rk4`, the contract must record:

- state-coordinate convention `(prey,predator)`;
- observation as direct noisy state;
- `domain_policy="diagnose_negative_after_noise"`;
- RK4 `delta`, `rk4_internal_step`, and substep count;
- parameter box and chosen physical parameterization;
- process, observation, and initial covariance;
- gradient inclusion or exclusion reason for every candidate knob.

## Evidence Contract

Scientific/engineering question:

Can BayesFilter and executable float64 FilterFlow evaluate the same declared
production-level SSM contracts for values and fixed-branch gradients across a
richer model suite, without treating either implementation as an oracle?

Comparator:

For each v2 row, BayesFilter and FilterFlow execute the same frozen JSON
contract: same dtype, model parameters, observations, initial particles,
transition innovations, fixed ancestor indices, scalar definition, physical
gradient knobs, finite-difference step, and tolerances.

Primary pass criteria:

1. All required density components match within declared tolerance.
2. All required no-resampling path scalars and per-step ledgers match within
   declared tolerance.
3. All required fixed-ancestor path scalars and per-step ledgers match within
   declared tolerance.
4. All required fixed-branch physical gradients match within declared tolerance
   and pass same-implementation finite-difference self-checks.
5. Any non-covered row is explicitly classified as `INTERFACE_BLOCKED`,
   `CONTRACT_BLOCKED`, or `SCIENTIFIC_CONTRACT_BLOCKED` with a concrete reason.

Before P2 begins, P1 must write a frozen pre-run row classification table with
one row per v2 model id.  Initial status must be one of `READY_FOR_P2`,
`INTERFACE_BLOCKED`, `CONTRACT_BLOCKED`, or `SCIENTIFIC_CONTRACT_BLOCKED`.
Density, path, and gradient execution is forbidden for any row not frozen as
ready for that phase.  Any later status change requires a reviewed amendment.

Veto diagnostics:

- missing or mutated v2 contract checksums;
- nonfinite scalar, density, path ledger, or gradient;
- changed fixtures, scalar definitions, tolerances, branch rules, or gradient
  knobs after seeing results without reviewed amendment;
- FilterFlow adapter using a different mathematical model than the v2 contract;
- BayesFilter adapter silently using a different observation path, transition
  mean, covariance, angle wrap, structural completion, domain policy, or
  parameterization;
- any student implementation command before v2 BayesFilter/FilterFlow closure;
- treating BF, FF, students, TT, dense quadrature, paper tables, or simulated
  truth as an oracle.

Explanatory-only diagnostics:

- runtime, wall time, ESS, filtered mean/variance, and finite-difference error
  magnitudes when the primary value/gradient checks pass;
- comparisons to prior v1 artifacts;
- comparisons to standalone fixture checksums after absorption.

Not concluded even if v2 passes:

- no filtering-algorithm correctness proof;
- no paper-scale Zhao--Cui reproduction;
- no TT/SIRT correctness or adaptive MATLAB equivalence;
- no stochastic-resampling distribution correctness;
- no student implementation correctness or failure;
- no HMC, DSGE, GPU, scalability, or production deployment readiness.

Primary artifacts:

- new JSON artifacts under `experiments/dpf_implementation/reports/outputs/`
  with prefix `dpf_common_model_suite_v2_`;
- new markdown reports under `experiments/dpf_implementation/reports/`;
- new result ledgers under `docs/plans/`;
- a v2 manifest recording all model contracts, checksums, runner checksums, and
  retirement status for the three old standalone fixture modules.

Each P2--P5 JSON and markdown report must separate:

- `primary_criterion_fields`;
- `veto_diagnostics`;
- `explanatory_only_fields`.

Only declared scalar/log-normalizer, density, ledger, and gradient equality
fields can determine PASS.  ESS, filtered means, variances, RMSE, runtime, and
finite-difference magnitudes beyond their stated veto role remain explanatory.

Every phase result or repair artifact must include:

- `review_round`;
- `open_material_blockers`;
- `repair_amendment_required`;
- `next_allowed_action`.

If a material blocker persists through the allowed review budget or requires
contract weakening, execution stops.

## Skeptical Plan Audit

Wrong baseline risk:

The goal is BF/FF same-contract consistency, not correctness against FilterFlow,
BayesFilter, TT, dense quadrature, student code, or paper tables.  The plan
therefore uses equality of frozen declared contracts as the criterion and
preserves non-claims.

Proxy-metric risk:

ESS, RMSE, runtime, finite-difference error sizes, and simulation truth are not
promotion criteria.  They can explain or veto only as stated above.

Environment mismatch risk:

All CPU-only TensorFlow commands must set `CUDA_VISIBLE_DEVICES=-1` before
import.  FilterFlow must run from the executable pinned `.localenv/filterflow-py311`
environment and the reference branch marker must be recorded.

Artifact adequacy risk:

Each phase must write a JSON artifact with contract checksums.  A console PASS
without JSON and markdown ledgers is not evidence.

Hidden assumption risk:

SIR and predator-prey currently exist as BayesFilter-side first-gate contracts.
They are not automatically FilterFlow-supported.  V2 may require local
FilterFlow subprocess adapters that directly implement the same declared
density equations.  If an adapter cannot be made without mutating
`.localsource/filterflow`, the row is blocked and must not be forced.

Stale-context risk:

The v1 P1--P6 closeout remains valid only for the closed v1 suite.  V2 is a new
program with new artifacts and cannot inherit v1 PASS status.

Audit decision:

PASS_TO_PLAN.  The plan is executable after Claude/governance review because it
does not change closed artifacts, states a fixed evidence contract, and makes
retirement contingent on passing v2 absorption and tie-out evidence.

## Phases

Phase subplans:

- P0 governance:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p0-governance-subplan-2026-06-07.md`
- P1 declarative spec:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p1-declarative-spec-subplan-2026-06-07.md`
- P2 density tie-out:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p2-density-tieout-subplan-2026-06-07.md`
- P3 no-resampling paths:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p3-noresampling-paths-subplan-2026-06-07.md`
- P4 fixed-ancestor paths:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p4-fixed-ancestor-paths-subplan-2026-06-07.md`
- P5 fixed-branch gradients:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p5-fixed-branch-gradients-subplan-2026-06-07.md`
- P6 retirement and regression:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p6-retirement-regression-subplan-2026-06-07.md`
- P7 terminal student planning:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p7-terminal-student-planning-subplan-2026-06-07.md`

Claude review ledger:

- `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-claude-review-ledger-2026-06-07.md`

### P0. V2 Governance And Retirement Contract

Create a v2 manifest schema covering:

- model ids and families;
- source surfaces absorbed;
- dtype and CPU/GPU policy;
- frozen observations, particles, innovations, ancestors, gradient knobs, and
  tolerances;
- old standalone fixture retirement state;
- non-claims and blocked-state taxonomy.

Exit criteria:

- reviewed v2 manifest schema;
- explicit list of files that may be edited;
- no `.localsource/filterflow` mutation need;
- no student implementation commands.
- P1 six-row model-id gate and P2 pre-run row classification table are defined.
- phase artifacts must include `review_round`, `open_material_blockers`,
  `repair_amendment_required`, and `next_allowed_action`.

### P1. Declarative CommonModelSpec V2

Refactor or extend `common_model_suite_tf.py` so v2 contracts are declarative
rather than runner-hard-coded by `model_id`.

Required fields include:

- model definition payload;
- `theta`;
- density probes;
- path contract: horizon, initial particles, observations, transition
  innovations, transition-mean route, observation-density route;
- fixed-ancestor replay contract;
- gradient contract: physical knob names, initial values, parameterization,
  finite-difference step;
- source/retirement provenance.

Exit criteria:

- v1 functions remain available for old closed runners;
- v1 row definitions, payloads, and checksums remain immutable under
  validation-only commands;
- v2 functions expose all six production rows;
- the v2 manifest row-count/model-id gate fails unless exactly the six declared
  v2 ids are present;
- standalone fixture semantics are absorbed into v2 payloads;
- SIR and predator-prey adapter contracts record all no-lookup semantics listed
  above, or the rows are pre-classified blocked before P2;
- import and manifest tests pass.

### P2. Density Tie-Out

Implement and run a v2 density runner:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_density_tf
```

Exit criteria:

- the pre-run row classification table exists and is frozen before density
  execution;
- BF/FF execute each non-blocked v2 row;
- density component values match within tolerance;
- blocked rows, if any, are classified with concrete reasons.

### P3. No-Resampling Path Tie-Out

Implement and run a v2 fixed-noise no-resampling path runner:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_noresampling_tf
```

Exit criteria:

- scalar predictive log-normalizers and per-step ledgers match for each
  non-blocked row;
- report fields visually and structurally separate primary, veto, and
  explanatory-only quantities;
- no stochastic resampling or RNG equality claim is made.

### P4. Fixed-Ancestor Path Tie-Out

Implement and run a v2 fixed-ancestor replay runner:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_fixed_resampling_tf
```

Exit criteria:

- fixed ancestor replay scalars and ledgers match for each non-blocked row;
- branch replay is frozen before results and checksum-protected.
- report fields visually and structurally separate primary, veto, and
  explanatory-only quantities.

### P5. Fixed-Branch Gradient Tie-Out

Implement and run a v2 fixed-branch gradient runner:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_gradients_tf
```

Required gradient knobs:

- LGSSM: transition-matrix scale and/or observation-noise scale;
- SV: `phi`, `sigma`, and optionally `mu`;
- range-bearing: `sigma_range` and optionally `sigma_bearing`;
- structural AR(1): `rho`, `sigma`, and at least one deterministic-completion
  coefficient such as `c`;
- SIR: reviewed physical knob only if the BF and FF adapter parameterizations
  are identical and stable;
- predator-prey: at least one ODE parameter from `(r,K,a,s,u,v)` inside the
  declared box.

Exit criteria:

- BF and FF gradients match within tolerance for each non-blocked required
  knob;
- each implementation passes its finite-difference self-check;
- any gradient-excluded knob is classified before seeing result values.

### P6. Retirement And Regression Gate

Only after P1--P5 pass or classify all rows, retire the old standalone fixture
modules from the production path.

Retirement actions:

- remove production-runner imports of `lgssm_tf.py`, `stochastic_volatility_tf.py`,
  and `range_bearing_tf.py`;
- write an import inventory ledger with classes:
  `production_v2_imports_forbidden`, `legacy_v1_validation_allowed`,
  `reference_only_allowed`, and `nonproduction_research_runner_allowed`;
- mark the files as `RETIRED_BY_V2_COMMON_SUITE` in a result ledger, or delete
  them only if a reviewed cleanup amendment says deletion is safe;
- keep v1 closed artifacts unchanged;
- run v1 validation-only commands to prove old evidence can still be read;
- run v2 manifest validation.

Exit criteria:

- no production v2 runner depends on the retired modules; retirement PASS does
  not require zero repo-wide imports;
- old closed v1 JSON artifacts validate;
- old validation commands validate against original v1 checksums and artifact
  schema;
- new v2 JSON artifacts validate;
- retirement ledger records source checksums and successor v2 model ids.

### P7. Terminal Student Repetition Planning

Student work remains out of scope until v2 BF/FF closure.

Exit criteria:

- write a separate reviewed student adapter plan only after v2 P0--P6 close;
- only static adapter/runner inventory inspection is allowed;
- do not run student filter, density, path, gradient, validation, or
  derived-metric commands in this v2 BF/FF program.

## Claude Review Loop

Before implementation, run Claude review on this plan and patch material
blockers until PASS/convergence or max five rounds.

During execution, each phase result receives Claude result/governance review.
For fixable blockers, write a repair amendment, review it, implement only the
reviewed repair, rerun evidence, and update the ledgers.

Stop only for:

- human-intervention blocker;
- exhausted Claude review with unresolved material blocker;
- unavailable required infrastructure;
- need to mutate `.localsource/filterflow`;
- scientific-contract change.

## Initial File Scope

Allowed implementation files:

- `experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py`
- new v2 runners under `experiments/dpf_implementation/tf_tfp/runners/`
- focused tests under `tests/` or `tests/highdim/`
- v2 reports under `experiments/dpf_implementation/reports/`
- v2 JSON artifacts under `experiments/dpf_implementation/reports/outputs/`
- v2 docs/results under `docs/plans/`

Do not edit or delete `.localsource/filterflow` in this program.

## Launch Prompt

Execute the DPF common model suite v2 production master plan:

`docs/plans/bayesfilter-dpf-common-model-suite-v2-production-master-plan-2026-06-07.md`

First run Claude review on the plan, patch material blockers until
PASS/convergence or max five rounds, then execute P0 through P7 under the stated
state machine.  Preserve all v1 closed artifacts.  Do not run student
implementation commands before v2 BF/FF closure.  Do not mutate
`.localsource/filterflow`.  Use `CUDA_VISIBLE_DEVICES=-1` for CPU-only
TensorFlow runs and preserve JSON artifacts, markdown ledgers, checksums, and
non-claims.
