# P13 Zhao-Cui TT Discrepancy Report

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.
- P10/P11/P12 BayesFilter Zhao-Cui artifacts.

what_is_not_concluded:
- No posterior accuracy.
- No HMC readiness.
- No global adaptive-code gradient.
- No production implementation.

## Open Disagreements

None at plan-review time.

## Plan Review Discrepancies

Claude accepted the plan.  Codex accepted all three residual risks as
nonblocking controls and recorded them in the Claude review ledger.

## Execution Review Discrepancies

Iteration 1:
Claude rejected with six findings.  Codex classified all six as `ACCEPT` and
patched them.  No disagreement was recorded.

Iteration 2:
Claude accepted the patched artifact.  Codex accepted the residual risks as
nonblocking limitations:
- Proposition 2 is dense but implementable at prototype level.
- The scalar example is illustrative, not a numerical validation.
- The appendix preserves provenance but does not replace the main derivations.

No Codex-Claude disagreement remains.

Decision:
`NO_ACTIVE_CODEX_CLAUDE_DISAGREEMENT_FINAL`
