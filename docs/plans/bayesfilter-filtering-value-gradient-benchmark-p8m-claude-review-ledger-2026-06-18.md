# P8m Claude Review Ledger

Date: 2026-06-18

Status: `PENDING_INITIAL_REVIEW`

## Review Policy

Claude is a read-only reviewer only.  Claude may inspect local repo paths and
return findings plus `VERDICT: AGREE` or `VERDICT: REVISE`.  Claude cannot edit
files, run commands, authorize execution, change pass/fail criteria, approve
GPU usage, or make scientific claims authoritative.

Use bounded prompts.  If a prompt is silent, run a small probe; if the probe
answers, reduce the review packet.

## Pending Review: Initial Planning Packet

status: `PROMPT_TOO_BROAD_REDESIGNED`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-generic-transport-core-optimization-master-program-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-visible-gated-execution-runbook-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase0-governance-boundary-subplan-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase1-instrumentation-design-subplan-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-visible-execution-ledger-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-visible-stop-handoff-2026-06-18.md`

Review checklist:

- generic transport-core scope;
- SIR d18 is only a stress fixture;
- exact implementation is separated from lower-iteration/epsilon validation;
- no particle-adequacy, leaderboard, HMC, exact-likelihood, or production
  overclaim;
- every GPU command requires trusted/escalated context;
- Phase 0/1 have required fields and stop conditions;
- repair loop and max five Claude rounds are explicit.

Attempted launch:

```bash
claude -p "<bounded review of master, runbook, Phase 0, Phase 1, ledgers>" --model opus
```

Outcome:

- The prompt stayed silent for about one minute.
- The worker was interrupted.
- A tiny read-only probe returned `PROBE_OK`.

Diagnosis:

- Claude service is responsive; the initial review packet was too broad.

Repair:

- Split review into smaller chunks.  First retry covers only the master program
  and visible runbook.

## Review Iteration 1b: Master And Runbook

status: `AGREE`
worker: `claude -p bounded master/runbook review`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-generic-transport-core-optimization-master-program-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-visible-gated-execution-runbook-2026-06-18.md`

Review checklist:

- generic transport-core scope;
- SIR d18 stress-fixture-only boundary;
- exact implementation separated from Sinkhorn/epsilon validation;
- no proxy metric promotion;
- trusted/escalated GPU boundary;
- repair loop, artifact coverage, and stop conditions.

Verdict:

- `VERDICT: AGREE`

Findings:

- No blocking findings on the requested checks.
- Generic transport-core scope is correctly fenced.
- SIR d18 is consistently kept as stress evidence only.
- Exact implementation is separated from Sinkhorn/epsilon validation.
- Proxy metrics are not promoted to scientific or policy conclusions.
- Trusted/escalated GPU boundary is explicit and enforceable.
- Repair loop is bounded and artifact coverage is adequate.
- Stop conditions are aligned with the stated boundaries.

## Review Iteration 2: Phase 0 Result And Phase 1 Subplan

status: `AGREE`
worker: `claude -p bounded Phase 1 launch review`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase0-governance-boundary-result-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase1-instrumentation-design-subplan-2026-06-18.md`

Review checklist:

- Phase 1 is design-only;
- generic transport boundary is preserved;
- no SIR-specific profiling route is authorized;
- required artifacts/checks/evidence contract/forbidden actions/handoff/stop
  conditions are present;
- Phase 1 is consistent with Phase 0.

Verdict:

- `VERDICT: AGREE`

Findings:

- Phase 1 is clearly design-only, not implementation.
- Generic transport boundary is preserved and SIR-specific route is fenced off.
- The plan does not overclaim what Phase 1 can establish.
- Required artifacts, evidence contract, forbidden actions, handoff, and stop
  conditions are present.
- Checks are intentionally light and appropriate for a design-only phase.
- Minor caveat: Phase 1 checks do not restate a direct grep for every Phase 0
  boundary phrase, but this was not a blocker because boundaries are carried in
  objective, veto list, forbidden actions, stop conditions, and inherited Phase
  0 closure.

## Review Iteration 3: Phase 1 Result And Phase 2 Subplan

status: `REVISE_PATCHED_PENDING_ITER3B`
worker: `claude -p bounded Phase 2 implementation review`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase1-instrumentation-design-result-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-microbenchmark-implementation-subplan-2026-06-18.md`

Verdict:

- `VERDICT: REVISE`

Findings:

- Phase 2 checks were too underspecified and still used placeholders instead
  of the exact CPU smoke and JSON assertions from Phase 1.
- The Phase 2 guardrail against SIR callbacks/data paths and intrusive timing
  inside differentiable compiled math was not restated strongly enough.
- The Phase 3 handoff reached beyond the Phase 2 evidence boundary by implying
  GPU-rung readiness rather than only planning readiness.

Patch disposition:

