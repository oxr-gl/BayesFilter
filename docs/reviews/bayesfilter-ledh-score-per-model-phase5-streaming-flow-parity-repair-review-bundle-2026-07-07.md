# Claude Read-Only Review Bundle: Phase 5 Actual-SV Streaming-Flow Parity Repair

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex remains supervisor and executor. Claude is read-only reviewer only.

## Objective

Review whether the Phase 5 actual-SV full-row gate was correctly blocked on a
same-algorithm parity gap and whether the streaming-flow parity repair subplan
is safe to execute.

## Fixed Paths To Review

- `docs/plans/bayesfilter-ledh-score-per-model-phase5-actual-sv-full-row-score-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-phase5-actual-sv-streaming-flow-parity-repair-subplan-2026-07-07.md`
- `docs/benchmarks/benchmark_ledh_same_target_actual_sv_score.py`
- `docs/benchmarks/benchmark_ledh_same_target_actual_sv_value.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`

## Evidence Contract

Actual-SV score admission requires the no-tape total derivative of the exact
same finite-`N` streaming-flow value algorithm admitted for:

```text
zhao_cui_sv_actual_nongaussian_T1000
```

The target scalar is:

```text
observed_data_log_likelihood_estimator
```

reported as:

```text
log_likelihood
```

The target observation policy is:

```text
transformed_actual_sv_log_y_square
```

The parameter vector is:

```text
[gamma_unconstrained, log_beta]
```

## Blocker Summary

The tiny actual-SV score diagnostic passed all-coordinate FD, but it used a
matrix-flow aux primitive while the admitted value route uses
`streaming_tf.batched_ledh_flow_streaming_particles_tf`.

Tiny parity probe at `T=2,N=64`:

```text
value_route   = [-3.603378542893297]
score_forward = [-3.6034006908781437]
diff          = [-2.214798484656555e-05]
```

The result therefore blocks full score/memory execution until a
streaming-flow-with-aux/VJP route restores same-forward-scalar parity.

## Repair Subplan Summary

The subplan requires:

- same-forward-scalar parity before FD score checks can support admission;
- a streaming-flow-with-aux wrapper that mirrors the value route's chunking,
  padding, and call to `batched_ledh_flow_core_tf`;
- a streaming-flow VJP that reverses retained chunks with the existing matrix
  flow VJP;
- no full `N=10000,T=1000` run until parity and tiny FD pass again;
- no tape, `ForwardAccumulator`, hidden autodiff, stopped partials, target
  substitution, or post-hoc tolerance loosening.

## Review Questions

1. Is it correct to block full actual-SV score execution because the score
   forward route is not exactly the admitted streaming-flow value route?
2. Does the repair subplan target the right dependency: streaming-flow
   parity before full score/memory work?
3. Does the subplan preserve no-tape and target-boundary constraints?
4. Is it boundary-safe to execute this repair subplan?

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
