# Read-Only Review Bundle: Phase 5 Actual-SV Adapter Smoke Result

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. Codex is
supervisor and executor. Claude is read-only reviewer only.

## Objective

Review the implementation/result for the tiny exact transformed actual-SV LEDH
adapter smoke. This is not a full-row admission review.

## Files To Inspect

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-adapter-smoke-subplan-2026-07-07.md`
- `docs/benchmarks/benchmark_ledh_same_target_actual_sv_value.py`
- `docs/plans/ledh-phase5-actual-sv-forward-scalar-tiny-smoke-artifact-2026-07-07.json`
- `tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_tiny_artifact.py`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-adapter-smoke-result-2026-07-07.md`

## Target Contract

Target scalar:

```text
observed_data_log_likelihood_estimator
```

Reported tensor:

```text
log_likelihood
```

Actual-SV target:

```text
z_t = log(y_t^2)
z_t - 2 log(beta) - x_t ~ log(chi_square_1)
```

The artifact must be tiny only:

```text
admission_status = tiny_executed_not_full_row
```

## Commands And Results

Plan review:

```text
direct narrowed Claude read-only review
VERDICT: AGREE
```

Compile check:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile \
  docs/benchmarks/benchmark_ledh_same_target_actual_sv_value.py
```

Result: passed.

Trusted GPU tiny smoke:

```text
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_ledh_same_target_actual_sv_value.py \
  --time-steps 4 --num-particles 128 --batch-seeds 81120 \
  --transport-policy active-all --sinkhorn-iterations 2 \
  --row-chunk-size 64 --col-chunk-size 64 --particle-chunk-size 64 \
  --history-mode full --warmups 0 --repeats 1 \
  --device /GPU:0 --expect-device-kind gpu \
  --output docs/plans/ledh-phase5-actual-sv-forward-scalar-tiny-smoke-artifact-2026-07-07.json \
  --markdown-output docs/plans/ledh-phase5-actual-sv-forward-scalar-tiny-smoke-artifact-2026-07-07.md
```

Result:

- output device: `/job:localhost/replica:0/task:0/device:GPU:0`;
- `log_likelihood_by_seed`: `[-7.566841125488281]`;
- `admission_status`: `tiny_executed_not_full_row`;
- finite output: `true`.

Replay checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py \
  tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_tiny_artifact.py -q
```

Result:

```text
15 passed, 2 warnings in 2.83s
```

## Review Questions

Return `VERDICT: REVISE` if any are true:

- the runner can accidentally run/admit the full `N=10000,T=1000` actual-SV
  row in this smoke subphase;
- the artifact is admitted instead of tiny-only;
- target correction uses raw Gaussian observation likelihood, KSC finite
  mixture, or augmented-noise Gaussian closure;
- exact `log(y^2)` with zero offset is not used;
- `exact_log_chi_square_log_density` is not used in target correction;
- the replay test fails to assert that `require_admitted=True` rejects the tiny
  artifact;
- implementation/result claims score admission, score correctness, HMC
  readiness, posterior correctness, scientific superiority, runtime ranking, or
  full actual-SV row admission.

Return `VERDICT: AGREE` if the implementation/result is consistent with the
tiny-only exact transformed actual-SV adapter smoke plan.

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
