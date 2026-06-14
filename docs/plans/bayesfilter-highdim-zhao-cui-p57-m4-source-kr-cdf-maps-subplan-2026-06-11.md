# P57-M4 Subplan: Source KR/CDF Maps

metadata_date: 2026-06-11
status: PLAN_REVIEW_CONVERGED

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter provide source-style KR maps rather than grid diagnostic KR maps? |
| Baseline/comparator | Paper conditional CDF construction at P56 paper anchors for conditional KR maps; author `SIRT.m:80-85` CDF construction; `AbstractIRT.m:152-188`, `:192-213`, `:217-270`, and `:299-354` map/pdf/random methods. |
| Primary pass criterion | Fixed transport exposes forward KR, inverse KR, and conditional KR maps whose densities tie to Proposition-2 conditionals and `eval_pdf` semantics. |
| Veto diagnostics | `transport.py` grid CDFs promoted as source-faithful; no monotonicity/inversion tests; no density/Jacobian tie-out. |
| Not concluded | No full filtering loop or paper-scale SIR. |

## Tasks

1. Keep existing grid KR as diagnostic-only.
2. Specify or implement source-style CDF constructors for fixed TT/SIRT.
3. Add tests for monotonicity, inverse/forward roundtrip, conditional map
   consistency, and log-density/Jacobian identity on analytic low-dimensional
   targets.
4. Preserve exact paper/source line anchors in the result artifact before any
   implementation pass is accepted.
5. Record numerical tolerances and failure modes.
6. Write result artifact. A pass cannot rely on `transport.py` grid CDFs except
   as independent diagnostics.

## Required Checks

- `rg -n "Grid-based KR|Knothe|transport|conditional_density|cdf|inverse" bayesfilter/highdim tests/highdim`
- Claude review must compare the map semantics to author `AbstractIRT.m`.
