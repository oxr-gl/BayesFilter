# Nonlinear SSM JIT/HMC Phase 3 Value/Score Chain Batching Result

Date: 2026-06-08

Owning root: `/home/ubuntu/python/BayesFilter`

Supervisor runbook:

- `/home/ubuntu/python/dsge_hmc/docs/plans/BayesFilterDSGE/nonlinear-ssm-jit-hmc-visible-phases-2-9-runbook-2026-06-08.md`

Phase subplan:

- `/home/ubuntu/python/dsge_hmc/docs/plans/BayesFilterDSGE/nonlinear-ssm-jit-hmc-phase-3-value-score-chain-batching-subplan-2026-06-07.md`

## Status

`PHASE_3_REVIEW_ROUND_1_REPAIRED_READY_FOR_REVIEW`

## Skeptical Audit

Status: passed for the narrow Phase 3 implementation.

- Wrong baseline: this phase certifies target-only value/score authority and
  static chain-batch semantics on tiny fixtures. It is not a sampler baseline,
  posterior-validity claim, DSGE result, MacroFinance result, NeuTra result, or
  score-matching result.
- Proxy metrics: XLA compile success, finite values, finite gradients, warning
  counts, and runtime are engineering diagnostics only.
- Missing stop conditions: the tests fail on unreviewed XLA authority, target
  scope mismatch, non-rank-2 chain state, missing static chain/parameter
  dimensions, chain-order drift, scalar/batched parity drift, MAP/mass signature
  mismatch, dense whitening orientation drift, or CPU-only GPU visibility.
- Unfair comparison: no method comparison, speed ranking, or sampler ranking is
  made.
- Hidden assumptions: the promoted chain policy is static Python unroll over a
  known leading chain axis; it intentionally does not claim true vectorized-map,
  map-fn, or full-chain TFP HMC semantics.
- Stale context: Phase 1R and Phase 2 were accepted before this phase. Phase 3
  adds only target value/score and static chain-batch authority on top of those
  contracts.
- Environment mismatch: CPU-only commands set `CUDA_VISIBLE_DEVICES=-1` before
  TensorFlow import. The explicit TensorFlow probe reported `GPUS=[]`; a CUDA
  no-device log is treated as CPU-hidden framework logging, not GPU evidence.
- Artifact adequacy: this note records commands, git state, write set, tests,
  authority metadata, derivative provenance, chain-batching policy, nonclaims,
  and review status.

Reason to proceed: the implementation adds a small target-only helper that
fails closed for unreviewed XLA value/score authority and target-scope mismatch.
It does not alter filter equations, target definitions, priors, sampler math,
HMC transitions, training objectives, or evidence criteria.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter expose graph-native or reviewed target value+score authority for scalar and chain-batched states? |
| Baseline | Phase 2 value path plus existing adapter value/score helpers and Phase 1 adapter metadata. |
| Primary criterion | Target-only CPU XLA value/score parity passes for scalar and chain-batched fixtures with accepted authority metadata and preserved chain order. |
| Vetoes | Unreviewed GradientTape accepted for XLA; scalar-only path mislabeled batched; chain-axis/order failure; target-scope mismatch accepted; wrong dense whitening score orientation; MAP/mass reuse without signature validation; GPU visible under CPU-only mode. |
| Explanatory only | Gradient norm, compile time, warning count, tiny fixture runtime, TensorFlow CPU feature logs. |
| Not concluded | No full-chain TFP HMC JIT, no sampler convergence, no posterior validity, no dynamic horizon readiness, no GPU readiness, no performance superiority, and no scientific model result. |
| Artifact | This result note plus focused Phase 3 tests. |

## Implementation Summary

Added target-only chain value/score helper in:

- `bayesfilter/inference/hmc.py`

New public helper:

- `static_unroll_chain_value_and_score(adapter, chain_state, use_xla=False, target_scope=None)`

Behavior:

- accepts adapters exposing `log_prob_and_grad`;
- refuses XLA use unless `value_score_capability(adapter)` advertises accepted
  XLA HMC authority;
- binds reviewed authority to `target_scope` when the capability declares one;
- requires static rank-2 chain state `[chain, parameter]`;
- requires statically known chain and parameter dimensions;
- evaluates each chain row in canonical leading-axis order by static Python
  unroll;
- stacks TensorFlow rows with `tf.stack` and NumPy rows with `np.stack`.

Also tightened `_make_hmc_target_log_prob_fn` so any XLA capability with a
declared `target_scope` is bound to the requested target scope, not only the
reviewed GradientTape exception.

Added exports in:

- `bayesfilter/inference/__init__.py`;
- `bayesfilter/__init__.py`.

Added focused tests in:

