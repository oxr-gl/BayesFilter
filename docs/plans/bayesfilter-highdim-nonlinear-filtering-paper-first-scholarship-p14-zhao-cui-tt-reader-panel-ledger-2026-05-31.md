# P14 Zhao-Cui TT Reader-Panel Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.
- P13 human-readable note.

what_is_not_concluded:
- This is not actual validation by a chemistry/physics professor.
- No numerical performance validation.

## Audience Standard

Proxy reader:
A former chemistry or physics academic who is comfortable with densities,
integrals, Gaussian likelihoods, least squares, and matrix factorizations, but
not with tensor-train filtering.

## Section Checks

| Section | Displayed object first? | Intermediate worked step? | Why object matters? | Failure mode? | Status |
|---|---|---|---|---|---|
| 1 Filtering Objects | SSM densities and \(q_t\) before prose conclusion | Derives \(Z_t=p(y_t\mid y_{1:t-1})\) | Yes | Yes | `PASS` |
| 2 Scalar Example | Scalar model and \(q_t\) | Derives \(\widehat Z_t\) and \(\widehat p_t\) decomposition | Yes | Yes | `PASS` |
| 3 Tensor Trains | Coefficient matrix \(F_{ab}\) | Rank factorization then three-coordinate TT | Yes | Yes | `PASS` |
| 4 Square-Root To Filter | \(s_t=\sqrt q\), \(\widehat q_t\), \(\widehat z_t\) | Mass-matrix contraction | Yes | Yes | `PASS` |
| 5 Zhao-Cui Construction | Sequential equations | Conditional factorization and KR inversion | Yes | Yes | `PASS` |
| 6 Adaptive vs Gradient | Branch \(B\), adaptive scalar | Fixed-branch derivative contrasted with adaptive path | Yes | Yes | `PASS` |
| 7 Fixed-Branch Algorithm | Branch specification \(B_t\) | Target values, core solve, normalizer, numerator | Yes | Yes | `PASS` |
| 8 Proposition 1 | Assumption and \(\widehat q,\widehat\pi,\widehat p\) | Normalization proof | Yes | Yes | `PASS` |
| 9 Proposition 2 Layers | Declared scalar | Layers A--F before proposition | Yes | Yes | `PASS` |
| 10 Gradient Recipe | Inputs and forward equations | Sensitivity pass and parity test | Yes | Yes | `PASS` |
| 11 Construction/Tests | Filter and gradient summary | Diagnostic quantities | Yes | Yes | `PASS` |

## Residual Reader Risks

- Layered Proposition 2 remains mathematically substantial.
- Section 3 is clearer than P13 but still assumes comfort with basis
  expansions and matrix factorization.
- The note teaches a construction; it does not include a numerical TT fit.

Decision:
`P14_READER_PANEL_PROXY_CHECK_PASSES_PENDING_CLAUDE_EXECUTION_REVIEW`
