# Actual-SIR Low-Rank Larger-Particle Replication Result

Date: 2026-06-23

Status: `N512_SCREEN_FIVE_CANDIDATES_REMAIN_VIABLE`

## Phase Objective

Run the smallest larger-particle paired GPU/XLA actual-SIR screen that tests
whether the five heldout-surviving low-rank candidates remain viable when the
particle count increases from `N=256` to `N=512`.

## Evidence Contract Result

- Question: do the five heldout-surviving candidates remain viable when the
  particle count increases from `N=256` to `N=512` under the same compiled
  GPU/XLA actual-SIR screen?
- Baseline/comparator: paired streaming actual-SIR route rows from the same
  harness, seeds, shape, dtype, TF32 mode, GPU visibility, and compiled-core
  timing contract.
- Primary screen: no hard vetoes, complete GPU/XLA compiled-core provenance,
  paired comparability pass, warm-time screen pass, and preserved per-row
  JSON/Markdown/log artifact paths.
- Result: `5/5` exact survivor candidates were labeled `freeze-nominated` at
  `N=512`.
- Candidate rejection: no candidate was rejected at this gate.
- Research direction: this result supports continued validation of the repaired
  low-rank route, but it is still a screen and not a scientific or default
  readiness claim.

## Checks And Runs

- Syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- Focused tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `17 passed`.
- Exact candidate dry-run:
  `python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode dry-run ... --candidate-ids <five survivor ids> --output /tmp/actual-sir-low-rank-larger-particle-exact-candidate-dry-run.json --markdown-output /tmp/actual-sir-low-rank-larger-particle-exact-candidate-dry-run.md --quiet`
  - Result: pass.
- Trusted GPU precheck:
  `nvidia-smi --query-gpu=index,name,uuid,memory.used,utilization.gpu --format=csv,noheader,nounits`
  - Result before execution: GPU 1 was visible and idle enough for the run:
    NVIDIA GeForce RTX 4080 SUPER,
    UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`, `18` MiB used,
    `0%` utilization.
- Trusted GPU larger-particle execution:
  `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode execute --route both --batch-seeds 81124,81125 --time-steps 20 --num-particles 512 --low-rank-ranks 16,32,64,128 --low-rank-assignment-epsilons 0.25,0.125 --low-rank-max-projection-iterations-list 120 --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120,r32_eps0p25_alpha1em08_it120,r64_eps0p25_alpha1em08_it120,r128_eps0p25_alpha1em08_it120 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --jit-compile --row-timeout-seconds 1800 --output docs/benchmarks/actual-sir-low-rank-larger-particle-replication-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-low-rank-larger-particle-replication-2026-06-23.md`
  - Result: pass, aggregate status `PASS`, wall time
    `1989.698265074985` seconds.
- Aggregate consistency check:
  - Result: pass for status, exact candidate ids, row statuses, row hard
    vetoes, provenance flags, labels, and per-row JSON/Markdown/log paths.

## N512 Summary

Execution shape and policy:

- Seeds: `[81124, 81125]`
- Shape: batch `2`, time steps `20`, particles `512`, state dimension `18`,
  observation dimension `9`
- Execution: `float32`, TF32 enabled, `CUDA_VISIBLE_DEVICES=1`, requested
  `/GPU:0`, expected GPU outputs, `jit_compile=true`
- Timing: streaming and low-rank timing source `compiled_core`
- Aggregate labels: `5` `freeze-nominated`

| Candidate | Label | Hard vetoes | Paired comparable | Warm screen | Warm median streaming/low-rank | Log-likelihood max abs delta | Log-likelihood mean abs delta | Row wall time seconds |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `2.9548579695148116` | `0.45111083984375` | `0.416046142578125` | `376.54728348599747` |
| `r16_eps0p125_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `3.0152117645714562` | `1.48187255859375` | `1.089385986328125` | `382.6141426318791` |
| `r32_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `2.8221766374101995` | `0.12750244140625` | `0.103851318359375` | `378.9011974579189` |
| `r64_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `2.708768311134464` | `0.13916015625` | `0.10455322265625` | `401.38394728978164` |
| `r128_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `2.837848487574939` | `0.34063720703125` | `0.1767578125` | `450.18388371914625` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance all five candidates to a same-particle seed-replication screen | Passed for `5/5` exact survivor candidates at `N=512` | No row hard vetoes; all rows had paired comparability, warm-time support, GPU/XLA provenance, and row artifact paths | One `N=512` seed batch; no uncertainty model or enough replications for ranking | Draft and review a seed-replication subplan at `N=512` using only these five candidates | No posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, speedup claim, scientific superiority, or statistical ranking |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for all five larger-particle rows; hard vetoes were `[]` |
| Paired comparability | Passed for all five candidates |
| Statistically supported ranking | Not established; observed warm ratios and row times are descriptive only |
| Descriptive-only differences | Warm median ratios, row wall times, residual magnitudes, and exact deltas are descriptive screen diagnostics |
| Default-readiness | Not established; this is not a public API/default promotion gate |
| Next evidence needed | Same-particle seed replication or staged larger-N validation with predeclared nonclaims and no ranking from descriptive timing alone |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Working tree | Dirty before and during the run; unrelated user/generated changes preserved |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` |
| Platform | `Linux-6.8.0-111-generic-x86_64-with-glibc2.35` |
| GPU | NVIDIA GeForce RTX 4080 SUPER, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| Started | `2026-06-22T18:59:45.017136+00:00` |
| Ended | `2026-06-22T19:32:54.669705+00:00` |
| Wall time | `1989.698265074985` seconds |
| Seeds | `81124,81125` |
| Shape | batch `2`, time steps `20`, particles `512`, state dimension `18`, observation dimension `9` |
| Execution policy | `float32`, TF32 enabled, GPU visible, `jit_compile=true`, `compiled_core` timing |
| Plan | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-larger-particle-replication-subplan-2026-06-23.md` |
| Aggregate JSON | `docs/benchmarks/actual-sir-low-rank-larger-particle-replication-2026-06-23.json` |
| Aggregate Markdown | `docs/benchmarks/actual-sir-low-rank-larger-particle-replication-2026-06-23.md` |
| Result artifact | This file |

## Post-Run Red-Team Note

- Strongest alternative explanation: the candidates may be favorable for the
  two `N=512` seeds used here but fail on another seed batch or at a larger
  particle count.
- What would overturn advancement: independent seed replication or a larger-N
  screen showing hard vetoes, missing GPU/XLA provenance, failed paired
  comparability, missing row artifacts, or warm-time screen failure.
- Weakest part of the evidence: the result is still a viability screen with one
  `N=512` seed batch; it does not support ranking among the five candidates.

## Next-Phase Handoff

Advance these five candidates to a same-particle seed-replication subplan:

- `r16_eps0p25_alpha1em08_it120`
- `r16_eps0p125_alpha1em08_it120`
- `r32_eps0p25_alpha1em08_it120`
- `r64_eps0p25_alpha1em08_it120`
- `r128_eps0p25_alpha1em08_it120`

Do not revive `r64_eps0p125_alpha1em08_it120` without a new repair/tuning
subplan, because it failed heldout paired comparability.

## Forbidden Claims Preserved

This result is a larger-particle viability screen only. It does not claim
speedup, posterior correctness, HMC readiness, dense Sinkhorn equivalence,
public API/default readiness, broad scalable-OT superiority, statistical
ranking, or production scientific validity. It also does not authorize NumPy as
BayesFilter-owned algorithmic implementation; the production route remains the
GPU/XLA TensorFlow/TFP lane.
