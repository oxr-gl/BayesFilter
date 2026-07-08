# Highdim Leaderboard Remaining Blockers Visible Execution Ledger

Date: 2026-07-02

Status: `OPEN`

Master program:

- `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-master-program-2026-07-02.md`

Runbook:

- `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-gated-execution-runbook-2026-07-02.md`

## Ledger Entries

Entries are appended as phases execute.

### 2026-07-02 - Launch Review And Phase 0 Complete

Evidence contract:

- Question: Is the July 2 remaining-blockers program safe to launch from the
  July 1 leaderboard baseline?
- Baseline/comparator:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
  and `.md`, plus July 1 SV/KSC Phase 1 result.
- Primary criterion: launch artifacts exist, July 1 JSON/Markdown baseline
  hashes are recorded, remaining blockers are parsed and classified, and
  plan/runbook controls prevent autodiff/FD score admission, wrong-target row
  promotion, detached execution, and untrusted GPU claims.
- Veto diagnostics: missing baseline, baseline modified during Phase 0,
  JSON/Markdown targeted-row inconsistency, silent N/A blocker,
  Claude-as-authority wording, detached runner authorization, GPU/XLA claim
  without trusted context.
- Non-claims: no row repair, score correctness, GPU readiness, HMC readiness,
  or production readiness.

Actions:

- Created July 2 master program, visible runbook, Claude review ledger,
  execution ledger, stop handoff, and Phase 0-6 subplans.
- Ran local structural checks.
- Claude reviewed master: `VERDICT: AGREE` after prompt narrowing.
- Claude reviewed runbook: two revise rounds for Claude non-response/probe
  wording, then `VERDICT: AGREE`.
- Claude reviewed Phase 0 subplan: one revise round for baseline-freeze
  integrity, then `VERDICT: AGREE`.
- Executed Phase 0 baseline hash and remaining-blocker inventory checks.

Artifacts:

- `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-master-program-2026-07-02.md`
- `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-gated-execution-runbook-2026-07-02.md`
- `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase0-baseline-freeze-result-2026-07-02.md`
- `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-subplan-2026-07-02.md`

Gate status:

- `PASS_PHASE0_BASELINE_FREEZE`
- `PHASE1_SUBPLAN_READY_AFTER_PHASE0`

Next action:

- Review Phase 1 predator-prey subplan with Claude, then start predator-prey
  target/evaluator inventory if it converges.

### 2026-07-02 - Phase 1 Predator-Prey Launch

Evidence contract:

- Question: Can `zhao_cui_predator_prey_T20` / Zhao-Cui execute under its real
  T20 target with an admitted analytical/manual score, or must the cell remain
  precisely blocked?
- Baseline/comparator:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
  and `.md`, with P47 only as diagnostic lower-rung context.
- Primary criterion: finite value plus finite analytical/manual score with
  theta coordinates `(r, K, a, s, u, v)` and no autodiff/FD provenance; or a
  precise blocker separating target, evaluator, and derivative gaps.
- Veto diagnostics: P47/two-observation evidence reported as T20, autodiff/FD
  admitted as score, no theta coordinates, nonfinite value/score, target
  mutation, or source-faithful language without paper/source anchors.
- Explanatory-only diagnostics: FD residuals, score norm, runtime,
  score-at-true calibration.
- Non-claims: no GPU/XLA readiness, HMC readiness, posterior correctness,
  production readiness, source-faithful adaptive Zhao-Cui reproduction, or
  exact native predator-prey claim.

Skeptical audit:

- Passed for Phase 1 precheck/inventory because the converged subplan freezes
  the July 1 baseline, prohibits P47 promotion and tape/FD score admission,
  names exact CPU-only commands, and requires a precise blocker rather than
  ad hoc row promotion if manual derivatives are unavailable.

Actions:

- Claude Phase 1 subplan review converged on iteration 3 with
  `VERDICT: AGREE`.
