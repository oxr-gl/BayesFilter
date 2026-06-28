# P04 N4096 Resource-Boundary Feasibility Result

Date: 2026-06-24

Status: `PASS_P04_READY_FOR_P05_REFRESH_AND_APPROVAL`

## Phase Objective

Run the approved trusted-GPU actual-SIR d18 N4096 paired resource-boundary gate
for locked candidate `r16_eps0p25_alpha1em08_it120` against the current
streaming GPU/TF32 comparator, preserving paired seeds, compiled-core timing,
hard-veto diagnostics, whole-row wall time, route provenance, and boundary-safe
interpretation.

## Entry Conditions

- P00 governance close record passed.
- P01 evidence/default-surface audit close record passed.
- P02 implementation/no-NumPy audit close record passed.
- P03 end-to-end actual-SIR N3072 benchmark result passed.
- P04 subplan review converged with Claude Opus/max read-only review.
- User approved continuing the run after the P04 approval boundary was
  explained; this approval is interpreted as P04 trusted GPU runtime approval
  only.

## Skeptical Pre-Run Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: P04 uses `--route both` so streaming and low-rank rows share seeds, shape, dtype, TF32 mode, device scope, and timing contract. |
| Proxy metric promoted | Guarded: timing is descriptive only and cannot promote, reject, or default the candidate in P04. |
| Missing stop conditions | Guarded by GPU, dry-run/path-length, timeout, artifact, hard-veto, provenance, and boundary stop conditions. |
| Unfair comparison | Guarded: the benchmark harness creates paired comparator/candidate rows under one request signature. |
| Hidden assumptions | Guarded: candidate `r16_eps0p25_alpha1em08_it120` is locked and no fallback substitution is allowed after seeing results. |
| Stale context | Guarded: P04 starts from the P03 close record and reruns focused checks before interpretation. |
| Environment mismatch | Guarded by trusted `nvidia-smi`, explicit CUDA ordinal, `--expect-device-kind gpu`, and GPU/TF32 artifact provenance. |
| Artifact mismatch | Guarded by aggregate JSON/Markdown, child rows/logs, validator, result note, ledgers, and P05/P06/P07 provisional drafts. |

Conclusion: the P04 plan remains executable after user approval.

## Trusted GPU Selection

Command:

```bash
nvidia-smi
nvidia-smi --query-gpu=index,uuid,name,memory.used,memory.total,utilization.gpu,temperature.gpu,power.draw --format=csv,noheader,nounits
```

Selection:

- Physical CUDA ordinal: `1`
- Visible TensorFlow device requested by benchmark: `/GPU:0`
- UUID: `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`
- Name: `NVIDIA GeForce RTX 4080 SUPER`
- Pre-run state: `18/32760 MiB`, `0%` utilization, `37 C`, `16.21 W`
- Reason: GPU 1 is present and materially less busy than GPU 0, while matching
  the P04 subplan preference for physical GPU 1 when suitable.

Comparator GPU state recorded for context:

- GPU 0 UUID `GPU-a008e90f-259e-df57-7988-63b6831fff68`: `1559/32760 MiB`,
  `34%` utilization, `89 C`, `84.66 W`.

## Evidence Contract

- Question: under a trusted-GPU actual-SIR d18 N4096 paired benchmark, does the
  locked low-rank candidate remain feasible and valid enough to continue toward
  bounded default-readiness review?
- Baseline/comparator: current streaming GPU/TF32 actual-SIR route in the same
  `--route both` run.
- Primary pass criterion: aggregate and row artifacts pass all hard vetoes,
  actual-SIR semantics, paired comparability, low-rank provenance, GPU/TF32
  provenance, route-fired/nonmaterialization checks, and preserve whole-row wall
  time and warm-call timing summaries.
- Veto diagnostics: P04 approval absent; trusted GPU unavailable; dry-run
  path-length failure; row timeout; nonzero benchmark exit; missing/corrupt
  artifacts; hard vetoes; actual-SIR semantics failure; paired comparability
  failure; route invocation mismatch; dense materialization; missing GPU/TF32
  provenance; unsupported default/scientific/HMC claim.
- Explanatory diagnostics: first-call time, warm-call timings, whole-row wall
  time, memory snapshots, log-likelihood deltas, filtered mean/variance deltas,
  ESS, residual magnitudes, projection iterations, warnings, and filename
  lengths.
