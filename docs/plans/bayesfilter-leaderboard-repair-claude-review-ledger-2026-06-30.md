# BayesFilter leaderboard repair Claude review ledger

Date: 2026-06-30

Status: `OPEN`

Claude role: read-only reviewer only.

## Review Entries

### Iteration 1 - Master Program

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-master-program-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact path.

Findings summary:

- `VERDICT: REVISE`.
- Required fixes:
  - score-zero must be expectation-based/multi-replicate, not per-dataset zero;
  - CPU/GPU trusted-context rules must cover all TensorFlow/GPU-touching phases;
  - key actual-SV and P91 artifacts need exact paths;
  - Phase 3 gate must not say loose "value and score" where analytical-score status is required;
  - final output artifacts must be named explicitly.

Codex action:

- Patched the master program, runbook, and affected subplans before rerunning checks and review.

### Iteration 2 - Master Program

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-master-program-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact path after iteration-1 revisions.

Findings summary:

- `VERDICT: REVISE`.
- Expected-score calibration, GPU/CPU TensorFlow context rules, Phase 3 score wording, proxy metric separation, baseline scoping, and fail-closed behavior were accepted.
- Remaining material fix:
  - path-anchor the review ledger, execution ledger, runbook, final review trail, nonclaims location, and final visible artifacts.
- Minor fix:
  - spell out the bounded Claude command form.

Codex action:

- Patched the master program to name the review ledger, execution ledger, visible runbook, stop handoff, nonclaims location, final artifacts, and bounded Claude command form explicitly.

### Iteration 3 - Master Program

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-master-program-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact path after artifact path anchoring.

Findings summary:

- `VERDICT: REVISE`.
- Review/execution ledger, visible runbook, bounded Claude command form, final review trail, and final output artifacts were accepted as anchored.
- Remaining fix:
  - nonclaims location was still ambiguous as "final leaderboard/result."

Codex action:

- Patched the Phase 8 close gate to require nonclaims in both `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md` and `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-result-2026-06-30.md`.

### Iteration 4 - Master Program

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-master-program-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact path after final nonclaims artifact anchoring.

Findings summary:

- `VERDICT: AGREE`.
- Claude agreed the nonclaims location ambiguity was fixed and saw no remaining blocker to launching Phase 0 from the master program.

Codex action:

- Launched Phase 0 under the visible runbook.

### Phase 1 Result Review - Iteration 1

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase1-actual-sv-sgqf-value-result-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact result path.

Findings summary:

- `VERDICT: AGREE`.
- Claude agreed Phase 1 closes the stale actual-SV SGQF `not_same_target` issue as value-only without claiming analytical score.
- Non-blocking note: cite the corrected actual-SV target note path directly in the result.

Codex action:

- Patched the Phase 1 result to cite `docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md`.

### Phase 2 Subplan Review - Iteration 1

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-subplan-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact subplan path.

Findings summary:

- `VERDICT: REVISE`.
- Claude agreed target locking and anti-autodiff provenance were directionally safe but found the strict analytical-score admission standard too weak.
- Required revisions:
  - add derivation/provenance artifact mapping score terms to the exact transformed target;
  - require a non-proxy correctness anchor beyond finite/no-tape provenance;
  - make expected-score calibration or independent same-target score reference/derivation review required for admission, otherwise defer;
  - add boundary-safety checks;
  - separate five-round review cap from substantive evidence criteria.

Codex action:

- Patched the Phase 2 subplan to require derivation/provenance mapping, non-proxy correctness anchor, boundary safety, and defer/value-only outcome when evidence is insufficient.

### Phase 2 Subplan Review - Iteration 2

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-subplan-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact subplan path after iteration-1 revisions.

Findings summary:

- `VERDICT: AGREE`.
- Claude accepted the revised Phase 2 subplan standard: strict analytical score requires derivation/provenance mapping, no tape/autodiff route, boundary safety, and a non-proxy correctness anchor; otherwise the row must remain value-only with a precise blocker.

Codex action:

- Executed Phase 2 under the agreed subplan and wrote the Phase 2 result.