- Launching CPU-only target/evaluator inventory and existing boundary tests.
- Implementation classification before code edits:
  `extension_or_invention` / documented-deviation fixed-design substitute, not
  `source_faithful`. The candidate repair uses the existing BayesFilter
  multistate fixed-design TT machinery for the local additive-Gaussian RK4
  predator-prey closure and manual density-score methods. It must not close a
  Zhao-Cui source-faithfulness gap or claim adaptive MATLAB TT-cross/SIRT
  reproduction.

Phase 1 close:

- Added manual predator-prey RK4 transition sensitivity and density-score
  methods in `bayesfilter/highdim/models.py`.
- Added row-local Zhao-Cui predator-prey T20 multistate fixed-design TT
  value/manual-score adapter in
  `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`.
- Added `tests/highdim/test_phase1_predator_prey_t20_zhaocui_admission.py`.
- Row-local artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-zhaocui-row-2026-07-02.json`.
- Result:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-result-2026-07-02.md`.

Numerical row-local result:

- `average_log_likelihood`: `-8.996196972444926`
- `log_likelihood`: `-179.92393944889852`
- `score`: `[141.17730810693365, 6.651004553129841, 0.16459087453501595, -61.27719592118952, -5.441160015818105, 6.293474048370024]`
- `score_l2_norm`: `154.27055472098652`
- `score_derivative_provenance`:
  `zhao_cui_predator_prey_t20_multistate_fixed_design_tt_manual_parameter_score_methods_only`

Checks:

- `tests/highdim/test_p45_target_registry.py` and
  `tests/highdim/test_p45_predator_prey_comparison_blocker.py`: `8 passed`.
- `tests/highdim/test_phase1_predator_prey_t20_zhaocui_admission.py`:
  `4 passed`.
- Focused compileall and `git diff --check`: passed.
- Broad all-row pytest/full-leaderboard regeneration were interrupted with
  code `130` because they recomputed unrelated rows and exceeded the Phase 1
  focused evidence budget; full regeneration remains Phase 6 work.

Gate status:

- `PASS_PHASE1_PREDATOR_PREY_T20_ZHAOCUI_VALUE_SCORE_ROW_LOCAL`

Next action:

- Review refreshed Phase 2 generalized-SV subplan, then start Phase 2 target
  inventory if it converges.

### 2026-07-02 - Phase 2 Generalized-SV Launch

Evidence contract:

- Question: Can `zhao_cui_generalized_sv_synthetic_from_estimated_values` be
  executed under its exact source-row target with finite value and
  analytical/manual score, or must it remain precisely blocked?
- Baseline/comparator: July 1 generalized-SV blocked rows and the exact
  source-row target contract.
- Primary criterion: finite value plus finite manual score under the exact
  source-row target, or precise blocker naming target/evaluator/derivative
  gaps.
- Veto diagnostics: actual-SV/KSC/precursor/auxiliary/native-oracle evidence
  admitted as generalized-SV exact source-row evidence, autodiff/FD admitted as
  score, no theta, target mismatch, source-faithfulness without anchors, or
  GPU/HMC overclaim.
- Explanatory-only diagnostics: FD residuals, runtime, score norm,
  score-at-true calibration.
- Non-claims: no exact likelihood correctness, posterior correctness, HMC
  readiness, production readiness, GPU readiness, or all-row leaderboard
  regeneration in Phase 2.

Skeptical audit:

- Passed for Phase 2 precheck/inventory because the converged subplan names
  the wrong-target risks, exact CPU-only commands, route/provenance scans, and
  precise blocker behavior if the exact source-row target cannot be admitted.

Actions:

- Claude Phase 2 subplan review converged on iteration 1 with
  `VERDICT: AGREE`.
- Launching CPU-only target/evaluator inventory and existing generalized-SV
  boundary tests.

Phase 2 close:

- Added `GeneralizedSVPriorMeanSSM` with explicit manual density-score methods
  in `bayesfilter/highdim/models.py`.
- Added row-local Zhao-Cui generalized-SV prior-mean scalar fixed-design TT
  value/manual-score adapter in
  `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`.
- Clarified the generated source-row third coordinate as `mu_over_tau` in
  `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py`.