- Not concluded: default readiness, statistical superiority, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API readiness,
  formal memory scaling, production readiness, or scientific validity.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p04-n4096-resource-boundary-subplan-2026-06-24.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p04-n4096-resource-boundary-result-2026-06-24.md` |
| Aggregate JSON | `docs/benchmarks/actual-sir-low-rank-default-certification-p04-n4096-resource-boundary-2026-06-24.json` |
| Aggregate Markdown | `docs/benchmarks/actual-sir-low-rank-default-certification-p04-n4096-resource-boundary-2026-06-24.md` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` |
| CPU/GPU status | GPU selected: physical CUDA `1`, visible TensorFlow `/GPU:0`, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| Data version | Synthetic actual-SIR harness, no external data |
| Random seeds | `81143,81144` |
| Command | Dry-run and execute records below |
| Wall time | Aggregate wall `416.97745982697234` seconds; child row wall `407.36601978284307` seconds |
| Output artifact paths | Aggregate JSON/Markdown, child row JSON/Markdown/log listed above |

## Required Checks

- Provisional P05/P06/P07 subplan consistency scan:
  - Result: passed, `errors=[]`.
- P04 trusted GPU precheck:
  - Result: passed.
  - Selected physical CUDA `1`, UUID
    `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`.
- Dry-run/path-length gate:
  - Result: passed.
  - Aggregate status/mode: `DRY_RUN` / `dry-run`.
  - Candidate row count: `1`.
  - Largest generated path component: `255` characters.
  - Command included `--jit-compile`, `--cuda-visible-devices 1`, and
    `--num-particles 4096`.
- Execute gate:
  - Result: passed, benchmark command exited `0`.
  - Aggregate status/mode: `PASS` / `execute`.
- Strict artifact validator:
  - Result: passed, `errors=[]`.
  - Metadata warnings:
    - aggregate `plan_path` is the legacy harness constant
      `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-master-program-2026-06-22.md`;
    - child row manifest `plan_path` is the legacy harness constant
      `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-master-program-2026-06-21.md`.
  - Interpretation: these are known reporting metadata caveats, not P04 hard
    vetoes. The command, phase id, output artifact names, execution ledger, and
    this result identify the current P04 default-certification gate.

## Benchmark Result

