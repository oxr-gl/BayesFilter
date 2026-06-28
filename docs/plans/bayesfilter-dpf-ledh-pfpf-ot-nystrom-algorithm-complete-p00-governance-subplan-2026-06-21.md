# P00 Subplan: Governance And Source Lock

Date: 2026-06-21

Status: `READY_FOR_REVIEW`

## Phase Objective

Lock the Nystrom algorithm-complete lane scope, evidence contract, source
provenance, candidate boundaries, and next-phase handoff before implementation.

## Entry Conditions Inherited From Previous Phase

- Human directive: implement the next algorithm thoroughly before screening.
- Selected algorithm: fixed-rank Nystrom kernel Sinkhorn for LEDH-PFPF-OT.
- Current default remains streaming TF32 LEDH-PFPF-OT.
- Existing Phase 11 Nystrom diagnostic exists and is provenance, not sufficient
  algorithm completion.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-master-program-2026-06-21.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-visible-gated-execution-runbook-2026-06-21.md`
- Review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-claude-review-ledger-2026-06-21.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-visible-execution-ledger-2026-06-21.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-visible-stop-handoff-2026-06-21.md`
- P00 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p00-governance-result-2026-06-21.md`

## Required Checks, Tests, Reviews

- Local content check that every phase subplan contains the required headings.
- Local source check for existing Nystrom implementation/test/provenance files.
- Compact read-only Claude review of master/runbook/P00/P01 boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the Nystrom algorithm-complete lane well scoped and safe to launch? |
| Baseline/comparator | Current streaming TF32 default and prior Phase 11 Nystrom diagnostic as context only. |
| Primary criterion | Required plan/runbook/subplans/ledgers exist, preserve evidence boundaries, and pass local content checks plus Claude read-only review. |
| Veto diagnostics | Missing phase required headings, wrong default change, unsupported ranking/default/posterior/HMC/API claim, missing stop conditions, or unresolved Claude material finding. |
| Explanatory diagnostics | Existing Phase 11 evidence and current git status. |
| Not concluded | No algorithm viability, speedup, posterior correctness, default readiness, HMC readiness, or leaderboard ranking. |
| Artifact | P00 result file. |

## Forbidden Claims And Actions

- Do not implement or run candidate benchmarks in P00.
- Do not change defaults or public API.
- Do not rank Nystrom against low-rank, positive-feature, or streaming default.
- Do not claim dense Sinkhorn equivalence beyond future small-reference tests.

## Exact Next-Phase Handoff Conditions

P01 may begin only after:

- P00 local content checks pass;
- Claude review returns `VERDICT: AGREE` or a reviewed local waiver/blocker is
  recorded by user direction;
- P01 subplan exists and is internally consistent.

## Stop Conditions

- Required plan/runbook/subplan artifacts are missing.
- Claude review finds a material issue that cannot be patched within five
  rounds.
- The plan would require changing defaults, public API, or production claims.

