# LEDH-Inclusive Highdim Leaderboard Master Program

Date: 2026-07-03

Status: `DRAFT_PENDING_CLAUDE_REVIEW`

## Objective

Produce a high-dimensional leaderboard comparable to
`docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`, with LEDH-PFPF-OT
added as an explicitly governed algorithm row and compared against the existing
high-dimensional algorithms on every existing high-dimensional model row.

This program must distinguish three different facts:

- whether LEDH computed the same observed-data filtering likelihood target as
  the existing leaderboard row;
- whether LEDH produced a finite and stable value estimate with reported Monte
  Carlo uncertainty;
- whether LEDH produced the total derivative of the stated log likelihood
  target, not a partial derivative with omitted parameter dependence.

## Algorithms

The intended comparison algorithms are:

- `fixed_sgqf`;
- `ukf`;
- `zhao_cui_scalar_or_multistate`;
- `ledh_pfpf_ot`.

The current July 3 highdim leaderboard is the non-LEDH baseline. It explicitly
excluded `ledh_pfpf_alg1_ukf_current` and `ledh_pfpf_ot`, so it must not be
described as a LEDH run.

## Model Rows

The target row set is the existing highdim row set:

- `benchmark_lgssm_exact_oracle_m3_T50`;
- `zhao_cui_sv_actual_nongaussian_T1000`;
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`;
- `zhao_cui_spatial_sir_austria_j9_T20`;
- `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`;
- `zhao_cui_predator_prey_T20`;
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`.

Every row must be classified as one of:

- `full_observed_data_filtering_row`: LEDH computes the same observed-data
  filtering target as the row;
- `scoped_component_row`: LEDH computes only a component or different target;
- `blocked_no_same_target_adapter`: no admitted LEDH adapter exists for that row;
- `blocked_score_only`: value is admitted but score is not.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific or engineering question | Can LEDH-PFPF-OT be added to the existing highdim leaderboard and compared to the existing algorithms on the same model rows without hiding target mismatch, value-only evidence, or missing score terms? |
| Baseline/comparator | `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json` for non-LEDH rows; LEDH-specific rows must come from new GPU/XLA/TF32 artifacts created by this program or from explicitly cited prior LEDH artifacts with matching target and row scope. |
| Primary pass criterion | A new JSON and Markdown leaderboard artifact exists with LEDH rows for every target row, where each LEDH row is either executed with required evidence or blocked with a direct reason. At least the LGSSM row must pass value and score gates before any "full value+score LEDH row" claim is allowed. |
| Veto diagnostics | GPU/XLA/TF32 device evidence missing for LEDH runs; same-target row classification unsupported; finite outputs missing; MCSE missing for Monte Carlo value rows; total derivative not checked for claimed score rows; existing baseline rows silently modified; parameterized SIR local complete-data row treated as full observed-data filtering evidence without proof. |
| Explanatory diagnostics | compile time, steady runtime, ESS, particle-count trend, adjacent-rung value change, memory use, failed-row stack traces, and Claude review notes. These explain behavior but do not by themselves establish correctness. |
| Not concluded | No HMC readiness, posterior correctness, broad scientific superiority, exact nonlinear likelihood correctness, or production default change unless separate gates explicitly check those claims. |
| Artifacts | Master program, phase subplans, phase results, Claude review ledger, visible execution ledger, raw LEDH result JSON/MD, merged leaderboard JSON/MD, logs under `docs/plans/logs/`. |

## Comparator Provenance Rule

The final artifact must choose one of two comparator modes and label it directly:

- `frozen_non_ledh_baseline_plus_fresh_ledh`: non-LEDH rows are copied from the
  July 3 baseline with provenance labels and are value/score comparable only by
  target/status, not by runtime environment;
- `fresh_all_algorithm_rerun`: all algorithms are rerun under a shared harness,
  device policy, seed policy, and artifact schema before runtime comparisons are
  made.

The default mode for this program is
`frozen_non_ledh_baseline_plus_fresh_ledh`. Therefore runtime rankings across
LEDH and non-LEDH algorithms are forbidden unless a later reviewed phase changes
to `fresh_all_algorithm_rerun` before seeing results.

Every requested row must appear in the final artifact as one of:

- full row;
- scoped component row;
- blocked value row;
- blocked score row;
- blocked no same-target adapter row.

No requested row may be silently omitted or replaced by a different target.

## LEDH Ladder Policy

The default LEDH value ladder uses:

