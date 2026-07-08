# BayesFilter NeuTra Real Target HMC Smoke Visible Execution Ledger

Date: 2026-07-06

## Ledger

### 2026-07-06 - Phase 0 - PRECHECK

Evidence contract:

- Question: Is the new real-target NeuTra/HMC-smoke program scoped, bounded,
  and safe to enter Phase 1 inventory?
- Baseline/comparator: Closed c603 import/mechanics fixture program and
  existing BayesFilter target-builder/fixed-transport surfaces.
- Primary criterion: Required planning artifacts exist, name approval/stop
  conditions, preserve nonclaims, and Phase 1 has exact handoff conditions.
- Veto diagnostics: Missing subplan headings, hidden HMC/training/GPU launch,
  unclear review authority, or unsupported HMC/posterior/product claims.
- Non-claims: no real target adapter correctness, no mechanics pass, no HMC
  readiness.

Skeptical audit:

- Wrong baseline blocked: the plan uses c603 import/mechanics fixture evidence,
  not HMC candidate rankings.
- Proxy promotion blocked: finite future probes cannot promote HMC readiness.
- Stop conditions are present in the master program and each subplan.
- Hidden assumption named: Phase 1 must decide whether a real c603 value/score
  authority exists before implementation.
- Environment boundary named: CPU-only checks use `CUDA_VISIBLE_DEVICES=-1`;
  GPU work requires approval.
- Commands planned for Phase 0 are text checks and review only.

Actions:

- Created draft master program, Phase 0-5 subplans, visible runbook, ledger,
  stop handoff, and launch review bundle.

Artifacts:

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-master-program-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase0-launch-contract-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase1-target-authority-inventory-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-visible-gated-execution-runbook-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-visible-stop-handoff-2026-07-06.md`

Gate status:

- `PASSED`

Next action:

- Enter Phase 1 read-only target-authority inventory.

### 2026-07-06 - Phase 0 - PASS_REVIEW

Actions:

- Ran local text checks for launch artifacts and subplan headings.
- Ran the bounded Claude read-only launch review gate.

Local checks:

- `PHASE0_TEXT_CHECK_OK`

Review gate:

- Status: `REVIEW_STATUS=agreed`
- Verdict: `VERDICT=AGREE`
- Summary:
  `/home/chakwong/BayesFilter/.claude_reviews/20260706-140732-bayesfilter-neutra-real-target-hmc-smoke-launch/status.json`

Artifacts:

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase0-launch-contract-result-2026-07-06.md`

Gate status:

- `PASSED`

Next action:

- Start Phase 1 read-only inventory.

### 2026-07-06 - Phase 1 - PRECHECK

Evidence contract:

- Question: Is there a reviewed real c603 target/value-score authority in
  BayesFilter that can support Phase 2 adapter work?
- Baseline/comparator: existing `GenericSSMPosteriorAdapter`, c603
  import/mechanics fixture results, c603 handoff proposal/preflight, and local
  BayesFilter code inventory.
- Primary criterion: classify the next boundary as
  `bridgeable_real_target_adapter`, `design_only`, or
  `blocked_missing_real_target_authority` with exact source paths.
- Veto diagnostics: historical `dsge_hmc` code treated as live BayesFilter
  authority, invented prior/filter/data fields, or synthetic fixture mechanics
  promoted to real-target evidence.
- Non-claims: no adapter correctness, no HMC readiness, no posterior
  correctness, no production readiness.

Skeptical audit:

- Wrong baseline blocked: c603 frozen transport import is not real target
  adapter evidence.
- Proxy promotion blocked: finite synthetic mechanics cannot promote c603
  Rotemberg value/score authority.
- Hidden assumption checked: dsge_hmc handoff source names are source anchors,
  not live BayesFilter callables.
- Environment boundary preserved: no GPU/CUDA, HMC, training, package install,
  or git operation was run.
- Artifact match: Phase 1 writes an inventory result and refreshes the Phase 2
  subplan.

Actions:

- Inspected BayesFilter target-builder, fixed-transport mechanics, c603
  import/mechanics tests, c603 result notes, c603 handoff proposal/preflight,
  and local BayesFilter nonlinear SVD sigma-point APIs.
- Wrote Phase 1 result with classification `design_only`.
- Refreshed Phase 2 as an adapter-authority bridge or blocker phase.

Artifacts:

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase1-target-authority-inventory-result-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase2-real-target-adapter-subplan-2026-07-06.md`
- `docs/reviews/bayesfilter-neutra-real-target-hmc-smoke-phase1-review-bundle-2026-07-06.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Run Phase 1 local checks and bounded Claude read-only review.

### 2026-07-06 - Phase 1 - REPAIR_LOOP_R1

Review gate:

