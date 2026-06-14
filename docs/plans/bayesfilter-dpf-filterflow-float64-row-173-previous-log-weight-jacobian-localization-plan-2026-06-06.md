# Plan: Row 173 Previous Log-Weight Jacobian Localization

## Scope

This is a BayesFilter-owned DPF difference-audit diagnostic. It localizes why
the accepted row-173 unit-upstream log-weight probe found:

- executable float64 FilterFlow
  `VJP(pre_log_weights wrt pre_particles, ones_like(pre_log_weights))`
  essentially zero;
- BayesFilter's matching unit-upstream previous-carry factor materially
  nonzero.

It does not claim either implementation is mathematically correct.

Allowed write set:

- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-previous-log-weight-jacobian-localization-*.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_previous_log_weight_jacobian_localization_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-previous-log-weight-jacobian-localization-2026-06-06.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_previous_log_weight_jacobian_localization_2026-06-06.json`

Forbidden write set:

- production `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow`
- vendored/student/highdim/DSGE/NAWM lanes

## Evidence Contract

Question:

At row 173, does the BayesFilter-vs-FilterFlow previous-log-weight carry
Jacobian difference originate in the time-92 component derivative of
`transition_ll + observation_ll - proposal_ll`, the proposal log-probability
route, the normalization route, or an unresolved edge?

Comparator:

The local executable float64 FilterFlow reference in `.localsource/filterflow`,
validated by the same marker, status, and fingerprint controls used by the
accepted row-173 probes.

Inputs:

- row 173 mesh parameters from the accepted row-173 VJP harness;
- previous time index `92`;
- target carry time index `93` only as provenance;
- CPU-only execution with `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import in
  parent and subprocess;
- prior accepted unit-upstream artifact:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_filterflow_unit_upstream_log_weight_2026-06-06.json`.

Primary criterion:

After vetoes clear, compare FilterFlow and BayesFilter unit-upstream VJPs with
respect to the time-92 `proposed_particles` for:

- `normalized`;
- `unnormalized`;
- `transition_ll`;
- `observation_ll`;
- `proposal_ll`;
- signed component sum `transition_ll + observation_ll - proposal_ll`;
- proposal-log-probability alternatives exposed by the harness.

Tolerance controls:

- `VALUE_TOLERANCE = 5e-8`;
- `GRADIENT_TOLERANCE = 2e-4`.

Veto diagnostics:

- executable FilterFlow subprocess cannot run;
- prior unit-upstream artifact missing or invalid;
- comparator fingerprint changes;
- CPU-only manifest violation;
- value-path mismatch for required component tensors;
- resampling flags differ;
- required VJP tensors are missing or non-finite;
- path-boundary contamination.

Hypothesis classifications:

- `h1_blocked_or_vetoed`: any veto fails.
- `h2_proposal_log_prob_route_differs`: proposal log-probability VJP differs
  materially and the signed component sum differs materially.
- `h3_transition_or_observation_route_differs`: transition or observation VJP
  differs materially before the proposal route explains the sum.
- `h4_normalization_route_differs`: signed unnormalized component VJP matches
  but normalized carry VJP differs materially.
- `h5_filterflow_zero_bayesfilter_nonzero_localized_to_signed_sum`: FilterFlow's
  signed component VJP is near zero while BayesFilter's is materially nonzero,
  without a single component uniquely explaining it.
- `h6_unresolved_previous_log_weight_jacobian`: finite evidence does not
  isolate the route.

What must not be concluded:

- correctness of FilterFlow or BayesFilter;
- analytic-gradient correctness;
- posterior correctness;
- global smoothness-surface agreement;
- that any boundary mode is a code fix;
- production or public API readiness;
- monograph, highdim, DSGE, NAWM, or banking/model-risk claims.

Artifact:

`experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_previous_log_weight_jacobian_localization_2026-06-06.json`

## Skeptical Pre-Execution Audit

- Wrong baseline risk: the comparator is only executable local float64
  FilterFlow, not paper notation or a fixed-target Sinkhorn surrogate.
- Proxy risk: total-gradient deltas are explanatory only; the primary criterion
  is component VJPs of the previous log-weight carry edge.
- Hidden-assumption risk: the previous-time component probe is a localization
  diagnostic, not a correctness proof.
- Stale-context risk: use previous time `92`, because target time `93`
  `pre_log_weights` is the time-92 normalized carry.
- Unfair-comparison risk: compute FilterFlow component VJPs inside the
  executable FilterFlow subprocess, not inferred from BayesFilter.
- Stop-condition risk: stop as blocked if value, CPU, fingerprint, tensor, or
  path-boundary gates fail.
- Lane risk: do not edit production code, tests, chapters, or FilterFlow source.

Audit status: passed for execution. This is the smallest direct follow-up to
the accepted unit-upstream result because it probes the exact previous update
that created the carried `pre_log_weights`.
