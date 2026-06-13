# Nonlinear SSM JIT/HMC Phase 2 Compiled Filter Value Result

Date: 2026-06-08

Owning root: `/home/ubuntu/python/BayesFilter`

Supervisor runbook:

- `/home/ubuntu/python/dsge_hmc/docs/plans/BayesFilterDSGE/nonlinear-ssm-jit-hmc-visible-phases-2-9-runbook-2026-06-08.md`

Phase subplan:

- `/home/ubuntu/python/dsge_hmc/docs/plans/BayesFilterDSGE/nonlinear-ssm-jit-hmc-phase-2-compiled-filter-value-paths-subplan-2026-06-07.md`

## Status

`PHASE_2_READY_FOR_CLAUDE_REVIEW`

## Skeptical Audit

Status: passed for the narrow Phase 2 implementation.

- Wrong baseline: this phase certifies fixed-shape nonlinear value paths only;
  it is not a sampler, posterior, DSGE, NeuTra, or MacroFinance baseline.
- Proxy metrics: XLA compile success, finite values, warning counts, and timing
  are engineering diagnostics only.
- Missing stop conditions: the new tests fail on host-callback tokens in
  promoted source paths, missing static shape metadata, regularization mismatch,
  unknown backends, hidden GPU visibility under CPU-only mode, or retracing for
  the same static shape.
- Unfair comparison: no method ranking or speed claim is made.
- Hidden assumptions: promoted value rows are restricted to existing Model B/C
  tiny fixtures and existing TensorFlow SVD sigma-point/CUT4 value filters.
- Stale context: Phase 1R was accepted before Phase 2 started; the result keeps
  Phase 1R and Phase 2 changes distinct.
- Environment mismatch: CPU-only commands set `CUDA_VISIBLE_DEVICES=-1` before
  TensorFlow import.  TensorFlow logged a CUDA no-device message in the explicit
  probe while reporting `GPUS=[]`; this is recorded as CPU-hidden framework log,
  not GPU evidence.
- Artifact adequacy: this note records commands, git state, write set, tests,
  promoted rows, nonclaims, and review status.

Reason to proceed: the implementation adds a small certification layer over
existing BayesFilter graph-native TensorFlow value paths and does not alter
filter equations, sigma-point rules, target definitions, sampler math, priors,
or evidence criteria.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the promoted nonlinear filter value paths run eager, graph, and CPU XLA with fixed-shape parity and no host callback? |
| Baseline | Existing BayesFilter nonlinear value paths and deterministic tiny Model B/C fixtures. |
| Primary criterion | Eager/XLA value and regularization parity passes for promoted paths with static-shape metadata, source host-callback scan success, and no same-shape retracing. |
| Vetoes | `tf.numpy_function`, `tf.py_function`, `.numpy()`, NumPy/SciPy in promoted production value source paths; regularization mismatch; dynamic shape presented as fixed-shape; GPU visible under CPU-only mode; value-only evidence upgraded to score/HMC evidence. |
| Explanatory only | Warning counts, TensorFlow CPU feature log, compile/warm timing implicit in pytest runtime. |
| Not concluded | No gradient correctness, chain-batched target correctness, full-chain HMC, posterior validity, GPU readiness, dynamic-horizon readiness, or performance superiority. |
| Artifact | This result note plus focused Phase 2 tests. |

## Implementation Summary

Added a fixed-shape value-path certification module:

- `bayesfilter/nonlinear/compiled_value_paths.py`

It defines:

- `NonlinearFilterValueStaticShape`;
- `NonlinearFilterValuePathContract`;
- `tensorflow_nonlinear_value_path_contract`;
- `stable_nonlinear_filter_value_path_signature`;
- `find_forbidden_compiled_value_tokens`;
- fail-closed `InvalidCompiledValuePathContract`.

Added focused tests:

- `tests/test_nonlinear_ssm_phase2_value_paths.py`

Updated exports additively in:

- `bayesfilter/nonlinear/__init__.py`;
- `bayesfilter/__init__.py`.

The large diff against git `HEAD` for `bayesfilter/__init__.py` and
`bayesfilter/nonlinear/__init__.py` includes prior Phase 1R lazy-export replay
that was already accepted before this phase.  The Phase 2 delta on top of that
is additive export symbols for the new value-path contract helpers.

## Promoted Value Rows

All promoted rows are fixed-shape CPU XLA value-path rows only.

