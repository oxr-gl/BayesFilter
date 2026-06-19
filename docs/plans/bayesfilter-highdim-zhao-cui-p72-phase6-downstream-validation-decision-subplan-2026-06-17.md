# P72 Phase 6 Subplan: Blocked-Result Root-Cause Decision

metadata_date: 2026-06-17
status: READY_FOR_PHASE6_ROOT_CAUSE_DECISION_AFTER_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Interpret the blocked Phase 5 diagnostic and decide the next root-cause
repair path.  Because Phase 5 did not pass the lower gate, Phase 6 must not
authorize downstream validation, HMC readiness, scaling, or rank/degree
promotion.  It may only produce a reviewed root-cause plan or a stop handoff.

## Entry Conditions Inherited From Phase 5

Phase 6 may begin only if:

- Phase 5 diagnostic JSON exists and is not schema-only:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json`;
- Phase 5 result exists and records the blocked decision:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-result-2026-06-17.md`;
- focused checks for the runner and tests passed;
- the Phase 5 result includes a decision table and nonclaims;
- Claude returns `VERDICT: AGREE` for the Phase 5 execution and this Phase 6
  subplan.

## Required Artifacts

Phase 6 must produce:

- Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase6-downstream-validation-decision-result-2026-06-17.md`;
- either a root-cause repair subplan for the next P72 phase or an updated stop
  handoff;
- updated execution and review ledgers.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Given the blocked real Phase 5 diagnostic, what is the smallest next root-cause action that can discriminate residual/line failure, condition failure, normalizer collapse, support construction mismatch, and fixed-fit objective mismatch? |
| Exact baseline/comparator | Phase 5 diagnostic JSON and P70 Phase 6h root-cause probes. |
| Primary pass/fail criterion | Phase 6 passes only if it produces a bounded, testable root-cause decision with no validation/promotion claims and no threshold changes after seeing Phase 5 outputs. |
| Veto diagnostics | Any attempt to launch downstream validation, treat Phase 5 as a repaired pass, tune thresholds post hoc, call guard/audit/line additions source-faithful, or ignore the stronger-row normalizer collapse. |
| Explanatory only | Relative magnitudes of residuals, condition numbers, line-channel statuses, normalizer terms, and runtime. |
| What will not be concluded | No d18 validation, HMC readiness, scaling, rank/degree promotion, or adaptive Zhao--Cui parity. |
| Artifact preserving result | Phase 6 result, reviewed next root-cause subplan or stop handoff, execution ledger, and review ledger. |

## Required Checks/Reviews

Before Phase 6 result:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json >/tmp/p72_phase5_json_check.json
rg -n "exception_type|p72_phase5_row_exception_fail_closed|schema_only_sentinel_present.*true|smoke_only_not_phase5_evidence.*true" docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json
```

Interpret the `rg` command's exit code `1` as expected sentinel absence only
if no matches are printed.

Claude review must check:

- whether the Phase 5 artifact is interpreted as blocked, not promoted;
- whether the proposed next action targets the actual failed gates;
- whether a downstream-validation decision remains blocked;
- whether the stronger-row normalizer collapse is represented as a real
  mathematical/numerical blocker, not merely a reporting bug.

## Required Decision Table

The Phase 6 result must include a decision table with:

- decision;
- primary criterion status;
- veto diagnostic status;
- main uncertainty;
- next justified action;
- what is not being concluded.

## Forbidden Claims/Actions

- Do not run d18 validation, HMC, scaling, or downstream validation ladder.
- Do not change any Phase 5 threshold.
- Do not use audit clouds or line probes for coefficient selection.
- Do not claim source-faithfulness for P72 guard/audit/line/admission gates.
- Do not treat the structured normalizer block as fixed by the reporting
  repair.

## Exact Next-Phase Handoff Conditions

A next root-cause phase may begin only if:

- Claude agrees the Phase 5 blocked interpretation is correct;
- the Phase 6 result names the chosen root-cause hypotheses and exact bounded
  probes;
- the next subplan states entry conditions, artifacts, checks, evidence
  contract, forbidden actions, handoff conditions, and stop conditions;
- the next action does not require downstream validation or promotion.

## Stop Conditions

Stop and write a handoff if:

- Claude disputes the Phase 5 artifact interpretation;
- the next root-cause action would require changing thresholds after seeing
  outputs;
- the next action would require a new scientific target or product boundary
  not authorized by the master program;
- the user redirects the lane.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit because it consumes the
blocked Phase 5 artifact as the governing evidence, blocks downstream
validation, and requires the next action to target the actual failed gates
instead of converting a diagnostic failure into a promotion claim.
