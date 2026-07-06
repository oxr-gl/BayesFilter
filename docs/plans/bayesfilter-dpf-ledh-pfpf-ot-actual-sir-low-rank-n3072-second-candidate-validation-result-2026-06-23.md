# Actual-SIR Low-Rank N3072 Second-Candidate Validation Result

Date: 2026-06-23

Status: `PASS_SECOND_CANDIDATE_ROW_WITH_CONSOLIDATION_HANDOFF`

## Phase Summary

The `N=3072` second-candidate validation phase completed with a valid paired
GPU/XLA aggregate:

- JSON:
  `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.json`
- Markdown:
  `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.md`

The single row was:

- `r16_eps0p125_alpha1em08_it120`
- seeds `81137,81138`
- batch `2`, time steps `20`, particles `3072`
- `float32`, TF32 enabled, GPU-visible execution
- streaming timing source `compiled_core`
- low-rank timing source `compiled_core`
- `jit_compile=True`
- `--cuda-visible-devices 1 --device /GPU:0`

The row passed the predeclared second-candidate validation screen and was
labeled `freeze-nominated` by the harness. This is a bounded completion and
artifact-validity result only. It is not a ranking, speedup claim,
posterior-correctness claim, HMC-readiness claim, dense Sinkhorn equivalence
claim, public API/default readiness claim, broad scalable-OT claim,
scientific-validity claim, or rejection of the other viable/deferred
candidates.

Human approval used for this runtime was the transcript message after the
N3072 resource-boundary closeout: `yesI approve`.

## Required Checks

Completed checks:

