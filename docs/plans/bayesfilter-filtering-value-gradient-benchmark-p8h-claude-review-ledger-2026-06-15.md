# P8h Claude Review Ledger

Date: 2026-06-15

Status: `CLOSED_PHASE10_BOUNDARY_REVIEWED`

Claude is a read-only reviewer only. Claude cannot authorize execution,
GPU/CUDA usage, package installation, model-file changes, funding/product
capability boundaries, or scientific-claim promotion.

## Review Rounds

| Round | Scope | Prompt artifact | Verdict | Disposition |
|---:|---|---|---|---|
| 0 | P8h master/runbook/subplans | N/A | `PENDING` | Awaiting local checks and bounded review prompt. |
| 1 | P8h master/runbook/subplans | bounded path-only Claude worker prompt | `BLOCKED_BY_APPROVAL_POLICY` | Escalated Claude worker was rejected by approval reviewer because private repository planning documents would be exposed to an external Claude service. Do not retry until the user explicitly approves after being informed of this risk. |
| 2 | P8h master/runbook/subplans | bounded path-only Claude worker prompt after user approval | `VERDICT: REVISE` | Material blockers: HMC entry could follow diagnostic-only gradient route; Phase 0 doc/build gates too weak; Phases 5-8 missing mandatory route/manifest preservation. Patched subplans visibly and rerunning focused checks/review. |
| 3 | P8h master/runbook/subplans | bounded path-only Claude worker prompt after user approval | `VERDICT: REVISE` | Iteration-1 blockers closed, but new transit blocker found: Phase 8 could still be reached without reviewed Phase 5 value/filtering pass for exact route/count. Patched Phase 5 handoff, Phase 7 entry/handoff/veto, Phase 8 entry/veto, and Phase 0 stale wording; rerunning focused checks/review. |
| 4 | P8h master/runbook/subplans | bounded path-only Claude worker prompt after user approval | `VERDICT: AGREE` | No material blockers. Planning gate is ready to launch Phase 0 under the visible runbook. |
| 5 | Phase 0 result and Phase 1 subplan | bounded path-only Claude worker prompt after user approval | `VERDICT: AGREE` | No material blockers. Phase 0 result accepted; Phase 1 governance reset may launch. |
| 6 | Phase 1 result and Phase 2 subplan | bounded path-only Claude worker prompt after user approval | `VERDICT: REVISE` | Phase 1 result accepted, but Phase 2 subplan had too narrow non-claim boundary, weak route-role inheritance, and insufficient exact entry-point coverage. Patched Phase 2 subplan; rerunning focused checks/review. |
| 7 | Phase 1 result and Phase 2 subplan | bounded path-only Claude worker prompt after user approval | `VERDICT: REVISE` | Remaining Phase 2 wording blocker: `GPU scaling` was missing from the inherited non-claim row. Patched wording; rerunning focused checks/review. |
| 8 | Phase 1 result and Phase 2 subplan | bounded path-only Claude worker prompt after user approval | `VERDICT: AGREE` | No material blockers. Phase 1 result accepted; Phase 2 may launch as design-contract-only. |
| 9 | Phase 2 result, design contract, and Phase 3 subplan | bounded path-only Claude worker prompt after user approval | `VERDICT: REVISE` | Material blocker: raw Sinkhorn and annealed transport matrices used different orientation/normalization conventions, so covariance carry needed one canonical `A[target, source]` contract. Phase 3 subplan also needed exact files, commands, and P8g quarantine. Patched Phase 2 contract/result and Phase 3 subplan; rerunning focused checks/review. |
| 10 | Phase 2 result, design contract, and Phase 3 subplan | bounded path-only Claude worker prompt after user approval | `VERDICT: AGREE` | No material blockers. Canonical `A[target, source]` convention, same-matrix particle/covariance carry, P8g quarantine, and Phase 3 execution details accepted. Phase 2 may close and Phase 3 may launch under Codex supervision. |
| 11 | Phase 3 implementation result, diff, smoke artifacts, and Phase 4 subplan | bounded path-only Claude worker prompt after user approval | `VERDICT: REVISE` | Material blocker: canonical transport shape/row-sum validity was diagnosed but not fail-closed before state mutation. Phase 4 commands also relied on CLI default rather than pinning exact P8h route. Patched fail-closed validation, added malformed-transport regression, pinned Phase 4 `--p8h-resampling-route`, and refreshed CPU/GPU smoke artifacts. Rerunning checks/review. |
| 12 | Phase 3 repaired implementation/result and Phase 4 subplan | bounded path-only Claude worker prompt after user approval | `VERDICT: AGREE` | No material blockers. Fail-closed canonical transport validation, malformed-transport regression, pinned Phase 4 route commands, refreshed CPU/GPU artifacts, and nonclaim boundaries accepted. Phase 3 may close and Phase 4 may launch. |
| 13 | Phase 10 plan refresh | bounded path-only Claude worker prompt after user approval | `VERDICT: REVISE` | Patched explicit reviewed Phase 9 handoff entry, manifest coverage for code/test/result/ledger/handoff/environment evidence, and narrower reproduction wording. |
| 14 | Phase 10 plan refresh repair | bounded path-only Claude worker prompt after user approval | `VERDICT: AGREE` | No material blockers. Phase 10 repo-hygiene gate accepted as boundary review without commit/push authority. |
| 15 | Phase 4 result and Phase 5 subplan | bounded prompt after user approval | `PROMPT_REDESIGNED_AFTER_PROBE` | Broad prompt stayed silent; small Claude probe returned `PROBE_OK`, so the review prompt was narrowed. |
| 16 | Phase 4 result and Phase 5 subplan | narrowed bounded prompt after user approval | `VERDICT: REVISE` | Phase 4 accepted, but Phase 5 needed historical-only P8g baseline wording, a hard implementation/test gate, deterministic thresholds, and explicit GPU-scaling non-claim. |
| 17 | Phase 5 subplan repair | narrowed bounded prompt after user approval | `VERDICT: AGREE` | No material blockers. Phase 5 may implement the P8h-specific tuning surface and run Stage 0 under trusted GPU execution. |
| 18 | Phase 5 result and Phase 6 subplan | bounded prompt after user approval | `VERDICT: REVISE` | Phase 5 result accepted, but Phase 6 stop conditions and artifact dates needed repair. |
| 19 | Phase 6 subplan repair | bounded prompt after user approval | `VERDICT: AGREE` | No material blockers. Phase 6 may run the trusted GPU OT-gradient diagnostic. |
| 20 | Phase 6 result and Phase 7 subplan | bounded prompt after user approval | `VERDICT: REVISE` | Phase 6 result accepted, but Phase 7 needed explicit reviewed Phase 5/6 verification, exact configuration pinning, and numerical-invalidity veto/stop coverage. |
| 21 | Phase 7 subplan repair | bounded prompt after user approval | `VERDICT: AGREE` | No material blockers. Phase 7 may run trusted GPU performance/scaling diagnostics for the exact route/count. |
| 22 | Phase 7 result | broad prompt after user approval | `PROMPT_REDESIGNED_AFTER_PROBE` | Broad result/subplan prompt stayed silent; small Claude probe returned `PROBE_OK`, so the review was split into narrower scopes. |
| 23 | Phase 7 result | narrowed bounded prompt after user approval | `VERDICT: AGREE` | No material blockers. Phase 7 result accepted as small-HMC-feasibility profile only, with no HMC readiness, full-scaling, or ranking claim. |
| 24 | Phase 8 subplan | narrowed bounded prompt after user approval | `VERDICT: REVISE` | Material blockers: tests did not explicitly require coordinate/trusted-GPU device-gate rejection, and CPU-only wording was too permissive for a GPU-only success artifact. |
| 25 | Phase 8 subplan repair | focused bounded prompt after user approval | `VERDICT: AGREE` | No material blockers. Phase 8 may implement and run the Tier-0 fixed-kernel HMC execution smoke under the reviewed boundary. |
| 26 | Phase 8 result and Phase 9 subplan | bounded prompt after user approval | `VERDICT: REVISE` | Phase 8 result accepted conditionally, but Phase 9 subplan omitted explicit posterior-convergence/NUTS/valid-tuning/stochastic-gradient nonclaim checks and Phase 8 needed row-alias provenance. |
| 27 | Phase 8 result and Phase 9 subplan repair | focused bounded prompt after user approval | `VERDICT: AGREE` | No material blockers. Phase 8 result is accepted as Tier-0 HMC execution-smoke evidence only; Phase 9 closeout may launch. |
| 28 | Phase 9 result, artifact index, reset/handoff, and Phase 10 subplan | bounded prompt after user approval | `VERDICT: REVISE` | Material blockers: artifact index omitted the Phase 9 result/reset memo and lacked explicit environment/run-manifest disposition for Phase 10 input. |
| 29 | Phase 9 artifact-index repair | focused bounded prompt after user approval | `VERDICT: AGREE` | No material blockers. Phase 9 closeout accepted; Phase 10 repo-hygiene/commit-boundary review may launch. |
| 30 | Phase 10 boundary manifest/result | bounded prompt after user approval | `VERDICT: REVISE` | Material blocker: Phase 10 result said manifest JSON validation passed while manifest still recorded that validation as pending. |
| 31 | Phase 10 boundary repair | focused bounded prompt after user approval | `VERDICT: AGREE` | No material blockers. Phase 10 boundary accepted; P8h gated program can close without commit/push. |
| 32 | Phase 11 broad closure-sync review | bounded prompt after user approval | `PROMPT_REDESIGNED_AFTER_PROBE` | Broad path list produced no usable output. A small probe returned `PROBE_OK`, so the review prompt was narrowed. |
| 33 | Phase 11 narrowed closure-sync review | focused bounded prompt after user approval | `VERDICT: AGREE` | No material blockers. Phase 11 closure sync accepted as bookkeeping-only; remaining scientific gaps should move to a new gated follow-on program. |