### Phase 2 Result Review - Iteration 1

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-result-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact result path.

Findings summary:

- `VERDICT: AGREE`.
- Claude agreed the Phase 2 result satisfies the gate as stated from the result note alone: manual no-tape analytical score route, derivation/provenance record, finite value and score, same-target coordinate scoping, focused checks, no exact-likelihood/HMC/GPU/source-faithfulness overclaims, and valid Phase 3 handoff.
- Caveat recorded by Claude: the review did not inspect the cited subplan or derivation artifact.

Codex action:

- Marked Phase 2 passed and advanced to Phase 3 precheck.

### Phase 3 Result Review - Iteration 1

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase3-zhaocui-lgssm-adapter-result-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact result path.

Findings summary:

- `VERDICT: AGREE`.
- Claude agreed the Phase 3 result satisfies the blocker-repair scope from the result note alone: target-compatible user-amended exact-oracle LGSSM adapter, tight Kalman tie-out, physical-theta differentiated-Kalman provenance, no ALS/training route, no source-faithful or paper-scale Zhao-Cui overclaim, adequate local checks, and safe Phase 4 handoff.
- Caveat recorded by Claude: the review did not independently inspect cited code, tests, or subplan.

Codex action:

- Marked Phase 3 passed and advanced to Phase 4 precheck.

### Phase 4 Subplan Review - Iteration 1

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase4-predator-prey-cells-subplan-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact subplan path after Codex added the P47/T20 target-drift guard.

Findings summary:

- `VERDICT: AGREE`.
- Claude agreed the revised subplan guards against reporting P47 two-observation lower-rung values as the source-scope `zhao_cui_predator_prey_T20` row, preserves the no-tape analytical-score boundary, and allows honest T20 execution or precise blockers.

Codex action:

- Launched Phase 4 execution under the revised subplan.

### Phase 4 Result Review - Iteration 1

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase4-predator-prey-cells-result-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact result path.

Findings summary:

- `VERDICT: AGREE`.
- Claude agreed the Phase 4 result note prevents the P47 two-observation diagnostic from being reported as the source-scope `zhao_cui_predator_prey_T20` row, preserves the analytical-score boundary by emitting no value/score for the blocked fixed-SGQF T20 cell, and hands off safely to Phase 5.
- Caveat recorded by Claude: the review did not independently inspect cited subplan, code, tests, or regenerated artifacts.

Codex action:

- Mark Phase 4 passed with precise blockers and advance to Phase 5 subplan review.

### Phase 5 Subplan Review - Iteration 1

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-subplan-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact subplan path.

Findings summary:

- `VERDICT: REVISE`.
- Claude found stale predator-prey entry-condition wording, weak handoff conditions, P91 incorrectly framed as a comparator rather than boundary context, an underpowered primary criterion, underspecified expected-score calibration, artifact mismatch, and GPU/XLA ambiguity.

Codex action:

- Patched the Phase 5 subplan to require a row-admission contract, boundary P91 as sidecar-only context, define minimum 10-dataset expected-score calibration with componentwise `abs(mean_score_j) <= 2 * sample_sd_j`, strengthen handoff/stop conditions, and clarify GPU/XLA as non-required unless claimed.

### Phase 5 Subplan Review - Iteration 2

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-subplan-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact subplan path after iteration-1 revisions.

Findings summary:

- `VERDICT: REVISE`.
- Claude agreed the substantive boundary fixes were mostly complete, but found the artifact phrase "Score-zero consistency manifest" still mismatched the expected-score calibration criterion.

Codex action:

- Renamed the required artifact to "Expected-score calibration manifest across generated observed-data datasets" and explicitly stated it is not a per-dataset score-zero manifest.

### Phase 5 Subplan Review - Iteration 3

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-subplan-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact subplan path after artifact wording revision.

Findings summary:

- `VERDICT: AGREE`.
- Claude agreed the artifact mismatch is fixed and that the prior boundary fixes were preserved: P91 is sidecar-only, free `theta` is required, observed-data target is separated from component evidence, and expected-score calibration at true theta is the gate rather than solving `score(theta)=0`.

