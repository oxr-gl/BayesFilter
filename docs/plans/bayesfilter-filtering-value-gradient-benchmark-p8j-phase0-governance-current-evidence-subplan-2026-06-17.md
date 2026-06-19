# P8j Phase 0 Subplan: Governance And Current Evidence Audit

metadata_date: 2026-06-17
status: DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 0
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Establish the P8j lane boundary and prove from local artifacts that SIR d18 DPF
leaderboard cells remain missing.  Phase 0 must prevent drift into the
Zhao-Cui fixed-branch/P71 lane or the monograph rewrite lane.

## Entry Conditions Inherited From Previous Phase

- P8d reset memo, current P8d runner, and current route tests are the primary
  evidence for the missing SIR d18 DPF route.
- P8g/P8h/P8i are historical non-SIR DPF/LEDH/OT provenance only and do not
  authorize treating scalar-SV DPF evidence as SIR d18 evidence.
- The user explicitly requested the missing DPF SIR d18 leaderboard lane.
- No SIR d18 DPF callback route is currently admitted by the P8d runner.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase0-governance-current-evidence-result-2026-06-17.md`
- Updated P8j visible execution ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md`
- Updated P8j Claude review ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md`
- Updated P8j stop handoff:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-stop-handoff-2026-06-17.md`
- Draft Phase 1 subplan, only if Phase 0 passes:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase1-sir-d18-dpf-callback-contract-subplan-2026-06-17.md`

## Required Checks/Tests/Reviews

Local text and code-surface checks:

```bash
rg -n "P8j|SIR d18|zhao_cui_spatial_sir_austria_j9_T20|not the Zhao-Cui fixed-branch/P71 lane|no free theta|five fixed seeds" docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-*
rg -n "SIR_ROW|def _dpf_route|def _has_dpf_route|no DPF callback route|_sir_structural|zhao_cui_spatial_sir_austria_j9_T20" scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase0-governance-current-evidence-subplan-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-gated-execution-runbook-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-stop-handoff-2026-06-17.md
```

Claude read-only review of the master program, runbook, and Phase 0 subplan is
required before Phase 0 execution.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the current repository show that DPF SIR d18 leaderboard cells are missing, and is P8j scoped correctly to close that gap without crossing claim boundaries? |
| Baseline/comparator | P8d reset memo, current P8d runner route table, and P8d route tests are primary.  P8g callback-closure material and P8h/P8i closeout handoffs are historical non-SIR provenance only. |
| Primary criterion | Local checks pass and the Phase 0 result records that `_has_dpf_route(SIR_ROW)` is currently false while P8h/P8i only tested the serious DPF route on actual SV. |
| Veto diagnostics | Any artifact treats P71 as the active lane; claims SIR DPF was already tested; authorizes theta-gradient/HMC claims for fixed-parameter SIR; drops five-seed DPF value requirement; or omits the no-free-theta boundary. |
| Explanatory diagnostics | Search hits for SIR row, existing deterministic SIR structural adapter, P8g callback-closure plan status, and current route tests. |
| Not concluded | No SIR DPF implementation, no SIR DPF numeric result, no leaderboard refresh, no particle-count adequacy, no GPU performance, no HMC readiness. |

## Forbidden Claims/Actions

- Do not edit implementation code in Phase 0.
- Do not launch DPF, GPU, tuning, HMC, or leaderboard runs in Phase 0.
- Do not claim that P8h/P8i tested SIR d18 DPF.
- Do not claim Zhao-Cui TT/SIRT source-faithfulness or MATLAB parity.
- Do not claim score/Hessian/theta-gradient/HMC readiness for fixed-parameter SIR.
- Do not stage, commit, merge, or push.

## Exact Next-Phase Handoff Conditions

Phase 1 may be drafted/reviewed only if:

- local checks pass;
- Claude returns `VERDICT: AGREE` on the P8j master/runbook/Phase 0 packet;
- Phase 0 result records the current missing SIR DPF route and exact claim
  boundaries;
- no implementation or numerical run was launched during Phase 0.

## Stop Conditions

Stop and write a blocker result if:

- local evidence contradicts the premise that SIR d18 DPF is missing;
- P8j scope cannot be separated from P71 or monograph work;
- Claude returns `VERDICT: REVISE` for an issue that cannot be patched within
  five rounds;
- executing Phase 1 would require human approval not yet granted.

## Skeptical Plan Audit

This phase could mislead us if it treats a Zhao-Cui fixed-branch SIR artifact
as DPF evidence, or if it treats actual-SV P8h/P8i DPF evidence as generic SIR
coverage.  Phase 0 therefore checks the concrete runner route table and tests,
not just prose artifacts, and keeps all numerical SIR DPF work blocked until
the callback contract is reviewed in Phase 1.
