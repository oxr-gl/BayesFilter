# P11 Zhao-Cui TT Claude Review Ledger

metadata_date: 2026-05-30

seed_papers:
- P11 analytical-derivative plan.
- P11 fixed-branch analytical-derivative note.
- Zhao-Cui JMLR 2024.
- Zhao-Cui companion code audit snapshot.

what_is_not_concluded:
- Claude review is not mathematical certification.
- Claude review is not implementation proof.
- Claude review is not HMC readiness.

## Plan Review Iteration 1

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-p11-zhao-cui-tt-derivative-plan-review-iter1 --model sonnet --effort high "<bounded hostile plan review prompt>"
```

Result:
`ACCEPT`

Minor risks recorded by Claude:
- preserve `log(sirt.z)-const` exactly;
- quarantine adaptive TT-cross, rank truncation, QR/SVD/rounding,
  ESS-triggered reapproximation, and random sampling;
- cite exact paper/code anchors in the note;
- keep MathDevMCP claims narrow;
- include recursive dependence on previous approximate filter.

Codex disposition:
Accepted and enforced in the derivation note.

## Execution Review Iteration 1

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-p11-zhao-cui-tt-derivative-exec-review-iter1 --model sonnet --effort high "<bounded hostile execution review prompt>"
```

Result:
`ACCEPT`

Claude found no major blockers.  Minor residual risks:
- exact differentiated local TT update remains abstract until a concrete
  BayesFilter frozen core-construction branch is chosen;
- future implementation must choose either the direct mass-contraction scalar
  or the QR-contraction code scalar and differentiate the same value path;
- regularity assumptions needed to be more explicit.

Codex disposition:
Accepted.  Codex patched the LaTeX note to add an explicit regularity
assumption paragraph covering differentiability, finite positive normalizers,
support stability, nonsingular fixed linear systems, interchange of
differentiation and contraction/integration, and fixed QR/SVD/Cholesky/root
branches.
