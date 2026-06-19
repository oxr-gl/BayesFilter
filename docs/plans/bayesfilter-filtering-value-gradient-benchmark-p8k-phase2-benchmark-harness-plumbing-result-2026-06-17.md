# P8k Phase 2 Result: Benchmark Harness Plumbing

metadata_date: 2026-06-18
status: PASS_HARNESS_PLUMBING_CPU_SMOKES
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md
phase: 2
executor: Codex
reviewer: Claude Opus max effort, read-only

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Phase 2 harness plumbing passed.  The actual-SIR benchmark now exposes and records `--history-mode {full,value-only}` while preserving `full` as the default; CPU-only smokes passed for LGSSM, actual-SIR value-only, and actual-SIR full-history. |
| Primary criterion status | Passed.  Pycompile, `git diff --check`, CPU-only smokes, and artifact metadata assertions passed. |
| Veto diagnostic status | No active veto.  CPU-only smokes intentionally hid CUDA; actual-SIR artifacts record history mode; CPU artifacts do not claim GPU runtime speedup or the old 5x runtime gate. |
| Main uncertainty | No trusted-GPU runtime improvement has been measured in Phase 2; Phase 3/4 still need focused engine tests before Phase 5 GPU profiling. |
| Next justified action | Draft/review Phase 3 value-only diagnostics fast-path execution using focused tests and no GPU profiling. |
| What is not concluded | No GPU speedup, no memory improvement, no particle adequacy, no leaderboard completion, no exact likelihood/gradient/HMC/NUTS/production readiness. |

## Implementation

Changed harness only:

- `docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py`

Changes:

- added `--history-mode {full,value-only}`, default `full`;
- passed `return_history=args.history_mode == "full"` to the streaming core;
- recorded `history_mode` and `return_history` in JSON output;
- recorded the streaming core's empty history shapes under value-only mode with
  `ess_summary_available=false`;
- made CPU/non-GPU smokes set `runtime_gate_applicable=false`,
  `speedup_vs_scalar_comparator_mean_warm_call=null`, and
  `primary_pass_5x_runtime_gate=false`.

No core streaming engine code was edited.

## Checks Run

```bash
python -m py_compile docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py
git diff --check -- docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-*
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py --device-scope cpu --expect-device-kind cpu --batch-size 1 --time-steps 2 --num-particles 8 --state-dim 4 --obs-dim 2 --transport-policy no-resampling --return-history --warmups 0 --repeats 1 --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-lgssm-harness-smoke-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-lgssm-harness-smoke-2026-06-18.md
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --device-scope cpu --expect-device-kind cpu --batch-seeds 81120 --time-steps 2 --num-particles 8 --transport-policy no-resampling --history-mode value-only --warmups 0 --repeats 1 --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-actual-sir-harness-smoke-value-only-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-actual-sir-harness-smoke-value-only-2026-06-18.md
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --device-scope cpu --expect-device-kind cpu --batch-seeds 81120 --time-steps 2 --num-particles 8 --transport-policy no-resampling --history-mode full --warmups 0 --repeats 1 --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-actual-sir-harness-smoke-full-history-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-actual-sir-harness-smoke-full-history-2026-06-18.md
```

All passed.  TensorFlow printed CUDA initialization warnings during CPU-only
runs because CUDA was intentionally hidden with `CUDA_VISIBLE_DEVICES=-1`;
the emitted artifacts report CPU output devices and no logical GPUs.

## Artifact Metadata Check

Durable smoke artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-lgssm-harness-smoke-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-lgssm-harness-smoke-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-actual-sir-harness-smoke-value-only-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-actual-sir-harness-smoke-value-only-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-actual-sir-harness-smoke-full-history-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-actual-sir-harness-smoke-full-history-2026-06-18.md`

Summary:

| Artifact | Finite | Device | History mode | Return history | Runtime gate applicable | Speedup claim |
| --- | --- | --- | --- | --- | --- | --- |
| LGSSM smoke | true | CPU | N/A | true | N/A | N/A |
| actual-SIR value-only | true | CPU | `value-only` | false | false | null |
| actual-SIR full-history | true | CPU | `full` | true | false | null |

The actual-SIR full-history and value-only runs produced the same log
likelihood for this tiny smoke, while only full-history reported ESS.

## Post-Run Red Team

Strongest alternative explanation:

- These are tiny CPU-only harness smokes.  They validate plumbing and metadata,
  not runtime scaling.

What would overturn the Phase 2 conclusion:

- A reviewer finding that `history_mode=value-only` changes value semantics
  rather than only diagnostic outputs, or a later focused test showing
  `return_history=True` and `False` disagree on log likelihood for matched
  seeds/settings.

Weakest part of the evidence:

- The Phase 2 checks do not yet include a formal unit test for value-only/full
  log-likelihood equivalence.  Phase 3 should add focused tests around this
  behavior before GPU profiling.

## Handoff

Phase 3 should focus on value-only diagnostics fast-path correctness.  It must
not run GPU profiling and must not claim speedup until Phase 5 trusted-GPU
profiling.
