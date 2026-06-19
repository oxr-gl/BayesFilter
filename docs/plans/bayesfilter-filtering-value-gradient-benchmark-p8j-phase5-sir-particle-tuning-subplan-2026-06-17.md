# P8j Phase 5 Subplan: SIR d18 Particle-Count Tuning

metadata_date: 2026-06-17
status: DRAFT_PENDING_PHASE4_CLAUDE_REVIEW_AND_CLAUDE_SUBPLAN_REVIEW
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 5
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Implement and execute a SIR-specific DPF particle-count tuning gate for:

- row: `zhao_cui_spatial_sir_austria_j9_T20`;
- bootstrap comparator: `bootstrap_dpf_current`;
- serious LEDH route: `ledh_pfpf_alg1_ukf_current` with
  `ot_sinkhorn_barycentric_covariance_carry`;
- fixed seeds: `81120,81121,81122,81123,81124`;
- full SIR horizon: `T=20`.

This phase must select a reviewed particle count for Phase 6 leaderboard
refresh, or write a blocker.  It must not treat the historical `N=8` P8d wiring
count or one-seed/N=4 smokes as adequate.

## Entry Conditions Inherited From Previous Phase

- Phase 4 OT-resampled LEDH SIR smoke is finite.
- Phase 4 result preserves smoke-only nonclaims.
- Claude has reviewed Phase 4 result and returned `VERDICT: AGREE`.
- This Phase 5 subplan has Claude `VERDICT: AGREE`.
- The row remains fixed-parameter SIR with no free theta; score,
  Hessian, theta-gradient, HMC, and NUTS claims remain forbidden.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-result-2026-06-17.md`
- Tuning JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-2026-06-17.json`
- Tuning CSV:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-2026-06-17.csv`
- Selected/blocker CSV:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-selected-blocked-2026-06-17.csv`
- Updated P8j execution ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md`
- Updated P8j Claude review ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md`
- Draft Phase 6 subplan, only if Phase 5 selects a particle count:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase6-sir-leaderboard-refresh-subplan-2026-06-17.md`

## Required Checks/Tests/Reviews

Local pre-implementation checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "sir_dpf"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-subplan-2026-06-17.md
```

Implementation scope:

- Add a P8j SIR particle-tuning helper or CLI mode to
  `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`.
- Reuse `_dpf_single_run()` and `_dpf_route(SIR_ROW)`; do not modify SIR model,
  observations, or callback semantics.
- For bootstrap runs use `resampling_route="none"`.
- For LEDH runs use:
  - `resampling_route=P8H_DEFAULT_RESAMPLING_ROUTE`;
  - `sinkhorn_epsilon=1.0`;
  - `sinkhorn_iterations=200`;
  - `sinkhorn_tolerance=1e-6`.
- Add focused tests that cover:
  - SIR-only admission;
  - exactly five seeds for value evidence;
  - rejection of `N=8` as selectable tuning count;
  - selected/blocker accounting;
  - preservation of no score/Hessian/theta-gradient/HMC claims;
  - route metadata for the LEDH OT cell.

