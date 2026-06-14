# P29 Zhao--Cui Critical Equation Audit Result

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," Annals of Mathematical Statistics 1952.
- Cui and Dolgov, squared inverse Rosenblatt transport / squared TT background used by Zhao and Cui.

audit_scope:
- Focused critical-equation audit over P28's highest-risk blockers.
- Proposition 2, KR/preconditioning Jacobians, mass/normalizer contractions, Algorithm 1/2/5 provenance, notation-shape contract, and MathDevMCP narrow algebra checks.

what_is_not_concluded:
- P29 does not certify all 754 P27 equation environments.
- P29 does not prove production readiness.
- P29 does not run empirical validation.
- P29 does not prove the adaptive Zhao--Cui algorithm is differentiable.

## Summary Verdict

critical_equation_audit_decision: `READY_WITH_TARGETED_LIMITATIONS`

P29 reduces the main P28 mathematical blockers.  The same-scalar fixed-branch derivative argument, the squared-TT mass/normalizer contractions, and the main KR/preconditioning Jacobian directions survive targeted audit.  The remaining high-risk item is Algorithm 5(c.2)'s dense retained-marginal pullback derivation, which should receive visual human source review before a flawlessness-oriented submission.

Front-page exclusion:

`No source-fidelity clearance is granted for Algorithm 5(c.2)'s retained physical marginal derivation, P27 eq:p24-p16--eq:p24-p17, until a visual source review is completed.`

## Ledger Verdicts

| ledger | verdict |
|---|---|
| Proposition 2 derivative | `PASS_TARGETED_AUDIT_WITH_LIMITATIONS` |
| KR and preconditioning Jacobians | `PASS_TARGETED_AUDIT_WITH_ONE_HUMAN_REVIEW_ITEM` |
| Mass and normalizer | `PASS_TARGETED_AUDIT_WITH_LIMITATIONS` |
| Algorithm provenance | `SOURCE_MATCH_TARGETED_WITH_ONE_HUMAN_REVIEW_ITEM` |
| Notation-shape contract | `PASS_TARGETED_AUDIT_WITH_IMPLEMENTATION_CAVEAT` |
| MathDevMCP | `NARROW_SUPPORT_ONLY` |

## Remaining Human-Review Item

| issue id | item | why it remains | recommended action |
|---|---|---|---|
| P29-I001 | Algorithm 5(c.2) retained physical marginal derivation, P27 `eq:p24-p16`--`eq:p24-p17` | It is a dense composite change-of-variables argument and central to preconditioned filtering. Targeted audit found it plausible and source-aligned, but not safe to declare fully certified without visual source review. | Visually compare Zhao--Cui Algorithm 5(c.2), nearby Section 5.4 text, and P27 expansion line by line; optionally add a diagram or short appendix derivation in a P30 submission candidate. |

## Assumption Envelope For Passed Items

The targeted pass statuses apply only under the following assumptions:

- fixed branch: ranks, domains, points, weights, sweep count, pivots, shifts, floors, and regularization are held fixed;
- same-scalar regime: the derivative concerns \(\widehat\ell_T(\beta;B)\), not the adaptive Zhao--Cui algorithm;
- positive finite normalizers: every \(\widehat Z_t\) used in a logarithm or quotient is positive and finite;
- nonzero conditionals: KR conditional denominators are positive on the evaluated support;
- admissible maps: coordinate transforms are invertible on the relevant fitting/sampling domain and use the stated Jacobian orientation;
- nonsingular solves: fixed ridge normal systems are nonsingular in the differentiated neighborhood;
- differentiation-under-integral/contraction conditions are valid for the finite-dimensional branch.

Non-claims:

- no numerical stability theorem;
- no production implementation signoff;
- no global source-fidelity clearance for all P27 displays;
- no empirical validation outcome.

## Provenance Decision Table

