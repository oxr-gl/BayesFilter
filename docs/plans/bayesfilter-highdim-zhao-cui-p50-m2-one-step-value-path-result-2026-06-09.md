# P50-M2 One-Step Value Path Result

metadata_date: 2026-06-09
phase: P50-M2
status: PASS_P50_M2_ONE_STEP_VALUE_PATH

## Decision Table

| Field | Decision |
| --- | --- |
| Gate decision | Pass M2 for the focused one-step deterministic value path gate after claim-boundary repair. |
| Primary criterion status | Passed: one-step tests cover exact Kalman increment agreement, scalar shape/dtype, log-likelihood equals step increment, retained normalizer identity, deterministic branch replay for the tested path, and helper-level Jacobian/shift/proposal accounting identities. |
| Veto diagnostic status | Passed after repair: no NumPy implementation path was added; no stochastic/adaptive operation appears in the tested one-step value path; helper-level accounting identities are preserved. |
| Main uncertainty | The M2 test is intentionally one-step and low-dimensional; nontrivial Jacobian/proposal accounting inside an executed filter path, sequential likelihood, and gradients begin in later phases. |
| Next justified action | Advance to M3 sequential likelihood path after Claude read-only review agrees. |
| Not concluded | No sequential likelihood completion, gradient accuracy, model-ladder pass, HMC readiness, smoothing support, or production readiness. |

## Artifacts

- `tests/highdim/test_p50_one_step_value_path.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-m2-one-step-value-path-result-2026-06-09.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-visible-execution-ledger-2026-06-09.md`

## Tests Added

`tests/highdim/test_p50_one_step_value_path.py` adds:

- exact one-step scalar LGSSM log-likelihood tieout to a known Kalman
  increment;
- equality of total log likelihood and the single step log normalizer;
- retained-filter normalizer identity `normalizer = exp(log_normalizer)`;
- deterministic branch replay checks for result, step, and retained-filter
  identities;
- helper-level Jacobian, target-shift, and proposal-correction accounting
  identities using P49 helper functions.

## Local Validation

Commands run CPU-only:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p50_one_step_value_path.py tests/highdim/test_public_api_highdim.py tests/highdim/test_phase0_contracts.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p50_one_step_value_path.py
git diff --check -- tests/highdim/test_p50_one_step_value_path.py docs/plans/bayesfilter-highdim-zhao-cui-p50-visible-execution-ledger-2026-06-09.md
git diff --check -- tests/highdim/test_p50_one_step_value_path.py docs/plans/bayesfilter-highdim-zhao-cui-p50-m2-one-step-value-path-result-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p50-visible-execution-ledger-2026-06-09.md
```

Observed results:

- `20 passed, 2 TensorFlow Probability deprecation warnings`;
- compileall passed with no output;
- `git diff --check` passed.

## Claude Review Repair

Claude returned `VERDICT: REVISE` on the first M2 review because the original
result prose overstated the evidence.  The tests show:

- integrated one-step LGSSM value-path agreement and normalizer identity;
- deterministic branch replay for the tested one-step path;
- helper-level Jacobian, shift, proposal, and discrete-normalizer algebra.

The tests do not yet show nontrivial Jacobian/proposal accounting inside an
executed one-step filter path, do not expose a `step.accounting_terms` object,
and do not exercise gradients.  The result and ledger were patched to state
that boundary explicitly.

## Non-Claims

M2 does not claim:

- sequential likelihood completion;
- value correctness beyond the one-step fixtures tested here;
- nontrivial Jacobian/proposal accounting inside an executed filter path;
- gradient correctness;
- SV, generalized SV, spatial SIR, or predator-prey readiness;
- HMC readiness;
- smoothing support.