- Added
  `tests/highdim/test_phase2_generalized_sv_exact_source_row_admission.py`.
- Row-local artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-zhaocui-row-2026-07-02.json`.
- Result:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-result-2026-07-02.md`.

Numerical row-local result:

- `average_log_likelihood`: `-1.4266238463369423`
- `log_likelihood`: `-1438.036837107638`
- `score`: `[2.348688687464202, 1.09941572140932, -0.06740000139302951]`
- `score_l2_norm`: `2.5941465338897247`
- `runtime_seconds`: `454.6250707899453`
- `score_derivative_provenance`:
  `zhao_cui_generalized_sv_prior_mean_scalar_fixed_design_tt_manual_parameter_score_methods_only`

Checks:

- `tests/highdim/test_p44_generalized_sv_target.py` and
  `tests/highdim/test_p47_generalized_sv_equality.py`: `26 passed`.
- `tests/highdim/test_phase2_generalized_sv_exact_source_row_admission.py`:
  `3 passed`.
- Focused compileall, row-local analytical score contract, and
  `git diff --check`: passed.

Gate status:

- `PASS_PHASE2_GENERALIZED_SV_ZHAOCUI_VALUE_SCORE_ROW_LOCAL`

Next action:

- Review refreshed Phase 3 spatial SIR subplan, then start Phase 3 target
  inventory if it converges.

### 2026-07-02 - Phase 3 Spatial SIR Launch

Evidence contract:

- Question: Can `zhao_cui_spatial_sir_austria_j9_T20` be repaired from P91
  local-component sidecar status to full observed-data/filtering value/manual
  score status, or must it remain precisely blocked?
- Baseline/comparator: July 1 SIR blocker and P91 sidecar evidence.
- Primary criterion: finite full filtering value and manual score with a
  reviewed theta binding, or precise blocker separating local component,
  previous-marginal/filtering value, theta, and derivative gaps.
- Veto diagnostics: P91 local complete-data component reported as full
  filtering row, autodiff/FD admitted as score, no reviewed theta, target
  mismatch.
- Explanatory-only diagnostics: runtime, score norm, score-at-true calibration
  if a reviewed simulator/truth binding exists, FD consistency.
- Non-claims: no posterior correctness, exact likelihood proof, HMC
  convergence, GPU/XLA readiness, product readiness, or all-row regeneration.

Skeptical audit:

- Passed for Phase 3 precheck/inventory because the converged subplan requires
  a row-local artifact, exact theta binding before any score admission,
  blocker-path P91 boundary tests, and a named blocker closeout if only local
  component evidence or no reviewed theta binding is available.

Actions:

- Claude Phase 3 subplan review converged on iteration 3 with
  `VERDICT: AGREE`.
- Launching CPU-only target/evaluator inventory and boundary checks.

Phase 3 close:

- Wrote row-local SIR blocker artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase3-spatial-sir-zhaocui-row-2026-07-02.json`.
- Wrote Phase 3 result:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase3-spatial-sir-result-2026-07-02.md`.
- Decision: SIR remains blocked for the main full observed-data/filtering
  leaderboard value+score row because no reviewed full-row free-theta binding
  exists. This is a target-contract blocker, not a claim that the existing
  local analytical SIR components are useless or that the problem is
  unsolvable.
- P91 local complete-data evidence remains sidecar-only and was not promoted
  to full observed-data/filtering row admission.
- Score-at-true calibration was skipped with
  `skipped_binding_unavailable` because the row-level theta binding is not
  available.

Checks:

- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p91_gpu_xla_local_target.py tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`:
  `12 passed, 2 warnings`.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py -k "sir or p91"`:
  `1 passed, 9 deselected`.
- `python -m json.tool` on the row-local SIR artifact: passed.
- `git diff --check` on Phase 3 result and row artifact: passed.

Gate status:

- `BLOCK_PHASE3_SIR_FULL_FILTERING_THETA_BINDING_UNAVAILABLE`
- `PHASE4_SUBPLAN_REFRESHED_PENDING_REVIEW`

Next action:

- Review the refreshed Phase 4 UKF analytical-score cleanup subplan, then
  start UKF target/route inventory if it converges.

