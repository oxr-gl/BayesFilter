# P20 Zhao--Cui Equation And Size Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P18 true annotated Zhao--Cui companion note and ledgers.
- P19 chair-readable fixed-branch gradient note and ledgers.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross/rank/pivot/domain
  choices.
- No HMC convergence claim.
- No production implementation readiness claim.
- No empirical validation on BayesFilter target models.

## Size Gate

| Quantity | Value |
|---|---:|
| P18 TeX lines | 3169 |
| P19 TeX lines | 1442 |
| P18 PDF pages | 37 |
| P19 PDF pages | 17 |
| Replaced P18 region | `Same-Scalar Analytical Derivative` through before `appendix` |
| Replaced P18 line range | 2796--3156 |
| Replaced P18 tail line count | 362 |
| Replaced P18 tail page estimate | 5 |
| Replaced P18 tail page-estimate method | In the compiled P18 PDF, the replaced tail starts on rendered page 33 and the appendix starts on rendered page 37; counting every rendered page touched by the replaced tail gives pages 33--37, hence 5 pages. The line-proportional estimate \(362/3169\times 37=4.23\) also rounds up to 5 pages. |
| Required P20 line lower bound | 4249 |
| Required P20 page lower bound | 49 |
| Actual P20 TeX lines | 4295 |
| Actual P20 PDF pages | 50 |

Decision: `SIZE_GATE_PASS`.

The actual P20 TeX line count exceeds P18's line count and exceeds the
merge-aware lower bound:
\[
    4295 > 3169,
    \qquad
    4295 \ge 3169 + 1442 - 362 = 4249.
\]
The actual P20 PDF page count also exceeds P18's page count:
\[
    50 > 37.
\]
It also meets the merge-aware page lower bound:
\[
    50 \ge 37 + 17 - 5 = 49.
\]

The replacement subtraction is limited to the named P18
derivative/diagnostic/minimal-example/conclusion tail required by the P20 plan.
No source-order Zhao--Cui reconstruction region was counted as replaced.

## Equation Tag Gate

| Quantity | Value |
|---|---:|
| P20 equation tags | 288 |
| Duplicate equation tags | 0 |

Decision: `EQUATION_TAG_GATE_PASS`.

Imported P19 tags were prefixed with `P19-`, and the P20-specific bridge uses
`P20-B` tags.  No duplicate `\tag{...}` labels were found.

## Source-Order Coverage Gate

Decision: `P18_SOURCE_ORDER_CARRY_FORWARD_PASS`.

The P20 merge ledger maps each P18 source-order section to a P20 destination in
the same order before the integrated gradient expansion.  The carried sections
are substantive sections, not summary placeholders.

## P19 Import Gate

Decision: `P19_GRADIENT_IMPORT_PASS`.

The P20 merge ledger maps each accepted P19 gradient component to a P20
destination.  The accepted design-row derivation, carried-marginal derivative,
fixed-branch semantic correction, and same-branch finite-difference rule are
all imported.
