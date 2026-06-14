# Nonlinear SSM JIT/HMC Phase 5 Runner/Device/Performance Result

Date: 2026-06-08

Owning root: `/home/ubuntu/python/BayesFilter`

Supervisor runbook:

- `/home/ubuntu/python/dsge_hmc/docs/plans/BayesFilterDSGE/nonlinear-ssm-jit-hmc-visible-phases-2-9-runbook-2026-06-08.md`

Phase subplan:

- `/home/ubuntu/python/dsge_hmc/docs/plans/BayesFilterDSGE/nonlinear-ssm-jit-hmc-phase-5-robust-runner-device-performance-subplan-2026-06-07.md`

## Status

`PHASE_5_READY_FOR_CLAUDE_REVIEW`

## Skeptical Audit

Status: passed for the narrow Phase 5 implementation.

- Wrong baseline: this phase adds common robust-runner primitives only. It is
  not a NeuTra, score-matching, DSGE, MacroFinance, posterior, or sampler
  baseline run.
- Proxy metrics: heartbeat records, reducer statuses, timeout records, and
  timing buckets are engineering diagnostics only.
- Missing stop conditions: focused tests fail on stale-artifact acceptance,
  missing worker/partial evidence, CPU-only pre-import policy drift, untrusted
  GPU fallback, timing bucket misuse, or candidate ordering/tie drift.
- Unfair comparison: no method ranking, speed ranking, sampler ranking, or
  scientific comparison is made.
- Hidden assumptions: normalized config, program signature, device policy,
  thread caps, and worker config hash all participate in exact stale matching.
- Stale context: Phase 4 was accepted by Claude review round 2 before this
  phase. This phase does not reinterpret Phase 4 HMC canary metrics.
- Environment mismatch: tests are CPU-only with `CUDA_VISIBLE_DEVICES=-1`.
  GPU selection is exercised only with synthetic trusted/untrusted metadata and
  does not probe hardware.
- Artifact adequacy: worker manifest, heartbeat/stage JSONL, partial snapshots,
  timeout records, worker records, reducer statuses, and timing buckets are
  independently writable artifacts suitable for postmortem inspection.

Reason to proceed: the implementation is confined to runner/device/performance
metadata plumbing and tests. It does not alter model equations, filtering
equations, HMC transition math, target definitions, priors, training
objectives, or evidence criteria.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter long workers preserve postmortem evidence, device policy, stale-artifact identity, timeout status, and timing metadata without relying on parent survival? |
| Baseline | Accepted Phase 4 tiny full-chain runtime and existing BayesFilter runtime helper skeletons, with DSGE robust-runner lessons used as reference only. |
| Primary criterion | Focused tests prove worker manifests, heartbeat/stage JSONL, partial artifacts, timeout/return-code records, reducer recovery/statuses, exact stale mismatch rejection including device/thread settings, CPU-only pre-import policy, trusted GPU selection metadata, timing nonclaims, and candidate identity/tie preservation. |
| Vetoes | Parent-only evidence; stale artifacts accepted after program/device/thread/worker drift; TensorFlow/JAX/PyTorch import before CPU-only hiding; untrusted GPU fallback; timing treated as validity; candidate completion-order affecting selection; sampler/model/filter math drift. |
| Explanatory only | Runtime costs, heartbeat intervals, reducer summaries, and timing buckets. |
| Not concluded | No sampler convergence, posterior validity, DSGE readiness, GPU readiness, performance superiority, production robustness for serious runs, or scientific result. |
| Artifact | This result note plus focused Phase 5 tests. |

## Implementation Summary

Extended BayesFilter robust-runner helpers in:

- `bayesfilter/runtime/runner.py`

New or hardened objects:

- `WorkerManifest`;
- `PartialResultSnapshot`;
- `ReducerRowStatus`;
- `TimingBucket`;
- `VALID_REDUCER_STATUSES`;
- `TIMING_BUCKET_NAMES`.

New helpers:

- `build_worker_manifest`;
- `write_worker_manifest`;
- `stale_match_payload`;
- `stale_artifacts_match_exact`;
- `append_stage_event`;
- `append_heartbeat`;
- `write_partial_result_snapshot`;
- `record_timeout`;
- `record_worker_result`;
- `reduce_worker_artifacts`;
- `make_timing_bucket`.

Existing schemas were hardened:

- `RunManifest` now can record program signature, device policy, thread caps,
  and worker config hash;
- `WorkerRecord` now can record PID, status, device policy, thread caps, and
  worker config hash.

Additive exports were added in:

- `bayesfilter/runtime/__init__.py`;
- `bayesfilter/__init__.py`;
- `tests/test_v1_public_api.py`.

