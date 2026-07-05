# SR-UKF Actual-SV Analytical Score Visible Execution Ledger

Date: 2026-07-01

Status: OPEN

## Entries

### 2026-07-01 - Program Creation - PRECHECK

Evidence contract:

- Question: can governance launch a derivation-first SR-UKF actual-SV repair
  without repeating UKF drift?
- Baseline/comparator: user request, visible runbook template, local governance.
- Primary criterion: artifacts exist, two-part split is explicit, and forbidden
  drift routes are blocked by an auditable drift inventory.
- Veto diagnostics: missing required artifact, detached launch, unbounded Claude
  review, missing/stale drift inventory, or unsupported readiness claim.
- Non-claims: no derivation, implementation, numeric correctness, or leaderboard
  admission yet.

Actions:

- Created master/subplan/runbook scaffolding.

Artifacts:

- `docs/plans/bayesfilter-srukf-actual-sv-score-master-program-2026-07-01.md`
- `docs/plans/bayesfilter-srukf-actual-sv-score-visible-gated-execution-runbook-2026-07-01.md`

Gate status:

- IN_PROGRESS

Next action:

- Run local plan checks and bounded Claude review.

### 2026-07-01 - Phase 2 Generic Audit - CLOSE

Evidence contract:

- Question: does the generic SR-UKF derivation survive formal/local audit for
  dimensions, factor reconstruction, derivative flow, and boundary safety?
- Primary criterion: no material MathDevMCP obligation or Claude `REVISE`
  remains unresolved for Phase 2.
- Veto diagnostics: route drift, missing derivative object, unsupported factor
  reconstruction, or unresolved solve/domain mismatch.
- Non-claims: no actual-SV adapter, implementation, numeric correctness, HMC
  readiness, or leaderboard admission.

Actions:

- Patched `docs/chapters/ch17_square_root_sigma_point.tex` with explicit audit
  assumptions, innovation-factor derivative reconstruction, score derivation
  text, and gain-solve derivation text.
- Ran MathDevMCP typed and derivation audits on material labels.
- Ran scalar symbolic sanity checks for score and gain identities.
- Ran bounded Claude read-only review.

Artifacts:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase2-generic-audit-result-2026-07-01.md`
- `docs/chapters/ch17_square_root_sigma_point.tex`

Gate status:

- PASSED_WITH_RECORDED_PROOF_BACKEND_LIMITATIONS

Next action:

- Begin Phase 3 actual-SV augmented-noise adapter derivation.

### 2026-07-01 - Phase 3 Augmented Adapter Derivation - CLOSE

Evidence contract:

- Question: does the actual-SV adapter derivation apply the generic
  factor-propagating SR-UKF backend to the raw augmented-noise
  Gaussian-closure surrogate without target drift?
- Primary criterion: derivation exists with stable labels, local checks pass,
  and bounded Claude review finds no material unresolved `REVISE`.
- Veto diagnostics: missing observation shock, wrong sigma-point variable,
  missing parameter derivative, exact-likelihood or same-target transformed
  claim leakage, hidden `GradientTape`, historical SVD/eigenderivative, or
  strict-SPD principal-root admission.
- Non-claims: no code, numerical accuracy, HMC readiness, leaderboard
  admission, exact actual-SV likelihood, or same-target transformed likelihood.

Actions:

- Patched `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
  with the Actual-SV SR-UKF augmented-noise adapter derivation.
- Created a bounded review excerpt after a full-chapter Claude review stalled.
- Ran a Claude probe, confirmed `PROBE_OK`, and reran review against the small
  excerpt path.
- Refreshed Phase 4 audit subplan with exact labels and the
  variance-vs-factor initial derivative caveat.
- Patched the derivation and review excerpt with the scalar stationary factor
  derivative label `eq:bf-hd-actual-sv-srukf-initial-factor-derivatives` for
  Phase 4 audit.

Artifacts:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase3-augmented-adapter-derivation-result-2026-07-01.md`
- `docs/plans/bayesfilter-srukf-actual-sv-score-phase3-adapter-derivation-review-excerpt-2026-07-01.md`
- `docs/plans/bayesfilter-srukf-actual-sv-score-phase4-adapter-audit-subplan-2026-07-01.md`
- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`

Gate status:

- PASSED_TO_PHASE_4_AUDIT

Next action:

- Begin Phase 4 adapter derivation audit.

### 2026-07-01 - Phase 4 Adapter Audit - CLOSE

Evidence contract:

- Question: does the adapter derivation survive audit for target law,
  dimensions, derivatives, and nonclaim boundaries?
- Primary criterion: no material MathDevMCP or Claude audit blocker remains
  unresolved.
