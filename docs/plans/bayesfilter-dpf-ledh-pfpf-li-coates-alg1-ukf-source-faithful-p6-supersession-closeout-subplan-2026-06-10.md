# P6 Subplan: Supersession Closeout

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the project close the loop by replacing all previous LEDH-PFPF-OT evidence with reviewed Algorithm 1 results and a clear nonclaim ledger? |
| Baseline/comparator | P0 quarantine manifest, P4 faithfulness audit, P5 comparison result, historical LEDH-PFPF-OT artifacts. |
| Primary pass criterion | A final closeout note declares previous LEDH-PFPF-OT results discarded/superseded for evidence use and points to the new reviewed Algorithm 1 artifacts. |
| Veto diagnostics | Ambiguous status of old rows; overwriting history; unsupported claims; missing P4/P5 dependencies; no Claude closeout review. |
| Explanatory diagnostics | Final table deltas, remaining model/filter gaps, next-step recommendations. |
| Not concluded | No production default, public API, HMC readiness, or universal method superiority unless future plans establish those separately. |
| Required artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p6-supersession-closeout-result-2026-06-10.md` |

## Required Closeout Content

1. Final decision table:
   - decision;
   - primary criterion status;
   - veto diagnostic status;
   - main uncertainty;
   - next justified action;
   - nonclaims.
2. Supersession table:
   - old LEDH-PFPF-OT artifact;
   - old status;
   - new replacement artifact or reason no replacement exists.
3. New result index:
   - documentation result;
   - design result;
   - implementation result;
   - faithfulness audit;
   - comparison result;
   - JSON/report outputs.
4. Remaining gaps:
   - model/filter pairs not applicable;
   - implementation gaps not fixed in this program;
   - scientific questions left open.
5. Claude closeout review trail.

## Gate

P6 passes only when the closeout can be read by a future agent without
accidentally reviving the previous LEDH-PFPF-OT results as method evidence.