Codex action:

- Execute Phase 5 under the agreed revised subplan.

### Phase 5 Result Review - Iteration 1

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-result-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact result path.

Findings summary:

- `VERDICT: AGREE`.
- Claude agreed the Phase 5 result preserves P91 SIR d18 as local complete-data sidecar evidence only, blocks the full observed-data/filtering leaderboard row with precise derivative/evaluator blockers, and avoids unsupported observed-data likelihood, score, GPU, or HMC claims.
- Minor caution recorded by Claude: positive P91 GPU/XLA/benchmark/HMC status strings are safe only because they remain clearly scoped as sidecar fields and are paired with nonclaims.

Codex action:

- Mark Phase 5 passed with precise blocker and advance to Phase 6 subplan review.

### Phase 6 Subplan Review - Iteration 1

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase6-generalized-sv-subplan-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact subplan path.

Findings summary:

- `VERDICT: REVISE`.
- Claude found the subplan did not explicitly bar precursor/native-oracle evidence from being used as SGQF/Zhao-Cui source-row admission evidence, framed prior blocked rows as a comparator instead of the exact source-row contract, allowed execution/progress to be read as admission, treated 2026-06-29 artifacts too weakly as context, and lacked backend/context artifact requirements.

Codex action:

- Patched the Phase 6 subplan to make `zhao_cui_generalized_sv_synthetic_from_estimated_values` exact source-row admission the comparator, downgrade prior artifacts to context only, forbid precursor/native-oracle/auxiliary/actual-SV/KSC evidence as admission evidence, require exact-row execution or precise blocker, and require backend/context provenance.

### Phase 6 Subplan Review - Iteration 2

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase6-generalized-sv-subplan-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact subplan path after iteration-1 revisions.

Findings summary:

- `VERDICT: AGREE`.
- Claude agreed the exact-row comparator, primary criterion, anti-promotion forbidden action, stale-context boundary, and backend/context artifact requirement were fixed.
- Minor non-blocking wording note: objective wording could be read as derivative review for value cells too, but the evidence contract is precise enough.

Codex action:

- Execute Phase 6 under the agreed revised subplan.

### Phase 6 Result Review - Iteration 1

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase6-generalized-sv-result-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact result path.

Findings summary:

- `VERDICT: REVISE`.
- Claude agreed the exact-source-row blocker conversion and CPU-only/backend context were present, but found a consistency gap: high-level text excluded auxiliary evidence, while concrete emitted blocker strings listed precursor/native-oracle/actual-SV/KSC without auxiliary.

Codex action:

- Patched row-facing code, tests, regenerated leaderboard artifacts, and Phase 6 result text so the concrete reason code and nonclaims include auxiliary evidence:
  `PRECURSOR_NATIVE_ORACLE_AUXILIARY_ACTUAL_SV_KSC_NOT_ADMISSION_EVIDENCE`.

### Phase 6 Result Review - Iteration 2

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase6-generalized-sv-result-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact result path after iteration-1 repair.

Findings summary:

- `VERDICT: AGREE`.
- Claude agreed the full forbidden evidence set, including auxiliary evidence, is now carried through the blocker/result wording, exact-source-row blocker status is preserved, and CPU-only/backend context is clear.

Codex action:

- Mark Phase 6 passed with precise blockers and advance to Phase 7 subplan review.

### Phase 7 Subplan Review - Iteration 1

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-subplan-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact subplan path.

Findings summary:

- `VERDICT: REVISE`.
- Claude agreed the scope and correctness-first timing boundary were mostly
  safe, but required stronger structural P91 sidecar separation and more
  concrete artifact path requirements.

Codex action:

- Patched the Phase 7 subplan to require P91 timing under a separate sidecar
  namespace/section, anti-promotion tests for P91 sidecar timing, exact
  regenerated leaderboard artifact paths, and explicit reused-evidence
  enumeration if no new benchmark is run.

### Phase 7 Subplan Review - Iteration 2

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-subplan-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact subplan path after iteration-1 repair.

