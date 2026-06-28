# Actual-SIR Low-Rank N1024 Seed-Replication Result

Date: 2026-06-23

Status: `N1024_SEED_REPLICATION_FIVE_CANDIDATES_REMAIN_VIABLE`

## Phase Objective

Run an independent `N=1024` seed-replication screen for the five low-rank
actual-SIR candidates that survived heldout, two `N=512` screens, and the first
`N=1024` paired-validation screen.

## Evidence Contract Result

- Question: do the five `N=1024` paired-validation survivors remain viable on
  an independent `N=1024` seed batch under the same compiled GPU/XLA actual-SIR
  paired screen?
- Baseline/comparator: paired streaming actual-SIR route rows from the same
  harness, seed batch, shape, dtype, TF32 mode, GPU visibility, and
  compiled-core timing contract.
- Primary screen: no hard vetoes, complete GPU/XLA compiled-core provenance,
  paired comparability pass, warm-time screen pass, and preserved per-row
  JSON/Markdown/log artifact paths.
- Warm-time screen criterion: each row satisfied
  `paired_comparability.warm_median_streaming_over_low_rank >= paired_comparability.thresholds.warm_median_streaming_over_low_rank`
  using the harness default threshold `1.25`.
- Result: `5/5` exact survivor candidates were labeled `freeze-nominated` on
  independent `N=1024` seeds.
- Candidate rejection: no candidate was rejected at this gate.
- Research direction: this result supports continued gated validation of the
  repaired low-rank route, but it is still not a statistical ranking, speedup
  claim, posterior-correctness claim, or default-readiness claim.

## Checks And Runs

- Syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- Focused tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `17 passed`.
- Exact candidate dry-run:
  `python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode dry-run ... --candidate-ids <five survivor ids> --output /tmp/actual-sir-low-rank-n1024-seed-replication-exact-candidate-dry-run.json --markdown-output /tmp/actual-sir-low-rank-n1024-seed-replication-exact-candidate-dry-run.md --quiet`
  - Result: pass, `n1024-seed-replication-dry-run-consistency-pass`.
- Trusted GPU precheck:
  `nvidia-smi --query-gpu=index,name,uuid,memory.used,utilization.gpu --format=csv,noheader,nounits`
  - Result immediately before execution: GPU 1 was visible and idle:
    NVIDIA GeForce RTX 4080 SUPER, UUID
    `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`, `18` MiB used, `0%`
    utilization.
