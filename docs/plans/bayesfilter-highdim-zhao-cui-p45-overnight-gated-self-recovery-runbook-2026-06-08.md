# P45 Overnight Gated Self-Recovery Runbook

metadata_date: 2026-06-08
phase: P45-overnight

## Parent Plans

- P45 master program:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-generalized-sv-sir-predator-prey-comparison-master-program-2026-06-08.md`
- P45 Claude plan review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-generalized-sv-sir-predator-prey-comparison-claude-review-ledger-2026-06-08.md`
- P42 validation rules:
  `docs/plans/bayesfilter-highdim-zhao-cui-p42-gradient-likelihood-validation-rules-2026-06-07.md`

## Purpose

Govern unattended or long supervised execution of P45.  Codex is the visible
supervisor and executor.  Claude is read-only reviewer.  The run may repair
fixable plan, implementation, artifact, or evidence-chain failures, but it may
not weaken target identity, parameterization, baseline, tolerance, or claim
class without a reviewed repair amendment.

## Launch Preconditions

- P45 plan review ledger latest status is `PASS_P45_PLAN_GOVERNANCE`.
- All P45-M0--M6 subplans exist.
- Execution result file records `READY_TO_LAUNCH_AFTER_P45_PLAN_PASS`.
- Any phase gate script used by the run has been created and locally checked
  before phase execution.

## Phase Queue

| Order | Phase | Required pass token |
| --- | --- | --- |
| 0 | P45-M0 | `PASS_P45_M0_CODE_GOVERNANCE` |
| 1 | P45-M1 | `PASS_P45_M1_CODE_GOVERNANCE` |
| 2 | P45-M2 | `PASS_P45_M2_CODE_GOVERNANCE` |
| 3 | P45-M3 | `PASS_P45_M3_CODE_GOVERNANCE` |
| 4 | P45-M4 | `PASS_P45_M4_CODE_GOVERNANCE` |
| 5 | P45-M5 | `PASS_P45_M5_CODE_GOVERNANCE` |
| 6 | P45-M6 | `PASS_P45_M6_CODE_GOVERNANCE` |

## State Machine

Each phase follows:

```text
PHASE_PLAN_CONFIRMED
-> SKEPTICAL_AUDIT_RECORDED
-> CLAUDE_PLAN_OR_REPAIR_REVIEW_PASS
-> IMPLEMENTED_OR_BLOCKER_RECORDED
-> LOCAL_EVIDENCE_RUN
-> EVIDENCE_AUDIT_RECORDED
-> RESULT_NOTE_WRITTEN
-> CLAUDE_CODE_GOVERNANCE_PASS
-> PHASE_PASS
```

Failure transition:

```text
BLOCKER_CLASSIFIED
-> REPAIR_PLAN_AMENDMENT
-> CLAUDE_REPAIR_REVIEW_PASS
-> REPAIR_IMPLEMENTED
-> LOCAL_EVIDENCE_RUN
```

Stop transition:

```text
BLOCKER_CLASSIFIED
-> HUMAN_INTERVENTION_REQUIRED
```

## Stop Conditions

- Claude blocks five review iterations without pass.
- Target equality requires a scientific decision not encoded in P45-M0.
- No feasible reference route exists inside declared resource caps.
- Trusted infrastructure or dependency access is unavailable after rerun.
- A phase would need to weaken target identity, parameterization, baseline, or
  tolerance to pass.

## Nonclaims

- no HMC readiness;
- no production analytic score API;
- no stable public API;
- no paper-scale Zhao--Cui reproduction;
- no adaptive MATLAB TT-cross/SIRT reproduction.

