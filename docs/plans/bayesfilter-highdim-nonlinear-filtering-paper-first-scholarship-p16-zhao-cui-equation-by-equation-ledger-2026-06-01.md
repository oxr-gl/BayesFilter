# P16 Zhao-Cui Equation-By-Equation Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.

what_is_not_concluded:
- No claim that equations outside the listed scope have been fully expanded.
- No claim that Section 6 numerical examples prove performance on BayesFilter's target model.
- No claim that adaptive branch derivatives are globally smooth.

## Scope

Required ordered scope: Zhao--Cui Sections 1--3 and 5.  Section 4 is used as
support for error-propagation interpretation.  Section 6 is used only as
numerical-evidence context.

## Disposition Table

| Source item | P16 disposition | P16 note anchor | Comment |
|---|---|---|---|
| Eq. (1) transition model | `expanded` | State-Space Model | Rewritten as BF-1. |
| Eq. (2) observation model | `expanded` | State-Space Model | Rewritten as BF-2. |
| Eq. (3) joint density | `expanded` | State-Space Model | Derived by chain rule as BF-3. |
| Eq. (4) posterior/evidence | `expanded` | State-Space Model | Rewritten as BF-4. |
| Eq. (5) filtering | `expanded` | Four Marginal Learning Problems | Rewritten as BF-5. |
| Eq. (6) parameter learning | `expanded` | Four Marginal Learning Problems | Rewritten as BF-6. |
| Eq. (7) path learning | `expanded` | Four Marginal Learning Problems | Rewritten as BF-7. |
| Eq. (8) smoothing | `expanded` | Four Marginal Learning Problems | Rewritten as BF-8. |
| Eq. (9) recursive posterior | `expanded` | Exact Recursive Bottleneck | Derived from BF-3 and Bayes rule. |
| Eq. (10) adjacent-state posterior | `expanded` | Exact Recursive Bottleneck | Derived by integrating old path. |
| Eq. (11) next filter marginal | `expanded` | Exact Recursive Bottleneck | Identified as bottleneck integral. |
| Algorithm 1 | `expanded` | Zhao--Cui Algorithm 1 | Three steps expanded. |
| Eq. (12) Alg. 1 pointwise target | `expanded` | Algorithm 1 | Rewritten as A1-1. |
| Eq. (13) squared-TT density | `expanded` | Squared-TT Density | Rewritten as S1-S3. |
| Lemma 1 | `deferred_to_support_section` | Squared-TT Density; Error Propagation | Used for Hellinger interpretation, not re-proved from Cui--Dolgov. |
| Proposition 2 / Eq. (14) | `expanded` | Squared-TT Marginalization | Derived as M1-M6. |
| Algorithm 2 | `expanded` | Zhao--Cui Algorithm 2 | Steps and scalar expanded. |
| Eq. (15) squared-TT target | `expanded` | Algorithm 2 | Rewritten as A2-1. |
| Eq. (16) nonnegative approximation | `expanded` | Algorithm 2 | Rewritten as A2-3. |
| Eq. (17) lower KR map | `expanded` | Conditional Maps; Backward Map | Rewritten as K4 and B1-B2. |
| Eq. (18) lower conditional CDF | `expanded` | Conditional Maps | Rewritten as K2-K3 and B1. |
| Eq. (19) lower conditional map | `expanded` | Backward Map | Rewritten as B2. |
| Proposition 4 | `expanded` | Conditional Maps | Triangular Jacobian proof given as K5. |
| Eq. (20) upper conditional map | `expanded` | Forward Map | Rewritten as F1-F2. |
| Eq. (21) forward inverse map sample | `expanded` | Forward Map | Rewritten as F2. |
| Eq. (22) proposal density | `expanded` | Forward Map | Rewritten as F3. |
| Eq. (23) forward correction weight | `expanded` | Forward Map | Rewritten as F4. |
| Algorithm 3 | `expanded` | Forward Map | Explained as proposal plus weights. |
| Eq. (24) backward inverse map sample | `expanded` | Backward Map | Rewritten as B2. |
| Eq. (25) approximate path factorization | `expanded` | Backward Map | Rewritten as B3. |
| Eq. (26) backward correction weight | `expanded` | Backward Map | Rewritten as B5. |
| Algorithm 4 | `expanded` | Backward Map | Explained as final draw plus backward recursion. |
| Eq. (27) error split | `deferred_to_support_section` | Error Propagation | Used to explain what the paper proves. |
| Eqs. (28)-(29) boundedness assumptions | `deferred_to_support_section` | Error Propagation | Described qualitatively; not central to implementation path. |
| Eq. (30) preconditioning KR map | `expanded` | Preconditioning | Rewritten as P1. |
| Eq. (31) preconditioned target | `expanded` | Preconditioning | Rewritten as P2. |
| Eq. (32) preconditioned squared TT | `expanded` | Preconditioning | Rewritten as P3. |
| Eq. (33) pullback approximation | `expanded` | Preconditioning | Rewritten as P4-P5. |
| Eq. (34) tempering bridge | `expanded` | Preconditioning | Rewritten as P6. |
| Eq. (35) bridge approximation | `expanded` | Preconditioning | Rewritten as P7. |
| Algorithm 5 | `expanded` | Preconditioning | Discussed as preconditioned replacement. |

## Gaps For Next Revision

- The note expands the mathematical flow but does not yet give line-by-line
  pseudocode for every source algorithm.
- The fixed-branch implementation protocol is summarized; P15 remains the
  more precise implementation contract.
