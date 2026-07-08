# P81 Phase 8 Result: Streamed Transition Prototype

status: PHASE8_TINY_STREAMING_PARITY_PASSED_D18_FULL_GRID_STILL_BLOCKED
date: 2026-06-21
supervisor_executor: Codex
readonly_reviewer: Claude Opus

## Skeptical Audit Before Execution

Pass after review repair.  Claude initially blocked the Phase 8 subplan because
it could have promoted a d=18 two-row smoke to LEDH/P8p comparator readiness,
treated bounded smoke as possible full-history correctness, and priced only one
tensor class in the chunk memory guard.  The subplan was patched and Claude
Round 2 returned `VERDICT: AGREE`.

Execution then found a material implementation-boundary bug: the first streamed
fallback bounded peak memory but not total chunk products, so the d=18 two-row
test could begin an enormous full-grid streamed computation.  That run was
interrupted and the implementation was patched with a total chunk-product gate.
The final checks below are after that repair.

## Decision Table

| Field | Status |
|---|---|
| Decision | Phase 8 passes only as a tiny streaming-transition implementation prototype.  It does not unlock d=18 comparison. |
| Primary criterion | Passed: dense-vs-streaming parity for tiny d=2 value and derivative, plus tiny two-row FD regression and streaming integration evidence. |
| Veto diagnostic status | Final state: no veto.  The unbounded d=18 two-row all-grid route still fails fast with `COMPLEXITY_GATE`; no LEDH/P8p diagnostic was run. |
| Main uncertainty | Streaming controls peak memory but total work remains quadratic.  Complete d=18 two-row all-grid streaming has 2,097,152 default chunk products and remains outside the reviewed Phase 8 budget. |
| Next justified action | Phase 9 must be a representation/scaling phase for a factorized or otherwise non-quadratic transition application, not an LEDH/P8p comparator phase. |
| Not concluded | No d=18 full-history correctness, no LEDH/P8p agreement, no HMC readiness, no posterior/scientific validity, no source-faithfulness, no default readiness. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `5ea363e594516be236ca7c78ab2067b28a5b6eb5` |
| Worktree status | Dirty before Phase 8; includes prior P81 edits and unrelated workspace changes. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase8-streamed-transition-prototype-subplan-2026-06-21.md` |
| Code files touched | `bayesfilter/highdim/filtering.py`; `tests/highdim/test_fixed_branch_derivatives.py` |
| Docs files touched | P81 Phase 8 subplan, result, runbook, master, ledgers, handoff, and Phase 9 subplan. |
| CPU/GPU status | CPU-hidden checks only: `CUDA_VISIBLE_DEVICES=-1`.  No GPU/CUDA command was run in Phase 8. |
| Random seeds | Deterministic fixed-branch test seeds embedded in test fixtures; no stochastic run. |
| Network/package/destructive actions | None. |

## Implementation Summary

- Added private streaming helpers for multistate retained-grid transition
  predictive log density and predictive derivative.
- The streaming recurrence maintains numerically stable blockwise logsumexp and
  derivative weighted averages without materializing the full current-previous
  transition matrix.
- Preserved the existing dense helper and unchunked `COMPLEXITY_GATE`.
- Added a conservative per-chunk memory guard pricing tiled point tensors plus
  log/weight/derivative work arrays with a safety multiplier.
- Added a total chunk-product gate.  The default full d=18 degree-0 two-row
  grid with `current_chunk=512` and `previous_chunk=64` would require
  `512 * 4096 = 2,097,152` chunk products, which exceeds the Phase 8 cap of
  `8192` and therefore remains blocked.
- Added tests for helper parity and integrated fallback routing.

## Quantitative Notes

Tiny d=2 parity tests used a `5 x 5 = 25` point current grid and a `25` point
previous retained grid.  With chunks `3 x 4`, the derivative streaming helper
uses `ceil(25/3) * ceil(25/4) = 63` chunk products and a conservative per-block
estimate of about `2304` bytes, under the test-local `100000` byte budget.

For d=18 degree-0 two-row retained all-grid propagation, the retained and
current grids each have `2^18 = 262144` points.  The unchunked route remains
blocked before allocation.  The default streamed full-grid route would bound
per-chunk memory but still require `2,097,152` chunk products, so Phase 8 blocks
it as computationally out of scope.

## Checks

All final checks were CPU-hidden with `CUDA_VISIBLE_DEVICES=-1`.

```bash
python -m py_compile bayesfilter/highdim/filtering.py tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_p81_analytical_sir_score.py
```

Result: passed.

```bash
pytest -q tests/highdim/test_fixed_branch_derivatives.py -k "multistate_fixed_design_tt_score_path or streaming"
```

Result: `5 passed, 18 deselected, 2 warnings`.

```bash
pytest -q tests/highdim/test_p81_analytical_sir_score.py -k "horizon0 or two_row"
```

Result: `2 passed, 2 deselected, 2 warnings`.

```bash
pytest -q tests/highdim/test_p46_multistate_zhaocui_adapter.py tests/highdim/test_p47_spatial_sir_filtering.py
```

Result: `10 passed, 2 warnings`.

Warnings were TensorFlow Probability `distutils` deprecation warnings and were
non-vetoing for this Phase 8 implementation question.

## Post-Run Red-Team Note

The strongest alternative explanation for the pass is that the tests validate
only tiny algebra and routing.  They do not show that full d=18 transition
application is viable.  The first implementation attempt confirmed the danger:
peak-memory streaming alone can still create an impractically large full-grid
computation.  The chunk-product cap fixes the governance boundary, not the
underlying `O(N_current N_previous d)` arithmetic.

The result that would overturn this limitation would be a reviewed
representation/transition-application route that avoids dense all-grid pair
enumeration while preserving the intended fixed-branch target and derivative
semantics.

## Handoff

Proceed to Phase 9 as a representation/scaling design phase.  Do not run
LEDH/P8p comparison from Phase 8 evidence.
