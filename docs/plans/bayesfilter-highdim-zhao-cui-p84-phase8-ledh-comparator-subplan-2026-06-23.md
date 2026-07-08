# P84 Phase 8 Subplan: LEDH Comparator

Date: 2026-06-23

Status: `DRAFT_BLOCKED_PENDING_PHASE7_AND_APPROVAL`

## Phase Objective

Define and execute, or block, a fair same-convention LEDH-PFPF-OT comparator.

## Entry Conditions Inherited From Previous Phase

- d=18 source-route stronger-tier evidence must exist before this phase can
  execute.
- Same SIR convention, seeds, particles, runtime posture, and uncertainty
  accounting are frozen.
- Explicit human approval is required before LEDH/GPU/long commands.

## Required Artifacts

- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase8-ledh-comparator-result-2026-06-23.md`
- Comparator JSON/CSV manifests.
- Updated execution ledger and Phase 9 subplan.

## Required Checks / Tests / Reviews

Before execution, exact commands must be added.  Design checks:

```bash
rg -n "LEDH|PFPF|OT|same convention|particles|seeds|TF32|uncertainty|comparator" \
  docs/plans \
  experiments \
  bayesfilter -S
```

Claude review and explicit human approval are required before LEDH comparison.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | How does the source-route Zhao-Cui d=18 candidate compare with LEDH-PFPF-OT under a fair same-convention protocol? |
| Baseline/comparator | Predeclared LEDH-PFPF-OT route and source-route candidate. |
| Primary criterion | Comparator manifests complete, uncertainty accounted for, no validity vetoes. |
| Veto diagnostics | Convention mismatch, weak baseline, failed validity diagnostics, unfair particle/seed handling. |
| Explanatory diagnostics | Runtime, memory, ESS, CE/residual summaries, uncertainty intervals. |
| Not concluded | No LEDH superiority or production default unless Phase 10 approves. |
| Artifact | LEDH comparator result. |

## Forbidden Claims / Actions

- Do not run GPU/LEDH without exact approval.
- Do not compare against a weak or mismatched baseline.

## Exact Next-Phase Handoff Conditions

Phase 9 may begin only if Phase 8 records that d=18 stronger-tier evidence
justifies scale/stress, or Phase 9 is explicitly stress-only.

## Stop Conditions

Stop if no fair same-convention comparator can be specified.
