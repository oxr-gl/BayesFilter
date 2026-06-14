# Nonlinear SSM JIT/HMC Phase 4 Full-Chain TFP HMC JIT Result

Date: 2026-06-08

Owning root: `/home/ubuntu/python/BayesFilter`

Supervisor runbook:

- `/home/ubuntu/python/dsge_hmc/docs/plans/BayesFilterDSGE/nonlinear-ssm-jit-hmc-visible-phases-2-9-runbook-2026-06-08.md`

Phase subplan:

- `/home/ubuntu/python/dsge_hmc/docs/plans/BayesFilterDSGE/nonlinear-ssm-jit-hmc-phase-4-full-chain-tfp-hmc-jit-runtime-subplan-2026-06-07.md`

## Status

`PHASE_4_REVIEW_ROUND_1_REPAIRED_READY_FOR_REVIEW`

## Skeptical Audit

Status: passed for the narrow Phase 4 implementation.

- Wrong baseline: this phase certifies a tiny full-chain runtime fixture, not a
  model baseline, posterior baseline, DSGE result, MacroFinance result, NeuTra
  result, or score-matching result.
- Proxy metrics: finite samples, acceptance, trace values, first-call timing,
  warm-call timing, and warning counts are engineering diagnostics only.
- Missing stop conditions: the new tests fail on unreviewed XLA value/score
  authority, target-scope mismatch, unreviewed adaptation policy, missing
  full-chain trace metadata, unavailable diagnostics reported as zero,
  `.numpy()` in the compiled sampling wrapper/target route source, or CPU-only
  GPU visibility.
- Unfair comparison: no method comparison, speed ranking, or sampler ranking is
  made.
- Hidden assumptions: the promoted fixture is a two-dimensional reviewed
  Gaussian adapter. It proves the exact `tfp.mcmc.sample_chain` wrapper can
  compile and return finite tiny-chain tensors under CPU XLA; it does not prove
  nonlinear SSM, DSGE, or real-model HMC readiness.
- Stale context: Phase 3 was accepted by Claude round 2 before this phase. The
  wrapper reuses the Phase 3 authority and target-scope contract shape, but the
  Phase 4 success fixture is a fresh two-dimensional Gaussian runtime canary,
  not the Phase 3 nonlinear SSM Model B target.
- Environment mismatch: CPU-only commands set `CUDA_VISIBLE_DEVICES=-1` before
  TensorFlow import. The explicit TensorFlow probe reported `GPUS=[]`; a CUDA
  no-device log is treated as CPU-hidden framework logging, not GPU evidence.
- Artifact adequacy: this note records commands, git state, write set, tests,
  HMC fixture config, program-signature metadata, CPU/GPU status, trace policy,
  timing metadata, finite checks, nonclaims, and review status.

Reason to proceed: the implementation adds a small BayesFilter-owned wrapper
around exact `tfp.mcmc.sample_chain` and does not alter HMC transition math,
filter equations, target definitions, priors, training objectives, or evidence
criteria.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter run exact full-chain `tfp.mcmc.sample_chain` under JIT on accepted tiny fixtures? |
| Baseline | Phase 3 reviewed target value/score authority and existing HMC helper patterns. |
| Primary criterion | CPU-only tiny full-chain JIT returns finite samples and trace metadata, with unavailable diagnostics reported as unavailable and no convergence claim. |
| Vetoes | Target-only compile treated as full-chain; `.numpy()` inside compiled chain path; unreviewed value/score authority accepted for XLA; target-scope mismatch accepted; unreviewed adaptation policy accepted; changed default HMC transition behavior; unavailable diagnostics reported as zero; tiny metrics overinterpreted. |
| Explanatory only | Acceptance, first/warm timing, trace size, warning counts. |
| Not concluded | No sampler convergence, no posterior validity, no nonlinear SSM readiness, no DSGE readiness, no GPU readiness, no serious model readiness, and no performance superiority. |
| Artifact | This result note plus focused Phase 4 tests. |

## Implementation Summary

Added Phase 4 runtime helpers in:

- `bayesfilter/inference/hmc.py`

New public objects:

- `FullChainHMCConfig`;
- `FullChainHMCRunResult`;
- `run_full_chain_tfp_hmc`.

Behavior:

- constructs exact `tfp.mcmc.HamiltonianMonteCarlo`;
- runs exact `tfp.mcmc.sample_chain`;
- refuses XLA use unless `value_score_capability(adapter)` advertises accepted
  XLA HMC authority;
- binds XLA runtime to the declared `target_scope`;
- uses a `tf.custom_gradient` target wrapper when `log_prob_and_grad` exists so
  TFP gradients follow reviewed value/score authority instead of silently using
  an unreviewed fallback;
