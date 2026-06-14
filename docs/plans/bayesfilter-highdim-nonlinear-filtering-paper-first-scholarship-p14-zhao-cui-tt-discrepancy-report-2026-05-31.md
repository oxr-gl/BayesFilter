# P14 Zhao-Cui TT Discrepancy Report

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.
- P10/P11/P12/P13 BayesFilter artifacts.

what_is_not_concluded:
- No posterior accuracy.
- No HMC readiness.
- No global adaptive-code derivative.
- No production implementation.

## Plan Review

Plan iteration 1:
Claude rejected with seven findings.  Codex classified all findings as
`ACCEPT` and patched the plan.

Plan iteration 2:
Claude accepted.  Codex classified residual risks as `ACCEPT` nonblocking
limitations.

## Execution Review

Iteration 1:
Claude rejected because equation labels inside unnumbered display math resolved
to section numbers, making the PDF's mathematical navigation ambiguous.  Codex
classified all three findings as `ACCEPT` and patched the note so displayed
formula references resolve to unique equation numbers.  No disagreement was
recorded.

Iteration 2:
Claude accepted.  Codex accepted the residual risks as nonblocking limitations.
No disagreement remains.

Decision:
`NO_ACTIVE_CODEX_CLAUDE_DISAGREEMENT_FINAL`
