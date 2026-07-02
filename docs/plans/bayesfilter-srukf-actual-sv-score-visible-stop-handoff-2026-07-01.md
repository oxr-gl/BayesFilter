# SR-UKF Actual-SV Analytical Score Visible Stop Handoff

Date: 2026-07-01

Status: COMPLETE

## Current Phase

Phase 8: Leaderboard Admission And Release Note.

## Final Status

The SR-UKF actual-SV analytical score program completed through Phase 8. The
actual-SV UKF highdim leaderboard row is now emitted as an admitted value/score
row using the reviewed factor-propagating SR-UKF manual score route. Bounded
Claude review of the Phase 8 result returned `VERDICT: AGREE`.

## Result Artifacts

- Master program:
  `docs/plans/bayesfilter-srukf-actual-sv-score-master-program-2026-07-01.md`
- Visible runbook:
  `docs/plans/bayesfilter-srukf-actual-sv-score-visible-gated-execution-runbook-2026-07-01.md`
- Phase 6 result:
  `docs/plans/bayesfilter-srukf-actual-sv-score-phase6-actual-sv-adapter-implementation-result-2026-07-01.md`
- Phase 7 result:
  `docs/plans/bayesfilter-srukf-actual-sv-score-phase7-test-ladder-result-2026-07-01.md`
- Phase 8 result:
  `docs/plans/bayesfilter-srukf-actual-sv-score-phase8-leaderboard-release-result-2026-07-01.md`
- Admitted implementation:
  `bayesfilter/highdim/actual_sv_srukf_tf.py`
- Generic backend:
  `bayesfilter/nonlinear/srukf_factor_tf.py`
- Regenerated leaderboard:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
  and
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`

## Claude Review Trail

- Phase 6 result: `VERDICT: AGREE`.
- Phase 7 result: `VERDICT: AGREE`.
- Phase 8 result: `VERDICT: AGREE`.
- Full trail:
  `docs/plans/bayesfilter-srukf-actual-sv-score-claude-review-ledger-2026-07-01.md`

## Tests/Checks Actually Run

- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_srukf_factor_tf.py tests/test_actual_sv_srukf_tf.py -q`
  - Passed after Phase 7 T=1 coverage: `14 passed`.
- `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_actual_sv_srukf_phase7_ladder.py`
  - Passed; generated score-at-true consistency artifacts.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_analytical_scores.py::test_actual_sv_ukf_cell_uses_reviewed_srukf_score_without_full_payload_rebuild tests/test_actual_sv_srukf_tf.py tests/test_srukf_factor_tf.py -q`
  - Passed: `15 passed`.
- `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`
  - Passed; regenerated leaderboard artifacts.
- `python -m json.tool docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
  - Passed.
- `git diff --check` on touched Phase 8 paths.
  - Passed.

## Unresolved Blockers

No blocker remains for the actual-SV UKF SR-UKF analytical score admission.

Other leaderboard cells still have unrelated structured blockers, including
source-row evaluator gaps for some non-actual-SV rows. Those are outside this
SR-UKF actual-SV program.

## Nonclaims

- The admitted actual-SV UKF row is a raw augmented-noise Gaussian-closure
  surrogate, not the exact transformed same-target likelihood.
- No HMC readiness is claimed.
- No GPU/XLA readiness or timing ranking is claimed for the admitted row.
- The score-at-true gamma consistency evidence is weak because the cubature
  SR-UKF surrogate can make the gamma score nearly zero structurally.
- Historical SVD UKF and GradientTape score routes remain excluded from the
  admitted actual-SV score path.
