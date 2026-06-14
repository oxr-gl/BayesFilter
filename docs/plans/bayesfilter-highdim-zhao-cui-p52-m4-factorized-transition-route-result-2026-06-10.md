# P52-M4 Result: Factorized Transition Route Contract

metadata_date: 2026-06-10
phase: P52-M4
status: BLOCK_P52_FACTORIZED_TRANSITION_ROUTE
supervisor: Codex
reviewer: Claude Code read-only agreed

## Decision

P52-M4 blocks rather than passes.  The current spatial SIR multistate route
still uses an all-axes retained-grid transition path that materializes dense
previous/current point pairs through `tf.repeat` and `tf.tile`.  That route is
the P51-M3 production blocker and cannot be used as the d=18 production-like
P52 route.

M4 added a reviewed contract and static guard for the required replacement
route, but no implemented TensorFlow streamed/local or TT-MPO factorized
transition application with deterministic replay, `R_eff` metadata, and memory
metadata exists yet.

Claude Opus read-only review agreed with the M4 blocker after two oversized
review prompts stalled and two minimal probes succeeded.  The successful
minimal review identified `bayesfilter/highdim/filtering.py` lines containing
`tf.repeat` and `tf.tile` as the active all-pairs materialization and returned
`VERDICT: AGREE`.

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | The current route cannot apply the spatial SIR transition without dense `N^2` pair materialization; a production-eligible factorized route is not implemented yet. |
| Baseline/comparator | P51-M3 dense route blocker, existing `bayesfilter/highdim/filtering.py` multistate route, and P52-M4 subplan. |
| Primary criterion | Blocked: static tests identify the current dense pairwise route and the contract object records the missing factorized route requirements. |
| Veto diagnostics | Fired: hidden/dense pairwise transition tensor remains in the current production candidate path. |
| Not concluded | No filtering accuracy, no d=18 spatial SIR filtering, no production spatial SIR readiness, no HMC readiness. |

## Implementation

Added:

- `bayesfilter/highdim/transition_route.py`
- internal `bayesfilter.highdim` exports for transition-route contracts
- `tests/highdim/test_p52_factorized_transition_route.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p52-m4-factorized-transition-route-manifest-2026-06-10.json`

The contract rejects forbidden dense pairwise transition interfaces and
requires any future passing route to provide:

- no dense pair materialization;
- deterministic replay;
- TensorFlow differentiability;
- an `R_eff` bound;
- memory metadata.

## Current Blocker

The static audit found the current route in:

- `multistate_nonlinear_transition_adjacent_target_batch`
- `_multistate_pairwise_transition_between_grids_log_density`

The blocked operations are:

```python
tf.repeat(current, repeats=previous_count, axis=0)
tf.tile(previous, [current_count, 1])
```

Those operations materialize all current/previous grid pairs.  They are
therefore not acceptable for the d=18 spatial SIR production-like route.

## Validation

Focused CPU-only validation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p52_factorized_transition_route.py
python -m compileall -q bayesfilter/highdim/transition_route.py tests/highdim/test_p52_factorized_transition_route.py
git diff --check -- bayesfilter/highdim/transition_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p52_factorized_transition_route.py docs/plans/bayesfilter-highdim-zhao-cui-p52-m4-factorized-transition-route-manifest-2026-06-10.json
```

Outcomes:

- pytest passed: `5 passed, 2 warnings in 3.08s`;
- compileall passed;
- git diff whitespace check passed.

The warnings came from TensorFlow Probability deprecation messages during the
existing broad `bayesfilter.highdim` import path.  GPU was intentionally hidden
with `CUDA_VISIBLE_DEVICES=-1`; no GPU claim is made.

## Nonclaims

- No factorized transition route implementation.
- No d=18 spatial SIR filtering.
- No filtering correctness.
- No production spatial SIR readiness.
- No HMC readiness.
- No GPU readiness.

## Required Repair

Before P52-M5/M6 can select ranks or run d=18 filtering, BayesFilter needs an
implemented TensorFlow factorized transition application that avoids dense
all-pairs materialization and emits deterministic replay, `R_eff`, and memory
metadata.
