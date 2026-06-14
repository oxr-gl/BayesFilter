# P37-M7 Subplan: Model-Suite Integration, Traceability, And Closeout

metadata_date: 2026-06-05

parent_plan:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md`

## Purpose

Close the P30 model-suite test program by reconciling plans, result ledgers,
traceability rows, and documentation claims.  This phase decides what the
implementation evidence actually supports and what remains blocked.

## Evidence Contract

Question: after model-specific phases run, can the project produce a coherent
governance closeout that maps every P30 validation claim to code, tests,
results, or explicit blockers?

Primary pass criteria:

- traceability ledger has updated rows for LGSSM, SV, SIR, predator-prey,
  stress ladders, and fixed-branch gradient tables;
- each row has one of the governed statuses:
  `SOURCE_MATCHED`, `MATLAB_BEHAVIOR_MATCHED`, `BAYESFILTER_EXTENSION`,
  `DOCUMENTED_DEVIATION`, `REFERENCE_ONLY`, `BLOCKED_UNTRACEABLE`,
  `BLOCKED_UNVALIDATED`;
- documentation claims are patched to match result evidence;
- remaining blockers are not hidden.

Vetoes:

- any claim in docs/plans or code comments that says the full P30 suite passed
  when only a subset passed;
- any `REFERENCE_ONLY` model used as BayesFilter evidence;
- any DSGE/HMC/public-API/GPU claim without separate downstream result;
- missing run manifest for a promoted test row;
- missing Claude review of the closeout.

## Implementation Tasks

1. Audit result ledgers from M0--M6.
2. Update traceability rows with exact statuses and anchors.
3. Add a closeout result note with decision table:
   model, value status, derivative status, stress status, primary evidence,
   veto status, remaining blocker.
4. Patch any planning or documentation text that overclaims.
5. Run a final Claude governance review.

## Planned File Ownership

Allowed writes:

```text
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
docs/plans/*p37*phase7*result*.md
docs/plans/*p37*closeout*claude-review-ledger*.md
```

Documentation files may be patched only when the closeout audit identifies a
specific overclaim or stale status.

## Planned Commands

```bash
git diff --check

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py \
  tests/highdim
```

If `tests/highdim` becomes too slow, the result ledger must list the exact
subset and justify why a full run is deferred.

## Exit Criteria

- final traceability ledger is consistent with executed tests;
- final closeout result states exactly what is supported;
- unresolved items remain visible with blocker statuses;
- Claude review returns pass/no blockers or residual findings are explicitly
  carried forward.

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW_AFTER_SCOPE_CONFIRMATION`.

The main M7 risk is a celebratory overclaim: after many green tests, the
closeout could accidentally say that the full Zhao--Cui model suite, adaptive
MATLAB TT-cross/SIRT behavior, paper-scale validation, HMC/DSGE/GPU readiness,
or a stable public score API has passed.  The executed phases do not support
those claims.  They support a source-governed BayesFilter extension lane with
exact/tiny LGSSM references, scalar SV value and TT-lane evidence, first-gate
SIR and predator-prey model contracts, stress-manifest governance, and scalar
fixed-branch gradient-table governance.

M7 therefore must be a reconciliation and blocker-preservation phase.  It may
summarize passed gates, update traceability and closeout ledgers, and run final
guardrails.  It may not introduce new algorithm claims, weaken row statuses,
or convert first-gate evidence into production/paper-scale readiness.

No material flaw remains in sending this closeout plan to Claude plan review.
Implementation may not begin until `PASS_M7_PLAN`.