- declares `fixed_kernel_no_adaptation` as the only Phase 4 adaptation policy,
  matching the existing BayesFilter `tf_hmc_readiness` smoke helpers; adaptive
  kernels require a later reviewed phase;
- supports `standard` trace and `reduced` trace policies;
- records unavailable trace diagnostics as unavailable, not zero;
- records first-call and warm-call timings outside the compiled sampling path;
- returns TensorFlow tensors and metadata; tensor materialization to NumPy is
  left to callers after the wrapper returns.

Added additive exports in:

- `bayesfilter/inference/__init__.py`;
- `bayesfilter/__init__.py`.

Added focused tests in:

- `tests/test_nonlinear_ssm_phase4_full_chain_hmc.py`.

The large diff against git `HEAD` for `bayesfilter/__init__.py` includes prior
Phase 1R lazy-export replay. The Phase 4 root export delta is additive symbols
for `FullChainHMCConfig`, `FullChainHMCRunResult`, and
`run_full_chain_tfp_hmc`.

## HMC Fixture Config

| Field | Value |
| --- | --- |
| Adapter | `ReviewedGaussianAdapter` |
| Target | two-dimensional standard Gaussian |
| Value | `-0.5 * theta @ theta` |
| Score | `-theta` |
| Authority | `graph_native` |
| Target scope | `phase4_reviewed_gaussian` |
| Initial state | `[0.1, -0.2]`, `tf.float64` |
| `num_results` | `4` |
| `num_burnin_steps` | `2` |
| `step_size` | `0.05` |
| `num_leapfrog_steps` | `2` |
| Seed | `(20260608, 4)` |
| Adaptation policy | `fixed_kernel_no_adaptation` |
| Runtime | `tfp.mcmc.sample_chain` |
| Kernel | `tfp.mcmc.HamiltonianMonteCarlo` |
| JIT | CPU XLA, `jit_compile=True` |
| Trace policies tested | `standard`, `reduced` |

## Trace And Diagnostic Policy

Standard trace records:

- `is_accepted`;
- `log_accept_ratio`;
- `target_log_prob`.

Reduced trace records:

- `trace_collected`.

Diagnostics deliberately record:

- `divergence_status = "unavailable"`;
- `divergence_count = None`;
- `acceptance_rate = None` under reduced trace;
- unavailable trace keys in `metadata["trace_unavailability"]`.

This phase does not report unavailable diagnostics as zero.

## Commands And Results

Commands run:

```text
PYTHONPYCACHEPREFIX=/tmp/bayesfilter_phase4_pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m py_compile bayesfilter/inference/hmc.py bayesfilter/inference/__init__.py bayesfilter/__init__.py tests/test_nonlinear_ssm_phase4_full_chain_hmc.py tests/test_nonlinear_ssm_phase3_value_score_chain.py
```

Result:

- exit code `0`.

Commands run:

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_nonlinear_ssm_phase4_full_chain_hmc.py
```

Result:

- `6 passed, 48 warnings in 4.08s`.

Commands run:

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_nonlinear_ssm_phase4_full_chain_hmc.py tests/test_nonlinear_ssm_phase3_value_score_chain.py tests/test_common_inference_runtime_contracts.py tests/test_nonlinear_ssm_phase2_value_paths.py tests/test_nonlinear_ssm_phase1_contract.py
```

Result:

- `56 passed, 9988 warnings in 38.45s`.

Warnings are TensorFlow Probability/GAST deprecations and pytest cache
read-only warnings. They are not promotion evidence or vetoes for this phase.

Commands run:

```text
CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -c "import os; print('CUDA_VISIBLE_DEVICES=' + str(os.environ.get('CUDA_VISIBLE_DEVICES'))); import tensorflow as tf; print('GPUS=' + repr(tf.config.list_physical_devices('GPU')))"
```

Result:

- `CUDA_VISIBLE_DEVICES=-1`;
- `GPUS=[]`;
- TensorFlow printed a CUDA no-device init log. This is CPU-hidden framework
  logging, not trusted GPU evidence.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `3dac444c22e8a366063f0fa0a73788cc9db96201` |
