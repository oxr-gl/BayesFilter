# P8o Result: SIR d18 DPF Particle Adequacy And Leaderboard Closure

metadata_date: 2026-06-18
status: PASS_SELECT_N10000_FOR_VALUE_ONLY_SIR_D18_DPF_CELL
plan: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-sir-d18-dpf-particle-adequacy-leaderboard-plan-2026-06-18.md
executor: Codex
reviewer: Claude Opus/max effort, read-only

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Select `N=10000` for the value-only SIR d18 DPF LEDH-PFPF-OT leaderboard cell under the current batched TF32/GPU streaming route. |
| Primary criterion status | Passed.  `N=10000` is finite, GPU-backed, five-seed, under the MC SE threshold, and adjacent-stable against `N=50000`. |
| Veto diagnostic status | No active veto.  Metadata checks passed for row/model, seeds, GPU, TF32, full-history route, transport policy, Sinkhorn settings, and chunks. |
| Main uncertainty | This is value-only SIR d18 evidence for the experimental batched streaming route; it is not exact likelihood correctness, gradient, HMC, TT/SIRT, MATLAB, or production evidence. |
| Next justified action | Use the P8o leaderboard-cell note when refreshing the SIR d18 DPF value evidence table; do not broaden claims beyond this cell. |
| What is not concluded | Exact nonlinear likelihood correctness, posterior convergence, DPF gradient correctness, HMC/NUTS readiness, Zhao-Cui TT/SIRT or MATLAB parity, production/default readiness, or cross-model default readiness. |

## Checks And Reviews

Pre-execution checks:

```bash
python -m py_compile docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-sir-d18-dpf-particle-adequacy-leaderboard-plan-2026-06-18.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-full-filter-chunk-comparison-result-2026-06-18.md
```

Both passed.

Claude plan review:

- `VERDICT: AGREE`
- Recorded in:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-claude-review-ledger-2026-06-18.md`

Execution check:

- Parsed P8n `N=10000` and `N=50000` JSON artifacts.
- Asserted finite output, GPU-backed tensors, five fixed seeds, row
  `zhao_cui_spatial_sir_austria_j9_T20`, shape `D=18`, observation dimension
  `9`, full-history mode, TF32 enabled, `active-all`, Sinkhorn 10, epsilon 1.0,
  and chunks `1024/1024/1024`.

## Artifacts

- Adequacy JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-sir-d18-dpf-particle-adequacy-2026-06-18.json`
- Adequacy CSV:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-sir-d18-dpf-particle-adequacy-2026-06-18.csv`
- Leaderboard cell note:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-sir-d18-dpf-leaderboard-cell-2026-06-18.md`
- P8n source artifacts:
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n10000-chunk1024-2026-06-18.json`
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n50000-chunk1024-2026-06-18.json`

## Adequacy Table

| N | Mean log likelihood | Sample SD | MC SE | MC SE threshold | Warm seconds | Min ESS | Gate |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 10000 | -902.830151 | 0.465599 | 0.208222 | 2.257075 | 8.629159 | 6432.781738 | pass |
| 50000 | -902.837939 | 0.228024 | 0.101975 | 2.257095 | 140.195284 | 31872.621094 | pass |

Adjacent stability:

| Field | Value |
| --- | ---: |
| Absolute mean delta | 0.0077880859375909495 |
| Combined MC SE | 0.2318521150120367 |
| Adjacent threshold | 1.4637042300240735 |
| Adjacent pass | true |

Selection:

```text
selected_particle_count = 10000
next_rung_checked = 50000
```

## Interpretation

`N=10000` is adequate for the current value-only SIR d18 DPF cell under the
selected batched TF32/GPU LEDH-PFPF-OT route.  The adjacent `N=50000` rung does
not move the five-seed mean in a practically material way under the declared
criterion, and both rungs have MC SE far below the threshold.

This updates the old P8j status: the previous small-`N` scalar/adaptive blocker
does not apply to the current batched TF32/GPU full-filter route.

## Boundary

This is a value-only DPF filtering evidence result.  The fixed-parameter SIR
row has no theta-gradient target in this lane.  Do not use this result as
evidence for gradients, HMC/NUTS, posterior convergence, exact source-filter
correctness, TT/SIRT parity, MATLAB parity, or production readiness.

## Post-Run Red Team

Strongest alternative explanation:

- The route is the current experimental batched streaming adapter, not a
  scalar Li-Coates Algorithm 1 UKF covariance-lifecycle parity proof.

What would overturn the decision:

- A later reviewed route-parity audit showing this adapter is not the intended
  leaderboard route, or a replicated adjacent ladder showing materially larger
  drift at the same settings.

Weakest part of the evidence:

- The adequacy criterion uses five fixed seeds and an adjacent high rung; it
  does not establish exact likelihood correctness against an independent
  reference.
