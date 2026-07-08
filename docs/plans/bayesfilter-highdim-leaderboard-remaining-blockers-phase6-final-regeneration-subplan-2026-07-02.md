# Phase 6 Subplan: Final Regeneration And Closeout

Date: 2026-07-02

Status: `DRAFT_READY_AFTER_PHASE5`

## Phase Objective

Regenerate the highdim leaderboard and write a closeout note that separates
row admission, readiness diagnostics, remaining blockers, and nonclaims.

## Entry Conditions Inherited From Previous Phase

- Phase 1 admitted the Zhao-Cui predator-prey row-local value/manual-score
  artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-zhaocui-row-2026-07-02.json`.
- Phase 2 admitted the Zhao-Cui generalized-SV row-local value/manual-score
  artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-zhaocui-row-2026-07-02.json`.
- Phase 3 closed spatial SIR as a full observed-data/filtering theta-binding
  blocker:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase3-spatial-sir-result-2026-07-02.md`.
- Phase 4 closed predator-prey/generalized-SV UKF target rows as value-only
  manual-SRUKF-route blockers:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-score-cleanup-result-2026-07-02.md`.
- Phase 5 classified batch/GPU/XLA and score-at-true readiness without
  changing row admission:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-readiness-calibration-result-2026-07-02.md`.

## Required Artifacts

- Final regenerated JSON leaderboard artifact:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.json`.
- Final regenerated Markdown leaderboard artifact:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.md`.
- Final preservation check artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase6-preservation-check-2026-07-02.json`.
- Phase 6 result:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase6-final-regeneration-result-2026-07-02.md`
- Stop handoff updated to complete or blocked:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-stop-handoff-2026-07-02.md`.
- Optional reset/release note if material state changed; not required for
  Phase 6 launch.

## Required Checks, Tests, Reviews

- Regenerate leaderboard with reviewed command.
- JSON syntax checks plus targeted invariant checks for every remaining-blocker
  row touched by Phases 1-5.
- Markdown table check includes value, score vector or score blocker, score
  provenance, and readiness status.
- Claude read-only final review.

## Exact Phase 6 Command Surface

CPU-only final regeneration:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.md
```

JSON and focused analytical-score checks:

```bash
python -m json.tool docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_two_lane_highdim_leaderboard_analytical_scores.py tests/highdim/test_phase1_predator_prey_t20_zhaocui_admission.py tests/highdim/test_phase2_generalized_sv_exact_source_row_admission.py
```

Preservation check command:

```bash
python - <<'PY'
import json
from pathlib import Path

out = Path('docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase6-preservation-check-2026-07-02.json')
payload = json.loads(Path('docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.json').read_text())
readiness = json.loads(Path('docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-readiness-manifest-2026-07-02.json').read_text())
batch = json.loads(Path('docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-batch-parity-2026-07-02.json').read_text())
gpu = json.loads(Path('docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-gpu-xla-readiness-2026-07-02.json').read_text())
score_true = json.loads(Path('docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-score-at-true-2026-07-02.json').read_text())
rows = {(row['row_id'], row['algorithm_id']): row for row in payload['rows']}
checks = {
    'predator_prey_zhao_cui_value_score': rows[('zhao_cui_predator_prey_T20', 'zhao_cui_scalar_or_multistate')]['comparison_status'] == 'executed_value_score',
    'generalized_sv_zhao_cui_value_score': rows[('zhao_cui_generalized_sv_synthetic_from_estimated_values', 'zhao_cui_scalar_or_multistate')]['comparison_status'] == 'executed_value_score',
    'sir_zhao_cui_still_blocked': rows[('zhao_cui_spatial_sir_austria_j9_T20', 'zhao_cui_scalar_or_multistate')]['comparison_status'] == 'blocked_or_status_only',
    'predator_prey_ukf_still_value_only': rows[('zhao_cui_predator_prey_T20', 'ukf')]['comparison_status'] == 'executed_value_only',
    'generalized_sv_ukf_still_value_only': rows[('zhao_cui_generalized_sv_synthetic_from_estimated_values', 'ukf')]['comparison_status'] == 'executed_value_only',
}
score_provenance_ok = {}
for key in [
    ('zhao_cui_predator_prey_T20', 'zhao_cui_scalar_or_multistate'),
    ('zhao_cui_generalized_sv_synthetic_from_estimated_values', 'zhao_cui_scalar_or_multistate'),
]:
    row = rows[key]
    provenance = str(row.get('score_derivative_provenance') or '').lower()
    score_provenance_ok['/'.join(key)] = (
        row.get('score_status') == 'analytical_score_emitted'
        and 'manual_parameter_score_methods_only' in provenance
        and 'autodiff' not in provenance
        and 'gradienttape' not in provenance
        and 'finite_difference' not in provenance
    )
