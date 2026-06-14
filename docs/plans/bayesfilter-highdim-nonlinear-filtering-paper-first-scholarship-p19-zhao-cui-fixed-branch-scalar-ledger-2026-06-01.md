# P19 Zhao--Cui Fixed-Branch Scalar Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- P10 filtering-scalar ledger.
- P15 fixed-branch implementation specification.
- P18 annotated companion.

what_is_not_concluded:
- No exact likelihood claim.
- No HMC target readiness claim.
- No claim that adaptive branch decisions are differentiated.

## Declared Scalar

P19 uses the same conservative fixed-branch scalar as P10/P15/P18:
\[
  \widehat\ell_T(\beta;B)
  =
  \sum_{t=1}^T\log\widehat Z_t(\beta;B_t),
\]
where \(B=(B_1,\ldots,B_T)\) stores the fixed branch objects.

## Frozen Objects

| Object | Frozen in P19? | Reason |
|---|---:|---|
| Domain maps | Yes | Avoids boundary and Jacobian branch derivatives. |
| Fitting points | Yes | Keeps design matrices tied to the same scalar. |
| Basis family and degree | Yes | Keeps mass matrices fixed. |
| TT ranks | Yes | Avoids rank-selection discontinuities. |
| Sweep count/order | Yes | Makes finite composition differentiable. |
| Ridge parameter | Yes | Keeps solve map fixed. |
| Defensive mass/reference | Yes | Avoids extra derivative terms and support changes. |
| Stabilizing shifts | Yes | Keeps the declared scalar identical across derivative checks. |
| Fitted core values \(C_{t,k}(\beta)\) | No | They are differentiable outputs of the frozen fitting rule and must change with \(\beta\). |
| Mass contractions \(M_{t,>k}(\beta)\) | No | They are differentiable outputs of the parameter-dependent core values. |

## Same-Scalar Clarification

The fixed branch means the structural choices are fixed, not that all numerical
outputs are copied from the base parameter.  The scalar is
\[
  \widehat\ell_T(\beta;B)
  =
  \sum_{t=1}^T\log\widehat Z_t(\beta;B_t),
\]
where \(B_t\) fixes domains, points, basis, ranks, shifts, defensive terms, and
solve protocol.  The fitted cores \(C_{t,k}(\beta;B_t)\), mass contractions,
normalizers, carried filters, and their derivatives remain functions of
\(\beta\).

Decision: `FIXED_BRANCH_SCALAR_DECLARED_FOR_P19`.
