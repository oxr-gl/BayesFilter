# Actual-SIR Low-Rank N1024 Paired Validation Result

Date: 2026-06-23

Status: `N1024_PAIRED_VALIDATION_FIVE_CANDIDATES_REMAIN_VIABLE`

## Phase Objective

Run a staged paired GPU/XLA actual-SIR validation screen at `N=1024` for the
five candidates that survived heldout, first `N=512`, and independent `N=512`
seed-replication screens.

## Evidence Contract Result

- Question: do the five `N=512` seed-replication survivors remain viable at
  `N=1024` under the same compiled GPU/XLA actual-SIR paired screen?
- Baseline/comparator: paired streaming actual-SIR route rows from the same
  harness, seed batch, shape, dtype, TF32 mode, GPU visibility, and
  compiled-core timing contract.
- Primary screen: no hard vetoes, complete GPU/XLA compiled-core provenance,
  paired comparability pass, warm-time screen pass, and preserved per-row
  JSON/Markdown/log artifact paths.
- Result: `5/5` exact survivor candidates were labeled `freeze-nominated` at
  `N=1024`.
- Candidate rejection: no candidate was rejected at this gate.
- Research direction: this result supports continued staged validation of the
  repaired low-rank route at `N=1024`, but it is still not a statistical
  ranking, speedup claim, posterior-correctness claim, or default-readiness
  claim.

## Checks And Runs

- Syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- Focused tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `17 passed` before execution under the reviewed subplan.
- Exact candidate dry-run:
  `python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode dry-run ... --candidate-ids <five survivor ids> --output /tmp/actual-sir-low-rank-n1024-paired-validation-exact-candidate-dry-run.json --markdown-output /tmp/actual-sir-low-rank-n1024-paired-validation-exact-candidate-dry-run.md --quiet`
  - Result: pass before execution under the reviewed subplan.
- Trusted GPU precheck:
  `nvidia-smi --query-gpu=index,name,uuid,memory.used,utilization.gpu --format=csv,noheader,nounits`
  - Result before execution: GPU 1 was visible and used for the run:
    NVIDIA GeForce RTX 4080 SUPER, UUID
    `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`.
- Trusted GPU N1024 paired-validation execution:
  `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode execute --route both --batch-seeds 81129,81130 --time-steps 20 --num-particles 1024 --low-rank-ranks 16,32,64,128 --low-rank-assignment-epsilons 0.25,0.125 --low-rank-max-projection-iterations-list 120 --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120,r32_eps0p25_alpha1em08_it120,r64_eps0p25_alpha1em08_it120,r128_eps0p25_alpha1em08_it120 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --jit-compile --row-timeout-seconds 3600 --output docs/benchmarks/actual-sir-low-rank-n1024-paired-validation-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-low-rank-n1024-paired-validation-2026-06-23.md`
  - Result: pass, aggregate status `PASS`, wall time
    `2271.9520021050703` seconds.
- Aggregate consistency check:
  - Result: pass for aggregate status, exact candidate ids, row statuses, hard
    vetoes, paired comparability, warm-screen support, GPU/TF32 provenance,
    low-rank provenance, and row JSON/Markdown/log artifact paths.

## N1024 Paired-Validation Summary

Execution shape and policy:

- Seeds: `[81129, 81130]`
- Shape: batch `2`, time steps `20`, particles `1024`, state dimension `18`,
  observation dimension `9`
- Execution: `float32`, TF32 enabled, `CUDA_VISIBLE_DEVICES=1`, requested
  `/GPU:0`, expected GPU outputs, `jit_compile=true`
- Timing: streaming and low-rank timing source `compiled_core`
- Aggregate labels: `5` `freeze-nominated`

