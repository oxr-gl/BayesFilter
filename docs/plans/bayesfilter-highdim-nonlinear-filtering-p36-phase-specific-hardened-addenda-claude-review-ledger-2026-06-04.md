# P36 Phase-Specific Hardened Addenda Claude Review Ledger

metadata_date: 2026-06-04

reviewed_artifact:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- Gorodetsky, Karaman, and Marzouk, "A Continuous Analogue of the Tensor-Train
  Decomposition," Computer Methods in Applied Mechanics and Engineering, 2019.

what_is_not_concluded:
- Claude review does not certify mathematical correctness.
- This ledger does not approve production implementation.
- This ledger does not approve DSGE trials.
- This ledger does not approve top-level public API exposure.
- This ledger does not claim adaptive Zhao--Cui differentiability.

## Review Rules

Codex is supervisor and final authority.  Claude Code is a bounded hostile
reviewer.  For each Claude finding, Codex must classify the finding as one of:

```text
ACCEPT
PARTIAL
DISPUTE
CLARIFY
```

Accepted and partially accepted findings require a patch to the addendum.
Disputed findings require a concise rebuttal.  If accepted blockers remain
after max iterations, final acceptance is blocked.

Maximum Claude iterations: 5.

## Iteration 1

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p36-phase-specific-addenda-review-iter1 \
  --model sonnet \
  --effort high \
  "<prompt>"
```

Claude verdict: `FAIL`.

Codex classification summary:

```text
ACCEPT: 6
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| BLOCKER | Phase 4 deferred multivariate Kalman and non-identity/non-uniform reference fixtures to a future result ledger instead of pinning them in the addendum. | ACCEPT | Added exact multivariate LGSSM matrices, observations, expected evidence and retained moments, plus exact affine non-uniform reference fixture with map, reference density, target formula, expected evidence/moments, and tolerances. |
| BLOCKER | Phase 5 finite-difference validity used full branch hashes while the manifest included parameter-perturbed target value hashes, making valid finite-difference rows impossible. | ACCEPT | Added `fd_compatibility_hash`, excluding parameter-perturbed target and derivative values but binding sample set, basis, retained axes/order, coordinate map identity, sweep order, ranks, ridge, solver backend, floors, seed, and pre-replay branch structure. |
| BLOCKER | Phase 5 branch manifest and replay tape were cyclic because `replay_tape_hash` was inside the identity used by the replay tape. | ACCEPT | Replaced replay-tape-in-branch identity with `pre_replay_branch_hash`; replay tape is materialized and hashed after pre-replay branch identity is fixed, then stored in score result and ledger. |
| BLOCKER | Mandatory result-ledger schema omitted evidence fields required by later phase exits. | ACCEPT | Expanded global phase ledger schema with tests, fixtures, tolerances, manifest version, branch hash, replay tape hash when applicable, exact-reference metrics, primary criterion status, veto diagnostics, termination reason, and stop condition. |
| MAJOR | Return types and tensor contracts were still vague for `FunctionalTT.contract_axes`, `SquaredTTDensity.marginal_density`, and `FixedTTFitSampleBatch`. | ACCEPT | Added `TTContractedRepresentation` and `SquaredTTMarginal` field contracts, and expanded `FixedTTFitSampleBatch` tensor shapes and dtypes. |
| MAJOR | Stop conditions were underspecified in Phases 3 and 6. | ACCEPT | Added Phase 3 termination rules for holdout veto, max sweeps, optional early convergence, and ledger fields; added Phase 6 ladder halt/continue rules for regression, numerical veto, resource, implementation, and tuning failures. |

No disputed findings remain after iteration 1.

## Iteration 2

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p36-phase-specific-addenda-review-iter2 \
  --model sonnet \
  --effort high \
  "<prompt>"
```

Claude verdict: `PASS`.

Codex classification summary:

```text
ACCEPT: 0
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| NONE | Claude found no remaining blocker or major defect. | N/A | No patch required. |

## Final Status

Final Claude status: `PASS`.

Open blockers: `NONE`.

Final Codex supervisor decision: `ACCEPT`.

Residual risk:
- This artifact is a hardened implementation contract, not production code.
- Phase 0 implementation may now start, but only under the file write set and
  result-ledger requirements in the addendum.
