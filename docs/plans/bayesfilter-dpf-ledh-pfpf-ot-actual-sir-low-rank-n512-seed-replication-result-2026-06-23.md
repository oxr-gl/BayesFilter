# Actual-SIR Low-Rank N512 Seed-Replication Result

Date: 2026-06-23

Status: `N512_SEED_REPLICATION_FIVE_CANDIDATES_REMAIN_VIABLE`

## Phase Objective

Run an independent same-particle `N=512` seed-batch replication over the five
larger-particle viable low-rank candidates, to test whether the larger-particle
viability screen survives another seed batch without using descriptive timing as
ranking evidence.

## Evidence Contract Result

- Question: do the five `N=512` larger-particle survivors remain viable on an
  independent `N=512` seed batch under the same compiled GPU/XLA actual-SIR
  screen?
- Baseline/comparator: paired streaming actual-SIR route rows from the same
  harness, seeds, shape, dtype, TF32 mode, GPU visibility, and compiled-core
  timing contract.
- Primary screen: no hard vetoes, complete GPU/XLA compiled-core provenance,
  paired comparability pass, warm-time screen pass, and preserved per-row
  JSON/Markdown/log artifact paths.
- Result: `5/5` exact survivor candidates were labeled `freeze-nominated` on
  the independent `N=512` seed batch.
- Candidate rejection: no candidate was rejected at this gate.
- Research direction: this result supports continued staged validation of the
  repaired low-rank route, but it is still not a statistical ranking or default
  readiness claim.

## Checks And Runs

- Syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- Focused tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `17 passed`.
- Exact candidate dry-run:
  `python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode dry-run ... --candidate-ids <five survivor ids> --output /tmp/actual-sir-low-rank-n512-seed-replication-exact-candidate-dry-run.json --markdown-output /tmp/actual-sir-low-rank-n512-seed-replication-exact-candidate-dry-run.md --quiet`
  - Result: pass.
- Trusted GPU precheck:
  `nvidia-smi --query-gpu=index,name,uuid,memory.used,utilization.gpu --format=csv,noheader,nounits`
  - Initial result: GPU 1 had the expected UUID but was temporarily occupied by
    an unrelated Nystrom diagnostic process. Execution waited rather than
    stealing the GPU or silently changing devices.
  - Final pre-run result: GPU 1 was free, NVIDIA GeForce RTX 4080 SUPER, UUID
    `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`, `18` MiB used, `0%`
    utilization.
- Trusted GPU N512 seed-replication execution:
  `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode execute --route both --batch-seeds 81126,81127,81128 --time-steps 20 --num-particles 512 --low-rank-ranks 16,32,64,128 --low-rank-assignment-epsilons 0.25,0.125 --low-rank-max-projection-iterations-list 120 --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120,r32_eps0p25_alpha1em08_it120,r64_eps0p25_alpha1em08_it120,r128_eps0p25_alpha1em08_it120 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --jit-compile --row-timeout-seconds 2400 --output docs/benchmarks/actual-sir-low-rank-n512-seed-replication-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-low-rank-n512-seed-replication-2026-06-23.md`
  - Result: pass, aggregate status `PASS`, wall time
    `2282.9774378379807` seconds.
- Aggregate consistency check:
  - Result: pass, `n512-seed-replication-aggregate-consistency-pass`.

## N512 Seed-Replication Summary

Execution shape and policy:

- Seeds: `[81126, 81127, 81128]`
- Shape: batch `3`, time steps `20`, particles `512`, state dimension `18`,
  observation dimension `9`
- Execution: `float32`, TF32 enabled, `CUDA_VISIBLE_DEVICES=1`, requested
  `/GPU:0`, expected GPU outputs, `jit_compile=true`
- Timing: streaming and low-rank timing source `compiled_core`
- Aggregate labels: `5` `freeze-nominated`

