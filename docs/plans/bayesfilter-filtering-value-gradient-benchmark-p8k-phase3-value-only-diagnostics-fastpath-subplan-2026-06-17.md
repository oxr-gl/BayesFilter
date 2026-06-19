# P8k Phase 3 Subplan: Value-Only Diagnostics Fast Path

metadata_date: 2026-06-17
status: DRAFT
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md
phase: 3

## Phase Objective

Make value-only execution genuinely avoid history-only diagnostics when
`return_history=False` or an equivalent reviewed diagnostic level is selected.

## Entry Conditions Inherited From Previous Phase

- Phase 2 harness plumbing passed.
- Any diagnostic-level API was reviewed in Phase 1 and exposed in Phase 2.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-value-only-diagnostics-fastpath-result-2026-06-17.md`
- Focused test output summary.

## Required Checks/Tests/Reviews

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py -q -k "likelihood_only or nonlinear_prior_mean"
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --device-scope cpu --expect-device-kind cpu --batch-seeds 81120 --time-steps 2 --num-particles 8 --transport-policy no-resampling --history-mode value-only --warmups 0 --repeats 1 --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-actual-sir-value-only-equivalence-2026-06-18.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --device-scope cpu --expect-device-kind cpu --batch-seeds 81120 --time-steps 2 --num-particles 8 --transport-policy no-resampling --history-mode full --warmups 0 --repeats 1 --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-actual-sir-full-history-equivalence-2026-06-18.json
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-*
```

Claude review is required for material implementation diffs before Phase 4.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can value-only mode skip unnecessary mean, variance, and ESS history work while preserving output semantics? |
| Baseline/comparator | Current `return_history=False` path, which returns empty history tensors but still shares diagnostic computations in `step_body`. |
| Primary criterion | Focused tests prove matched `return_history=False` and `return_history=True` paths have equal log likelihoods for the generic streaming core, and matched actual-SIR `--history-mode value-only` and `full` smokes have equal log likelihoods while only history/ESS availability changes. |
| Veto diagnostics | Changed log-likelihood values for equivalent settings, broken `return_history=True`, missing empty-history shape for value-only, missing ESS metadata difference for actual-SIR, or hidden SIR-specific logic. |
| Explanatory diagnostics | CPU smoke runtime and code-path notes. |
| Not concluded | No GPU speedup claim until Phase 5, no statistical adequacy. |

## Forbidden Claims/Actions

- Do not remove diagnostics from `return_history=True`.
- Do not change default outputs.
- Do not run long GPU profiling in Phase 3.
- Do not treat shape-only checks as sufficient; value equivalence is required.
- Do not claim default suitability, default promotion, production readiness, or
  preferred-mode status from Phase 3.

## Exact Next-Phase Handoff Conditions

Phase 4 may proceed if focused tests pass and the result records exact
behavioral invariants:

- generic streaming core `return_history=False` and `True` log likelihoods are
  equal under matched inputs;
- actual-SIR harness `history-mode value-only` and `full` log likelihoods are
  equal under matched seeds/settings;
- only history tensors and ESS metadata differ as expected.

## Stop Conditions

Stop if value-only optimization changes log-likelihood values, breaks history
mode, cannot prove actual-SIR value-only/full equivalence, or requires a
non-generic callback.
