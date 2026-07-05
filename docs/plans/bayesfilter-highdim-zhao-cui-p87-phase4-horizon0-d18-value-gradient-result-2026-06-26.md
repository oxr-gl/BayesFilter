# P87 Phase 4 Result: Horizon-0 d18 Value And Gradient Gate

Date: 2026-06-27

Status: `P87_PHASE4_HORIZON0_D18_VALUE_GRADIENT_PASS_REVIEWED_CLOSED`

## Decision

Phase 4 passed the bounded horizon-0 SIR d18 value/gradient gate under
CPU-hidden local execution.

The evidence supports only this claim:

> The repaired JVP-free fixed-design score route runs on the reviewed SIR d18
> horizon-0 observation-term fixture, returns finite value/score, preserves
> same-branch finite-difference rows, and keeps the Phase 2 JVP sentinel clean.

`BLOCK_HORIZON0_OVERCLAIM` remains active for every full-history d18 claim.
This phase does not establish full-history filtering likelihood correctness,
d18 transition feasibility, source-route correctness, HMC readiness,
production readiness, GPU readiness, LEDH comparison, training readiness, or a
default-policy change.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `97ad05d` |
| Repository root | `/home/chakwong/BayesFilter` |
| Execution target | CPU-only local horizon-0 gate |
| CPU-only enforcement | `CUDA_VISIBLE_DEVICES=-1` on Python/pytest commands |
| Tensor dtype | `tf.float64` |
| Network/model access | None for local checks; Claude review was external/read-only before execution |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase4-horizon0-d18-value-gradient-subplan-2026-06-26.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase4-horizon0-d18-value-gradient-result-2026-06-26.md` |

## Checks Run

```bash
env CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/highdim/filtering.py tests/highdim/test_p81_analytical_sir_score.py
```

Result: passed.

```bash
env CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p81_analytical_sir_score.py -k "sir_d18 or parameterized_sir"
```

Result: passed, `5 passed, 2 deselected, 2 warnings`.

```bash
if rg -n "ForwardAccumulator|tensorflow_forward_accumulator_for_model_log_density" bayesfilter/highdim/filtering.py bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py tests/highdim/test_fixed_branch_derivatives.py; then
  echo "BLOCK_ANALYTICAL_ROUTE_HAS_JVP_COMPONENT: JVP backend remains in Phase 4 repair scope" >&2
  exit 1
fi
```

Result: passed with no matches.

```bash
git diff --check -- bayesfilter/highdim/filtering.py tests/highdim/test_p81_analytical_sir_score.py docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

Result: passed.

## Evidence Table

| Evidence item | Status | Notes |
| --- | --- | --- |
| Horizon-0 SIR d18 score fixture | Passed | Targeted pytest includes `test_multistate_fixed_design_tt_score_path_runs_on_sir_d18_horizon0_observation_term`. |
| Finite value/score | Passed | Test asserts finite log-likelihood and finite score. |
| Same-branch FD rows | Passed | Test asserts valid FD rows and equal plus/minus/base branch hashes. |
| JVP sentinel | Passed | No `ForwardAccumulator` or old backend string in Phase 4 repair/check scope. |
| Two-row d18 all-grid transition blocker | Preserved | Targeted pytest includes the `COMPLEXITY_GATE` blocker test; no d18 full-history feasibility is claimed. |
| Horizon-0 limitation | Preserved | Result keeps `BLOCK_HORIZON0_OVERCLAIM` active. |

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Horizon-0 d18 value/gradient gate passes. |
| Primary criterion | Met for bounded horizon-0 only. |
| Veto diagnostics | No horizon-0 overclaim; no branch drift in FD rows; no nonfinite score; no old JVP backend in repair/check scope; d18 two-row all-grid transition remains blocked. |
| Main uncertainty | Tiny full-history propagation still needs exact regression; d18 full-history feasibility remains unproven. |
| Next justified action | Execute reviewed Phase 5 tiny full-history exact regression gate. |
| What is not concluded | Full-history d18 likelihood, source-route correctness, HMC/production readiness, GPU readiness, LEDH/training/default readiness. |

## Phase 5 Handoff

Phase 5 may proceed because its refreshed subplan received Claude
`VERDICT: AGREE`. It must remain a tiny d2/d3 full-history regression gate and
must not execute or claim d18 full-history feasibility.

The refreshed handoff artifact is:

- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase5-tiny-full-history-regression-subplan-2026-06-26.md`
