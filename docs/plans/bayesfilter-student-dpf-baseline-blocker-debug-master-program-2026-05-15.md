# Master program: student DPF blocker debug gates

## Date

2026-05-15

## Status

Proposed master program for the next quarantined student DPF
experimental-baseline blocker-debug stream.

This is a planning document only.  It does not execute the debug gates, commit
files, push changes, edit vendored student source, or authorize production use.

This program is a narrow post-MP8 addendum.  It does not reopen MP5-MP8, does
not replace the clean-room controlled-baseline closeout, and does not delay
BayesFilter-owned clean-room implementation work for families that the
future-work usability gates already classified as ready.  It only resolves or
records the five remaining blocked or excluded student-lane surfaces below.

## Governing Purpose

The student DPF future-work usability gates completed with final label
`future_work_usability_gates_complete`, but five blocker families remain:

1. MLCOE transformer resampler shape error inside
   `WeightedMultiHeadAttention.call`;
2. advanced TensorFlow DPF with soft resampling shape-invariant error inside
   the TensorFlow time loop;
3. MLCOE stochastic flow missing exact model/covariance/observation contract;
4. MLCOE dPFPF missing exact model and flow/resampling contract;
5. kernel PFF excluded from routine panels because earlier bounded checks found
   long runtime or iteration-cap behavior.

This program turns those blockers into independent, bounded debug gates.  The
goal is not to make student code production-ready.  The goal is to decide which
blocked surfaces can become:

- `usable_component_only`;
- `usable_for_clean_room_spec`;
- `debug_gate_resolved_but_not_promoted`;
- `blocked_with_reproducible_root_cause`;
- `excluded_from_future_clean_room_inputs`.

## Lane Boundary

Owned write surfaces:

- `docs/plans/bayesfilter-student-dpf-baseline-*`;
- `experiments/student_dpf_baselines/runners/`;
- `experiments/student_dpf_baselines/reports/`;
- `experiments/student_dpf_baselines/reports/outputs/`;
- `docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md`,
  only for a short addendum after successful completion.

Read-only surfaces:

- `experiments/student_dpf_baselines/vendor/`;
- existing student-lane reports and JSON outputs.

Forbidden:

- production `bayesfilter/`;
- `docs/chapters/`;
- `docs/references.bib`;
- DPF monograph/reviewer-grade plans and reset memos;
- vendored student source edits;
- copying student implementation into production;
- broad dependency installs;
- network, live API, GPU-required runs, notebook conversion, training jobs,
  HMC chains, or unbounded experiments.

No commit or push is authorized by this plan.

## Governing Evidence

Primary input:

- `experiments/student_dpf_baselines/reports/student-dpf-baseline-future-work-usability-gates-result-2026-05-15.md`;
- `experiments/student_dpf_baselines/reports/outputs/future_work_usability_gates_2026-05-15.json`;
- `experiments/student_dpf_baselines/reports/outputs/future_work_usability_gates_summary_2026-05-15.json`.

Prior kernel PFF evidence:

- `docs/plans/bayesfilter-student-dpf-baseline-mp3-kernel-pff-debug-gate-plan-2026-05-11.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-mp3-kernel-pff-debug-gate-plan-audit-2026-05-11.md`;
- `experiments/student_dpf_baselines/reports/advanced-particle-filter-kernel-pff-debug-gate-result-2026-05-11.md`.

Current blocker decisions from the future-work usability gates:

| Blocker | Current class | Next decision |
| --- | --- | --- |
| MLCOE transformer resampler | `blocked_environment_drift` | `debug_gate_next` |
| Advanced TF DPF soft resampling | `blocked_environment_drift` | `debug_gate_next` |
| MLCOE stochastic flow | `blocked_missing_assumption` | `defer_until_artifacts_or_assumptions` |
| MLCOE dPFPF | `blocked_missing_assumption` | `defer_until_artifacts_or_assumptions` |
| Kernel PFF | `algorithm_test_sensitivity_and_long_runtime` | excluded pending separate debug |

Ready-family decisions from the future-work usability gates remain unchanged:

- differentiable resampling: `component_spec_next`;
- neural OT / advanced amortized OT: `component_spec_next`;
- successful stochastic-flow paths: `clean_room_spec_next`;
- successful DPF paths: `clean_room_spec_next`.

