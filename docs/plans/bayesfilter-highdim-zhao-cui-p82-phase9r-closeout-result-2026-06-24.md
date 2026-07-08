# P82 Phase 9R Result: Closeout After P7R/P8R

status: CLOSED_WITH_P8R_DIAGNOSTIC_ISSUE
date: 2026-06-24
phase: P9R-CLOSEOUT

## Closeout Decision

P82 has now been resumed from the old P7 blocker and executed through the
remaining governed runbook phases:

- P7R resolved the old N10000 memory blocker by producing a valid five-seed
  N10000 actual-gradient artifact through `manual-reverse`, XLA, and
  chunk `2500 x 2500`.
- P8R ran the governed N1000 five-seed 13-point regression-FD comparison.
- P8R did not validate FD consistency: `log_kappa_scale` and `log_nu_scale`
  exceeded the 2 combined-SE triage threshold by large margins.

Therefore P82 closes with a diagnostic issue, not a validation pass.

## Decision Table

| Field | Result |
|---|---|
| Final decision | CLOSED_WITH_P8R_DIAGNOSTIC_ISSUE. |
| P7R status | PASS: N10000 five-seed actual-gradient artifact exists and satisfies route/finite/metadata checks. |
| P8R protocol status | PASS: governed FD protocol ran with 13 raw points, value trimming, 11 fit points, five seeds, N1000, `manual-reverse` XLA AD side, and matching same-scalar metadata. |
| P8R consistency status | FAIL/ISSUE: kappa and nu exceed 2 combined SE; obs-noise is within 2 combined SE. |
| Main blocker now | Gradient-vs-FD mismatch in rate parameters, not memory. |
| Next justified action | New bounded remediation plan focused on kappa/nu mismatch mechanisms. |
| Not concluded | No FD validation, no HMC/default readiness, no posterior correctness, no production readiness, no scientific superiority, and no Zhao-Cui comparator claim. |

## Phase Results

| Phase | Result |
|---|---|
| P6 | Tiny trusted GPU smoke passed previously. |
| P7 old | Blocked by N10000 GPU memory under old `reverse-gradient`/chunk-512 route. |
| P7R | Passed with `manual-reverse` XLA chunk `2500 x 2500`. |
| P8R | Completed but produced diagnostic issue rows. |
| P9R | This closeout. |

## Key Artifacts

| Artifact | Path |
|---|---|
| P7R subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-xla-chunk2500-actual-gradient-remediation-subplan-2026-06-24.md` |
| P7R result | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-xla-chunk2500-actual-gradient-remediation-result-2026-06-24.md` |
| P7R JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-actual-gradient-n10000-xla-chunk2500-gpu-tf32-2026-06-24.json` |
| P8R subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-consistency-subplan-2026-06-24.md` |
| P8R result | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-consistency-result-2026-06-24.md` |
| P8R JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-gpu-tf32-2026-06-24.json` |
| Chunk-sizing memo | `docs/plans/bayesfilter-ledh-pfpf-ot-n10000-chunk-sizing-reset-memo-2026-06-24.md` |

## P8R Comparison Outcome

| Direction | P7R actual | P7R SE | P8R FD slope | FD slope SE | Difference / combined SE | Status |
|---|---:|---:|---:|---:|---:|---|
| `log_kappa_scale` | `-156.6765899658203` | `5.062162399291992` | `-263.2330322265625` | `1.1118820905685425` | `20.559492924382802` | ISSUE |
| `log_nu_scale` | `70.43897247314453` | `1.2023807764053345` | `105.13096618652344` | `0.11481457948684692` | `-28.722101408698713` | ISSUE |
| `log_obs_noise_scale` | `46.97493362426758` | `0.038100458681583405` | `46.83678436279297` | `0.062081485986709595` | `1.8965964644293025` | WITHIN_2SE |

## What Changed Since The Old Stop

The old stop was a compute blocker: P7 N10000 failed before producing the
actual-gradient artifact.  The P7R work resolved that by switching to the
reviewed `manual-reverse` XLA route and using the empirical chunk sizing rule.

The new stop is a numerical/diagnostic mismatch: the actual-gradient artifact
exists, but the governed FD comparison disagrees strongly for rate parameters.

## Recommended Next Remediation

Open a new bounded plan, not an unplanned rerun.  The next plan should isolate
the kappa/nu mismatch with the smallest discriminating checks:

1. Repeat P8R for selected directions only, starting with `log_kappa_scale` and
   `log_nu_scale`, with a base-step ladder around `0.001` to test FD window
   stability.
2. Consider an N ladder for FD (`N=1000`, `2500`, maybe `5000`) before comparing
   against N10000 actual gradient, because P8R compares different particle
   counts.
3. Preserve same seeds and same scalar metadata checks.
4. Keep FD diagnostic-only; do not promote either side as an oracle.
5. Investigate the current repeated XLA retracing/compile overhead separately
   as a performance issue.

## Final Non-Claims

This closeout does not certify LEDH-PFPF-OT gradients, FD agreement, HMC
readiness, posterior correctness, production readiness, scientific superiority,
or Zhao-Cui comparator readiness.
