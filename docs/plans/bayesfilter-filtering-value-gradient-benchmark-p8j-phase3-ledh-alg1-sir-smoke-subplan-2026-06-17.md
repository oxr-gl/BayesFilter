# P8j Phase 3 Subplan: Algorithm 1 UKF LEDH SIR Smoke

metadata_date: 2026-06-17
status: DRAFT_PENDING_PHASE2_CLAUDE_REVIEW_AND_CLAUDE_SUBPLAN_REVIEW
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 3
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Run a minimal no-OT Algorithm 1 UKF LEDH smoke on the fixed-parameter SIR d18
row using the Phase 2 callback route.  This phase tests whether the richer
LEDH callback surface is executable for SIR; it does not test OT resampling,
particle-count adequacy, five-seed value evidence, leaderboard completion, or
gradient/HMC readiness.

## Entry Conditions Inherited From Previous Phase

- Phase 2 implementation/result packet has Claude `VERDICT: AGREE`.
- `_has_dpf_route(SIR_ROW)` is true.
- SIR callback semantic tie-out tests pass.
- One-seed N=4 bootstrap SIR smoke is finite.
- Fixed-parameter SIR has no free theta; score/Hessian/theta-gradient/HMC/NUTS
  claims remain forbidden.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-result-2026-06-17.md`
- Smoke JSON if execution is finite:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-2026-06-17.json`
- Updated P8j execution ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md`
- Updated P8j Claude review ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md`
- Draft Phase 4 subplan, only if Phase 3 passes:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-subplan-2026-06-17.md`

## Required Checks/Tests/Reviews

Local checks before smoke:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "sir_dpf"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-subplan-2026-06-17.md
```

Minimal no-OT LEDH smoke:

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
    resampling_route="none",
)
log_likelihood = tf.convert_to_tensor(result.log_likelihood_estimate, dtype=tf.float64)
ess = tf.convert_to_tensor(result.ess_by_time, dtype=tf.float64)
payload = {
    "phase": "P8J_PHASE3_LEDH_ALG1_SIR_SMOKE",
    "schema_version": "filter_bench.p8j.ledh_alg1_sir_smoke.v1",
    "status": (
        "executed_one_seed_ledh_alg1_sir_smoke"
        if bool(result.finite)
        else "blocked_one_seed_ledh_alg1_sir_smoke_nonfinite"
    ),
    "row_id": p8d.SIR_ROW,
    "algorithm_id": p8d.LEDH_ALG1_DPF,
    "resampling_route": "none",
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
        "one-seed N=4 no-OT LEDH smoke only",
        "not OT-resampled LEDH-PFPF-OT evidence",
        "not five-seed DPF value evidence",
        "not particle-count adequacy",
        "not leaderboard completion",
        "not score, Hessian, theta-gradient, HMC, or NUTS evidence",
    ],
}
out = Path("docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-2026-06-17.json")
out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(payload["status"])
PY
```

Claude read-only review of the Phase 3 result and any implementation repair is
required before Phase 4.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the reviewed SIR d18 callback route execute one no-OT Algorithm 1 UKF LEDH smoke without nonfinite values or semantic drift? |
| Baseline/comparator | Phase 2 callback tests and one-seed bootstrap smoke; existing no-OT LEDH implementation path for non-SIR rows. |
| Primary criterion | Focused tests pass and one-seed N=4 no-OT LEDH smoke is finite, or a reviewed blocker records the exact failure. |
| Veto diagnostics | Treating no-OT smoke as OT result; treating one seed or N=4/N=8 as particle adequacy; changing SIR model/data; claiming score/Hessian/theta-gradient/HMC/NUTS readiness; claiming Zhao-Cui TT/SIRT source-faithfulness. |
| Explanatory diagnostics | Log likelihood, ESS, resampling count, route identifiers, finite flags, runtime. |
| Not concluded | OT SIR readiness, five-seed value evidence, particle-count adequacy, leaderboard completion, exact source-filter correctness, gradient/HMC readiness, production readiness. |

## Forbidden Claims/Actions

- Do not change SIR model/data definitions.
- Do not run OT-resampled LEDH in Phase 3.
- Do not tune particles or refresh leaderboard.
- Do not promote N=4/N=8 or one-seed smoke to adequacy.
- Do not claim score/Hessian/theta-gradient/HMC/NUTS evidence.
- Do not claim exact source-filter correctness, Zhao-Cui TT/SIRT parity,
  MATLAB parity, or production readiness.
- Do not stage, commit, merge, or push.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only if:

- Phase 3 smoke is finite;
- Phase 3 result preserves all smoke-only nonclaims;
- Claude returns `VERDICT: AGREE` on Phase 3 result and any repair;
- Phase 4 OT-resampled LEDH-PFPF-OT SIR smoke subplan is drafted and reviewed.

If Phase 3 writes a blocker, execution stops or enters a reviewed Phase 3 repair
loop.  A blocker does not authorize advancing to Phase 4.

## Stop Conditions

Stop and write a blocker if:

- no-OT LEDH SIR smoke is nonfinite and the failure is not a small callback
  repair;
- runtime exceeds a short smoke budget of about five minutes;
- repair would require changing SIR model/data definitions;
- Claude review does not converge after five rounds for the same blocker.

## Skeptical Plan Audit

This phase could mislead us if a finite no-OT LEDH smoke is treated as proof of
the serious OT-resampled route.  The smoke therefore fixes `resampling_route`
to `none`, records one-seed/N=4 limits, and leaves OT, tuning, and leaderboard
evidence to later reviewed phases.