| Fixture | Model | Backend | Return filtered | Observation shape | Compile mode | Status | Nonclaim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `phase2_model_b_value_fixture` | `model_b_nonlinear_accumulation` | `tf_svd_cubature` | `False` | `(3, 1)` | XLA CPU | passed | no dynamic horizon, score, HMC, GPU, or posterior claim |
| `phase2_model_b_value_fixture` | `model_b_nonlinear_accumulation` | `tf_svd_cubature` | `True` | `(3, 1)` | XLA CPU | passed | no dynamic horizon, score, HMC, GPU, or posterior claim |
| `phase2_model_b_value_fixture` | `model_b_nonlinear_accumulation` | `tf_svd_ukf` | `False` | `(3, 1)` | XLA CPU | passed | no dynamic horizon, score, HMC, GPU, or posterior claim |
| `phase2_model_b_value_fixture` | `model_b_nonlinear_accumulation` | `tf_svd_ukf` | `True` | `(3, 1)` | XLA CPU | passed | no dynamic horizon, score, HMC, GPU, or posterior claim |
| `phase2_model_b_value_fixture` | `model_b_nonlinear_accumulation` | `tf_svd_cut4` | `False` | `(3, 1)` | XLA CPU | passed | no dynamic horizon, score, HMC, GPU, or posterior claim |
| `phase2_model_b_value_fixture` | `model_b_nonlinear_accumulation` | `tf_svd_cut4` | `True` | `(3, 1)` | XLA CPU | passed | no dynamic horizon, score, HMC, GPU, or posterior claim |
| `phase2_model_c_value_fixture` | `model_c_univariate_nonlinear_growth` | `tf_svd_cubature` | `False` | `(2, 1)` | XLA CPU | passed | no dynamic horizon, score, HMC, GPU, or posterior claim |
| `phase2_model_c_value_fixture` | `model_c_univariate_nonlinear_growth` | `tf_svd_cubature` | `True` | `(2, 1)` | XLA CPU | passed | no dynamic horizon, score, HMC, GPU, or posterior claim |
| `phase2_model_c_value_fixture` | `model_c_univariate_nonlinear_growth` | `tf_svd_ukf` | `False` | `(2, 1)` | XLA CPU | passed | no dynamic horizon, score, HMC, GPU, or posterior claim |
| `phase2_model_c_value_fixture` | `model_c_univariate_nonlinear_growth` | `tf_svd_ukf` | `True` | `(2, 1)` | XLA CPU | passed | no dynamic horizon, score, HMC, GPU, or posterior claim |
| `phase2_model_c_value_fixture` | `model_c_univariate_nonlinear_growth` | `tf_svd_cut4` | `False` | `(2, 1)` | XLA CPU | passed | no dynamic horizon, score, HMC, GPU, or posterior claim |
| `phase2_model_c_value_fixture` | `model_c_univariate_nonlinear_growth` | `tf_svd_cut4` | `True` | `(2, 1)` | XLA CPU | passed | no dynamic horizon, score, HMC, GPU, or posterior claim |

## Regularization Diagnostics

The promoted contracts record:

| Field | Value |
| --- | --- |
| Jitter | `0.0` |
| Covariance floor | `1e-12` |
| PSD repair | `tf.linalg.eigh_floor` |
| Symmetrize | `True` |
| Logdet convention | `implemented_regularized_covariance` |
| Implemented covariance | `post_floor_innovation_covariance` |
| Repair role | `target` |

The Phase 2 XLA parity tests compare:

- log likelihood;
- innovation floor count;
- innovation PSD projection residual;
- implemented innovation covariance;
- filtered means and covariances when `return_filtered=True`.

## Host-Callback Scan

Promoted source paths scanned:

- `bayesfilter/nonlinear/sigma_points_tf.py`;
- `bayesfilter/nonlinear/svd_cut_tf.py`;
- `bayesfilter/nonlinear/cut_tf.py`;
- `bayesfilter/linear/svd_factor_tf.py`;
- `bayesfilter/structural_tf.py`.

Forbidden tokens:

- `tf.numpy_function`;
- `tf.py_function`;
- `.numpy(`;
- `np.` or `numpy.`;
- `scipy.`.

Result: no forbidden tokens found in promoted source paths.  The test also
checks that an intentionally blocked fixture containing `tf.numpy_function` and
`.numpy()` is rejected by the scanner.

## Commands And Results

Commands run:

