# P04 Known Brittle Row Repair Gate Subplan

Date: 2026-06-23

## Phase Objective

Run the first serious trusted GPU repair gate on the known brittle actual-SIR
row: `rank=32,epsilon=0.25`, `N=1024`, `T=20`, seeds `81920..81924`.

## Entry Conditions Inherited From Previous Phase

- P03 implementation passed focused tests.
- Selected repair is opt-in and recorded in harness metadata.
- P04 subplan has exact command, log, JSON, Markdown, and thresholds.
- GPU policy: use GPU1 if available, otherwise GPU0, in trusted context.

## Required Artifacts

- P04 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-brittle-row-repair-gate-result-2026-06-23.md`
- Benchmark JSON:
  `docs/benchmarks/actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.json`
- Benchmark Markdown:
  `docs/benchmarks/actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.md`
- Benchmark log:
  `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.log`
- P05 refreshed subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p05-neighborhood-control-subplan-2026-06-23.md`

## Required Checks, Tests, And Reviews

- Trusted GPU preflight with `nvidia-smi`.
- Select GPU1 if it is usable/available, otherwise GPU0.  Record
  `--selected-physical-gpu` and `--gpu-selection-note` in the command.
- Run compiled actual-SIR benchmark with:
  - route `both`;
  - batch seeds `81920,81921,81922,81923,81924`;
  - `T=20`, `N=1024`;
  - `rank=32`, `epsilon=0.25`;
  - `float32`, TF32 enabled, JIT compiled;
  - GPU1 if available, otherwise GPU0;
  - selected P03 repair mode;
  - diagnostics enabled.
- Exact command shape, after replacing `<GPU_ID>` and `<GPU_NOTE>` from the
  trusted preflight:

```bash
python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py \
  --route both \
  --batch-seeds 81920,81921,81922,81923,81924 \
  --time-steps 20 \
  --num-particles 1024 \
  --transport-policy active-all \
  --sinkhorn-iterations 10 \
  --sinkhorn-epsilon 1.0 \
  --annealed-scaling 0.9 \
  --annealed-convergence-threshold 0.001 \
  --row-chunk-size 1024 \
  --col-chunk-size 1024 \
  --particle-chunk-size 1024 \
  --nystrom-diagnostics \
  --nystrom-rank 32 \
  --nystrom-epsilon 0.25 \
  --nystrom-max-iterations 160 \
  --nystrom-convergence-threshold 0.0001 \
  --nystrom-kernel-mode raw \
  --nystrom-scaling-normalization balanced \
  --history-mode value-only \
  --warmups 0 \
  --repeats 1 \
  --dtype float32 \
  --tf32-mode enabled \
  --jit-compile \
  --device-scope visible \
  --cuda-visible-devices <GPU_ID> \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --selected-physical-gpu <GPU_ID> \
  --gpu-selection-note "<GPU_NOTE>" \
  --phase-id ACTUAL-SIR-NYSTROM-LESS-INTRUSIVE-STABILITY-P04-R32-EPS0P25 \
  --quiet \
  --output docs/benchmarks/actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.json \
  --markdown-output docs/benchmarks/actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.md
```
- Summarize JSON status, hard vetoes, paired deltas, finite flags, residuals,
  and selected repair diagnostics.
- Write P04 result with decision table and inference-status table.
- Claude read-only review is required if P04 passes and would advance to P05,
  or if P04 failure interpretation affects the program direction.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the selected less-intrusive repair pass the original brittle row without breaking paired comparability? |
| Baseline/comparator | Compiled streaming TF32 comparator in the same artifact; raw and positive-projection prior evidence for context only. |
| Primary pass criterion | Aggregate artifact `status == PASS`: finite outputs, no Nystrom residual hard veto, paired max delta <= `10.0`, paired mean delta <= `5.0`, trusted GPU/TF32 evidence present. |
| Veto diagnostics | Any aggregate hard veto, missing GPU evidence, missing selected-repair metadata, nonfinite outputs, row/column residual threshold failure, paired threshold failure, missing artifact. |
| Explanatory diagnostics | Runtime, scaling ranges, denominator floor hits, factor ranges, spectra, selected-repair counters. |
| Not concluded | No default readiness, no ranking, no HMC readiness, no scalable high-N readiness. |
| Artifact preserving result | P04 JSON/Markdown/log and result file. |

## Forbidden Claims And Actions

- Do not change thresholds after seeing results.
- Do not run neighborhood or high-N gates if P04 hard vetoes.
- Do not call finite/residual-only behavior a repair success.
- Do not claim default readiness from one row.
- Do not use `positive_projected` as a promotion repair.

## Exact Next-Phase Handoff Conditions

Advance to P05 only if:

- P04 aggregate status is `PASS`;
- P04 result and benchmark artifacts exist;
- Claude review, if material, returns `VERDICT: AGREE`;
- P05 subplan is refreshed with exact rows and stop rules.

If P04 fails by a repair-effectiveness veto but artifacts are valid, do not
classify it as a continuation blocker.  Route to P06 for failure
classification and next-loop decision.  P06 may close out, recommend fixed
policy, or draft a bounded return-to-P02 repair-selection loop if the failure
is exactly the kind of candidate failure this master program was designed to
repair.

## Stop Conditions

Stop or close out if:

- GPU trusted context is unavailable;
- benchmark artifact is missing or invalid;
- selected repair metadata is missing;
- any P04 hard veto fires in a way that invalidates the harness or artifact;
- continuing would require changing thresholds or target row.

A valid candidate failure with complete artifacts is not by itself a stop
condition; it is routed to P06 classification or the reviewed repair loop.

## Skeptical Plan Audit

Wrong baseline risk: comparing to raw only would miss semantic drift.
Mitigation: route `both` with paired streaming comparator is mandatory.

Proxy risk: finite/residual success might hide likelihood drift.  Mitigation:
paired thresholds are hard vetoes.

Environment risk: sandbox GPU errors could be misleading.  Mitigation: trusted
GPU preflight and artifact device manifest are required.

Audit status: `READY_AFTER_P03_PASS`.
