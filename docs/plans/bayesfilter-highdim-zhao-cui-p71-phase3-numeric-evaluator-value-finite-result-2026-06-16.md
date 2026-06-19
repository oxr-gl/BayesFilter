# P71 Phase 3 Result: Numeric Evaluator And Value-Finite Gate

metadata_date: 2026-06-16
status: PASS_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 3

## Objective

Check whether the reviewed SIR d18 source route provides finite numeric target,
proposal, and transport values on the Phase 2 evaluator path, without claiming
filtering accuracy.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the reviewed d18 source route provide finite numeric target, proposal, and transport values on the Phase 2 evaluator path? |
| Baseline/comparator | Phase 2 execution-only JSON branch identity and row-adequacy boundary. |
| Primary criterion | Finite evaluator values, exact Phase 2 fit/density branch hashes, zero replay drift on retained target/proposal values, and preserved nonclaims. |
| Veto diagnostics | Nonfinite target/proposal/transport values, nonpositive transport density, branch hash drift, row-adequacy boundary drift, or finite values promoted to accuracy evidence. |
| Explanatory diagnostics | Log marginal likelihood, normalizer increments, retained correction weights, replay diffs, runtime, and CPU-only environment. |
| Not concluded | No filtering accuracy, no same-route rank convergence, no d50/d100 scaling, no HMC readiness. |
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase3-numeric-evaluator-value-finite-2026-06-16.json` |

## Command

CPU-only by design:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p71_phase3_numeric_evaluator_value_finite_probe.py --phase2-artifact docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2-execution-only-reproduction-2026-06-16.json --output docs/plans/bayesfilter-highdim-zhao-cui-p71-phase3-numeric-evaluator-value-finite-2026-06-16.json
```

## Result Summary

The Phase 3 finite-value probe passed locally.

- Status: `PASS_P71_PHASE3_NUMERIC_EVALUATOR_VALUE_FINITE`
- Blockers: none
- Fit sample count: `9`
- Log marginal likelihood: `-329.0602743516211`
- Normalizer increments: `[-183.23346210446937, -145.82681224715174]`
- Baseline artifact:
  `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2-execution-only-reproduction-2026-06-16.json`
- Baseline artifact status: `PASS_P59_9E_D18_EXECUTION_ONLY`
- Row adequacy matches Phase 2 artifact: `true`
- Wall time after repair rerun: `140.293` seconds
- Environment: `CUDA_VISIBLE_DEVICES=-1`, `MPLCONFIGDIR=/tmp`

The Phase 2 branch identity was preserved exactly:

- Fit hashes:
  - `10bde66eeab15ab47c5f7a4d09d86780f1cdab400238379c301b52155f5bce1f`
  - `9c8d5639bb8f90843412c0f9d38bbea6b3690d97894d2aac615ac6dc8c39a023`
- Density hashes:
  - `c8c7a82339098159c3020d5d0af355ba04a9d8f54e331091af8bcd0dcaca1127`
  - `36ebf98f85cb9e83a78d97a77879137284113e67c33294c1fb78c028275dfcc8`

Both retained-step evaluator rows were finite:

- Step 1 target/proposal/transport values finite; transport density positive;
  target replay max absolute diff `0.0`; proposal replay max absolute diff
  `0.0`.
- Step 2 target/proposal/transport values finite; transport density positive;
  previous marginal present; target replay max absolute diff `0.0`; proposal
  replay max absolute diff `0.0`.

## Local Checks

Passed:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p71-phase3-numeric-evaluator-value-finite-2026-06-16.json
python -m compileall -q scripts/p71_phase3_numeric_evaluator_value_finite_probe.py
git diff --check -- scripts/p71_phase3_numeric_evaluator_value_finite_probe.py docs/plans/bayesfilter-highdim-zhao-cui-p71-phase3-numeric-evaluator-value-finite-2026-06-16.json docs/plans/bayesfilter-highdim-zhao-cui-p71-phase3-numeric-evaluator-value-finite-result-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-phase3-numeric-evaluator-value-finite-subplan-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4-same-route-rank-degree-ladder-subplan-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-execution-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-stop-handoff-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-runbook-claude-review-ledger-2026-06-16.md
rg -n "phase2_baseline_artifact|phase2_baseline_artifact_status|phase2_artifact_fit_branch_hashes|phase2_artifact_density_branch_hashes|row_adequacy_matches_phase2_artifact|PASS_P71_PHASE3|diagnostic_only_below_preferred_rows|condition-vetoed|finite numeric values are not correctness evidence|target_replay_max_abs_diff|proposal_replay_max_abs_diff" docs/plans/bayesfilter-highdim-zhao-cui-p71-phase3-numeric-evaluator-value-finite-2026-06-16.json docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4-same-route-rank-degree-ladder-subplan-2026-06-16.md scripts/p71_phase3_numeric_evaluator_value_finite_probe.py
rg -n "EXPECTED_PHASE2_FIT_BRANCH_HASHES|EXPECTED_PHASE2_DENSITY_BRANCH_HASHES|phase2_artifact|row_adequacy_drift_from_phase2_artifact" scripts/p71_phase3_numeric_evaluator_value_finite_probe.py
```

## Claude R1 Repair

Claude R1 found two material handoff issues:

- the probe named the Phase 2 JSON artifact as the baseline but compared
  against copied branch-hash constants;
- the Phase 4 subplan did not explicitly inherit the Phase 2
  `diagnostic_only_below_preferred_rows` boundary or the known P60
  condition-veto boundary.

Repair:

- `scripts/p71_phase3_numeric_evaluator_value_finite_probe.py` now reads
  `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2-execution-only-reproduction-2026-06-16.json`
  by default and compares branch hashes and row-adequacy status against that
  artifact.
- The Phase 3 JSON now records the Phase 2 baseline artifact path/status,
  Phase 2 artifact branch hashes, Phase 2 artifact row adequacy, and
  `row_adequacy_matches_phase2_artifact`.
- The Phase 4 subplan now explicitly inherits the finite-value nonclaim,
  Phase 2 row-adequacy boundary, and P60 condition-veto boundary.

## Handoff To Phase 4

Claude R2 returned `VERDICT: AGREE`, so Phase 4 may start.  The Phase 4
structural ladder must inherit these boundaries:

- Phase 3 finite values are not accuracy evidence.
- Phase 2 row adequacy remains
  `diagnostic_only_below_preferred_rows`.
- P60 high-rank comparator remains condition-vetoed and unrepaired by Phase 3.
- Phase 4 must treat rank/degree ladder output as a structural stability gate,
  not correctness or filtering accuracy.

## Nonclaims

- No d18 filtering accuracy claim.
- No same-route rank convergence claim.
- No d50 or d100 scaling claim.
- No HMC readiness claim.
- No adaptive Zhao-Cui parity claim.