Findings summary:

- `VERDICT: AGREE`.
- Claude agreed the revised subplan is consistent, feasible,
  artifact-complete, and boundary-safe, including structural P91 sidecar
  isolation and no timing promotion of blocked value/score cells.

Codex action:

- Executed Phase 7 under the agreed revised subplan.

### Phase 7 Result Review - Iteration 1

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-result-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact result path.

Findings summary:

- `VERDICT: AGREE`.
- Claude agreed the Phase 7 result satisfied the agreed boundary: every main
  row has batch/GPU/XLA status, blocked/value-only cells are not timing-rankable,
  P91 local complete-data timing is structurally isolated as sidecar evidence,
  and no unsupported GPU/full-SIR-production claim is made.

Codex action:

- Advanced to Phase 8 final regeneration subplan review.

### Phase 8 Subplan Review - Iteration 1

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-subplan-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact refreshed subplan path.

Findings summary:

- `VERDICT: REVISE`.
- Claude requested exact artifact paths, exact commands/environment, explicit
  Phase 7 preservation comparison, reset/release note clarification, and an
  explicit N/A/full-program test handling rule.

Codex action:

- Patched Phase 8 subplan with exact artifact paths, exact commands, and Phase
  7 preservation validation.

### Phase 8 Subplan Review - Iteration 2

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-subplan-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact subplan path after iteration-1 repair.

Findings summary:

- `VERDICT: REVISE`.
- Claude found remaining placeholder heredocs, missing reset memo/review-ledger
  end-protocol steps, and missing review ledger in the diff-check artifact list.

Codex action:

- Replaced placeholder commands with executable heredocs, added reset memo and
  review ledger protocol steps, and added the review ledger to `git diff --check`.

### Phase 8 Subplan Review - Iteration 3

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-subplan-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact subplan path after iteration-2 repair.

Findings summary:

- `VERDICT: REVISE`.
- Claude found the snapshot baseline was mutable, the exception language was
  inconsistent with the validator, and the full-program focused test set needed
  to be named explicitly.

Codex action:

- Created immutable Phase 7 preservation baseline
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-phase7-preservation-baseline-2026-06-30.json`
  with SHA-256
  `cb71a48830d6daf62062a3dec55ad93f238c1d41aad6a75e5f1bfc6b803c6f2f`;
  removed exception language; named the focused Python/test set.

### Phase 8 Subplan Review - Iteration 4

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-subplan-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact subplan path after immutable-baseline repair.

Findings summary:

- `VERDICT: REVISE`.
- Claude agreed the immutable baseline fixed the largest gap but requested
  generic P91 sidecar preservation/leakage validation across all rows rather
  than a hard-coded SIR row check.

Codex action:

- Patched the validator to compare sidecar presence/equality for every row and
  assert no P91 sidecar evidence leaks into main timing/ranking/admission fields.

### Phase 8 Subplan Review - Iteration 5

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-subplan-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact subplan path after generalized sidecar validator repair.

Findings summary:

- `VERDICT: AGREE`.
- Claude agreed the subplan now satisfies consistency, feasibility, artifact
  completeness, exact command reproducibility, Phase 7 preservation, and P91
  sidecar boundary safety.

Codex action:

- Executed Phase 8 local regeneration and checks under the agreed subplan.

### Phase 8 Result Review - Iteration 1

Reviewed path:

- `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-result-2026-06-30.md`

Prompt shape:

- Bounded read-only review of one exact result path.

Findings summary:

- `VERDICT: AGREE`.
- Claude agreed the Phase 8 result documents the agreed closeout: final
  leaderboard regenerated, immutable Phase 7 preservation/baseline validation
  passed, P91 sidecar isolation preserved, nonclaims and remaining blockers
  recorded, and no unsupported production/scientific/GPU/full-SIR claim made.
- Caveat: Claude reviewed the result note only and did not independently verify
  linked JSON/Markdown artifacts, per bounded review scope.

Codex action:

- Closed the visible runbook program and updated the stop handoff.
