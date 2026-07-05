# LEDH-PFPF-OT LGSSM N1000 XLA Statistical Result

Date: 2026-06-26

## Decision Table

| Field | Status |
|---|---|
| Decision | Do not close LGSSM value/gradient correctness. The XLA/TF32/manual harness wiring is repaired, but the opt-in N1000 statistical gate fails on value before gradient comparison. |
| Primary criterion | FAIL: LEDH value mean is outside the 2 seed-SD band against the FP64 Kalman reference for both 1d and 2d LGSSM. |
| Veto diagnostics | PASS for route wiring: bounded Claude exact-path review found full-batch XLA, TF32, manual VJP, no Python loops in the compiled/manual route, no `GradientTape`, and no `transport_ad_mode=full`. |
| Main uncertainty | Whether the remaining value mismatch is from LEDH flow/OT value semantics, finite entropic transport bias, or another value-path formula issue. A focused diagnostic suggests it is not mainly Kalman time-index convention. |
| Next justified action | Add a focused value-decomposition test: no-transport SIS, LEDH flow without OT, OT only, and Kalman reference under the same state-time convention. Only after value parity/bias is understood should the gradient gate be interpreted. |
| Not concluded | No SIR gradient correctness, no large-N correctness, no posterior correctness, no HMC readiness, and no scientific claim that LEDH-PFPF-OT is invalid in general. |

## Evidence Contract

Question: does the rewritten LGSSM statistical harness use the intended GPU/XLA/TF32/manual LEDH route, and do the N1000, 10-seed 1d/2d LGSSM value and score estimates fall within 2 seed SD of the exact Kalman value and analytic score?

Baseline/comparator: FP64 analytic Kalman value and score from `tf_batched_kalman_value_and_score`, with the LEDH route kept FP32/TF32/XLA.

Primary criterion: LEDH seed mean must be within `2 * seed_sd` of Kalman for value and score.

Diagnostics that veto: route uses generic autodiff, `transport_ad_mode=full`, Python loops inside the compiled/manual route, XLA does not compile, trusted GPU unavailable, nonfinite output, or value/score outside the stated statistical gate.

Diagnostics that explain only: CUDA/cuDNN duplicate registration warnings, CPU-only focused diagnostics, no-transport SIS comparison, and Kalman time-index convention checks.

## Run Manifest

| Field | Value |
|---|---|
| Git commit | Not recorded in command output; worktree dirty with unrelated existing changes. |
| Main test file | `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py` |
| Route review | Claude exact-path read-only review of `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py`, verdict PASS. |
| Fast checks | `python -m py_compile tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py`; `pytest -q tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py -q` |
| Fast check result | PASS: `ss.....` with full N1000 tests skipped by default. |
| GPU command | `BAYESFILTER_TEST_DEVICE_SCOPE=visible BAYESFILTER_RUN_LEDHPFPFOT_LGSSM_N1000=1 CUDA_VISIBLE_DEVICES=0 TF_FORCE_GPU_ALLOW_GROWTH=true /usr/bin/timeout 900 pytest -q tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py -s` |
| GPU status | Trusted/elevated GPU execution; RTX 4080 SUPER visible; TensorFlow created GPU device; XLA compiled cluster. |
| GPU result | FAIL: 2 failed, 5 passed in 134.47s. |
| Seeds | 10 stateless seed rows, `9100 + seed_index` with independent initial/transition streams. |
| Particle count | N=1000. |
| Time steps | T=10. |
| Precision | LEDH route `float32` with TF32 enabled; Kalman reference arm explicitly FP64. |

## Observed Failure

The test reached the real statistical comparison after XLA compilation. Both opt-in tests failed on value, before the score assertions ran.

| State dim | LEDH value mean | Kalman value | Delta | Seed SD | 2 seed SD |
|---:|---:|---:|---:|---:|---:|
| 1 | -6.507701 | -6.914505 | -0.406804 | 0.00821487 | 0.0164298 |
| 2 | -12.874835 | -13.784139 | -0.909304 | 0.0198057 | 0.0396114 |

## N2000 Particle-Count Diagnostic

The same trusted GPU/XLA/TF32/manual route was rerun with
`BAYESFILTER_LEDHPFPFOT_LGSSM_NUM_PARTICLES=2000`.  XLA compiled and the test
again failed on value before score assertions.

Command:

```bash
BAYESFILTER_TEST_DEVICE_SCOPE=visible \
BAYESFILTER_RUN_LEDHPFPFOT_LGSSM_N1000=1 \
BAYESFILTER_LEDHPFPFOT_LGSSM_NUM_PARTICLES=2000 \
CUDA_VISIBLE_DEVICES=0 \
TF_FORCE_GPU_ALLOW_GROWTH=true \
/usr/bin/timeout 1200 pytest -q tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py -s
```

Result: 2 failed, 5 passed in 147.06s.

| State dim | LEDH value mean at N2000 | Kalman value | Delta | Seed SD | 2 seed SD |
|---:|---:|---:|---:|---:|---:|
| 1 | -6.513121 | -6.914505 | -0.401384 | 0.00862375 | 0.0172475 |
| 2 | -12.870150 | -13.784139 | -0.913989 | 0.0125990 | 0.0251979 |