Implementation checks after patch:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "sir_dpf or p8j"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-subplan-2026-06-17.md
```

Tuning execution plan:

1. Run a Stage 0 pilot on CPU or trusted GPU with full horizon `20`, five seeds,
   algorithms `bootstrap_dpf_current,ledh_pfpf_alg1_ukf_current`, and candidate
   counts beginning above the historical P8d wiring count, for example
   `16,32`.
2. If both algorithms are finite and within runtime budget, run the adjacent
   confirmation ladder with candidates `16,32,64` unless Stage 0 runtime
   projects that this would exceed the declared budget.
3. Prefer trusted GPU for long tuning.  Any GPU command must use escalated or
   trusted permissions and record `nvidia-smi`/TensorFlow device evidence.  CPU
   execution is allowed only for short pilot/runtime projection and must not be
   promoted as final tuned-count evidence if runtime makes the full ladder
   impractical.

Selection rule:

- For each algorithm, select the smallest candidate particle count that:
  - is finite for all five seeds;
  - has MC standard error below
    `max(2.0, 0.0025 * abs(mean_log_likelihood))`;
  - is within the runtime budget;
  - has an adjacent higher-count rung;
  - has adjacent mean difference at most
    `2 * adjacent_combined_mc_se + 1.0`;
  - for LEDH OT, has passing OT route and transport diagnostics.
- If no candidate passes, write a blocker with the first material reason:
  `BLOCK_P8J_SIR_PARTICLE_TUNING_NONFINITE`,
  `BLOCK_P8J_SIR_PARTICLE_TUNING_TRANSPORT`,
  `BLOCK_P8J_SIR_PARTICLE_TUNING_GPU_EVIDENCE`,
  `BLOCK_P8J_SIR_PARTICLE_TUNING_RUNTIME_BUDGET`,
  `BLOCK_P8J_SIR_PARTICLE_TUNING_SEED_COUNT`,
  `BLOCK_P8J_SIR_PARTICLE_TUNING_MC_SE`,
  `BLOCK_P8J_SIR_PARTICLE_TUNING_ADJACENT_STABILITY`, or
  `BLOCK_P8J_SIR_PARTICLE_TUNING_MISSING_NEXT_RUNG`.

Claude read-only review of the Phase 5 implementation/result and any repair is
required before Phase 6.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What particle count, if any, is adequate for SIR d18 bootstrap and OT-resampled LEDH DPF value evidence under five fixed seeds and reviewed route metadata? |
| Baseline/comparator | Phase 2 bootstrap smoke, Phase 4 OT LEDH smoke, P8d five-seed value contract, and within-P8j adjacent-rung comparisons. |
| Primary criterion | Select the smallest count per algorithm passing five-seed finite, MC SE, runtime, adjacent-rung stability, and route/transport gates; otherwise emit a blocker. |
| Veto diagnostics | Using N=8 as selectable; fewer than five seeds; treating N=4 smoke as tuning; missing next rung; nonfinite values; failed OT transport metadata; untrusted GPU evidence for final GPU tuning; runtime budget failure; model/data mutation; score/Hessian/theta-gradient/HMC claims. |
| Explanatory diagnostics | Per-seed log likelihood, MC SE, ESS, resampling count, runtime, route identifiers, transport diagnostics, CPU/GPU device evidence. |
| Not concluded | Exact likelihood correctness, posterior convergence, DPF gradients, HMC/NUTS readiness, source-faithful TT/SIRT parity, MATLAB parity, production readiness, or final leaderboard completion. |

## Forbidden Claims/Actions

- Do not change SIR model/data definitions.
- Do not use the scalar-SV P8h tuning helper unchanged if it rejects or
  mislabels SIR; implement a SIR-specific P8j wrapper instead.
- Do not select historical `N=8`; it is wiring evidence only.
- Do not promote one-seed/N=4 smoke to particle adequacy.
- Do not use fewer than five seeds for value evidence.
- Do not claim score/Hessian/theta-gradient/HMC/NUTS evidence.
- Do not claim exact source-filter correctness, Zhao-Cui TT/SIRT parity,
  MATLAB parity, or production readiness.
- Do not stage, commit, merge, or push.

## Exact Next-Phase Handoff Conditions

Phase 6 may begin only if:

- Phase 5 selects a particle count for every requested SIR DPF leaderboard cell
  that Phase 6 will refresh, or explicitly narrows Phase 6 to only selected
  cells;
- Phase 5 result preserves no-gradient/no-HMC/no-source-faithfulness nonclaims;
- Claude returns `VERDICT: AGREE` on the Phase 5 implementation/result packet;
- Phase 6 leaderboard-refresh subplan is drafted and reviewed.

If Phase 5 writes a blocker, execution stops or enters a reviewed Phase 5
repair loop.  A blocker does not authorize leaderboard refresh.

## Stop Conditions

Stop and write a blocker if:

- final tuning would require untrusted GPU execution;
- projected runtime exceeds the declared budget and no smaller reviewed pilot
  can discriminate the next action;
- either algorithm is nonfinite at all tested candidate counts;
- LEDH OT route metadata or transport diagnostics are missing/failing;
- selection would require accepting `N=8`, one-seed smoke, or missing adjacent
  rung evidence;
- repair would require changing SIR model/data definitions;
- Claude review does not converge after five rounds for the same blocker.

## Skeptical Plan Audit

This phase could mislead us if it treats a finite small-count run as an
accuracy result or silently imports scalar-SV tuning scope.  The plan therefore
requires SIR-specific admission, five fixed seeds, adjacent-rung checks,
explicit nonclaims, and blocker records when tuning does not converge.  The
existing P8h tuning helper is useful as a schema pattern, but its initial scope
is actual-SV; SIR needs a P8j-specific wrapper or CLI path.
