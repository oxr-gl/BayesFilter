# Broader Exact-Transformed SV Fixed-SGQF Precursor Ladder Result Note

metadata_date: 2026-06-26
program_id: exact-transformed-sv-fixed-sgqf-broader-precursor-ladder
status: PASS_SMALL_INTERNAL_VALUE_ONLY_PRECURSOR_LADDER
plan_file: docs/plans/bayesfilter-exact-transformed-sv-fixed-sgqf-broader-precursor-ladder-plan-2026-06-26.md

## Plan reference
- `docs/plans/bayesfilter-exact-transformed-sv-fixed-sgqf-broader-precursor-ladder-plan-2026-06-26.md`
- `docs/plans/bayesfilter-exact-transformed-sv-fixed-sgqf-precursor-result-2026-06-26.md`
- `docs/plans/bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md`

## Question
Does the current internal
`exact_transformed_sv_independent_panel_fixed_sgqf_filter(...)` route remain a
numerically controlled same-target, independent-panel, value-only precursor when
we move beyond the original single tiny fixture to a small nearby ladder?

## Skeptical audit outcome
Pass, with explicit claim ceiling.

Why the audit still passes:
- every comparison stays against the same-target dense exact-transformed
  reference;
- the ladder remains a focused deterministic diagnostic, not a runner/leaderboard
  promotion run;
- runtime or sparse-level improvement are explanatory only and not promotion
  criteria;
- the failure policy stayed explicit: if the broadened ladder failed, the claim
  would fall back to the earlier single-fixture result rather than expanding by
  narration.

## Evidence contract
Baseline / truth anchor:
- `highdim.exact_transformed_sv_independent_panel_dense_reference(...)`

Primary promotion criterion:
- on the broadened ladder, SGQF remains finite and within declared dense
  reference tolerances for:
  - total log-likelihood,
  - per-time log normalizers,
  - filtered mean path,
  - filtered covariance path.

Veto diagnostics:
- non-finite outputs,
- dense-reference disagreement beyond the broadened thresholds,
- covariance structure inconsistent with the independent-panel design,
- evidence that the original single-fixture tolerances were accidental.

Explanatory-only diagnostics:
- sparse-level sensitivity,
- whether modest horizon extension enlarges the gaps,
- whether nearby parameter changes are more important than horizon extension.

What is not concluded:
- no analytical-score claim,
- no generic non-Gaussian SGQF core support,
- no source-faithful/source-row admission,
- no generalized-SV or spatial-SIR unlock,
- no HMC or production-readiness claim.

## Command actually run
Gap-probing diagnostic:
```bash
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
import tensorflow as tf
import bayesfilter.highdim as highdim
import bayesfilter.highdim.sv_mixture_cut4 as mod

BASE_VALUES = tf.constant([[0.12, -0.08, 0.05],[-0.07,0.11,-0.04]], dtype=tf.float64)
BASE_GAMMA = tf.constant([0.60, 0.52, 0.47], dtype=tf.float64)
BASE_BETA = tf.constant([0.40, 0.35, 0.45], dtype=tf.float64)
BASE_SIGMA = tf.constant([1.00, 0.85, 0.75], dtype=tf.float64)
# ... deterministic ladder probes over nearby parameters, longer horizon, and sparse levels ...
PY
```

Compile check:
```bash
CUDA_VISIBLE_DEVICES=-1 python -m compileall -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py
```

