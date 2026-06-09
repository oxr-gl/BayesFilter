# P2 Claude Review Ledger: Tiny Nonlinear Dense Oracle

metadata_date: 2026-06-08
phase: P2
status: PASS_P2_TINY_NONLINEAR_DENSE_ORACLE_READY_FOR_P3

## Role Contract

Codex is supervisor and executor in this dialogue.

Claude is a read-only critical reviewer only. Claude must not edit files, run
experiments, launch agents, or change state.

## Review Protocol

Claude must check wrong baselines, proxy metrics being treated as promotion
criteria, missing stop conditions, unfair comparisons, hidden assumptions,
stale context, environment mismatches, unsupported dense-oracle claims, missing
artifacts, and whether P2 evidence answers the tiny nonlinear dense-oracle
question.

Claude must end with exactly `VERDICT: AGREE` or `VERDICT: REVISE`.

## Iteration 1

Status: `VERDICT: REVISE`.

Scope for review:

- P2 subplan:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p2-tiny-nonlinear-dense-oracle-subplan-2026-06-08.md`
- P2 result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p2-tiny-nonlinear-dense-oracle-result-2026-06-08.md`
- P2 JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_2026-06-08.json`
- P2 runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_tf.py`
- P0 registry:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-target-route-registry-2026-06-08.json`
- Visible ledger:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md`

Questions:

1. Does P2 correctly use dense/refined quadrature as the only exact oracle for
   the selected tiny nonlinear target?
2. Are UKF, SVD/cubature, CUT4, and Zhao-Cui/fixed-design TT kept in their P0
   claim classes, without calling UKF/SVD/CUT4 or Zhao-Cui ground truth?
3. Are DPF bootstrap-OT and LEDH-PFPF-OT correctly deferred to P5 rather than
   executed or promoted in P2?
4. Are dense refinement, value gaps, gradient gaps, directional finite
   differences, veto diagnostics, nonclaims, and run manifest sufficiently
   recorded for the P2 gate?

Claude findings:

- Dense/refined quadrature is kept as the only exact oracle for the selected
  tiny nonlinear target.
- UKF and SVD/cubature remain `DIAGNOSTIC_ONLY`; CUT4 and
  Zhao-Cui/fixed-design TT remain `CERTIFIED_APPROXIMATION`; the result note
  labels them as not oracle.
- DPF bootstrap-OT and LEDH-PFPF-OT are correctly deferred to P5 rather than
  executed or promoted in P2.
- Dense refinement, value gaps, gradient-gap proxies, multi-step directional
  finite differences, veto diagnostics, stop conditions, nonclaims, and run
  manifest are broadly sufficient for a P2 gate.
- Material blocker: the runner compared different initial-state
  parameterizations across routes while calling them same-target. The dense
  oracle used `initial_mean = rho * raw_initial_mean` and
  `initial_variance = rho^2 * raw_initial_variance + transition_variance`,
  while the structural sigma-point model used `raw_initial_mean` and
  `raw_initial_variance` directly.
- Related validator blind spot: `single_step_finite_difference_used_as_promotion`
  and `gradient_parameterization_mismatch` were hard-coded `False`; the
  initial-state mismatch made the all-false veto claim insufficient.

Codex-supervisor classification:

| Finding | Classification | Patch/control added |
| --- | --- | --- |
| Dense and structural initial law mismatch | `ACCEPT` | Changed the structural model to use `initial_mean` and `initial_variance`, matching the dense scalar route. |
| Missing derived mismatch check | `ACCEPT` | Added `initial_law_alignment` to each dense row and derive `gradient_parameterization_mismatch` from it. |
| Hard-coded FD promotion veto | `DEFER_NON_BLOCKING` | Existing FD diagnostics remain multi-step and validator rejects large FD diagnostics; no single-step FD promotion appears. |

Decision after patch: rerun P2 and then rerun Claude review.

## Iteration 2

Status: `VERDICT: AGREE`.

Claude findings:

- Iteration-1 blocker is resolved: the scalar dense route and structural
  sigma-point routes now share the same predictive initial law using
  `initial_mean` and `initial_variance` from the common physical-part map.
- The artifact records same-target `initial_law_alignment` per dimension, with
  zero mean and covariance gaps for dims 1, 2, and 3.
- `gradient_parameterization_mismatch` is now derived from the recorded
  alignment, and validation rejects unaligned rows.
- Dense refined quadrature remains the only `EXACT_ORACLE`; UKF and SVD remain
  `DIAGNOSTIC_ONLY`; CUT4 and Zhao-Cui/fixed-design TT remain
  `CERTIFIED_APPROXIMATION`, with non-oracle labels preserved.
- DPF bootstrap-OT and LEDH-PFPF-OT remain deferred to P5 rather than promoted
  in P2.
- Dense refinement, value gaps, gradient/directional gaps, multi-step finite
  difference diagnostics, veto diagnostics, and CPU-only environment recording
  are present for the P2 gate.
- Non-blocking note: `single_step_finite_difference_used_as_promotion` is still
  hard-coded `False`, but the actual promotion path is dense refinement plus
  multi-step finite-difference checks, so this is hardening debt rather than a
  P2 blocker.

Codex-supervisor classification:

| Finding | Classification | Decision |
| --- | --- | --- |
| Same-target initial-law repair accepted | `ACCEPT_AGREE` | P2 review gate passed. |
| No remaining material P2 blocker | `ACCEPT_AGREE` | Advance to P3 precheck. |
| Hard-coded single-step FD veto | `DEFER_NON_BLOCKING` | Track as cleanup hardening; not required before P3 because P2 promotion path is dense refinement plus multi-step FD checks. |

Decision: `PASS_P2_TINY_NONLINEAR_DENSE_ORACLE_READY_FOR_P3`.