Command:

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode execute --route both --candidate-ids r16_eps0p25_alpha1em08_it120 --batch-seeds 81143,81144 --time-steps 20 --num-particles 4096 --transport-policy active-all --low-rank-ranks 16 --low-rank-assignment-epsilons 0.25 --low-rank-alphas 1e-8 --low-rank-max-projection-iterations-list 120 --low-rank-convergence-threshold 1e-6 --low-rank-denominator-floor 1e-30 --streaming-timing-source compiled_core --low-rank-timing-source compiled_core --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --device /GPU:0 --expect-device-kind gpu --cuda-visible-devices 1 --jit-compile --phase-id-prefix ACTUAL-SIR-LR-DEFAULT-P04 --row-timeout-seconds 1800 --output docs/benchmarks/actual-sir-low-rank-default-certification-p04-n4096-resource-boundary-2026-06-24.json --markdown-output docs/benchmarks/actual-sir-low-rank-default-certification-p04-n4096-resource-boundary-2026-06-24.md --quiet
```

Aggregate:

- Status: `PASS`
- Mode: `execute`
- Candidate label: `freeze-nominated`
- Candidate: `r16_eps0p25_alpha1em08_it120`
- Shape: `B=2`, `T=20`, `N=4096`, `D=18`, `M=9`
- Seeds: `81143,81144`
- Aggregate wall time: `416.97745982697234` seconds
- Child row wall time: `407.36601978284307` seconds

Hard-veto and provenance checks:

| Check | Status |
| --- | --- |
| Aggregate status | Passed |
| Child row status | Passed |
| Hard vetoes | Passed: `[]` |
| Actual-SIR semantics | Passed |
| Paired comparability | Passed under declared thresholds |
| Low-rank provenance | Passed |
| GPU/TF32 provenance | Passed |
| XLA/JIT | Passed: `jit_compile=True`, log records XLA compilation |
| Selected GPU | Passed: physical CUDA `1`, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| Route-fired evidence | Passed: `20` route invocations and `20` active resampling steps |
| Dense materialization | Passed: both routes report `transport_matrix_materialized=False` and shape `[[2, 0, 0]]` |

Route metrics:

| Route | First call seconds | Warm median seconds | Warm calls | ESS fraction min | Final logsumexp residual | Hard vetoes |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| streaming | `219.03653532313183` | `11.6201760196127` | `11.619981643045321`, `11.620370396180078` | `0.6359876394271851` | `0.0` | `[]` |
| low_rank | `150.76937992707826` | `0.8781711575575173` | `0.8731793139595538`, `0.8831630011554807` | `0.6359876394271851` | `0.0` | `[]` |

Paired diagnostics:

| Metric | Value | Threshold |
| --- | ---: | ---: |
| `log_likelihood_mean_abs_delta` | `0.068206787109375` | `5.0` |
| `log_likelihood_max_abs_delta` | `0.10302734375` | `10.0` |
| `filtered_mean_relative_l2` | `9.199723015520317e-05` | `0.2` |
| `filtered_mean_rms` | `0.01567241683567131` | `2.5` |
| `filtered_variance_relative_l2` | `0.007262945915558883` | `0.75` |
| `filtered_variance_rms` | `0.009320643041934506` | `25.0` |
| `final_particle_mean_relative_l2` | `0.0001785495473223063` | `0.2` |
| `final_particle_mean_abs_l2` | `0.030544091162949764` | `25.0` |
| `warm_median_streaming_over_low_rank` | `13.232245126260159` | descriptive in P04 |

Low-rank route diagnostics:

- `max_factor_marginal_residual`: `1.4901161193847656e-08`
- `max_induced_row_residual`: `6.556510925292969e-07`
- `max_induced_column_residual`: `1.430511474609375e-06`
- `projection_iterations_used_max_explanatory`: `13.0`
- `transport_object_kind`: `low_rank_coupling_factors`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | P04 passes the N4096 resource-boundary hard-veto/runtime-feasibility gate and can hand off to a refreshed P05 default-implementation subplan |
| Primary criterion status | Passed: artifacts preserve actual-SIR semantics, paired comparability, low-rank provenance, GPU/TF32/XLA provenance, route-fired evidence, nonmaterialization evidence, row wall time, and route warm timing summaries |
| Veto diagnostic status | No hard veto, timeout, nonzero exit, route mismatch, dense materialization, paired comparability failure, missing GPU/TF32 provenance, or unsupported default/scientific/HMC claim was found |
| Main uncertainty | P04 is still one N4096 seed batch with two warm repeats; timing is descriptively favorable but not statistical superiority. Legacy harness `plan_path` constants remain a reporting metadata caveat for P05 cleanup consideration |
| Next justified action | Refresh P05 after P04, discover exact default surface, review P05, and request explicit P05 implementation approval before code/default-surface changes |
| What is not being concluded | No final default readiness, statistical superiority, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API readiness, formal memory scaling, production readiness, or scientific validity |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the P04 N4096 paired actual-SIR resource-boundary benchmark |
| Statistically supported ranking | None; only one N4096 seed batch was added |
| Descriptive-only differences | Low-rank warm median was `0.8781711575575173` seconds versus streaming `11.6201760196127` seconds, ratio `13.232245126260159`; this is favorable but descriptive only |
| Default-readiness | Not final-certified; P05 default-surface/code gate and P07 final review remain open |
| Next evidence needed | Refreshed/reviewed P05 implementation/default-surface gate with explicit P05 approval |

## Post-Run Red-Team Note

The strongest alternative explanation is that P04 validates the candidate at a
larger resource boundary in this harness, not broad production readiness. The
descriptive timing is favorable and becomes more favorable at N4096 than P03,
but it is still a small-seed, small-repeat benchmark without uncertainty
analysis. P05 should not treat timing alone as a default switch; it should rely
on the full hard-veto/provenance/resource chain and preserve the streaming
fallback.

The weakest part of the evidence is still reporting metadata hygiene: the
benchmark harness embeds legacy `plan_path` constants. This did not invalidate
P04 because command, phase id, output names, and ledgers are current, but P05
should consider a scoped reporting-metadata cleanup if it touches the harness.

## Next-Phase Handoff

Refresh and review:

`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p05-default-implementation-subplan-2026-06-24.md`

P05 implementation/default-surface changes are not authorized by this P04
result. P05 requires the refreshed subplan to converge and separate explicit
P05 human approval before any implementation action.
