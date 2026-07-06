# Actual-SIR Low-Rank N3072 Representative Resource-Smoke Result

Date: 2026-06-23

Status: `PASS_RESOURCE_SMOKE_WITH_RESOURCE_BOUNDARY_HANDOFF`

## Phase Summary

The `N=3072` representative resource-smoke phase completed with a valid paired
GPU/XLA aggregate:

- JSON:
  `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.json`
- Markdown:
  `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.md`

The single representative row was:

- `r16_eps0p25_alpha1em08_it120`
- seeds `81137,81138`
- batch `2`, time steps `20`, particles `3072`
- `float32`, TF32 enabled, GPU-visible execution
- streaming timing source `compiled_core`
- low-rank timing source `compiled_core`
- `jit_compile=True`

The row passed the predeclared resource-smoke screen and was labeled
`freeze-nominated` by the harness. This is a resource-smoke pass only. It is
not a candidate ranking, speedup claim, posterior-correctness claim,
HMC-readiness claim, dense Sinkhorn equivalence claim, public API/default
readiness claim, broad scalable-OT claim, scientific-validity claim, or
rejection of `r16_eps0p125_alpha1em08_it120`.

## Required Checks

Completed checks:

- Aggregate artifact validation: `PASS`
  - `summary.num_candidates = 1`
  - `summary.num_freeze_nominated = 1`
  - exact candidate id `r16_eps0p25_alpha1em08_it120`
  - aggregate status `PASS`
  - row status `PASS`
  - row label `freeze-nominated`
  - row hard vetoes `[]`
  - paired comparability pass `true`
  - warm-time screen pass `true`
  - low-rank provenance complete `true`
  - GPU/TF32 provenance complete `true`
  - warm threshold `1.25`
  - row JSON/Markdown/log artifacts exist
  - row JSON basename is `255` bytes, Markdown basename is `253` bytes, and log
    basename is `254` bytes
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: `18 passed`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Close the N3072 representative resource smoke as passed, then move to a local resource-boundary closeout decision before any further runtime |
| Primary criterion status | Passed: one representative row completed with no hard vetoes, complete provenance, comparability pass, warm-screen pass, and preserved artifacts |
| Veto diagnostic status | No hard veto, timeout, provenance, comparability, warm-screen, stale-row, artifact, or filename-length veto fired |
| Main uncertainty | One N3072 representative row does not establish two-candidate N3072 feasibility, N4096 feasibility, statistical ranking, or formal memory scaling |
| Next justified action | Draft and review a local N3072 resource-boundary closeout subplan |
| What is not being concluded | No speedup, superiority, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, statistical ranking, scientific validity, or invalidity of other viable/deferred candidates |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the one representative N3072 row |
| Statistically supported ranking | None; the representative row was selected by fixed carry-forward order, not by statistical evidence |
| Descriptive-only differences | Warm ratio, wall time, first-call times, log-likelihood deltas, factor residual, and GPU memory snapshots |
| Default-readiness | Not evaluated by this phase |
| Next evidence needed | Local resource-boundary closeout; any future runtime needs a separate reviewed subplan with explicit resource stop conditions |

## Row Result

| Candidate | Status | Label | Warm ratio | Threshold | Mean abs loglik delta | Max abs loglik delta | Max factor residual | Row wall time |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | `PASS` | `freeze-nominated` | 10.344294680968009 | 1.25 | 0.097137451171875 | 0.1087646484375 | 2.9802322387695312e-08 | 396.94959120010026s |

For the row:

- row hard vetoes: `[]`
- paired comparability: `true`
- warm-time screen: `true`
- low-rank provenance complete: `true`
- GPU/TF32 provenance complete: `true`
- active resampling mask count: `20`
- route invocations: `20`
- streaming first call: `217.34201490390114s`
- low-rank first call: `147.60029216995463s`
- selected GPU: GPU 1, NVIDIA GeForce RTX 4080 SUPER, UUID
  `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`
- selected physical GPU memory snapshot: the aggregate's `nvidia-smi`-derived
  `selected_physical_gpu.memory_used_mib` field is `30693` MiB at provenance
  capture

Memory observations are explanatory only. A trusted post-review `nvidia-smi`
check on this host reported `32760` MiB total memory for the named device class,
so the recorded `30693` MiB value is not internally contradictory to this
machine's local GPU report. It is still not formal memory-scaling evidence,
does not by itself prove or disprove larger shapes, and is not the sole basis
for the resource-boundary handoff.

## Artifact Manifest

| Artifact | Status |
| --- | --- |
| N3072 aggregate JSON | Present and validated |
| N3072 aggregate Markdown | Present |
| Row JSON | Present: `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23-b2-t20-n3072-r16-eps0p25-a1em08-it120-seed81137_81138-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-floa-h062c4f3957dc21a0.json` |
| Row Markdown | Present: `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23-b2-t20-n3072-r16-eps0p25-a1em08-it120-seed81137_81138-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-floa-h062c4f3957dc21a0.md` |
| Row log | Present: `docs/benchmarks/logs/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23-b2-t20-n3072-r16-eps0p25-a1em08-it120-seed81137_81138-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-floa-h062c4f3957dc21a0.log` |
| Local artifact consistency check | Passed |
| Local syntax check | Passed |
| Focused grid tests | `18 passed` |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | `python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode execute --route both --batch-seeds 81137,81138 --time-steps 20 --num-particles 3072 --low-rank-ranks 16 --low-rank-assignment-epsilons 0.25,0.125 --low-rank-max-projection-iterations-list 120 --candidate-ids r16_eps0p25_alpha1em08_it120 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --jit-compile --row-timeout-seconds 7200 --output docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.md` |
| Environment | Python `3.13.13`, TensorFlow `2.20.0`, active TensorFlow GPU environment |
| GPU/CPU status | Trusted GPU execution on GPU 1, NVIDIA GeForce RTX 4080 SUPER, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`; CPU-only was not used |
| Seeds | `81137,81138` |
| Shape | batch `2`, time steps `20`, particles `3072`, state dim `18`, obs dim `9` |
| Dtype/TF32 | `float32`, TF32 enabled |
| Timing source | streaming `compiled_core`, low-rank `compiled_core`, `jit_compile=True` |
| Wall time | aggregate wall time `397.0012169149704s`; row wall time `396.94959120010026s` |
| Aggregate `plan_path` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-master-program-2026-06-22.md` |
| Governing phase subplan | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-representative-resource-smoke-subplan-2026-06-23.md` |
| Result file | this file |

The grid runner's aggregate `plan_path` field records the broader tuning master
program because the runner does not accept a per-phase subplan path argument.
The dedicated N3072 resource-smoke subplan governed the current phase through
the visible execution/review protocol and is preserved here as the phase plan
artifact.

## Post-Run Red-Team Note

The strongest alternative explanation is that the N3072 pass demonstrates only
that one representative row completed under this exact GPU, seed batch, shape,
candidate id, and harness state. It does not establish that the second
rank-16 candidate will complete at N3072, that N4096 will fit, that memory
behavior is stable, or that timing differences are stable. Larger or broader
paired runs should be treated as resource-risky until a separate reviewed
runtime plan pins stop conditions, artifact expectations, and human/resource
approval boundaries.

## Handoff

Proceed to a local N3072 resource-boundary closeout subplan before any further
GPU execution:

`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-resource-boundary-closeout-subplan-2026-06-23.md`