| Dirty worktree | `true` |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` |
| CPU/GPU status | CPU-only for tests |
| GPU intentionally hidden | yes, `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import |
| Framework GPU visibility | `tf.config.list_physical_devices("GPU") == []` |
| Write set | `bayesfilter/inference/hmc.py`, `bayesfilter/inference/__init__.py`, `bayesfilter/__init__.py`, `tests/test_nonlinear_ssm_phase4_full_chain_hmc.py`, this result note |
| Tests | py_compile with `/tmp` pycache, Phase 4 focused pytest, Phase 1-4 focused pytest |
| Random seeds | `(20260608, 4)` for the tiny HMC fixture |
| Serious experiment | not run |
| GPU experiment | not run |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Submit Phase 4 for Claude review | Passed for tiny full-chain CPU XLA `tfp.mcmc.sample_chain` on reviewed Gaussian fixture | Unreviewed XLA authority rejected; target-scope mismatch rejected; unreviewed adaptation policy rejected; reduced trace reports unavailable diagnostics; source scan test rejects `.numpy()` in compiled wrapper/target route; CPU-only GPU hidden | Only a tiny Gaussian fixture was tested; nonlinear SSM full-chain HMC remains future engineering evidence | Run Claude read-only Phase 4 review; if accepted, proceed to Phase 5 | No convergence, posterior validity, nonlinear SSM readiness, DSGE readiness, GPU readiness, or performance claim |

## Inference-Status Table

| Row | Status |
| --- | --- |
| Hard veto screen | Passed for the Phase 4 engineering gates listed above |
| Statistically supported ranking | N/A; no stochastic method comparison or ranking |
| Descriptive-only differences | Acceptance, finite sample count, first/warm timing, and warning counts are descriptive engineering diagnostics only |
| Default-readiness | Not established |
| Next evidence needed | Phase 5 robust runner/device/performance instrumentation |

## What Is Not Concluded

- This is not evidence of HMC convergence.
- This is not evidence of posterior validity.
- This is not evidence that a nonlinear SSM or DSGE target is ready.
- This is not GPU evidence.
- This is not performance-superiority evidence.
- This does not change HMC defaults.

## Post-Run Red-Team Note

The strongest alternative explanation for a Phase 4 pass is that the reviewed
Gaussian fixture is too simple and does not exercise nonlinear SSM target
complexity or real-model pathological geometry. The result would be overturned
if a nonlinear SSM target cannot use the same full-chain wrapper without host
callbacks, unreviewed gradients, target-scope drift, or unavailable diagnostics.
The weakest part of the evidence is that the tiny chain is only an engineering
canary and cannot support convergence or scientific claims.

## Claude Review

Round 1:

- Reviewer: `nonlinear-ssm-visible-phase-4-review-1`.
- Verdict: `VERDICT: REVISE`.
- Material findings:
  - The implementation used a bare fixed HMC kernel without an artifact saying
    fixed-kernel/no-adaptation is the accepted Phase 4 diagnostic policy rather
    than silent drift from the subplan's default-preservation language.
  - The `.numpy()` source scan did not include `_make_tfp_target_log_prob_fn` or
    the adapter-provided reviewed-score route.
  - The result note wording blurred the baseline by implying the Phase 4 success
    fixture was the Phase 3 nonlinear SSM authority fixture rather than a fresh
    toy Gaussian runtime canary.

Round-1 repairs:

- Added `adaptation_policy="fixed_kernel_no_adaptation"` to
  `FullChainHMCConfig`, recorded it in metadata, and rejected any other policy
  until a later reviewed phase authorizes adaptation.
- Added a Phase 4 test rejecting an unreviewed adaptation policy.
- Widened the `.numpy()` source scan test to include
  `_make_tfp_target_log_prob_fn` and the reviewed Gaussian adapter's
  `log_prob_and_grad` route.
- Clarified this result note: Phase 4 reuses Phase 3-style authority metadata
  and target-scope binding, but its success fixture is a fresh toy Gaussian
  runtime canary, not the Phase 3 nonlinear SSM Model B target.

Status: ready for Claude review round 2 after post-repair focused checks.

Post-repair focused checks:

```text
PYTHONPYCACHEPREFIX=/tmp/bayesfilter_phase4_pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m py_compile bayesfilter/inference/hmc.py bayesfilter/inference/__init__.py bayesfilter/__init__.py tests/test_nonlinear_ssm_phase4_full_chain_hmc.py tests/test_nonlinear_ssm_phase3_value_score_chain.py
```

Result:

- exit code `0`.

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_nonlinear_ssm_phase4_full_chain_hmc.py
```

Result:

- `7 passed, 48 warnings in 4.05s`.

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_nonlinear_ssm_phase4_full_chain_hmc.py tests/test_nonlinear_ssm_phase3_value_score_chain.py tests/test_common_inference_runtime_contracts.py tests/test_nonlinear_ssm_phase2_value_paths.py tests/test_nonlinear_ssm_phase1_contract.py
```

Result:

- `57 passed, 9988 warnings in 38.58s`.

Status: ready for Claude review round 2.