- Command used `claude_review_gate.sh` with `--model opus --effort max`.
- Health probe returned `OK`.
- Primary review timed out with no output.
- Bounded fallback returned `VERDICT=REVISE`.
- Summary:
  `/home/chakwong/BayesFilter/.claude_reviews/20260706-154335-bayesfilter-neutra-real-target-hmc-smoke-phase1/status.json`

Finding:

- The review packet was not self-contained enough to distinguish
  `design_only` from a terminal missing-authority blocker.
- The missing c603 real-target bridge must remain explicitly non-authorizing.

Repair:

- Added an explicit classification rule for `design_only`.
- Listed exact missing authority pieces and handoff source anchors.
- Tightened Phase 2 to stop on insufficient portable real-target authority.

Gate status:

- `REPAIR_IN_PROGRESS`

Next action:

- Rerun focused local checks and bounded review.

### 2026-07-06 - Phase 1 - REVIEW_SUBSTITUTION

Claude availability:

- Round 2 review gate timed out at the tiny probe:
  `/home/chakwong/BayesFilter/.claude_reviews/20260706-161225-bayesfilter-neutra-real-target-hmc-smoke-phase1-r2/status.json`.
- Direct probe `timeout 90s claude -p "Return exactly CLAUDE_PROBE_OK."`
  exited with status `124`.

Decision:

- Claude is unavailable for this gate.
- Per the user instruction and runbook, substitute with a fresh Codex
  read-only review.

Substitute reviewer:

- Agent id: `019f3682-8aa1-77c0-a7e9-8cae370612f5`
- Scope: exactly the Phase 1 result and refreshed Phase 2 subplan.
- Authority: read-only advisory reviewer; cannot authorize runtime, model-file,
  funding, product, default-policy, or scientific-claim boundaries.

Gate status:

- `SUBSTITUTE_REVIEW_IN_PROGRESS`

Next action:

- Wait for substitute review verdict, then advance or repair.

### 2026-07-06 - Phase 1 - PASS_REVIEW

Substitute Codex review:

- Agent id: `019f3682-8aa1-77c0-a7e9-8cae370612f5`
- Verdict: `VERDICT: AGREE`
- Finding summary: no blocking findings; `design_only` is coherent and
  fail-closed; Phase 2 safely authorizes only a source-anchored bridge attempt
  or blocker; residual risk is bounded by Phase 2 stop conditions.

Phase 1 result:

- `PASSED_INVENTORY_DESIGN_ONLY`

Gate status:

- `PASSED`

Next action:

- Enter Phase 2 adapter-authority bridge under the refreshed subplan.

### 2026-07-06 - Phase 2 - PRECHECK

Evidence contract:

- Question: Can BayesFilter expose a real c603 target adapter with
  batch-native finite value/score under reviewed authority?
- Baseline/comparator: Phase 1 `design_only` classification, c603
  proposal/preflight, `GenericSSMPosteriorAdapter`, and existing BayesFilter
  batch SVD sigma-point APIs.
- Primary criterion: either a reviewed adapter-authority bridge emits finite
  rank-2 values/scores with the c603 target signature, or a blocker records
  the exact missing port/source/runtime authority.
- Veto diagnostics: synthetic target mislabeled real, live `dsge_hmc` runtime
  promoted as BayesFilter authority, unreviewed fallback promoted,
  target-signature mismatch, nonfinite probes, HMC/GPU/training launch.
- Non-claims: no HMC convergence, posterior correctness, production readiness,
  or scientific promotion.

Skeptical audit:

- Wrong baseline blocked: c603 frozen transport import is not real target
  value/score authority.
- Proxy promotion blocked: preflight finite probe metadata cannot become a
  batch-native real adapter.
- Stop conditions are present in the Phase 2 subplan.
- Hidden assumption checked: the handoff source anchors are source-port inputs,
  not live BayesFilter runtime authority.
- Environment boundary preserved: no GPU/CUDA, HMC, training, package install,
  or git operation was run.
- Artifact match: Phase 2 must write either an adapter result with tests or a
  blocker result.

Actions:

- Inspected the c603 handoff script posterior wrapper and Rotemberg source
  anchors.
- Checked for portable preflight `.npz` files named by the c603 preflight JSON.
- Searched BayesFilter code/tests for the required real-target wrapper symbols.

Gate status:

- `IN_PROGRESS`

Next action:

- Write Phase 2 blocker result and refresh Phase 3 as blocker-handoff handling.

### 2026-07-06 - Phase 2 - BLOCKER_DRAFTED

Decision:

- Phase 2 closes fail-closed as
  `BLOCKED_MISSING_PORTABLE_REAL_TARGET_AUTHORITY`.

Local checks:

