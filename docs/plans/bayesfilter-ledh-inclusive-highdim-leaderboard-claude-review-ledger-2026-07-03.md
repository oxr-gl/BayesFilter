# LEDH-Inclusive Highdim Leaderboard Claude Review Ledger

Date: 2026-07-03

Status: `OPEN`

Claude role: read-only reviewer only. Codex remains supervisor and executor.

## Review Rounds

### 2026-07-03 - Health Probe

- Command: `claude -p "Return exactly CLAUDE_PROBE_OK."`
- Trusted execution: yes.
- Result: `CLAUDE_PROBE_OK`.
- Interpretation: Claude is responsive.

### 2026-07-03 - Broad Path Review Attempt

- Scope: master program, runbook, and all phase subplans by exact path.
- Result: no output after repeated polling; command interrupted.
- Interpretation: Claude health is good, so the broad prompt is too large or
  insufficiently bounded. Replace with a compact packet-read probe and
  packet-only review.

### 2026-07-03 - Packet-Only Review Round 1

Verdict: `VERDICT: REVISE`.

Material findings:

- Comparator provenance was underspecified: frozen baseline rows vs fresh LEDH
  rows could create unfair runtime comparisons.
- Phase 4 ladder policy used vague "where feasible" language.
- Score admission needed an explicit row-specific artifact proving total
  derivative of the stated target.
- Every requested row must appear as full, scoped, or blocked.

Patch applied:

- Added comparator provenance mode and runtime-ranking prohibition.
- Added default LEDH ladder seeds and particle rungs.
- Added row-by-row total-derivative score admission rule.
- Added final artifact rule that every requested row appears as full, scoped,
  or blocked.

### 2026-07-03 - Focused Review Round 2

Verdict: `VERDICT: AGREE`.

Claude read-only review summary:

- Comparator provenance blocker is closed at plan-policy level.
- Every-row inclusion blocker is closed.
- LEDH ladder feasibility blocker is closed enough for launch, with execution
  still gated by pre-run budget and memory checks.
- Total-derivative score admission blocker is closed in the summary.
- Residual caution: this was a summary-only review, so Codex must verify that
  the rules are propagated into the actual files before execution.

Codex propagation check:

- `git diff --check` passed on revised plan artifacts.
- `rg` verified the comparator mode, runtime-ranking prohibition, default seed
  policy, default `N=1000,10000` ladder, total-derivative score admission rule,
  and every-row rule appear in the plan artifacts.

### 2026-07-03 - Phase 1 Review Round 1

Verdict: `VERDICT: REVISE`.

Material findings:

- "LGSSM/SIR executable" wording was too broad; it could include the
  parameterized SIR component row or score arms.
- Admitted candidate rows needed clearer wording that target match remains
  gated, not already admitted.
- Phase 2 dry-run artifact must emit explicit blocked/scoped reasons, not just
  row presence.

Patch applied:

- Narrowed Phase 2 executable scope to exact arms:
  `benchmark_lgssm_exact_oracle_m3_T50:ledh_value_dry_run_or_tiny_value_gate_only`
  and `zhao_cui_spatial_sir_austria_j9_T20:fixed_spatial_sir_value_arm_only`.
- All LEDH score arms remain blocked until total-derivative gates pass.
- Parameterized SIR remains scoped and not executable as a full observed-data
  row.
- Phase 2 must emit explicit blocked/scoped reasons for every non-executed row
  and score arm.

### 2026-07-03 - Phase 1 Focused Closure Review Round 2

Verdict: `VERDICT: AGREE`.

Claude read-only review summary:

- Exact initial executable arms close the admission-boundary ambiguity.
- Explicitly blocked LEDH score arms close the dangerous score overclaim.
- Parameterized SIR remains scoped, not full observed-data executable.
- Phase 2 dry-run blocked/scoped reason requirement closes omission risk.
- Review limitation: summary-level closure review only.

Codex file-level check:

- JSON parse and row coverage passed.
- Exact initial executable arms are present in the ledger and Phase 2 subplan.
- `git diff --check` passed for revised Phase 1/2 artifacts.

### 2026-07-03 - Phase 2 Review Attempt 1

Result: no output after repeated polling; command interrupted.

Interpretation: Claude health is known-good, so the prompt was too broad or
insufficiently bounded. Retry with a tiny closure question.

### 2026-07-03 - Phase 2 Tiny Closure Review Round 2

Verdict: `VERDICT: AGREE`.

Claude read-only review summary:

- Phase 2 schema-boundary goal is satisfied at summary level.
- No LEDH value or score execution is being smuggled into Phase 2.
- Runtime ranking governance is correctly blocked.
- Blocked/scoped semantics are explicit enough for downstream execution.
- Phase 3 handoff is coherent if limited to LGSSM value/score and fixed SIR
  value tiny gates.

Nonclaim preserved:

- Phase 2 is not LEDH mathematical correctness, broad executable readiness, or
  leaderboard rankability evidence.

### 2026-07-03 - Phase 3 Pending Review Packet

Status: `PENDING_CLAUDE_REVIEW`.

Packet summary for bounded review:

- Phase 3 result path:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-tiny-gpu-xla-gates-result-2026-07-03.md`.
- Phase 4 handoff path:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-ledh-particle-ladders-subplan-2026-07-03.md`.
- LGSSM `N=1000` artifact failed narrowly on `ar_coefficient` score:
  z `-3.768`, relative error `1.223%`.