## Cross-Program Rules

1. Each blocker is an independent debug gate.  A pass or failure in one gate
   does not promote or demote another gate.
2. The default outcome is conservative exclusion unless a bounded gate produces
   explicit evidence.
3. Debug code may live in student-lane runners, but vendored student source
   must remain untouched.
4. Any successful debug result remains student-lane evidence only.  A separate
   BayesFilter-owned clean-room spec is required before production work.
5. A gate may create an adapter-side shim only if the shim records the exact
   assumption it supplies and does not patch or mask the student implementation.
6. A gate that cannot satisfy its input contract must exit with a blocker label
   instead of fabricating fixtures, covariance semantics, observations, or
   training artifacts.
7. A gate may not promote a neural or learned component past `api_smoke_only`
   unless the archived artifact, weights, training meaning, and input contract
   are all explicit.

## Program Phases

### DBG0: Plan Audit And Convergence

Purpose:

- audit this master program before execution;
- optionally use Claude Code as a read-only critical reviewer;
- revise until the execution path is bounded and lane-safe.

Primary criterion:

- Codex and, if used, Claude both accept that the program is executable without
  production, monograph, vendored, network, GPU, training, notebook, or HMC
  work.

Veto diagnostics:

- any phase depends on editing vendored code;
- any phase hides a blocker by changing the student algorithm semantics;
- any phase lacks a structured result label.

Exit labels:

- `dbg0_plan_accepted`;
- `dbg0_plan_needs_revision`;
- `dbg0_plan_blocked`.

### DBG1: MLCOE Transformer Resampler Shape Debug Gate

Observed blocker:

- `mlcoe_transformer_resampler` failed with an incompatible shape error in
  `WeightedMultiHeadAttention.call`;
- the recorded call had attention score shape `[1, 2, 16, 16]` and weight shape
  `[1, 1, 1, 8]`.

Primary hypotheses:

- DBG1-H1: the probe input shape was wrong for the MLCOE transformer contract;
- DBG1-H2: the transformer implementation mixes particle, feature, and head
  dimensions incorrectly and cannot run without source fixes;
- DBG1-H3: the path is untrained API surface only even if the shape issue is
  avoided.

Implementation details:

1. Read only the MLCOE transformer code and existing failed JSON record.
2. Create a runner that tests only tiny synthetic inputs:
   - `N=8`;
   - one-dimensional particle input if the code's `dec_out_linear` implies
     scalar output;
   - optional two-dimensional input only if the signature and internal shape
     flow support it.
3. Run constructor and forward-call probes with strict timeout and no training.
4. Record:
   - input shape;
   - attention score shape if observable from exception text;
   - output shape;
   - finite output status;
   - whether hidden-state output shape is coherent.

Primary criterion:

- classify whether the blocker is probe-shape mismatch, implementation-shape
  bug, or untrained API-only limitation.

Allowed output labels:

- `transformer_api_smoke_resolved_shape_only`;
- `transformer_blocked_implementation_shape_bug`;
- `transformer_blocked_missing_training_artifact`;
- `transformer_excluded_from_clean_room_inputs`.

Promotion rule:

- this gate cannot produce `usable_for_clean_room_spec` because the MLCOE
  transformer is untrained in the current archive.  At most it can become
  `api_smoke_only`.

### DBG2: Advanced TF DPF Soft Resampling Shape-Invariant Debug Gate

Observed blocker:

- `advanced_tf_dpf_soft` failed with a TensorFlow `tf.while_loop` shape
  invariant error: input tensor entered with shape `(1, 8)` but had shape
  `(None, 8)` after one iteration.

Primary hypotheses:

- DBG2-H1: the issue is caused by the runner using a dynamic batch dimension
  or watched tensor shape that the student implementation does not constrain;
- DBG2-H2: the issue is internal to the student soft DPF implementation's
  `tf.while_loop` shape invariants;
- DBG2-H3: a narrower eager or non-gradient forward-only probe may run, but
  gradient usability remains blocked.

Implementation details:

1. Read only the advanced soft DPF implementation and failed JSON record.
2. Test three bounded probes:
   - constructor-only;
   - forward-only with fixed `B=1`, `N=8`, `T=2`, `D=2`;
   - gradient smoke only if forward-only passes.
