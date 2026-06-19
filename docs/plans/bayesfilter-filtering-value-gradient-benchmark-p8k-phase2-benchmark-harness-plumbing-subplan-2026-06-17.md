# P8k Phase 2 Subplan: Benchmark Harness Plumbing

metadata_date: 2026-06-17
status: DRAFT
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md
phase: 2

## Phase Objective

Expose generic configuration knobs consistently in benchmark harnesses and
result metadata without changing the engine defaults.  Phase 2 must explicitly
repair the actual-SIR harness gap identified in Phase 1: actual-SIR must expose
an opt-in value-only/history-output mode, or equivalent diagnostic-level knob,
and must record the selected mode in output metadata.

## Entry Conditions Inherited From Previous Phase

- Phase 1 has a reviewed configuration contract.
- Implementation scope is limited to generic harness plumbing and metadata.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-benchmark-harness-plumbing-result-2026-06-17.md`
- Focused JSON/markdown smoke artifacts for the required CPU-only harness
  smokes.

## Required Checks/Tests/Reviews

```bash
python -m py_compile docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py --device-scope cpu --expect-device-kind cpu --batch-size 1 --time-steps 2 --num-particles 8 --state-dim 4 --obs-dim 2 --transport-policy no-resampling --return-history --warmups 0 --repeats 1 --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-lgssm-harness-smoke-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-lgssm-harness-smoke-2026-06-18.md
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --device-scope cpu --expect-device-kind cpu --batch-seeds 81120 --time-steps 2 --num-particles 8 --transport-policy no-resampling --history-mode value-only --warmups 0 --repeats 1 --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-actual-sir-harness-smoke-value-only-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-actual-sir-harness-smoke-value-only-2026-06-18.md
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --device-scope cpu --expect-device-kind cpu --batch-seeds 81120 --time-steps 2 --num-particles 8 --transport-policy no-resampling --history-mode full --warmups 0 --repeats 1 --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-actual-sir-harness-smoke-full-history-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-actual-sir-harness-smoke-full-history-2026-06-18.md
git diff --check -- docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-*
```

Use CPU-only smoke commands intentionally for this phase.  GPU profiling is
deferred to Phase 5.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the harnesses expose and record generic knobs consistently with the Phase 1 configuration contract? |
| Baseline/comparator | Phase 1 configuration-surface contract. Existing P8j actual-SIR and LGSSM harness behavior is preserved only where Phase 1 says to preserve the current default. |
| Primary criterion | Pycompile and CPU-only smoke commands pass; actual-SIR exposes and records value-only/history-output mode; all artifacts record selected generic configuration. |
| Veto diagnostics | Missing metadata for a knob; actual-SIR artifact cannot prove selected history/value-only mode; changed default without review; GPU command run unintentionally; SIR-only logic introduced outside the harness adapter. |
| Explanatory diagnostics | Smoke runtime and output shape. |
| Not concluded | No GPU speedup, no particle adequacy, no leaderboard readiness. |

## Forbidden Claims/Actions

- Do not run GPU profiling in Phase 2.
- Do not edit the core engine except for metadata needed by reviewed Phase 1.
- Do not change default benchmark semantics without a documented opt-in flag.
- Do not treat actual-SIR value-only mode as a scientific or performance claim;
  it is harness plumbing until Phase 5 trusted-GPU profiling.

## Exact Next-Phase Handoff Conditions

Phase 3 may proceed only if harness smoke checks pass and the Phase 2 result
lists the exact changed files and knobs.  The Phase 2 result must include the
actual-SIR selected history/value-only metadata field observed in both required
CPU smoke artifacts.

## Stop Conditions

Stop if a harness cannot expose a generic knob without SIR-specific logic, or
if CPU-only smoke fails for reasons unrelated to the edited harness.  Also stop
if the emitted smoke artifacts do not prove the selected generic knobs,
especially actual-SIR history/value-only mode, were recorded.
