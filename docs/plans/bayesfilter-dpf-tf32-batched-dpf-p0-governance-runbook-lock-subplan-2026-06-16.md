# Phase 0 Subplan - Governance And Runbook Lock - 2026-06-16

## Phase Objective

Create a clean, visible, recoverable governance layer for the TF32 batched DPF
program after the previous execution became tangled.

This phase creates and reviews the master program, visible runbook, execution
ledger, stop handoff, and Phase 1 subplan. It does not change algorithm code,
run benchmarks, or make scientific/performance claims.

## Entry Conditions Inherited From Previous Phase

- No previous phase in this clean run.
- Active reset memo is
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-reset-memo-2026-06-16.md`.
- Supporting DPF reset memo is
  `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-reset-memo-2026-06-15.md`.
- Worktree may be dirty; unrelated user/session changes must be preserved.
- Claude may be used only as read-only reviewer.

## Required Artifacts

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-master-program-2026-06-16.md`
- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-visible-gated-execution-runbook-2026-06-16.md`
- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-visible-execution-ledger-2026-06-16.md`
- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-visible-stop-handoff-2026-06-16.md`
- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p0-governance-runbook-lock-result-2026-06-16.md`
- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p1-implementation-precision-inventory-subplan-2026-06-16.md`
- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p0-claude-review-round-01-2026-06-16.md`

## Required Checks, Tests, And Reviews

Local checks:

1. Verify the required Phase 0 and Phase 1 artifact paths exist.
2. Verify no unresolved template placeholders remain in the new artifacts.
3. Verify the master/runbook/subplans mention TF32 scope, independent rows, and
   forbidden HMC/default-readiness claims.
4. Verify the runbook preserves visible foreground execution and forbids
   detached or nested supervisors.

Review:

1. Run Claude Opus max effort as read-only reviewer on concise named paths.
2. Save the review output as the required Claude review artifact.
3. Continue only if the review ends with `VERDICT: AGREE`.
4. If review says `VERDICT: REVISE`, patch the same artifacts visibly, rerun
   focused local checks, and retry review. Stop after five rounds for the same
   blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the governance artifacts sufficient and safe for a fresh visible execution of TF32 batched DPF work? |
| Baseline/comparator | The reset memos, visible runbook template, project AGENTS policy, and prior TF32 precision/capacity result notes. |
| Primary pass criterion | All required artifacts exist, local checks pass, Claude read-only review returns `VERDICT: AGREE`, and the Phase 0 result records exact Phase 1 handoff conditions. |
| Veto diagnostics | Missing artifact; unresolved template placeholder; Claude used as executor; detached execution allowed; HMC/default-readiness claim; single-filter multi-GPU sharding claim; missing stop condition; missing Phase 1 handoff. |
| Explanatory diagnostics | Wording clarity, artifact naming, and stream-output discipline. |
| Not concluded | No algorithm correctness, speed improvement, HMC readiness, production readiness, or public API readiness. |
| Artifact preserving result | Phase 0 result file and Claude review artifact. |

## Skeptical Audit Before Execution

- Wrong baseline: use the two reset memos and prior TF32 result notes, not the
  tangled live chat state.
- Proxy metric risk: no timings, memory readings, or smoke outputs are promoted
  in this governance phase.
- Missing stop condition: the subplan includes human-required stops and Claude
  nonconvergence stops.
- Unfair comparison: no method comparison is performed in this phase.
- Hidden assumption: independent row batching is explicitly separated from
  single-filter particle sharding.
- Stale context: all cited artifacts are dated and named; Phase 1 will refresh
  implementation inventory before code changes.
- Environment mismatch: this phase does not interpret GPU results.
- Artifact adequacy: artifact existence and placeholder checks are sufficient
  for the governance question.

Skeptical audit status: `PASSED_FOR_PHASE_0_GOVERNANCE`.

## Forbidden Claims And Actions

- Do not edit algorithm, benchmark, or test code in this phase.
- Do not launch detached execution.
- Do not run GPU benchmarks or long diagnostics.
- Do not claim HMC readiness, production readiness, public API readiness, or
  scientific correctness.
- Do not claim multi-GPU particle-cloud sharding.
- Do not let Claude edit files, run commands, or authorize phase crossing.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only after:

- Phase 0 result exists and records `PHASE_0_PASSED`;
- the visible runbook, master program, ledger, stop handoff, and Phase 1
  subplan exist;
- local checks pass;
- Claude review artifact exists and ends with `VERDICT: AGREE`;
- no human-required stop condition is active.

## Stop Conditions

Stop and write/update the stop handoff if:

- required artifacts cannot be written;
- local checks reveal a material governance inconsistency that cannot be fixed
  locally;
- Claude review does not converge after five rounds for the same blocker;
- a detached, destructive, credentialed, package-install, network-fetch, or
  product/default-policy action would be required;
- continuing would modify unrelated dirty worktree files.
