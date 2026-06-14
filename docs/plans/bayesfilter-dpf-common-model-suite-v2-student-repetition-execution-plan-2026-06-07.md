# DPF Common Model Suite V2 Student Repetition Execution Plan

metadata_date: 2026-06-07
status: DRAFT_PENDING_CLAUDE_REVIEW

## Question

After the BayesFilter/FilterFlow V2 production tie-out has closed through P7,
can the same frozen density, deterministic path, fixed-ancestor path, and
fixed-branch-gradient contracts be applied to the two quarantined student
repositories, with every cell classified without treating any implementation as
an oracle?

## Skeptical Audit

Status: `PASS_WITH_CONSERVATIVE_EXECUTION_BOUNDARY`.

Wrong-baseline risk:

- the old student baseline panels use different fixtures, stochastic runs,
  Kalman/proxy metrics, and implementation-specific likelihoods;
- they must not be promoted into V2 equality evidence.

Proxy-metric risk:

- RMSE, ESS, runtime, stochastic particle summaries, FD diagnostics, and
  implementation-specific likelihoods are explanatory only.

Hidden-assumption risk:

- a student cell can be `MATCHED` only when the mathematical model, scalar,
  particles, observations, innovations, ancestor schedule, dtype, tolerance,
  and parameterization are the frozen V2 contract;
- otherwise it must be `EXPLAINED_MISMATCH`, `INTERFACE_BLOCKED`, or
  `OUT_OF_SCOPE`.

Command-answer risk:

- running a broad student panel would answer a different question;
- the execution command must instead read the closed V2 artifacts, inspect the
  student adapter surfaces, and execute only exact/replayable student cells.

## Evidence Contract

Primary comparator:

- frozen V2 artifacts:
  - `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_manifest_2026-06-07.json`;
  - `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_density_2026-06-07.json`;
  - `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_noresampling_2026-06-07.json`;
  - `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_fixed_resampling_2026-06-07.json`;
  - `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_gradients_2026-06-07.json`.

Student implementations:

- `advanced_particle_filter` vendored under
  `experiments/student_dpf_baselines/vendor/advanced_particle_filter`;
- `2026MLCOE` vendored under
  `experiments/student_dpf_baselines/vendor/2026MLCOE`.

Primary pass criterion:

- every implementation/model/surface cell is terminally classified as
  `MATCHED`, `EXPLAINED_MISMATCH`, `INTERFACE_BLOCKED`, or `OUT_OF_SCOPE`;
- `MATCHED` requires all declared primary values within the frozen V2
  tolerance and no unreviewed fixture/scalar/branch/parameterization change;
- `EXPLAINED_MISMATCH` requires a concrete source-level or contract-level
  reason preserved in the artifact;
- interface blocking is not a student failure.

Diagnostics that can veto:

- V2 BF/FF closure artifacts missing;
- a student output used to revise the frozen V2 comparator;
- BayesFilter, FilterFlow, either student repo, TT/SIRT, dense quadrature,
  simulated truth, or paper tables treated as an oracle;
- tolerance, fixture, scalar, branch, comparator, or gradient-contract change
  after seeing student results without reviewed amendment;
- FD used as a gate;
- unclassified executed discrepancy;
- student command run before this plan passes Claude review;
- CPU-only TensorFlow run without pre-import `CUDA_VISIBLE_DEVICES=-1`.

Explanatory-only diagnostics:

- per-cell deltas, FD diagnostics, ESS/moment fields, stochastic proxy panels,
  source-code line notes, branch timing notes, adapter checksums, and command
  stderr.

Not concluded even if the run passes:

- no filter correctness proof;
- no claim that BayesFilter, FilterFlow, or either student repository is
  scientifically correct;
- no stochastic-resampling distribution claim;
- no differentiable-resampling claim;
- no TT/SIRT, paper-table, GPU, HMC, DSGE, scalability, deployment, or
  production-readiness claim.

## Planned Phases

S0 governance and review:

- Claude reviews this plan until PASS/convergence or max five rounds;
- material blockers are patched before execution.

S1 adapter-surface dry classification:

- inspect current student adapters and vendored model/filter surfaces;
- freeze adapter/source checksums;
- predeclare runnable cells before comparing results.

S2 density:

- run density components only where the student surface exposes the same
  density semantics or a clearly declared adapter-derived density from student
  model attributes;
- otherwise classify as `INTERFACE_BLOCKED` or `OUT_OF_SCOPE`.

S3 deterministic no-resampling path:

- run exact replay only where fixed initial particles, fixed transition
  innovations, observations, scalar, and log-weight semantics can be forced
  without editing vendored code.

S4 fixed-ancestor path:

- run exact replay only where fixed ancestor indices and branch timing can be
  mapped before execution;
- any timing map must be declared in the artifact and may not change after
  seeing results.

S5 fixed-branch AD gradients:

- run only if an exact differentiable fixed-branch physical-knob scalar is
  exposed;
- FD remains diagnostic-only and cannot pass or fail a gradient cell.

S6 closeout:

- write machine-readable JSON, markdown report, result ledger, command
  manifest, decision table, and non-claims.

## Planned Command

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_student_repetition_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_student_repetition_tf --validate-only
```

## Planned Artifacts

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_student_repetition_2026-06-07.json`
- report:
  `experiments/dpf_implementation/reports/dpf-common-model-suite-v2-student-repetition-2026-06-07.md`
- result ledger:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-student-repetition-execution-result-2026-06-07.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-student-repetition-execution-claude-review-ledger-2026-06-07.md`

## Predeclared Runnable Surface

Before student results are inspected, the only currently runnable exact/replay
surface identified from the adapters is:

- `advanced_particle_filter`, `lgssm_2d_h25_rich`, density and deterministic
  no-resampling particle-filter replay through its NumPy LGSSM and bootstrap
  particle-filter code.  The replay adapter must supply standard-normal noises
  which, after APF's own Cholesky factors, reproduce the frozen V2 initial
  particles and transition innovations; it must not pass particles as if they
  were noises.

Known conservative blockers before execution:

- `advanced_particle_filter` bootstrap resampling occurs after the measurement
  update, whereas the frozen V2 fixed-ancestor path branches at the start of
  the step before propagation; fixed-ancestor is therefore interface-blocked
  until a branch-timing adapter/amendment is reviewed;
- `advanced_particle_filter` range-bearing uses Student-t observation noise in
  its exposed range-bearing model, whereas V2 range-bearing is Gaussian;
- `advanced_particle_filter` SVSSM/DPF surfaces do not expose the V2 scalar and
  fixed branch replay contract;
- `advanced_particle_filter` does not expose structural AR(1), spatial SIR, or
  predator-prey V2 models;
- `2026MLCOE` current adapters expose LGSSM KF/BPF and separate nonlinear
  proxy models but not the V2 density/path/fixed-ancestor/gradient scalar
  surfaces;
- neither repository currently exposes the V2 fixed-branch AD-gradient
  contract.

## Exit Gate

The phase closes only when every cell has a terminal classification, all
executed discrepancies are explained, Claude result/governance review has no
material blocker, and the result ledger preserves the non-claims.
