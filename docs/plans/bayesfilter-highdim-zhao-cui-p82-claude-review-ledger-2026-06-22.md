# P82 Claude Review Ledger

Date: 2026-06-22

Status: INITIALIZED

## Review Protocol

Claude Opus may be used only as a read-only reviewer.

Use the trusted worker wrapper:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name <short-review-name> \
  --model opus \
  --effort max \
  "<bounded prompt>"
```

Do not send whole files.  Use compact path-anchored fact packets.  Require a
final line of exactly `VERDICT: AGREE` or `VERDICT: REVISE`.

If Claude stalls, send:

```text
READ-ONLY PROBE. Reply exactly PROBE_OK.
```

If the probe responds, redesign the prompt.

Use the one-path review pattern from `AGENTS.md` and `memory.md` whenever a
single result/subplan can answer the gate.  Do not send artifact packets or
large path lists as the first attempt.

## Reviews

### p82-p0-bootstrap-review-r1

Status: `VERDICT: AGREE`

Scope: compact P82 bootstrap fact packet covering master program, visible
runbook, P0 result, P1 read-only inventory subplan, and corrected comparator /
regression-FD protocol.

Key findings:

- no wrong-baseline blocker;
- P1 may launch as read-only inventory;
- `> 2 combined SE` should be kept as a triage heuristic rather than a
  calibrated hypothesis test;
- `<= 2 combined SE` is not certification of either method;
- P7 should state seed-pairing, independence, and trimming assumptions before
  interpreting combined SE.

Action:

- Patched master program, runbook, and P0 result to preserve this caution
  before P1 launch.

### p82-p1-p2-handoff-review-r1

Status: `VERDICT: REVISE`

Scope: compact P1 inventory and P2 harness-repair subplan fact packet.

Key findings:

- P1/P2 gate is coherent only as a harness-repair gate, not as
  comparator-validation.
- P2 must explicitly state that regression FD is a diagnostic construction,
  not an oracle, not promotion evidence by itself, and not a substitute for P3
  Zhao-Cui analytical-route audit/repair.
- P2 needs deterministic tie-breaking for tied highest/lowest mean objective
  values.
- P2 needs explicit raw-record preservation and exact 11-point OLS/slope-SE
  test invariants.
- P2 must avoid authorizing N=1000 or N=10000 governed research jobs.

Action:

- Patched P1 result and P2 subplan with the requested guardrails before P2 code
  edits.

### p82-p1-p2-handoff-review-r2

Status: `VERDICT: AGREE`

Scope: focused review of R1 guardrail patches only.

Key findings:

- R1 concerns are closed.
- Regression FD is now explicitly diagnostic-only and not a substitute for P3.
- Deterministic y-trim tie-breaking, raw-record preservation, exact 13-to-11
  OLS/slope-SE tests, and no N=1000/N=10000 research-run authorization are now
  present in the P2 subplan.

Action:

- P2 code edits may begin under the reviewed subplan boundaries.

### p82-p2-p3-handoff-review-r1

Status: `VERDICT: REVISE`

Scope: compact P2 implementation result and P3 analytical-route subplan fact
packet.

Key findings:

- P2 harness implementation is protocol-consistent on the reviewed facts.
- Because the harness default remains backward-compatible `offset`, every
  governed P82 FD run must explicitly pass `--trim-extreme-mode value` and
  record 13 raw points, 11 fit points, and y-based mean-over-seed trimming.
- P3 needs a stricter no-edit discovery-before-edit gate.
- P3 must treat FD/JVP agreement as explanatory only, classify routes per
  variant, block unsupported multistate comparator promotion, and verify
  backend labels after any edit.

Action:

- Patched the P82 master/runbook/P2 result to pin `--trim-extreme-mode value`
  for governed FD runs.
- Patched the P3 subplan with explicit no-edit discovery, per-variant
  classification, hard blocker, backend-label gate, and artifact obligations.

### p82-p2-p3-handoff-review-r2

Status: `VERDICT: REVISE`

Scope: focused review of R1 guardrail patches.

Key findings:

- P2 governed FD pin and metadata rule are sufficient.
- P3 still needed backend-label verification elevated into explicit required
  checks.
- P3 work sequence still had a loophole allowing a missing multistate
  comparator to be invented from derivation artifacts.

Action:

- Patched P3 required checks to require targeted backend-label verification
  after any comparator-route edit or approval.
- Narrowed the analytical-helper exception to helpers inside an already
  implemented, source-backed, already-classified multistate comparator route;
  it cannot create a missing comparator route.

### p82-p2-p3-handoff-review-r3

Status: `VERDICT: AGREE`

Scope: focused review of the two R2 residual blockers.

Key findings:

- Backend-label verification is now an explicit required check.
- The analytical-helper exception no longer permits invention of a missing
  source-backed multistate comparator route.
- No remaining material blocker was found for the read-only P3 inventory step.

Action:

- P3 no-edit inventory may begin under the reviewed subplan boundaries.

### p82-p3-blocker-review-r1/r2

Status: stalled after no output; probe succeeded.

Scope: attempted compact P3 blocker route-classification reviews.

Action:

- Interrupted the stalled review attempts rather than treating them as evidence.
- Ran `p82-p3-claude-probe`, which returned `PROBE_OK`.
- Redesigned the prompt twice, reducing it to the decisive protocol rule and
  anchors.

### p82-p3-blocker-review-r3

Status: `VERDICT: AGREE`

Scope: minimal read-only review of the P3 stop decision.

Key findings:

- The multistate target derivative route is explicitly
  ForwardAccumulator/JVP-backed in `bayesfilter/highdim/filtering.py`.
- Given the P82 rule that the promoted Zhao-Cui comparator must be analytical
  and source-backed while JVP/autodiff remains diagnostic-only, and given that
  P12/P15/P16 are derivation/specification rather than a ready wired multistate
  SIR d=18 comparator, stopping at P3 with
  `BLOCK_P82_P3_ANALYTICAL_COMPARATOR_ROUTE_NOT_READY` before GPU work is
  consistent.

Action:

- P3 blocker and stop handoff remain in force.

### p82-p5-manual-streaming-wiring-review-r1

Status: `VERDICT: AGREE`

Scope: one-path read-only review of
`docs/plans/bayesfilter-highdim-zhao-cui-p82-phase5-manual-streaming-gradient-wiring-result-2026-06-23.md`.

Key findings:

- The result consistently scopes P5 to CLI/API forwarding and metadata capture.
- It preserves non-claims for P82 validation, GPU feasibility, FD agreement,
  Zhao-Cui source-faithfulness, and production readiness.
- The local evidence matches the wiring-only objective: parser acceptance,
  forwarding via test double, metadata recording, compile, focused pytest, diff
  hygiene, and route scan.
- The handoff is bounded to a separate tiny trusted GPU smoke subplan and does
  not authorize immediate P82 validation.

Action:

- P5 may close as reviewed-passed.
- P6 may be drafted as a separate tiny trusted GPU smoke phase.

### p82-p6-p8-completion-plan-review-r1-r4

Status: `VERDICT: AGREE` after R4

Scope: one-path bounded review of
`docs/plans/bayesfilter-highdim-zhao-cui-p82-p6-p8-completion-plan-2026-06-23.md`,
with inspection limited to cited P6-P9 subplans as needed.

Key findings and repairs:

- R1 required P8 to explicitly pass `--fd-mode enabled`; patched.
- R1 required P7 N10000 progress JSON to be conditional on launching the
  N10000 rung; patched.
- R2 required P7/P8 ledger and stop-handoff artifacts; patched.
- R2 required P7 to wait for P6 result plus one-path Claude `VERDICT: AGREE`;
  patched.
- R2 required P7/P8 primary criteria to name the full route tuple; patched.
- R3 required P6 primary/veto criteria to verify
  `transport_plan_mode=streaming`; patched.
- R4 found no remaining material internal-consistency blocker.

Action:

- Completion plan may proceed to P6 execution.

### p82-p6-execution-review-r1

Status: `VERDICT: AGREE`

Scope: one-path read-only review of
`docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-result-2026-06-23.md`.

Key findings:

- No material scope creep: the result stays within tiny GPU route-execution
  smoke and preserves non-claims for P82 validation, FD agreement, N10000
  feasibility, Zhao-Cui comparator readiness, HMC/default readiness,
  production readiness, and scientific superiority.
- Required P6 evidence is present in-file: trusted GPU preflight, exact smoke
  command, route settings, exit-0 claim, finite objective/gradient values, and
  GPU placement.
- No unsafe handoff found: P7 is framed as future feasibility work, not as
  already established.

Action:

- P6 may close as reviewed-passed.
- P7 actual-gradient feasibility may begin under the reviewed subplan.

### p82-p9-closeout-review-r1-r2

Status: `VERDICT: AGREE` after R2

Scope: one-path read-only review of
`docs/plans/bayesfilter-highdim-zhao-cui-p82-phase9-closeout-result-2026-06-23.md`.

Key findings and repairs:

- R1 found no overclaiming or hidden N10000 failure, but requested stronger
  provenance: governing plan path and run manifest for the failed N10000
  command/environment.
- Patched the closeout with the reviewed completion-plan path, git commit,
  Python/TensorFlow environment, GPU status, seeds, failed N10000 command, and
  artifact/stderr status.
- R2 returned `VERDICT: AGREE`; no remaining findings.

Action:

- P82 closeout may stand at
  `P82_STOPPED_AT_P7_N10000_GPU_OOM_P8_NOT_RUN`.
