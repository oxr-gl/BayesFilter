# P15 Claude Review Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," FoCM 2022.
- P10-P14 BayesFilter Zhao-Cui TT artifacts.

what_is_not_concluded:
- No posterior accuracy claim.
- No global derivative claim for adaptive TT-cross or rank-changing code.
- No HMC convergence claim.
- No production BayesFilter implementation.
- No default-method recommendation.
- No numerical validation on the target high-dimensional model.

## Plan Review History

| Round | Status | Codex classification | Action |
|---|---|---|---|
| Plan iter1 | REJECT | six findings ACCEPT | patched plan |
| Plan iter2 | ACCEPT | ACCEPT | execution authorized |

## Execution Review History

Pending.

## Execution Review Iteration 1

Claude status: `REJECT`.

| ID | Finding | Codex classification | Patch/action | Status |
|---|---|---|---|---|
| E1-F1 | Next-filter derivative machinery schematic | `ACCEPT` | Added exact square-core coefficients, Q/E/T matrices, prefix/suffix contractions, value/log/derivative/log-derivative evaluator, shapes, and pseudocode; updated two-step script to use saved filter derivative in step 2. | resolved pending rereview |
| E1-F2 | General-rank ALS initialization ambiguous | `ACCEPT` | Replaced prose with exact first-rank-channel initialization formula using e_1 vectors and gamma values. | resolved pending rereview |
| E1-F3 | Source-support ledger missing explicit status fields | `ACCEPT` | Rewrote source-support ledger with publication, local full text, retraction/quarantine, check basis, anchors, allowed/forbidden claims. | resolved pending rereview |
| E1-F4 | Audit-trace anchors inconsistent | `ACCEPT` | Reconciled claim/gradient ledgers to section/proposition descriptions rather than stale proposition numbers. | resolved pending rereview |
| E1-F5 | One-step example did not close recursive persuasion gap | `ACCEPT` | Upgraded reference example and note to two-step carry-forward example using saved numerator/sensitivity object. | resolved pending rereview |

## Execution Review Iteration 2

Claude status: `ACCEPT`.

Codex audit: `ACCEPT`. The acceptance is justified because the patched note specifies the recursive next-filter evaluator, fixed branch choices, same-scalar gradient, source boundaries, and two-step reference example.

Residual non-blocking nit accepted by Codex: result file still said draft in progress. Patched in final result.
