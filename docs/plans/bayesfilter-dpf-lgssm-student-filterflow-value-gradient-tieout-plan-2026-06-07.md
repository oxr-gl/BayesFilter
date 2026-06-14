# DPF LGSSM Student/FilterFlow Value and Gradient Tie-Out Plan

metadata_date: 2026-06-07
status: DRAFT_READY_FOR_REVIEW

## Question

For the LGSSM row only, can the two quarantined student implementations expose
value and gradient surfaces that match the already closed FilterFlow-side V2
contracts, and if they do not match, can we classify the reason without treating
FilterFlow, BayesFilter, or either student repository as an oracle?

Student implementations:

- `advanced_particle_filter`, source commit
  `d2a797c330e11befacbb736b5c86b8d03eb4a389`;
- `2026MLCOE`, source commit
  `020cfd7f2f848afa68432e95e6c6e747d3d2402d`.

Frozen V2 LGSSM comparator artifacts:

- density:
  `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_density_2026-06-07.json`;
- no-resampling path:
  `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_noresampling_2026-06-07.json`;
- fixed-ancestor path:
  `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_fixed_resampling_2026-06-07.json`;
- fixed-branch gradient:
  `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_gradients_2026-06-07.json`.

## Skeptical Plan Audit

Status: `PASS_WITH_EXPLICIT_CONTRACT_BOUNDARIES`.

Wrong-baseline risk:

- the old student baseline panels use stochastic fixtures, Kalman/proxy
  quantities, and implementation-specific likelihood definitions;
- they must not be used as equality evidence against FilterFlow V2 artifacts.

Proxy-metric risk:

- Kalman RMSE, ESS, posterior means, runtime, finite differences, and stochastic
  replay diagnostics are explanatory only unless the exact scalar contract is
  stated before execution.

Hidden-assumption risk:

- `advanced_particle_filter` adds hard-coded `1e-8` covariance jitter to
  `P0`, `Q`, and `R`;
- `2026MLCOE` BPF uses internal random draws, omits Gaussian normalizing
  constants in its BPF observation log-likelihood, and does not expose a PF
  log-normalizer scalar through its current adapter;
- neither implementation should be called buggy merely because it does not
  expose the frozen V2 contract.

Gradient-risk audit:

- FilterFlow/BayesFilter V2 LGSSM gradient knobs are
  `transition_matrix_scale` and `observation_noise_scale`;
- finite differences are diagnostic-only and never a gate;
- a student value match must not excuse a gradient mismatch;
- a student gradient cell is executable only if the scalar, random/fixed
  branch, parameterization, and autodiff path are all predeclared.

Command-answer risk:

- running a broad student panel would answer a different question;
- the implementation must run an LGSSM-only runner that reads the closed V2
  artifacts and records a terminal classification for each student/surface.

## Evidence Contract

Primary comparator:

- closed local FilterFlow-side V2 LGSSM artifacts, under the same frozen
  fixture, dtype, particles, observations, innovations, ancestor schedule,
  scalar definitions, and gradient knobs used in P2--P5.

Primary pass criterion:

- every LGSSM student/surface cell is terminally classified as `MATCHED`,
  `EXPLAINED_MISMATCH`, `INTERFACE_BLOCKED`, or `OUT_OF_SCOPE`;
- `MATCHED` requires the predeclared student scalar/gradient to equal the
  frozen FilterFlow V2 scalar/gradient within the frozen V2 tolerance;
- `EXPLAINED_MISMATCH` requires a concrete source-level or contract-level
  reason, with line references where practical;
- `INTERFACE_BLOCKED` is not a student failure.

Veto diagnostics:

- using student output to revise FilterFlow/BayesFilter V2 comparators;
- tolerance, fixture, scalar, branch, comparator, or gradient-contract changes
  after seeing student results without reviewed amendment;
- FD used as a value or gradient gate;
- stochastic student runs promoted as deterministic equality evidence;
- hidden RNG or random ancestor selection inside a claimed fixed-branch
  gradient cell;
- nonfinite scalar or AD gradient in an executed cell;
- unclassified executed discrepancy;
- CPU-only TensorFlow run without pre-import `CUDA_VISIBLE_DEVICES=-1`;
- vendored student source mutation.

Explanatory-only diagnostics:

- same-implementation finite differences;
- Kalman exact likelihood comparisons;
- APF no-jitter/jitter decomposition probes;
- MLCOE missing-constant decomposition probes;
- ESS, means, variances, resampling counts, runtime, and TensorFlow CUDA
  import stderr in CPU-only runs.