| claim | status | allowed use | prohibited inference |
|---|---|---|---|
| Algorithm 1 annotation follows Zhao--Cui | SOURCE_MATCH_TARGETED | Use as targeted provenance support. | Do not claim visual symbol-by-symbol audit of the PDF. |
| Algorithm 2 main squared-TT spine follows Zhao--Cui | SOURCE_MATCH_TARGETED_WITH_REVIEW | Use as targeted provenance support with dense-map caveat. | Do not claim every KR line is visually certified. |
| Algorithm 5 Eq. (30)--(33) preconditioning identities follow Zhao--Cui | SOURCE_MATCH_TARGETED | Use for the general preconditioning framework. | Do not extend this to Algorithm 5(c.2). |
| Algorithm 5(c.2) retained marginal derivation is correct | HUMAN_REVIEW_REQUIRED | Present as plausible targeted-audit item requiring visual review. | Do not claim source-fidelity clearance. |
| MathDevMCP supports selected algebra | NARROW_SANITY_CHECK_ONLY | Cite only as local scalar sanity evidence. | Do not treat as source fidelity or full derivation certification. |
| Fixed-branch derivative differentiates same scalar | PASS_TARGETED_AUDIT_WITH_LIMITATIONS | Use under fixed-branch assumption envelope. | Do not claim adaptive TT-cross differentiability. |

## Direction Ledger Requirement

Before final submission, add or visually verify a one-page direction ledger for the preconditioning/KR chain:

| map | direction | density identity | Jacobian orientation | P27 anchor |
|---|---|---|---|---|
| \(F\) | fitted density to uniform | \(F_\#\widehat p = \mathrm{Unif}\) | \(|\det\nabla F|=\widehat p\) | `eq:p24-k4`--`eq:p24-k5` |
| \(T\) | physical bridge to reference | \(T_\#\rho \propto \eta\) | \(\rho(T^{-1}(u))|\det\nabla T^{-1}(u)|\) | `eq:p24-p1` |
| residual pullback | reference residual to physical | \(\widehat\pi(r)=\widehat\nu^\sharp(T(r))\rho(r)/\eta(T(r))\) | encoded through bridge density ratio | `eq:p24-p4` |
| Algorithm 5(c.2) | residual marginal to retained physical marginal | human-review-required | human-review-required | `eq:p24-p16`--`eq:p24-p17` |

## Residual-Risk Register

| risk class | remaining after P29 | why not fully blocking for targeted verdict | what reopens it |
|---|---|---|---|
| unaudited P28 critical/high displays outside P29 scope | yes | P29 deliberately audited load-bearing pillars only. | Any submission claim that all P27 equations are correct. |
| visual source fidelity for dense maps | yes | Main source spine is targeted-matched, but dense maps need visual check. | Any claim of complete Zhao--Cui annotation fidelity. |
| implementation vectorization/index order | yes | Shape contract is coherent but not executable. | Any production implementation handoff. |
| numerical stability | yes | P27 has diagnostics, but P29 is algebra/source audit. | Any claim of robust large-scale performance. |
| Algorithm 5(c.2) | yes | Explicitly excluded from clearance. | Any preconditioned-filtering submission without visual review. |

## Submission Language After P29

Allowed:

- "The load-bearing fixed-branch derivative, mass-contraction, and main transport identities have passed targeted audit under the stated assumptions."
- "The document is substantially stronger than P28 status and is suitable for expert human review."
- "MathDevMCP supports selected scalar identities; it is not a global proof certificate."

Not allowed:

- "All equations in P27 are certified correct."
- "The adaptive Zhao--Cui algorithm has an analytical gradient."
- "The validation protocol proves large-scale accuracy."
- "Algorithm 5(c.2) is fully source-certified."
- "MathDevMCP establishes full derivation correctness."
- "The P29 target pass clears all P28 critical/high-risk displays."

## Practical Submission Decision

If the submission is to an internal panel with a live presentation and caveats:

- decision: `READY_WITH_TARGETED_LIMITATIONS`

If the submission must claim fully audited mathematical correctness of the entire 103-page note:

- decision: `NOT_READY_PATCH_REQUIRED`

## Recommended Final Patch Before Panel

Create a small P30 or revised submission candidate that either:

1. adds a short visual-source-checked appendix for Algorithm 5(c.2), or
2. narrows the wording around preconditioned retained marginals to say it follows the Zhao--Cui construction and remains a targeted-audit item.

If moving from document audit to implementation, add executable tests for:

- KR Jacobian direction in a two-dimensional density;
- TT mass contraction ordering for a hand-computable three-coordinate example;
- fixed-branch vectorization convention for `A_{j,k} vec(C_k)`;
- quotient derivative for a retained filter;
- branch-stable finite-difference derivative.
