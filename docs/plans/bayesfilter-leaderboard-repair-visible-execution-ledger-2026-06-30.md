# BayesFilter leaderboard repair visible execution ledger

Date: 2026-06-30

Status: `OPEN`

Master program: `docs/plans/bayesfilter-leaderboard-repair-master-program-2026-06-30.md`

Runbook: `docs/plans/bayesfilter-leaderboard-repair-visible-gated-execution-runbook-2026-06-30.md`

## Ledger Entries

### 2026-06-30 - Phase 0 - PRECHECK

Evidence contract:

- Question: Does the program have a fail-closed leaderboard contract before implementation starts?
- Baseline/comparator: Current June 30 leaderboard artifacts plus corrected actual-SV and P91 SIR evidence.
- Primary criterion: Every planned phase has explicit artifacts, checks, forbidden claims, next handoff, and stop conditions.
- Veto diagnostics: Missing phase subplan; missing evidence contract; stale `not_same_target` not listed as veto; no rule excluding `GradientTape` as analytical score; no rule requiring free `theta` for score rows.
- Non-claims: No implementation correctness, production readiness, GPU performance, or scientific superiority.

Actions:

- Drafted master program, phase subplans, visible runbook, review ledger, execution ledger, and stop handoff.
- Ran local structural checks.
- Claude review iteration 1 returned `VERDICT: REVISE`; patched score calibration, GPU/CPU context, artifact anchors, Phase 3 score wording, and final artifact obligations.
- Claude review iteration 2 returned `VERDICT: REVISE`; patched remaining review/execution/runbook artifact path anchors and bounded Claude command form.
- Claude review iteration 3 returned `VERDICT: REVISE`; patched final nonclaims location to exact artifacts.
- Claude review iteration 4 returned `VERDICT: AGREE`; launched Phase 0.
- Ran Phase 0 artifact/heading check and current SGQF score contract check.

Artifacts:

- `docs/plans/bayesfilter-leaderboard-repair-master-program-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-phase0-contract-audit-subplan-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-visible-gated-execution-runbook-2026-06-30.md`

Gate status:

- `PASSED`

Next action:

- Write Phase 0 result and advance to Phase 1 precheck.

### 2026-06-30 - Phase 1 - ASSESS_GATE

Evidence contract:

- Question: Can the corrected direct actual-SV SGQF value route be represented honestly in the highdim leaderboard?
- Baseline/comparator: Corrected actual-SV derivation note and existing direct SGQF filter function.
- Primary criterion: Fixed SGQF actual-SV cell is finite `executed_value_only` with same-target direct transformed-SV target status.
- Veto diagnostics: stale `blocked_not_same_target`; score emitted from `GradientTape`; actual-SV/KSC target merge.
- Non-claims: No analytical SGQF score, no exact nonlinear likelihood, no GPU performance, no production readiness.

Actions:

- Patched the highdim leaderboard emitter to execute the direct exact-transformed SGQF actual-SV value route.
- Regenerated the highdim leaderboard CPU-only with `CUDA_VISIBLE_DEVICES=-1`.
- Wrote Phase 1 result.

Artifacts:

- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-phase1-actual-sv-sgqf-value-result-2026-06-30.md`

Gate status:

- `PASSED`

Next action:

- Start Phase 2 precheck.

### 2026-06-30 - Phase 2 - PRECHECK

Evidence contract:

- Question: Can the direct exact-transformed actual-SV SGQF row emit a strict analytical score?
- Baseline/comparator: Phase 1 value row, derivation/provenance artifact, FD diagnostic, and either expected-score calibration or independent same-target score reference/derivation review.
- Primary criterion: Strict analytical admission requires derivation-backed same-target differentiation, finite score, no tape/autodiff, and a non-proxy correctness anchor.
- Veto diagnostics: tape/autodiff provenance; target/transform-term mismatch; no derivation artifact; no non-proxy correctness anchor; unsafe boundary behavior.
- Non-claims: No exact likelihood proof, no HMC posterior correctness, no GPU performance.

Actions:

- Read current direct actual-SV SGQF value/score code and generic SGQF derivative infrastructure.
- Claude Phase 2 subplan review iteration 1 returned `VERDICT: REVISE`.
- Patched the Phase 2 subplan to strengthen analytical-score admission standards.

Artifacts:

- `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-subplan-2026-06-30.md`

Gate status:

- `LOCAL_CHECKS_PASSED_PENDING_CLAUDE_REVIEW`

Next action:

- Claude read-only review of Phase 2 result. If accepted, advance to Phase 3.

### 2026-06-30 - Phase 2 - EXECUTION

Evidence contract:

- Question: Can the direct exact-transformed actual-SV SGQF row emit a strict analytical score?
- Baseline/comparator: Phase 1 value row, derivation/provenance artifact, centered finite-difference diagnostic, and no-tape implementation scan.
- Primary criterion: finite value+score, manual analytical provenance, same-target differentiation, and no `GradientTape`/autodiff in the admitted route.
- Veto diagnostics: tape/autodiff provenance, target mismatch, nonfinite value/score, missing derivation, FD contradiction.
- Non-claims: no exact likelihood proof, no HMC posterior correctness, no GPU performance, no coupled Zhao-Cui TT source-faithfulness claim.

Actions:

- Replaced the direct actual-SV fixed-SGQF score wrapper with a manual forward-sensitivity recurrence.
- Updated the focused P43 test to require manual score provenance and retain centered finite-difference consistency.
- Updated the highdim leaderboard emitter so the actual-SV fixed-SGQF row emits `executed_value_score`.
- Regenerated the highdim leaderboard CPU-only with `CUDA_VISIBLE_DEVICES=-1`.
- Wrote Phase 2 derivation/provenance and result artifacts.

Artifacts:

- `bayesfilter/highdim/sv_mixture_cut4.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-derivation-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-result-2026-06-30.md`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`

Local checks:

- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/highdim/sv_mixture_cut4.py docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py -k lane_a_fixed_sgqf_wrapper_score_matches_centered_finite_difference -q`: passed, 3 passed and 36 deselected.
- Route scan for `GradientTape`, `.gradient(`, `tape.watch`: passed.
- JSON row assertion for actual-SV fixed-SGQF value+score: passed.
- `git diff --check` on changed Phase 2 code/artifact paths: passed.

Gate status:

- `PASSED`

Next action:

- Start Phase 3 precheck for the Zhao-Cui LGSSM m3 evaluator adapter.

### 2026-06-30 - Phase 3 - EXECUTION

Evidence contract:

- Question: Can Zhao-Cui evaluate the affine LGSSM m3 row with value and score rather than an adapter blocker?
- Baseline/comparator: user-amended exact-oracle LGSSM row, exact Kalman log likelihood, and differentiated Kalman score for the same row.
- Primary criterion: finite value and score, target-compatible status, and score provenance that identifies the exact-oracle affine adapter.
- Veto diagnostics: ALS fallback; source-faithful or paper-scale Zhao-Cui claim without anchors; nonfinite value/score; score coordinate mismatch.
- Non-claims: no nonlinear Zhao-Cui production readiness, no broad source-faithful TT claim, no GPU/HMC readiness.

Actions:

- Added a narrow `zhao_cui_scalar_or_multistate` LGSSM exact-oracle adapter for `benchmark_lgssm_exact_oracle_m3_T50`.
- Added a focused adapter test.
- Regenerated the highdim leaderboard CPU-only with `CUDA_VISIBLE_DEVICES=-1`.
- Wrote Phase 3 result.

Artifacts:

- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- `tests/test_two_lane_highdim_leaderboard_phase3.py`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-phase3-zhaocui-lgssm-adapter-result-2026-06-30.md`

Local checks:

- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase3.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_phase3.py -q`: passed.
- Adapter row assertion and boundary guard: passed.
- Regenerated leaderboard LGSSM full-three-way assertion: passed.
- `git diff --check` on changed Phase 3 paths: passed.

Gate status:

- `PASSED`

Next action:

- Start Phase 4 precheck for predator-prey SGQF and Zhao-Cui cells.

### 2026-06-30 - Phase 4 - PRECHECK

Evidence contract:

- Question: Can predator-prey cells be upgraded without target drift or mislabeling taped derivatives as analytical?
- Baseline/comparator: source-scope T20 predator-prey dataset and current highdim leaderboard row.
- Primary criterion: each predator-prey cell is executed on the T20 target or explicitly blocked with a narrow reason.
- Veto diagnostics: P47 lower-rung value reported as T20 source-scope value; tape/autodiff analytical score claim; target mismatch; nonfinite likelihood; missing theta coordinate for score.
- Non-claims: no broad nonlinear production readiness or HMC convergence.

Actions:

- Audited the current leaderboard emitter and found the SGQF predator-prey value route used the P47 two-observation diagnostic fixture while reporting under the source-scope `zhao_cui_predator_prey_T20` row.
- Patched the Phase 4 subplan to make P47/T20 target drift an explicit veto.
- Claude Phase 4 subplan review iteration 1 returned `VERDICT: AGREE`.

Gate status:

- `PASSED`

Next action:

- Execute Phase 4 repair: block or rewire predator-prey cells so emitted values are T20-aligned.

### 2026-06-30 - Phase 4 - EXECUTION

Evidence contract:

- Question: Can predator-prey cells be upgraded without target drift or mislabeling taped derivatives as analytical?
- Baseline/comparator: source-scope T20 predator-prey dataset and current highdim leaderboard row; P47 two-observation fixtures are diagnostic only.
- Primary criterion: each predator-prey cell is executed on the T20 target or explicitly blocked with a narrow reason.
- Veto diagnostics: P47 lower-rung value reported as T20 source-scope value; tape/autodiff analytical score claim; target mismatch; nonfinite likelihood; missing theta coordinate for score.
- Non-claims: no broad nonlinear production readiness or HMC convergence.

Actions:

- Removed the stale P47 fixture import path from the highdim leaderboard emitter.
- Blocked the fixed-SGQF `zhao_cui_predator_prey_T20` row with `blocked_missing_t20_fixed_sgqf_evaluator` and `blocked_target_alignment`.
- Added a focused regression test that prevents P47 lower-rung SGQF diagnostic values from being reported under the T20 source-scope row.
- Regenerated the highdim leaderboard CPU-only with `CUDA_VISIBLE_DEVICES=-1`.
- Wrote Phase 4 result.

Artifacts:

- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- `tests/test_two_lane_highdim_leaderboard_phase4.py`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-phase4-predator-prey-cells-result-2026-06-30.md`

Local checks:

- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase4.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_phase4.py -q`: passed.
- `git diff --check docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase4.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`: passed.
- Regenerated JSON assertion for the fixed-SGQF predator-prey T20 blocker: passed.

Gate status:

- `PASSED_WITH_PRECISE_BLOCKERS`

Next action:

- Start Phase 5 subplan review for the spatial SIR d18 parameterized observed-data row.

### 2026-06-30 - Phase 5 - PRECHECK

Evidence contract:

- Question: Can the SIR d18 row be turned into a real observed-data likelihood/score row?
- Baseline/comparator: P91 local complete-data component evidence plus a new observed-data target contract if implementation proceeds.
- Primary criterion: a declared free theta and finite observed-data value/score, or a precise blocker preserving P91 as scoped sidecar only.
- Veto diagnostics: no free theta; complete-data component called full filtering likelihood; expected-score calibration failure; nonfinite value/score; untrusted GPU/XLA claim.
- Non-claims: no exact likelihood proof, no posterior/HMC convergence, no broad production claim unless separate gates pass.

Skeptical audit:

- Wrong-baseline risk: high, because P91 evidence is local complete-data component evidence, not full observed-data/filtering likelihood evidence.
- Proxy-promotion risk: controlled by the subplan's requirement that expected-score calibration and FD are diagnostics, not exact-likelihood proof.
- Hidden-assumption risk: the old source-scope SIR row had no free theta; Phase 5 requires a declared parameter vector before any score row can execute.
- Environment risk: any GPU/XLA claim must use trusted context; CPU-only local checks must set `CUDA_VISIBLE_DEVICES=-1`.
- Audit result: `PASSED_FOR_CLAUDE_SUBPLAN_REVIEW`; do not execute until the bounded Phase 5 subplan review converges.

Artifacts:

- `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-subplan-2026-06-30.md`

Gate status:

- `PASSED_CLAUDE_SUBPLAN_REVIEW_ITER3`

Next action:

- Execute Phase 5 under the agreed revised subplan.

### 2026-06-30 - Phase 5 - EXECUTION

Evidence contract:

- Question: Can the SIR d18 row be turned into a real observed-data likelihood/score row?
- Baseline/comparator: observed-data leaderboard row-admission contract; P91 local complete-data evidence is sidecar context only.
- Primary criterion: observed-data row admission with free `theta`, finite value/score, and expected-score calibration, or a precise blocker preserving P91 sidecar-only boundaries.
- Veto diagnostics: no free theta; complete-data component called full filtering likelihood; expected-score calibration failure/inconclusive status; nonfinite value/score; untrusted GPU/XLA claim.
- Non-claims: no exact likelihood proof, no posterior/HMC convergence, no broad production claim.

Actions:

- Audited P91 artifacts and current SIR d18 code surfaces.
- Found no reviewed full observed-data/filtering evaluator with previous-marginal and fixed-TTSIRT proposal/transport derivatives.
- Added a focused regression test preserving the P91 sidecar and full-filtering blocker.
- Regenerated the highdim leaderboard CPU-only with `CUDA_VISIBLE_DEVICES=-1`.
- Wrote Phase 5 result.

Artifacts:

- `tests/test_two_lane_highdim_leaderboard_phase5.py`
- `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-subplan-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-result-2026-06-30.md`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`

Local checks:

- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase5.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_phase5.py -q`: passed.
- `git diff --check docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase5.py docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-subplan-2026-06-30.md`: passed.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`: passed.
- Regenerated JSON assertion for SIR P91 sidecar plus full-filtering blocker: passed.

Gate status:

- `PASSED_WITH_PRECISE_BLOCKER`

Next action:

- Start Phase 6 subplan review for generalized-SV target/evaluator status.

### 2026-06-30 - Phase 6 - PRECHECK

Evidence contract:

- Question: Can generalized-SV cells be converted from generic blocked status to reviewed target/evaluator status?
- Baseline/comparator: existing generalized-SV governed plan artifacts and current highdim leaderboard blocked rows.
- Primary criterion: each generalized-SV cell has reviewed target status and either executed value/score or precise blocker.
- Veto diagnostics: unsupported same-target claim; score without theta; tape/autodiff analytical score; nonfinite value; stale assumptions from older generalized-SV experiments.
- Non-claims: no broad generalized-SV production readiness unless all separate gates pass.

Skeptical audit:

- Wrong-baseline risk: high, because actual-SV, KSC surrogate SV, native generalized-SV dense oracle, and source-row generalized-SV evaluator are distinct.
- Proxy-promotion risk: high, because a native dense oracle or precursor route must not be promoted as a source-row evaluator.
- Stale-context risk: high, because the generalized-SV governed master program is draft/pending and says no same-target SGQF source-row admission exists at launch.
- Environment risk: the current Phase 6 subplan can likely close by document/status checks only; runtime would need a refreshed reviewed executable plan.
- Audit result: `PASSED_FOR_CLAUDE_SUBPLAN_REVIEW`; do not execute until the bounded Phase 6 subplan review converges.

Artifacts:

- `docs/plans/bayesfilter-leaderboard-repair-phase6-generalized-sv-subplan-2026-06-30.md`

Gate status:

- `PASSED_CLAUDE_SUBPLAN_REVIEW_ITER2`

Next action:

- Execute Phase 6 under the agreed revised subplan.

### 2026-06-30 - Phase 6 - EXECUTION

Evidence contract:

- Question: Can generalized-SV cells be converted from generic blocked status to reviewed target/evaluator status?
- Baseline/comparator: exact source-row contract for `zhao_cui_generalized_sv_synthetic_from_estimated_values`.
- Primary criterion: exact-row execution under reviewed target/evaluator route, or precise target/evaluator/derivative blocker. Precursor/native-oracle/auxiliary/actual-SV/KSC evidence is not admission.
- Veto diagnostics: unsupported same-target claim; score without theta; tape/autodiff analytical score; nonfinite value; stale assumptions from older generalized-SV experiments.
- Non-claims: no generalized-SV SGQF or Zhao-Cui source-row execution, no analytical score, no GPU/HMC/production readiness.

Actions:

- Patched fixed-SGQF generalized-SV row blocker to name the missing exact source-row evaluator.
- Patched Zhao-Cui generalized-SV row blocker to name the missing exact source-row evaluator adapter.
- Added a focused regression test for both generalized-SV blocker cells.
- Regenerated the highdim leaderboard CPU-only with `CUDA_VISIBLE_DEVICES=-1`.
- Wrote Phase 6 result.

Artifacts:

- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- `tests/test_two_lane_highdim_leaderboard_phase6.py`
- `docs/plans/bayesfilter-leaderboard-repair-phase6-generalized-sv-subplan-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-phase6-generalized-sv-result-2026-06-30.md`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`

Local checks:

- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase6.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_phase6.py -q`: passed.
- `git diff --check docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase6.py docs/plans/bayesfilter-leaderboard-repair-phase6-generalized-sv-subplan-2026-06-30.md`: passed.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`: passed.
- Regenerated JSON assertion for generalized-SV fixed-SGQF and Zhao-Cui exact-source-row blockers: passed.

Gate status:

- `PASSED_WITH_PRECISE_BLOCKERS`

Next action:

- Start Phase 7 subplan review for batched CPU/GPU/XLA benchmarking.

### 2026-06-30 - Phase 7 - PRECHECK

Evidence contract:

- Question: Which current leaderboard cells have reviewed batched and GPU/XLA
  evidence, and which remain blocked/not-applicable because value/score row
  admission is not present?
- Baseline/comparator: correctness-passing Phases 1-6 rows plus scoped P91
  local complete-data sidecar evidence.
- Primary criterion: batch/GPU/XLA status is reported per cell only after
  correctness status is known; blocked/value-only main rows are not timing
  rankable; P91 timing is structurally isolated as sidecar evidence.
- Veto diagnostics: GPU claim from non-escalated context; CPU/GPU parity
  failure for a claimed target; timing compared for an invalid value/score
  cell; P91 local complete-data timing promoted to full SIR
  observed-data/filtering row evidence.
- Non-claims: no universal GPU superiority, no HMC convergence, no production
  GPU timing packet, no full SIR observed-data/filtering timing from P91.

Skeptical audit:

- Wrong-baseline risk: controlled by separating main leaderboard rows from P91
  local complete-data sidecar scope.
- Proxy-metric risk: controlled by making timing explanatory only.
- Hidden-assumption risk: controlled by explicit not-applicable statuses for
  rows without value/score admission.
- Environment risk: no new GPU run planned; any future GPU claim still requires
  trusted context.
- Audit result: `PASSED_AFTER_SCOPE_TIGHTENING_FOR_CLAUDE_REVIEW`.

Artifacts:

- `docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-subplan-2026-06-30.md`

Gate status:

- `PASSED_CLAUDE_SUBPLAN_REVIEW_ITER2`

Next action:

- Execute Phase 7 under the agreed revised subplan.

### 2026-06-30 - Phase 7 - EXECUTION

Actions:

- Added `phase7_batch_gpu_xla_status` fields to every main leaderboard row.
- Added P91 local complete-data timing under
  `p91_scoped_evidence.phase7_sidecar_performance`.
- Preserved main-row blocked/value-only cells as not timing-rankable.
- Regenerated the highdim leaderboard CPU-only with `CUDA_VISIBLE_DEVICES=-1`.
- Wrote Phase 7 result and refreshed the Phase 8 subplan.

Artifacts:

- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- `tests/test_two_lane_highdim_leaderboard_phase7.py`
- `docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-subplan-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-result-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-subplan-2026-06-30.md`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`

Local checks:

- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase7.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_phase7.py -q`: passed, 4 tests, 2 warnings, 380.15 seconds.
- `git diff --check docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase7.py docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-subplan-2026-06-30.md`: passed.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`: passed.
- Regenerated JSON assertion for Phase 7 status fields and P91 sidecar isolation: passed.

Gate status:

- `PENDING_CLAUDE_RESULT_REVIEW`

Gate update:

- Phase 7 result Claude review returned `VERDICT: AGREE`.
- Phase 7 status: `PASSED_WITH_STATUS_FIELDS_AND_SIDECAR_ISOLATION`.

Next action:

- Start Phase 8 final regeneration subplan review.

### 2026-06-30 - Phase 8 - PRECHECK

Evidence contract:

- Question: Is the final leaderboard internally consistent and honest about
  value, analytical score, target, batch, and GPU/XLA status?
- Baseline/comparator: initial June 30 leaderboard, phase results, and the
  immutable Phase 7 preservation baseline.
- Primary criterion: final artifacts contain no stale target blockers, no
  invalid analytical-score claims, no ambiguous score rows, and no Phase 7
  timing fields that can rank or admit blocked cells.
- Veto diagnostics: tape/autodiff fixed-SGQF analytical score claim; missing
  free theta for a score row; stale actual-SV SGQF `not_same_target`; missing
  nonclaims; P91 sidecar timing rendered as full SIR observed-data/filtering
  evidence; failed local checks.
- Non-claims: no scientific superiority, exactness, posterior convergence, or
  deployment readiness beyond recorded gates.

Skeptical audit:

- Wrong-baseline risk: controlled by immutable Phase 7 baseline with SHA-256
  `cb71a48830d6daf62062a3dec55ad93f238c1d41aad6a75e5f1bfc6b803c6f2f`.
- Proxy-metric risk: controlled by preserving timing non-ranking fields and P91
  sidecar isolation.
- Artifact risk: controlled by exact artifact paths and executable validation
  commands in the subplan.
- Audit result: `PASSED_CLAUDE_SUBPLAN_REVIEW_ITER5`.

Artifacts:

- `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-subplan-2026-06-30.md`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-phase7-preservation-baseline-2026-06-30.json`

Next action:

- Execute Phase 8 local checks and closeout artifacts.

### 2026-06-30 - Phase 8 - EXECUTION

Actions:

- Verified immutable Phase 7 baseline hash.
- Regenerated final highdim leaderboard JSON and Markdown CPU-only.
- Ran focused phase3-phase7 tests.
- Ran final schema/preservation validator.
- Wrote reset/release memo, Phase 8 result, and visible stop handoff.

Artifacts:

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-phase7-preservation-baseline-2026-06-30.json`
- `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-result-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-reset-memo-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-visible-stop-handoff-2026-06-30.md`

Local checks:

- Baseline hash check: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase3.py tests/test_two_lane_highdim_leaderboard_phase4.py tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase6.py tests/test_two_lane_highdim_leaderboard_phase7.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_phase3.py tests/test_two_lane_highdim_leaderboard_phase4.py tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase6.py tests/test_two_lane_highdim_leaderboard_phase7.py -q`: passed, 9 tests, 2 warnings, 382.52 seconds.
- Final schema/preservation validation against the immutable Phase 7 baseline: passed.

Gate status:

- `PENDING_FINAL_CLAUDE_RESULT_REVIEW`