| Candidate | Label | Hard vetoes | Paired comparable | Warm screen | Warm median streaming/low-rank | Log-likelihood max abs delta | Log-likelihood mean abs delta | Row wall time seconds |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | 4.331733 | 0.302246 | 0.20752 | 464.762864 |
| `r16_eps0p125_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | 4.365650 | 1.952148 | 1.73074 | 457.445307 |
| `r32_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | 4.255293 | 0.192749 | 0.157288 | 462.766333 |
| `r64_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | 4.697958 | 0.305542 | 0.287689 | 451.059117 |
| `r128_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | 4.390261 | 0.270325 | 0.174164 | 435.859869 |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance all five candidates to an independent `N=1024` seed-replication screen | Passed for `5/5` exact survivor candidates at `N=1024` | No row hard vetoes; all rows had paired comparability, warm-time support, GPU/XLA provenance, and row artifact paths | One `N=1024` seed batch; no uncertainty model or enough replications for ranking | Draft and review an `N=1024` seed-replication subplan for these five candidates | No posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, speedup claim, scientific superiority, production scientific validity, or statistical ranking |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for all five N1024 paired-validation rows; hard vetoes were `[]` |
| Paired comparability | Passed for all five candidates |
| Statistically supported ranking | Not established; observed warm ratios and row times are descriptive only |
| Descriptive-only differences | Warm median ratios, row wall times, residual magnitudes, and exact deltas are descriptive screen diagnostics |
| Default-readiness | Not established; this is not a public API/default promotion gate |
| Next evidence needed | Independent `N=1024` seed replication with exact candidate ids and no ranking from descriptive timing alone |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Working tree | Dirty before and during the run; unrelated user/generated changes preserved |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` |
| Platform | `Linux-6.8.0-111-generic-x86_64-with-glibc2.35` |
| GPU | NVIDIA GeForce RTX 4080 SUPER, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| Started | `2026-06-22T20:35:06.245628+00:00` |
| Ended | `2026-06-22T21:12:58.161397+00:00` |
| Wall time | `2271.9520021050703` seconds |
| Seeds | `81129,81130` |
| Shape | batch `2`, time steps `20`, particles `1024`, state dimension `18`, observation dimension `9` |
| Execution policy | `float32`, TF32 enabled, GPU visible, `jit_compile=true`, `compiled_core` timing |
| Plan | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n1024-paired-validation-subplan-2026-06-23.md` |
| Aggregate JSON | `docs/benchmarks/actual-sir-low-rank-n1024-paired-validation-2026-06-23.json` |
| Aggregate Markdown | `docs/benchmarks/actual-sir-low-rank-n1024-paired-validation-2026-06-23.md` |
| Result artifact | This file |

## Post-Run Red-Team Note

- Strongest alternative explanation: all five candidates may be viable for the
  first `N=1024` seed batch but fail on an independent seed batch, especially
  through runtime, paired-comparability, or numerical diagnostics.
- What would overturn advancement: an independent `N=1024` seed-replication
  screen showing hard vetoes, missing GPU/XLA provenance, failed paired
  comparability, missing row artifacts, warm-screen failure, or timeout under
  the predeclared contract.
- Weakest part of the evidence: the result is still a viability screen with one
  `N=1024` seed batch; it does not support ranking among the five candidates.

## Next-Phase Handoff

Advance these five candidates to an independent `N=1024` seed-replication
subplan:

- `r16_eps0p25_alpha1em08_it120`
- `r16_eps0p125_alpha1em08_it120`
- `r32_eps0p25_alpha1em08_it120`
- `r64_eps0p25_alpha1em08_it120`
- `r128_eps0p25_alpha1em08_it120`

Do not revive `r64_eps0p125_alpha1em08_it120` without a new repair/tuning
subplan, because it failed heldout paired comparability.

## Forbidden Claims Preserved

This result is an `N=1024` paired-validation viability screen only. It does not
claim speedup, posterior correctness, HMC readiness, dense Sinkhorn equivalence,
public API/default readiness, broad scalable-OT superiority, statistical
ranking, or production scientific validity. It also does not authorize NumPy as
BayesFilter-owned algorithmic implementation; the production route remains the
GPU/XLA TensorFlow/TFP lane.
