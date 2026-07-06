# Actual-SIR Low-Rank Heldout Replication Result

Date: 2026-06-23

Status: `HELDOUT_SCREEN_FIVE_CANDIDATES_REMAIN_VIABLE`

## Phase Objective

Validate the six repaired compiled-screen low-rank freeze-nominated candidates
on heldout seeds under the same GPU/XLA compiled-core provenance contract, then
decide whether any candidate may advance to a larger-shape validation screen.

## Evidence Contract Result

- Question: do any of the six bounded-screen freeze-nominated low-rank
  candidates remain viable on heldout seeds under the same compiled GPU/XLA
  actual-SIR screen?
- Baseline/comparator: paired streaming actual-SIR route rows from the same
  harness, shape, seeds, dtype, TF32 mode, GPU visibility, and compiled-core
  timing contract.
- Primary screen: no hard vetoes, complete low-rank compiled/XLA provenance,
  complete GPU/TF32 provenance, paired comparability pass, and warm-time screen
  pass on the heldout batch.
- Result: `5/6` exact heldout candidates were labeled `freeze-nominated`;
  `1/6` was labeled `faster-but-incomparable`.
- Candidate rejection: `r64_eps0p125_alpha1em08_it120` is rejected at this gate
  because paired comparability failed, not because of a hard route veto.
- Route/research direction: this result does not reject the repaired low-rank
  route; it narrows the viable candidate set for the next phase.

## Checks And Runs

- Syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- Focused tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `17 passed`.
- Exact candidate dry-run:
  `python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode dry-run ... --candidate-ids <six heldout ids> --output /tmp/actual-sir-low-rank-heldout-exact-candidate-dry-run.json --markdown-output /tmp/actual-sir-low-rank-heldout-exact-candidate-dry-run.md`
  - Result: pass; dry-run emitted exactly the six requested candidate ids.
- Trusted GPU heldout execution:
  `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode execute --route both --batch-seeds 81121,81122,81123 --time-steps 20 --num-particles 256 --low-rank-ranks 16,32,64,128 --low-rank-assignment-epsilons 0.25,0.125 --low-rank-max-projection-iterations-list 120 --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120,r32_eps0p25_alpha1em08_it120,r64_eps0p25_alpha1em08_it120,r64_eps0p125_alpha1em08_it120,r128_eps0p25_alpha1em08_it120 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --jit-compile --row-timeout-seconds 1200 --output docs/benchmarks/actual-sir-low-rank-heldout-replication-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-low-rank-heldout-replication-2026-06-23.md`
  - Result: pass, aggregate status `PASS`, wall time
    `2366.7426987669896` seconds.
- Aggregate consistency check:
  - Result: pass, `heldout-aggregate-consistency-pass`.

## Heldout Summary

Execution shape and policy:

- Seeds: `[81121, 81122, 81123]`
- Shape: batch `3`, time steps `20`, particles `256`, state dimension `18`,
  observation dimension `9`
- Execution: `float32`, TF32 enabled, `CUDA_VISIBLE_DEVICES=1`, requested
  `/GPU:0`, expected GPU outputs, `jit_compile=true`
- Timing: streaming and low-rank timing source `compiled_core`
- Aggregate labels: `5` `freeze-nominated`, `1`
  `faster-but-incomparable`

| Candidate | Label | Hard vetoes | Paired comparable | Warm screen | Warm median streaming/low-rank | Log-likelihood max abs delta | Log-likelihood mean abs delta |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `1.8753985467825245` | `0.538818359375` | `0.24674479166666666` |
| `r16_eps0p125_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `1.7477454952049019` | `5.6849365234375` | `2.8760172526041665` |
| `r32_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `2.072013685722924` | `0.10589599609375` | `0.06005859375` |
| `r64_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `1.9749575539640345` | `0.46295166015625` | `0.16355387369791666` |
| `r64_eps0p125_alpha1em08_it120` | `faster-but-incomparable` | `[]` | `false` | `true` | `1.6279639455559005` | `20.61773681640625` | `10.37982177734375` |
| `r128_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | `1.968254973636949` | `0.2415771484375` | `0.14990234375` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance five candidates to larger-shape validation | Passed for `5/6` exact heldout candidates | No row hard vetoes; one candidate failed paired comparability and is not advanced | Three heldout seeds at one particle count; descriptive warm timing does not support ranking | Draft and review a larger-particle paired GPU/XLA subplan for the five heldout survivors only | No posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, speedup claim, scientific superiority, or statistical ranking |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for all six heldout rows; hard vetoes were `[]` |
| Paired comparability | Passed for five candidates; failed for `r64_eps0p125_alpha1em08_it120` |
| Statistically supported ranking | Not established; no uncertainty model or replication sufficient for ranking |
| Descriptive-only differences | Warm median ratios, row wall times, residual magnitudes, and exact deltas are descriptive screen diagnostics |
| Default-readiness | Not established; this is not a public API/default promotion gate |
| Next evidence needed | Larger-particle paired GPU/XLA screen over the five heldout-surviving candidates, followed by uncertainty-aware replication only if larger-shape validity survives |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Working tree | Dirty before and during the run; unrelated user/generated changes preserved |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` |
| Platform | `Linux-6.8.0-111-generic-x86_64-with-glibc2.35` |
| GPU | NVIDIA GeForce RTX 4080 SUPER, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| Started | `2026-06-22T18:02:41.710023+00:00` |
| Ended | `2026-06-22T18:42:08.405426+00:00` |
| Wall time | `2366.7426987669896` seconds |
| Seeds | `81121,81122,81123` |
| Shape | batch `3`, time steps `20`, particles `256`, state dimension `18`, observation dimension `9` |
| Execution policy | `float32`, TF32 enabled, GPU visible, `jit_compile=true`, `compiled_core` timing |
| Plan | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-heldout-replication-subplan-2026-06-23.md` |
| Aggregate JSON | `docs/benchmarks/actual-sir-low-rank-heldout-replication-2026-06-23.json` |
| Aggregate Markdown | `docs/benchmarks/actual-sir-low-rank-heldout-replication-2026-06-23.md` |
| Result artifact | This file |

## Post-Run Red-Team Note

- Strongest alternative explanation: the five surviving candidates may be
  favorable only at `N=256` and may fail paired comparability, hard validity,
  or warm-time support at a larger particle count.
- What would overturn advancement: larger-particle rows showing hard vetoes,
  missing GPU/XLA provenance, failed paired comparability for the survivor set,
  or invalid artifacts under the next subplan.
- Weakest part of the evidence: heldout replication is still a screen without
  uncertainty analysis; it should not be used for ranking or default claims.

## Next-Phase Handoff

Advance only these five heldout-surviving candidates:

- `r16_eps0p25_alpha1em08_it120`
- `r16_eps0p125_alpha1em08_it120`
- `r32_eps0p25_alpha1em08_it120`
- `r64_eps0p25_alpha1em08_it120`
- `r128_eps0p25_alpha1em08_it120`

Do not advance `r64_eps0p125_alpha1em08_it120` without a new repair/tuning
subplan, because it failed paired comparability on heldout seeds.

## Forbidden Claims Preserved

This result is a heldout viability screen only. It does not claim speedup,
posterior correctness, HMC readiness, dense Sinkhorn equivalence, public
API/default readiness, broad scalable-OT superiority, statistical ranking, or
production scientific validity.
