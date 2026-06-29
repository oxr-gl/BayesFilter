# P87 Phase 4 Subplan: Horizon-0 d18 Value And Gradient Gate

Date: 2026-06-26

Status: `REVIEWED_READY_FOR_PHASE4_EXECUTION`

## Phase Objective

Upgrade the existing SIR d18 horizon-0 smoke into a bounded value and gradient
gate while preserving the horizon-0 limitation and the Phase 2 JVP-free route
repair boundary.

## Entry Conditions Inherited From Previous Phase

- Phase 2 repaired the candidate route so the Phase 2 code/test repair scope
  has no `ForwardAccumulator` or old
  `tensorflow_forward_accumulator_for_model_log_density` backend.
- Phase 3 local SIR algebra passed under CPU-hidden local execution.
- Phase 4 may use the repaired JVP-free score route for horizon-0 evidence.
- Phase 4 still cannot claim full-history d18 filtering correctness,
  source-route correctness, HMC readiness, production readiness, or GPU
  readiness.

## Required Artifacts

- Phase 4 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase4-horizon0-d18-value-gradient-result-2026-06-26.md`
  - The result must record the CPU-only command manifest, including
    `CUDA_VISIBLE_DEVICES=-1` for Python/pytest commands.
- Focused d18 horizon-0 tests.
- Updated Phase 5 subplan.

## Required Checks/Tests/Reviews

Allowed edit scope:

- `tests/highdim/test_p81_analytical_sir_score.py`
- `bayesfilter/highdim/filtering.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase4-horizon0-d18-value-gradient-result-2026-06-26.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase5-tiny-full-history-regression-subplan-2026-06-26.md`
- P87 execution/review ledgers

Allowed read/check scope:

- The allowed edit scope above.
- `bayesfilter/highdim/models.py` and
  `tests/highdim/test_fixed_branch_derivatives.py` for read-only JVP
  regression grep and diff hygiene only, because the Phase 2 repair-scope veto
  spans those files.
- P87 plan files matched by `docs/plans/bayesfilter-highdim-zhao-cui-p87*.md`
  for diff hygiene only.

Any broader implementation edit, source-route, GPU, HMC, training, or
default-policy change requires a refreshed reviewed subplan.

Execution environment:

- Repository root: `/home/chakwong/BayesFilter`.
- Execution target: local CPU-only horizon-0 gate; no GPU/CUDA command is
  required or allowed in Phase 4.
- CPU-only enforcement: every Python/pytest command below must be launched with
  `CUDA_VISIBLE_DEVICES=-1` before TensorFlow imports.
- Python environment: current active repository Python environment used by
  Phases 2 and 3 focused checks.
- Tensor dtype: float64.
- Network/model access: none during local checks; Claude is read-only review
  only.

```text
env CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/highdim/filtering.py tests/highdim/test_p81_analytical_sir_score.py
env CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p81_analytical_sir_score.py -k "sir_d18 or parameterized_sir"
if rg -n "ForwardAccumulator|tensorflow_forward_accumulator_for_model_log_density" bayesfilter/highdim/filtering.py bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py tests/highdim/test_fixed_branch_derivatives.py; then
  echo "BLOCK_ANALYTICAL_ROUTE_HAS_JVP_COMPONENT: JVP backend remains in Phase 4 repair scope" >&2
  exit 1
fi
git diff --check -- bayesfilter/highdim/filtering.py tests/highdim/test_p81_analytical_sir_score.py docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

Claude review required for any test/implementation change and for Phase 4
result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does bounded horizon-0 SIR d18 value/score evidence pass without overclaiming full-history validation? |
| Baseline/comparator | Existing horizon-0 d18 fixed-branch result, same-branch finite differences, branch hashes, and local algebra from Phase 3. |
| Primary criterion | Finite horizon-0 value/score, valid same-branch FD rows, branch-hash stability, explicit horizon-0-only claim language, and JVP-free repair-scope grep remains clean. |
| Veto diagnostics | `BLOCK_HORIZON0_OVERCLAIM`, branch drift, nonfinite score, old JVP backend in repair scope, missing same-branch FD row, d18 all-grid transition attempt. |
| Explanatory diagnostics | FD residuals, branch hashes, backend strings, score vector/parameter coverage. |
| Not concluded | Full-history filtering likelihood, source-route correctness, HMC/production readiness, GPU readiness. |
| Artifact | Phase 4 result and tests, with CPU-only command manifest recorded. |

## Forbidden Claims/Actions

- Do not claim full-history d18 validation.
- Do not claim source-faithfulness.
- Do not use all-grid transition or GPU/long runs.
- Do not use horizon-0 evidence to close d18 full-history feasibility.
- Do not revive ALS training, training-base sweeps, rank/degree claims, or
  default-policy claims in Phase 4.

## Exact Next-Phase Handoff Conditions

Phase 5 may start only if:

- Phase 4 passes the horizon-0 gate with explicit horizon-0-only claim
  language;
- the Phase 4 result records CPU-only local commands and JVP-free repair-scope
  grep evidence;
- the Phase 5 subplan remains a tiny exact full-history regression, not a d18
  full-history run;
- Phase 5 subplan is refreshed and reviewed.

## Stop Conditions

- Horizon-0 value/score mismatch.
- Branch-hash drift.
- Old JVP backend reappears in the Phase 4 repair scope.
- Result attempts full-history, source-route, HMC, production, GPU, or
  default-policy claims.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 4 result/close record.
3. Draft or refresh Phase 5 subplan.
4. Review Phase 5 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