### 2026-07-02 - Phase 4 UKF Cleanup Prelaunch

Evidence contract:

- Question: Can the predator-prey and generalized-SV UKF value-only rows be
  upgraded to analytical-score rows without historical SVD, tape, or FD
  provenance?
- Baseline/comparator: July 1 UKF value-only rows plus reviewed
  principal-square-root/factor SR-UKF score standards from actual-SV/KSC work.
- Primary criterion: each target UKF row is admitted with finite analytical
  score and reviewed principal-square-root/factor provenance, or remains
  value-only with a precise blocker naming the missing derivative/route.
- Veto diagnostics: historical SVD, `GradientTape`, `ForwardAccumulator`, or
  FD admitted as analytical score; wrong target; nonfinite score; score row
  without theta; SIR no-free-theta row repaired without a reviewed theta
  contract.
- Explanatory-only diagnostics: runtime, score norm, FD residual, and
  score-at-true calibration.
- Non-claims: no HMC readiness, GPU/XLA readiness, production readiness, exact
  nonlinear likelihood correctness, or superiority claim.

Skeptical audit:

- Pending Claude review. The refreshed subplan now names exact CPU-only
  commands, route/provenance scans, conditional post-repair tests, wrong-route
  vetoes, and SIR no-free-theta boundaries.

Claude review:

- Phase 4 subplan iteration 1 returned `VERDICT: REVISE` for missing concrete
  derivative-inventory artifact paths, conditional-only row-local blocker
  artifacts, and provenance-string-only admission risk.
- Patched the same subplan with:
  - explicit derivative inventory:
    `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-derivative-inventory-2026-07-02.json`;
  - row-local artifacts for both target rows regardless of admission/blocker
    outcome;
  - structured route-binding ledger:
    `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-route-bindings-2026-07-02.json`.
- Phase 4 subplan iteration 2 returned `VERDICT: AGREE`.

Actions:

- Ran baseline UKF target-row extraction from the July 1 leaderboard.
- Ran static SR-UKF route guard checks.
- Performed route/provenance inventory for existing UKF score functions.
- Wrote Phase 4 derivative inventory, route-binding ledger, row-local UKF
  artifacts, and result.

Phase 4 close:

- Result:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-score-cleanup-result-2026-07-02.md`.
- Predator-prey UKF row-local artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-predator-prey-ukf-row-2026-07-02.json`.
- Generalized-SV UKF row-local artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-generalized-sv-ukf-row-2026-07-02.json`.
- Decision: both target UKF rows remain `executed_value_only`; no analytical
  UKF score is admitted because no reviewed exact-row principal-square-root or
  factor-propagating SR-UKF manual route binding exists.

Checks:

- Broad preflight:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_two_lane_highdim_leaderboard_analytical_scores.py tests/test_actual_sv_srukf_tf.py tests/test_srukf_factor_tf.py`
  was interrupted with code `130` after no useful output and narrowed under
  the smallest-focused-diagnostic rule.
- Narrowed mixed bundle with artifact-building tests was interrupted with code
  `130` after progress dots because it was too broad for Phase 4 launch
  inventory.
- Static SR-UKF guardrail bundle:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_srukf_factor_tf.py::test_srukf_backend_source_passes_static_route_guard tests/test_srukf_factor_tf.py::test_srukf_route_guard_rejects_forbidden_route_families tests/test_srukf_factor_tf.py::test_srukf_route_guard_assertion_rejects_forbidden_file`:
  `7 passed in 2.24s`.
- `python -m json.tool` on all Phase 4 JSON artifacts: passed.
- `git diff --check` on Phase 4 artifacts/result: passed.

Gate status:

- `BLOCK_PHASE4_UKF_TARGET_ROWS_MANUAL_SRUKF_ROUTES_MISSING`
- `PHASE5_SUBPLAN_REFRESHED_PENDING_REVIEW`

Next action:

- Review Phase 4 result and refreshed Phase 5 readiness/calibration subplan
  with Claude, then launch Phase 5 if review converges.
