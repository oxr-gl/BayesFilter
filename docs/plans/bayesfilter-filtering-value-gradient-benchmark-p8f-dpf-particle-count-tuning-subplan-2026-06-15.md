# P8f Subplan: DPF Particle-Count Tuning Gate

Date: 2026-06-15

Status: `SUPERSEDED_BY_P8G_GPU_LEDHPFPF_GRADIENT_PROGRAM`

## Scope

Tune DPF particle counts for the P8d DPF rows before any serious DPF value
comparison or full P8d rerun. This phase starts after P8e repaired the
`ledh_pfpf_alg1_ukf_current` SV adapter finite-execution blocker.

P8f is limited to DPF value stability. It does not tune deterministic filters,
does not implement Zhao-Cui adapters, does not revive CUT4 on Spatial SIR, and
does not certify DPF gradients.

Supersession note: after user review on 2026-06-15, value-only tuning is no
longer sufficient for the DPF lane. LEDH gradients and GPU execution are core
requirements for HMC-facing usefulness. Execute
`docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-gpu-ledh-gradient-dpf-program-2026-06-15.md`
instead; reuse this P8f plan only as the value-tuning component inside P8g.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What particle count is needed for each executable P8d DPF algorithm/row so five fixed-seed value summaries have acceptable Monte Carlo stability and no veto diagnostics? |
| Baseline/comparator | Current P8d DPF wiring with `DPF_PARTICLE_COUNT = 8`, five seeds `[81120, 81121, 81122, 81123, 81124]`, and P8e repaired LEDH SV adapters. |
| Primary criterion | For each executable DPF cell, choose the smallest tested particle count whose five-seed MC SE, relative ESS, and mandatory next-rung stability diagnostics satisfy the predeclared row-specific gate, or mark the cell `BLOCK_DPF_PARTICLE_TUNING_NOT_CONVERGED`. |
| Veto diagnostics | Any non-finite result; relative ESS collapse below the row gate at the selected particle count; unstable MC SE across ladder increases; missing next-rung stability evidence for a selected count; wall-time/resource blowup; treating `N=8` as serious evidence; ranking filters before tuning converges; changing model/data definitions to make tuning pass. |
| Explanatory diagnostics | Per-seed log likelihoods, MC SE, sample SD, min/mean ESS, min/mean relative ESS, resampling counts, runtime, adjacent-rung mean deltas, and adjacent-rung combined MC SE. |
| Not concluded | No gradient certification, no final filter ranking, no Bayesian-estimation readiness, no proof of asymptotic correctness, and no Zhao-Cui source-faithful production equivalence. |
| Artifacts | P8f tuning JSON/CSV/Markdown outputs plus `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8f-dpf-particle-count-tuning-result-2026-06-15.md`. |

## Skeptical Plan Audit

- Wrong-baseline risk: P8f must compare against the current repaired P8d/P8e
  DPF code, not historical LEDH-PFPF-OT results.
- Proxy-metric risk: ESS and MC SE are tuning diagnostics, not scientific
  ranking criteria.
- Missing-stop risk: the ladder must stop on non-finite runs, resource blowup,
  missing next-rung confirmation, or failure to improve after the maximum tested
  particle count.
- Unfair-comparison risk: bootstrap and LEDH may require different particle
  counts; choosing one global count is allowed only if it satisfies every
  retained cell's gate.
- Artifact-answer risk: the output must preserve both passing selected counts
  and blocked/non-converged counts. Silent omission is a failure.

Audit status: `PASS_FOR_REVIEW`. The plan is bounded and answers a tuning
question without crossing model, source-route, product-capability, or
scientific-claim boundaries.

## Review Record

Claude read-only local-file review:

- Round 1: `VERDICT: REVISE`.
- Fixes applied: relative ESS gate, mandatory next-rung confirmation, staged
  CPU feasibility probe, per-cell runtime stop rules, and explicit tuning
  verdict artifact fields.
- Round 2: `VERDICT: AGREE`.

Codex local review agrees that the revised plan is consistent with P8e,
feasible as a staged gate, and boundary-safe for the next phase.

## Candidate Rows

Run only cells with existing P8d DPF routes:

- `bootstrap_dpf_current`:
  - `benchmark_lgssm_exact_oracle_m3_T50`;
  - `zhao_cui_sv_actual_nongaussian_T1000`;
  - `zhao_cui_predator_prey_T20`;
  - `zhao_cui_generalized_sv_synthetic_from_estimated_values`.