- Replaced placeholder checks with the exact Phase 1 CPU smoke command and JSON
  assertions.
- Explicitly forbade SIR callbacks, SIR-only data paths, SIR state-layout
  assumptions, disease-model-specific inputs, side-effect timers inside
  differentiable compiled transport math, and semantic transport changes.
- Narrowed the handoff so Phase 2 proves CPU smoke and metadata correctness,
  not GPU performance/readiness.

## Review Iteration 3b: Patched Phase 2 Subplan

status: `AGREE`
worker: `claude -p focused patched Phase 2 review`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-microbenchmark-implementation-subplan-2026-06-18.md`

Verdict:

- `VERDICT: AGREE`

Findings:

- No remaining findings.
- Exact CPU smoke command and JSON assertions replaced placeholders.
- SIR callbacks/data paths and side-effect timers inside differentiable
  compiled transport math are explicitly forbidden.
- Phase 3 handoff is narrowed to CPU smoke and metadata assertions; Phase 2
  does not prove GPU readiness or performance.

## Review Iteration 4: Phase 2 Implementation And Result

status: `AGREE`
worker: `claude -p bounded Phase 2 implementation review`

Paths:

- `docs/benchmarks/benchmark_p8m_transport_core_tf.py`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-microbenchmark-implementation-result-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-microbenchmark-implementation-subplan-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-transport-core-cpu-smoke-2026-06-18.json`

Verdict:

- `VERDICT: AGREE`

Findings:

- No blocking findings for Phase 2 close under the stated scope.
- Benchmark is generic synthetic only and avoids model callbacks.
- No SIR callbacks or SIR data paths were found.
- No transport algorithm or default-policy change was found.
- CPU smoke and metadata assertions are documented as passed and consistent
  with the JSON artifact.
- No GPU speed or performance claim is made.
- Artifacts are sufficient for Phase 2 close.

## Review Iteration 5: Phase 3 GPU Chunk Ladder Subplan

status: `AGREE`
worker: `claude -p focused Phase 3 launch-blocker review`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-gpu-chunk-ladder-subplan-2026-06-18.md`

Verdict:

- `VERDICT: AGREE`

Findings:

- Generic synthetic benchmark requirement is satisfied.
- Trusted/escalated GPU commands are explicitly required.
- No SIR-specific path was found.
- Sinkhorn iterations and epsilon are fixed in this phase; tuning is forbidden.
- `N=50000` is not included and is explicitly forbidden without separate
  review.
- Finite/GPU JSON assertions are present.
- Stop conditions are aligned with launch safety.

## Review Iteration 6: Phase 3 Result And Phase 4 Subplan

status: `AGREE`
worker: `claude -p bounded Phase 4 decision review`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-gpu-chunk-ladder-result-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase4-exact-optimization-decision-subplan-2026-06-18.md`

Verdict:

- `VERDICT: AGREE`

Findings:

- No blocking overclaim in Phase 3.
- 1024 is presented as a candidate, not a default.
- 4096 is rejected only for the synthetic shape tested.
- There is no SIR or cross-model overreach.
- Phase 4 is scoped to a decision, not implementation.

## Review Iteration 7: Phase 4 Result And Phase 7 Closeout Path

status: `REVISE_PATCHED_PENDING_ITER7B`
worker: `claude -p bounded Phase 4/Phase 7 closeout review`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase4-exact-optimization-decision-result-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase7-cross-fixture-closeout-subplan-2026-06-18.md`

Verdict:

- `VERDICT: REVISE`

Findings:

- Phase 4 correctly defers exact implementation repair.
- 1024 is kept as a candidate, not promoted to default.
- Phase 5 should not launch, and Phase 4 says so explicitly.
- No SIR, cross-model, or full-filter overclaim appears in Phase 4.
- Phase 7 body is mostly safe, but the title and required result artifact name
  said "Cross-Fixture Confirmation" even though no cross-fixture confirmation
  step is in lane.

Patch disposition:

- Renamed Phase 7 title to administrative boundary closeout.
- Renamed the required Phase 7 result artifact to
  `phase7-administrative-boundary-closeout-result`.
- Added an explicit sentence that cross-fixture or full-filter confirmation is
  out-of-lane future work unless separately reviewed.

## Review Iteration 7b: Patched Phase 7 Closeout

status: `AGREE`
worker: `claude -p focused patched Phase 7 review`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase7-cross-fixture-closeout-subplan-2026-06-18.md`

Verdict:

- `VERDICT: AGREE`

Findings:

- The prior issue is fixed.
- Title is now administrative boundary closeout.
- Required result artifact uses administrative-boundary-closeout naming.
- Cross-fixture or full-filter confirmation is explicitly out-of-lane future
  work unless separately reviewed.
- Forbidden claims reinforce that no cross-model/performance conclusion should
  be claimed without actual multi-fixture evidence.