- `rotemberg_second_order_svd_target_arrays.npz`: absent.
- `rotemberg_second_order_svd_probe_cloud.npz`: absent.
- `rotemberg_second_order_svd_data.npz`: absent.
- BayesFilter real target symbols
  `RotembergSecondOrderSVDBayesFilterPosterior`,
  `rotemberg_second_order_svd_bayesfilter_model_and_derivatives`,
  `tf_batched_svd_sigma_point_value_and_score_custom_gradient`,
  `log_prior_value_and_score_analytical_batch`, and `RotembergNKEstimable`:
  absent from BayesFilter Python code/tests.

Artifacts:

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase2-real-target-adapter-result-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase3-real-target-mechanics-subplan-2026-07-06.md`
- `docs/reviews/bayesfilter-neutra-real-target-hmc-smoke-phase2-review-bundle-2026-07-06.md`

Gate status:

- `REVIEW_PENDING`

Next action:

- Run focused local checks and bounded Claude read-only review.

### 2026-07-06 - Phase 2 - PASS_REVIEW

Review gate:

- `REVIEW_STATUS=agreed`
- `VERDICT=AGREE`
- `RUN_DIR=/home/chakwong/BayesFilter/.claude_reviews/20260706-173915-bayesfilter-neutra-real-target-hmc-smoke-phase2`
- `SUMMARY_JSON=/home/chakwong/BayesFilter/.claude_reviews/20260706-173915-bayesfilter-neutra-real-target-hmc-smoke-phase2/status.json`

Decision:

- Phase 2 blocker result accepted.
- Phase 3 remains blocker-handoff handling, not mechanics.

Gate status:

- `PASSED_BLOCKER_CLOSE`

Next action:

- Enter Phase 3 blocker handoff.

### 2026-07-06 - Phase 3 - PRECHECK

Evidence contract:

- Question: Does the program preserve the Phase 2 real-target authority blocker
  without accidentally running or claiming mechanics?
- Baseline/comparator: Phase 2 blocker result and original Phase 3 mechanics
  plan.
- Primary criterion: a blocker-handoff result records that mechanics did not
  run, names the next valid repair boundary, and preserves all nonclaims.
- Veto diagnostics: mechanics/HMC/GPU/training launch, synthetic target
  promotion, live `dsge_hmc` runtime promotion, unsupported claims.
- Non-claims: real target adapter correctness, mechanics validity, HMC
  readiness, posterior correctness, production readiness.

Skeptical audit:

- Wrong baseline blocked: synthetic mechanics and transport import are not
  promoted to real c603 mechanics.
- Proxy promotion blocked: no finite preflight metadata is treated as HMC
  smoke evidence.
- Stop conditions are present in the refreshed Phase 3 subplan.
- Hidden assumption resolved: Phase 3 has no adapter prerequisite and must not
  run mechanics.
- Environment boundary preserved: no GPU/CUDA, HMC, training, package install,
  or git operation is planned.

Actions:

- Wrote Phase 3 blocker-handoff result.
- Refreshed Phase 4 as no-entry HMC-smoke blocker.

Artifacts:

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase3-real-target-mechanics-result-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase4-tiny-hmc-smoke-subplan-2026-07-06.md`

Gate status:

- `LOCAL_CHECKS_PENDING`

Next action:

- Run Phase 3 local checks and review refreshed Phase 4 subplan.

### 2026-07-06 - Phase 3 - LOCAL_CHECKS_OK

Local checks:

- Phase 2 result exists.
- Phase 3 result exists.
- Phase 2 blocker status is recorded.
- Phase 3 no-mechanics status is recorded.
- Phase 4 subplan is refreshed as no-entry HMC-smoke blocker.
- `git diff --check` passed for Phase 2/3/4, ledger, and handoff artifacts.

Artifacts:

- `docs/reviews/bayesfilter-neutra-real-target-hmc-smoke-phase3-review-bundle-2026-07-06.md`

Gate status:

- `REVIEW_PENDING`

Next action:

- Run bounded Claude read-only review for Phase 3 handoff and Phase 4 no-entry
  subplan.

### 2026-07-06 - Phase 3 - PASS_REVIEW_SUBSTITUTE

Claude review gate:

- `REVIEW_STATUS=timeout`
- `VERDICT=NONE`
- `RUN_DIR=/home/chakwong/BayesFilter/.claude_reviews/20260706-175303-bayesfilter-neutra-real-target-hmc-smoke-phase3`
- `SUMMARY_JSON=/home/chakwong/BayesFilter/.claude_reviews/20260706-175303-bayesfilter-neutra-real-target-hmc-smoke-phase3/status.json`

Probe handling:

- Two subsequent trusted tiny-probe attempts could not launch because the
  approval review layer timed out. This is recorded as approval/probe
  unavailability, not a Claude verdict.

Substitute review:

- Fresh Codex read-only substitute reviewer:
  `019f36ec-2b84-7db0-89e5-a86d4fc71b03`.
