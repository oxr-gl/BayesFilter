# Clean XLA JIT Claude Review Ledger

Date: 2026-07-02

Status: `OPEN`

Claude is read-only reviewer only.  Codex remains supervisor and executor.

## Reviews

## Launch Mini-Packet Review

Reviewer: Claude Opus via `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh`

Scope: embedded mini packet only, read-only review.  Claude was instructed not
to read files, edit, run commands, or launch agents after fixed-path packet
read hung despite a successful health probe.

Verdict: `VERDICT: AGREE`

Key finding:

- Phase 0 is valid as an inventory-only first executable phase before
  implementation, provided it stays strictly at inventory scope and does not
  overclaim.

## Current Health Probe

Reviewer: Claude Opus via `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh`

Scope: tiny health probe only.

Result token: `CLEAN_XLA_CURRENT_PROBE_OK`

Interpretation:

- Claude is responsive. A later fixed-path review hang should be treated as a
  prompt/scope/path-read problem unless a fresh tiny probe also fails.

## Phase 1 Subplan Review Iteration 1

Reviewer: Claude Opus via `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh`

Scope: exact fixed-path read-only review of
`docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-guardrails-subplan-2026-07-02.md`.

Verdict: `VERDICT: REVISE`

Key findings:

- The subplan did not list the required Phase 0 pattern classes as a closed
  checklist tied to exact symbols/files.
- Streaming Sinkhorn helper scope was too imprecise.
- Line anchoring expectations were not explicit enough to prevent file-level
  only output.

Repair:

- Patched the Phase 1 subplan to add a closed required-pattern checklist with
  exact files, symbols, pattern classes, severity, and absence handling.
- Added line-anchoring rules requiring AST or span-relative line numbers for
  every required finding.

## Phase 1 Subplan Review Iteration 2

Reviewer: Claude Opus via `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh`

Scope: exact fixed-path read-only review of the patched Phase 1 subplan.

Verdict: `VERDICT: REVISE`

Key finding:

- The warning-only `SINK-TOTAL-CUSTOM-TAPE` row conflicted with a global rule
  that all missing Sinkhorn symbols must fail with `MISSING_SYMBOL`.

Repair:

- Patched the subplan so `MISSING_SYMBOL` is a hard failure only for
  `current veto` rows.
- Warning-only rows now report `MISSING_WARNING_SYMBOL` without blocking Phase
  1, unless a later phase explicitly promotes that helper to a hard gate.
- Updated the primary pass criterion to require all current-veto Phase 0
  classes while reporting warning-only rows separately.
- Corrected the warning helper symbol to
  `_filterflow_manual_streaming_finite_transport_total_vjp`.

## Phase 1 Subplan Review Iteration 3

Reviewer: Claude Opus via `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh`

Scope: exact fixed-path read-only review focused on the patched warning versus
current-veto consistency repair.

Verdict: `VERDICT: AGREE`

Key finding:

- No material blocker remained for Phase 1 execution.
- Non-blocking watchpoint: implementation must verify the checklist symbol
  names match live code exactly because symbol mismatch is an explicit audit
  outcome, not a reason for whole-file fallback scanning.

## Phase 1 Result And Phase 2 Subplan Review

Reviewer: Claude Opus via `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh`

Scope: exact two-file read-only review of:

- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-guardrails-result-2026-07-02.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase2-fixed-randomness-tensorization-subplan-2026-07-02.md`

Verdict: `VERDICT: AGREE`

Key findings:

- Phase 1 result does not overclaim clean XLA; it correctly reports the current
  route as still unclean.
- Phase 2 is bounded to fixed randomness tensorization and preserves the old
  stateless seed policy.
- Non-blocking nit: Phase 2 result should spell out the exact execution and
  Claude review ledger paths to avoid ledger drift.

## Phase 2 Result And Phase 3 Subplan Review Iteration 1

Reviewer: Claude Opus via `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh`

Scope: attempted exact two-file read-only review of:

- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase2-fixed-randomness-tensorization-result-2026-07-02.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase3-rk4-loop-hygiene-subplan-2026-07-02.md`

Verdict: no verdict; interrupted after bounded polling with no useful output.

Interpretation:

- Treat as prompt/scope friction, not a network failure.  A fresh small Claude
  probe had already returned `CLEAN_XLA_CURRENT_PROBE_OK`, and earlier
  fixed-path reviews returned verdicts.

Next prompt repair:

- Use a compact embedded packet containing the Phase 2 result summary and Phase
  3 plan summary, with no file reads requested.

## Phase 2 Result And Phase 3 Subplan Review Iteration 2

Reviewer: Claude Opus via embedded no-file packet.

Verdict: `VERDICT: REVISE`

Key finding:

- The RK4 parity criterion was underspecified. Refactoring forward and VJP
  together could preserve internal agreement while drifting from pre-change
  semantics.

