# P81 Phase 8 Subplan: Streamed Transition Prototype

status: REVIEWED_AGREED_EXECUTED
date: 2026-06-21

## Phase Objective

Implement a bounded streaming transition predictive logsumexp prototype for the
multistate retained all-grid score route.  Phase 8 must preserve the current
fail-fast unbounded `COMPLEXITY_GATE`, prove dense-vs-streaming parity on tiny
d=2 fixtures, and prove that the integrated multistate score route actually
exercises the streaming path when selected or fallback-triggered.

An optional d=18 two-row timing/subset probe may be recorded only as a scaling
diagnostic.  It cannot promote the route to LEDH/P8p comparison readiness and
cannot establish d=18 full-history correctness.

Phase 8 is not an LEDH/P8p comparator phase.

## Entry Conditions Inherited From Phase 7

- Phase 6 tiny d=2 two-row multistate score finite-difference regression passed.
- Phase 6 SIR d=18 two-row all-grid route is blocked by unchunked pairwise
  transition complexity.
- Phase 7 identified double-chunk streaming as a bounded peak-memory prototype
  route but not a total-work solution.
- Existing P51 governance already names the missing component as
  `streamed_or_factorized_transition_application`.

## Required Artifacts

- This Phase 8 subplan.
- Phase 8 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase8-streamed-transition-prototype-result-2026-06-21.md`.
- Updated P81 master, runbook, execution ledger, Claude review ledger, and stop
  handoff.
- Focused code/test edits if reviewed:
  `bayesfilter/highdim/filtering.py`,
  `tests/highdim/test_fixed_branch_derivatives.py`,
  `tests/highdim/test_p81_analytical_sir_score.py`.

The Phase 8 result must include a skeptical-audit note, decision table, run
manifest, quantitative memory/runtime notes, and explicit non-claims.

## Required Checks, Tests, And Reviews

Pre-implementation checks:

```bash
rg -n "_multistate_grid_predictive_log_density_from_retained|_multistate_grid_predictive_log_density_and_derivative_from_retained|_check_pairwise_transition_tensor_budget" bayesfilter/highdim/filtering.py
rg -n "test_multistate_fixed_design_tt_score_path_matches_same_branch_fd_for_tiny_two_row_fixture|test_multistate_fixed_design_tt_score_path_blocks_sir_d18_two_row_all_grid_transition" tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_p81_analytical_sir_score.py
```

Implementation targets:

- Add a private streaming helper for multistate transition predictive
  log-density.
- Add a private streaming helper for multistate transition predictive
  log-density plus derivative.
- Add a per-chunk guard with a conservative summed peak bound.  The bound must
  include at least a safety multiplier for tiled point tensors plus transition
  log/weight/derivative work arrays; it must not price only
  `current_chunk * previous_chunk * state_dim * sizeof(float64)`.
- Keep the existing unchunked helper and its `COMPLEXITY_GATE` behavior.
- Wire streaming into the multistate transition target path only behind an
  explicit bounded internal option or automatic fallback when unchunked would
  exceed the guard.  No default policy outside this candidate path may change.
- Add an integration test that verifies the streaming path is actually exercised
  on a tiny multistate score case when the bounded route is selected or
  fallback-triggered; helper parity alone is insufficient.

Required CPU-hidden checks:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/highdim/filtering.py tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_p81_analytical_sir_score.py
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_fixed_branch_derivatives.py -k "multistate_fixed_design_tt_score_path or streaming"
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p81_analytical_sir_score.py -k "horizon0 or two_row"
```

Optional d=18 smoke:

- CPU-hidden only unless a reviewed GPU subplan is drafted.
- Wall-time cap: 180 seconds for the optional d=18 two-row smoke.
- Chunk-product cap: at most 8192 `(current_chunk, previous_chunk)` products
  may be evaluated in the optional d=18 smoke.
- The optional smoke, if attempted, must be a reviewed subset/timing-probe mode
  with an exact command, deterministic selection rule, recorded chunk sizes,
  and a hard abort when either 180 seconds or 8192 chunk products is reached.
  It may not silently run the complete d=18 grid.
- Default optional-smoke chunk proposal, if separately reviewed:
  `current_chunk=512`, `previous_chunk=64`, giving about 4.7 MB for the tiled
  point tensor alone and 512 * 4096 = 2,097,152 full chunk products for the
  complete grid.  That full-grid run is outside Phase 8.
- If it hits a timeout or budget gate, record blocker; do not escalate to LEDH.

Review this subplan with Claude read-only before implementation.  Review the
Phase 8 execution result with Claude read-only after checks.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can streaming preserve the current multistate transition target while avoiding full all-pairs materialization? |
| Exact baseline/comparator | Dense all-pairs helper on tiny d=2 fixtures; current unbounded d=18 route remains complexity-gated. |
| Primary criterion | Dense-vs-streaming parity for value and derivative on tiny d=2, plus tiny two-row FD regression remains passing. |
| Veto diagnostics | Removing the unbounded complexity gate; nonfinite streaming values; dense-vs-streaming mismatch; branch-hash drift; d=18 smoke materializes all pairs; timeout/budget overrun. |
| Explanatory diagnostics | Chunk size, chunk count, peak byte estimate, runtime, FD residual, TensorFlow warnings. |
| Not concluded | No LEDH agreement, no d=18 full-history correctness, no HMC readiness, no posterior/scientific validity, no production/default readiness.  Tiny dense-vs-streaming parity is implementation correctness evidence only for the tiny fixtures. |
| Artifact preserving result | Phase 8 result markdown and updated P81 ledgers. |

## Forbidden Claims And Actions

- Do not run LEDH/P8p diagnostics.
- Do not remove the unbounded transition complexity gate.
- Do not claim source-faithfulness, HMC readiness, posterior validity, or
  default readiness.
- Do not install/fetch packages, use network, launch detached agents, or take
  destructive git/filesystem actions.
- Do not use NumPy as BayesFilter algorithmic implementation backend.

## Exact Next-Phase Handoff Conditions

Phase 9 is not allowed to be an LEDH/P8p comparator phase based on Phase 8
alone.  Phase 8 can hand off to a representation/scaling phase if it records:

- dense-vs-streaming parity on tiny d=2;
- streaming-path integration exercised on a tiny score route;
- tiny d=2 two-row FD regression passing;
- Claude execution review convergence.

If a reviewed optional d=18 timing/subset probe is attempted, its result may
inform the representation/scaling phase but cannot by itself authorize
LEDH/P8p comparison.  If d=18 remains too slow or budget-gated, Phase 9 must
be a representation change plan, not LEDH/P8p comparison.

## Stop Conditions

Stop if streaming cannot preserve dense tiny parity, if it requires a broad
refactor/default change, if it still materializes all pairs, if d=18 smoke
exceeds the reviewed budget, or if Claude review does not converge after five
rounds.
