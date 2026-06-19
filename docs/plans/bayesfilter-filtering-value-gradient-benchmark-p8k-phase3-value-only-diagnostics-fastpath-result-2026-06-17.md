# P8k Phase 3 Result: Value-Only Diagnostics Fast Path

metadata_date: 2026-06-18
status: PASS_VALUE_ONLY_EQUIVALENCE
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md
phase: 3
executor: Codex
reviewer: Claude Opus max effort, read-only

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Value-only mode now avoids history-only diagnostic mean/variance/ESS computation in the generic streaming core, while preserving log-likelihood values under matched settings. |
| Primary criterion status | Passed.  Focused pytest covered generic streaming likelihood-only equivalence; matched actual-SIR value-only/full-history CPU artifacts have identical log likelihoods and expected history/ESS metadata differences. |
| Veto diagnostic status | No active veto.  Full-history mode still works; value-only mode returns empty history tensors; no GPU/speed/default/adequacy claim is made. |
| Main uncertainty | No trusted-GPU runtime gain has been measured yet; Phase 4 still needs inactive-transport skip semantics before Phase 5 profiling. |
| Next justified action | Review Phase 4 inactive-transport skip subplan with Claude, then implement/test that generic skip path if review agrees. |
| What is not concluded | No GPU speedup, no memory improvement, no particle adequacy, no leaderboard completion, no default suitability or production readiness. |

## Implementation

Changed generic streaming core only:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`

Change:

- `step_body` now accepts `compute_diagnostics`.
- `return_history=True` computes ESS, filtered means, and variances.
- `return_history=False` skips those diagnostics and returns ignored zero
  placeholders inside the loop; final public history tensors remain empty as
  before.

Changed planning/tests only:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-value-only-diagnostics-fastpath-subplan-2026-06-17.md`

The existing test
`test_streaming_value_likelihood_only_omits_history` already checks generic
streaming log-likelihood equivalence; Phase 3 corrected the pytest selector so
that test is part of the gate.

## Checks Run

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-*
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py -q -k "likelihood_only or nonlinear_prior_mean"
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --device-scope cpu --expect-device-kind cpu --batch-seeds 81120 --time-steps 2 --num-particles 8 --transport-policy no-resampling --history-mode value-only --warmups 0 --repeats 1 --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-actual-sir-value-only-equivalence-2026-06-18.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --device-scope cpu --expect-device-kind cpu --batch-seeds 81120 --time-steps 2 --num-particles 8 --transport-policy no-resampling --history-mode full --warmups 0 --repeats 1 --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-actual-sir-full-history-equivalence-2026-06-18.json
```

Results:

- pycompile: passed;
- `git diff --check`: passed;
- focused pytest: `3 passed, 7 deselected`;
- actual-SIR value-only CPU smoke: finite;
- actual-SIR full-history CPU smoke: finite;
- assertion check: matched actual-SIR log likelihoods equal exactly.

## Artifacts

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-actual-sir-value-only-equivalence-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-actual-sir-full-history-equivalence-2026-06-18.json`

Equivalence summary:

| Field | Value-only | Full-history |
| --- | --- | --- |
| `log_likelihood` | `[-69.82728576660156]` | `[-69.82728576660156]` |
| `return_history` | false | true |
| `ess_summary_available` | false | true |
| `ess_by_time` shape | `[0, 1]` | `[2, 1]` |
| `runtime_gate_applicable` | false | false |
| speedup claim | null | null |

## Post-Run Red Team

Strongest alternative explanation:

- The CPU-only actual-SIR equivalence smoke is tiny (`T=2,N=8,B=1`) and proves
  plumbing semantics, not large-run performance.

What would overturn the Phase 3 conclusion:

- A later test showing value-only mode changes log likelihood under active OT
  resampling or larger batched settings.

Weakest part of the evidence:

- The explicit actual-SIR equivalence smoke uses `transport-policy
  no-resampling`; the generic pytest fixture includes an active mask row and
  guards the streaming core invariant.

## Handoff

Phase 4 may proceed after Claude review of this result and the Phase 4 subplan.
Phase 4 must test inactive-transport skip semantics and must not claim GPU
speedup before Phase 5.
