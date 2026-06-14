# Plan: R1 Time-3 Observation Log-Probability Micro-Audit

## Scope

This plan executes the exact next diagnostic from the accepted R1
observation-path mismatch localization: freeze the first failing R1
micro-ledger at prefix `T=4`, time `3`, and compare observation
log-probability arithmetic across BayesFilter BF64, executable filterflow
BF32, local BF32 arithmetic, and closed-form scalar formulas.

The question is cross-implementation difference only. This plan does not
assert correctness of BayesFilter or filterflow.

Lane boundary: BayesFilter-owned DPF implementation/evidence lane only. Do not
edit production `bayesfilter/`, `tests/`, `docs/chapters/`, high-dimensional
filtering artifacts, student/vendored code, DSGE/NAWM artifacts, or
`.localsource/filterflow` source.

## Evidence Contract

Primary question: at the first BF64 R1 failure, does the BayesFilter/filterflow
observation-log-likelihood discrepancy arise from observation log-probability
arithmetic itself, from different predicted-particle inputs, from dtype
rounding, or from an upstream mismatch before the observation likelihood?

Primary comparator: local executable filterflow checkout under
`.localsource/filterflow`, with the same R1 fixture used in the accepted
localization result.

Primary criterion:

- `arithmetic_explained` if closed-form recomputation from the recorded
  predicted particles and observation reproduces the observed
  BayesFilter/filterflow observation-log-likelihood delta at time `3` within
  `1e-8` absolute or `1e-8` relative residual;
- `state_delta_dominant` if BF64 closed form on BayesFilter predicted
  particles versus BF64 closed form on filterflow predicted particles explains
  at least 80% of the observed delta;
- `dtype_delta_dominant` if BF64 versus BF32 closed form on the same
  filterflow predicted particles explains at least 80% of the observed delta;
- `mixed_arithmetic_state_dtype` if the combined closed-form decomposition
  explains the observed delta but neither state nor dtype alone explains at
  least 80%;
- `unexplained_upstream_or_wrapper` if closed-form recomputation does not
  reproduce the observed delta.

Veto diagnostics:

- filterflow subprocess blocker;
- nonfinite particles, observations, log-probs, weights, or normalizers;
- trigger mismatch before time `3`;
- CPU-only manifest failure;
- comparator drift;
- forbidden path/import use.

Explanatory diagnostics:

- transport residuals;
- absolute scalar magnitude;
- relative scalar delta;
- AD/FD gradients.

Not concluded:

- production readiness;
- public API readiness;
- posterior correctness;
- HMC readiness;
- general nonlinear-SSM validity;
- DSGE/NAWM validation;
- banking/model-risk claims;
- monograph claims;
- correctness of either implementation;
- dtype or tolerance policy changes.

## Fixed Inputs

- observation path: local executable filterflow `simple_linear_smoothness`
  observation path, scalar first coordinate, `data_seed=123`;
- initial particles: controlled 1D audit `INITIAL_PARTICLES`;
- transition noises: accepted controlled `generated_T100` ledger, prefix `T=4`;
- `theta=0.7`, `Q=0.04`, `R=0.04`, `N=4`, `epsilon=0.25`,
  `scaling=0.9`, `convergence_threshold=1e-6`, `max_iterations=200`;
- target time index: `3`.

## Skeptical Pre-Execution Audit

- Wrong-goal risk: do not decide correctness of either implementation.
- Wrong-baseline risk: use local executable filterflow only.
- Fixture drift risk: transition noises must come from accepted
  `generated_T100`, not from the filterflow fixture.
- Arithmetic overclaim risk: closed-form agreement explains this micro-ledger
  only; it does not validate the full smoothness surface.
- Dtype-policy risk: BF32 is diagnostic only, not a default change.
- Artifact relevance: result must decompose the time-3 observation likelihood
  delta or record a structured blocker.

Audit status: proceed.

## Artifacts

- `docs/plans/bayesfilter-dpf-r1-time3-observation-logprob-audit-plan-2026-06-02.md`
- `docs/plans/bayesfilter-dpf-r1-time3-observation-logprob-audit-result-2026-06-02.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_time3_observation_logprob_audit_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-r1-time3-observation-logprob-audit-2026-06-02.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_r1_time3_observation_logprob_audit_2026-06-02.json`

## Verification

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_time3_observation_logprob_audit_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_r1_time3_observation_logprob_audit_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_r1_time3_observation_logprob_audit_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_r1_time3_observation_logprob_audit_2026-06-02.json
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_time3_observation_logprob_audit_tf.py
rg -n "student|vendored|highdim|DSGE|NAWM|docs/chapters|bayesfilter/" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_time3_observation_logprob_audit_tf.py
git diff --check
git status --short -- bayesfilter tests docs/chapters
git status --short --branch
```
