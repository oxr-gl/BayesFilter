# P91 Phase 7 Result: HMC GPU/XLA Smoke

Date: 2026-06-29

Status: `PASS_P91_PHASE7_HMC_SMOKE_PENDING_REVIEW`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 7 passes as a narrow implementation smoke for the local complete-data Zhao-Cui SIR d18 target under trusted GPU/XLA TFP HMC. |
| Primary criterion status | Passed after harness repair: compiled HMC returned finite samples, target values, per-sample scalar gradients, and log-accept ratios on GPU output devices, with no post-warmup retrace. |
| Veto diagnostic status | Passed: trusted GPU evidence was used; XLA compiled; TensorFlow saw `/physical_device:GPU:0`; output tensors were on `/GPU:0`; no OOM, retry, NaN/Inf, or retrace veto remains. |
| Main uncertainty | This is a tiny local complete-data HMC implementation smoke. It does not establish posterior correctness, convergence, full observed-data/filtering HMC readiness, exact likelihood correctness, or production readiness. |
| Next justified action | Review this Phase 7 result and the refreshed Phase 8 packaging/release subplan. |
| What is not being concluded | No posterior correctness, no convergence claim, no exact likelihood correctness, no full observed-data/filtering HMC target readiness, no package/default readiness, and no production readiness. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the local complete-data Zhao-Cui SIR d18 target component survive a tiny trusted GPU/XLA TFP HMC implementation smoke? |
| Baseline/comparator | Phase 5 GPU/XLA local target capability and Phase 6 model-specific CPU/GPU/batched execution evidence. |
| Primary criterion | Passed for the deterministic local complete-data fixture and reviewed sampler settings. |
| Veto diagnostics | Passed after repairing the smoke harness gradient diagnostic; no runtime veto remains in the final manifest. |
| Explanatory diagnostics | Acceptance rate, first-call compile-plus-run time, second-call time, sample mean/standard deviation, trace counts, TensorFlow/TFP versions, and device metadata. |
| Not concluded | No posterior correctness, convergence, exact likelihood correctness, full observed-data/filtering target readiness, package/default readiness, or production readiness. |
| Artifact | HMC smoke manifest, this result, and refreshed Phase 8 subplan. |

## What Initially Failed

The first trusted GPU/XLA run compiled and executed the HMC smoke, but returned:

```text
BLOCK_P91_PHASE7_HMC_SMOKE
veto_reasons = ["sample gradients nonfinite"]
```

The failure was not a target-value, HMC-kernel, GPU-device, XLA, OOM, retry, or
retrace failure. The manifest showed finite samples, finite target values,
finite log-accept ratios, GPU output devices, and stable trace counts.

Focused diagnosis showed the post-sample gradient diagnostic was using the
batched/vectorized target wrapper inside a single gradient tape. That wrapper
returned finite values but a disconnected gradient in this TensorFlow context.
The scalar local complete-data target returned finite gradients at the same
theta points when evaluated one point at a time, matching the Phase 5 validated
scalar score path.

Repair applied:

- `scripts/p91_hmc_smoke.py` now keeps the HMC target unchanged;
- post-sample diagnostics compute scalar value/gradient pairs per sampled theta
  using `tf.map_fn`;
- the smoke still fails closed if any sampled scalar gradient is nonfinite.

## Local Checks

Commands:

```bash
git diff --check -- scripts/p91_hmc_smoke.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p91_hmc_smoke.py
```

Outcome:

- `git diff --check`: passed before and after the harness repair.
- Harness compile check: passed before and after the harness repair.
- CPU-only compile check intentionally set `CUDA_VISIBLE_DEVICES=-1`.

## Trusted GPU/XLA Commands

Commands:

```bash
nvidia-smi
python scripts/p91_hmc_smoke.py --manifest docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-2026-06-29.json --chains 2 --num-results 8 --num-burnin-steps 4 --step-size 1e-4 --num-leapfrog-steps 3 --seed 9107 --xla true
```

