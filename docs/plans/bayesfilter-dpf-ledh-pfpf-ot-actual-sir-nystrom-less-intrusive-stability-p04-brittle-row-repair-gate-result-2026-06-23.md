# P04 Known Brittle Row Repair Gate Result

Date: 2026-06-23

Status: `P04_VALID_CANDIDATE_FAILURE_ROUTE_TO_P06`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Reject opt-in balanced scaling normalization as a successful repair for the original brittle row | `FAIL`: aggregate artifact status is `FAIL` | `FAIL`: Nystrom row produced nonfinite log likelihood, nonfinite factors, and nonfinite particles | This rejects the current candidate on the original brittle row; it does not by itself prove all less-intrusive repairs are impossible | Skip P05 and route to P06 candidate-failure classification / closeout decision | No default readiness, no ranking, no posterior correctness, no HMC readiness, no claim that the whole research direction is invalid |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Does the selected less-intrusive repair pass the original brittle row without breaking paired comparability? |
| Baseline/comparator | Compiled streaming TF32 comparator in the same artifact; raw and positive-projection prior evidence for context only. |
| Primary pass criterion | `FAIL`: aggregate artifact status was `FAIL`. |
| Veto diagnostics | `FAIL`: `nystrom:nonfinite_log_likelihood`, `nystrom:nonfinite_nystrom_factors`, `nystrom:nonfinite_nystrom_particles`. |
| Explanatory diagnostics | Balanced scaling metadata was present; denominator floor hits were present; scaling/gauge diagnostics became nonfinite. |
| Not concluded | No default readiness, no ranking, no HMC readiness, no broad impossibility claim. |
| Artifact preserving result | P04 JSON/Markdown/log and this result file. |

## Command And Artifacts

Trusted GPU preflight selected physical GPU1:

```text
0, NVIDIA GeForce RTX 4080 SUPER, 1463 MiB used / 32760 MiB, 39% utilization
1, NVIDIA GeForce RTX 4080 SUPER, 18 MiB used / 32760 MiB, 0% utilization
```

Command:

```bash
python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds 81920,81921,81922,81923,81924 --time-steps 20 --num-particles 1024 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.25 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-kernel-mode raw --nystrom-scaling-normalization balanced --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu 1 --gpu-selection-note "GPU1 selected by P04 trusted preflight: 18 MiB used of 32760 MiB, 0 percent utilization; GPU0 had 1463 MiB used and 39 percent utilization" --phase-id ACTUAL-SIR-NYSTROM-LESS-INTRUSIVE-STABILITY-P04-R32-EPS0P25 --quiet --output docs/benchmarks/actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.md
```

Artifacts:

- JSON: `docs/benchmarks/actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.md`
- Log: `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.log`

## Result Summary

Aggregate status: `FAIL`.

Aggregate hard vetoes:

- `nystrom:nonfinite_log_likelihood`;
- `nystrom:nonfinite_nystrom_factors`;
- `nystrom:nonfinite_nystrom_particles`.

Streaming comparator:

- status: `PASS`;
- output device: `/device:GPU:0` inside process, with physical GPU1 selected;
- log likelihoods:
  `[-902.23779296875, -901.313720703125, -901.726806640625, -902.2744140625, -900.0975952148438]`.

Nystrom candidate:

- status: `FAIL`;
- output device: `/device:GPU:0` inside process, with physical GPU1 selected;
- log likelihoods:
  `[-902.5842895507812, nan, -902.0941772460938, -902.8893432617188, nan]`;
- `finite_factors`: `False`;
- `finite_particles`: `False`;
- `max_row_residual`: `nan`;
- `max_column_residual`: `nan`;
- `nystrom_kernel_mode`: `raw`;
- `nystrom_scaling_normalization`: `balanced`;
- `nystrom_rank`: `32`;
- `nystrom_epsilon`: `0.25`;
- `iterations_used_max`: `160`;
- `route_invocations`: `20`;
- `min_kernel_denominator`: `nan`;
- `denominator_floor_hits`: `1178.0`;
- `max_abs_log_scaling_gauge_shift`: `nan`;
- `scaling_normalization_applications`: `14130.0`;
- `scaling_u_min`, `scaling_u_max`, `scaling_v_min`, `scaling_v_max`: all `nan`;
- `landmark_core_effective_rank_min`: `0.0`.

Paired comparability was not interpretable because Nystrom produced nonfinite
log likelihoods:

- deltas: `[-0.34649658203125, nan, -0.36737060546875, -0.61492919921875, nan]`;
- max absolute delta: `nan`;
- mean absolute delta: `nan`.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu`; TensorFlow GPU run |
| GPU status | Trusted GPU; physical GPU1 selected; process visible device `/GPU:0` |
| CUDA_VISIBLE_DEVICES | `1` |
| TF32 | Enabled and recorded true for float32 |
| Dtype | `float32` |
| Shape | batch seeds `81920..81924`, `T=20`, `N=1024` |
| Wall time | `38.44749143300578` seconds |
| Started | `2026-06-23T06:51:54.627277+00:00` |
| Ended | `2026-06-23T06:52:33.074826+00:00` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-brittle-row-repair-gate-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-brittle-row-repair-gate-result-2026-06-23.md` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `FAIL`: nonfinite Nystrom log likelihood, factors, and particles. |
| Statistically supported ranking | `NO`. |
| Descriptive-only differences | Runtime and finite per-seed deltas are descriptive only and not interpretable as a ranking after hard veto failure. |
| Default-readiness | `NO`. |
| Next evidence needed | P06 classification: decide whether the balanced repair lane should close, restrict policy to the known viable fixed row, or draft a bounded return-to-P02 repair loop. |

## Post-Run Red Team

Strongest alternative explanation: the balanced gauge transform may have
amplified a deeper raw low-rank-kernel pathology instead of stabilizing it, as
shown by nonfinite factors/particles and `landmark_core_effective_rank_min=0.0`.

What would overturn this P04 decision: a reproducible artifact showing the same
command and selected metadata pass finite-factor, finite-particle, residual, and
paired thresholds without changing thresholds or target row.  No such artifact
exists in this lane.

Weakest part of evidence: this is one predeclared brittle row, not a full
repair-family impossibility proof.

## Next Action

Do not run P05 because P04 hard-vetoed.  Route to P06 for candidate-failure
classification and next-loop/closeout decision.
