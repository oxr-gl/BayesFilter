# P06 P09 Repair Gate And Decision Subplan

Date: 2026-06-23

Status: `READY_FOR_SERIOUS_GPU_REPAIR_GATE`

## Phase Objective

Test whether the opt-in `positive_projected` Nystrom kernel diagnostic rescues
the known failing rows while preserving the viable control, then decide whether
to rerun P09 sensitivity or stop.

## Entry Conditions Inherited From Previous Phase

- P05 focused tests passed.
- Repair configuration is fixed before serious GPU execution:
  `--nystrom-kernel-mode positive_projected`.
- Raw/default behavior remains unchanged and is not automatically switched to
  the opt-in mode.

## Required Artifacts

- Paired GPU JSON/Markdown/log artifacts for:
  - `rank=32,epsilon=0.25`
  - `rank=64,epsilon=0.3`
  - `rank=32,epsilon=0.5`
- Per-row run manifest fields: git commit/status, exact command, Python/TensorFlow
  environment, CUDA visibility, selected physical GPU, trusted GPU preflight,
  dtype/TF32/JIT state, seeds, shape, model row, transport policy, log path,
  structured artifact path, wall time, and exit status.
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p06-p09-regate-decision-result-2026-06-23.md`
- Promotion runbook update if repair passes.
- Refreshed P07 closeout subplan.

## Required Checks, Tests, Reviews

- Trusted GPU preflight with GPU1 preferred and GPU0 fallback.
- Bounded artifact summaries after each row.
- Claude read-only review of P06 result before any claim that P09 can reopen.

Required local pre-launch check:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does `--nystrom-kernel-mode positive_projected` rescue failing rows and preserve the control under the original paired thresholds? |
| Baseline/comparator | Compiled streaming TF32 actual-SIR route and pre-repair P09B/P09C/P09D artifacts. |
| Primary pass criterion | All three rows have `status=PASS`, `hard_vetoes=[]`, finite factors/particles/log-likelihood, residuals pass, paired thresholds pass, and `nystrom_kernel_mode="positive_projected"` recorded. |
| Veto diagnostics | Any nonfinite, residual threshold failure, paired threshold failure, missing GPU/TF32/JIT evidence, control regression, missing `positive_projected` metadata, or zero projection floor hits in both failing rows. |
| Explanatory diagnostics | Runtime, warm ratios, spectra, denominator stats, projection floor hits, raw/projected kernel minima, per-seed deltas. |
| Not concluded | No default readiness, no ranking, no posterior correctness, no HMC readiness. |
| Artifacts | Row artifacts, P06 result, Claude review, promotion runbook update if applicable. |

## Exact Command Template

Use the trusted GPU selection protocol from the visible runbook.  Try GPU1 if
available; otherwise use GPU0 and record the fallback reason.

Replace `<GPU>`, `<NOTE>`, `<RANK>`, `<EPS>`, `<PHASE>`, `<JSON>`, `<MD>`, and
`<LOG>`:

```bash
timeout 1800 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds 81920,81921,81922,81923,81924 --time-steps 20 --num-particles 1024 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <GPU> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <GPU> --gpu-selection-note '<NOTE>' --quiet --nystrom-diagnostics --nystrom-kernel-mode positive_projected --nystrom-rank <RANK> --nystrom-epsilon <EPS> --phase-id <PHASE> --output <JSON> --markdown-output <MD> > <LOG> 2>&1
```

Rows:

| Row | Rank | Epsilon | Phase | JSON |
| --- | ---: | ---: | --- | --- |
| failing row 1 | `32` | `0.25` | `p06-positive-projected-r32-eps0p25` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p06-positive-projected-r32-eps0p25-2026-06-23.json` |
| failing row 2 | `64` | `0.3` | `p06-positive-projected-r64-eps0p3` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p06-positive-projected-r64-eps0p3-2026-06-23.json` |
| control | `32` | `0.5` | `p06-positive-projected-r32-eps0p5-control` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p06-positive-projected-r32-eps0p5-control-2026-06-23.json` |

Stop after the first hard-veto failure only if the artifact is valid and the
failure is not a runtime/artifact blocker.  If the first failing row passes,
continue automatically to the second failing row; if both pass, continue
automatically to the control.

## Forbidden Claims And Actions

- Do not continue to P10 automatically unless P06 explicitly reopens P09/P10
  gates and the promotion runbook is updated.
- Do not relax paired thresholds after observing results.
- Do not treat one repaired row as broad robustness.
- Do not claim scalable/high-N readiness from the dense diagnostic
  `positive_projected` mode.
- Do not change rank, epsilon, seed batch, dtype, TF32/JIT, residual thresholds,
  paired thresholds, or transport policy after observing row outcomes.

## Exact Next-Phase Handoff Conditions

Advance to P07 closeout if:

- P06 passes, fails, or blocks with clear result.
- P07 subplan names final status and required handoff updates.

If P06 passes, the next scientific action is rerun full P09 sensitivity under a
new reviewed subplan, not immediate default promotion.

## Stop Conditions

- Any hard veto in a required row.
- Missing artifact or trusted GPU evidence.
- Any required row missing `nystrom_kernel_mode="positive_projected"` metadata.
- Both known failing rows have zero projection floor hits, because that would
  show the selected repair path was not exercised on the target failure surface.
- Review non-convergence after five rounds.

## End-Of-Subplan Required Actions

1. Run required local checks/GPU preflight.
2. Write P06 result/close record.
3. Draft or refresh P07 subplan.
4. Review P07 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