- seeds: `81120,81121,81122,81123,81124`;
- rungs: `N=1000` and `N=10000` for all admitted rows;
- adjacent high rung: `N=50000` only when Phase 3/4 pre-run budget estimates say
  it is feasible within the visible runtime and memory gate;
- primary value criterion: finite outputs, MCSE reported from the five-seed
  sample mean, ESS reported, and adjacent-rung mean change no larger than the
  predeclared row tolerance or else the row is value-diagnostic only;
- deviation rule: any row that cannot run both default rungs must record a
  direct blocker or a reviewed row-specific ladder before execution.

Phase 4 may refine tolerances row by row before execution, but it must not
change them after seeing row results.

## Score Admission Rule

LEDH score admission is row specific. A row can be marked
`executed_value_score` only if at least one of the following is preserved:

- an exact derivation in the repo notation showing that the implemented score is
  the total derivative of the stated row log likelihood target;
- a trusted numerical check against the same deterministic target with fixed
  random numbers and a finite-difference step policy declared before execution;
- an exact oracle comparison such as Kalman for LGSSM.

If the implemented score omits functional dependence on parameters, the score
is wrong relative to the stated total-derivative target unless the row
explicitly declares a partial-derivative target. Partial derivatives are not
MLE/HMC score evidence.

## Skeptical Plan Audit

This plan checks the main failure modes before execution:

- Wrong baseline: controlled by freezing the July 3 non-LEDH leaderboard as a
  baseline and recording that it excludes LEDH.
- Proxy metrics: runtime, compile time, ESS, and value stability can explain
  results but cannot certify score correctness or HMC readiness.
- Missing stop conditions: every phase has explicit stop conditions and a
  repair loop.
- Unfair comparisons: LEDH rows are compared only when row scope says the same
  target is computed. Otherwise the row is blocked or scoped.
- Comparator provenance: default comparison uses frozen non-LEDH baseline rows
  and fresh LEDH rows, so runtime cross-ranking is forbidden unless all
  algorithms are rerun under a shared harness.
- Hidden assumptions: GPU/XLA/TF32, particle count, seeds, transport policy,
  and score route must be written into artifacts.
- Stale context: the row inventory is read from the current runner and July 3
  leaderboard before implementation.
- Environment mismatch: GPU work must use escalated trusted execution per
  `AGENTS.md`.
- Non-answering artifacts: every run must write structured JSON/MD preserving
  row status, MCSE, score status, and device metadata.

Audit result: `PLAN_SURFACE_READY_FOR_BOUNDED_CLAUDE_REVIEW`.

## Phase Index

| Phase | Name | Subplan | Required result |
| --- | --- | --- | --- |
| 0 | Launch Boundary Freeze | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase0-launch-boundary-freeze-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase0-launch-boundary-freeze-result-2026-07-03.md` |
| 1 | Row Admission And Adapter Inventory | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-adapter-inventory-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-adapter-inventory-result-2026-07-03.md` |
| 2 | Runner And Artifact Schema | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase2-runner-schema-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase2-runner-schema-result-2026-07-03.md` |
| 3 | Tiny GPU/XLA Value And Score Gates | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-tiny-gpu-xla-gates-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-tiny-gpu-xla-gates-result-2026-07-03.md` |
| 4 | LEDH Particle Ladders | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-ledh-particle-ladders-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-ledh-particle-ladders-result-2026-07-03.md` |
| 5 | Merge And Cross-Algorithm Comparison | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase5-merge-comparison-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase5-merge-comparison-result-2026-07-03.md` |
| 6 | Closeout And Reset Memo | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase6-closeout-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase6-closeout-result-2026-07-03.md` |

## Repair Loop

For each phase:

1. run local checks named in the phase subplan;
2. write the phase result or blocker result;
3. draft or refresh the next subplan;
4. ask Claude for bounded read-only review when the phase is material;
5. patch fixable plan or implementation defects visibly;
6. repeat Claude review for the same blocker at most five times;
7. stop and ask for human direction if the same material blocker remains.

Claude is a reviewer only. Claude cannot authorize changing pass criteria,
model target, runtime permissions, scientific claims, package installs, or
default policy.

## Anticipated Approvals

The following operations will need trusted or escalated execution:

- `claude -p` or the local Claude wrapper for read-only reviews;
- `nvidia-smi`;
- TensorFlow GPU/XLA/TF32 probes and GPU benchmark runs;
- long LEDH particle ladder runs.

No network package install, destructive git command, or detached agent launch is
part of this plan.
