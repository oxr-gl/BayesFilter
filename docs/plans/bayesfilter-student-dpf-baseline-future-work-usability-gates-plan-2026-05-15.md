# Plan: student DPF future-work usability gates

## Date

2026-05-15

## Status

Draft master-program revision and phase plan for the quarantined student DPF
experimental-baseline lane.

MP8 remains closed as
`student_dpf_baseline_program_complete_with_caveats`.  This document is a new
student-lane master revision for future-work usability gates, created only
because the user explicitly requested follow-up on stochastic flow, DPF/dPFPF,
neural OT, and differentiable resampling.  It does not reopen MP5-MP8, weaken
their caveats, or authorize production use.

Execution of this plan is subordinate to the lane boundaries and stop rules
below.  If any phase conflicts with MP8 caveats, MP8 wins and this plan stops.

## Scope

This plan tests whether the remaining future-work families can move from
`importable surface` to bounded student-lane evidence:

- differentiable resampling;
- stochastic flow;
- DPF and dPFPF;
- neural OT / amortized resampling.

Here, `usable` means:

- a small CPU-only command can import and execute one bounded component or
  filter smoke gate;
- outputs are finite or fail as structured blockers;
- metrics, artifact requirements, assumptions, and model contracts are
  explicit;
- the result can inform a later BayesFilter-owned clean-room specification.

`Usable` does not mean production-ready, correctness-certified, publication
evidence, or safe to copy into production.

## Lane Boundary

Allowed write set:

- `docs/plans/bayesfilter-student-dpf-baseline-*`;
- `experiments/student_dpf_baselines/runners/`;
- `experiments/student_dpf_baselines/reports/`;
- `experiments/student_dpf_baselines/reports/outputs/`;
- `docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md`,
  only for a short addendum that records this requested master-program
  revision and final result label.

Forbidden:

- production `bayesfilter/`;
- `docs/chapters/`;
- `docs/references.bib`;
- monograph plans, monograph reset memos, and reviewer-grade monograph files;
- `experiments/student_dpf_baselines/vendor/`;
- `experiments/controlled_dpf_baseline/`, except read-only comparison to
  existing clean-room artifacts if needed;
- broad dependency installs, GPU-only runs, network/API calls, notebook
  conversion, training jobs, HMC chains, or long experiments.

No commit or push is authorized by this plan.

## Motivation

The MP4 readiness review found 28 importable flow/DPF-related surfaces.  Only
the deterministic EDH/PFPF family advanced into bounded comparison and later
clean-room baseline work.  The remaining families are important for future
BayesFilter work, but MP4 explicitly classified them as requiring separate
reproduction gates.

This plan therefore does not run a broad mixed-family panel.  It executes
family-specific gates in increasing dependency/risk order:

1. contract and artifact audit;
2. non-neural differentiable resampling component gate;
3. neural OT and neural-resampling artifact/API gate;
4. stochastic-flow reduced gate;
5. DPF/dPFPF contract-conditional smoke gate;
6. final readiness map and clean-room recommendations.

Each family is an independent reproduction gate.  A pass, failure, blocker, or
defer decision in one family does not validate, reopen, advance, or weaken the
classification of any other family.  Later phases may continue after an earlier
family-specific blocker only to classify a different family, and only if no
environment-wide veto diagnostic fired.

## Classification Labels

Every probe must end with one of:

- `usable_for_clean_room_spec`: bounded run succeeded and the semantics are
  clear enough for a future clean-room spec;
- `usable_component_only`: bounded component run succeeded, but it is not yet a
  filter-level or algorithm-level gate;
- `api_smoke_only`: constructor or forward API ran, but training/artifact
  status or target semantics are too weak for usability claims;
- `blocked_missing_artifact`: required checkpoint, weights, data, or trained
  state is missing;
- `blocked_missing_assumption`: model, shape, hidden-state, likelihood, or
  target semantics are unavailable or ambiguous;
- `blocked_runtime_or_memory`: bounded execution exceeds the local cap or would
  require unbounded/GPU-scale execution;