3. Do not modify vendored `shape_invariants`.
4. If a probe fails, capture the exact TensorFlow error and classify whether it
   occurs before forward, during forward, or during gradient.

Primary criterion:

- determine whether advanced soft DPF is usable as a clean-room input, forward
  smoke only, or remains blocked by student implementation shape invariants.

Allowed output labels:

- `advanced_soft_dpf_forward_only`;
- `advanced_soft_dpf_gradient_smoke_ok`;
- `advanced_soft_dpf_blocked_shape_invariant`;
- `advanced_soft_dpf_excluded_pending_vendor_fix`.

Promotion rule:

- `clean_room_spec_next` is justified only if forward and gradient smoke both
  pass without vendored edits.

### DBG3: MLCOE Stochastic Flow Contract Debug Gate

Observed blocker:

- `mlcoe_stochastic_flow` was not executed because the contract audit lacked a
  complete model object with exact flow/dPF field semantics, validated
  covariance, and observation contract.

Primary hypotheses:

- DBG3-H1: the existing range-bearing MLCOE adapter model can be extended
  adapter-side to supply the required fields without vendored edits;
- DBG3-H2: the stochastic-flow classes require fields or truth-dependent
  quantities that are not appropriate for a clean comparison gate;
- DBG3-H3: a single-step contract smoke can classify the path even if a full
  filter run is not justified.

Implementation details:

1. Inventory required attributes from MLCOE stochastic-flow classes:
   - `state_dim`;
   - `P_prior`;
   - `R_filter`;
   - `R_inv_filter`;
   - `x_truth`, if required;
   - `x_prior`, if required;
   - `h_func`;
   - `jacobian_h`.
2. Create an adapter-side contract object only if every supplied field has a
   documented source from the existing nonlinear Gaussian fixture.
3. Run at most a single-step or reduced `N=8`, `n_steps<=5` smoke.
4. Do not claim full filter usability from contract-only success.

Primary criterion:

- decide whether MLCOE stochastic flow has a satisfiable adapter contract or
  depends on assumptions too specific to use as future clean-room evidence.

Allowed output labels:

- `mlcoe_stochastic_flow_contract_satisfiable`;
- `mlcoe_stochastic_flow_single_step_smoke_ok`;
- `mlcoe_stochastic_flow_blocked_truth_dependent_contract`;
- `mlcoe_stochastic_flow_blocked_missing_model_semantics`.

### DBG4: MLCOE dPFPF Contract Debug Gate

Observed blocker:

- `mlcoe_dpfpf` was not executed because the contract audit lacked exact model,
  EDH solver, covariance, observation, and resampling semantics.

Primary hypotheses:

- DBG4-H1: a minimal fixture-backed model can satisfy `DifferentiablePFPF.step`
  without vendored edits;
- DBG4-H2: the default `EDHSolver` and `SinkhornResampler` contracts require
  model fields that are under-specified by the current archive;
- DBG4-H3: the path may be classified as component-contract evidence even if a
  full differentiable filtering chain is not justified.

Implementation details:

1. Inventory required model fields from `DifferentiablePFPF`, `EDHSolver`, and
   `SinkhornResampler`.
2. Build a contract table mapping each required field to:
   - fixture-derived;
   - adapter-derived;
   - unavailable;
   - ambiguous.
3. Execute at most one `step` smoke with `N<=8`, `n_steps<=3` only if all
   required fields are mapped without ambiguity.
4. Record gradient smoke only if the step smoke succeeds.

Primary criterion:

- decide whether MLCOE dPFPF should enter a future clean-room contract, remain
  component-only, or be excluded pending student-side clarification.

Allowed output labels:

- `mlcoe_dpfpf_contract_satisfiable`;
- `mlcoe_dpfpf_step_smoke_ok`;
- `mlcoe_dpfpf_gradient_smoke_ok`;
- `mlcoe_dpfpf_blocked_missing_contract`;
- `mlcoe_dpfpf_excluded_pending_clarification`.

### DBG5: Kernel PFF Bounded Reclassification Gate

Observed blocker:

- earlier kernel PFF evidence found slow/test-sensitive behavior and
  iteration-cap hits.