- Verdict: `VERDICT: AGREE`.
- Finding summary: Phase 3 preserves the Phase 2 blocker and records no
  mechanics run; Phase 4 correctly blocks HMC entry and lists HMC/GPU/training
  runtime authority/scientific-claim stop conditions.

Gate status:

- `PASSED_BLOCKER_HANDOFF`

Next action:

- Enter Phase 4 no-entry HMC-smoke blocker.

### 2026-07-06 - Phase 4 - PRECHECK

Evidence contract:

- Question: Does Phase 4 correctly refuse HMC smoke because the real-target
  mechanics prerequisite is missing?
- Baseline/comparator: Phase 2 blocker and Phase 3 no-mechanics handoff.
- Primary criterion: Phase 4 result records no HMC run and preserves the exact
  blocking prerequisite.
- Veto diagnostics: any HMC/sampler launch, GPU use, retuning, training, or
  claim that the smoke passed.
- Non-claims: convergence, posterior correctness, sampler ranking, default
  readiness, HMC readiness.

Skeptical audit:

- Wrong baseline blocked: there is no real-target mechanics baseline to smoke.
- Proxy promotion blocked: no transport/synthetic mechanics evidence is
  promoted to HMC evidence.
- Stop conditions are explicit in the refreshed Phase 4 subplan.
- Environment boundary preserved: no GPU/CUDA, HMC, training, package install,
  or git operation is planned.

Actions:

- Wrote Phase 4 blocked/no-entry result.
- Refreshed Phase 5 closeout subplan to close the stopped program.

Artifacts:

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase4-tiny-hmc-smoke-result-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase5-closeout-subplan-2026-07-06.md`

Gate status:

- `LOCAL_CHECKS_PENDING`

Next action:

- Run Phase 4 local checks and then close Phase 5.

### 2026-07-06 - Phase 4 - LOCAL_CHECKS_OK

Local checks:

- Phase 3 result exists.
- Phase 4 result exists.
- Phase 3 no-mechanics status is recorded.
- Phase 4 no-entry HMC status is recorded.
- Phase 5 subplan is refreshed for terminal closeout.
- `git diff --check` passed for Phase 3/4/5, ledger, and handoff artifacts.

Gate status:

- `PASSED_NO_ENTRY`

Next action:

- Enter Phase 5 closeout.

### 2026-07-06 - Phase 5 - PRECHECK

Evidence contract:

- Question: What did this program prove, block, or leave for a separate
  program?
- Baseline/comparator: Phase 0-4 results.
- Primary criterion: closeout separates transport/import evidence, missing
  real-target authority, no-mechanics/no-HMC blockers, and nonclaims.
- Veto diagnostics: unsupported HMC/posterior/product claims or missing blocker
  details.
- Non-claims: anything not explicitly supported by phase artifacts.

Skeptical audit:

- Wrong baseline blocked: no transport or synthetic mechanics evidence is
  promoted to real c603 target evidence.
- Proxy promotion blocked: no preflight metadata is treated as HMC or posterior
  evidence.
- Stop conditions preserved: continuation requires a separate reviewed repair
  program.
- Environment boundary preserved: no GPU/CUDA, HMC, training, package install,
  or git operation is planned.

Actions:

- Wrote Phase 5 closeout result.
- Updated visible stop handoff to terminal review-pending status.

Artifacts:

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase5-closeout-result-2026-07-06.md`

Gate status:

- `LOCAL_CHECKS_PENDING`

Next action:

- Run final closeout checks and final read-only review.

### 2026-07-06 - Phase 5 - LOCAL_CHECKS_OK

Local checks:

- Phase 0-5 result artifacts exist.
- Required blocker/status strings are present.
- Closeout result records `PHASE5_CLOSEOUT_LOCAL_CHECKS_OK`.
- `git diff --check` passed for visible program artifacts.

Artifacts:

- `docs/reviews/bayesfilter-neutra-real-target-hmc-smoke-phase5-closeout-review-bundle-2026-07-06.md`

Gate status:

- `FINAL_REVIEW_PENDING`

Next action:

- Run final read-only review and update terminal handoff.

### 2026-07-06 - Phase 5 - PASS_FINAL_REVIEW

Final read-only review:

- Fresh Codex reviewer: `019f36f4-209f-74f1-8210-4d17c740cfff`.
- Verdict: `VERDICT: AGREE`.
- Finding summary: no blocking findings; closeout stops on
  `CLOSED_BLOCKED_MISSING_PORTABLE_REAL_TARGET_AUTHORITY`, preserves transport
  import evidence without promoting it to real target adapter evidence,
  constrains synthetic mechanics to fixture-only evidence, and keeps nonclaims
  and next repair boundaries clear.

Gate status:

- `CLOSED_BLOCKED_MISSING_PORTABLE_REAL_TARGET_AUTHORITY`

Next action:

- Separate reviewed repair program is required before real-target mechanics or
  HMC smoke.
