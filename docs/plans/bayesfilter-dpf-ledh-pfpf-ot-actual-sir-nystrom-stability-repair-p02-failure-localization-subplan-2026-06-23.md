# P02 Failure Localization Diagnostics Subplan

Date: 2026-06-23

Status: `READY_FOR_P02_LAUNCH`

## Phase Objective

Run instrumented diagnostics on the two known failing rows and one viable
control to identify the first failing component: core solve, factor construction,
Sinkhorn scaling, transport, or downstream likelihood.

## Entry Conditions Inherited From Previous Phase

- P01 instrumentation exists.
- Focused CPU-hidden tests passed.
- P01 result confirms default behavior was not changed except for diagnostics.

## Required Artifacts

- JSON/Markdown diagnostics for:
  - `rank=32,epsilon=0.25`:
    - JSON: `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r32-eps0p25-2026-06-23.json`
    - Markdown: `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r32-eps0p25-2026-06-23.md`
    - Log: `docs/plans/logs/actual-sir-nystrom-stability-repair-p02-r32-eps0p25-2026-06-23.log`
  - `rank=64,epsilon=0.3`:
    - JSON: `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r64-eps0p3-2026-06-23.json`
    - Markdown: `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r64-eps0p3-2026-06-23.md`
    - Log: `docs/plans/logs/actual-sir-nystrom-stability-repair-p02-r64-eps0p3-2026-06-23.log`
  - `rank=32,epsilon=0.5`:
    - JSON: `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r32-eps0p5-control-2026-06-23.json`
    - Markdown: `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r32-eps0p5-control-2026-06-23.md`
    - Log: `docs/plans/logs/actual-sir-nystrom-stability-repair-p02-r32-eps0p5-control-2026-06-23.log`
- Log files under `docs/plans/logs/`.
- Per-row run manifest fields: git commit/status, exact command, Python/TensorFlow
  environment, CUDA visibility, selected physical GPU, trusted GPU preflight,
  dtype/TF32/JIT state, seeds, shape, model row, transport policy, log path,
  structured artifact path, wall time, and exit status.
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p02-failure-localization-result-2026-06-23.md`
- Refreshed P03 subplan.

## Required Checks, Tests, Reviews

- Trusted GPU preflight with GPU1 preferred, GPU0 fallback.
- Each GPU command writes full stdout/stderr to a log file.
- Bounded JSON summary after each row.
- Commands must use `--nystrom-diagnostics` and otherwise preserve the P09
  paired serious-model condition:
  `--route both --batch-seeds 81920,81921,81922,81923,81924 --time-steps 20 --num-particles 1024 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --device /GPU:0 --expect-device-kind gpu --quiet`.
- Claude read-only review of P02 result and P03 subplan if localization is
  ambiguous or changes planned ablation set.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Where does the first nonfinite or invalid Nystrom diagnostic appear? |
| Baseline/comparator | P09B/P09C/P09D failing artifacts plus viable `rank=32,epsilon=0.5` control. |
| Primary pass criterion | Diagnostics identify first failing stage or explicitly classify the localization as ambiguous with sufficient artifacts for P03. |
| Veto diagnostics | Missing GPU/TF32 evidence, diagnostics change behavior, missing row artifact, or failure before diagnostic data is written. |
| Explanatory diagnostics | Spectra, condition proxies, factor diagonal min/max/error, denominator minima/hits, first nonfinite seed/time/iteration, runtime. |
| Not concluded | No repair or promotion claim. |
| Artifacts | Row JSON/Markdown/logs and P02 result. |

## Forbidden Claims And Actions

- Do not tune parameters in P02.
- Do not treat diagnostic spectra as pass/fail unless predeclared in P02 result.
- Do not continue to repair implementation before P03/P04 classify a repair
  candidate.

## Exact Next-Phase Handoff Conditions

Advance to P03 only if:

- All three planned rows have artifacts, or P02 result explains a true blocker.
- P02 result names the ablation family or ambiguity that P03 will test.
- P03 subplan is refreshed with exact row list and stop conditions.

## Stop Conditions

- GPU unavailable in trusted context.
- Repeated timeout before any artifact is written.
- Diagnostic instrumentation invalidates default control behavior.
- Human decision required to change rows or criteria after observing results.

## End-Of-Subplan Required Actions

1. Run required local checks or GPU preflight.
2. Write P02 result/close record.
3. Draft or refresh P03 subplan.
4. Review P03 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