checks.update(score_provenance_ok)
admitted_readiness_keys = {
    'phase1_zhao_cui_predator_prey_T20',
    'phase2_zhao_cui_generalized_sv_synthetic_from_estimated_values',
}
readiness_keys = {row['row_key'] for row in readiness['admitted_rows']}
batch_statuses = {row['row_key']: row['status'] for row in batch['row_statuses']}
gpu_statuses = {row['row_key']: row['status'] for row in gpu['row_statuses']}
score_true_statuses = {row['row_key']: row['status'] for row in score_true['row_statuses']}
checks.update({
    'phase5_readiness_keys_match_admitted_rows': readiness_keys == admitted_readiness_keys,
    'phase5_readiness_no_blocker_promotion': readiness['scope']['non_admitted_phase3_phase4_blockers_promoted'] is False,
    'phase5_readiness_no_gpu_claim': readiness['scope']['gpu_xla_claimed'] is False,
    'phase5_batch_statuses_deferred_exact_harness_missing': all(
        batch_statuses.get(key) == 'deferred_exact_harness_missing'
        for key in admitted_readiness_keys
    ),
    'phase5_gpu_statuses_not_run': all(
        gpu_statuses.get(key) == 'not_run_requires_explicit_trusted_approval'
        for key in admitted_readiness_keys
    ),
    'phase5_score_at_true_statuses_deferred_multiseed_missing': all(
        score_true_statuses.get(key) == 'deferred_exact_multiseed_harness_missing'
        for key in admitted_readiness_keys
    ),
})
artifact = {
    'schema_version': 'bayesfilter.highdim_leaderboard.remaining_blockers.phase6.preservation_check.v1',
    'date': '2026-07-02',
    'status': 'PASS' if all(checks.values()) else 'FAIL',
    'checks': checks,
    'nonclaims': [
        'preservation checks do not prove exact likelihood correctness',
        'preservation checks do not certify GPU/XLA readiness',
    ],
}
out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + '\n')
print(json.dumps(artifact, indent=2, sort_keys=True))
raise SystemExit(0 if artifact['status'] == 'PASS' else 1)
PY
```

Whitespace check:

```bash
git diff --check -- docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.json docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.md docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase6-preservation-check-2026-07-02.json docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase6-final-regeneration-result-2026-07-02.md docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-stop-handoff-2026-07-02.md
```

GPU/XLA commands are not authorized in Phase 6.

## Phase 6 Skeptical Audit / Pre-Mortem

Material risks before execution:

- Stale generator risk: the final regeneration command may still emit July 1
  metadata or omit Phase 5 readiness artifacts unless the result explains that
  readiness is sidecar evidence.
- Silent blocker erasure: regeneration could make row summaries look complete
  while SIR and UKF target blockers remain open.
- Score provenance drift: final rows could admit autodiff/FD/historical-SVD
  score evidence after earlier phases rejected it.
- Readiness promotion drift: Phase 5 deferred/no-claim readiness statuses could
  be treated as batch/GPU/HMC readiness.

Audit status for launch: `PASSED_AFTER_CLAUDE_REVIEW_ITERATION_2`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the final honest highdim leaderboard state after the remaining-blockers program? |
| Baseline/comparator | July 1 leaderboard and phase results. |
| Primary criterion | Final artifacts match phase results and contain no silent score blockers or unsupported claims. |
| Veto diagnostics | Autodiff/FD admitted as analytical score; wrong target promotion; readiness result treated as scientific proof; stale row status; Phase 3/4 blocker erased; Phase 5 readiness deferred/no-claim status promoted. |
| Explanatory diagnostics | Runtime, readiness status, blocker counts. |
| Not concluded | Exact nonlinear likelihood correctness, posterior correctness, HMC convergence, release readiness. |
| Artifact | Final leaderboard JSON/Markdown and Phase 6 result. |

## Forbidden Claims And Actions

- Do not erase unresolved blockers.
- Do not rename value-only rows as score rows.
- Do not claim production readiness from row admission alone.
- Do not claim Phase 5 batch, GPU/XLA, or score-at-true readiness was executed.
- Do not use GPU/XLA in Phase 6.
- Do not change leaderboard admission criteria after seeing regenerated output.

## Exact Next-Phase Handoff Conditions

There is no next phase. Mark the program complete if final review agrees, or
update stop handoff with blockers.

## Stop Conditions

Stop if regenerated artifacts disagree with phase results or if final review
finds unsupported claims that cannot be repaired.

Also stop if final regeneration requires GPU/XLA, package/network access, or a
new scientific/admission decision outside the reviewed phase results.

## End-of-Subplan Protocol

1. Run required local checks.
2. Write Phase 6 result / close record.
3. Update stop handoff or completion note.
4. Review final artifacts for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
