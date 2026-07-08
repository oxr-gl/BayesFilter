# P82 Phase 2 Result: Regression-FD Harness Protocol Repair

status: COMPLETE_PENDING_REVIEW
date: 2026-06-22
phase: P2

## Question

Does the regression-FD harness implement the corrected P82 13-point,
five-seed, value-outlier-trim protocol without changing scientific claims?

## Decision

P2 passed its local engineering gate.  The regression-FD harness now accepts
13-point offset lines and can explicitly select value-outlier trimming with
deterministic tie-breaking.  The existing offset-trim behavior remains
available for older diagnostics through `--trim-extreme-mode offset`; P82
commands must use `--trim-extreme-mode value`.

Governed P82 regression-FD runs must explicitly pass `--trim-extreme-mode value`
and record `raw_point_count = 13`, `fit_point_count = 11`, and that trimming
used highest/lowest mean-over-seed objective values rather than offset
magnitude.  If the flag is omitted, the harness remains backward compatible but
the resulting run is not P82-protocol compliant.

This result is harness-protocol evidence only.  It does not validate LEDH
gradients, does not certify Zhao-Cui as an analytical comparator, and does not
authorize the N=1000 or N=10000 governed research runs.

## Skeptical Plan Audit

Pass.  The patched code path is the same benchmark harness P6 will call:
`docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`.  The new
value trim operates after the existing mean-over-seed value aggregation.  Five
seeds and `--num-particles 1000` remain runtime settings, not hard-coded helper
defaults.  The focused tests are CPU-only protocol tests and cannot be read as
GPU-path or gradient-validation evidence.  P2 did not edit comparator logic and
did not promote regression FD, Zhao-Cui, or LEDH to oracle status.

## Code Changes

| File | Change |
|---|---|
| `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:57` to `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:65` | Allows 13 regression offsets and updates the validation error message. |
| `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:105` to `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:122` | Adds `--trim-extreme-mode {offset,value}`; default remains `offset` for backward compatibility. |
| `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:658` to `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:775` | Extends trimming to support value-based highest/lowest mean-objective drops with deterministic tie-breaking and dropped/retained metadata. |
| `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:789` to `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:833` | Passes the selected trim mode into the regression diagnostic and preserves raw line values plus fit subset values. |
| `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:1122` to `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:1136` | Records trim count and trim mode in the top-level `regression_fd` metadata. |
| `tests/highdim/test_p82_regression_fd_harness_protocol.py:18` to `tests/highdim/test_p82_regression_fd_harness_protocol.py:163` | Adds focused CPU-only tests for the P82 harness protocol. |

The safe argparse form for a negative offset list is:

```bash
--regression-offsets=-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6 --trim-extreme-mode value
```

Using a separate argument beginning with `-6` can be parsed as another option.

## Local Checks

Run with GPU intentionally hidden:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-highdim-zhao-cui-p82-*
```

Observed result:

| Check | Status |
|---|---|
| Focused pytest | `7 passed, 2 TFP deprecation warnings` |
| `py_compile` | passed |
| `git diff --check` | passed |

## Test Coverage

| Test | Evidence |
|---|---|
| 13-offset acceptance | `test_p82_parse_offsets_accepts_thirteen_points` accepts 13 and rejects unsupported 11. |
| Governed CLI switches | `test_p82_cli_accepts_governed_fd_protocol_switches` parses 13 offsets, `--trim-extreme-mode value`, batched theta, and N=1000 as runtime configuration. |
| Five seed default | `test_p82_default_seed_count_remains_five` preserves `[81120, 81121, 81122, 81123, 81124]`. |
| Value trim not offset trim | `test_p82_value_trim_drops_objective_extrema_not_extreme_offsets` drops interior y-extrema while retaining extreme x offsets. |
| Deterministic tie-break | `test_p82_value_trim_has_deterministic_tie_breaking` verifies equal y extrema use the declared deterministic order. |
| Raw/fitted subset and 11-point OLS | `test_p82_value_trim_preserves_raw_line_metadata_and_fits_eleven_points` verifies 13 raw values, 11 fit points, and slope/SE computed from retained points. |
| Backward-compatible offset trim | `test_p82_offset_trim_mode_is_preserved_for_existing_diagnostics` keeps old offset trimming available. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Accept P2 harness protocol repair | Passed | No GPU run, no comparator edit, no oracle promotion | Later full harness run may expose runtime/memory limits | Move to P3 comparator-route audit/repair | No gradient validation |
| Preserve value-trim auditability | Passed | Raw values retained; dropped/retained metadata added | Per-seed raw values are still not emitted separately by the harness | P6 may add per-seed output if needed for run artifacts | No MC variance decomposition from P2 |
| Defer Zhao-Cui comparator readiness | Passed | ForwardAccumulator route not touched or promoted | Exact analytical route implementation status still needs audit | Execute P3 with paper/source/code anchors | No analytical comparator certification |

## P3 Handoff

P3 must audit and, if narrowly justified, repair the Zhao-Cui analytical
comparator route.  It must not use the current ForwardAccumulator/JVP-backed
path as the primary comparator.  It must first locate the already-implemented
analytical derivative surface, if present, and classify any route choice under
the Zhao-Cui source-anchor gate.

Drafted next subplan:

`docs/plans/bayesfilter-highdim-zhao-cui-p82-phase3-zhaocui-analytical-route-subplan-2026-06-22.md`
