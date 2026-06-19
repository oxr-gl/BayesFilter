# P8j Phase 2 Subplan: Bootstrap SIR d18 Smoke Implementation

metadata_date: 2026-06-17
status: DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 2
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Implement and test the minimal SIR d18 DPF callback route required for
`bootstrap_dpf_current`, then run a small deliberate CPU bootstrap smoke.  This
phase admits the SIR row into the DPF route table but does not tune particles,
run LEDH, run OT, or refresh the leaderboard.

## Entry Conditions Inherited From Previous Phase

- Phase 0 established that SIR d18 DPF callbacks are missing.
- Phase 1 callback contract passed Claude review.
- Fixed-parameter SIR has no free theta; score/Hessian/theta-gradient/HMC/NUTS
  claims remain forbidden.
- `DPF_PARTICLE_COUNT=8` is historical/smoke-only and must not be promoted to
  leaderboard adequacy.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-result-2026-06-17.md`
- Optional smoke JSON if command execution is finite:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-2026-06-17.json`
- Updated P8j execution ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md`
- Updated P8j Claude review ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md`
- Draft Phase 3 subplan, only if Phase 2 passes:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-subplan-2026-06-17.md`

## Required Checks/Tests/Reviews

Allowed implementation files:

- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`

Local checks after implementation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "source_scope_and_route_policy or spatial_sir_value_only or sir_dpf"
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_p57_m1_author_sir_callback_parity.py -q
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-subplan-2026-06-17.md
```

Minimal bootstrap smoke after focused tests pass:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY'
import json
from pathlib import Path
import tensorflow as tf
import scripts.filtering_value_gradient_benchmark_run_p8d_numeric as p8d

seed = 81120
particle_count = 4
callbacks, observations, route_label, horizon = p8d._dpf_route(p8d.SIR_ROW)
result = p8d._dpf_single_run(
    p8d.BOOTSTRAP_DPF,
    row_id=p8d.SIR_ROW,
    seed=seed,
    particle_count=particle_count,
)
log_likelihood = tf.convert_to_tensor(result.log_likelihood_estimate, dtype=tf.float64)
ess = tf.convert_to_tensor(result.ess_by_time, dtype=tf.float64)
payload = {
    "phase": "P8J_PHASE2_BOOTSTRAP_SIR_SMOKE",
    "schema_version": "filter_bench.p8j.bootstrap_sir_smoke.v1",
    "status": (
        "executed_one_seed_bootstrap_sir_smoke"
        if bool(result.finite)
        else "blocked_one_seed_bootstrap_sir_smoke_nonfinite"
    ),
    "row_id": p8d.SIR_ROW,
    "algorithm_id": p8d.BOOTSTRAP_DPF,
    "route_label": route_label,
    "horizon": int(horizon),
    "observation_shape": list(observations.shape),
    "particle_count": particle_count,
    "seed": seed,
    "seed_count": 1,
    "finite": bool(result.finite),
    "log_likelihood": float(log_likelihood.numpy()),
    "average_log_likelihood": float((log_likelihood / tf.cast(horizon, tf.float64)).numpy()),
    "effective_sample_size_min": float(tf.reduce_min(ess).numpy()),
    "effective_sample_size_mean": float(tf.reduce_mean(ess).numpy()),
    "resampling_count": int(result.resampling_count),
    "method_id": result.method_id,
    "route_identifiers": dict(getattr(result, "route_identifiers", {})),
    "nonclaims": [
        "one-seed N=4 smoke only",
        "not five-seed DPF value evidence",
        "not particle-count adequacy",
        "not leaderboard completion",
        "not score, Hessian, theta-gradient, HMC, or NUTS evidence",
    ],
}

out = Path("docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-2026-06-17.json")
out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(payload["status"])
PY
```

Claude read-only review of the implementation diff, focused test output, and
Phase 2 result is required before Phase 3.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the SIR d18 row be admitted to the DPF route table and execute a minimal bootstrap smoke without changing model/data semantics or overclaiming particle adequacy? |
| Baseline/comparator | Phase 1 callback contract, current SIR deterministic route, author-source SIR parity tests, existing bootstrap DPF callback interface. |
| Primary criterion | Focused tests pass, `_has_dpf_route(SIR_ROW)` is true, callback semantic tie-outs pass, and one-seed N=4 bootstrap smoke through `_dpf_single_run()` returns a finite value or a recorded blocker reason with explicit one-seed smoke schema. |
| Veto diagnostics | Any SIR model/data change; shape-only callback admission without semantic tie-outs; clipping policy drift; nonfinite smoke hidden as pass; N=4 or N=8 smoke promoted to particle adequacy; score/Hessian/theta-gradient/HMC/NUTS claim. |
| Explanatory diagnostics | Smoke log likelihood, ESS, resampling count, route metadata, callback metadata, runtime. |
| Not concluded | LEDH SIR readiness, OT SIR readiness, five-seed value, particle-count adequacy, leaderboard completion, exact source-filter correctness, gradient/HMC readiness, production readiness. |

## Implementation Tasks

1. Add `_dpf_sir_callbacks()` to
   `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py` following
   the Phase 1 contract.
2. Add SIR to `_dpf_route()` with route label
   `spatial_sir_austria_j9_T20` and horizon `20`.
3. Add SIR to `_has_dpf_route()`.
4. Update route-policy test to expect SIR DPF route admission.
5. Add SIR callback contract tests:
   - required keys and metadata;
   - shapes and finite values;
   - semantic tie-outs to `zhao_cui_sir_austria_model()`;
   - infectious-selector Jacobian;
   - clip-only-susceptible behavior;
   - route label/horizon.
6. Add or adapt a bootstrap smoke test for a short SIR row with one seed and
   low particle count, explicitly labeled smoke-only and not routed through
   `_numeric_dpf_cell()` five-seed status/schema.
7. Run focused tests and minimal smoke command.
8. Write Phase 2 result with pass/blocker decision.

## Forbidden Claims/Actions

- Do not change SIR model/data definitions.
- Do not change source-scope or adapter-matrix semantics unless a focused test
  proves a mechanical metadata update is required; if so, stop and document.
- Do not tune particles or refresh leaderboard.
- Do not run LEDH/OT SIR numerics in Phase 2.
- Do not claim score/Hessian/theta-gradient/HMC/NUTS evidence.
- Do not claim exact source-filter correctness, Zhao-Cui TT/SIRT parity,
  MATLAB parity, or production readiness.
- Do not stage, commit, merge, or push.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if:

- focused tests pass;
- bootstrap smoke is finite or a reviewed blocker is written;
- Phase 2 result records smoke-only limits and preserves no-free-theta claims;
- Claude returns `VERDICT: AGREE` on the Phase 2 result/diff packet;
- Phase 3 Algorithm 1 UKF LEDH SIR smoke subplan is drafted and reviewed.

## Stop Conditions

Stop and write a blocker if:

- callback semantic tie-outs fail;
- bootstrap smoke is nonfinite for reasons not fixable by the callback route;
- tests require changing SIR model/data definitions;
- runtime exceeds a short smoke budget of about five minutes;
- Claude review does not converge after five rounds for the same blocker.

## Skeptical Plan Audit

This phase could mislead us if finite bootstrap smoke is treated as a
leaderboard result or particle-count decision.  The smoke therefore uses
deliberate CPU-only execution with tiny N/seed count, labels those limits in
the artifact, and leaves tuning and five-seed evidence to later phases.
