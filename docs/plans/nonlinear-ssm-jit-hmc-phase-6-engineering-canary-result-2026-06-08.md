# Nonlinear SSM JIT/HMC Phase 6 Engineering Canary Result

Date: 2026-06-08

Owning root: `/home/ubuntu/python/BayesFilter`

Supervisor runbook:

- `/home/ubuntu/python/dsge_hmc/docs/plans/BayesFilterDSGE/nonlinear-ssm-jit-hmc-visible-phases-2-9-runbook-2026-06-08.md`

Phase subplan:

- `/home/ubuntu/python/dsge_hmc/docs/plans/BayesFilterDSGE/nonlinear-ssm-jit-hmc-phase-6-bayesfilter-engineering-canary-subplan-2026-06-07.md`

Artifact root:

- `docs/plans/artifacts/nonlinear-ssm-jit-hmc-phase-6-canary-2026-06-08`

## Status

`PHASE_6_READY_FOR_CLAUDE_REVIEW`

## Skeptical Audit

Status: passed for a bounded CPU-only BayesFilter engineering canary.

- Wrong baseline: this is a toy BayesFilter integration canary, not a DSGE,
  MacroFinance, NeuTra, score-matching, real-model, or posterior baseline.
- Proxy metrics: finite values, finite tiny-chain samples, acceptance, and
  timing are engineering diagnostics only.
- Missing stop conditions: the canary fails on missing artifacts, stale reducer
  status, nonfinite value/score/sample, hidden GPU drift, wrong authority
  metadata, or required serious/model-specific budgets.
- Unfair comparison: no method comparison, performance comparison, or sampler
  ranking is made.
- Hidden assumptions: CPU-only hiding is set before TensorFlow import. The GPU
  path is out of scope; no trusted GPU preflight or GPU canary was run.
- Stale context: Phases 1R-5 were accepted before this phase. Phase 6 does not
  reinterpret any earlier tiny-chain evidence as sampler validity.
- Environment mismatch: all commands set `CUDA_VISIBLE_DEVICES=-1`. TensorFlow
  printed CUDA diagnostics saying GPUs were hidden; artifact metadata records
  `tensorflow_visible_gpus=[]`.
- Artifact adequacy: the durable canary writes manifest, stage events,
  heartbeats, partial snapshot, worker result, reducer status, and summary.

Reason to proceed: the implementation adds a script-level BayesFilter-only
canary and focused test. It does not alter model equations, filtering
equations, HMC transition math, target definitions, priors, training
objectives, or evidence criteria.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the consolidated BayesFilter stack run end to end on a toy fixture with complete reducer-readable artifacts? |
| Baseline | Accepted Phase 1R-5 components and result notes. |
| Primary criterion | CPU-only toy canary returns complete non-stale artifacts with accepted authority metadata, full-chain JIT evidence, finite engineering diagnostics, heartbeat/partial/result artifacts, exact stale matching, and reducer status. |
| Vetoes | Missing artifact fields; nonfinite value/score/sample; stale artifact; hidden GPU drift; wrong authority metadata; tiny-chain metrics overinterpreted; need for serious/model-specific budgets. |
| Explanatory only | Runtime, acceptance, tiny trace metrics, timing buckets, warning counts, and artifact file count. |
| Not concluded | No sampler convergence, posterior validity, real-NK readiness, DSGE readiness, MacroFinance readiness, GPU readiness, production robustness, performance superiority, or scientific result. |
| Artifact | This result note plus `docs/plans/artifacts/nonlinear-ssm-jit-hmc-phase-6-canary-2026-06-08`. |

## Implementation Summary

Added:

- `scripts/run_nonlinear_ssm_phase6_engineering_canary.py`;
- `tests/test_nonlinear_ssm_phase6_engineering_canary.py`.

The canary exercises:

- Phase 2-style fixed-shape compiled nonlinear value path using
  `tf_svd_cut4_filter` on Model B observations;
- Phase 3-style reviewed graph-native value/score authority using
  `ModelBNonlinearSVDTarget.default()`;
- Phase 3-style static chain-batched value/score;
- Phase 4 full-chain exact `tfp.mcmc.sample_chain` wrapper with
  `FullChainHMCConfig`;
- Phase 5 runner artifacts: manifest, stage events, heartbeats, partial
  snapshot, worker result, reducer status, stale-match payload, and timing
  buckets.

Repair during execution:

- Initial test failed because running the script by file path set `sys.path` to
  `scripts/` and made `bayesfilter` unavailable. The script now inserts the
  repository root on `sys.path` before local imports.
- Second test failed because the canary wrapped `tf_svd_cut4_filter` directly
  in `tf.function` and returned a dataclass object. The canary now follows the
  Phase 2 pattern by returning tensor fields from the compiled function. No
  production filter code or math was changed.

## Canary Fixture And Budget

| Field | Value |
| --- | --- |
| Fixture | `ModelBNonlinearSVDTarget.default()` |
| Value backend | `tf_svd_cut4` |
| Observation shape | `[3, 1]` |
| State dimension | `2` |
| Parameter dimension | `3` |
| Value/score authority | `graph_native` |
| Target scope | `phase6_model_b_nonlinear_canary` |
| HMC runtime | `tfp.mcmc.sample_chain` |
| JIT | `true` |
| Adaptation policy | `fixed_kernel_no_adaptation` |
| `num_results` | `2` |
| `num_burnin_steps` | `1` |
| `step_size` | `0.0005` |
| `num_leapfrog_steps` | `1` |
| Seed | `[20260608, 6]` |
| Serious budget | no |

## Durable Canary Artifacts

Artifact files:

- `worker_manifest.json`;
- `stage_events.jsonl`;
- `partial_snapshot.json`;
- `worker_result.json`;
- `reducer_status.json`;
- `summary.json`.

