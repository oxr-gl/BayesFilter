# Actual-SIR Nystrom Less-Intrusive Stability Visible Execution Ledger

Date: 2026-06-23

Status: `INITIALIZED_FOR_P00`

## Ledger

### 2026-06-23 - Program Initialization - PRECHECK

Evidence contract:

- Question: Can a less-intrusive Nystrom stabilization repair the brittle
  actual-SIR row without breaking paired comparability?
- Baseline/comparator: compiled production-style streaming TF32 actual-SIR
  route; raw brittle artifacts; positive projection as diagnostic-only rescue
  evidence.
- Primary criterion: every phase reaches exact handoff conditions with required
  artifacts and no forbidden claims; P04 requires finite/residual and paired
  threshold pass.
- Veto diagnostics: missing artifact, unsupported claim, missing trusted GPU
  evidence for GPU phases, Nystrom residual veto, paired threshold veto, or
  review non-convergence after five rounds.
- Non-claims: no default readiness, ranking, posterior correctness, dense
  equivalence, HMC readiness, scalable high-N readiness, broad robustness, or
  broad unusability.

Actions:

- Created initial master program, visible runbook, execution ledger, review
  ledger, stop handoff, and phase subplans P00-P07.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-master-program-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-visible-gated-execution-runbook-2026-06-23.md`

Gate status:

- `P00_PASS`

Next action:

- Begin P01 diagnostic adequacy and missing-instrumentation gate.

### 2026-06-23 - Phase P02 - REVISE_AFTER_REVIEW_R1

Evidence contract:

- Question: Which single less-intrusive repair is justified for focused
  implementation?
- Baseline/comparator: P01 diagnostics, closed-lane P03/P06 artifacts, P09D
  SVD negative result, and positive-projection paired failure.
- Primary criterion: exactly one repair family selected with implementation
  scope, validation gate, nonclaims, and stop conditions.
- Veto diagnostics: multiple simultaneous repairs, threshold drift,
  positive-projection promotion, unsupported default claim, missing P04
  validation row, or unresolved Claude revision after five rounds.
- Non-claims: no repair effectiveness, no default readiness, no ranking, no
  posterior correctness, no HMC readiness.

Actions:

- Selected opt-in balanced Sinkhorn scaling gauge normalization for review.
- Ran local selection consistency check: `P02 selection consistency check PASS`.
- Ran Claude read-only review round 1: `VERDICT: REVISE`.
- Patched P02/P03 with exact `[B,N]` formula, explicit P03 code scope, required
  diagnostics, and unconditional Claude implementation review before P04.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-repair-selection-result-2026-06-23.md`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-claude-review-r1-2026-06-23.log`

Gate status:

- `PATCHED_AFTER_R1_PENDING_R2_REVIEW`

Next action:

- Run focused local consistency check and Claude P02 review round 2.

### 2026-06-23 - Phase P02 - PASS_REVIEW_R2

Actions:

- Ran focused local consistency check:
  `P02/P03 R1 repair structural check PASS`.
- Ran Claude read-only review round 2: `VERDICT: AGREE`.

Artifacts:

- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-claude-review-r2-2026-06-23.log`

Gate status:

- `PASSED`

Next action:

- Begin P03 focused implementation.

### 2026-06-23 - Phase P03 - PASS_FOCUSED_TESTS_PENDING_REVIEW

Evidence contract:

- Question: Is balanced Sinkhorn scaling gauge normalization implemented as a
  scoped opt-in path without changing default raw behavior?
- Baseline/comparator: existing raw Nystrom behavior and focused tests.
- Primary criterion: focused tests pass, balanced path is exercised by
  discriminating tests, default `scaling_normalization="none"` behavior remains
  unchanged, and P04 artifact contract is ready.
- Veto diagnostics: test failure, default behavior change, metadata missing,
  repair not exercised, broad unrelated edits, or threshold changes.
- Non-claims: no GPU repair success, no default readiness, no scientific
  validity.

Actions:

- Implemented opt-in `scaling_normalization="balanced"` in the scoped tensor
  Nystrom implementation.
- Added CLI `--nystrom-scaling-normalization {none,balanced}` to the compiled
  actual-SIR benchmark.