Primary hypotheses:

- DBG5-H1: kernel PFF can be used only as a reduced diagnostic, not routine
  comparison evidence;
- DBG5-H2: a very small bounded configuration can classify the failure mode
  more precisely;
- DBG5-H3: kernel PFF should remain excluded from clean-room implementation
  inputs unless convergence and runtime improve under explicit caps.

Implementation details:

1. Reuse prior kernel PFF debug artifacts rather than broad reruns.
2. Run only if prior artifacts do not already answer the classification:
   - tiny linear fixture;
   - `N<=16`;
   - explicit iteration cap;
   - explicit wall-clock cap;
   - no notebooks or experiment scripts.
3. Record:
   - convergence iterations;
   - hit-cap flag;
   - runtime;
   - finite output status;
   - whether classification changes from `excluded_pending_debug`.

Primary criterion:

- decide whether kernel PFF remains excluded, becomes diagnostic-only, or
  deserves a future clean-room debug plan.

Allowed output labels:

- `kernel_pff_diagnostic_only`;
- `kernel_pff_excluded_runtime`;
- `kernel_pff_excluded_iteration_cap`;
- `kernel_pff_reduced_smoke_ok_not_routine`;
- `kernel_pff_needs_separate_research_plan`.

### DBG6: Integrated Blocker Map And Next Clean-Room Queue

Purpose:

- consolidate DBG1-DBG5 into a final blocker map;
- update reset memo and master program;
- decide what, if anything, enters the future BayesFilter-owned clean-room
  implementation queue.

Required artifacts:

- Markdown result:
  `experiments/student_dpf_baselines/reports/student-dpf-baseline-blocker-debug-gates-result-2026-05-15.md`;
- JSON records:
  `experiments/student_dpf_baselines/reports/outputs/blocker_debug_gates_2026-05-15.json`;
- summary JSON:
  `experiments/student_dpf_baselines/reports/outputs/blocker_debug_gates_summary_2026-05-15.json`.
- bounded debug runner:
  `experiments/student_dpf_baselines/runners/run_blocker_debug_gates.py`.

Primary criterion:

- every blocker has one final label, one interpretation, and one next action.

Exit labels:

- `student_dpf_blocker_debug_complete`;
- `student_dpf_blocker_debug_complete_with_exclusions`;
- `student_dpf_blocker_debug_needs_revision`;
- `student_dpf_blocker_debug_blocked`.

## Validation Contract

Before this program can be considered complete, run:

```bash
python -m py_compile experiments/student_dpf_baselines/runners/run_blocker_debug_gates.py
python -m experiments.student_dpf_baselines.runners.run_blocker_debug_gates
python -m experiments.student_dpf_baselines.runners.run_blocker_debug_gates --validate-only
rg -n "experiments/student_dpf_baselines|advanced_particle_filter|2026MLCOE" bayesfilter tests
git diff --check -- docs/plans/bayesfilter-student-dpf-baseline-* experiments/student_dpf_baselines/runners experiments/student_dpf_baselines/reports
```

Expected:

- every planned blocker is represented in the JSON output;
- every non-`ok` result has a blocker class and blocker message;
- no vendored files are modified;
- production import-boundary search returns no matches;
- generated artifacts remain suitable for normal repository history.
- `git status --short experiments/student_dpf_baselines/vendor` shows no
  vendored snapshot modifications.

## Recommended Execution Order

1. DBG0 plan audit.
2. DBG2 advanced TF DPF soft shape-invariant gate.
3. DBG1 MLCOE transformer shape gate.
4. DBG3 MLCOE stochastic-flow contract gate.
5. DBG4 MLCOE dPFPF contract gate.
6. DBG5 kernel PFF reclassification gate.
7. DBG6 integrated blocker map.

Reasoning:

- DBG2 and DBG1 are the most concrete code-shape blockers.
- DBG3 and DBG4 are contract blockers and should not execute until the required
  fields are mapped explicitly.
- DBG5 is lower priority because prior evidence already justifies exclusion
  from routine panels.

## Final Policy

This program may make a blocked student surface more usable as comparison-only
evidence.  It must not promote any student implementation into production.
Any future production work must be BayesFilter-owned, clean-room, separately
planned, and independently tested.