- Claude read-only review:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n1024-seed-replication-review-ledger-2026-06-23.md`
  - Round 1: `VERDICT: REVISE`; fixed close-record artifact contract and
    warm-screen boundary.
  - Round 2: `VERDICT: AGREE`.
- Trusted GPU N1024 seed-replication execution:
  `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode execute --route both --batch-seeds 81131,81132 --time-steps 20 --num-particles 1024 --low-rank-ranks 16,32,64,128 --low-rank-assignment-epsilons 0.25,0.125 --low-rank-max-projection-iterations-list 120 --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120,r32_eps0p25_alpha1em08_it120,r64_eps0p25_alpha1em08_it120,r128_eps0p25_alpha1em08_it120 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --jit-compile --row-timeout-seconds 3600 --output docs/benchmarks/actual-sir-low-rank-n1024-seed-replication-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-low-rank-n1024-seed-replication-2026-06-23.md`
  - Result: pass, aggregate status `PASS`, wall time
    `2005.9731243301649` seconds.
- Aggregate consistency check:
  - Result: pass,
    `n1024-seed-replication-aggregate-consistency-pass`.

## N1024 Seed-Replication Summary

Execution shape and policy:

- Seeds: `[81131, 81132]`
- Shape: batch `2`, time steps `20`, particles `1024`, state dimension `18`,
  observation dimension `9`
- Execution: `float32`, TF32 enabled, `CUDA_VISIBLE_DEVICES=1`, requested
  `/GPU:0`, expected GPU outputs, `jit_compile=true`
- Timing: streaming and low-rank timing source `compiled_core`
- Aggregate labels: `5` `freeze-nominated`

| Candidate | Label | Hard vetoes | Paired comparable | Warm screen | Warm median streaming/low-rank | Log-likelihood max abs delta | Log-likelihood mean abs delta | Factor residual | Row wall time seconds |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | 4.483958 | 0.175903 | 0.164490 | 2.23517e-08 | 401.505289 |
| `r16_eps0p125_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | 4.393109 | 2.094177 | 1.820709 | 2.98023e-08 | 408.110848 |
| `r32_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | 4.504955 | 0.132324 | 0.066193 | 7.45058e-09 | 401.683671 |
| `r64_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | 4.421705 | 0.124329 | 0.111206 | 5.58794e-09 | 397.682322 |
| `r128_eps0p25_alpha1em08_it120` | `freeze-nominated` | `[]` | `true` | `true` | 4.430927 | 0.159485 | 0.091492 | 1.70199e-07 | 396.924044 |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance all five candidates to a separately reviewed consolidation/resource-envelope or larger-`N` validation subplan | Passed for `5/5` exact survivor candidates on independent `N=1024` seeds | No row hard vetoes; all rows had paired comparability, warm-time support, GPU/XLA provenance, low-rank provenance, and row artifact paths | The evidence still does not support statistical ranking; later phases may expose resource-envelope, high-`N`, or broader scientific-validity failures | Draft and review the next subplan before execution; consolidation, if chosen, must use hard-veto survival and resource-envelope criteria, not descriptive timing rank | No posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, speedup claim, scientific superiority, production scientific validity, or statistical ranking |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for all five independent N1024 rows; hard vetoes were `[]` |
| Paired comparability | Passed for all five candidates |
| Warm-screen viability | Passed for all five candidates against the predeclared threshold source |
| Statistically supported ranking | Not established; observed warm ratios and row times are descriptive only |
| Descriptive-only differences | Warm median ratios, row wall times, residual magnitudes, and exact deltas are descriptive screen diagnostics |
| Default-readiness | Not established; this is not a public API/default promotion gate |
| Next evidence needed | Reviewed consolidation/resource-envelope or larger-`N` validation plan with explicit criteria and nonclaims |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Working tree | Dirty before and during the run; unrelated user/generated changes preserved |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` |
| Platform | `Linux-6.8.0-111-generic-x86_64-with-glibc2.35` |
| GPU | NVIDIA GeForce RTX 4080 SUPER, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| Started | `2026-06-23T10:58:17.915507+00:00` |
| Ended | `2026-06-23T11:31:43.842813+00:00` |
| Wall time | `2005.9731243301649` seconds |
| Seeds | `81131,81132` |
| Shape | batch `2`, time steps `20`, particles `1024`, state dimension `18`, observation dimension `9` |
| Execution policy | `float32`, TF32 enabled, GPU visible, `jit_compile=true`, `compiled_core` timing |
| Plan | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n1024-seed-replication-subplan-2026-06-23.md` |
| Aggregate JSON | `docs/benchmarks/actual-sir-low-rank-n1024-seed-replication-2026-06-23.json` |
| Aggregate Markdown | `docs/benchmarks/actual-sir-low-rank-n1024-seed-replication-2026-06-23.md` |
| Result artifact | This file |

## Post-Run Red-Team Note

- Strongest alternative explanation: the current candidate set may be robust
  across the tested N1024 seed batches but still fail at larger `N`, under a
  tighter resource envelope, or under a scientific-validity gate not exercised
  by this viability screen.
- What would overturn advancement: a reviewed next phase showing hard vetoes,
  missing GPU/XLA provenance, failed paired comparability, failed warm screen,
  missing row artifacts, timeout, or a boundary violation under the predeclared
  contract.
- Weakest part of the evidence: the result is still a staged viability screen.
  It does not contain an uncertainty model or enough replication to rank viable
  candidates, and it does not validate posterior correctness.

## Next-Phase Handoff

Advance these five candidates to a reviewed next subplan:

- `r16_eps0p25_alpha1em08_it120`
- `r16_eps0p125_alpha1em08_it120`
- `r32_eps0p25_alpha1em08_it120`
- `r64_eps0p25_alpha1em08_it120`
- `r128_eps0p25_alpha1em08_it120`

The next subplan should be either a consolidation/resource-envelope gate or a
larger-`N` validation gate. Candidate consolidation is allowed only if the
subplan declares an engineering-only criterion based on hard-veto survival and
resource envelope, not descriptive timing rank.

Do not revive `r64_eps0p125_alpha1em08_it120` without a new repair/tuning
subplan, because it failed heldout paired comparability.

## Forbidden Claims Preserved

This result is an independent `N=1024` seed-replication viability screen only.
It does not claim speedup, posterior correctness, HMC readiness, dense Sinkhorn
equivalence, public API/default readiness, broad scalable-OT superiority,
statistical ranking, or production scientific validity. It also does not
authorize NumPy as BayesFilter-owned algorithmic implementation; the production
route remains the GPU/XLA TensorFlow/TFP lane.
