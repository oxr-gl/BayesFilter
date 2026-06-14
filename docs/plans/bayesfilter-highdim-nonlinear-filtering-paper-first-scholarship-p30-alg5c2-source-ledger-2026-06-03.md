# P30 Algorithm 5(c.2) Source Ledger

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

audit_scope:
- Source support for the expanded Algorithm 5(c.2) derivation.

what_is_not_concluded:
- This source ledger does not certify every equation in P30.
- This ledger does not run empirical validation.

## Source Anchor

Zhao--Cui Section 5.4 / Algorithm 5(c.2) states that using the lower-triangular transformation
\((u_t,u_\theta)=(T_{t,t}^\ell(x_t),T_{t,\theta}^\ell(\theta\mid x_t))\), the retained marginal density is obtained by combining the residual marginal \(\widehat\nu_{\sharp,t}(u_t,u_\theta)\), the reference density \(\eta(u_t,u_\theta)\), and the bridge marginal \(\widehat\rho_t(x_t,\theta)\).

PDF-text extraction is imperfect, so this ledger records source support as targeted rather than global visual certification.

## P30 Expansion Status

| P30 anchor | role | source/audit status | notes |
|---|---|---|---|
| `eq:p30-c2-0`--`eq:p30-c2-3` | defines retained block \(a=(x_t,\theta)\), old block \(b=x_{t-1}\), transformed blocks \(u_A,u_B\), and marginal densities | SOURCE_SUPPORTED_PROJECT_DERIVATION | Makes Zhao--Cui Algorithm 5(c.2) notation explicit. |
| `eq:p30-c2-4`--`eq:p30-c2-6` | bridge pushforward and conditional bridge identity | SOURCE_SUPPORTED_PROJECT_DERIVATION | Follows Zhao--Cui Eq. (30) / Algorithm 5(b.2) and conditionalizes it. |
| `eq:p30-c2-7`--`eq:p30-c2-9` | cancellation of reference density and derivation of retained marginal | SOURCE_SUPPORTED_PROJECT_DERIVATION | Expands Algorithm 5(c.2)'s one-line formula. |
| `eq:p24-p17` | final retained physical marginal | SOURCE_MATCH_TARGETED | Matches Zhao--Cui Algorithm 5(c.2) structure: residual marginal divided by retained reference density times bridge marginal. |
| `eq:p30-c2-10`--`eq:p30-c2-11` | perfect-residual sanity check | PROJECT_DERIVATION | Confirms formula reduces to ordinary marginalization when residual fit is exact. |
| `eq:p30-basis-q`--`eq:p30-basis-policy` | basis-family defense, tuning ladder, diagnostics, and fixed-branch freeze rule | BACKGROUND_SUPPORTED_PROJECT_DESIGN | Cites standard approximation, polynomial-chaos, wavelet, dictionary-learning, and sparse/low-rank approximation sources for context.  Does not claim a universal optimal basis theorem.  The residual/evidence/marginal/conditioning checks are a proposed BayesFilter audit protocol. |

## Basis-Choice Literature Support Added On 2026-06-03

| source | classification | support used in P30 | claim not made |
|---|---|---|---|
| Trefethen, *Approximation Theory and Approximation Practice* | FOUNDATIONAL_BACKGROUND | Smooth functions on simple domains motivate global polynomial approximation; local nonsmooth features require different approximation spaces. | Does not certify any TT posterior approximation. |
| Ghanem and Spanos, *Stochastic Finite Elements* | FOUNDATIONAL_BACKGROUND | Polynomial-chaos basis families are standard for stochastic/spectral approximation. | Does not certify the proposed filtering ladder. |
| Xiu and Karniadakis, Wiener--Askey polynomial chaos | FOUNDATIONAL_BACKGROUND | Hermite and related polynomial-chaos families are natural for Gaussian/reference-measure settings. | Does not imply Hermite is optimal for all preconditioned filtering targets. |
| Daubechies and Mallat wavelet references | FOUNDATIONAL_BACKGROUND | Wavelets are standard sparse/local multiscale approximation bases. | Does not imply wavelets should be the default TT basis. |
| Aharon--Elad--Bruckstein K-SVD | BACKGROUND_METHOD | Supports the statement that dictionaries/bases can be learned from pilot data. | Does not support differentiating through learned-basis retraining. |
| Bachmayr--Cohen--Dahmen sparse/low-rank approximation paper | BACKGROUND_CONTEXT | Supports framing sparse and low-rank approximations as competing structure-exploiting designs. | Does not prove a rank bound for Zhao--Cui filtering targets. |

## Verdict

source_status: `TARGETED_SOURCE_SUPPORTED_AND_CLAUDE_REVIEWED`

The P30 expansion makes Algorithm 5(c.2) explicit enough for focused hostile review, and Claude's focused review found no blocker or major mathematical issue.  The accepted notation clarifications were patched in the P30 note.  PDF text extraction is still imperfect, so this ledger does not claim a full visual source certification of every page in the note.
