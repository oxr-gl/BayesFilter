# Claude Review Ledger: Total-VJP GPU/XLA Validation

Date: 2026-07-01

Status: `COMPLETE`

Claude is read-only reviewer only.  Codex remains supervisor and executor.

## Reviews

### Plan Review Iteration 1

Prompt:

- Asked Claude to review the master program, visible runbook, Phase 0 subplan,
  Phase 1 subplan, and execution ledger for material blockers.

Verdict:

- `VERDICT: REVISE`

Material finding:

- Phase 0 did not require a static proof that the legacy selector
  `manual_streaming_finite_sinkhorn_stopped_scale_keys` paired with
  `transport_ad_mode="full"` dispatches to the corrected total-derivative
  helper.  Metadata alone was insufficient.

Patch response:

- Phase 0 now requires static dispatch proof with exact code anchors before
  Phase 1 can launch.
- Phase 1 now treats absence of the dispatch proof as a veto even if output
  metadata says `transport_ad_mode="full"`.

### Phase 1 Result Review Packet Pending

Scope:

- Phase 1 trusted GPU/XLA smoke result.
- Phase 2 skipped result.
- Refreshed Phase 3 particle ladder subplan.

Question for Claude:

- Does the Phase 1 result satisfy the reviewed gate?
- Is skipping Phase 2 justified by the Phase 1 result?
- Is the Phase 3 subplan consistent, feasible, and bounded, without overclaiming
  the tiny smoke?

Status:

- `COMPLETE`

Verdict:

- `VERDICT: AGREE`

Review summary:

- Phase 1 closure as passed is supported by the result and JSON artifact:
  status pass, primary pass true, GPU placement, XLA JIT, full route metadata,
  finite objective, finite gradients, finite MCSE, and connected gradients.
- Phase 2 skip is justified because the existing harness successfully exercised
  the corrected full route; the prior blocker was approval/launch plumbing.
- Phase 3 is safe to launch under the stated gates.  Claude noted that the
  subplan preserves trusted GPU execution, `float32`/TF32, manual-reverse XLA,
  streaming transport, `transport_ad_mode="full"`, exact JSON gates, and
  nonclaims.

### Phase 3 Result And Phase 4 Subplan Review

Prompt:

- Asked Claude to review the Phase 3 result, Phase 3 rung JSON artifacts, the
  refreshed Phase 4 subplan, and the visible execution ledger.

Verdict:

- `VERDICT: AGREE`

Review summary:

- Phase 3 is properly closed as passed at the right scope: GPU/XLA/TF32
  viability through `N=1000,T=3`, not HMC direction validity or posterior
  correctness.
- Phase 4 is a valid same-scalar direction diagnostic because it uses the same
  regression-FD runner, `--fd-mode enabled`, raw directions only,
  manual-reverse XLA, streaming transport, and `transport_ad_mode="full"`.
- Claude confirmed the legacy selector-name ambiguity remains accounted for:
  the derivative claim depends on `transport_ad_mode="full"` plus the Phase 0
  dispatch proof, not the stale gradient-mode string.

### Phase 4 Batched-Theta FD Repair Review

Prompt:

- Asked Claude to review the serial-FD runtime blocker and the proposed
  `--fd-evaluation-mode batched-theta --theta-offset-batch-size 3` repair.

Verdict:

- `VERDICT: AGREE`

Review summary:

- Claude found that batched-theta mode builds the same theta rows as serial FD
  and changes only the objective-evaluation shape.
- Claude found that the batching helper repeats the same fixed inputs and seed
  structure across offset rows, preserving per-row scalar semantics within the
  reviewed scope.
- Claude agreed the ledger records the interrupted serial attempt as a
  harness/runtime blocker, not derivative evidence.

### Phase 4 Result And Final Label Review

Prompt:

- Asked Claude to review the Phase 4 result, Phase 4 JSON, Phase 5 subplan,
  and visible ledger for rule application and overclaiming.

Verdict:

- `VERDICT: AGREE`

Review summary:

- Claude agreed Phase 4 applied the predeclared direction rule correctly.
- Claude agreed the kappa one-window caveat and the serial-FD runtime caveat are
  plainly recorded.
- Claude agreed the final label
  `GPU_XLA_VIABLE_TOTAL_DERIVATIVE_EXPERIMENTAL_ROUTE_WITH_RAW_DIRECTION_GATE_PASS`
  is supported without overclaiming.
