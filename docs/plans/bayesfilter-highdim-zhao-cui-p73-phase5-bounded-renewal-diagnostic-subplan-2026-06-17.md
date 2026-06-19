# P73 Phase 5 Subplan: Bounded Renewal Diagnostic

metadata_date: 2026-06-17
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE5
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Run the first bounded P73 renewal diagnostic visibly in this session.  The
diagnostic asks whether P73-A, the one-renewal square-root regression variant,
improves the P72 blocked lower gate without using same-round audit points for
coefficient selection.

P73-B is not runnable in this phase because Phase 4 records
`P73_B_OPTIMIZER_BLOCKED_NONLINEAR_OBJECTIVE_NOT_IMPLEMENTED`.

## Entry Conditions Inherited From Phase 4

Phase 5 may begin only if:

- Phase 4 result exists;
- Phase 4 local checks pass;
- Claude returns `VERDICT: AGREE` for the Phase 4 implementation, tests,
  result, and this subplan;
- P73-A is implemented and tested as the mandatory renewal-only arm;
- P73-B is explicitly marked blocked and `phase5_runnable = False`;
- the run remains covered by the reviewed visible runbook.

## Required Artifacts

Phase 5 must produce:

- bounded diagnostic JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json`;
- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-result-2026-06-17.md`;
- refreshed Phase 6 result-decision subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase6-result-decision-subplan-2026-06-17.md`;
- updated execution and review ledgers.

## Required Checks/Tests/Reviews

Before the bounded diagnostic:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p73_density_aware_renewal_diagnostic.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p73_density_aware_renewal.py
```

The bounded diagnostic command must be frozen in the Phase 5 result before
interpretation.  The intended command is CPU-only:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p73_density_aware_renewal_diagnostic.py --output docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json
```

If the existing Phase 4 script cannot yet run real P73-A rows, Phase 5 must
first patch the script within the reviewed Phase 5 scope, rerun focused local
checks, and then run the bounded diagnostic.  It must not report the Phase 4
schema/smoke payload as the bounded diagnostic.

Review:

- Claude read-only review of the diagnostic command, JSON artifact, Phase 5
  result, and Phase 6 subplan;
- loop to convergence or max 5 rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does one-renewal P73-A reduce or clear the P72 lower-gate blockers under fresh guard/audit certification without training on same-round audit data? |
| Exact baseline/comparator | P72 Phase 5 blocked diagnostic row `rank_candidate_1_2_fit36`; P73-A uses the same rank/degree row with one renewal. |
| Primary pass/fail criterion | The P73-A row passes fit RMS, fresh guard RMS/max residual, fresh audit RMS/max residual, guard-line and audit-line gates, support diagnostics, full normalizer gate, condition/effective-rank gate, rank-activity gate, and `NO_AUDIT_COEFFICIENT_SELECTION`. |
| Diagnostics that can veto | Audit or audit-line points in coefficient selection; certification on newly added training points; nonfinite values; residual, line, support, normalizer, condition/effective-rank, or rank-activity block; threshold drift; P73-B executed despite blocked optimizer. |
| Explanatory only | Training loss, fit-cloud cross-entropy, toy schema values, runtime, condition spectra beyond the frozen gate, and any P73-B objective value if merely evaluated. |
| What will not be concluded | No d18 validation, no HMC readiness, no scaling, no rank or degree promotion, no adaptive Zhao--Cui source-faithful parity. |
| Artifact preserving result | Phase 5 JSON, Phase 5 result note, execution/review ledgers, and Phase 6 subplan. |

## Required Row And Arm Labels

The first bounded diagnostic is limited to:

| Label | Status |
| --- | --- |
| `rank_candidate_1_2_fit36` | required P73-A row |
| `p73_a_renewal_only` | runnable |
| `p73_b_density_aware_optin` | blocked by `P73_B_OPTIMIZER_BLOCKED_NONLINEAR_OBJECTIVE_NOT_IMPLEMENTED` |

Rank-3 retry, degree ladders, validation ladders, HMC, and scaling are not
part of Phase 5.

## Forbidden Claims/Actions

- Do not run P73-B while the optimizer status is blocked.
- Do not run downstream validation, HMC, scaling, GPU, or rank promotion.
- Do not change thresholds after seeing outputs.
- Do not treat training loss or cross-entropy as the primary pass criterion.
- Do not report schema-only or smoke-only payloads as bounded diagnostic
  evidence.
- Do not call P73 renewal, audit exclusion, cross-entropy, or lower-gate
  thresholds source-faithful Zhao--Cui operations.

## Exact Next-Phase Handoff Conditions

Phase 6 may begin only if:

- Phase 5 JSON exists and is not schema-only or smoke-only;
- Phase 5 result exists and records the exact command, CPU/GPU status, git
  state, seeds, wall time, row labels, pass/block decision, and nonclaims;
- Claude returns `VERDICT: AGREE`;
- Phase 6 subplan exists and limits itself to interpreting the bounded
  diagnostic and selecting the next root-cause or downstream planning action.

## Stop Conditions

Stop and write a blocker if:

- the script cannot be safely patched to run real P73-A rows within Phase 5
  boundaries;
- `NO_AUDIT_COEFFICIENT_SELECTION` cannot be proven from the artifact;
- P73-B execution is required to answer the Phase 5 question;
- the diagnostic would need GPU, validation, HMC, scaling, or rank promotion;
- thresholds or row labels need to change after seeing outputs;
- Claude and Codex do not converge after five rounds for the same blocker;
- the user redirects the lane.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit as a bounded diagnostic plan
because it fixes the comparator, row label, runnable arm, blocked arm,
CPU-only environment, primary gates, veto diagnostics, explanatory metrics,
and nonclaims before execution.  It explicitly forbids promoting schema
smoke, training loss, or cross-entropy values to lower-gate evidence.
