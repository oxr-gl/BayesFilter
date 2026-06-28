# Actual-SIR Low-Rank Compiled Rerun Result

Date: 2026-06-23

Status: `COMPILED_BOUNDED_SCREEN_FREEZE_CANDIDATES_NOMINATED`

## Phase Objective

Rerun the actual-SIR low-rank tuning/performance screen after the TensorFlow
tensor-only XLA repair, using GPU-targeted compiled-core route timing only, to
answer whether the earlier stale no-freeze-candidate tuning verdict changes.

## Evidence Contract Result

- Question: after removing eager/NumPy-style timing barriers from the low-rank
  route, does the repaired GPU/XLA compiled-core route nominate any low-rank
  freeze candidate on the bounded actual-SIR screen?
- Baseline/comparator: paired streaming actual-SIR route rows from the same
  harness, seed, shape, dtype, TF32 mode, GPU visibility, and compiled-core
  timing contract.
- Primary screen: `freeze-nominated` rows only, requiring no hard vetoes,
  paired comparability pass, complete low-rank compiled/XLA provenance,
  complete GPU/TF32 provenance, and the predeclared warm-time screen.
- Result: the repaired bounded grid produced `6` freeze-nominated rows out of
  `12` candidates.
- Verdict change: yes. The earlier contaminated/stale P03 practical verdict
  of no freeze candidate is superseded for this bounded repaired-provenance
  screen. The repair result itself remains accepted; this result changes the
  performance/tuning-screen conclusion, not the repair-safety conclusion.

## Required Checks And Runs

- Syntax check:
  `python -m py_compile docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_low_rank_coupling_solver_tf.py tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- Solver/harness guard scan:
  `rg -n "import numpy|\\.numpy\\(|np\\." ...`
  - Result: no NumPy or `.numpy()` hit in the solver source; remaining
    `.numpy()` hits are in artifact/reporting harness boundaries and test
    guards, not in the compiled solver region.
- Trusted GPU precheck:
  `nvidia-smi --query-gpu=index,name,uuid,memory.used,utilization.gpu --format=csv,noheader,nounits`
  - Result before smoke: GPU 1 was visible and idle enough for the run:
    NVIDIA GeForce RTX 4080 SUPER,
    UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`, `18` MiB used,
    `0%` utilization.
- Tiny compiled GPU smoke:
  `docs/benchmarks/actual-sir-low-rank-compiled-rerun-p01-smoke-2026-06-23.json`
  and matching Markdown.
  - Result: `PASS`; hard vetoes `[]`; `jit_compile=true`;
    streaming and low-rank timing source `compiled_core`; outputs on GPU.
- Bounded compiled GPU grid:
  `docs/benchmarks/actual-sir-low-rank-compiled-rerun-p02-grid-2026-06-23.json`
  and matching Markdown.
  - Result: `PASS`; `12` candidates; `6` `freeze-nominated`; `6`
    `faster-but-incomparable`; no `comparable-but-slow` rows.

## Grid Summary

Shape and execution policy:

- Seeds: `[81120]`
- Shape: batch `1`, time steps `20`, particles `256`, state dimension `18`,
  observation dimension `9`
- Grid: ranks `16,32,64,128`; assignment epsilons `0.25,0.125,0.0625`;
  alpha `1e-8`; max projection iterations `120`
- Execution: `float32`, TF32 enabled, `CUDA_VISIBLE_DEVICES=1`, requested
  `/GPU:0`, expected GPU outputs, `jit_compile=true`, streaming and low-rank
  timing source `compiled_core`
- Aggregate wall time: `4526.399282467086` seconds