- `blocked_environment_drift`: local TF/TFP/NumPy/Python behavior prevents the
  run;
- `not_comparable_without_new_target`: a path can run but has no matched target
  or metric contract.

Untrained neural paths cannot receive `usable_for_clean_room_spec` or
`usable_component_only`.  They can receive only `api_smoke_only` or a blocker
unless training artifacts and target semantics are present and recorded.

## Required Artifact Schema

Each JSON record must include:

- `schema_version`;
- `date`;
- `phase`;
- `gate_phase`;
- `gate_name`;
- `family`;
- `probe_id`;
- `planned_probe`;
- `implementation_name`;
- `source_commit`;
- `command`;
- `working_directory`;
- `fixture_or_input`;
- `seed`;
- `runtime_seconds`;
- `status`;
- `classification`;
- `blocker_class`;
- `blocker_message`;
- `artifact_dependency_status`;
- `model_contract_status`;
- `contract_satisfiable_without_vendor_edits`;
- `execution_attempted`;
- `prohibited_actions_avoided`;
- `metrics`;
- `assumptions`;
- `provenance`;
- `next_decision`.

The summary JSON must include:

- records expected and observed;
- status counts;
- classification counts;
- planned probe inventory by family and path;
- observed record inventory by family and path;
- missing planned probes, which must be an empty list for validation success;
- family decisions;
- artifact size bytes;
- whether any veto diagnostic fired;
- final label.

## Primary Hypotheses

### H1: Non-neural differentiable resampling is the easiest usable component

Advanced soft and Sinkhorn resamplers and MLCOE soft and Sinkhorn resamplers
can run on a tiny weighted particle cloud with finite output particles,
normalized/reset weights, and local gradient smoke where applicable.

### H2: Neural OT is artifact-dependent and must be classified conservatively

Advanced amortized OT is usable only if its bundled checkpoint restores locally
and a tiny forward/gradient smoke succeeds.  MLCOE transformer resampling is an
untrained neural API smoke unless trained weights and target semantics are
available.

### H3: Stochastic flow needs a mandatory reduced gate

Advanced stochastic PFF/PFPF and MLCOE stochastic-flow surfaces may run on a
short-horizon Gaussian range-bearing fixture only with mandatory lightweight
settings and per-probe runtime caps.

### H4: DPF/dPFPF usability depends on an adapter-free model-contract audit

Advanced TensorFlow DPF and MLCOE DPF/dPFPF can be probed only after their
required transition, observation, state, hidden-state, resampling, and gradient
contracts are documented and judged satisfiable without vendored edits.

## Execution Phases

### FW0: Plan Review And Audit

Actions:

1. Read this plan against the MP4 readiness result, MP8 closeout, and existing
   student-lane runners.
2. Ask Claude Code, through the supervised wrapper, for a read-only critical
   review.
3. Codex audits Claude's review and revises this plan until both agents accept
   it as executable.

Exit criterion:

- Claude returns `ACCEPT`, and Codex agrees no blocker remains.

Veto diagnostics:

- plan requires production, monograph, vendored, GPU, network, training, HMC,
  or broad dependency work;
- plan claims production readiness or correctness from student evidence;
- plan lacks structured blocker classes for non-runnable paths.

### FW1: Contract And Artifact Audit

Actions:

1. Create a bounded runner:
   `experiments/student_dpf_baselines/runners/run_future_work_usability_gates.py`.
2. In the runner, first inspect and record contract readiness for each family
   before running any family-specific probe.
3. Record:
   - import path;
   - constructor signature;
   - callable method signature;
   - required model fields;
   - required hidden state shape;
   - required artifact/checkpoint path;
   - whether a tiny adapter-owned input can satisfy the contract without
     vendored edits.
4. For every planned path, record the explicit verdict
   `contract_satisfiable_without_vendor_edits = yes/no`.
5. If the verdict is `no`, record exact missing contract fields or artifacts in
   `blocker_message` before any execution probe is attempted.

Primary criterion:

- every planned future-work family receives a contract and artifact readiness
  record before execution probes.

Veto diagnostics:

- a family requires vendored edits to instantiate;
- a family requires training, notebook conversion, HMC, GPU, or network access
  to establish contract readiness.

### FW2: Non-Neural Differentiable Resampling Component Gate

Actions:

1. Use a fixed tiny particle cloud:
   - batch dimension where required: `B=1`;
   - particle count: `N=8`;
   - state dimension: `D=2`;
   - fixed seed: `20260515`;
   - nonuniform normalized weights.
2. Probe only non-neural resampling components:
   - advanced `tf_utils.soft_resampler.soft_resample`;
   - advanced `tf_utils.sinkhorn.sinkhorn_resample`, with at most 5 Sinkhorn
     iterations;
   - MLCOE `SoftResampler`;
   - MLCOE `SinkhornResampler`, with at most 5 Sinkhorn iterations.
3. Record:
   - output shape;
   - finite outputs;
   - weight normalization or uniform reset;
   - approximate weighted-mean preservation where applicable;
   - finite local gradient flag if a TensorFlow gradient tape can compute it
     without training.

Primary criterion:

- every non-neural resampling component returns finite outputs or a structured
  blocker.

Next-phase gate:

- continue to FW3 if all FW2 probes are represented and no environment-wide
  TensorFlow failure occurs.

### FW3: Neural OT And Neural-Resampling Artifact/API Gate

Actions:

1. Check advanced bundled amortized-OT checkpoint paths before construction.
2. If the checkpoint exists, run advanced
   `tf_utils.amortized_resampler.AmortizedOTResampler` on `B=1`, `N=8`, `D=2`.
3. Probe MLCOE `TransformerResampler` as API smoke only, because no trained
   weights or target semantics are recorded in the student-lane evidence.
4. Do not train, download, convert notebooks, or run HMC.

Primary criterion:

- advanced amortized OT is classified as `usable_component_only`,
  `blocked_missing_artifact`, `blocked_runtime_or_memory`, or
  `blocked_environment_drift`;
- MLCOE transformer resampling is classified only as `api_smoke_only` or a
  blocker.

Next-phase gate:

- continue to FW4 if all neural probes are represented and no unbounded action
  is required.

### FW4: Stochastic Flow Reduced Gate

Actions:

1. Use the existing Gaussian range-bearing fixture.
2. Run reduced horizon only:
   - fixture: `range_bearing_gaussian_moderate`;
   - horizon: `4`;
   - particles: `16`;
   - flow steps: at most `3`;
   - seed: `20260515`.
3. Mandatory advanced settings:
   - `beta_schedule="linear"`;
   - no optimal BVP;
   - `Q_flow_mode="fixed"`;
   - small diagonal `Q_flow_fixed`;
   - `integration_method="euler"` or another explicitly bounded method;
   - per-probe runtime warning at 10 seconds and local subprocess timeout at
     30 seconds if a subprocess wrapper is used.
4. Probe advanced `StochasticPFFlow` and `StochasticPFParticleFilter`.
5. Probe MLCOE stochastic-flow surfaces only if FW1 contract audit says the
   model contract is satisfiable without vendored edits.  Otherwise record
   `blocked_missing_assumption`.
6. Record:
   - finite means or particles;
   - position RMSE proxy if a trajectory mean is available;
   - ESS and resampling count if exposed;
   - exact lightweight settings used.

Primary criterion:

- each stochastic-flow candidate runs under mandatory lightweight settings or
  receives a structured blocker.

Next-phase gate:

- continue to FW5 unless FW4 reveals an environment-wide failure that would
  invalidate DPF/dPFPF probes.

### FW5: DPF And dPFPF Contract-Conditional Smoke Gate

Actions:

1. Execute only probes whose FW1 contract audit says the required model and
   hidden-state contract can be supplied without vendored edits.
2. Probe advanced `TFDifferentiableParticleFilter` with:
   - `resampler="soft"`;
   - `resampler="sinkhorn"` with very small `N`, short horizon, and at most 5
     Sinkhorn iterations;
   - `resampler="amortized"` only if FW3 confirmed advanced amortized OT.
