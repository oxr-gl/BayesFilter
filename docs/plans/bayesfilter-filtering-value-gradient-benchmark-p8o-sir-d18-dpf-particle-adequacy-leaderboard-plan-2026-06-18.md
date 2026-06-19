# P8o Plan: SIR d18 DPF Particle Adequacy And Leaderboard Closure

metadata_date: 2026-06-18
status: DRAFT_PENDING_CLAUDE_REVIEW
lane: DPF / SIR d18 leaderboard completion
executor: Codex
reviewer: Claude Opus/max effort, read-only

## Objective

Close the SIR d18 DPF value-evidence gap using the current trusted-GPU
batched TF32 full-filter route.

The concrete target is:

- row: `zhao_cui_spatial_sir_austria_j9_T20`;
- algorithm: experimental batched TF32/GPU LEDH-PFPF-OT streaming adapter;
- particle ladder: `N=10000` and adjacent high rung `N=50000`;
- fixed seeds: `81120,81121,81122,81123,81124`;
- horizon: `T=20`;
- selected setting candidate: `row_chunk_size=1024`, `col_chunk_size=1024`,
  `particle_chunk_size=1024`, `active-all`, Sinkhorn 10, epsilon 1.0.

## Entry Conditions

- P8j established the SIR row/callback governance boundary.
- P8j old scalar/adaptive Phase 5 path is superseded for this decision by the
  P8j/P8n batched TF32/GPU full-filter harness.
- P8n current matched chunk comparison passed finite/GPU gates and selected
  `1024/1024` as the near-term SIR d18 benchmark setting.
- P8n produced current full-filter artifacts for `N=10000` and `N=50000`.

## Required Artifacts

- This plan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-sir-d18-dpf-particle-adequacy-leaderboard-plan-2026-06-18.md`
- Claude review ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-claude-review-ledger-2026-06-18.md`
- Adequacy JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-sir-d18-dpf-particle-adequacy-2026-06-18.json`
- Adequacy CSV:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-sir-d18-dpf-particle-adequacy-2026-06-18.csv`
- Leaderboard cell note:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-sir-d18-dpf-leaderboard-cell-2026-06-18.md`
- Result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-sir-d18-dpf-particle-adequacy-leaderboard-result-2026-06-18.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is `N=10000` adequate for the SIR d18 DPF LEDH-PFPF-OT value cell, given an adjacent trusted-GPU `N=50000` rung? |
| Baseline/comparator | P8n `N=10000` and `N=50000` full-filter artifacts with identical seeds/model/TF32/GPU/transport settings except particle count. |
| Primary criterion | Select the smallest rung with finite GPU output, five fixed seeds, MC SE <= `max(2.0, 0.0025 * abs(mean_log_likelihood))`, and adjacent mean delta <= `2 * combined_mc_se + 1.0`. |
| Veto diagnostics | CPU fallback, nonfinite output, fewer than five seeds, wrong row/model, wrong transport settings, missing adjacent higher rung, changed model/data, or unsupported gradient/HMC/source-faithfulness claims. |
| Explanatory diagnostics | Per-seed log likelihood, sample SD, MC SE, ESS minima, runtime, chunk sizes, memory counters, adjacent mean delta. |
| Not concluded | Exact nonlinear likelihood correctness, posterior convergence, DPF gradient correctness, HMC/NUTS readiness, Zhao-Cui TT/SIRT or MATLAB parity, production/default readiness, or cross-model default readiness. |

## Selection Rule

1. Parse P8n `N=10000` and `N=50000` current `1024/1024` JSON artifacts.
2. Verify both artifacts are finite, GPU-backed, five-seed, full SIR d18,
   `history-mode full`, TF32 enabled, `transport-policy active-all`,
   Sinkhorn 10, epsilon 1.0, and `particle_chunk_size=1024`.
3. Compute:
   - mean log likelihood;
   - sample SD;
   - MC SE;
   - MC SE threshold;
   - adjacent absolute mean delta;
   - adjacent combined MC SE;
   - adjacent threshold;
   - runtime and ESS summaries.
4. Select `N=10000` if it passes the finite/GPU/MC-SE gate and the adjacent
   `N=50000` stability gate.
5. If `N=10000` fails only adjacent stability, optionally run `N=25000` under
   the same settings after writing a focused amendment.
6. If any veto fires, write a blocker result instead of a leaderboard cell.

## Required Checks / Reviews

Pre-execution checks:

```bash
python -m py_compile docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-sir-d18-dpf-particle-adequacy-leaderboard-plan-2026-06-18.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-full-filter-chunk-comparison-result-2026-06-18.md
```

Claude read-only plan review:

- Review only this P8o plan plus named P8n artifact paths.
- Required review dimensions: consistency, correctness, feasibility, artifact
  coverage, boundary safety, and whether the selection rule is sufficient for a
  value-only SIR d18 DPF leaderboard cell.

Execution checks:

```bash
python - <<'PY'
# parse P8n JSONs, assert metadata, compute adequacy table, write JSON/CSV
PY
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-*
```

Claude read-only result review:

- Review the P8o result and leaderboard cell note against this plan.
- Claude is not an execution authority; a passing Claude review is consistency
  evidence only.

## Forbidden Claims / Actions

- Do not rerun the old slow scalar/adaptive P8j tuning harness for this
  decision.
- Do not change SIR model/data definitions.
- Do not claim score, Hessian, theta-gradient, HMC, NUTS, posterior, TT/SIRT
  source-faithfulness, MATLAB parity, or production readiness.
- Do not claim a repository-wide default chunk policy.
- Do not stage, commit, merge, or push.

## Stop Conditions

- Claude review finds a material issue that is not fixable within this plan.
- P8n artifacts fail metadata, finite, GPU, or five-seed checks.
- The adjacent `N=50000` rung is missing or mismatched.
- Selection would require changing criteria after seeing the results.
- A result would need an unsupported scientific or production claim.

## Skeptical Audit

The plan avoids the known traps:

- It treats P8n as full-filter SIR evidence, not synthetic transport-core
  evidence.
- It does not compare against the obsolete scalar/adaptive small-`N` runtime as
  the primary adequacy baseline.
- It requires an adjacent high rung before selecting `N=10000`.
- It separates value-cell adequacy from exact likelihood, gradient, HMC, and
  source-faithfulness claims.

Execution may proceed only after Claude review converges or after a visible
patch resolves material review issues.
