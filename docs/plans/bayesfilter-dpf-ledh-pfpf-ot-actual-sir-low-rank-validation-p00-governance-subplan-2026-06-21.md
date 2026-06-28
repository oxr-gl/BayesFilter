# P00 Governance And Skeptical Audit Subplan

Status: `DRAFT_FOR_REVIEW`

## Phase Objective

Establish the real-workload validation evidence contract, ownership boundary,
source anchors, skeptical plan audit, approval boundary, and review protocol
before implementation or benchmark execution.

## Entry Conditions Inherited From Previous Phase

This is the first phase. It inherits the user request to execute a governed
actual-SIR d18 low-rank validation program and the repository policies in
`AGENTS.md`.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-master-program-2026-06-21.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-visible-gated-execution-runbook-2026-06-21.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-visible-execution-ledger-2026-06-21.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-claude-review-ledger-2026-06-21.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-visible-stop-handoff-2026-06-21.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p00-governance-result-2026-06-21.md`

## Required Checks, Tests, Reviews

- Confirm source anchor paths exist.
- Confirm the existing actual-SIR `N=50000` result is the real workload anchor.
- Confirm the existing low-rank result is synthetic/LGSSM-shaped and cannot by
  itself support actual-SIR claims.
- Run local path/contract checks with `rg` and `sed`.
- Claude read-only review of the master program and P00/P01 plan paths until
  `VERDICT: AGREE` or max five rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the planned validation capable of answering whether low-rank helps actual-SIR d18 LEDH/PFPF-OT large-N efficiency? |
| Baseline/comparator | Existing streaming actual-SIR benchmark route. |
| Primary pass criterion | Source anchors exist, owned write set is bounded, skeptical audit passes, and Claude agrees the plan is feasible and boundary-safe. |
| Veto diagnostics | Missing real workload anchor, wrong comparator, missing stop conditions, proxy runtime promoted ahead of validity/comparability, unsupported claim language, or shared contract change required. |
| Explanatory diagnostics | Existing high-N runtime/memory context and prior low-rank synthetic speed evidence. |
| Not concluded | No implementation correctness, no runtime result, no actual-SIR efficiency claim. |
| Artifact | P00 result and Claude review ledger. |

## Forbidden Claims/Actions

- Do not claim low-rank helps actual-SIR before actual-SIR route artifacts pass.
- Do not run long GPU benchmarks in P00.
- Do not modify public exports, shared schemas, or existing benchmarks.
- Do not send full file contents or whole repo to Claude.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if P00 result is `PASS`, the Claude review has
converged or a nonmaterial review waiver is documented, and the next subplan is
present and internally consistent.

## Stop Conditions

- `BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED` if implementation requires shared
  API/schema/export changes.
- Stop for human direction if Claude and Codex do not converge after five
  review rounds for the same blocker.
- Stop if source anchors are missing or contradict the planned comparator.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write the P00 phase result.
3. Draft or refresh P01.
4. Review P01 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