Interpretation: doubling particles from N1000 to N2000 did not materially shrink
the value gap.  The 1d gap moved from about 0.4068 to 0.4014; the 2d gap moved
from about 0.9093 to 0.9140.  This weakens the hypothesis that the observed
failure is ordinary N1000 particle-count error and strengthens the hypothesis
that the current LEDH flow/OT value path is estimating a different or biased
scalar relative to the Kalman likelihood comparator.

## Focused Diagnostic

After the failed GPU test, a small CPU-only diagnostic was run deliberately with `CUDA_VISIBLE_DEVICES=-1` to compare value semantics. It did not use the GPU; TensorFlow still printed CUDA initialization warnings, which are not GPU evidence.

Comparator values:

| State dim | Kalman transition-first | Kalman observe-initial-first | No-transport SIS mean | No-transport SIS SD |
|---:|---:|---:|---:|---:|
| 1 | -6.914505 | -6.981905 | -6.925509 | 0.065124 |
| 2 | -13.784139 | -13.918564 | -13.857245 | 0.228338 |

Interpretation: the no-transport SIS diagnostic is close to the transition-first Kalman value within its seed variability, while the LEDH+OT value is much higher. This weakens the hypothesis that the main mismatch is only Kalman time-index convention and strengthens the hypothesis that the LEDH flow/OT value path is introducing the value offset.

## Code Changes In This Step

- Rewired stale guard tests to enforce the current policy: no Python `for`/`while` loops in the XLA compiled driver or manual time recursion, with positive checks for `tf.while_loop` and `tf.TensorArray`.
- Kept the LEDH route FP32/TF32/XLA/manual.
- Made only the Kalman reference arm explicitly FP64 to satisfy the existing analytic Kalman helper contract.

## Next Step

Build a focused value decomposition fixture before making gradient claims:

1. FP64 Kalman reference under explicit transition-first convention.
2. Plain no-transport SIS under the same random seeds.
3. LEDH flow without OT transport, preserving corrected weights.
4. LEDH flow plus OT, current route.
5. Per-time incremental log-likelihood table for all arms.

Stop if the value discrepancy appears before OT; then inspect LEDH proposal density/log-det correction. If it appears only after OT, inspect whether the OT step changes the likelihood estimator being compared to Kalman.

## Follow-Up Decomposition Result

The follow-up plan
`docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-value-decomposition-hypothesis-test-plan-2026-06-26.md`
was reviewed by Claude. The first review failed because the threshold, time-index
probe, and LEDH-no-OT/LEDH+OT isolation contract were underspecified. The plan
was patched and the second Claude review returned `VERDICT: PASS`.

Executed diagnostic artifacts:

- `docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_value_decomposition.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-value-decomposition-n1000-xla-2026-06-26.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-value-decomposition-n1000-xla-2026-06-26.md`

Trusted GPU/XLA command:

```bash
BAYESFILTER_TEST_DEVICE_SCOPE=visible \
CUDA_VISIBLE_DEVICES=0 \
TF_FORCE_GPU_ALLOW_GROWTH=true \
/usr/bin/timeout 900 \
python docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_value_decomposition.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --xla \
  --num-particles 1000 \
  --state-dims 1 2 \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-value-decomposition-n1000-xla-2026-06-26.json \
  --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-value-decomposition-n1000-xla-2026-06-26.md
```

Result: PASS for execution and localization. TensorFlow created the GPU device
and XLA compiled the diagnostic cluster. Runtime was 18.54s.

| State dim | Arm | Mean | Kalman | Delta | SD | MCSE | abs z | abs seed-SD units | First failing prefix |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | SIS/no transport | -6.925509 | -6.914505 | -0.011004 | 0.065124 | 0.020594 | 0.534 | 0.169 | None |
| 1 | LEDH/no OT | -6.912147 | -6.914505 | 0.002358 | 0.004565 | 0.001444 | 1.634 | 0.517 | None |
| 1 | LEDH+OT | -6.507701 | -6.914505 | 0.406804 | 0.008215 | 0.002598 | 156.597 | 49.520 | 1 |
| 2 | SIS/no transport | -13.858361 | -13.784139 | -0.074222 | 0.228468 | 0.072248 | 1.027 | 0.325 | None |
| 2 | LEDH/no OT | -13.793434 | -13.784139 | -0.009296 | 0.021238 | 0.006716 | 1.384 | 0.438 | None |
| 2 | LEDH+OT | -12.874837 | -13.784139 | 0.909302 | 0.019806 | 0.006263 | 145.181 | 45.910 | 1 |

Interpretation: the value gap appears only after OT/reset. This weakens the
LEDH proposal-density/log-determinant hypothesis for the current LGSSM fixture:
the LEDH-no-OT arm is close to Kalman in both 1d and 2d. The next focused
hypothesis is that the current OT reset-to-uniform operation changes the future
proposal/filtering scalar being compared to Kalman rather than preserving the
same marginal likelihood estimator.