- Claude Opus/max focused R2 read-only review:
  - Result: `VERDICT: AGREE`
  - Ledger:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-second-candidate-validation-review-ledger-2026-06-23.md`
- Trusted GPU precheck:
  - GPU 1: `18 / 32760 MiB`, utilization `0%`
  - decision: GPU 1 suitable for the bounded run
- Refreshed exact dry-run:
  - Result: pass
  - `summary.num_candidates = 1`
  - exact candidate id `r16_eps0p125_alpha1em08_it120`
  - exact assignment epsilon `0.125`
  - exact seeds `81137,81138`
  - exact shape batch `2`, time steps `20`, particles `3072`
  - row JSON basename `254` bytes, Markdown basename `252` bytes, log basename
    `253` bytes
- Aggregate artifact validation after execution: `PASS`
  - aggregate status `PASS`
  - `summary.num_candidates = 1`
  - `summary.num_freeze_nominated = 1`
  - exact candidate id `r16_eps0p125_alpha1em08_it120`
  - exact assignment epsilon `0.125`
  - exact seeds `81137,81138`
  - exact shape batch `2`, time steps `20`, particles `3072`
  - row status `PASS`
  - row hard vetoes `[]`
  - actual-SIR semantics pass `true`
  - row JSON/Markdown/log artifacts exist
  - row JSON basename `255` bytes, Markdown basename `253` bytes, log basename
    `254` bytes
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: `18 passed`
- Trusted post-run GPU check:
  - GPU 1 returned to `18 / 32760 MiB`, utilization `0%`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Close the N3072 second-candidate validation as passed, then move to a local no-runtime N3072 two-row consolidation/resource-boundary subplan |
| Primary criterion status | Passed: one exact second-candidate row completed with no hard vetoes, GPU/XLA/TF32 compiled-core provenance, paired comparability diagnostics within thresholds, and preserved artifacts |
| Veto diagnostic status | No hard-veto, timeout, provenance, comparability-threshold, stale-row, artifact, GPU, or filename-length veto fired |
| Main uncertainty | One N3072 row for each rank-16 candidate does not establish statistical ranking, speedup, N4096 feasibility, seed robustness at N3072, posterior correctness, HMC readiness, dense equivalence, or product/scientific readiness |
| Next justified action | Draft and review a no-runtime N3072 two-row consolidation/resource-boundary subplan |
| What is not being concluded | No speedup, superiority, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, statistical ranking, scientific validity, or invalidity of viable/deferred candidates |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the one second-candidate N3072 row |
| Statistically supported ranking | None; this phase ran one fixed candidate and does not rank candidates |
| Descriptive-only differences | Warm ratio, warm medians, wall time, first-call times, log-likelihood deltas, residual magnitudes, ESS, and GPU memory snapshots |
| Default-readiness | Not evaluated by this phase |
| Next evidence needed | Local consolidation/resource-boundary result; any future runtime needs a fresh reviewed subplan and approval |

## Row Result

| Candidate | Status | Label | Warm ratio | Threshold | Mean abs loglik delta | Max abs loglik delta | ESS min | Final logsumexp residual | Row wall time |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `r16_eps0p125_alpha1em08_it120` | `PASS` | `freeze-nominated` | 10.140608807393965 | 1.25 | 1.33868408203125 | 1.6871337890625 | 0.6319534778594971 | 9.5367431640625e-07 | 386.48628454096615s |

For the row:

- row hard vetoes: `[]`
- actual-SIR semantics pass: `true`
- filtered mean relative L2: `0.0007172919954221708`
- filtered variance relative L2: `0.08573564561058275`
- final particle mean relative L2: `0.00043105992246831194`
- paired comparability thresholds were present in the row artifact and the row
  status was `PASS`
- selected GPU: GPU 1, NVIDIA GeForce RTX 4080 SUPER, UUID
  `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`
- selected physical GPU memory snapshot in the row manifest:
  `30693` MiB

The warm ratio and memory snapshot are descriptive/resource-triage diagnostics
only in this phase. They do not establish speedup, ranking, or formal memory
scaling.

## Artifact Manifest

| Artifact | Status |
| --- | --- |
| Subplan | Present: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-second-candidate-validation-subplan-2026-06-23.md` |
| Review ledger | Present: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-second-candidate-validation-review-ledger-2026-06-23.md` |
| Aggregate JSON | Present and validated: `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.json` |
| Aggregate Markdown | Present: `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.md` |
| Row JSON | Present: `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23-b2-t20-n3072-r16-eps0p125-a1em08-it120-seed81137_81138-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float-h63fd5ec16a683262.json` |
| Row Markdown | Present: `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23-b2-t20-n3072-r16-eps0p125-a1em08-it120-seed81137_81138-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float-h63fd5ec16a683262.md` |
| Row log | Present: `docs/benchmarks/logs/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23-b2-t20-n3072-r16-eps0p125-a1em08-it120-seed81137_81138-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float-h63fd5ec16a683262.log` |
| Local artifact consistency check | Passed |
| Local syntax check | Passed |
| Focused grid tests | `18 passed` |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Top-level command | `python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode execute --route both --batch-seeds 81137,81138 --time-steps 20 --num-particles 3072 --low-rank-ranks 16 --low-rank-assignment-epsilons 0.125 --low-rank-max-projection-iterations-list 120 --candidate-ids r16_eps0p125_alpha1em08_it120 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --jit-compile --row-timeout-seconds 7200 --output docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.md --quiet` |
| Row command | `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py --route both --streaming-timing-source compiled_core --low-rank-timing-source compiled_core --batch-seeds 81137,81138 --time-steps 20 --num-particles 3072 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --low-rank-rank 16 --low-rank-assignment-epsilon 0.125 --low-rank-alpha 1e-08 --low-rank-max-projection-iterations 120 --low-rank-convergence-threshold 1e-06 --low-rank-denominator-floor 1e-30 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --device /GPU:0 --expect-device-kind gpu --phase-id ACTUAL-SIR-LR-TUNING-r16_eps0p125_alpha1em08_it120 --output docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23-b2-t20-n3072-r16-eps0p125-a1em08-it120-seed81137_81138-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float-h63fd5ec16a683262.json --markdown-output docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23-b2-t20-n3072-r16-eps0p125-a1em08-it120-seed81137_81138-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float-h63fd5ec16a683262.md --jit-compile --cuda-visible-devices 1` |
| Environment | Python `3.13.13`, TensorFlow `2.20.0`, active TensorFlow GPU environment |
| GPU/CPU status | Trusted GPU execution on GPU 1, NVIDIA GeForce RTX 4080 SUPER, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`; CPU-only was not used |
| Seeds | `81137,81138` |
| Shape | batch `2`, time steps `20`, particles `3072`, state dim `18`, obs dim `9` |
| Dtype/TF32 | `float32`, TF32 enabled |
| Timing source | streaming `compiled_core`, low-rank `compiled_core`, `jit_compile=True` |
| Started/ended | `2026-06-23T13:52:58.721173+00:00` to `2026-06-23T13:59:25.207447+00:00` |
| Wall time | row manifest `386.48628454096615s` |
| Aggregate `plan_path` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-master-program-2026-06-22.md` |
| Row manifest `plan_path` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-master-program-2026-06-21.md` |
| Governing phase subplan | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-second-candidate-validation-subplan-2026-06-23.md` |
| Result file | this file |

The runner records broader master-program paths because it does not accept a
per-phase subplan-path argument. The dedicated second-candidate subplan governed
the current phase through the visible execution/review protocol.

## Post-Run Red-Team Note

The strongest alternative explanation is that the pass demonstrates only that
this exact candidate, seed batch, shape, GPU, and harness state completed one
N3072 paired row. The result does not show seed robustness at N3072, N4096
feasibility, candidate superiority, a statistically supported ranking, formal
memory scaling, posterior correctness, or HMC readiness. The row JSON basename
is exactly `255` bytes, so future artifact-name growth is a practical boundary
risk and must be checked before any future runtime.

## Handoff

Proceed to a no-runtime N3072 two-row consolidation/resource-boundary subplan
before any additional GPU runtime:

`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-two-row-consolidation-resource-boundary-subplan-2026-06-23.md`
