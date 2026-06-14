# P35 Zhao--Cui Production Implementation Claude Review Ledger

metadata_date: 2026-06-03

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports," Foundations of Computational Mathematics, 2022.

what_is_not_concluded:
- Claude review does not certify implementation correctness.
- Claude review does not replace Codex audit or mathematical tests.
- This ledger does not approve production code changes.

## Iteration 1

Claude verdict: `FAIL`.

Codex classification summary: all findings `ACCEPT`.

| Severity | Claude finding | Codex classification | Patch |
|---|---|---|---|
| BLOCKER | Missing measure contract for fitting versus mass contraction. | ACCEPT | Added `Measure Convention Gate`, measure mismatch veto diagnostics, measure assertions in basis/density phases, and non-uniform reference tests. |
| BLOCKER | Fixed-branch identity contract too weak; finite differences may compare different scalars. | ACCEPT | Added `Realized Branch Identity Contract`, branch hash requirements, and `INVALID_BRANCH_MISMATCH` finite-difference status. |
| MAJOR | Gradient tests certify only internal surrogate differentiation, not inference usefulness. | ACCEPT | Added exact score baselines for one-step/two-step Kalman and dense scalar nonlinear oracles. |
| MAJOR | Clean-room/license boundary is policy-only. | ACCEPT | Added operational provenance rules and a pre-merge code-contamination audit requirement. |
| MAJOR | Performance ladder is too late and misses design-matrix blow-up. | ACCEPT | Added early row/column/memory/rank/coordinate-order gates in Phases 1--3. |
| MINOR | P10 smoke could be overread as correctness evidence. | ACCEPT | Added `STAGE_SANITY_ONLY` label requirement. |

No disputed findings remain after iteration 1.

## Iteration 2

Claude verdict: `PASS_WITH_REQUIRED_EDITS`.

Codex classification summary: all new findings `ACCEPT`.

| Severity | Claude finding | Codex classification | Patch |
|---|---|---|---|
| BLOCKER | Phase 0 backend policy incorrectly started production algebra with NumPy, conflicting with BayesFilter TensorFlow/TFP governance. | ACCEPT | Replaced NumPy-first backend language with TensorFlow/TFP default; NumPy limited to references/fixtures/sanity checks/serialization/reviewed exceptions; JAX/PyTorch require reviewed exception. |
| MAJOR | Realized branch hash could be selective unless full-manifest hashing is required. | ACCEPT | Required canonical serialization and hashing over the full realized branch manifest, including numeric arrays under stable serialization rules. |
| MAJOR | Clean-room provenance lacked role separation after direct upstream inspection. | ACCEPT | Added role separation for modules informed by upstream internals, or explicit single-author non-copy standard plus independent contamination audit. |
| MINOR | Exact score baselines resolved prior surrogate-only gradient issue. | ACCEPT | No further patch required beyond iteration-1 additions. |
| MINOR | Measure contract resolved prior ambiguity. | ACCEPT | No further patch required beyond iteration-1 additions. |
| MINOR | Early memory/rank gates resolved prior late-performance issue. | ACCEPT | No further patch required beyond iteration-1 additions. |
| MINOR | P10 smoke scope is fenced correctly. | ACCEPT | No further patch required beyond iteration-1 additions. |

No disputed findings remain after iteration 2.

## Iteration 3

Claude verdict: `PASS`.

Scope: narrow final review of iteration-2 required edits only.

| Checked item | Status |
|---|---|
| TensorFlow/TFP backend default replaces NumPy-first implementation language. | PASS |
| Realized branch hash is over the full canonical branch manifest. | PASS |
| Clean-room process includes role separation or explicit single-author non-copy standard with independent contamination audit. | PASS |

Final review status: no blockers or required edits remain for P35 plan
execution.