Key artifact values:

| Field | Value |
| --- | --- |
| Reducer status | `complete` |
| Reducer reason | `complete_result_present` |
| Worker return code | `0` |
| Stale | `false` |
| `CUDA_VISIBLE_DEVICES` | `-1` |
| TensorFlow visible GPUs | `[]` |
| Value log likelihood | `-1.5372792647414193` |
| Value path floor count | `0.0` |
| Value path PSD projection residual | `0.0` |
| Value/score nonfinite count | `0` |
| HMC sample shape | `[2, 3]` |
| HMC finite sample count | `2` |
| HMC nonfinite sample count | `0` |
| HMC acceptance | `1.0` |
| Divergence status | `unavailable` |
| Worker runtime | `15.34570554702077` seconds |

Stage events:

- `start`;
- heartbeat `compiled_value`;
- heartbeat `chain_value_score`;
- heartbeat `full_chain_hmc`;
- `complete`.

Timing buckets:

- filter: `2.020028869039379` seconds;
- value_score: `6.9601049199700356` seconds;
- hmc_kernel: `6.21307937905658` seconds;
- artifact_overhead: `0.0` seconds.

All timing buckets are marked `explanatory_only` and include the nonclaim that
timing is not a validity or promotion criterion.

## Commands And Results

Commands run:

```text
PYTHONPYCACHEPREFIX=/tmp/bayesfilter_phase6_pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m py_compile scripts/run_nonlinear_ssm_phase6_engineering_canary.py tests/test_nonlinear_ssm_phase6_engineering_canary.py
```

Result:

- exit code `0`.

Commands run:

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_nonlinear_ssm_phase6_engineering_canary.py
```

Result:

- first run failed on script import path;
- second run failed on returning a dataclass from a compiled TensorFlow
  function;
- post-repair run: `1 passed in 18.72s`.

Commands run:

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_nonlinear_ssm_phase6_engineering_canary.py tests/test_nonlinear_ssm_phase5_runner_device_performance.py tests/test_nonlinear_ssm_phase4_full_chain_hmc.py tests/test_nonlinear_ssm_phase3_value_score_chain.py tests/test_common_inference_runtime_contracts.py tests/test_nonlinear_ssm_phase2_value_paths.py tests/test_nonlinear_ssm_phase1_contract.py tests/test_v1_public_api.py
```

Result:

- `68 passed, 9987 warnings in 57.04s`.

Commands run:

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python scripts/run_nonlinear_ssm_phase6_engineering_canary.py --artifact-root docs/plans/artifacts/nonlinear-ssm-jit-hmc-phase-6-canary-2026-06-08 --num-results 2 --num-burnin-steps 1 --step-size 0.0005 --num-leapfrog-steps 1 --force
```

Result:

- exit code `0`;
- wrote durable artifact root listed above.

TensorFlow warnings/logs:

- CPU feature log;
- CUDA diagnostic log confirming `CUDA_VISIBLE_DEVICES="-1"` hides GPUs;
- Host XLA compile log;
- XLA assert-operator warnings.

These are recorded as engineering logs, not GPU evidence or sampler evidence.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `3dac444c22e8a366063f0fa0a73788cc9db96201` |
| Dirty worktree | `true` |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` |
| CPU/GPU status | CPU-only |
| GPU intentionally hidden | yes, `CUDA_VISIBLE_DEVICES=-1` |
| Framework visible GPUs | `[]` |
| Hardware probe | not run |
| Phase 6 write set | `scripts/run_nonlinear_ssm_phase6_engineering_canary.py`, `tests/test_nonlinear_ssm_phase6_engineering_canary.py`, durable artifact root, this result note |
| Pre-existing dirty work | yes; BayesFilter already had Phase 1R-5 and unrelated dirty/untracked files before Phase 6 |
| Serious experiment | not run |
| GPU experiment | not run |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Submit Phase 6 for Claude review | Passed for bounded CPU-only BayesFilter engineering canary with complete artifacts | Reducer complete; stale false; CPU-hidden GPUs `[]`; value/score/sample nonfinite counts zero; authority metadata accepted; tiny metrics not promoted | Tiny two-draw HMC and synthetic artifact path do not prove serious-run robustness or sampler validity | Run Claude read-only Phase 6 review; if accepted, proceed to DSGE Phase 7 adapter equivalence | No sampler convergence, posterior validity, DSGE readiness, GPU readiness, production robustness, performance superiority, or scientific result |

## Inference-Status Table

| Row | Status |
| --- | --- |
| Hard veto screen | Passed for Phase 6 engineering gates listed above |
| Statistically supported ranking | N/A; no stochastic method comparison or ranking |
| Descriptive-only differences | Acceptance `1.0`, timing buckets, and runtime are descriptive engineering diagnostics only |
| Default-readiness | Not established |
| Next evidence needed | Phase 7 DSGE adapter equivalence |

## What Is Not Concluded

- This is not HMC convergence evidence.
- This is not posterior validity evidence.
- This is not real-NK or DSGE readiness.
- This is not GPU evidence.
- This is not production robust-runner proof under all failure modes.
- This is not performance superiority evidence.
- This does not change sampler or filtering defaults.

## Post-Run Red-Team Note

The strongest alternative explanation for the Phase 6 pass is that the toy
fixture and two-draw budget are too small to expose serious-run performance,
memory, adaptation, or diagnostic failures. The result would be overturned for
engineering-integration purposes if a future DSGE adapter cannot produce the
same manifest/stale/reducer artifacts without model-specific runner forks. The
weakest part of the evidence is that Phase 6 exercises a real subprocess and
durable artifacts, but not a killed-process or timeout recovery path in a heavy
workload.

## Claude Review

Pending.
