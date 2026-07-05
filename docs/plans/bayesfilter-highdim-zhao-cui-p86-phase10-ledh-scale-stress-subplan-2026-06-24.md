# P86 Phase 10 Subplan: LEDH Comparator And Scale Stress

Date: 2026-06-24

Status: `DRAFT_BLOCKED_PENDING_PHASE9_AND_APPROVAL`

## Phase Objective

Define and execute, or block, fair same-convention LEDH-PFPF-OT comparison and
any d=50/d=100 scale-stress evidence needed for the final production decision.

## Entry Conditions Inherited From Previous Phase

- Phase 9 derivative/HMC scope is recorded.
- d=18 author-route stronger-tier evidence exists if used to justify scale.
- Same SIR convention, seeds, particles, runtime posture, uncertainty
  accounting, and artifact paths are frozen.
- Explicit approval is required before GPU, LEDH, d=50/d=100, or long commands.

## Required Artifacts

- LEDH comparator protocol and manifests if run.
- Scale/stress manifests if run.
- Uncertainty accounting ledger.
- Phase 10 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase10-ledh-scale-stress-result-2026-06-24.md`
- Updated execution ledger and refreshed Phase 11 subplan.

## Required Checks / Tests / Reviews

- Confirm same-convention comparator baseline and fairness.
- Confirm trusted GPU context for GPU commands.
- Confirm multi-seed or justified uncertainty accounting.
- Claude read-only bounded review and explicit human approval before runtime
  commands and before interpreting comparator/scale evidence.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | How does the author-route candidate compare with LEDH-PFPF-OT under a fair protocol, and does any claimed scale target survive stress diagnostics? |
| Baseline/comparator | Predeclared LEDH-PFPF-OT route, author-route candidate, and scale/stress targets. |
| Primary criterion | Comparator and scale manifests are complete, uncertainty is accounted for, and no validity vetoes fail. |
| Veto diagnostics | Convention mismatch; weak baseline; failed validity diagnostics; unfair seed/particle handling; GPU evidence without trusted context; one-seed overclaim. |
| Explanatory diagnostics | Runtime, memory, ESS, residuals, uncertainty intervals, hardware telemetry. |
| Not concluded | No LEDH superiority, d=50/d=100 production claim, or default-policy change unless Phase 11 approves. |
| Artifact | Comparator manifests, scale/stress manifests, uncertainty ledger, and Phase 10 result. |

## Forbidden Claims / Actions

- Do not run GPU/LEDH/d=50/d=100/long commands without exact approval.
- Do not compare against weak or mismatched baselines.
- Do not promote one-seed or failed-validity evidence.

## Exact Next-Phase Handoff Conditions

Phase 11 may begin only if:

- comparator/scale status is pass, blocked, or explicitly out of production
  scope;
- all prior phase statuses and nonclaims are summarized for final decision.

## Stop Conditions

Stop if:

- fair same-convention comparator cannot be specified;
- exact runtime approval is unavailable;
- validity, uncertainty, or trusted-context vetoes fail;
- Claude and Codex do not converge after five review rounds.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 10 result / close record;
3. draft or refresh the Phase 11 subplan;
4. review the Phase 11 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
