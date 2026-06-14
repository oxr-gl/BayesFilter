# P50-M3 Sequential Likelihood Path Result

metadata_date: 2026-06-09
phase: P50-M3
status: PASS_P50_M3_SEQUENTIAL_LIKELIHOOD_PATH

## Decision Table

| Field | Decision |
| --- | --- |
| Gate decision | Pass M3 for the focused deterministic sequential likelihood path gate. |
| Primary criterion status | Passed: multi-step tests cover independent Kalman reference agreement, per-step increment agreement, total equals sum of step increments, scalar shape/dtype, retained moment agreement, and deterministic branch replay for the tested path. |
| Veto diagnostic status | Passed: the sequential pass does not rely on one-step tests only; log-likelihood signs are tied to an independent Kalman reference; no stochastic/adaptive operation appears in the tested path. |
| Main uncertainty | M3 covers a low-dimensional linear-Gaussian sequential path only; nonlinear model ladders and gradients begin in later phases. |
| Next justified action | Advance to M4 value/gradient calibration rules after Claude read-only review agrees. |
| Not concluded | No nonlinear model-suite completion, gradient accuracy, HMC readiness, smoothing support, or production readiness. |

## Artifacts

- `tests/highdim/test_p50_sequential_likelihood_path.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-m3-sequential-likelihood-path-result-2026-06-09.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-visible-execution-ledger-2026-06-09.md`

## Tests Added

`tests/highdim/test_p50_sequential_likelihood_path.py` adds:

- an independent covariance-form Kalman reference for a two-dimensional LGSSM;
- three-observation sequential likelihood agreement against the independent
  reference;
- per-step log-normalizer agreement against independent reference increments;
- total log likelihood equals sum of step increments;
- retained mean/covariance agreement after the last update;
- replay stability for result, retained-filter, and per-step branch identities.

## Local Validation

Commands run CPU-only:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p50_sequential_likelihood_path.py tests/highdim/test_p50_one_step_value_path.py tests/highdim/test_public_api_highdim.py tests/highdim/test_phase0_contracts.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p50_sequential_likelihood_path.py tests/highdim/test_p50_one_step_value_path.py
git diff --check -- tests/highdim/test_p50_sequential_likelihood_path.py docs/plans/bayesfilter-highdim-zhao-cui-p50-visible-execution-ledger-2026-06-09.md
git diff --check -- tests/highdim/test_p50_sequential_likelihood_path.py docs/plans/bayesfilter-highdim-zhao-cui-p50-m3-sequential-likelihood-path-result-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p50-visible-execution-ledger-2026-06-09.md
```

Observed results:

- `22 passed, 2 TensorFlow Probability deprecation warnings`;
- compileall passed with no output;
- `git diff --check` passed.

## Claude Review Repair

Claude returned `VERDICT: REVISE` on the first M3 review because the ledger
veto language was too broad.  The tests show sequential value-path agreement and
deterministic replay for the tested path.  They do not exercise gradients,
autodiff robustness, HMC paths, nontrivial integrated Jacobian/proposal
accounting, or nonlinear model ladders.

The result and ledger were patched to keep the M3 pass scoped to deterministic
sequential value-path evidence.

## Non-Claims

M3 does not claim:

- nonlinear model-suite completion;
- value correctness beyond the low-dimensional sequential fixtures tested here;
- gradient correctness;
- autodiff robustness;
- HMC-path robustness;
- nontrivial integrated Jacobian/proposal accounting;
- SV, generalized SV, spatial SIR, or predator-prey readiness;
- HMC readiness;
- smoothing support.