| Candidate | Label | Hard vetoes | Paired comparable | Warm screen | Warm median streaming/low-rank | Log-likelihood max abs delta | Log-likelihood mean abs delta | Row wall time seconds |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `2.886379191912811` | `0.42852783203125` | `0.3413899739583333` | `458.9466289130505` |
| `r16_eps0p125_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `2.9479213090923313` | `1.266357421875` | `0.8516031901041666` | `460.7499922371935` |
| `r32_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `2.462814632372316` | `0.51788330078125` | `0.3531494140625` | `455.51635225699283` |
| `r64_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `2.863995979190796` | `0.49481201171875` | `0.2730916341145833` | `456.00933637982234` |
| `r128_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `2.5931231270912` | `0.2108154296875` | `0.16953531901041666` | `451.6773744809907` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance all five candidates to a staged `N=1024` paired validation screen | Passed for `5/5` exact survivor candidates on independent `N=512` seeds | No row hard vetoes; all rows had paired comparability, warm-time support, GPU/XLA provenance, and row artifact paths | Two `N=512` batches still do not establish statistical ranking; `N=1024` may expose runtime, comparability, or memory failures | Draft and review a staged `N=1024` paired validation subplan for these five candidates | No posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, speedup claim, scientific superiority, or statistical ranking |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for all five independent N512 rows; hard vetoes were `[]` |
| Paired comparability | Passed for all five candidates |
| Statistically supported ranking | Not established; observed warm ratios and row times are descriptive only |
| Descriptive-only differences | Warm median ratios, row wall times, residual magnitudes, and exact deltas are descriptive screen diagnostics |
| Default-readiness | Not established; this is not a public API/default promotion gate |
| Next evidence needed | Staged `N=1024` paired validation with exact candidate ids and no ranking from descriptive timing alone |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Working tree | Dirty before and during the run; unrelated user/generated changes preserved |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` |
| Platform | `Linux-6.8.0-111-generic-x86_64-with-glibc2.35` |
| GPU | NVIDIA GeForce RTX 4080 SUPER, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| Started | `2026-06-22T19:47:56.448763+00:00` |
| Ended | `2026-06-22T20:25:59.378858+00:00` |
| Wall time | `2282.9774378379807` seconds |
| Seeds | `81126,81127,81128` |
| Shape | batch `3`, time steps `20`, particles `512`, state dimension `18`, observation dimension `9` |
| Execution policy | `float32`, TF32 enabled, GPU visible, `jit_compile=true`, `compiled_core` timing |
| Plan | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n512-seed-replication-subplan-2026-06-23.md` |
| Aggregate JSON | `docs/benchmarks/actual-sir-low-rank-n512-seed-replication-2026-06-23.json` |
| Aggregate Markdown | `docs/benchmarks/actual-sir-low-rank-n512-seed-replication-2026-06-23.md` |
| Result artifact | This file |

## Post-Run Red-Team Note

- Strongest alternative explanation: all five candidates may be viable at
  `N=512` but fail at `N=1024` due to runtime, memory, comparability, or
  numerical behavior not exercised by the current particle count.
- What would overturn advancement: a staged `N=1024` screen showing hard
  vetoes, missing GPU/XLA provenance, failed paired comparability, missing row
  artifacts, warm-screen failure, or timeout under the predeclared contract.
- Weakest part of the evidence: even two `N=512` screens are descriptive
  viability evidence, not a ranking or production/default-readiness proof.

## Next-Phase Handoff

Advance these five candidates to a staged `N=1024` paired validation subplan:

- `r16_eps0p25_alpha1em08_it120`
- `r16_eps0p125_alpha1em08_it120`
- `r32_eps0p25_alpha1em08_it120`
- `r64_eps0p25_alpha1em08_it120`
- `r128_eps0p25_alpha1em08_it120`

Do not revive `r64_eps0p125_alpha1em08_it120` without a new repair/tuning
subplan, because it failed heldout paired comparability.

## Forbidden Claims Preserved

This result is a seed-replication viability screen only. It does not claim
speedup, posterior correctness, HMC readiness, dense Sinkhorn equivalence,
public API/default readiness, broad scalable-OT superiority, statistical
ranking, or production scientific validity. It also does not authorize NumPy as
BayesFilter-owned algorithmic implementation; the production route remains the
GPU/XLA TensorFlow/TFP lane.
