# Phase 4 Claude Review Round 01: Nystrom Subplan

Date: 2026-06-17
Review timestamp: 2026-06-18T00:49:52+08:00

## Scope

Read-only review of:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p03-common-interface-harness-result-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-subplan-local-review-2026-06-17.md`

Claude was used as read-only reviewer only.  This review did not authorize
phase advancement.

## Findings

Claude reported two material fixable findings:

1. Phase 4 referenced dense-reference and residual tolerances but did not
   declare concrete Phase 4 pass thresholds.  The handoff condition also
   required recording dense-reference error but did not require saying whether
   the threshold passed.
2. Source-faithfulness was too loose around the epsilon/reg/sigma/eta map and
   FilterFlow adapter route.  Paper-anchored Nystrom operations needed to be
   separated from local wrapper/adaptation operations.

Claude found no material issue on the other reviewed boundaries:

- comparator remains the local Phase 1 TensorFlow dense/streaming baseline;
- runtime/memory remain explanatory only;
- TensorFlow/default-backend boundary is explicit;
- unsupported correctness/speedup/ranking/production/default claims are
  disclaimed;
- Claude remains read-only reviewer, not executor or authority.

## Verdict

`VERDICT: REVISE`

## Repair

The Phase 4 subplan was patched to add:

- `Phase 4 Validity And Viability Thresholds`;
- `Source-Route Classification For Phase 4`;
- an explicit non-promoted-but-completed candidate result status;
- a handoff condition requiring the result to state whether the Phase 4
  thresholds passed or failed.

Focused local repair checks passed:

- `P04_REPAIR_THRESHOLD_SOURCE_ROUTE_PASS`
- `P04_SUBPLAN_STRUCTURE_PASS`
- `P04_LOCAL_REVIEW_REPAIR_RECORD_PASS`
