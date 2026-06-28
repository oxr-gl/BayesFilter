# Actual-SIR Nystrom Stability Repair Visible Execution Ledger

Date: 2026-06-23

Status: `CLOSED_REPAIR_FAILED_OR_BLOCKED`

## Ledger

### 2026-06-23 - Program Initialization - PRECHECK

Evidence contract:

- Question: Can visible gated execution localize and repair the P09 Nystrom
  nonfinite failure without uncontrolled tuning?
- Baseline/comparator: P09B/P09C/P09D artifacts and compiled streaming TF32
  comparator for paired repair validation.
- Primary criterion: every phase reaches exact handoff conditions with required
  artifacts and no forbidden claims.
- Veto diagnostics: missing artifact, unsupported claim, missing trusted GPU
  evidence for GPU phases, nonfinite repair-validation row, or review
  non-convergence after five rounds.
- Non-claims: no default readiness, ranking, posterior correctness, dense
  equivalence, or HMC readiness.

Actions:

- Created master program, phase subplans, visible runbook, review ledger, and
  stop handoff placeholders.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-master-program-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-visible-gated-execution-runbook-2026-06-23.md`

Gate status:

- `P00_PASS`

Next action:

- Start P01 instrumentation precheck and local implementation.

### 2026-06-23 - Phase P00 - PASS_REVIEW

Evidence contract:

- Question: Is the repair program safe and complete enough to launch visible
  gated execution?
- Baseline/comparator: AGENTS policy, visible runbook template, P09D result,
  and promotion runbook blocker.
- Primary criterion: local checks pass and Claude review ends with
  `VERDICT: AGREE` within five rounds.
- Veto diagnostics: missing sections, detached execution authority, Claude as
  execution authority, missing stop conditions, or unsupported claims.
- Non-claims: no repair/default/scientific validity.

Actions:

- Ran local structural check.
- Ran Claude read-only review rounds 1-3.
- Patched material review findings after rounds 1 and 2.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p00-program-review-result-2026-06-23.md`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p00-claude-review-r1-2026-06-23.log`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p00-claude-review-r2-2026-06-23.log`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p00-claude-review-r3-2026-06-23.log`

Gate status:

- `PASSED`

Next action:

- Begin P01 instrumentation.

### 2026-06-23 - Phase P01 - ASSESS_GATE

Evidence contract:

- Question: Can the harness record where the Nystrom failure starts without
  changing algorithm behavior?
- Baseline/comparator: existing P09D code path and focused tests.
- Primary criterion: focused tests pass and default `cholesky` behavior remains
  unchanged except for opt-in diagnostics.
- Veto diagnostics: default behavior change, CLI incompatibility, missing
  diagnostic fields, or altered thresholds.
- Non-claims: no repair or default readiness.

Actions:

- Added opt-in diagnostic tensors and harness aggregation.
- Ran focused CPU-hidden tests.
- Refreshed P02 subplan with exact row/log/artifact paths.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p01-instrumentation-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p02-failure-localization-subplan-2026-06-23.md`

Gate status:

- `PASSED`

Next action:

- Begin P02 trusted GPU preflight and failure-localization rows.

### 2026-06-23 - Phase P02 - ASSESS_GATE

Evidence contract:

- Question: Where does the first nonfinite or invalid Nystrom diagnostic appear?
- Baseline/comparator: P09B/P09C/P09D failing artifacts plus viable
  `rank=32,epsilon=0.5` control.
- Primary criterion: diagnostics identify first failing stage or classify
  localization as ambiguous with sufficient artifacts for P03.
- Veto diagnostics: missing GPU/TF32 evidence, diagnostics changing behavior,
  missing row artifact, or failure before diagnostic data is written.
- Non-claims: no repair or promotion claim.

Actions:

- Ran three trusted GPU diagnostic rows with `--nystrom-diagnostics`.
- Wrote P02 result and refreshed P03 for prefix/first-failure diagnostics.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p02-failure-localization-result-2026-06-23.md`
- `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r32-eps0p25-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r64-eps0p3-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r32-eps0p5-control-2026-06-23.json`

Gate status:

- `PASSED_WITH_AMBIGUOUS_LOCALIZATION`

Next action:

- Claude review refreshed P03 subplan before P03 prefix launch.

### 2026-06-23 - Phase P03 - ASSESS_GATE

Evidence contract:

- Question: At what prefix do the known failing rows first fail, and does the
  control remain finite at that prefix?
- Baseline/comparator: P02 instrumented rows and compiled streaming TF32 paired
  comparator in each artifact.
- Primary criterion: bracket both known failing rows and verify the control at
  the smallest failing prefix and `T=20`.
- Veto diagnostics: missing GPU artifact, skipped control, changed thresholds,
  or treating prefix evidence as repair/default evidence.
- Non-claims: no repair effectiveness, default readiness, ranking, posterior
  correctness, or HMC readiness.

Actions:

- Claude P03 subplan review converged after a redesigned focused prompt.
- Ran trusted GPU prefix rows on GPU0 after GPU1 was memory-busy at preflight.
- Bracketed both known failing rows at `T=2 -> T=4`.
- Verified `rank=32,epsilon=0.5` control at `T=4` and `T=20`.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p03-minimal-ablations-result-2026-06-23.md`
- `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r32-eps0p25-t1-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r32-eps0p25-t2-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r32-eps0p25-t4-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r64-eps0p3-t1-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r64-eps0p3-t2-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r64-eps0p3-t4-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r32-eps0p5-control-t4-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r32-eps0p5-control-t20-2026-06-23.json`

