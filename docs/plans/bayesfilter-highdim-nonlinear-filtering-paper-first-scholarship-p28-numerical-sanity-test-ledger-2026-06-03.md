# P28 Numerical Sanity-Test Ledger

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

audit_scope:
- Audit whether P27 specifies enough test models and diagnostics for large-scale method validation.

what_is_not_concluded:
- This ledger does not run experiments.
- Passing the proposed tests would not prove exact posterior accuracy.
- Zhao--Cui model reproduction would not by itself validate the fixed-branch derivative.

## Test Coverage

| test class | P27 anchor | status | veto condition |
|---|---|---|---|
| low-dimensional exact/brute-force comparator | Sections 52--54, 57 | SPECIFIED | Normalizer/filter mismatch exceeds declared tolerance. |
| Zhao--Cui benchmark suite | Sections 58--61 | SPECIFIED_WITH_SOURCE_REVIEW_REQUIRED | Model settings differ from Zhao--Cui without explanation. |
| memory/runtime scaling | Section 55 | SPECIFIED | Memory or time grows contrary to stated TT cost model without diagnosis. |
| normalizer/mass/stability | Sections 55, 62 | SPECIFIED | Nonpositive normalizer, mass drift, ill-conditioned solve, or unstable KR inversion. |
| finite-difference derivative | Sections 52, 57, 62 | SPECIFIED | No branch-stable decreasing window or derivative mismatch outside tolerance. |
| negative control | P28 plan requirement | GAP_IN_P27 | P27 should explicitly include a negative control if this becomes a validation paper rather than a companion note. |

## Verdict

numerical_sanity_verdict: `VALIDATION_PROTOCOL_GOOD_BUT_NOT_EXECUTED`

P27 gives a credible mathematical validation protocol and includes Zhao--Cui model families.  It is not empirical evidence yet.  A negative-control test is the main missing protocol detail if the document is used as a testing specification.
