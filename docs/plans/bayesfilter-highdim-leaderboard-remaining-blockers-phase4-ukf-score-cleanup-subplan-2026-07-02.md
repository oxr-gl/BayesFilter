# Phase 4 Subplan: UKF Analytical-Score Cleanup

Date: 2026-07-02

Status: `DRAFT_READY_AFTER_PHASE3_BLOCKER_CLOSE`

## Phase Objective

Repair, or precisely preserve as value-only, UKF score blockers for
`zhao_cui_predator_prey_T20` and
`zhao_cui_generalized_sv_synthetic_from_estimated_values`. UKF score admission
requires analytical principal-square-root or factor-propagating SR-UKF
provenance, not historical SVD, `GradientTape`, `ForwardAccumulator`, or
finite differences.

## Entry Conditions Inherited From Previous Phase

- Phase 1 predator-prey Zhao-Cui row is closed row-local admitted.
- Phase 2 generalized-SV Zhao-Cui row is closed row-local admitted.
- Phase 3 spatial SIR is closed as a precise full-row theta-binding blocker:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase3-spatial-sir-result-2026-07-02.md`.
- The Phase 3 row-local blocker artifact is:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase3-spatial-sir-zhaocui-row-2026-07-02.json`.
- The July 1 UKF rows still classify predator-prey and generalized-SV as
  `executed_value_only` because the available score provenance was autodiff.
- Spatial SIR UKF remains value-only/no-free-theta and is not a Phase 4 repair
  target unless a reviewed full-row theta binding is introduced first.

## Required Artifacts

- Per-row UKF target and structural derivative inventory for predator-prey and
  generalized-SV:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-derivative-inventory-2026-07-02.json`.
- Analytical principal-square-root/factor score implementation if reviewed
  component derivatives already exist, or a precise blocker for each row.
- Row-local UKF artifacts for both target rows, including unchanged value-only
  blocker outcomes:
  - `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-predator-prey-ukf-row-2026-07-02.json`
  - `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-generalized-sv-ukf-row-2026-07-02.json`
- Structured route-binding ledger:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-route-bindings-2026-07-02.json`.
- Tests for no historical SVD/tape/FD score admission.
- Phase 4 result:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-score-cleanup-result-2026-07-02.md`
- Refreshed Phase 5 subplan.

## Required Checks, Tests, Reviews

- Route scan excluding `GradientTape`, `ForwardAccumulator`, FD, and
  historical SVD score paths for admitted UKF scores.
- Existing analytical-score route tests for actual-SV/KSC are allowed only as
  guardrails for route standards; they do not admit predator-prey or
  generalized-SV.
- Finite value/manual-score checks if implemented for Phase 4 target rows.
- Same-target diagnostics and score-at-true calibration only if a reviewed
  simulator/truth/theta binding exists for the exact UKF row.
- Claude read-only review for material UKF score admission or blocker closeout.

## Exact Phase 4 Command Surface

All TensorFlow checks in this phase are CPU-only unless a later reviewed
subplan explicitly requests trusted GPU/XLA work:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_two_lane_highdim_leaderboard_analytical_scores.py tests/test_actual_sv_srukf_tf.py tests/test_srukf_factor_tf.py
```

Baseline UKF target-row extraction:

```bash
python -c "import json; p='docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json'; d=json.load(open(p)); rows=[r for r in d['rows'] if r['algorithm_id']=='ukf' and r['row_id'] in {'zhao_cui_predator_prey_T20','zhao_cui_generalized_sv_synthetic_from_estimated_values','zhao_cui_spatial_sir_austria_j9_T20'}]; print(json.dumps(rows, indent=2, sort_keys=True))"
```

Route/provenance scan:

```bash
rg -n "zhao_cui_predator_prey_T20|zhao_cui_generalized_sv_synthetic_from_estimated_values|ukf|principal_sqrt|principal-square-root|factor_propagating_srukf|GradientTape|ForwardAccumulator|finite.?diff|fd|svd|eigenderivative" docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py bayesfilter/highdim bayesfilter/nonlinear tests/test_two_lane_highdim_leaderboard_analytical_scores.py tests/test_actual_sv_srukf_tf.py tests/test_srukf_factor_tf.py tests/highdim -S
```

Before any row admission, Phase 4 must write or refresh the structured
route-binding ledger with, for each target row:

- `row_id`;
- `algorithm_id`;
- `route_status`: `admitted`, `value_only_blocked`, or `blocked`;
- `route_family`: one of
  `principal_sqrt_ukf_manual_derivatives`,
  `factor_propagating_srukf_manual_score`, or `none`;
- exact `implementation_path` and `function_symbol`, or `null` if blocked;
- exact `derivative_contract_path` or `derivative_inventory_reference`;
- exact `theta_coordinate_system`;
- `forbidden_route_scan_status`;
- `route_guard_status`;
- `score_admission_status`;
- `blocker_code` and `blocker_reason` when not admitted.