Focused verification:
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py -k "fixed_sgqf or exact_transformed"
```

## Run manifest
| Field | Value |
|---|---|
| git commit | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| git branch | `zhaocui-fixed-branch-derivative-validation` |
| environment | `tf-gpu` conda env |
| CPU/GPU status | `CPU-only; CUDA_VISIBLE_DEVICES=-1` |
| plan path | `docs/plans/bayesfilter-exact-transformed-sv-fixed-sgqf-broader-precursor-ladder-plan-2026-06-26.md` |
| result path | `docs/plans/bayesfilter-exact-transformed-sv-fixed-sgqf-broader-precursor-ladder-result-2026-06-26.md` |
| code surfaces | `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py` |
| seeds | deterministic fixture cases only |
| wall time | probe + focused pytest under a minute of direct compute; pytest 17.33s |

## Result summary
The broadened precursor ladder passed.

New evidence now covers:
- the original dim 1/2/3 tiny fixture,
- two nearby parameter families,
- a modest horizon extension,
- explanatory sparse-level sensitivity on a representative longer-horizon dim-1
  case.

This broadens the evidence claim from:
- **single tiny fixture precursor**

to:
- **small internal exact-transformed value-only precursor ladder**.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| focused pytest status | `25 passed` | Expanded exact-transformed / Fixed-SGQF ladder passed on CPU-only execution. |
| warnings | `2 deprecation warnings` | TFP packaging/version warnings only. |
| worst-case `log_likelihood` gap | `0.06737006949565583` | Occurred on the longer-horizon dim-3 case; within the broadened longer-horizon threshold. |
| worst-case `log_normalizers` gap | `0.030094481231031978` | Longer-horizon case dominates stepwise gap growth. |
| worst-case `mean_path` gap | `0.07965599847609695` | Longer-horizon case dominates mean-path gap growth. |
| worst-case `variance_path` gap | `0.2039057603443306` | Nearby-parameter case `nearby_b` produced the widest variance gap; still within the broadened nearby-parameter threshold. |
| worst-case off-diagonal leakage | `0.0` | Independent-panel diagonal covariance structure held exactly across the tested ladder. |
| representative level-1 gap | `log=1.1517425471414242` | Level 1 is clearly too coarse on the representative longer-horizon dim-1 case. |
| representative level-2 gap | `log=0.052509973784054864` | Level 2 remains usable but materially less accurate than level 3 on the representative case. |
| representative level-3 gap | `log=0.004196109570013817` | Level 3 sharply improves the representative longer-horizon dim-1 case. |

## Engineering observations
- No implementation-file change was needed; the broadened evidence came entirely
  from test expansion.
- The off-diagonal leakage stayed identically zero because the wrapper remains an
  independent-panel diagonal-covariance construction.
- The broadened evidence required relaxed thresholds relative to the original
  two-step tiny fixture, especially on the longer-horizon ladder and one nearby
  parameter family.
- Sparse-level behavior is informative: level 1 is much too coarse on the
  representative longer-horizon case, while level 3 provides a substantial
  accuracy improvement over level 2.

## Empirical evidence
- The current exact-transformed SGQF wrapper is not merely a one-fixture
  curiosity: it remains numerically controlled on a small nearby internal ladder.
- The modest horizon extension increases gaps more than the nearby parameter
  perturbations do, though one nearby parameter family widened the variance gap.
- The representative sparse-level diagnostic shows a clear refinement story for
  the tested dim-1 longer-horizon case: level 3 > level 2 > level 1 on the
  value-path gap metrics.

## Mathematical claims
- No new mathematical claim is promoted.
- This note records broader numerical agreement against the same-target dense
  exact-transformed reference on a small deterministic ladder only.
- It does not establish generic non-Gaussian SGQF correctness.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| pass broadened precursor ladder with recorded limits | satisfied on the broadened deterministic ladder with explicit longer-horizon and nearby-parameter thresholds | no non-finite outputs, no covariance leakage, and no target-identity drift observed in the tested lane | whether this small internal ladder says anything useful about the program’s preferred augmented-noise-first unlock path | keep the route internal/value-only and use this broader result as a bounded evidence anchor, then return to augmented-noise-first planning | no analytical score, source-row admission, generic non-Gaussian core, generalized-SV, HMC, or production claim |

## Post-run red-team note
Strongest alternative explanation:
- the route may still look stronger than it is because the broadened ladder is
  small and factorized, so success here may still be specific to independent-
  panel tiny fixtures rather than evidence for a general non-Gaussian SGQF path.

What would overturn the broadened conclusion:
- failure on the next modest horizon increase,
- instability under a slightly wider nearby-parameter family,
- or downstream artifacts using this internal ladder as if it were source-row or
  analytical-score evidence.

Weakest part of the evidence:
- the broader ladder remains value-only and wrapper-specific; it still does not
  exercise a generic non-Gaussian Fixed-SGQF core.

## Next steps
1. Treat this note as the evidence ceiling for the current internal exact-
   transformed SGQF wrapper: a **small internal value-only precursor ladder**.
2. Do not broaden the claim further without a reviewed plan and another same-
   target dense-reference pass.
3. Return to the master program’s augmented-noise-first source-scope unlock path
   rather than continuing to build a generic non-Gaussian SGQF story from this
   wrapper alone.
4. If this wrapper is revisited later, the next honest expansion would be a
   slightly broader horizon/parameter ladder, not public export or score
   promotion.
