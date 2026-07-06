# P04 Result: Threshold-Support Failure Repair Selection

Date: 2026-06-24

Status: `P04_HANDOFF_POLICY_TUNING`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Select a focused Nystrom policy robustness/tuning path, starting with the existing `svd_truncated` core solver as the next discriminating repair candidate. |
| Primary criterion status | `PASS`: P3 counts reproduced, deterministic invalid rows are empty, and one next path is selected without changing threshold or policy in P04. |
| Veto diagnostic status | `PASS`: P04 did not reinterpret P3 as deterministic failure, did not loosen `tau_component`, did not launch GPU work, and did not make default/HMC/posterior claims. |
| Main uncertainty | The P3 exceedance tail may reflect threshold tightness, stochastic paired-comparator tails, or fixed-policy robustness; P04 cannot decide this without a fresh tuning split. |
| Next justified action | Draft and review P05 SVD core-solver focused tuning on fresh disjoint tuning seeds. |
| What is not being concluded | No new threshold, no validation pass, no policy repair, no default readiness, no posterior correctness, no HMC readiness, no statistical superiority, no broad Nystrom rejection. |

## Reproduced P3 Facts

| Quantity | Value |
| --- | ---: |
| Final P3 status | `P3_INCONCLUSIVE_STOP_THRESHOLD_UNSUPPORTED_BY_PANEL` |
| Deterministic invalid rows | `0` |
| Total deterministic-valid rows | `19` |
| Total exceedances | `3` |
| Exceedance seeds | `82943`, `82944`, `82950` |
| One-sided 95% CP upper bound at stop | `0.35942564964037305` |

The exceedance rows were deterministic-valid legacy-threshold-only benchmark
`FAIL` rows.  They were correctly scored as stochastic exceedances of the frozen
P3 threshold, not deterministic blockers.

## Diagnostic Classification

| Diagnostic | Interpretation |
| --- | --- |
| Nystrom residuals | Small for all included rows; no residual validity failure. |
| Finite factors/particles | Passed for all included rows. |
| Metadata/GPU/TF32/shape/policy | Passed for all included rows. |
| Exceedance magnitude | Modest threshold-tail exceedances: normalized errors around `0.0317`, `0.0376`, `0.0392`. |
| Legacy process exits | Deprecated legacy threshold only; audit-trailed and not deterministic invalidity. |

This pattern points to value-route tail robustness or threshold calibration,
not to a hard implementation failure.

## Candidate Path Selection

| Path | P04 decision | Reason |
| --- | --- | --- |
| Threshold revision | Not selected now | A looser threshold chosen after seeing P3 validation outcomes would need a new calibration principle and fresh validation; it is not the smallest clean next action. |
| Policy robustness/tuning | Selected | Existing opt-in `svd_truncated` core solver changes a plausible numerical robustness lever without changing the threshold, shape, dtype, TF32 mode, comparator, or validation interpretation. |
| Closeout/no-promotion | Not selected now | Valid fallback, but less informative while a bounded, existing SVD robustness lever can be tested on a fresh tuning split. |

## Handoff

Proceed to:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-subplan-2026-06-24.md`

P05 must be reviewed before execution because it would launch material GPU
tuning runs and could influence the next validation design.

## Post-Run Red Team

Strongest alternative explanation: SVD core solving may not affect paired
log-likelihood tails at all because the observed exceedances may be dominated by
landmark selection, kernel approximation, particle path variability, or the
practical threshold being too tight.

What would overturn this handoff: evidence that SVD changes the algorithmic
route too broadly for fair comparison, deterministic failures in focused smoke
tests, or a human decision to close the lane rather than spend GPU on tuning.

Weakest evidence: P04 uses only P3 artifacts and cannot rank repair candidates.
P05 tuning evidence must remain nomination evidence until followed by a fresh
validation split.