If Phase 4 introduces or changes any implementation/test file for predator-prey
or generalized-SV UKF score admission, append every new path to the
route/provenance scan before admission. The admitted route fails if the new
score path uses `GradientTape`, `ForwardAccumulator`, `.gradient`, `jacobian`,
FD, historical SVD eigenderivative routes, or a structured route binding whose
`route_family`, `implementation_path`, `function_symbol`, and derivative
contract are not explicitly reviewed.

Conditional post-repair tests, required only if Phase 4 implements or changes a
UKF score route:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_two_lane_highdim_leaderboard_analytical_scores.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py bayesfilter/highdim bayesfilter/nonlinear tests/test_two_lane_highdim_leaderboard_analytical_scores.py
```

Any new Phase 4 admission test must assert:

- exact row id and theta coordinate system;
- finite value and finite score;
- exact structured route binding for that row;
- exact implementation path and function symbol used for the score;
- admitted score provenance contains `principal_sqrt`,
  `principal-square-root`, or `factor_propagating_srukf_manual_score`;
- admitted score provenance does not contain `autodiff`, `GradientTape`,
  `ForwardAccumulator`, `fd`, `finite_difference`, `svd`, or
  `eigenderivative`;
- value-only/blocker cells keep score fields null, emit a row-local structured
  artifact, and explain the blocker.

Any new Phase 4 blocker test must assert:

- the row-local artifact exists for each target row;
- `route_status` is not `admitted`;
- score fields are null;
- the blocker names the missing manual derivative/route or target/theta issue;
- no SVD/tape/FD score can be admitted through provenance-only relabeling.

Full all-row leaderboard regeneration remains Phase 6 work unless Phase 4 has a
small row-local emitter that only emits the changed UKF row artifact.

## Phase 4 Skeptical Audit / Pre-Mortem

Material risks before execution:

- Wrong route: reusing the historical SVD UKF route would look like a working
  score while violating the user's square-root route requirement.
- Proxy drift: FD residuals or tape agreement could validate local algebra but
  cannot be the admitted leaderboard score.
- Stale context: actual-SV and KSC SR-UKF repairs show route standards only;
  they do not imply predator-prey or generalized-SV derivatives exist.
- Hidden target mismatch: generalized-SV exact source-row semantics must not
  borrow actual-SV/KSC/precursor evidence.
- SIR confusion: the SIR UKF value-only/no-free-theta row is not repaired in
  Phase 4 because Phase 3 closed the missing theta binding.

Audit status for launch: `PENDING_CLAUDE_REVIEW`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the remaining predator-prey and generalized-SV UKF value-only rows be upgraded to analytical-score rows without historical SVD/tape/FD provenance? |
| Baseline/comparator | July 1 UKF value-only rows and reviewed principal-square-root/factor SR-UKF score standards from actual-SV/KSC work. |
| Primary criterion | Each target UKF row is admitted with finite analytical score plus reviewed structured principal-square-root/factor route binding, or remains value-only with a precise row-local blocker naming the missing derivative/route. |
| Veto diagnostics | Historical SVD, tape, ForwardAccumulator, or FD admitted as analytical score; wrong target; nonfinite score; score row without theta; SIR no-free-theta row repaired without a reviewed theta contract. |
| Explanatory diagnostics | Runtime, score norm, FD residual, score-at-true calibration. |
| Not concluded | HMC readiness, GPU/XLA readiness, production readiness, exact nonlinear likelihood correctness, or superiority over Zhao-Cui/SGQF. |
| Artifact | Phase 4 result, derivative-inventory JSON, route-binding JSON, and row-local JSON artifacts for both target rows regardless of admission/blocker status. |

## Forbidden Claims And Actions

- Do not use historical SVD route for leaderboard score admission.
- Do not admit `GradientTape` score.
- Do not admit `ForwardAccumulator` or finite-difference score.
- Do not claim GPU/HMC readiness.
- Do not repair the SIR UKF score row without a reviewed full-row theta
  binding.
- Do not treat actual-SV/KSC SR-UKF route success as predator-prey or
  generalized-SV route success.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 if the predator-prey and generalized-SV UKF value-only score
statuses are repaired or precisely blocked, and SIR UKF remains honestly
classified as value-only/no-free-theta unless a reviewed theta contract exists.

## Stop Conditions

Stop admission work for a row and write a precise blocker if reviewed
analytical UKF structural derivatives are unavailable, if a repair would
require unreviewed algorithm invention, if only tape/FD/SVD evidence exists, or
if a target/theta mismatch appears.

## End-of-Subplan Protocol

1. Run required local checks.
2. Write Phase 4 result / close record.
3. Draft or refresh Phase 5 subplan.
4. Review Phase 5 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
