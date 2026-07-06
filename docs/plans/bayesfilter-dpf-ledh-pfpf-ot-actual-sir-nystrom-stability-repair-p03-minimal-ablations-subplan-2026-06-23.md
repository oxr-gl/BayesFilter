# P03 Prefix Localization Subplan

Date: 2026-06-23

Status: `READY_FOR_PREFIX_LOCALIZATION_REVIEW`

## Phase Objective

Run the smallest prefix/first-failure diagnostics needed after P02 before
choosing precision, scaling, landmark, Sinkhorn, or factor-quality ablations.

## Entry Conditions Inherited From Previous Phase

- P02 result is `PASS_AMBIGUOUS_LOCALIZATION_NEEDS_PREFIX_TRACE`.
- P02 artifacts include both failing rows and the control.
- P02 shows the control diagnostics are finite and the failing rows are all-NaN
  in aggregate diagnostics.

## Required Artifacts

- Prefix diagnostic JSON/Markdown/log artifacts under
  `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-*`.
- Per-row run manifest fields for every GPU/CUDA row: git commit/status, exact
  command, Python/TensorFlow environment, CUDA visibility, selected physical
  GPU, trusted GPU preflight, dtype/TF32/JIT state, seeds, shape, model row,
  transport policy, log path, structured artifact path, wall time, and exit
  status.
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p03-minimal-ablations-result-2026-06-23.md`
- Refreshed P04 subplan.
- P03 result must include a per-prefix table with row, prefix `T`, pass/fail,
  hard vetoes, finite factor/core/scaling status, first nonfinite stage if
  available, control status, JSON/Markdown path, and log path.

## Required Checks, Tests, Reviews

- Claude read-only review of this refreshed P03 subplan before launch, because
  P02 produced ambiguous localization and changed the planned ablation set.
- Trusted GPU preflight for GPU rows.
- No local code changes are planned in P03 before the prefix rows.
- Claude read-only review of P03 result if more than one repair family remains
  plausible or if any later ablation changes algorithm semantics.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | At what time prefix does each failing row first become nonfinite, and does the control remain finite at the same prefix? |
| Baseline/comparator | P02 instrumented failing/control rows. |
| Primary pass criterion | P03 brackets the first failing prefix for both known failing rows and verifies the control at the smallest failing prefix and at `T=20`, or records a true artifact/runtime blocker. |
| Veto diagnostics | Multi-knob tuning before prefix localization, changed thresholds after results, missing control at the failing prefix, or treating prefix evidence as promotion. |
| Explanatory diagnostics | Diagnostic summaries by prefix, runtime, memory, finite factor/core/scaling status. |
| Not concluded | No default readiness, no statistical ranking, no final repair approval. |
| Artifacts | Ablation artifacts and P03 result. |

## Exact Command Template

Use this template for each row, replacing `<GPU>`, `<NOTE>`, `<T>`, `<RANK>`,
`<EPS>`, `<PHASE>`, `<JSON>`, `<MD>`, and `<LOG>`:

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds 81920,81921,81922,81923,81924 --time-steps <T> --num-particles 1024 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <GPU> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <GPU> --gpu-selection-note '<NOTE>' --quiet --nystrom-diagnostics --nystrom-rank <RANK> --nystrom-epsilon <EPS> --phase-id <PHASE> --output <JSON> --markdown-output <MD> > <LOG> 2>&1
```

All rows must use seeds `81920,81921,81922,81923,81924`, shape
`B=5,N=1024,D=18,M=9`, `float32`, TF32 enabled, JIT enabled, active-all
transport policy, and the trusted GPU selection protocol from the visible
runbook.  Deviations must be recorded in the P03 result with a justification.

## Planned Prefix Rows

Run with `--nystrom-diagnostics` and the same P09 serious-model condition as P02.

Initial prefix ladder for each failing row:

- `T=1,2,4,8,12,16,20`

Rows:

- `rank=32,epsilon=0.25`
- `rank=64,epsilon=0.3`
- `rank=32,epsilon=0.5` control at the smallest failing prefix observed across
  the failing rows and at `T=20`

For each failing row, stop its ladder once its first failing prefix is
bracketed, defined as one finite/pass prefix followed by one failed prefix, or
`T=1` failing immediately.  If a failing row stays finite through `T=20`, write
that as a repair-relevant contradiction and do not infer rescue without a
rerun/manifest audit.

Only after the prefix result is written may P03 add one of these ablation
families in a patched/reviewed addendum:

- precision: Nystrom-only float64 or TF32-disabled check;
- scaling: scale multiplier probes;
- landmark: deterministic alternative landmarks;
- scaling dynamics: damped or log-domain Sinkhorn prototype;
- factor repair: diagonal/PSD correction diagnostic.

## Forbidden Claims And Actions

- Do not run a broad tuning grid.
- Do not run repair ablations before the prefix diagnostic result is written or
  this subplan is patched and reviewed.
- Do not promote descriptive runtime or spectra to ranking.
- Do not implement a permanent repair in P03.

## Exact Next-Phase Handoff Conditions

Advance to P04 only if:

- P03 result brackets first failing prefix and either selects a repair-family
  diagnostic addendum, fixed-policy path, or blocker.
- P04 subplan states exactly one candidate repair route, a fixed-policy decision
  path, or a blocker-classification path if P03 could not select a repair family.
- Any material ambiguity has Claude read-only review or is explicitly recorded.

## Stop Conditions

- Ablations contradict each other without a smaller discriminating next test.
- Required GPU evidence missing.
- Any ablation requires new scientific or product direction not already
  approved.
- `rank=32,epsilon=0.25` stays finite through `T=20` unless the result records a
  rerun/manifest audit plan.
- The control row fails at the smallest failing prefix unless the result
  records instrumentation/control regression as the primary blocker.
- The two failing rows localize to materially different prefixes or stages
  without a smaller discriminating next test.

## End-Of-Subplan Required Actions

1. Run required local checks.
2. Write P03 result/close record.
3. Draft or refresh P04 subplan.
4. Review P04 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