Not concluded even if all executable cells match:

- no filter correctness proof;
- no claim that FilterFlow, BayesFilter, APF, or MLCOE is scientifically
  correct;
- no stochastic-resampling distribution claim;
- no differentiable-resampling claim;
- no TT/SIRT, paper-table, GPU, HMC, DSGE, scalability, deployment, or
  production-readiness claim.

## Surfaces to Test

Strict V2 surfaces:

1. `density_components`: initial, transition, observation, and scalar density
   probes for `lgssm_2d_h25_rich`.
2. `noresampling_path`: deterministic fixed initial particles and fixed
   transition innovations, no resampling.
3. `fixed_ancestor_path`: deterministic fixed initial particles, fixed
   transition innovations, and fixed ancestor indices under the V2 branch
   timing.
4. `fixed_branch_gradient`: fixed-branch scalar and AD gradients for
   `transition_matrix_scale` and `observation_noise_scale`.

Diagnostic student-native mirrors:

- `apf_jittered_density_mirror`: a neutral local mirror of APF's documented
  `+1e-8 I` covariance jitter, used only to localize APF strict-V2 deltas;
- `mlcoe_weight_only_likelihood_mirror`: a neutral local mirror of MLCOE BPF's
  `-0.5 * quadratic` weight update without Gaussian constants, used only to
  localize missing-constant deltas;
- these mirrors cannot create `MATCHED` status against strict V2.  They can
  only support `EXPLAINED_MISMATCH`.

## Predeclared Hypotheses

H1. APF strict density values will not match V2 at `5e-10` because APF adds
`1e-8` covariance jitter in its Gaussian covariance Cholesky factors.

H2. APF strict no-resampling particles can replay exactly when the adapter
supplies standard-normal noises transformed by APF's own Cholesky factors, but
log-normalizers and weights will differ at about the jitter scale.

H3. APF fixed-ancestor path is interface-blocked unless a reviewed adapter can
map the V2 pre-propagation branch timing to APF's post-measurement resampling
timing without changing the scalar contract.

H4. APF fixed-branch AD gradient is interface-blocked unless an exact
parameterized LGSSM scalar is exposed without detaching parameters through
`tf.constant` construction and without substituting the SV/HMC differentiable
PF contract for the V2 LGSSM contract.

H5. MLCOE strict density/path value surfaces are interface-blocked or explained
mismatches unless an adapter exposes the V2 Gaussian constants, fixed particles,
fixed innovations, log-normalizer scalar, and branch timing.

H6. MLCOE fixed-branch AD gradient is interface-blocked unless an exact
LGSSM fixed-branch scalar with the V2 knobs can be expressed through its current
TensorFlow code without hidden random draws or nondifferentiated mutable state.

## Phases

### P0. Governance and Plan Review

Tasks:

- review this plan with Claude until `PASS` or max five rounds;
- patch material plan blockers before running any student command;
- record the review in
  `docs/plans/bayesfilter-dpf-lgssm-student-filterflow-value-gradient-tieout-claude-review-ledger-2026-06-07.md`.

Gate:

- no student LGSSM evidence command runs before the plan review passes.

### P1. Static Interface Inventory

Tasks:

- inspect APF NumPy LGSSM, APF TF LGSSM, APF TF/NumPy PF, MLCOE LGSSM/KF/BPF,
  and MLCOE DPF/PHMC surfaces;
- record source file checksums and line-level notes for jitter, constants,
  RNG, resampling timing, scalar exposure, and AD parameter flow;
- predeclare which strict V2 surfaces are executable before comparing values.

Gate:

- all cells have a pre-execution status candidate:
  `RUNNABLE_STRICT_V2`, `RUNNABLE_DIAGNOSTIC_ONLY`, or `INTERFACE_BLOCKED`.

### P2. Strict V2 Value Tie-Out

Tasks:

- run only `RUNNABLE_STRICT_V2` value cells against the frozen FilterFlow V2
  LGSSM density and no-resampling/fixed-ancestor artifacts;
- preserve per-component deltas, scalar deltas, particle/weight/log-normalizer
  deltas, and source-level mismatch reasons.

Expected executable cells before P1 confirmation:

- APF NumPy LGSSM density;
- APF NumPy bootstrap no-resampling replay.

Expected blocked cells before P1 confirmation:

