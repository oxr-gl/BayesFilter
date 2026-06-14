# Summary: FilterFlow Float64 Row 173 Gradient Debug

## Decision

`row_173_gradient_residual_localized_to_time_93_implicit_transport_derivative`

## What Changed

The earlier row-173 localization reported a gradient failure at `time_index=1`.
That was not the true same-contract residual. A corrected full-path diagnostic
showed that FilterFlow and BayesFilter match at time `1` to about `1e-11` when
both sides use a single persistent full-path GradientTape.

## Corrected Evidence

| Diagnostic | Decision | Key result |
| --- | --- | --- |
| Time-1 VJP decomposition | `filterflow_float64_row_173_vjp_total_gradient_match` | scalar and total gradient match; intermediate VJPs differ only as graph-structure diagnostics |
| Full-path cumulative scan | `filterflow_float64_row_173_full_path_scan_gradient_residual_localized` | first true gradient residual is `time_index=93` |
| Time-92 VJP decomposition | `filterflow_float64_row_173_vjp_total_gradient_match` | immediately before the first failure, scalar path aligns and max total-gradient delta is only `8.997739007554628e-05` |
| Time-93 VJP decomposition | `filterflow_float64_row_173_vjp_gradient_difference_localized` | scalar/value tensors match; first VJP delta is `pre_particles`; transport-matrix upstream adjoint now matches after all-rows topology instrumentation |
| Time-94 VJP decomposition | `filterflow_float64_row_173_vjp_value_difference_localized` | immediately after the first failure, the same gradient offset persists and a tiny normalized-weight value drift appears downstream |
| Time-93 resampling-adjoint split | `implicit_transport_derivative_delta` | direct `T^T grad(post_particles)` adjoint matches to `3.268496931441156e-11`; implicit `dT/dx` contribution carries max delta `14.961877181675323` |
| Proposal-sample gradient probe | `proposal_sample_gradient_contract_differs` | FilterFlow sample-to-proposal-mean VJP is zero while BayesFilter/TFP sample is reparameterized, but a target-time stop-gradient control does not close the total row-gradient residual |

## Numerical Signal

At `time_index=93`, scalar delta is `6.2123888255882775e-09`, so the scalar
path remains aligned. The gradient delta is
`[5.302734403676368, -0.1337765252068337]`, with max absolute delta
`5.302734403676368`.

The updated time-93 VJP decomposition reports:

- first value delta: none over `5e-08`;
- first VJP delta: `pre_particles`;
- FilterFlow transport upstream clip fraction: `0.88`;
- BayesFilter transport upstream clip fraction: `0.88`;
- transport-matrix adjoint max delta: `3.360472966562611e-08`;
- direct pre-particle adjoint `T^T grad(post_particles)` max delta:
  `3.268496931441156e-11`;
- implicit transport derivative contribution max delta:
  `14.961877181675323`.

The bracketing VJP decompositions show:

- at `time_index=92`, scalar delta is `6.351314141284092e-09` and total
  gradient delta is `[8.997739007554628e-05, 1.5021129229353392e-07]`, so the
  total gradient still passes the `2e-4` tolerance;
- at `time_index=93`, the first true total-gradient residual appears with
  `[5.302734403676368, -0.1337765252068337]`;
- at `time_index=94`, the same offset persists as
  `[5.302730942314156, -0.13377622534002853]`, and the first value delta is a
  tiny normalized-weight sum drift (`7.342077879002318e-08`) after the
  time-93 gradient split.

## Interpretation

The remaining row-173 residual is not a data mismatch, seed mismatch, dtype
mismatch, or scalar/log-likelihood mismatch. It is also not explained by the
direct post-resampling matrix multiply: the direct adjoint agrees. The local
proposal-sample AD contract differs between FilterFlow and BayesFilter/TFP, but
that difference is already visible at `time_index=92`, where the total gradient
still matches, and a target-time sampled-particle stop-gradient control does not
move the time-93 total-gradient residual. The residual therefore enters through
the implicit derivative of the transport matrix with respect to the
pre-resampling particles at the first true residual time, `time_index=93`.

