# P03 End-To-End Actual-SIR Benchmark Gate Result

Date: 2026-06-24

Status: `PASS_P03_READY_FOR_P04_REVIEW`

## Phase Objective

Run the approved trusted-GPU actual-SIR d18 N3072 paired benchmark gate for
locked candidate `r16_eps0p25_alpha1em08_it120` against the current streaming
GPU/TF32 comparator, preserving paired seeds, compiled-core timing, hard-veto
diagnostics, whole-row wall time, route provenance, and boundary-safe
interpretation.

## Entry Conditions

- P00 governance close record passed.
- P01 evidence/default-surface audit close record passed.
- P02 implementation/no-NumPy audit close record passed.
- P03 subplan review converged with Claude Opus/max read-only review.
- User approved P03 trusted GPU runtime after review convergence.

## Skeptical Pre-Run Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: P03 uses `--route both` so streaming and low-rank rows share seeds, shape, dtype, TF32 mode, device scope, and timing contract. |
| Proxy metric promoted | Guarded: timing is descriptive only and cannot promote, reject, or default the candidate in P03. |
| Missing stop conditions | Guarded by GPU, dry-run/path-length, timeout, artifact, hard-veto, provenance, and boundary stop conditions. |
| Unfair comparison | Guarded: the benchmark harness creates paired comparator/candidate rows under one request signature. |
| Hidden assumptions | Guarded: candidate `r16_eps0p25_alpha1em08_it120` is locked and no fallback substitution is allowed after seeing results. |
| Stale context | Guarded: P03 starts from the P02 close record and reruns focused checks before interpretation. |
| Environment mismatch | Guarded by trusted `nvidia-smi`, explicit CUDA ordinal, `--expect-device-kind gpu`, and GPU/TF32 artifact provenance. |
| Artifact mismatch | Guarded by aggregate JSON/Markdown, child rows/logs, validator, result note, ledgers, and P04 draft. |

Conclusion: the P03 plan remains executable after user approval.

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
- Pre-run state: `18/32760 MiB`, `0%` utilization, `36 C`, `16.17 W`
- Reason: GPU 1 is present and materially less busy than GPU 0, while matching
  the P03 subplan preference for physical GPU 1 when suitable.

Comparator GPU state recorded for context:

- GPU 0 UUID `GPU-a008e90f-259e-df57-7988-63b6831fff68`: `1604/32760 MiB`,
  `19%` utilization, `73 C`, `79.17 W`.

## Evidence Contract

- Question: under a fresh trusted-GPU actual-SIR d18 N3072 paired benchmark,
  does the locked low-rank candidate remain viable and provide end-to-end
  performance evidence strong enough to continue default-certification?
- Baseline/comparator: current streaming GPU/TF32 actual-SIR route in the same
  `--route both` run.
- Primary pass criterion: aggregate and row artifacts pass all hard vetoes,
  actual-SIR semantics, paired comparability, low-rank provenance, GPU/TF32
  provenance, route-fired/nonmaterialization checks, and preserve whole-row wall
  time and warm-call timing summaries.
- Veto diagnostics: trusted GPU unavailable; dry-run path-length failure; row
  timeout; nonzero benchmark exit; missing/corrupt artifacts; hard vetoes;
  actual-SIR semantics failure; paired comparability failure; route invocation
  mismatch; dense materialization; missing GPU/TF32 provenance; unsupported
  default/scientific/HMC claim.
- Explanatory diagnostics: first-call time, warm-call timings, whole-row wall
  time, memory snapshots, log-likelihood deltas, filtered mean/variance deltas,
  ESS, residual magnitudes, projection iterations, warnings, and filename
  lengths.
- Not concluded: default readiness, statistical superiority, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API readiness,
  N4096 feasibility, formal memory scaling, production readiness, or scientific
  validity.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Pending |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p03-end-to-end-benchmark-subplan-2026-06-24.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p03-end-to-end-benchmark-result-2026-06-24.md` |
| Aggregate JSON | `docs/benchmarks/actual-sir-low-rank-default-certification-p03-end-to-end-2026-06-24.json` |
| Aggregate Markdown | `docs/benchmarks/actual-sir-low-rank-default-certification-p03-end-to-end-2026-06-24.md` |
| Environment | Pending |
| CPU/GPU status | GPU selected: physical CUDA `1`, visible TensorFlow `/GPU:0`, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| Data version | Synthetic actual-SIR harness, no external data |
| Random seeds | `81141,81142` |
| Command | Dry-run and execute records below |
| Wall time | Aggregate wall `397.84828382497653` seconds; child row wall `387.6884493001271` seconds |
| Output artifact paths | Aggregate JSON/Markdown, child row JSON/Markdown/log listed above |

## Required Checks

- Skeptical pre-run audit: passed, no material flaw found.
- Trusted GPU precheck: passed.
- GPU selection: physical CUDA ordinal `1`, UUID
  `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`.
- Syntax check:
  `python -m py_compile docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: passed.