Focused Phase 5 tests were added in:

- `tests/test_nonlinear_ssm_phase5_runner_device_performance.py`.

## Schema And Artifact Behavior

Worker manifest exact stale identity includes:

- normalized config;
- program signature;
- device policy;
- thread caps;
- worker config hash.

Worker-side evidence helpers write independently:

- JSON manifest via atomic replace;
- stage-event JSONL;
- heartbeat JSONL entries;
- partial result JSON;
- timeout JSON;
- worker result JSON.

Reducer statuses covered by tests:

- `complete`;
- `partial`;
- `stale`;
- `failed`;
- `timed_out`.

The module also supports `invalid` and `missing` statuses for future callers.

Timing buckets are labeled `explanatory_only` and include a nonclaim that
timing is not a validity or promotion criterion.

## Commands And Results

Commands run:

```text
PYTHONPYCACHEPREFIX=/tmp/bayesfilter_phase5_pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m py_compile bayesfilter/runtime/runner.py bayesfilter/runtime/__init__.py bayesfilter/__init__.py tests/test_nonlinear_ssm_phase5_runner_device_performance.py tests/test_common_inference_runtime_contracts.py tests/test_v1_public_api.py
```

Result:

- exit code `0`.

Commands run:

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_nonlinear_ssm_phase5_runner_device_performance.py tests/test_common_inference_runtime_contracts.py tests/test_v1_public_api.py
```

Result:

- `29 passed, 2 warnings in 2.53s`.

Commands run:

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_nonlinear_ssm_phase5_runner_device_performance.py tests/test_nonlinear_ssm_phase4_full_chain_hmc.py tests/test_nonlinear_ssm_phase3_value_score_chain.py tests/test_common_inference_runtime_contracts.py tests/test_nonlinear_ssm_phase2_value_paths.py tests/test_nonlinear_ssm_phase1_contract.py tests/test_v1_public_api.py
```

Result:

- `67 passed, 9987 warnings in 37.76s`.

Warnings are TensorFlow Probability/GAST deprecations. They are not promotion
evidence or Phase 5 vetoes.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `3dac444c22e8a366063f0fa0a73788cc9db96201` |
| Dirty worktree | `true` |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` |
| CPU/GPU status | CPU-only for tests |
| GPU intentionally hidden | yes, `CUDA_VISIBLE_DEVICES=-1` |
| Hardware probe | not run |
| Synthetic GPU metadata | trusted/untrusted selector fixtures only |
| Phase 5 write set | `bayesfilter/runtime/runner.py`, `bayesfilter/runtime/__init__.py`, `bayesfilter/__init__.py`, `tests/test_nonlinear_ssm_phase5_runner_device_performance.py`, `tests/test_v1_public_api.py`, this result note |
| Pre-existing dirty work | yes; BayesFilter already had Phase 1R-4 and unrelated dirty/untracked files before Phase 5 |
| Serious experiment | not run |
| GPU experiment | not run |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Submit Phase 5 for Claude review | Passed for focused runner/device/performance metadata tests | Stale thread/program drift rejected; heartbeat/partial/timeout/reducer artifacts tested; untrusted GPU fallback rejected; timing nonclaims tested; candidate order/tie tested | Synthetic tests do not prove production serious-run robustness under process crashes or heavy workloads | Run Claude read-only Phase 5 review; if accepted, proceed to Phase 6 | No sampler convergence, posterior validity, DSGE readiness, GPU readiness, performance superiority, or scientific result |

## Inference-Status Table

| Row | Status |
| --- | --- |
| Hard veto screen | Passed for Phase 5 engineering gates listed above |
| Statistically supported ranking | N/A; no stochastic method comparison or ranking |
| Descriptive-only differences | Timing buckets and reducer summaries are descriptive engineering diagnostics only |
| Default-readiness | Not established |
| Next evidence needed | Phase 6 BayesFilter engineering canary |

## What Is Not Concluded

- This is not evidence of HMC convergence.
- This is not evidence of posterior validity.
- This is not evidence of real crash recovery under all production failure
  modes.
- This is not GPU evidence.
- This is not performance-superiority evidence.
- This does not change sampler or filtering defaults.

## Post-Run Red-Team Note

The strongest alternative explanation for a Phase 5 pass is that synthetic
artifact tests do not reproduce every way a long worker can die under a serious
run. The result would be overturned if a real worker can still complete,
timeout, crash, or become stale without leaving enough independent artifacts for
the reducer to classify it. The weakest part of the evidence is that no
separate subprocess failure is exercised yet; that belongs in the Phase 6
engineering canary.

## Claude Review

Pending.
