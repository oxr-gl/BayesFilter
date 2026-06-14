# P12 Zhao-Cui TT Self-Contained Proof Expansion Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- Zhao-Cui companion code audit snapshot at `third_party/audit/zhao_cui_tensor_ssm_p10/source`.

what_is_not_concluded:
- No exact posterior accuracy.
- No global analytical gradient for adaptive TT-cross/rank-changing code.
- No HMC readiness.
- No production BayesFilter implementation.
- No default-method recommendation.

## Execution Scope

The P12 note expands the P11 derivative note into a self-contained
proposition-proof document.  It covers:

- state-space filtering from first principles;
- tensor-train notation and squared-TT integration;
- Zhao-Cui sequential squared-TT filtering in BayesFilter notation;
- the fixed-branch TT filtering variant;
- Proposition 1 on normalized approximate filtering;
- Proposition 2 on same-scalar analytical differentiation.

## Skeptical Audit Outcome

The original P12 plan was rejected by Claude on iteration 1 because it did not
force scoped scholarly ledgers required by the audit policy.  Codex agreed,
patched the plan to require source-support, claim-support, coverage/omission,
and quarantine/version checks, and resubmitted.  Claude accepted the patched
plan on iteration 2.

## File Outputs

- LaTeX note:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.tex`
- PDF:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.pdf`
- This ledger plus source, claim, proof, MathDevMCP, Claude, and result
  ledgers.

Decision:
`P12_EXECUTION_DRAFT_REVIEWED_AND_PATCHED_AFTER_CLAUDE_REJECT`
