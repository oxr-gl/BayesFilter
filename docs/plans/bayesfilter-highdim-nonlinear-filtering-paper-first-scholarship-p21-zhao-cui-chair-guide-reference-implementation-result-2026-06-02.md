# P21 Zhao--Cui Chair Guide And Implementation-Ready Specification Result

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.

what_is_not_concluded:
- No executable prototype claim.
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive branch choices.
- No HMC convergence claim.
- No production implementation readiness claim.
- No full adaptive Zhao--Cui implementation claim.

## Status

Decision: `ACCEPTED_AFTER_CLAUDE_EXECUTION_REVIEW_ITERATION_2`.

Outputs created and reviewed:

- P21 chair guide and implementation-ready specification note.
- Fixed-branch implementation-ready specification ledger.
- Equation-to-specification ledger.
- Finite-difference protocol ledger.
- Chair teachability ledger.
- Implementation-readiness ledger.
- Full-algorithm gap register.
- Discrepancy report.

## Review History

Plan review:

- Iteration 1: Claude `ACCEPT`.
- After user guardrails, plan was patched to require P21 to be strictly
  additive to P20 and to forbid executable-code production.
- Iteration 2: Claude `ACCEPT`.

Execution review:

- Iteration 1: Claude `REJECT` for three fixable blockers: carried-filter
  shape/storage contract, finite-difference report schema, and missing
  teach-back checkpoints.
- Codex audit: all three findings classified `ACCEPT`; patches were applied
  to the note and ledgers.
- Iteration 2: Claude `ACCEPT`.

## Main Controls Added After Iteration 1

- Carried one-coordinate coefficient representation:
  \(Q_t,\dot Q_t,P_t,\dot P_t:(p,p)\), query basis
  \(B^{\rm query}:(M,p)\), evaluator outputs \((M,)\), and next-step query
  rule.
- Finite-difference report schema:
  \(\mathcal R_{\rm FD}\), manifest flags \(I_\pm\), recomputed-core flags
  \(K_\pm\), decreasing-window flags \(W_i\), and pass/fail status.
- Equation-backed teach-back checkpoints for squared-density derivative, mass
  contraction derivative, fixed solve derivative, and carried-filter quotient.

## Validation Summary

- P21 PDF rebuilt successfully with `latexmk`; final PDF has 17 pages.
- `git diff --check` passed on modified P21 files.
- LaTeX log scan found no fatal errors, undefined references, citation
  warnings, missing files, or rerun blockers.  Only harmless underfull boxes
  remain in the front table.
- `pdftotext` confirmed the PDF contains the new carried-filter
  representation contract and finite-difference report/status schema.
- P21 markdown artifacts contain `metadata_date`, `seed_papers`, and
  `what_is_not_concluded`.
- No P21 executable code files were found.
- P20 Zhao--Cui artifacts were not edited by this P21 execution.

No executable code was created.  P20 was not edited.

## Residual Risks

- P21 is implementation-ready only for the minimal fixed-branch \(T=2\),
  two-coordinate mathematical specification.
- Full adaptive Zhao--Cui remains future work: TT-cross pivot/rank adaptation,
  domain adaptation, KR engineering, preconditioning, high-dimensional
  diagnostics, and production recovery are intentionally not claimed.
- No finite-difference numerical result or empirical posterior-accuracy result
  is claimed.
