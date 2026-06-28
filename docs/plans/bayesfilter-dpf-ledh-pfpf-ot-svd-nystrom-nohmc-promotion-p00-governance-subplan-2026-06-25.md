# P00 Subplan: Governance And Runbook Lock

Date: 2026-06-25

Status: `DRAFT_LOCAL_AND_CLAUDE_REVIEW_REQUIRED`

## Phase Objective

Lock the SVD-Nystrom no-HMC promotion master program, visible runbook, repair
loop, role boundaries, and phase index before any model-suite or GPU execution.

## Entry Conditions Inherited From Previous Phase

- Actual-SIR SVD threshold-calibration lane closed at
  `P07_CLOSEOUT_READY_FOR_NEXT_MODEL_SUITE_OR_DEFAULT_GAP_PLAN`.
- P06 entry evidence: `14/14` deterministic-valid, `0/14` exceedances,
  one-sided 95% CP upper bound `0.1926361756501353 <= 0.20`.
- User removed HMC readiness as a promotion requirement.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-master-program-2026-06-25.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-gated-execution-runbook-2026-06-25.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-claude-review-ledger-2026-06-25.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-execution-ledger-2026-06-25.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-stop-handoff-2026-06-25.md`
- P00 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p00-governance-result-2026-06-25.md`
- P01 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p01-scope-inventory-subplan-2026-06-25.md`

## Required Checks, Tests, And Reviews

- Local document check that all phase subplans exist.
- Local check that every subplan contains the required headings.
- Local boundary scan for unsupported HMC/default/scientific claims.
- Claude exact-path read-only review of the master program/runbook/subplan set.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the no-HMC promotion program complete, bounded, executable, and safe to launch? |
| Baseline/comparator | P06/P07 SVD threshold-calibration evidence as entry evidence; no model comparison in P00. |
| Primary criterion | Local checks pass and Claude review converges to `VERDICT: AGREE`. |
| Veto diagnostics | Missing phase artifacts, missing required subplan fields, detached execution, HMC readiness as criterion, default-code change authorization, unsupported scientific/product claim, or review nonconvergence. |
| Explanatory diagnostics | Document inventory, heading coverage, review findings. |
| Not concluded | No promotion, model-suite validity, default readiness, HMC readiness, or statistical superiority. |
| Artifact | P00 result and updated review/execution ledgers. |

## Forbidden Claims And Actions

- Do not run GPU/model-suite benchmarks in P00.
- Do not claim promotion readiness.
- Do not claim HMC readiness or use HMC as a gate.
- Do not change code defaults.
- Do not launch detached/background agents.

## Exact Next-Phase Handoff Conditions

- `P00_PASS_TO_P01_SCOPE_INVENTORY`: local checks pass, Claude review agrees,
  and P01 subplan is locally reviewed.
- `P00_REPAIR_LOOP`: fixable document/review issue.
- `P00_BLOCKED`: review nonconvergence after five rounds or human approval
  required.

## Stop Conditions

- Missing required phase subplan.
- Claude review cannot be run without path/content approval after bounded
  prompt repairs.
- Local/Claude review finds a material unfixable boundary flaw.
- Continuing would require default-policy/code changes or GPU runtime before
  governance is locked.

## Local Self-Review Of Next Subplan

P01 is feasible as an inventory-only phase, covers artifacts, and preserves
boundary safety by not running model-suite/GPU benchmarks.