| Candidate | Label | Hard vetoes | Paired comparable | Warm screen | Warm median streaming/low-rank | Log-likelihood max abs delta |
| --- | --- | --- | --- | --- | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `2.2901924084391547` | `0.1278076171875` |
| `r16_eps0p125_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `2.045022721630183` | `3.01861572265625` |
| `r16_eps0p0625_alpha1em08_it120` | `faster-but-incomparable` | `[]` | `false` | `true` | `2.055144526330265` | `8.1591796875` |
| `r32_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `1.9589795469158031` | `0.07293701171875` |
| `r32_eps0p125_alpha1em08_it120` | `faster-but-incomparable` | `[]` | `false` | `true` | `2.0006952688498263` | `5.277587890625` |
| `r32_eps0p0625_alpha1em08_it120` | `faster-but-incomparable` | `[]` | `false` | `true` | `1.8285954735630399` | `12.01556396484375` |
| `r64_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `2.0621770248004045` | `0.0103759765625` |
| `r64_eps0p125_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `1.8226511607244062` | `2.2313232421875` |
| `r64_eps0p0625_alpha1em08_it120` | `faster-but-incomparable` | `[]` | `false` | `true` | `1.8536465238719768` | `17.04644775390625` |
| `r128_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `2.1603238361840957` | `0.374267578125` |
| `r128_eps0p125_alpha1em08_it120` | `faster-but-incomparable` | `[]` | `false` | `true` | `1.766378204289601` | `13.794677734375` |
| `r128_eps0p0625_alpha1em08_it120` | `faster-but-incomparable` | `[]` | `false` | `true` | `1.7256428395754424` | `30.131103515625` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Bounded repaired screen nominates low-rank freeze candidates | Passed: `6/12` rows are `freeze-nominated` under compiled GPU/XLA provenance | No row hard vetoes in the aggregate labels; smoke hard vetoes `[]` | One seed and one target shape; warm timing is descriptive screen evidence, not statistical speed evidence | Draft heldout/replication subplan for the six nominated candidates | No posterior correctness, HMC readiness, dense Sinkhorn equivalence, production readiness, or statistical ranking |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for smoke and grid rows used in candidate nomination |
| Statistically supported ranking | Not established; one-seed bounded screen only |
| Descriptive-only differences | Warm median ratios and row wall times are descriptive screen diagnostics |
| Default-readiness | Not established; this is not a public API/default promotion gate |
| Next evidence needed | Heldout/replicated GPU/XLA runs over nominated candidates, with predeclared uncertainty discipline and no ranking from descriptive timing alone |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Working tree | Dirty before this run; unrelated user/generated changes preserved |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` |
| TensorFlow | `2.20.0` |
| GPU | NVIDIA GeForce RTX 4080 SUPER, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| Command | `python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode execute --route both --batch-seeds 81120 --time-steps 20 --num-particles 256 --low-rank-ranks 16,32,64,128 --low-rank-assignment-epsilons 0.25,0.125,0.0625 --low-rank-max-projection-iterations-list 120 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --jit-compile --row-timeout-seconds 900 --output docs/benchmarks/actual-sir-low-rank-compiled-rerun-p02-grid-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-low-rank-compiled-rerun-p02-grid-2026-06-23.md` |
| Plan | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-compiled-rerun-subplan-2026-06-23.md` |
| Smoke artifact | `docs/benchmarks/actual-sir-low-rank-compiled-rerun-p01-smoke-2026-06-23.json` |
| Grid artifact | `docs/benchmarks/actual-sir-low-rank-compiled-rerun-p02-grid-2026-06-23.json` |
| Result artifact | This file |

## Post-Run Red-Team Note

- Strongest alternative explanation: the bounded screen may be favorable for
  this single seed and shape but fail heldout seeds, larger particle counts, or
  stricter downstream scientific criteria.
- What would overturn this result: heldout/replicated compiled GPU rows showing
  hard vetoes, failed comparability for nominated candidates, or warm screen
  failures under the predeclared heldout contract.
- Weakest part of the evidence: timing and candidate selection are based on one
  seed and one shape; no uncertainty analysis supports ranking.

## Next-Phase Handoff

Proceed to a heldout/replication subplan only for the nominated rows:

- `r16_eps0p25_alpha1em08_it120`
- `r16_eps0p125_alpha1em08_it120`
- `r32_eps0p25_alpha1em08_it120`
- `r64_eps0p25_alpha1em08_it120`
- `r64_eps0p125_alpha1em08_it120`
- `r128_eps0p25_alpha1em08_it120`

The next phase must preserve compiled GPU/XLA provenance and must not rank
candidates statistically without predeclared uncertainty evidence.

## Forbidden Claims Preserved

This result nominates candidates for the next evidence gate only. It does not
claim posterior correctness, HMC readiness, dense Sinkhorn equivalence, public
API/default readiness, broad scalable-OT superiority, statistical ranking, or
production scientific validity.