`nvidia-smi` outcome:

- Trusted command passed.
- Driver `591.86`, CUDA `13.1` reported by `nvidia-smi`.
- GPU reported as NVIDIA GeForce RTX 4080-class device with 16376 MiB memory.

Final HMC smoke outcome:

- Trusted command passed with status `PASS_P91_PHASE7_HMC_SMOKE`.
- TensorFlow version `2.19.1`.
- TensorFlow Probability version `0.25.0`.
- TensorFlow saw physical GPU `/physical_device:GPU:0` and logical GPU
  `/device:GPU:0`.
- GPU name: NVIDIA GeForce RTX 4080 SUPER.
- TensorFlow logs recorded XLA CUDA service initialization and one compiled
  XLA cluster.

## Manifest Summary

Manifest:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-2026-06-29.json`

Manifest status:

```text
PASS_P91_PHASE7_HMC_SMOKE
```

Key fields:

- initial target value: `-227.76731057912758`;
- initial gradient: `[15.804320716438662, 0.6904322032950861, -44.9925]`;
- sample finite: `true`;
- target values finite: `true`;
- sample gradients finite: `true`;
- log-accept ratios finite: `true`;
- acceptance rate: `1.0`;
- output devices: all recorded tensors on `/GPU:0`;
- first call seconds: `8.222991356044076`;
- second identical call seconds: `0.1347640580497682`;
- trace counts: `0 -> 1 -> 1`;
- post-warmup retrace detected: `false`;
- OOM status: `false`;
- retry count: `0`;
- native divergence status: `unavailable` because the TFP trace did not expose
  a native boolean divergence field for this harness.

## Blockers Preserved

The manifest preserves:

- `full_observed_data_filtering_score_identity = NOT_CLAIMED`;
- `BLOCK_FIXED_TTSIRT_PREVIOUS_MARGINAL_DERIVATIVE_NOT_IMPLEMENTED`;
- `BLOCK_FIXED_TTSIRT_PROPOSAL_TRANSPORT_DERIVATIVE_NOT_IMPLEMENTED`;
- `BLOCK_FULL_SOURCE_ROUTE_FD_NOT_CLAIMED`.

Phase 3 remains owner-accepted for continuation with caveats, not a full FD
pass.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Worktree status | Dirty research worktree; unrelated dirty changes preserved. |
| Python executable | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` |
| Conda environment | `tf-gpu` |
| Execution target | Trusted GPU/XLA local complete-data HMC smoke. |
| CPU/GPU status | CPU-only py_compile hid GPU intentionally; HMC smoke used trusted/escalated GPU execution. |
| Commands | `git diff --check -- scripts/p91_hmc_smoke.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md`; `CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p91_hmc_smoke.py`; `nvidia-smi`; `python scripts/p91_hmc_smoke.py --manifest docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-2026-06-29.json --chains 2 --num-results 8 --num-burnin-steps 4 --step-size 1e-4 --num-leapfrog-steps 3 --seed 9107 --xla true` |
| Data version | `N/A`; deterministic local complete-data fixture. |
| Random seeds | `9107` for the TFP HMC smoke. |
| Wall time | Final HMC smoke shell-reported elapsed time was approximately `16.70s`; manifest first/second call timings are recorded separately. |
| Phase 7 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-subplan-2026-06-29.md` |
| Exact-command refresh | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-exact-command-refresh-2026-06-29.md` |
| Manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-2026-06-29.json` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-result-2026-06-29.md` |
| Refreshed Phase 8 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase8-packaging-release-subplan-2026-06-29.md` |

## Phase 8 Handoff

Phase 8 may proceed only after Claude review agrees on this Phase 7 result and
the refreshed Phase 8 subplan. Phase 8 must preserve that Phase 7 is only a
tiny local complete-data HMC implementation smoke and not posterior,
convergence, exact-likelihood, full filtering-target, release, default-policy,
or production evidence by itself.