```text
PYTHONPYCACHEPREFIX=/tmp/bayesfilter_phase2_pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m py_compile bayesfilter/nonlinear/compiled_value_paths.py bayesfilter/nonlinear/__init__.py bayesfilter/__init__.py tests/test_nonlinear_ssm_phase2_value_paths.py
```

Result:

- exit code `0`.

Initial py_compile without `PYTHONPYCACHEPREFIX` failed with:

- `[Errno 30] Read-only file system: 'bayesfilter/nonlinear/__pycache__/compiled_value_paths.cpython-313.pyc...'`.

Interpretation: environment write-location failure for pycache, not syntax
failure.  The redirected-pycache compile is the accepted compile check.

Commands run:

```text
CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_nonlinear_ssm_phase2_value_paths.py tests/test_nonlinear_xla_parity_tf.py
```

Result:

- `30 passed, 4409 warnings in 31.38s`.

Commands run:

```text
CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -c "import os; print('CUDA_VISIBLE_DEVICES=' + str(os.environ.get('CUDA_VISIBLE_DEVICES'))); import tensorflow as tf; print('GPUS=' + repr(tf.config.list_physical_devices('GPU')))"
```

Result:

- `CUDA_VISIBLE_DEVICES=-1`;
- `GPUS=[]`;
- TensorFlow printed a CUDA no-device init log.  This is CPU-hidden framework
  logging, not trusted GPU evidence.

Commands run:

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_nonlinear_ssm_phase2_value_paths.py tests/test_nonlinear_xla_parity_tf.py tests/test_nonlinear_ssm_phase1_contract.py tests/test_v1_public_api.py
```

Result:

- `42 passed, 4409 warnings in 31.20s`.

Warnings are TensorFlow Probability/GAST deprecations and pytest cache
read-only warnings.  They are not promotion evidence or vetoes for this phase.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `3dac444c22e8a366063f0fa0a73788cc9db96201` |
| Dirty worktree | `true` |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` |
| CPU/GPU status | CPU-only for tests |
| GPU intentionally hidden | yes, `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import |
| Framework GPU visibility | `tf.config.list_physical_devices("GPU") == []` |
| Write set | `bayesfilter/nonlinear/compiled_value_paths.py`, `bayesfilter/nonlinear/__init__.py`, `bayesfilter/__init__.py`, `tests/test_nonlinear_ssm_phase2_value_paths.py`, this result note |
| Tests | py_compile with `/tmp` pycache, Phase 2 value-path pytest, existing XLA parity pytest, Phase 1 contract pytest, public API pytest |
| Random seeds | N/A |
| Serious experiment | not run |
| GPU experiment | not run |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Submit Phase 2 for Claude review | Passed for fixed-shape CPU XLA value paths on Model B/C cubature, UKF, and CUT4 rows | No host-callback tokens in promoted source paths; regularization parity passed; CPU-only GPU hidden; unknown backend rejected; same-shape concrete function count stable | Only tiny fixed shapes were tested; dynamic horizon, score, chain-batched target, full-chain HMC, and GPU remain untested | Run Claude read-only Phase 2 review; if accepted, proceed to Phase 3 | No gradient correctness, no chain batching, no HMC readiness, no posterior validity, no performance or GPU claim |

## Inference-Status Table

| Row | Status |
| --- | --- |
| Hard veto screen | Passed for Phase 2 engineering gates listed above |
| Statistically supported ranking | N/A; no stochastic method comparison or ranking |
| Descriptive-only differences | Warning counts and runtimes are descriptive only |
| Default-readiness | Not established |
| Next evidence needed | Phase 3 value+score and chain-batched target authority |

## What Is Not Concluded

- No score-path correctness or XLA readiness.
- No chain-batched target correctness.
- No full-chain `tfp.mcmc.sample_chain` JIT readiness.
- No posterior validity or sampler convergence.
- No DSGE, real-NK, NeuTra, score-matching, or MacroFinance readiness.
- No dynamic-horizon support.
- No trusted GPU support or speedup.
- No default policy change.

## Post-Run Red-Team Note

The strongest alternative explanation for a Phase 2 pass is that the current
tiny fixed-shape fixtures are easier than future real targets and that the
existing Python loop over static horizon remains acceptable only because the
horizon is known at trace time.  The result would be overturned if a promoted
source path later acquires a host callback, if a broader fixture reveals a
regularization mismatch, or if Phase 3 cannot compile the actual value+score
target used by HMC.  The weakest part of the evidence is breadth: it certifies
small deterministic value fixtures only.

## Claude Review Status

| Round | Status |
| --- | --- |
| 1 | pending |