- Veto diagnostics: wrong augmented variable, missing derivative, dimension
  mismatch, unclarified variance-vs-factor initial derivative handoff,
  exact-likelihood claim, or hidden autodiff/SVD/principal-root dependency.
- Non-claims: no implementation, numerical accuracy, HMC readiness,
  leaderboard admission, exact actual-SV likelihood, or same-target transformed
  likelihood.

Actions:

- Ran MathDevMCP label/context checks and one symbolic equality check.
- Ran deterministic local SymPy checks for transition, observation,
  stationary variance, and stationary factor derivative residuals.
- Wrote Phase 4 audit result.
- Ran bounded Claude result review; Claude returned `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase4-adapter-audit-result-2026-07-01.md`
- `docs/plans/bayesfilter-srukf-actual-sv-score-phase5-generic-implementation-subplan-2026-07-01.md`

Gate status:

- PASSED_TO_PHASE_5_IMPLEMENTATION_SCOPE

Next action:

- Refresh and execute Phase 5 generic factor-propagating SR-UKF implementation
  subplan.

### 2026-07-01 - Phase 5 Generic Backend Implementation - LOCAL CLOSE

Evidence contract:

- Question: does the generic implementation follow the audited SR-UKF
  derivation and expose analytical score diagnostics?
- Primary criterion: focused tests pass and static guards prove the admitted
  score path avoids autodiff, historical SVD, `tf_svd_sigma_point_filter`, and
  principal-root derivative substitution.
- Veto diagnostics: forbidden dependency in the admitted path, failed
  reconstruction, failed affine parity, failed FD consistency, or nonfinite
  branch diagnostics.
- Non-claims: no actual-SV readiness, no leaderboard admission, no HMC/GPU
  readiness, no exact actual-SV likelihood, and no same-target transformed
  likelihood.

Actions:

- Added `bayesfilter/nonlinear/srukf_factor_tf.py`.
- Added `bayesfilter/nonlinear/srukf_route_guard.py`.
- Added `tests/test_srukf_factor_tf.py`.
- Refreshed Phase 6 subplan with exact four-route forbidden-set preservation.
- Ran focused CPU-only tests with `CUDA_VISIBLE_DEVICES=-1`: `9 passed`.

Artifacts:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase5-generic-implementation-result-2026-07-01.md`
- `docs/plans/bayesfilter-srukf-actual-sv-score-phase6-actual-sv-adapter-implementation-subplan-2026-07-01.md`

Gate status:

- PASSED_TO_PHASE_6_ADAPTER_IMPLEMENTATION

Next action:

- Begin Phase 6 actual-SV adapter implementation.

### 2026-07-01 - Phase 6 Actual-SV Adapter Implementation - LOCAL CLOSE

Evidence contract:

- Question: does the actual-SV adapter map the audited augmented-noise law to
  the generic factor-propagating SR-UKF backend and produce an analytical score?
- Primary criterion: focused adapter tests pass with analytical provenance and
  no forbidden score route.
- Veto diagnostics: wrong sigma-point law, missing observation shock,
  nonfinite score, failed same-scalar FD, or forbidden dependency.
- Non-claims: no leaderboard admission, HMC readiness, GPU/XLA readiness,
  exact actual-SV likelihood, or same-target transformed likelihood.

Actions:

- Added `bayesfilter/highdim/actual_sv_srukf_tf.py` as the separate admitted
  actual-SV SR-UKF analytical score path.
- Exported the admitted route through `bayesfilter.highdim`.
- Added `tests/test_actual_sv_srukf_tf.py`.
- Refreshed the Phase 7 ladder subplan with exact forbidden-route preservation.
- Ran focused CPU-only tests with `CUDA_VISIBLE_DEVICES=-1`.

Local checks:

- `python -m py_compile bayesfilter/highdim/actual_sv_srukf_tf.py bayesfilter/highdim/__init__.py tests/test_actual_sv_srukf_tf.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_actual_sv_srukf_tf.py -q`: `4 passed`.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_srukf_factor_tf.py tests/test_actual_sv_srukf_tf.py -q`: `13 passed`.
- `git diff --check` on touched Phase 6 code/tests/subplan paths: passed.
- Forbidden-token scan on `bayesfilter/highdim/actual_sv_srukf_tf.py`: no
  matches.

Artifacts:

- `bayesfilter/highdim/actual_sv_srukf_tf.py`
- `tests/test_actual_sv_srukf_tf.py`
- `docs/plans/bayesfilter-srukf-actual-sv-score-phase6-actual-sv-adapter-implementation-result-2026-07-01.md`
- `docs/plans/bayesfilter-srukf-actual-sv-score-phase7-test-ladder-subplan-2026-07-01.md`

