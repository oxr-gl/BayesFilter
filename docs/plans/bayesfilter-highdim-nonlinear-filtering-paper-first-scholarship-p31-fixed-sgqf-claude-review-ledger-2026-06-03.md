# P31 Fixed-SGQF Claude Review Ledger

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- Claude review does not certify exact posterior accuracy, production readiness, or every equation in the final note.
- Codex remains final authority and independently classifies every Claude finding.

## Plan Review

### Iteration 1

command:
- `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-p31-fixed-sgqf-plan-review-iter1 --model sonnet --effort high "<focused P31 plan review prompt>"`

claude_verdict:
- `REJECT` for plan execution.

findings:

| id | severity | finding | Codex classification | action |
|---|---|---|---|---|
| P31-PLAN-C1 | `MAJOR` | Same-scalar validation was not a veto; finite-difference parity could remain merely explanatory. | `ACCEPT` | Added same-scalar finite-difference parity and identical saved cloud/branch/stabilization choices as veto diagnostics. |
| P31-PLAN-C2 | `MAJOR` | Plan could still oversell posterior fidelity without an early truth-telling example. | `ACCEPT` | Required a "what this note computes / does not compute" opening plus a nonlinear scalar counterexample. |
| P31-PLAN-C3 | `MAJOR` | Source-order reconstruction still allowed polished summary without claim-to-source mapping. | `ACCEPT` | Required claim-to-source mapping for SGQF blocks and explicit tagging of BayesFilter extensions. |
| P31-PLAN-C4 | `MAJOR` | Implementation contract underspecified for value-and-gradient implementation. | `ACCEPT` | Required implementation-contract table with stored objects, shapes, computation time, and reuse path. |
| P31-PLAN-C5 | `MINOR` | Validation too PDF/algebra heavy and not concrete enough for sparse-grid object. | `ACCEPT` | Required a toy fixed-grid construction check with merged nodes, signed weights, totals, and branch choices. |
| P31-PLAN-C6 | `MINOR` | Reader-facing note structure was looser than review machinery. | `ACCEPT` | Added required reader-facing outline. |

codex_plan_status:
- `PATCHED_AFTER_REJECT_AND_READY_FOR_EXECUTION`

## Execution Review

### Iteration 1

non-substantive attempts:
- Two non-escalated Claude worker attempts failed with API error `400 服务繁忙,请稍后再试`; these are recorded as service failures, not review findings.

trusted command:
- `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-p31-fixed-sgqf-exec-review-iter1-trusted --model sonnet --effort high "<focused P31 execution review prompt>"`

claude_verdict:
- `REJECT`

findings:

| id | severity | finding | Codex classification | action |
|---|---|---|---|---|
| P31-EXEC-C1 | `BLOCKER` | Same-scalar contract omitted observations, initial law, parameter dependence of \(m_0,P_0\), and preprocessing; note and gradient ledger were inconsistent. | `ACCEPT` | Expanded branch tuple, boxed algorithm, implementation contract, and gradient ledger to include \(y_{1:T}\), preprocessing, \(m_0(\theta),P_0(\theta)\), and \(\dot m_0,\dot P_0\). |
| P31-EXEC-C2 | `BLOCKER` | The note included stabilization/floors/clipping in the saved scalar but only derived the plain Cholesky branch. | `ACCEPT` | Narrowed the differentiable lane to symmetrize then veto, with no adaptive jitter/floor/clipping/pivoting inside the differentiated scalar. |
| P31-EXEC-C3 | `MAJOR` | Finite-difference protocol lacked step ladder, absolute/relative acceptance rule, and same-branch requirement. | `ACCEPT` | Added a step ladder, branch-validity rule, relative error metric, and pass criterion. |
| P31-EXEC-C4 | `MAJOR` | Worked finite-difference example tested only innovation-score algebra, not fixed-SGQF-specific plumbing. | `ACCEPT` | Added a cloud-sensitive nonlinear trace using the merged two-dimensional sparse grid and fourth moment. |
| P31-EXEC-C5 | `MINOR` | Notation \(C_t^-C_t^{-\top}\) could be misread as inverse transpose. | `ACCEPT` | Replaced with \(C_t^-(C_t^-)^\top\). |
| P31-EXEC-C6 | `MINOR` | HMC-readiness prose was too strong relative to branch diagnostics. | `ACCEPT` | Softened wording to candidate fixed target for HMC experiments when branch diagnostics remain stable. |

codex_execution_status:
- `PATCHED_AFTER_ITER1_REJECT_CODEX_VALIDATED_POSTPATCH_CLAUDE_API_BLOCKED`

### Iteration 2 Post-Patch Attempts

Post-patch Claude review was attempted three times in trusted mode:

- `highdim-p31-fixed-sgqf-postpatch-review-iter2`
- `highdim-p31-fixed-sgqf-postpatch-review-iter2-retry`
- `highdim-p31-fixed-sgqf-postpatch-minimal-review`

All three attempts failed with API error `400 服务繁忙,请稍后再试`.

postpatch_claude_status:
- `API_BLOCKED_NO_SUBSTANTIVE_FINDINGS`

codex_postpatch_audit:
- Codex independently inspected the patched note and ledger.
- The scalar contract now includes data, preprocessing, initial law, and initial sensitivities.
- The differentiable stabilization branch is narrowed to symmetrize then veto.
- The finite-difference protocol now includes a step ladder, same-branch rule, relative error metric, and pass criterion.
- A nonlinear cloud-sensitive finite-difference trace was added.
- The ambiguous predictive-factor transpose notation was corrected.
- HMC wording was softened to a candidate fixed target when branch diagnostics remain stable.

codex_final_review_status:
- `TARGETED_PASS_WITH_POSTPATCH_CLAUDE_API_BLOCKER`

## Codex Classifications

All iteration-1 execution findings were classified `ACCEPT` and patched.
