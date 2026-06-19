# P8j Phase 4 Subplan: OT-Resampled LEDH-PFPF-OT SIR Smoke

metadata_date: 2026-06-17
status: REVIEWED_READY_TO_EXECUTE
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 4
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Run a minimal one-seed/N=4 OT-resampled Algorithm 1 UKF LEDH SIR smoke using
the inherited P8h covariance-carry route:

`ot_sinkhorn_barycentric_covariance_carry`

This phase tests whether the serious OT-resampled route can execute on SIR d18.
It does not tune particles, run five seeds, refresh the leaderboard, or claim
gradient/HMC readiness.

## Entry Conditions Inherited From Previous Phase

- Phase 3 no-OT LEDH SIR smoke is finite.
- Claude has reviewed Phase 3 result and returned `VERDICT: AGREE`.
- Phase 4 subplan has Claude `VERDICT: AGREE`.
- Fixed-parameter SIR has no free theta; score/Hessian/theta-gradient/HMC/NUTS
  claims remain forbidden.

## Required Artifacts

- Phase 4 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-result-2026-06-17.md`
- Smoke JSON if execution is finite:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-2026-06-17.json`
- Updated P8j execution ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md`
- Updated P8j Claude review ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md`
- Draft Phase 5 subplan, only if Phase 4 passes:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-subplan-2026-06-17.md`

## Required Checks/Tests/Reviews

Local checks before smoke:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "sir_dpf"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-subplan-2026-06-17.md
```

Minimal OT LEDH smoke:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY'
import json
from pathlib import Path
import tensorflow as tf
import scripts.filtering_value_gradient_benchmark_run_p8d_numeric as p8d

seed = 81120
particle_count = 4
result = p8d._dpf_single_run(
    p8d.LEDH_ALG1_DPF,
    row_id=p8d.SIR_ROW,
    seed=seed,
    particle_count=particle_count,
    resampling_route=p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
    sinkhorn_epsilon=1.0,
    sinkhorn_iterations=200,
    sinkhorn_tolerance=1e-6,
)
log_likelihood = tf.convert_to_tensor(result.log_likelihood_estimate, dtype=tf.float64)
ess = tf.convert_to_tensor(result.ess_by_time, dtype=tf.float64)
payload = {
    "phase": "P8J_PHASE4_OT_LEDH_SIR_SMOKE",
    "schema_version": "filter_bench.p8j.ot_ledh_sir_smoke.v1",
    "status": (
        "executed_one_seed_ot_ledh_sir_smoke"
        if bool(result.finite)
        else "blocked_one_seed_ot_ledh_sir_smoke_nonfinite"
    ),
    "row_id": p8d.SIR_ROW,
    "algorithm_id": p8d.LEDH_ALG1_DPF,
    "resampling_route": p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
    "sinkhorn_epsilon": 1.0,
    "sinkhorn_iterations": 200,
    "sinkhorn_tolerance": 1e-6,
    "particle_count": particle_count,
    "seed": seed,
    "seed_count": 1,
    "finite": bool(result.finite),
    "log_likelihood": float(log_likelihood.numpy()),
    "average_log_likelihood": float((log_likelihood / tf.cast(20, tf.float64)).numpy()),
    "effective_sample_size_min": float(tf.reduce_min(ess).numpy()),
    "effective_sample_size_mean": float(tf.reduce_mean(ess).numpy()),
    "resampling_count": int(result.resampling_count),
    "method_id": result.method_id,
    "route_identifiers": dict(getattr(result, "route_identifiers", {})),
    "nonclaims": [
        "one-seed N=4 OT LEDH smoke only",
        "not five-seed DPF value evidence",
        "not particle-count adequacy",
        "not leaderboard completion",
        "not score, Hessian, theta-gradient, HMC, or NUTS evidence",
    ],
}
out = Path("docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-2026-06-17.json")
out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(payload["status"])
PY
```

Claude read-only review of the Phase 4 result and any implementation repair is
required before Phase 5.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the inherited OT covariance-carry LEDH-PFPF-OT route execute one SIR d18 smoke without nonfinite values or route metadata mismatch? |
| Baseline/comparator | Phase 3 no-OT LEDH smoke and P8h reviewed OT covariance-carry route. |
| Primary criterion | Focused tests pass and one-seed/N=4 OT LEDH smoke is finite with route identifiers showing the inherited OT covariance-carry route, or a reviewed blocker records the exact failure. |
| Veto diagnostics | Treating one-seed N=4 smoke as particle adequacy; treating OT smoke as leaderboard evidence; missing/incorrect OT route metadata; changing SIR model/data; claiming score/Hessian/theta-gradient/HMC/NUTS readiness; claiming Zhao-Cui TT/SIRT source-faithfulness. |
| Explanatory diagnostics | Log likelihood, ESS, resampling count, route identifiers, finite flags, runtime. |
| Not concluded | Five-seed value evidence, particle-count adequacy, leaderboard completion, exact source-filter correctness, gradient/HMC readiness, production readiness. |

## Forbidden Claims/Actions

- Do not change SIR model/data definitions.
- Do not tune particles or refresh leaderboard.
- Do not promote N=4/N=8 or one-seed smoke to adequacy.
- Do not claim score/Hessian/theta-gradient/HMC/NUTS evidence.
- Do not claim exact source-filter correctness, Zhao-Cui TT/SIRT parity,
  MATLAB parity, or production readiness.
- Do not stage, commit, merge, or push.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only if:

- Phase 4 OT smoke is finite;
- Phase 4 result preserves all smoke-only nonclaims;
- Claude returns `VERDICT: AGREE` on Phase 4 result and any repair;
- Phase 5 particle-count tuning subplan is drafted and reviewed.

If Phase 4 writes a blocker, execution stops or enters a reviewed Phase 4 repair
loop.  A blocker does not authorize particle tuning.

## Stop Conditions

Stop and write a blocker if:

- OT LEDH SIR smoke is nonfinite and the failure is not a small route/callback
  repair;
- route identifiers do not show the reviewed OT covariance-carry route;
- runtime exceeds a short smoke budget of about five minutes;
- repair would require changing SIR model/data definitions;
- Claude review does not converge after five rounds for the same blocker.

## Skeptical Plan Audit

This phase could mislead us if a finite OT smoke is treated as a tuned
leaderboard result.  The artifact therefore records one-seed/N=4 limits, route
metadata, and nonclaims, leaving particle-count tuning and five-seed evidence to
later reviewed phases.

Execution note: the inherited OT covariance-carry route should use the same
Sinkhorn solver settings as the P8h profile path (`epsilon=1.0`,
`iterations=200`, `tolerance=1e-6`).  The default `_dpf_single_run()` values
(`epsilon=0.5`, `iterations=80`, `tolerance=1e-7`) are too strict for the SIR
d18 smoke and can fail with `Sinkhorn row residual exceeded tolerance envelope`;
that failure is a command-configuration defect for this phase, not evidence
against the SIR model.
