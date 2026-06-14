# P57-M2 Subplan: FixedTTSIRT Transport Contract

metadata_date: 2026-06-11
status: PLAN_REVIEW_CONVERGED

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What interface and invariants must a fixed-HMC `FixedTTSIRTTransport` satisfy to preserve the author TT/SIRT route? |
| Baseline/comparator | Paper Algorithm 2/3, `SIRT.m`, `AbstractIRT.m`, `TTIRT`/`TTSIRT` construction in `full_sol.m`, P56 D03. |
| Primary pass criterion | A reviewed contract requires fixed TT cores, defensive density, normalizer, `eval_pdf`/potential, inverse KR, forward KR, conditional KR, marginalization, and Jacobian-aware proposal density. |
| Veto diagnostics | Contract only wraps current grid KR; contract exposes only inverse transport and base reference density; `FixedTTFitter` is promoted without proving source semantics. |
| Not concluded | No implementation yet unless this phase explicitly patches and tests a minimal contract. |

## Tasks

1. Re-open source anchors for `eval_irt`, `eval_rt`, `eval_cirt`, `eval_pdf`,
   `random`, and `marginalise`.
2. Define the Python protocol/dataclass surface needed by later phases.
3. Classify existing `SourceRouteTransportProtocol` gaps and immediate API
   compatibility risks.
4. Write tests that reject transports without source-route density semantics.
5. Record implementation plan and result token.

## Required Checks

- `rg -n "SourceRouteTransportProtocol|log_reference_density|inverse_transport|eval_pdf|source_route_generate_retained_samples" bayesfilter/highdim tests/highdim`
- Claude review must check that proposal density is not base/reference density
  unless mathematically proven equivalent for a test double.