Claude review:

- Bounded one-path review of the Phase 6 result returned `VERDICT: AGREE`.

Gate status:

- PASSED_TO_PHASE_7_TEST_LADDER

Next action:

- Begin Phase 7 thorough test ladder.

### 2026-07-01 - Phase 7 Thorough Test Ladder - LOCAL CLOSE

Evidence contract:

- Question: does the SR-UKF analytical score route pass necessary engineering
  and statistical sanity checks for leaderboard admission consideration?
- Primary criterion: all veto tests pass and the result preserves uncertainty
  and nonclaims.
- Veto diagnostics: static guard failure, reconstruction failure, affine parity
  failure, same-scalar FD failure, nonfinite score, or score-at-true interval
  excluding zero.
- Non-claims: no exact likelihood, HMC readiness, GPU/XLA readiness, method
  superiority, or leaderboard admission yet.

Actions:

- Added `docs/benchmarks/benchmark_actual_sv_srukf_phase7_ladder.py`.
- Added T=1 same-scalar FD coverage for the actual-SV SR-UKF adapter.
- Ran score-at-true consistency for two parameter settings, 10 seeds each.
- Wrote JSON and Markdown consistency artifacts.
- Refreshed Phase 8 subplan with exact admitted-route and release-warning
  requirements.

Local checks:

- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_srukf_factor_tf.py tests/test_actual_sv_srukf_tf.py -q`: `14 passed`.
- `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_actual_sv_srukf_phase7_ladder.py`: passed.
- `git diff --check` on touched Phase 7 paths: passed.
- Forbidden-token scan on `bayesfilter/highdim/actual_sv_srukf_tf.py`: no
  matches.

Artifacts:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase7-test-ladder-result-2026-07-01.md`
- `docs/plans/bayesfilter-srukf-actual-sv-score-phase7-score-true-consistency-2026-07-01.json`
- `docs/plans/bayesfilter-srukf-actual-sv-score-phase7-score-true-consistency-2026-07-01.md`
- `docs/plans/bayesfilter-srukf-actual-sv-score-phase8-leaderboard-release-subplan-2026-07-01.md`

Claude review:

- Bounded one-path review of the Phase 7 result returned `VERDICT: AGREE`.

Gate status:

- PASSED_TO_PHASE_8_LEADERBOARD_RELEASE

Next action:

- Begin Phase 8 leaderboard admission/release wiring.

### 2026-07-01 - Phase 8 Leaderboard Admission And Release - LOCAL CLOSE

Evidence contract:

- Question: should the actual-SV UKF row move from value-only diagnostic to
  admitted value-score analytical SR-UKF row?
- Primary criterion: all prior gates passed and leaderboard provenance names
  the analytical SR-UKF route.
- Veto diagnostics: missing prior result, forbidden score provenance,
  unsupported release claim, or failed leaderboard test.
- Non-claims: no exact likelihood, HMC readiness, GPU/XLA readiness, timing
  ranking, or method superiority.

Actions:

- Added a highdim leaderboard actual-SV UKF SR-UKF cell using
  `actual_transformed_sv_independent_panel_augmented_noise_srukf_score`.
- Updated UKF score-provenance validation to admit reviewed
  `factor_propagating_srukf_manual_score` while preserving historical
  SVD/eigenderivative and autodiff demotion.
- Added a narrow test for the admitted actual-SV SR-UKF UKF cell.
- Cached the Phase 7 leaderboard payload helper to avoid repeated expensive
  rebuilds in that test file.
- Regenerated July 1 highdim leaderboard JSON/Markdown artifacts.

Local checks:

- `python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_analytical_scores.py tests/test_two_lane_highdim_leaderboard_phase7.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_analytical_scores.py::test_actual_sv_ukf_cell_uses_reviewed_srukf_score_without_full_payload_rebuild tests/test_actual_sv_srukf_tf.py tests/test_srukf_factor_tf.py -q`: `15 passed`.
- `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`: passed.
- `python -m json.tool docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`: passed.
- `git diff --check` on touched Phase 8 paths: passed.

Artifacts:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase8-leaderboard-release-result-2026-07-01.md`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`
- `docs/plans/bayesfilter-srukf-actual-sv-score-visible-stop-handoff-2026-07-01.md`

Claude review:

- Bounded one-path review of the Phase 8 result returned `VERDICT: AGREE`.
- Claude suggested explicit prior-result path traceability; the Phase 8 result
  was patched to name the Phase 6 and Phase 7 result paths.

Gate status:

- COMPLETE

Next action:

- Program complete. Final handoff is
  `docs/plans/bayesfilter-srukf-actual-sv-score-visible-stop-handoff-2026-07-01.md`.