- Added `max_abs_log_scaling_gauge_shift` and
  `scaling_normalization_applications` diagnostics to tensor, Python, row, and
  transport metadata.
- Added focused tests for default `none`, XLA/tensor acceptance of `balanced`,
  positive gauge-shift diagnostics, and benchmark propagation.
- Ran syntax check: `PASS`.
- Ran focused CPU-hidden tests: `13 passed, 15109 warnings in 30.10s`.
- Refreshed P04 subplan with exact GPU command template and selected repair
  flags.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-focused-implementation-result-2026-06-23.md`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-focused-tests-2026-06-23.log`

Gate status:

- `LOCAL_PASS_PENDING_CLAUDE_IMPLEMENTATION_REVIEW`

Next action:

- Run mandatory Claude read-only P03 implementation review before P04.

### 2026-06-23 - Phase P03 - PASS_REVIEW

Actions:

- Ran mandatory Claude read-only implementation review round 1:
  `VERDICT: AGREE`.

Artifacts:

- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-claude-review-r1-2026-06-23.log`

Gate status:

- `PASSED`

Next action:

- Launch P04 trusted GPU brittle-row repair gate using GPU1 if available,
  otherwise GPU0.

### 2026-06-23 - Phase P04 - VALID_CANDIDATE_FAILURE

Evidence contract:

- Question: Does the selected less-intrusive repair pass the original brittle
  row without breaking paired comparability?
- Baseline/comparator: compiled streaming TF32 comparator in the same artifact;
  raw and positive-projection prior evidence for context only.
- Primary criterion: aggregate artifact `status == PASS`, finite GPU outputs,
  no Nystrom residual hard veto, paired max delta <= `10.0`, paired mean delta
  <= `5.0`, trusted GPU/TF32 evidence present.
- Veto diagnostics: any aggregate hard veto, missing GPU evidence, missing
  selected-repair metadata, nonfinite outputs, row/column residual threshold
  failure, paired threshold failure, missing artifact.
- Non-claims: no default readiness, no ranking, no HMC readiness, no scalable
  high-N readiness.

Actions:

- Ran trusted GPU preflight; selected physical GPU1 per user rule because GPU1
  was available with 18 MiB used and 0% utilization.
- Ran P04 compiled actual-SIR benchmark with `--nystrom-kernel-mode raw` and
  `--nystrom-scaling-normalization balanced`.
- Artifact status: `FAIL`.
- Hard vetoes:
  `nystrom:nonfinite_log_likelihood`,
  `nystrom:nonfinite_nystrom_factors`,
  `nystrom:nonfinite_nystrom_particles`.
- Streaming comparator passed on GPU.
- Nystrom selected metadata was present, so this is a valid repair-candidate
  failure rather than a missing-metadata or trusted-GPU artifact failure.
- Wrote P04 result.
- Refreshed P06 for P04 valid-candidate-failure entry path.

Artifacts:

- `docs/benchmarks/actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.md`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.log`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-brittle-row-repair-gate-result-2026-06-23.md`

Gate status:

- `FAILED_VALID_CANDIDATE_REJECTION`

Next action:

- Skip P05 and begin P06 candidate-failure classification.

### 2026-06-23 - Phase P06 - REPAIR_FAILED_OR_RESTRICT_POLICY

Evidence contract:

- Question: Does this lane justify a separate promotion/stress program, and
  what must that next program test?
- Baseline/comparator: P04 repair gate artifact, prior SVD and
  positive-projection evidence, and repo evidence policy.
- Primary criterion: P06 result makes a boundary-safe decision and does not
  claim default readiness.
- Veto diagnostics: unsupported default claim, missing uncertainty caveat,
  missing next evidence list, threshold drift, invalid prior artifact, or
  unreviewed promotion/repair-loop recommendation.
- Non-claims: no default readiness, no superiority, no posterior correctness,
  no HMC readiness.

Actions:

- Classified P04 as a valid repair-candidate failure, not a harness or artifact
  invalidation.
- Decided not to run a return-to-P02 loop automatically because remaining
  obvious alternatives are either already rejected, policy tuning, or a new
  method lane.
- Refreshed P07 closeout subplan with expected final status
  `CLOSED_REPAIR_FAILED_OR_RESTRICT_POLICY`.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p06-promotion-readiness-decision-result-2026-06-23.md`