- LGSSM `N=3000` artifact passed value+score; all score components passed by
  the predeclared within-1%-relative-error rule.
- LGSSM `N=10000` current unchunked score path is blocked by GPU OOM, with an
  attempted allocation of about `33.75 GiB`.
- Fixed spatial SIR passed only a tiny GPU/XLA/TF32 value smoke; score remains
  blocked.

Review question:

- Does the Phase 3 close record and Phase 4 handoff avoid overclaiming, preserve
  the memory blocker, keep SIR value-only, and keep blocked/scoped rows intact?

### 2026-07-03 - Phase 3 Review Round 1

Verdict: `VERDICT: REVISE`.

Material findings:

- Phase 4 named adjacent particle-count tolerance but did not define the
  numeric rule.
- Phase 4 stop condition referenced a visible runtime gate without defining
  the time limit.
- Phase 1 ledger had a vocabulary mismatch: `row_status_meaning` used generic
  labels while row decisions used exact labels such as
  `in_scope_for_later_full_value_score_only_after_gates` and
  `fixed_spatial_sir_value_arm_candidate_only`.

Patch applied:

- Added the Phase 4 adjacent value-stability rule:
  `abs(mean_b - mean_a) <= 5 * sqrt(mcse_a^2 + mcse_b^2)`.
- Added a larger-rung MCSE sanity rule.
- Added explicit runtime gates: 30 minutes without artifact/log progress for a
  row/rung command, and 4 hours without a completed row artifact for a full
  Phase 4 row.
- Aligned Phase 1 `row_status_meaning` keys with the actual row-decision
  labels.

### 2026-07-03 - Phase 3 Focused Closure Review Round 2

Verdict: `VERDICT: AGREE`.

Claude read-only review summary:

- The adjacent-rung value-stability tolerance is now explicit:
  `abs(mean_b - mean_a) <= 5 * sqrt(mcse_a^2 + mcse_b^2)`.
- Runtime stop gates are now explicit: 30 minutes without artifact/log progress
  for a row/rung command, and 4 hours without a completed row artifact for a
  full Phase 4 row.
- Phase 1 `row_status_meaning` now aligns with actual
  `ledh_row_scope_decision` labels and Phase 2 preservation labels.
- No new material overclaim was introduced by the patch.

Codex local closure checks:

- Phase 1 ledger JSON parse and status-key coverage passed.
- Focused Phase 2 runner tests still passed: `5 passed`.
- `git diff --check` passed.

### 2026-07-03 - Phase 4 Target-Mismatch Repair Packet Review

Health probe:

- `CLAUDE_PROBE_OK`.

Initial exact-path review:

- A broader exact-path review prompt produced no output after repeated polls.
  Because the health probe passed, Codex treated this as prompt surface area,
  stopped the review, and narrowed the prompt.

Review packet:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-claude-review-packet-2026-07-03.md`

Verdict: `VERDICT: AGREE`.

Claude read-only review summary:

- The packet states the target mismatch plainly: Contract E is `D=2`, `T=10`,
  three-parameter route evidence, while
  `benchmark_lgssm_exact_oracle_m3_T50` is `D=3`, `T=50`, five-parameter,
  dataset seed `81100` evidence.
- The repair keeps LGSSM as same-target value-only evidence and leaves score
  blocked.
- Fixed spatial SIR is value-only, score-blocked, and not exact nonlinear
  likelihood correctness evidence.
- Runtime ranking, HMC readiness, and Zhao-Cui source-faithfulness claims remain
  forbidden.

Scope limit:

- Claude explicitly said this pass reviewed the packet text and claim
  discipline only, not the full referenced artifacts or tests. Codex local
  checks covered the referenced paths and JSON content.

Codex local closure checks:

- `py_compile`: passed.
- Focused tests: `6 passed`.
- Same-target LGSSM and fixed SIR JSON content assertions: passed.
- `git diff --check`: passed.

### 2026-07-03 - Phase 5 Merge Packet Review

Review packet:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase5-claude-review-packet-2026-07-03.md`

Verdict: `VERDICT: REVISE`.

Material finding:

- The packet phrase "all LEDH scores blocked" was too blunt. The
  parameterized SIR LEDH row is scoped component evidence with
  `scoped_score_diagnostic_not_full_observed_data_score`, not a blocked
  main-row score. The scientifically correct statement is:
  - no LEDH leaderboard score rows are admitted;
  - LGSSM and fixed SIR main-row LEDH scores are blocked;
  - parameterized SIR remains scoped component evidence only.

Patch applied:

- Updated the Phase 5 review packet to say "no LEDH row has a populated
  leaderboard score vector" and to distinguish blocked main-row scores from
  scoped parameterized SIR evidence.

Codex local closure checks:

- Focused tests and JSON checks are rerun after this patch in the Phase 5
  closeout path.

### 2026-07-03 - Phase 5 Focused Closure Review

Verdict: `VERDICT: AGREE`.

Claude read-only review summary:

- The packet now says no LEDH leaderboard score rows are admitted.
- It says LGSSM and fixed SIR main-row LEDH scores are blocked.
- It says parameterized SIR remains scoped component evidence only, not a
  blocked or admitted full observed-data leaderboard score.

Codex closure checks:

- Focused tests: `8 passed`.
- JSON content checks: passed.
- `git diff --check`: passed.
