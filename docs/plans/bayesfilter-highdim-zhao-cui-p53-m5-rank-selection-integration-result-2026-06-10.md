# P53-M5 Result: Rank Selection Integration

metadata_date: 2026-06-10
phase: P53-M5
status: BLOCK_P53_M5_RANK_SELECTION_INTEGRATION

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can rank selection consume real scaling-route metadata and freeze a rank before HMC without adaptive branch changes? |
| Baseline/comparator | P52 rank-budget implementation, P52 UKF scout as scout-only context, P53-M4D admitted scaling-route metadata, and M4C lower-rung tie-out evidence. |
| Primary criterion | Blocked: rank selection consumed the admitted route metadata, but no candidate rank, including rank 1, is below the hard step-memory ceiling. |
| Veto diagnostics | Fired as a designed gate: memory cap would be exceeded.  Other vetoes did not fire: M4D admission is required, route metadata is present, UKF is not promoted to truth, and rank mutation inside likelihood is forbidden. |
| Nonclaims | No rank selected, no d=18 spatial SIR run, no d=50/d=100 run, no filtering correctness, no HMC readiness, no GPU readiness. |

## Blocker

The admitted exact local-neighborhood route has conservative lower-rung
metadata:

```text
R_eff = 2916
basis_order = 3
dimension = 18
candidate_ranks = {1, 2, 4, 8, 16, 32}
step_cap = 8 GiB
```

Using the P52 memory formula,

```text
M_step = bytes * d * n * (R_eff * r)^2 * omega,
```

the hard rank ceiling is:

```text
r_max = 0.
```

Even rank 1 has forecast step memory:

```text
29,386,561,536 bytes
```

which exceeds the 8 GiB step cap.  Therefore no fixed rank can be frozen for
the current admitted route under the active memory contract.

A direct d=18 local-route metadata probe with `tt_rank_left = tt_rank_right = 1`
also blocks with:

```text
local scaling route memory forecast exceeds cap
```

P53-M6 must not start from this state.

## Interpretation

This is not a TensorFlow implementation crash and not a reason to relax the
tolerance after the fact.  It is the intended rank-selection gate detecting
that the exact local-neighborhood scaling route is too wide for the current
fixed-rank memory contract.

The next fix requires a new reviewed route or policy decision, for example:

- derive and implement a smaller approximation route with explicit
  approximation status and tie-out evidence;
- derive a TT-MPO/operator-compression route whose effective transition rank is
  genuinely smaller;
- change the memory contract or claim class under a new reviewed plan.

Those are scientific/design decisions outside the current M5 repair scope.

## Manifest

Persisted manifest:

- `docs/plans/bayesfilter-highdim-zhao-cui-p53-m5-rank-selection-integration-manifest-2026-06-10.json`

Required token emitted:

`BLOCK_P53_M5_RANK_SELECTION_INTEGRATION`

Forbidden tokens:

- `PASS_P53_M5_RANK_SELECTION_INTEGRATION`;
- `PASS_P53_M6_SPATIAL_SIR_D18`;
- `PASS_P53_M7_SPATIAL_SIR_D50_D100`;
- `PASS_P53_M8_INTEGRATION_CLOSEOUT`.

## Validation

Focused validation command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p53_m5_rank_selection_integration.py tests/highdim/test_p53_m4d_scaling_route_admission.py tests/highdim/test_p53_planning_failure_lock.py
```

Result:

```text
16 passed, 2 warnings in 2.97s
```

Additional checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall bayesfilter/highdim/rank_budget.py bayesfilter/highdim/__init__.py tests/highdim/test_p53_m5_rank_selection_integration.py
git diff --check
```

Result:

```text
compileall exited 0
git diff --check exited 0
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | dirty worktree; P53 is uncommitted workspace work |
| Environment | local Python environment |
| CPU/GPU status | CPU-only planned with `CUDA_VISIBLE_DEVICES=-1`; no GPU conclusion |
| Random seeds | N/A |
| Wall time | pytest 2.97s; compile/check commands completed successfully |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m5-rank-selection-integration-subplan-2026-06-10.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m5-rank-selection-integration-result-2026-06-10.md` |
| Manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m5-rank-selection-integration-manifest-2026-06-10.json` |

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Block P53-M5 pending Claude review | No feasible fixed rank exists under admitted route metadata and 8 GiB step cap; focused validation passed | Memory cap exceeded; no adaptive rank mutation allowed | Whether a smaller approximation or TT-MPO route can reduce effective rank | Request Claude review; stop after agreement because M6 cannot start | d=18 filtering, HMC/GPU readiness, scientific rejection of Zhao-Cui |

Required token:

`BLOCK_P53_M5_RANK_SELECTION_INTEGRATION`