- APF fixed-ancestor under strict V2 branch timing;
- MLCOE BPF strict fixed-particle/fixed-innovation scalar.

Gate:

- every value cell is `MATCHED`, `EXPLAINED_MISMATCH`, or
  `INTERFACE_BLOCKED`;
- no stochastic proxy panel is promoted.

### P3. Student-Native Value Localization

Tasks:

- for strict value mismatches, run diagnostic-only localization mirrors:
  APF `+1e-8 I` jitter mirror and MLCOE missing-Gaussian-constant mirror where
  applicable;
- record whether the diagnostic mirror explains the observed strict-V2 delta.

Gate:

- diagnostics may support explanations but cannot turn a strict mismatch into
  a strict match.

### P4. Strict V2 Gradient Tie-Out

Tasks:

- test only exact LGSSM fixed-branch AD-gradient cells with the V2 scalar:
  fixed initial particles, fixed innovations, fixed ancestor schedule, V2
  branch timing, and knobs `transition_matrix_scale` and
  `observation_noise_scale`;
- reject any cell with hidden RNG, random resampling, differentiable-resampling
  substitution, detached parameters, or different scalar.

Expected status before P1 confirmation:

- APF gradient likely `INTERFACE_BLOCKED` because TF LGSSM builders store
  parameters as constants and APF differentiable PF is SV/HMC-oriented rather
  than the V2 LGSSM fixed-branch scalar;
- MLCOE gradient likely `INTERFACE_BLOCKED` because its BPF/DPF surfaces do not
  expose the V2 fixed-branch log-normalizer scalar or knobs.

Gate:

- an executable gradient cell must match both scalar and AD gradients within
  tolerance;
- FD remains diagnostic-only.

### P5. Result and Governance Review

Tasks:

- write JSON, markdown report, result ledger, command manifest, and decision
  table;
- run Claude result/governance review until `PASS` or max five rounds;
- if Claude finds a material blocker, create a reviewed repair amendment before
  rerunning evidence.

Gate:

- close only after every LGSSM student/surface cell is terminally classified
  and the Claude result/governance review passes.

## Planned Artifacts

Plan:

- `docs/plans/bayesfilter-dpf-lgssm-student-filterflow-value-gradient-tieout-plan-2026-06-07.md`

Claude review ledger:

- `docs/plans/bayesfilter-dpf-lgssm-student-filterflow-value-gradient-tieout-claude-review-ledger-2026-06-07.md`

Runner:

- `experiments/dpf_implementation/tf_tfp/runners/run_lgssm_student_filterflow_value_gradient_tieout_tf.py`

JSON:

- `experiments/dpf_implementation/reports/outputs/dpf_lgssm_student_filterflow_value_gradient_tieout_2026-06-07.json`

Report:

- `experiments/dpf_implementation/reports/dpf-lgssm-student-filterflow-value-gradient-tieout-2026-06-07.md`

Result ledger:

- `docs/plans/bayesfilter-dpf-lgssm-student-filterflow-value-gradient-tieout-result-2026-06-07.md`

## Planned Commands

Plan review:

```bash
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name lgssm-student-tieout-plan-review --model sonnet --effort high "Review docs/plans/bayesfilter-dpf-lgssm-student-filterflow-value-gradient-tieout-plan-2026-06-07.md for scientific-contract weakening, oracle misuse, FD-as-gate risk, student proxy panel leakage, stale V2 artifact assumptions, gradient-contract ambiguity, and missing stop conditions. Return PASS or BLOCKED."
```

Evidence after review:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_student_filterflow_value_gradient_tieout_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_student_filterflow_value_gradient_tieout_tf --validate-only
```

## Decision Table Template

| Decision | Primary criterion | Veto status | Main uncertainty | Next action | Not concluded |
|---|---|---|---|---|---|
| TBD | every LGSSM student/surface cell terminally classified; executable strict V2 cells match or have explained mismatch | TBD | student adapters may not expose exact V2 scalar/gradient surfaces | TBD | no correctness, oracle, stochastic-resampling, differentiable-resampling, or production claim |

## Stop Conditions

Stop for human review if:

- a strict V2 match would require changing V2 fixtures, tolerances, scalar,
  branch timing, comparator, or gradient knobs;
- a student gradient would require editing vendored student code;
- a diagnostic mirror starts being used as strict match evidence;
- Claude review remains blocked after five rounds;
- required infrastructure is unavailable.