3. Probe MLCOE `DPF` with `method="soft"` and `method="sinkhorn"` only if a
   tiny transition/observation contract is available.
4. Probe MLCOE `DifferentiablePFPF` only if FW1 confirms required model fields
   for `EDHSolver`, covariance, observation, and resampling contracts.
5. Use finite-output and gradient-smoke metrics only.
6. Do not run HMC or any parameter-inference chain.
7. Probes are forbidden unless the per-path FW1 verdict
   `contract_satisfiable_without_vendor_edits` is `yes`.  If the verdict is
   `no`, classify the path immediately as `blocked_missing_assumption` or
   `blocked_missing_artifact` with `execution_attempted = false`.

Primary criterion:

- DPF/dPFPF paths are classified into usable filter-level smoke,
  usable component-only, or structured blocker classes.

Next-phase gate:

- continue to FW6 if all planned DPF/dPFPF paths are classified and no
  unbounded command was required.

### FW6: Classification, Clean-Room Recommendation, And Reset Memo

Actions:

1. Write machine-readable outputs:
   - `experiments/student_dpf_baselines/reports/outputs/future_work_usability_gates_2026-05-15.json`;
   - `experiments/student_dpf_baselines/reports/outputs/future_work_usability_gates_summary_2026-05-15.json`.
2. Write a Markdown report:
   - `experiments/student_dpf_baselines/reports/student-dpf-baseline-future-work-usability-gates-result-2026-05-15.md`.
3. Update the student reset memo with:
   - phase result;
   - interpretation;
   - remaining blockers;
   - which families, if any, justify a clean-room specification.
4. Add a short addendum to the student master program recording this requested
   post-MP8 master revision and its final result label.

Primary criterion:

- each future-work family has a concrete next decision:
  `clean_room_spec_next`, `component_spec_next`, `debug_gate_next`, or
  `defer_until_artifacts_or_assumptions`.

## Required Validation

Run after implementation:

```bash
python -m py_compile experiments/student_dpf_baselines/runners/run_future_work_usability_gates.py
python -m experiments.student_dpf_baselines.runners.run_future_work_usability_gates
python -m experiments.student_dpf_baselines.runners.run_future_work_usability_gates --validate-only
rg -n "experiments/student_dpf_baselines|advanced_particle_filter|2026MLCOE" bayesfilter tests
git diff --check -- docs/plans/bayesfilter-student-dpf-baseline-* experiments/student_dpf_baselines/runners experiments/student_dpf_baselines/reports
```

Expected:

- py_compile passes;
- runner exits normally;
- validate-only confirms every planned probe has a record and classification;
- validate-only reconciles the plan's declared probe inventory against observed
  records family-by-family and path-by-path, with zero silent omissions;
- every non-`ok` path has `blocker_class` and `blocker_message`;
- JSON outputs include `schema_version`;
- generated artifact sizes are recorded and suitable for normal repository
  history;
- no `usable_*` label appears for untrained or checkpoint-missing neural paths;
- no production or normal-test imports from student-lane code;
- no whitespace errors in the student-lane diff.

## Stop Rules

Stop and record a blocker if:

- a probe requires vendored-code edits;
- a probe requires production or monograph edits;
- a probe requires network, GPU, live API, notebook conversion, broad
  dependency installation, training, HMC, or unbounded runtime;
- generated artifacts become too large for normal repository history;
- a family cannot be assigned a structured classification;
- any phase would need to reinterpret MP8 evidence as production or monograph
  evidence.

## Expected Final Interpretation

The useful outcome is a defensible readiness map:

- non-neural differentiable resampling should likely become a clean-room
  component specification first if FW2 succeeds;
- neural OT should remain artifact-dependent unless FW3 restores the bundled
  checkpoint and runs a bounded call;
- stochastic flow should become a clean-room algorithm specification only if
  FW4 gives finite, interpretable behavior under mandatory lightweight
  settings;
- DPF/dPFPF should remain behind a production contract until FW5 clarifies
  filter-level gradient, shape, state, and resampling semantics.