Gate status:

- `PASSED_PREFIX_LOCALIZED_SCALING_RESIDUAL_FAILURE`

Next action:

- Refresh and review P04 repair selection.

### 2026-06-23 - Phase P04 - PASS_SELECTION

Evidence contract:

- Question: Which repair path is justified by P03 diagnostics without tuning
  after the fact?
- Baseline/comparator: P02/P03 artifacts and P09B/P09C/P09D prior evidence.
- Primary criterion: select exactly one path with clear nonclaims and validation
  gates.
- Veto diagnostics: multiple simultaneous repairs, missing validation control,
  unsupported default claim, or repair not connected to diagnostics.
- Non-claims: no repair effectiveness, default readiness, scalable readiness,
  dense Sinkhorn equivalence, posterior correctness, or HMC readiness.

Actions:

- Proposed a scaling repair; Claude review rejected it as not distinct from
  existing denominator flooring.
- Patched P04/P05 to select an opt-in `positive_projected` Nystrom kernel
  diagnostic repair with required projection floor-hit evidence.
- Claude focused re-review returned `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p04-repair-selection-result-2026-06-23.md`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p04-selection-claude-review-r1-2026-06-23.log`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p04-selection-claude-review-r2-2026-06-23.log`

Gate status:

- `PASSED_SELECT_POSITIVE_PROJECTED_NYSTROM_DIAGNOSTIC_REPAIR`

Next action:

- Begin P05 focused implementation.

### 2026-06-23 - Phase P05 - PASS_IMPLEMENTATION

Evidence contract:

- Question: Was the opt-in positive-projected Nystrom kernel diagnostic
  implemented correctly and narrowly enough to test?
- Baseline/comparator: P04 selected repair contract and pre-repair focused
  tests.
- Primary criterion: raw remains default; opt-in mode is selectable; projection
  diagnostics prove the path is exercised; focused tests pass.
- Veto diagnostics: test failure, broad refactor, default-policy change,
  missing diagnostics, threshold change, or repair diverging from P04.
- Non-claims: no serious-model rescue, default readiness, scalable readiness,
  dense Sinkhorn equivalence, posterior correctness, or HMC readiness.

Actions:

- Added `kernel_mode="raw"` and `kernel_mode="positive_projected"` to the
  Nystrom transport.
- Added benchmark flag `--nystrom-kernel-mode`.
- Added projected-kernel diagnostics and dense diagnostic scope metadata.
- Added focused tests, including a discriminating projection floor-hit fixture.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p05-focused-repair-result-2026-06-23.md`
- `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
- `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`
- `tests/test_nystrom_transport_tf.py`
- `tests/test_actual_sir_nystrom_compiled_redo.py`

Gate status:

- `PASSED_FOCUSED_IMPLEMENTATION_READY_FOR_P06`

Next action:

- Run P06 trusted GPU repair gate.

### 2026-06-23 - Phase P06 - FAIL_REPAIR_GATE

Evidence contract:

- Question: Does `--nystrom-kernel-mode positive_projected` rescue failing rows
  and preserve the control under original paired thresholds?
- Baseline/comparator: compiled streaming TF32 actual-SIR route and pre-repair
  P09/P03 artifacts.
- Primary criterion: all required rows pass finite/residual/paired thresholds
  with positive-projected metadata.
- Veto diagnostics: any nonfinite, residual threshold failure, paired threshold
  failure, missing GPU evidence, control regression, or missing repair metadata.
- Non-claims: no default readiness, no ranking, no scalable readiness, no dense
  equivalence, no posterior correctness, no HMC readiness.

Actions:

- Ran first required trusted GPU row on GPU1:
  `rank=32,epsilon=0.25`, `--nystrom-kernel-mode positive_projected`.
- Stopped after a valid hard veto in the first required row.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p06-p09-regate-decision-result-2026-06-23.md`
- `docs/benchmarks/actual-sir-nystrom-stability-repair-p06-positive-projected-r32-eps0p25-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-stability-repair-p06-positive-projected-r32-eps0p25-2026-06-23.md`
- `docs/plans/logs/actual-sir-nystrom-stability-repair-p06-positive-projected-r32-eps0p25-2026-06-23.log`

Gate status:

- `FAILED_PAIRED_THRESHOLD_AFTER_FINITE_RESCUE`

Next action:

- Refresh P07 closeout; do not reopen P09/P10 from this result.

### 2026-06-23 - Phase P07 - CLOSED

Evidence contract:

- Question: What did the repair program establish, and what remains blocked?
- Baseline/comparator: all completed phase results and the current promotion
  runbook blocker.
- Primary criterion: final handoff separates finite rescue from paired
  comparability failure and preserves blocked P09/P10 status.
- Veto diagnostics: unsupported default claim, missing artifact, stale status,
  or failure to distinguish candidate failure from research-direction failure.
- Non-claims: No default readiness, repair success, broad robustness/unusability,
  ranking, posterior correctness, dense equivalence, scalable readiness, or HMC
  readiness.

Actions:

- Refreshed visible stop handoff.
- Wrote P07 closeout result.
- Ran local artifact/status check.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p07-closeout-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-visible-stop-handoff-2026-06-23.md`

Gate status:

- `CLOSED_REPAIR_FAILED_OR_BLOCKED`

Next action:

- No next phase in this master program.
