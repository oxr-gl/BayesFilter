# P49-M6 Smoothing Boundary Result

metadata_date: 2026-06-09
phase: P49-M6
status: PASS_P49_M6_SMOOTHING_BOUNDARY

## Decision Table

| Field | Decision |
| --- | --- |
| Gate decision | Pass M6 for explicit smoothing-boundary governance and deferred backward-conditional requirements. |
| Primary criterion status | Passed: tests forbid filtering tokens from acting as smoothing evidence, require backward conditional maps and backward weights in any smoother contract, and reject deferred smoothing rows that carry smoother pass tokens. |
| Veto diagnostic status | Passed: filtering likelihood passes are not promoted to smoothing passes; backward weights are required by the boundary contract. |
| Main uncertainty | No source-style smoother or backward conditional map implementation exists in M6. |
| Next justified action | Advance to M7 gradient-lane boundary. |
| Not concluded | No smoothing support, smoothing marginal accuracy, backward conditional map round trip, or smoother production readiness. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Are smoothing claims excluded or separately tested with source-style backward conditionals? |
| Baseline/comparator | M1 source smoothing roles from `full_sol.smooth`, `pre_sol.smooth`, and `smooth_t`; current filtering tokens and retained-object contracts. |
| Primary pass criterion | Artifacts forbid smoothing claims unless a dedicated smoother test passes; deferred row preserves backward-conditional requirements. |
| Diagnostics that can veto | Filtering likelihood pass promoted to smoothing pass; backward weights omitted. |
| Explanatory diagnostics | CPU-only pytest, compileall, static diff whitespace check. |
| What will not be concluded | Smoothing implementation or smoothing accuracy. |
| Artifact preserving result | This file plus `tests/highdim/test_p49_source_route_smoothing_boundary.py`. |

## Implemented Scope

M6 added `SourceRouteSmoothingBoundary` in
`bayesfilter/highdim/source_route.py`.

The boundary requires:

- `smoothing_status` of `deferred` or `implemented`;
- explicit `backward_conditional_maps`;
- explicit `backward_weights`;
- non-claims separating filtering from smoothing;
- a dedicated smoother token for any implemented smoother claim.

The boundary rejects:

- deferred smoothing rows that carry smoother pass tokens;
- implemented smoothing rows without a dedicated smoother token;
- contracts that omit backward conditional maps or backward weights.

No source-style smoother was implemented.

## Local Validation

Commands run CPU-only with `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`:

```text
pytest -q tests/highdim/test_p49_source_route_smoothing_boundary.py tests/highdim/test_p49_source_route_preconditioned_predator_prey.py tests/highdim/test_p49_source_route_recenter_normalizer.py tests/highdim/test_p49_source_route_sample_proposal.py tests/highdim/test_p49_source_route_retained_object.py tests/highdim/test_public_api_highdim.py tests/highdim/test_phase0_contracts.py
```

Result:

```text
52 passed, 2 TensorFlow Probability deprecation warnings
```

```text
python -m compileall -q bayesfilter/highdim/source_route.py tests/highdim/test_p49_source_route_smoothing_boundary.py tests/highdim/test_p49_source_route_preconditioned_predator_prey.py tests/highdim/test_p49_source_route_recenter_normalizer.py tests/highdim/test_p49_source_route_sample_proposal.py tests/highdim/test_p49_source_route_retained_object.py
```

Result: passed.

```text
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p49_source_route_smoothing_boundary.py docs/plans/bayesfilter-highdim-zhao-cui-p49-visible-execution-ledger-2026-06-09.md
```

Result: passed.

## Interpretation

The M6 gate closes the smoothing overclaim risk.  Filtering phases M0--M5 do
not imply smoothing.  Any future smoothing claim must carry separate backward
conditional maps, backward weights, and a dedicated smoother test/pass token.
