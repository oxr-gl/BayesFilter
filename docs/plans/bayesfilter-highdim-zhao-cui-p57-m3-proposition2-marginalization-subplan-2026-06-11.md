# P57-M3 Subplan: Proposition-2 Marginalization

metadata_date: 2026-06-11
status: PLAN_REVIEW_CONVERGED

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter implement the source squared-TT marginalization needed for retained objects and KR conditionals? |
| Baseline/comparator | Paper Proposition 2 and author `@TTSIRT/marginalise.m`. |
| Primary pass criterion | Implemented source-style mass-matrix/QR marginal contractions produce normalized marginal pdf/potential and normalizer semantics for retained prefix/suffix cases used by the route, with tests. |
| Veto diagnostics | Tensor-product grid integration claimed as source marginalization; metadata-only marginal objects; normalizer mismatch with source semantics. |
| Not concluded | No full transport map or sequential loop until M4-M6 pass. |

## Tasks

1. Translate the author marginalization recursion into BayesFilter notation.
2. Implement fixed-rank TensorFlow contractions for squared TT cores.
3. Add low-dimensional analytic tests where grid integration can be an
   independent comparator, not the implementation definition.
4. Verify normalizer and determinant policy.
5. Write result artifact with remaining blockers if implementation is deferred.
   A plan-only or deferred-implementation outcome must emit
   `BLOCK_P57_M3_PROPOSITION2_MARGINALIZATION`, not a pass token.

## Required Checks

- `rg -n "SquaredTTDensity|marginal_density|conditional_density|normalizer|TTSIRT" bayesfilter/highdim tests/highdim`
- Claude review must reject any pass that only preserves current grid
  diagnostics.
