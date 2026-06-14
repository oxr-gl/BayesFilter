# P22 Zhao--Cui Implementation Specification Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.
- P21 chair guide and implementation-ready mathematical specification.

what_is_not_concluded:
- No executable prototype claim.
- No numerical finite-difference pass claim.
- No production implementation readiness claim.
- No full adaptive Zhao--Cui implementation claim.
- No HMC convergence claim.

## Decision

Decision: `FIELD_LEVEL_SPECIFICATION_CARRIED_FORWARD`.

P22 preserves P20's fixed-branch derivation and adds the P21 field-level
controls needed for a later minimal implementation.

## Carried-Filter Representation Contract

| Required field | P22 anchor | Status |
|---|---|---|
| \(Q_t:(p,p)\) | P22-K1 | `SPECIFIED` |
| \(\dot Q_t:(p,p)\) | P22-K4 | `SPECIFIED` |
| \(P_t:(p,p)\) | P22-K5 | `SPECIFIED` |
| \(\dot P_t:(p,p)\) | P22-K5 | `SPECIFIED` |
| query basis \(B^{\rm query}:(M,p)\) | P22-K6 | `SPECIFIED` |
| evaluator output \(\widehat p_t^{\rm ref}:(M,)\) | P22-K7 | `SPECIFIED` |
| evaluator output \(\dot{\widehat p}_t^{\rm ref}:(M,)\) | P22-K7 | `SPECIFIED` |
| next-step query rule \(z^{\rm query}_j=Z_{\rm fit}[j,2]\) | P22-K8 | `SPECIFIED` |

## Finite-Difference Report Schema

| Required field | P22 anchor | Status |
|---|---|---|
| declared scalar \(\widehat\ell_2(\beta_0;B)\) | P22-FD1 | `SPECIFIED` |
| analytical derivative \(G\) | P22-FD0b, P22-FD1 | `SPECIFIED` |
| branch-manifest equality rule | P22-FD2 | `SPECIFIED` |
| recompute-core rule | P22-FD0e, P22-FD3 | `SPECIFIED` |
| step sizes | P22-FD0d | `SPECIFIED` |
| centered difference \(D(h)\) | P22-FD0a, P22-FD1 | `SPECIFIED` |
| absolute and relative errors | P22-FD0c, P22-FD1 | `SPECIFIED` |
| pass/fail criterion | P22-FD5 | `SPECIFIED` |
| expected decreasing-error trend | P22-FD8 | `SPECIFIED` |
| failure interpretations | P22-FD9 | `SPECIFIED` |
| what is not concluded | P22-FD7 | `SPECIFIED` |

## Scope Boundary

The ledger supports a later minimal fixed-branch implementation plan.  It does
not certify adaptive TT-cross, rank adaptation, KR map engineering, nonlinear
preconditioning, or production BayesFilter implementation.