- `ledh_pfpf_alg1_ukf_current`:
  - `benchmark_lgssm_exact_oracle_m3_T50`;
  - `zhao_cui_sv_actual_nongaussian_T1000`;
  - `zhao_cui_predator_prey_T20`;
  - `zhao_cui_generalized_sv_synthetic_from_estimated_values`.

Keep KSC and Spatial SIR DPF rows out of P8f unless a separate callback plan
materializes them first.

## Staged Ladder

Use five fixed seeds for every ladder point:

```text
[81120, 81121, 81122, 81123, 81124]
```

Stage 0 is a CPU-only feasibility probe, not tuning evidence:

```text
horizon prefix in [50, 200]
N in [16]
rows: the two SV-style LEDH rows first, then the remaining executable DPF rows
```

Stage 0 pass criteria:

- all probed rows are finite;
- row runtime can be projected to the next full-horizon rung without exceeding
  a per-cell supervisor budget recorded in the result artifact;
- the result records that prefix-horizon diagnostics are explanatory only.

Stage 1 is full-horizon tuning, run one algorithm/row cell at a time:

```text
N in [16, 32, 64, 128]
```

Do not run the full ladder for all cells as a single unattended CPU job. P8e
already showed that five-seed full-horizon LEDH `N=8` on two SV-style rows took
`725.942s`; P8f must therefore gate each cell independently and stop before
starting a larger rung when runtime projections exceed the recorded budget.

Escalate to GPU only under a separate GPU run contract if CPU wall time makes
the ladder infeasible. GPU commands require escalated permissions and GPU
status artifacts.

## Preliminary Gates

Before the ladder:

1. Add a runner or helper that executes selected DPF cells over a particle
   ladder without editing global `DPF_PARTICLE_COUNT` for unrelated P8d runs.
2. Emit a manifest with commit, dirty state, command, environment, CPU/GPU
   status, seeds, particle ladder, rows, algorithms, and output paths.
3. Add focused tests for schema, selected-count logic, blocked-cell retention,
   and nonclaim text.
4. Add explicit tuning verdict fields to the artifact schema:
   - `tuning_status`;
   - `selected_particle_count`;
   - `selection_rule`;
   - `selection_rung`;
   - `next_rung_checked`;
   - `next_rung_particle_count`;
   - `adjacent_mean_delta`;
   - `adjacent_combined_mc_se`;
   - `min_relative_ess`;
   - `mean_relative_ess`;
   - `runtime_budget_status`;
   - `blocker_reason` when no count is selected.

## Selection Gate

For a particle count to be selected for a cell:

- all five seeds must be finite;
- min relative ESS over all time/seed must be at least `0.25` for the selected
  count, where relative ESS is `ESS / particle_count`, unless a reviewed
  row-specific exception is recorded before seeing that cell's result;
- MC SE must be no worse than `max(2.0, 0.25% * abs(mean_log_likelihood))`;
- the next larger rung must be run before a non-terminal rung can be selected;
- the next larger rung must not shift the mean by more than
  `2 * combined_MC_SE + 1.0`;
- the terminal rung `N=128` can be selected only if it satisfies the finite,
  relative-ESS, and MC-SE gates and the result explicitly records that no larger
  CPU rung was attempted; otherwise mark the cell blocked or request a reviewed
  GPU/full-rung extension;
- runtime must remain feasible for a P8d rerun.

If no tested count passes, mark the cell blocked and record the smallest
discriminating next action.

## Local Checks

Required before any result closeout:

```bash
python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q
git diff --check
```

Any new P8f runner/test files must be added to the compile and pytest command.

## Stop Conditions

- Stop if the ladder shows severe degeneracy that does not improve by `N=128`.
- Stop if Stage 0 projects infeasible full-horizon runtime for a cell and no
  GPU run has been explicitly authorized.
- Stop if a full-horizon cell exceeds the recorded per-cell runtime budget
  before completing the next-rung confirmation needed for selection.
- Stop if passing requires changing benchmark observations, truth parameters,
  or likelihood formulas.
- Stop if a review finds the selection gate is being used as a filter-ranking
  criterion rather than a tuning gate.

## Next-Subplan Review Checklist

The reviewer must check:

- consistency with P8e adapter metadata and nonclaims;
- correctness of finite/ESS/MC-SE gates;
- feasibility of CPU ladder runtime;
- artifact coverage for pass and block outcomes;
- boundary safety around GPU use, model data, Zhao-Cui lanes, and scientific
  claims.
