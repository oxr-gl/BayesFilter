# P36 Zhao--Cui Subplan Hardening Claude Review Ledger

metadata_date: 2026-06-04

reviewed_plan:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-plan-2026-06-04.md`

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
- This ledger does not claim adaptive Zhao--Cui differentiability.
- This ledger does not approve top-level public API exposure.
- This ledger does not approve DSGE trials.

## Review Rules

Codex is supervisor and final authority.  Claude Code is a bounded hostile
reviewer.  For each Claude finding, Codex must classify the finding as one of:

```text
ACCEPT
PARTIAL
DISPUTE
CLARIFY
```

Accepted or partially accepted findings require a patch to the P36 plan.
Disputed findings require a concise rebuttal.  If any accepted blocker remains
unpatched after max iterations, P36 final acceptance is blocked.

Maximum Claude iterations: 5.

## Iteration 1

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p36-subplan-hardening-review-iter1 \
  --model sonnet \
  --effort high \
  "<prompt>"
```

Claude verdict: `FAIL`.

Codex classification summary:

```text
ACCEPT: 6
PARTIAL: 1
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| BLOCKER | P36 violated its own symbol-surface rule in Phases 2, 4, and 5 by naming symbols without fields or signatures. | ACCEPT | Added required signature blocks for `DefensiveDensityProtocol`, `TensorProductReferenceDensity`, `SquaredTTDiagnostics`, `KRCDFConfig`, `KRTransport`, `KRInversionResult`, `HighDimCoordinateMap`, `FixedBranchFilterConfig`, `RetainedFilter`, `AdjacentTargetBatch`, `FixedBranchFilterStepResult`, `FixedBranchFilterResult`, `FixedBranchSquaredTTFilter`, `FixedBranchDerivativeConfig`, `FixedBranchReplayTape`, `CoreDerivativeState`, `SweepDerivativeDiagnostics`, `FixedBranchScoreResult`, `FiniteDifferenceRow`, and `FiniteDifferenceTable`. |
| BLOCKER | Phase 5 had derivative equations but not an executable alternating-sweep replay contract. | ACCEPT | Added a Phase 5 replay algorithm with forward/reverse sweep order, pre-update/post-update semantics, replay tape entry schema, accepted/rejected update behavior, cache invalidation rules, and replay-specific tests. |
| MAJOR | Phase 5 branch manifest fields were underspecified. | ACCEPT | Added explicit Phase 5 branch manifest fields including observation hash, retained-filter hashes and axes, coordinate-map identity and parameter-dependence flag, sample/target/weight hashes, per-step fit config, per-sweep update statuses, floors, defensive density, solver backend, deterministic seed, replay tape hash/version, and `moving_basis_supported: false`. |
| MAJOR | Test contracts were named but not pinned with fixture values and tolerances. | PARTIAL | Added exact scalar one-step and two-step Kalman fixture values, a scalar transition-score fixture, finite-difference step grid, LS derivative fixture, normalizer derivative fixture, seeds, branch equality rules, and tolerances. For multivariate Kalman and non-identity reference fixtures, P36 now requires exact matrices and expected values to be checked into the hardened Phase 4 result ledger before production code can pass; Codex did not invent unverified multivariate values in this plan. |
| MAJOR | Failure exits were described as vetoes but not all named as deterministic statuses. | ACCEPT | Added a global deterministic status contract covering CDF, inversion, retained storage, retained measure, unsupported moving-basis derivative, replay mismatch, stale environment, nonfinite retained derivative, derivative solve failure, and finite-difference branch mismatch statuses. |
| MAJOR | Clean-room boundary from P34 was not hardened into implementation phases. | ACCEPT | Added global clean-room rule forbidding `third_party/audit/tensor-ssm-paper-demo/**` and `third_party/audit/zhao_cui_tensor_ssm_p10/source/**` as implementation sources, and required result-ledger fields `clean_room_inputs`, `third_party_code_consulted`, and `clean_room_attestation`. |
| BLOCKER | The review ledger was still pending. | ACCEPT | Updated this ledger with iteration-1 verdict, Codex classifications, and patches. |

No disputed findings remain after iteration 1.

## Iteration 2

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p36-subplan-hardening-review-iter2 \
  --model sonnet \
  --effort high \
  "<prompt>"
```

Claude verdict: `FAIL`.

Codex classification summary:

```text
ACCEPT: 5
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| BLOCKER | The review ledger still had iteration-2 and final status placeholders. | ACCEPT | Updated the ledger with iteration-2 verdict, classifications, and patches; final status remains pending until the next review. |
| BLOCKER | Phase 5 replay omitted the initial core state and initial derivative-core policy/hashes. | ACCEPT | Added Phase 5 manifest fields `initial_core_hashes`, `initialization_rule`, `initial_dot_core_policy`, and `initial_dot_core_hashes`; added replay-tape entry fields and replay algorithm checks before the first core update. |
| BLOCKER | The status contract was inconsistent because Phase 0's enum listed only a partial set. | ACCEPT | Expanded Phase 0 `HighDimStatus(Enum)` to match the full global status namespace and removed conflicting ad hoc names. |
| MAJOR | Phase 5 used both `INVALID_BRANCH_MISMATCH` and `FINITE_DIFFERENCE_BRANCH_MISMATCH` for finite-difference branch mismatch. | ACCEPT | Standardized finite-difference row branch mismatch to `FINITE_DIFFERENCE_BRANCH_MISMATCH`. |
| MAJOR | Phase 5 named one-step Kalman score and scalar nonlinear dense-quadrature score tests without pinned fixtures. | ACCEPT | Added pinned fixtures for one-step scalar Kalman prior-mean score and scalar nonlinear dense-quadrature score, including model, differentiated parameter, observations, expected values, oracle source, and tolerances. |

No disputed findings remain after iteration 2.

## Iteration 3

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p36-subplan-hardening-review-iter3 \
  --model sonnet \
  --effort high \
  "<prompt>"
```

Claude verdict: `FAIL_ON_LEDGER_PLACEHOLDER_ONLY`.

Codex classification summary:

```text
ACCEPT: 1
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| BLOCKER | Review ledger was not closed because iteration 3 and final status still had placeholders while Claude was running. Claude stated the iteration-2 plan-text blockers were resolved. | ACCEPT | Closed iteration 3 in this ledger and set final status to pass on content with no open blockers. |

## Iteration 4

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p36-subplan-hardening-review-iter4 \
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
| NONE | Claude found no remaining blocker or major issue. | N/A | No patch required. |

## Final Status

Final Claude status: `PASS`.

Open blockers: `NONE`.

Final Codex supervisor decision: `ACCEPT`.

Residual risk:
- P36 is a hardening plan, not the hardened P35 implementation specs
  themselves.  Before production code starts, the P35 phase subplans should be
  patched in place or replaced with P36 phase-specific hardened addenda.
- Multivariate Kalman and non-identity reference-map exact fixture values must
  still be checked into the Phase 4 hardened result ledger before Phase 4
  production code can pass.  P36 intentionally does not invent those unverified
  values.
