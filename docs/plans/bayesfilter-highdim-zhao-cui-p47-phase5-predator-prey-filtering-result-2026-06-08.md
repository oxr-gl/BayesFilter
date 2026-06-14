# P47-M5 Result: Predator-Prey Filtering And Preconditioning

metadata_date: 2026-06-08
phase: P47-M5
status: `PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | M5a passed local evidence as lower-rung small additive-Gaussian RK4 predator-prey reference filtering. |
| Primary criterion status | `PASS_LOCAL_M5A`: focused M5a tests pass for dense-reference and Zhao--Cui lower-rung value, state means, and state covariance on the promoted near-RK4 replayable fixture; CUT4 remains finite-metadata diagnostic only; preconditioning metrics remain proxy-only. |
| Veto diagnostic status | The target manifest separates lower-rung reference filtering from production filtering and forbids proxy-only preconditioning promotion. |
| Main uncertainty | The M5a target is a two-state, two-observation lower-rung closure fixture; the earlier tense P44 observation pair remains a documented non-promoted stress failure. |
| Next justified action | Request Claude read-only review for `PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING`; keep M5b production blocked absent a separate production row. |
| Not concluded | No production predator-prey filtering, no nonlinear preconditioning usefulness, no native or non-Gaussian predator-prey correctness beyond the declared closure, no HMC readiness, no production score API, no adaptive MATLAB TT-cross/SIRT reproduction, and no S&P 500 reproduction. |

## Evidence Contract Outcome

M5a freezes the promoted target as a small additive-Gaussian RK4
predator-prey closure on a near-RK4 replayable two-observation fixture.  The
dense reference and Zhao--Cui fixed-design route use the same state law,
observation law, parameter vector, domain policy, and observations.  CUT4
remains a same-closure finite-metadata diagnostic; its likelihood gap, state
moments, and derivative metadata are not promoted.  Predator-prey
preconditioning metrics are explanatory only unless downstream filtering
quality passes under a matched-budget contract.

M5a does not emit `PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING`.

The earlier P44 tense observation pair
`[[51.0, 4.6], [51.7, 5.1]]` was explicitly kept as a non-promoted
transition-approximation stress diagnostic.  On that pair the retained-grid
transition gap was too large for a lower-rung equality pass:
log-likelihood gap about `12.154953`, prey mean error about `18.262935`, and
predator mean error about `0.225982`.  The self-recovery decision was to avoid
promoting that stress pair, not to loosen the pass threshold.

## Skeptical Phase Audit

Status: `PASS_TO_LOCAL_M5A_GATES`.

- Wrong baseline risk: dense tensor-product quadrature is the reference for
  lower-rung Zhao--Cui filtering; CUT4 is not treated as the sole truth.
- Target-mismatch risk: native/non-Gaussian predator-prey and the
  additive-Gaussian RK4 closure are explicitly separated.
- Proxy-metric risk: raw ESS, proposal, or preconditioner metrics cannot
  satisfy M5a without downstream filtering value/state-quality evidence.
- Production-overreach risk: the lower-rung row cannot emit the production
  token.
- Stale-stress-fixture risk: the P44 tense observation pair is preserved as a
  diagnostic non-promotion rather than hidden or retuned into a pass.

## Artifacts

- Target manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-predator-prey-filtering-target-manifest-2026-06-08.json`
- Focused test:
  `tests/highdim/test_p47_predator_prey_filtering.py`

## Local Commands

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p47-predator-prey-filtering-target-manifest-2026-06-08.json
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_predator_prey_filtering.py
```

Result: 5 passed, 2 TensorFlow Probability deprecation warnings.

Promoted near-RK4 fixture metrics:

- Dense reference log likelihood: `-16.415853869084955`
- Zhao--Cui log likelihood: `-16.415898185773344`
- Zhao--Cui minus dense gap: `-4.4316688388335024e-05`
- Log-normalizer gaps: `[-3.217318802484215e-05, -1.2143500364381055e-05]`
- Maximum prey/predator mean errors: `[2.96031998914259e-09, 3.9605652091267984e-11]`
- Maximum covariance-entry error: `1.5164981481976875e-07`
- CUT4 diagnostic log likelihood: `-65.11130903755324`

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_predator_prey_filtering.py
```

Result: passed.

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p47-predator-prey-filtering-target-manifest-2026-06-08.json docs/plans/bayesfilter-highdim-zhao-cui-p47-phase5-predator-prey-filtering-subplan-2026-06-08.md docs/plans/bayesfilter-highdim-zhao-cui-p47-phase5-predator-prey-filtering-result-2026-06-08.md docs/plans/bayesfilter-highdim-zhao-cui-p47-phase5-predator-prey-filtering-claude-review-ledger-2026-06-08.md tests/highdim/test_p47_predator_prey_filtering.py
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_target_registry.py tests/highdim/test_p47_paper_scale_readiness.py tests/highdim/test_p47_predator_prey_filtering.py tests/highdim/test_p46_multistate_zhaocui_adapter.py tests/highdim/test_p45_predator_prey_comparison_blocker.py tests/highdim/test_p44_predator_prey_diagnostic.py tests/highdim/test_p30_predator_prey.py
```

Result: 38 passed, 2 TensorFlow Probability deprecation warnings.

## Claude Review

Iteration 1 returned:

```text
BLOCK_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING
```

Claude found that the executable gate compared value and state means but did
not gate covariance/state-uncertainty despite the result claiming value/state
moments.  Codex repaired the manifest, focused test, and result wording.

Iteration 2 returned:

```text
PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING
```

Claude accepted the lower-rung token after the covariance gate was added and
confirmed that the production token remains out of scope.

## M5b Production Gate Status

Status: `BLOCKED_NO_PRODUCTION_TOKEN`.

A future M5b attempt needs a separate reviewed production/near-paper-scale row
preserving the M5a target, M2 readiness, downstream filtering value/state
metrics, resource caps, wall-time accounting, and matched-budget controls for
any promoted preconditioning claim.