- Focused tests:
  `python -m pytest tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: passed, `23 passed`.
  - Warnings: TensorFlow Probability/gast Python deprecation warnings only.
- Dry-run/path-length gate:
  - Result: passed.
  - Aggregate status/mode: `DRY_RUN` / `dry-run`.
  - Candidate row count: `1`.
  - Largest generated path component: `255` characters.
  - Command included `--jit-compile` and `--cuda-visible-devices 1`.
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
  - Interpretation: these warnings are reporting metadata caveats, not P03 hard
    vetoes, because the phase id, command, output artifact names, execution
    ledger, and this result identify the current P03 default-certification gate.

## Benchmark Result

Command:

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode execute --route both --candidate-ids r16_eps0p25_alpha1em08_it120 --batch-seeds 81141,81142 --time-steps 20 --num-particles 3072 --transport-policy active-all --low-rank-ranks 16 --low-rank-assignment-epsilons 0.25 --low-rank-alphas 1e-8 --low-rank-max-projection-iterations-list 120 --low-rank-convergence-threshold 1e-6 --low-rank-denominator-floor 1e-30 --streaming-timing-source compiled_core --low-rank-timing-source compiled_core --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --device /GPU:0 --expect-device-kind gpu --cuda-visible-devices 1 --jit-compile --phase-id-prefix ACTUAL-SIR-LR-DEFAULT-P03 --row-timeout-seconds 1200 --output docs/benchmarks/actual-sir-low-rank-default-certification-p03-end-to-end-2026-06-24.json --markdown-output docs/benchmarks/actual-sir-low-rank-default-certification-p03-end-to-end-2026-06-24.md --quiet
```

Aggregate:

- Status: `PASS`
- Mode: `execute`
- Candidate label: `freeze-nominated`
- Candidate: `r16_eps0p25_alpha1em08_it120`
- Shape: `B=2`, `T=20`, `N=3072`, `D=18`, `M=9`
- Seeds: `81141,81142`
- Aggregate wall time: `397.84828382497653` seconds
- Child row wall time: `387.6884493001271` seconds

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
| streaming | `216.56467499095015` | `6.769766104524024` | `6.764694652985781`, `6.774837556062266` | `0.6257693370183309` | `9.5367431640625e-07` | `[]` |
| low_rank | `148.73629216197878` | `0.6633626661496237` | `0.6539835291914642`, `0.6727418031077832` | `0.6257693370183309` | `9.5367431640625e-07` | `[]` |

Paired diagnostics:

| Metric | Value | Threshold |
| --- | ---: | ---: |
| `log_likelihood_mean_abs_delta` | `0.118499755859375` | `5.0` |
| `log_likelihood_max_abs_delta` | `0.13641357421875` | `10.0` |
| `filtered_mean_relative_l2` | `0.00011509658020761563` | `0.2` |
| `filtered_mean_rms` | `0.01960821680725705` | `2.5` |
| `filtered_variance_relative_l2` | `0.008207319939360727` | `0.75` |
| `filtered_variance_rms` | `0.010462244676018811` | `25.0` |
| `final_particle_mean_relative_l2` | `0.00024503494159076563` | `0.2` |
| `final_particle_mean_abs_l2` | `0.041911805131948365` | `25.0` |
| `warm_median_streaming_over_low_rank` | `10.205226266075517` | descriptive in P03 |

Low-rank route diagnostics:

- `max_factor_marginal_residual`: `2.2351741790771484e-08`
- `max_induced_row_residual`: `5.960464477539062e-07`
- `max_induced_column_residual`: `2.86102294921875e-06`
- `projection_iterations_used_max_explanatory`: `13.0`
- `transport_object_kind`: `low_rank_coupling_factors`
- Source route component classifications include `source_faithful`,
  `fixed_hmc_adaptation`, and `extension_or_invention`; this P03 result does
  not claim Zhao-Cui source-faithfulness or HMC readiness.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | P03 passes the end-to-end actual-SIR N3072 hard-veto/runtime-viability gate and should hand off to P04 N4096 resource-boundary review |
| Primary criterion status | Passed: artifacts preserve actual-SIR semantics, paired comparability, low-rank provenance, GPU/TF32/XLA provenance, route-fired evidence, nonmaterialization evidence, row wall time, and route warm timing summaries |
| Veto diagnostic status | No hard veto, timeout, nonzero exit, route mismatch, dense materialization, paired comparability failure, missing GPU/TF32 provenance, or unsupported default/scientific/HMC claim was found |
| Main uncertainty | One fresh seed batch cannot establish statistical superiority or default readiness; legacy harness `plan_path` constants should be repaired in a later implementation/reporting phase |
| Next justified action | Draft and review P04 N4096 resource-boundary subplan; ask for separate approval before P04 trusted GPU runtime |
| What is not being concluded | No default readiness, statistical superiority, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API readiness, N4096 feasibility, formal memory scaling, production readiness, or scientific validity |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the P03 N3072 paired actual-SIR benchmark |
| Statistically supported ranking | None; only one fresh seed batch was added |
| Descriptive-only differences | Low-rank warm median was `0.6633626661496237` seconds versus streaming `6.769766104524024` seconds, ratio `10.205226266075517`; this is favorable but descriptive only |
| Default-readiness | Not certified; P04 resource-boundary, P05 default-surface/code gate, and final P07 review remain open |
| Next evidence needed | Reviewed P04 N4096 resource-boundary feasibility or a reviewed resource-boundary blocker |

## Post-Run Red-Team Note

The strongest alternative explanation is that P03 confirms this benchmark row
and candidate configuration, not broad default readiness. The timing result is
descriptively favorable for LEDH transport on this N3072 actual-SIR gate, but it
has only two warm repeats and one fresh seed batch. The stale harness
`plan_path` constants also show that reporting metadata needs cleanup before a
default implementation phase, even though the P03 command and artifacts are
otherwise phase-specific.

A result that would overturn the P03 continuation decision would be a failed
P04 resource-boundary run, a discovered artifact/provenance bug that invalidates
the P03 row, or a focused review showing the low-rank route used a forbidden
implementation path.

## Next-Phase Handoff

Draft and review:

`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p04-n4096-resource-boundary-subplan-2026-06-24.md`

P04 trusted GPU runtime is not authorized by this P03 result. It requires the
P04 subplan to converge and separate human approval for the P04 runtime gate.