Gate status:

- `PASSED_CLASSIFICATION`

Next action:

- Complete P07 closeout and stop handoff.

### 2026-06-23 - Phase P07 - CLOSED

Evidence contract:

- Question: What exactly did this lane establish, and what is the safest next
  action?
- Baseline/comparator: all completed phase results and artifacts.
- Primary criterion: P07 result and stop handoff accurately reflect phase
  outcomes, blockers, and nonclaims.
- Veto diagnostics: missing artifact, unsupported claim, mismatch between
  ledger and stop handoff, or claiming default readiness.
- Non-claims: default readiness, superiority, posterior correctness, dense
  equivalence, HMC readiness unless a future separate program proves them.

Actions:

- Wrote P07 closeout result.
- Updated visible stop handoff with final status
  `CLOSED_REPAIR_FAILED_OR_RESTRICT_POLICY`.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p07-closeout-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-visible-stop-handoff-2026-06-23.md`

Gate status:

- `CLOSED_REPAIR_FAILED_OR_RESTRICT_POLICY`

### 2026-06-23 - Phase P01 - ASSESS_GATE

Evidence contract:

- Question: Are diagnostics sufficient to select one less-intrusive repair, or
  is minimal opt-in instrumentation needed?
- Baseline/comparator: current Nystrom diagnostics and compiled redo harness
  output fields.
- Primary criterion: required diagnostic fields are available or minimally
  implemented with focused tests passing and no default/raw behavior change.
- Veto diagnostics: default behavior change, CLI incompatibility, missing
  focused tests after code edit, diagnostic changes that alter raw computation,
  or missing P02 handoff.
- Non-claims: no repair selection, no repair effectiveness, no default
  readiness.

Actions:

- Inspected tensor and compiled harness diagnostic fields.
- Found tensor-level `min_kernel_denominator` and `denominator_floor_hits`, but
  missing compiled-row serialization.
- Patched only compiled-row instrumentation and focused test assertions.
- Ran focused CPU-hidden tests: `10 passed`.
- Ran focused serialization check: `P01 denominator diagnostic serialization check PASS`.
- Refreshed P02 subplan with inherited diagnostic surface.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p01-diagnostic-adequacy-result-2026-06-23.md`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p01-focused-tests-2026-06-23.log`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-repair-selection-subplan-2026-06-23.md`

Gate status:

- `PASSED_MINIMAL_INSTRUMENTATION`

Next action:

- Begin P02 repair selection and Claude read-only review.

### 2026-06-23 - Phase P00 - PASS_REVIEW

Evidence contract:

- Question: Is this new less-intrusive repair program safe and complete enough
  to launch?
- Baseline/comparator: repo policy, visible runbook template, prior closeout
  result, and user protocol.
- Primary criterion: local structural checks pass and Claude review ends with
  `VERDICT: AGREE` within five rounds.
- Veto diagnostics: missing required section, missing stop condition, detached
  execution, Claude as executor, changed thresholds, positive projection as
  promotion repair, unsupported default claim.
- Non-claims: no repair effectiveness, no default readiness, no scientific
  validity, no performance/ranking claim.

Actions:

- Ran local structural check: `P00 structural check PASS`.
- Ran Claude read-only review round 1: `VERDICT: REVISE`.
- Patched P04/P05/P06 handoffs so valid candidate failures route to P06
  classification or reviewed repair loop instead of automatic closeout.
- Patched P02 prior-artifact wording to `closed-lane P03/P06 artifacts`.
- Ran post-patch structural check: `P00 post-R1 structural repair check PASS`.
- Ran Claude read-only review round 2: `VERDICT: AGREE`.
- Wrote P00 result.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p00-program-review-result-2026-06-23.md`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p00-claude-review-r1-2026-06-23.log`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p00-claude-review-r2-2026-06-23.log`

Gate status:

- `PASSED`

Next action:

- Begin P01 diagnostic adequacy and missing-instrumentation gate.
