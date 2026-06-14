# P13 Zhao-Cui TT Claude Review Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao-Cui code-audit and source ledgers.
- P11 fixed-branch derivative note.
- P12 self-contained proof expansion note.

what_is_not_concluded:
- No posterior accuracy claim.
- No HMC readiness claim.
- No global derivative of adaptive TT-cross/rank-changing code.
- No production BayesFilter implementation.
- No field-complete literature survey claim.

## Plan Review Iteration 1

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-p13-zhao-cui-tt-human-readable-plan-review-iter1 --model sonnet --effort high "<bounded hostile plan review prompt>"
```

Claude decision:
`ACCEPT`

## Codex-Supervisor Classification Of Claude Residual Risks

| Claude residual risk | Codex classification | Codex audit | Control/action |
|---|---|---|---|
| MathDevMCP is optional for inherited P12 math; execution could under-audit new derivations if the rewrite adds new math. | `ACCEPT` | Correct. The P13 note adds a scalar example and reorganizes derivative exposition. Broad P12 proof checks can be inherited, but new scalar-example algebra should be explicitly classified. | Add a P13 MathDevMCP ledger. Use MathDevMCP for narrow algebra where feasible and mark inherited or human-reviewed proof content honestly. |
| P13 is scoped to note claims, not a full six-ledger field literature audit. | `ACCEPT` | Correct and compatible with the task. The user requested a human-readable rewrite, not a new field survey. | State in source-support ledger and result that P13 relies on P10/P12 source ledgers and does not claim field-complete coverage. |
| The plan says "review-loop artifact" but should make the artifact explicit. | `ACCEPT` | Correct. The explicit artifact should be this ledger. | This ledger is the named review-loop artifact for plan and execution reviews. |

Plan review conclusion:
`PLAN_ACCEPTED_WITH_CODEX_ACCEPTED_NONBLOCKING_CONTROLS`

## Execution Review

### Iteration 1

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-p13-zhao-cui-tt-human-readable-exec-review-iter1 --model sonnet --effort high "<bounded hostile human-reader mathematical review prompt>"
```

Claude decision:
`REJECT`

## Codex-Supervisor Classification Of Execution Iteration 1 Findings

| Claude finding | Codex classification | Codex audit | Patch/control added |
|---|---|---|---|
| Proposition 2 / Section 10 PDF cross-references render ambiguously as repeated "(9)", making implementation path unclear. | `ACCEPT` | Correct. The source used labels on unnumbered displays inside proposition-like contexts, which produced ambiguous PDF references. | Rewrote the sensitivity recipe to name the log-target identity, interpolation sensitivity, least-squares sensitivity, and mass-contraction derivative directly instead of relying on ambiguous numeric cross-references. |
| Section 6 fixed-branch algorithm remains too compressed for minimal prototype implementation. | `ACCEPT` | Correct. The draft gave the right conceptual sequence but did not split interpolation/least-squares and saved derivative objects enough. | Expanded the pseudocode to include target evaluation table, shifted square-root targets, interpolation-vs-LS core solves, mass contraction, normalized joint, marginal numerator, and exact saved branch objects. |
| Scalar example does not fully close the loop with a concrete defensive density and marginal decomposition. | `ACCEPT` | Correct. The example defined the equations but did not instantiate \(\lambda_t\). | Added normalized product defensive density \(\lambda_t=\lambda_x\lambda_{x^-}\) and explicit decomposition of \(\widehat p_t(x_t)\). |
| Proposition 2 needs one more human bridge explaining why same-scalar differentiation matters. | `ACCEPT` | Correct. The previous motivation was present but not sufficiently attached to Proposition 2. | Added sentences explaining that the backward pass must differentiate the stored forward branch, not a fresh adaptive rerun. |
| Appendix wording still sounded like audit language: "implementation evidence ... not mathematical proof." | `ACCEPT` | Correct for user preference. | Rephrased to human reader language: code references show the inspected MATLAB snapshot computes the same scalar structure; mathematical justification remains in main derivations. |
| Result artifact and execution-review closure were incomplete. | `ACCEPT` | Correct at the time of review. | This ledger is being closed after iteration 2; result artifact will be created after final validation. |

Iteration 1 Codex conclusion:
`ALL_FINDINGS_ACCEPTED_AND_PATCHED`

### Iteration 2

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-p13-zhao-cui-tt-human-readable-exec-review-iter2 --model sonnet --effort high "<bounded hostile human-reader mathematical review prompt>"
```

Claude decision:
`ACCEPT`

Residual risks recorded by Claude:
- Proposition 2 remains the densest section for a fresh reader; it is adequate
  for a prototype but not a substitute for model-specific numerical design.
- The scalar example teaches the construction but is not a numerical TT fit or
  performance validation.
- The appendix contains code/source anchors for provenance; Claude did not
  independently re-audit the MATLAB snapshot in iteration 2.

Codex classification:
- `ACCEPT` for all residual risks as nonblocking limitations.

Execution review conclusion:
`EXECUTION_ACCEPTED_ITER2`