- `tests/test_nonlinear_ssm_phase3_value_score_chain.py`;
- `tests/test_common_inference_runtime_contracts.py`.

The large diff against git `HEAD` for `bayesfilter/__init__.py` includes prior
Phase 1R lazy-export replay that was already accepted before Phase 2. The Phase
3 delta on top of that is the additive export for
`static_unroll_chain_value_and_score`.

## Authority Table

| Adapter/fixture | Authority | XLA accepted | Runtime backend | Target scope | Evidence path | Status | Nonclaim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ModelBReviewedValueScoreAdapter` | `graph_native` | yes | `tensorflow` | `phase3_model_b_cut4_target_only` | `tests/test_nonlinear_ssm_phase3_value_score_chain.py` | passed scalar and static-chain parity | target-only fixture, not full-chain HMC |
| `ReviewedAdapter` toy NumPy fixture | `graph_native` | yes | `toy_graph` | none | common runtime contract tests | passed static chain order and scalar parity | toy fixture only |
| `DebugValueScoreAdapter` | implicit `gradient_tape_fallback` | no | inferred/debug | none | common runtime contract tests | correctly rejected for XLA chain helper | debug fallback only |
| `ReviewedTapeAdapter` | `reviewed_gradient_tape_xla_exception` | yes when scoped | toy/debug | `toy-target` | `docs/plans/reviewed-target.md` | accepted only for matching scope | toy contract fixture only; not promoted scientific authority |

## Derivative Provenance

| Path | Provenance | Phase 3 role | Status |
| --- | --- | --- | --- |
| Model B scalar value/score | Existing TensorFlow target `target_log_prob_and_grad` from `ModelBNonlinearSVDTarget.default()` | Promoted target-only scalar parity fixture | passed eager, graph, and CPU XLA parity |
| Model B static chain value/score | Static unroll over the same scalar `log_prob_and_grad` authority | Promoted target-only chain-batch fixture | passed CPU XLA parity and order-preservation checks |
| Toy NumPy adapter | Analytic toy score `-theta` | Runtime-contract semantics check | passed scalar/chain parity and fail-closed tests |
| Dense whitening score | Algebraic helper `theta = center + z @ W.T`, latent score `W.T @ grad_theta` | Orientation guard | passed orientation test |
| MAP/mass reuse | Stable adapter signature plus shape checks | Reuse guard only | mismatched dimension, covariance shape, signature, and process-local signature rejected |

## Chain-Batching Policy

Phase 3 uses static Python unroll over a statically known leading chain axis.
This was chosen as the narrowest safe bridge between scalar target authority
and future full-chain TFP HMC gates.

This phase deliberately does not promote:

- `tf.map_fn`;
- `tf.vectorized_map`;
- dynamic chain counts;
- full `tfp.mcmc.sample_chain`;
- sampler transition semantics.

If candidate results complete in nondeterministic order in a future worker
runner, that belongs to runner/candidate-result logic, not this target-only
value/score helper. This helper preserves the input chain order exactly.

## Commands And Results

Commands run:

```text
PYTHONPYCACHEPREFIX=/tmp/bayesfilter_phase3_pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m py_compile bayesfilter/inference/hmc.py bayesfilter/inference/__init__.py bayesfilter/__init__.py tests/test_common_inference_runtime_contracts.py tests/test_nonlinear_ssm_phase3_value_score_chain.py
```

Result:

- exit code `0`.

Commands run:

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_nonlinear_ssm_phase3_value_score_chain.py tests/test_common_inference_runtime_contracts.py tests/test_nonlinear_ssm_phase1_contract.py tests/test_nonlinear_ssm_phase2_value_paths.py
```

Result:

- `48 passed, 9897 warnings in 37.25s`.

Warnings are TensorFlow Probability/GAST deprecations and pytest cache
read-only warnings. They are not promotion evidence or vetoes for this phase.