Repair:

- Patched Phase 3 subplan to require an independent test-local RK4 reference
  for primal and aux parity.
- Patched VJP check to compare the edited VJP against `tf.GradientTape` on the
  independent reference forward map for points, kappa, and nu.
- Added a stricter Phase 3 scope guard limiting implementation edits to the two
  RK4 symbols, focused tests, audit expectations, and phase artifacts.

## Phase 3 Patch Review

Reviewer: Claude Opus via embedded no-file packet.

Verdict: `VERDICT: AGREE`

Key finding:

- The previous RK4 parity blocker was resolved by requiring an independent
  reference, tape-based VJP comparison for points/kappa/nu, aux parity, and a
  narrow scope guard.

## Phase 3 Result And Phase 4 Subplan Review

Reviewer: Claude Opus via `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh`

Scope: exact two-file read-only review of:

- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase3-rk4-loop-hygiene-result-2026-07-02.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-manual-scan-hygiene-subplan-2026-07-02.md`

Verdict: `VERDICT: AGREE`

Key findings:

- Phase 3 result does not overclaim; it correctly keeps `FAIL_CURRENT_ROUTE`.
- Phase 4 scope is bounded to manual time scan only.
- Parity is sufficient for semantic preservation if the comparator is captured
  pre-edit as a test-local reference or frozen fixture.
- Phase 4 result should state which comparator was used and report exact
  value/score differences.

## Phase 4 Result And Phase 5 Subplan Review Iteration 1

Reviewer: Claude Opus via embedded no-file packet after exact fixed-path review
hung.

Probe status:

- Fresh health probe returned `CLEAN_XLA_CURRENT_PROBE_OK`.
- Exact two-file fixed-path review of the Phase 4 result and Phase 5 subplan
  produced no useful output after bounded polling and was interrupted.
- Embedded packet review returned a verdict.

Verdict: `VERDICT: REVISE`

Key findings:

- Phase 4 is properly closed as a bounded manual-scan migration and does not
  overclaim clean-XLA, GPU, or HLO evidence.
- Phase 5 has an artifact coverage gap: it targets
  `_filterflow_streaming_finite_sinkhorn_potentials_total_vjp` but did not
  explicitly require a dedicated total-VJP parity artifact.
- Phase 5 had a syntax-specific stop condition; it must block semantic Python
  step iteration and Python Tensor state accumulation in targeted helpers, not
  only the literal tokens `range(steps)`, `states = []`, and
  `states.append(...)`.

Repair:

- Patched the Phase 5 subplan to require focused total-VJP parity against the
  pre-refactor Python-loop reference or frozen fixture.
- Patched the Phase 5 evidence contract and implementation details to state
  the semantic rule: no Python loop may perform Sinkhorn step iteration, and no
  Python container may accumulate per-step TensorFlow state in targeted helper
  symbols.

## Phase 5 Subplan Patch Review Iteration 2

Reviewer: Claude Opus via embedded no-file packet.

Verdict: `VERDICT: AGREE`

Key findings:

- The total-VJP parity blocker is resolved because the subplan now requires
  explicit parity for
  `_filterflow_streaming_finite_sinkhorn_potentials_total_vjp`, includes it in
  the primary criterion, makes failure a veto, carries it into handoff, and
  includes it in stop conditions.
- The semantic loop/state-hygiene blocker is resolved because the subplan now
  forbids Python step iteration and Python Tensor state accumulation in the
  targeted helper symbols, with literal token checks only as examples/audit
  anchors.

Caveat:

- Execution must freeze or preserve the parity reference so it matches exact
  pre-refactor semantics.

## Phase 5 Result And Phase 6 Subplan Review Iteration 1

Reviewer: Claude Opus via embedded no-file packet.

Verdict: `VERDICT: REVISE`

Key findings:

- Phase 5 is closed for loop/state mechanics only, not for route-level score
  correctness.
- Phase 6 route-selection guard is directionally correct because it requires
  `transport_ad_mode="full"` and the total-VJP transport helper.
- Phase 6 needs an explicit actual executed route/call-path artifact, not only
  config metadata.
- Phase 6 HLO/compiler pass/veto signatures were underspecified.
- Phase 6 result must require a run manifest and decision table.
- If the trusted GPU probe fails, Phase 6 must stop immediately and classify
  the result as environment-blocked, not route evidence.

Repair:

- Patched the Phase 6 subplan to require actual call-path evidence, source
  anchors or runtime counters, concrete `while`/`While`/`WhileRegion` and
  retrace/compiler metrics, a run manifest, a decision table, and an explicit
  environment-blocked stop classification for failed trusted GPU probes.

## Phase 6 Subplan Patch Review Iteration 2

Reviewer: Claude Opus via embedded no-file packet.

Verdict: `VERDICT: AGREE`

Key findings:

- The executed route/call-path artifact blocker is resolved.
- The concrete HLO/compiler pass-veto signature blocker is resolved.
- The run manifest and decision table requirement is resolved.
- Trusted GPU probe failure is now correctly classified as an immediate
  environment-blocked stop, not negative route evidence.

Caveat:

- Source-anchored static call-path evidence is weaker than runtime-observed
  call-path evidence; the result note must state which kind was obtained.

## Phase 6 Result And Phase 7 Subplan Review Iteration 1

Reviewer: Claude Opus via embedded no-file packet.

Verdict: `VERDICT: REVISE`

Key findings:

- Phase 6 is properly closed for the narrow compiler-evidence objective only.
- Phase 7 needs runtime-emitted route manifest evidence for the exact executed
  scalar, not only config knobs or prior static anchors.
- Phase 7 repeat determinism needs an explicit pass rule.
- Phase 7 compile/HLO behavior veto was too vague and movable.
- Phase 7 result artifact contents must explicitly include a run manifest and
  decision table.

Repair:

- Patched Phase 7 to require a runtime route manifest with selected helper
  path, stopped-key score-use flag, source anchors or runtime counters, and
  exact scalar/FD route settings.
- Patched repeat determinism to use max absolute repeat deltas at most
  `1.0e-5` for objective, log-likelihood, mean gradient, and per-seed gradient
  under TF32/float32 GPU execution.
- Patched compile/HLO behavior into a concrete stop rule: 10-minute compile/run
  bound for the bounded fixture, or same-shape HLO size more than four times
  the Phase 6 tiny fixture.
- Patched Phase 7 result contents to require a decision table, run manifest,
  runtime route manifest summary, primary/veto status, and nonclaims.

## Phase 7 Review Invocation Probe And Patch Review

Reviewer: Claude Opus through mixed probe paths.

Probe findings:

- Claude worker health probe returned `CLEAN_XLA_CURRENT_PROBE_OK`, but output
  flushed only after the no-output wait was interrupted.
- Direct `claude -p` health probe returned `DIRECT_CLAUDE_PROBE_OK`.
- Fixed-path read-only review of the Phase 7 subplan hung/no-output and was
  stopped.
- Embedded bounded packet review returned usable verdicts.

Interpretation:

- Claude was reachable. The fixed-path review prompt was unstable for this
  session. The stable review shape was a bounded embedded packet with exact path
  provenance.

Patch review:

- First bounded packet verdict: `VERDICT: REVISE`.
- Repair: added a fixed same-scalar FD acceptance rule, same-process warm-call
  repeat-determinism scope, and exact HLO comparator
  `hlo_text_length = 27766809`.
- Minimal repaired packet verdict: `VERDICT: AGREE`.

## Phase 7 Execution Result Pending Review

Reviewer: Claude Opus via embedded bounded packet.

Codex result classification:

- Phase 7 status: `BLOCKED_FD_SENTINEL`.
- Route/GPU/repeat/HLO evidence passed.
- Same-scalar FD sentinel failed for `log_obs_noise_scale`.
- The closest miss was absolute error `0.10050010681152344` against
  predeclared tolerance `0.09968621826171875`.
- Because the threshold was predeclared, Codex stopped rather than changing the
  tolerance or handing off to Phase 8.

Verdict: `VERDICT: AGREE`

Claude review summary:

- The classification is correct under the predeclared Phase 7 gate because all
  required items had to pass, including the same-scalar FD sentinel.
- The result is boundary-safe because it does not widen the tolerance after
  seeing the result and does not hand off to Phase 8 on incomplete evidence.
- The correct interpretation is not that the whole route is disproven, but that
  Phase 7 promotion is blocked by the unresolved `log_obs_noise_scale`
  discrepancy and needs a focused Phase 7a repair/investigation artifact.

## Phase 7 Owner Acceptance Override

Reviewer: N/A. This is owner direction, not a Claude authorization.

Owner decision:

- On 2026-07-03, the owner approved accepting and promoting the Phase 7 bounded
  result as closed enough and not worth extra repair effort.

Codex action:

- Updated the Phase 7 result and JSON to `OWNER_ACCEPTED_WITH_FD_WAIVER`.
- Preserved the original evidence: the preregistered same-scalar FD gate did
  not pass for `log_obs_noise_scale`.
- Preserved `primary_pass=false` in the machine-readable artifact and added
  `promoted_by_owner_acceptance=true`.

Boundary:

- This owner acceptance overrides the stop-for-repair decision for this bounded
  clean-XLA fixture only. It does not convert the failed FD gate into a pass and
  does not authorize HMC-readiness, exact nonlinear likelihood correctness,
  all-model validation, or treating stopped-key partial derivatives as scores.