The strongest current hypothesis is a remaining arithmetic/topology mismatch
inside `d(transport_matrix)/d(particles)` for the annealed transport solve
under the matched upstream matrix adjoint. The next discriminating check should
compare FilterFlow and BayesFilter gradients of the transport matrix with
respect to input particles on the frozen time-93 tensors, using the same
clipped upstream matrix adjoint.

## Artifacts

- Time-1 VJP:
  `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-vjp-decomposition-result-2026-06-03.md`
- Full-path scan:
  `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-full-path-gradient-scan-result-2026-06-03.md`
- Time-93 VJP:
  `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-vjp-decomposition-result-2026-06-03.md`
- Time-92 VJP:
  `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-92-vjp-decomposition-result-2026-06-03.md`
- Time-94 VJP:
  `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-94-vjp-decomposition-result-2026-06-03.md`

## 2026-06-04 Continuation

The frozen/local transport-Jacobian probe moved the strongest suspect away from
the raw transport solve. With the same time-93 pre-resampling particles, log
weights, and clipped upstream transport-matrix adjoint, BayesFilter's local
clipped transport derivative matches the executable FilterFlow frozen transport
derivative:

- local clipped particle VJP max: `1.0756725359001307`;
- FilterFlow same-tape transport VJP max: `1.0756725353924719`;
- local clipped particle VJP sum: `-7.598639322386266`;
- FilterFlow same-tape transport VJP sum: `-7.598639330065231`.

The remaining full-graph residual is therefore not explained by the frozen
transport arithmetic alone.

The proposal-topology probe showed a real graph-topology difference in the
diagnostic replay:

- scalar/value paths still match at time 93;
- raw BayesFilter records `target -> proposal_ll` as disconnected (`None`/zero)
  because `proposal_dist.log_prob(proposal_dist.sample(...))` cancels through
  the reparameterized sample path;
- executable FilterFlow constructs proposal log probability through
  `OptimalProposalModel.loglikelihood`, which builds a fresh proposal
  distribution, so the recorded `proposal_ll` adjoint is `-softmax`;
- a BayesFilter `fresh_proposal_log_prob_filterflow_contract` boundary restores
  the target-time local adjoint topology: `proposal_ll`, `proposed_particles`,
  `proposal_mean`, `pre_particles`, and `post_particles` move into the
  FilterFlow-shaped local pattern.

That topology repair does not close the cumulative parameter-gradient residual:

- raw BayesFilter delta: `[5.302734403676368, -0.1337765252068337]`;
- fresh-proposal-log-prob boundary delta:
  `[5.306097234606568, -0.13386136230751333]`.

A true cut-set check at the time-93 post-resampling boundary split the residual:

- FilterFlow incoming-history push through
  `(post_particles, post_log_weights, pre_current_log_likelihoods)`:
  `[10598.93128336304, -292.3081844413939]`;
- BayesFilter fresh-proposal incoming-history push:
  `[10598.931318240252, -292.3081850063425]`;
- incoming-history push delta:
  `[3.4875251688063145e-05, -5.649485174881527e-07]`.

So the remaining row-173/time-93 residual is localized to the direct
current-step theta contribution after the post-resampling state is held fixed,
not to the incoming history, fixed data, seeds, dtype, scalar path, or frozen
transport derivative.

## Updated Next Action

Build a focused current-step direct-theta probe at time 93 with the
post-resampling state held fixed. Compare executable FilterFlow and BayesFilter
term by term for the direct theta derivative of
`transition_ll + observation_ll - proposal_ll`, using FilterFlow's fresh
proposal-log-prob topology. The terms to isolate are:

- direct derivative through transition log probability;
- direct derivative through the first proposal sample branch;
- direct derivative through the fresh proposal log-probability branch;
- cancellation between the optimal-proposal transition/observation/proposal
  terms.

Do not patch the algorithm until that direct current-step probe identifies the
specific executable FilterFlow arithmetic or topology rule being missed.