Review-round-1 repair added two explicit unknown-static-dimension tests to
`tests/test_nonlinear_ssm_phase3_value_score_chain.py`. The post-repair rerun
is:

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_nonlinear_ssm_phase3_value_score_chain.py tests/test_common_inference_runtime_contracts.py tests/test_nonlinear_ssm_phase1_contract.py tests/test_nonlinear_ssm_phase2_value_paths.py
```

Result:

- `50 passed, 9943 warnings in 36.51s`.

Commands run:

```text
CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -c "import os; print('CUDA_VISIBLE_DEVICES=' + str(os.environ.get('CUDA_VISIBLE_DEVICES'))); import tensorflow as tf; print('GPUS=' + repr(tf.config.list_physical_devices('GPU')))"
```

Result:

- `CUDA_VISIBLE_DEVICES=-1`;
- `GPUS=[]`;
- TensorFlow printed a CUDA no-device init log. This is CPU-hidden framework
  logging, not trusted GPU evidence.

## Known Caveat

TensorFlow/XLA can ignore `tf.debugging.assert_*` ops in compiled graphs. Phase
3 does not rely on those graph asserts as scientific safety evidence. The
promoted evidence is limited to deterministic tiny-fixture value/score parity,
explicit Python-side capability checks, target-scope binding, static shape
checks, and order-preservation tests.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `3dac444c22e8a366063f0fa0a73788cc9db96201` |
| Dirty worktree | `true` |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` |
| CPU/GPU status | CPU-only for tests |
| GPU intentionally hidden | yes, `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import |
| Framework GPU visibility | `tf.config.list_physical_devices("GPU") == []` |
| Write set | `bayesfilter/inference/hmc.py`, `bayesfilter/inference/__init__.py`, `bayesfilter/__init__.py`, `tests/test_common_inference_runtime_contracts.py`, `tests/test_nonlinear_ssm_phase3_value_score_chain.py`, `docs/plans/reviewed-target.md`, `docs/plans/artifacts/nonlinear-ssm-jit-hmc-phase-3-export-delta-2026-06-08.md`, this result note |
| Tests | py_compile with `/tmp` pycache, Phase 3 value/score pytest, common runtime contracts, Phase 1 contract, Phase 2 value paths |
| Random seeds | N/A |
| Serious experiment | not run |
| GPU experiment | not run |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Submit Phase 3 for Claude review | Passed for target-only scalar and static-chain CPU XLA value/score parity on the Model B fixture | Unreviewed XLA authority rejected; target-scope mismatch rejected; chain order preserved; rank/static-shape requirements enforced; MAP/mass and whitening guards passed; CPU-only GPU hidden | Only tiny target fixtures and static chain shape were tested; full-chain TFP HMC remains untested | Run Claude read-only Phase 3 review; if accepted, proceed to Phase 4 | No full-chain HMC, no sampler convergence, no posterior validity, no dynamic-shape or GPU claim |

## Inference-Status Table

| Row | Status |
| --- | --- |
| Hard veto screen | Passed for the Phase 3 engineering gates listed above |
| Statistically supported ranking | N/A; no stochastic method comparison or ranking |
| Descriptive-only differences | Warning counts and runtime are descriptive only |
| Default-readiness | Not established |
| Next evidence needed | Phase 4 full-chain TFP HMC JIT runtime canary |

## What Is Not Concluded

- This is not evidence that a full TFP HMC chain compiles.
- This is not evidence of HMC convergence.
- This is not evidence that any DSGE, MacroFinance, NeuTra, or score-matching
  run is ready.
- This is not GPU evidence.
- This is not performance-superiority evidence.

## Post-Run Red-Team Note

The strongest alternative explanation for a Phase 3 pass is that the static
unroll helper is too narrow and avoids the real TFP chain semantics that Phase 4
must confront. The result would be overturned if full-chain TFP HMC cannot use
the reviewed target authority without host callbacks, dynamic-shape leaks, or
target-scope drift. The weakest part of the evidence is that it uses tiny
deterministic fixtures and target-only value/score parity rather than a real
sampler transition.

## Claude Review

Round 1:

- Reviewer: `nonlinear-ssm-visible-phase-3-review-1`.
- Verdict: `VERDICT: REVISE`.
- Material findings:
  - `docs/plans/reviewed-target.md` was referenced by the toy
    `ReviewedTapeAdapter` tests but did not exist.
  - The result note claimed missing static chain/parameter dimension checks,
    but tests only covered successful static shape and non-rank-2 failure.
  - The public export diff in `bayesfilter/__init__.py` was not isolated from
    prior Phase 1R lazy-export replay.
- Claude found no material model-math, filter-equation, sampler, or target
  drift in `static_unroll_chain_value_and_score`.

Round-1 repairs:

- Added `docs/plans/reviewed-target.md` as a toy contract-fixture evidence note
  for the reviewed GradientTape exception tests. It explicitly does not
  authorize real model, nonlinear SSM, DSGE, MacroFinance, NeuTra,
  score-matching, full-chain HMC, GPU, performance, or scientific claims.
- Added explicit unknown chain-dimension and unknown parameter-dimension
  rejection tests in `tests/test_nonlinear_ssm_phase3_value_score_chain.py`.
- Added
  `docs/plans/artifacts/nonlinear-ssm-jit-hmc-phase-3-export-delta-2026-06-08.md`
  to isolate the Phase 3 public export delta from prior accepted Phase 1R
  lazy-export changes.

Status: ready for Claude review round 2 after post-repair focused checks.

Post-repair focused checks:

- `py_compile`: passed.
- Focused pytest: `50 passed, 9943 warnings in 36.51s`.

Status: ready for Claude review round 2.
