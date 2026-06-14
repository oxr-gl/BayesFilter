# P58 Plan: M9 Source-Route Pipeline Blocker Audit And Repair

metadata_date: 2026-06-11
status: PLAN_DRAFT_FOR_CLAUDE_REVIEW

## Supervisor Contract

Codex is the visible supervisor and execution agent.

Claude Code is a read-only reviewer only.  Claude must not edit files, run
experiments, launch agents, or mutate the workspace.

If Claude does not respond, Codex will run the minimal read-only probe
`READ-ONLY PROBE. Reply with exactly: PROBE_OK`.  If the probe succeeds, Codex
will reduce or redesign the review prompt instead of treating Claude as
unavailable.

## Scope

This P58 lane starts from the reviewed P57 stop:
`BLOCK_P57_M9_SPATIAL_SIR_VALIDATION_LADDER`.

P57-M9 did not fail numerically.  It stopped because the repo had source-route
components but no assembled author-SIR d=18 fixed TT/SIRT source-route fitting
pipeline that could honestly launch the M9 ladder.

Non-goals for this lane:

- adaptive Zhao-Cui parity;
- S&P 500 reproduction;
- smoothing;
- old local/operator/all-grid spatial-SIR routes;
- UKF or memory preflight promoted as correctness evidence.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What concrete blockers prevent launching Phase 9's source-route spatial SIR ladder, which blockers are locally repairable now, and after repairs are any blockers left? |
| Baseline/comparator | P56 source-anchor audit, P57 M0-M8 reviewed artifacts, P57-M9 block result, Zhao-Cui paper/source anchors, and current BayesFilter source-route code/tests. |
| Primary criterion | Produce a Claude-reviewed blocker ledger; fix all source-grounded local blockers that are small enough for this lane; then emit a re-audit stating whether M9 can launch or remains blocked. |
| Veto diagnostics | Treating old local/operator/all-grid routes as source-route; treating M6 contract doubles as author SIR; treating UKF/rank/memory preflight as M9 evidence; implementing an agent-invented route without paper/source anchors; hiding a remaining M9 blocker as future work while claiming launch readiness. |
| Explanatory diagnostics | Static source searches, focused CPU-only pytest, compile checks, source-anchor notes, lower-rung pipeline assembly checks, Claude reviews, and manifest completeness checks. |
| Not concluded | Even if this lane fixes local assembly blockers, it does not by itself prove d=18 accuracy, d=50/d=100 scaling, HMC production readiness, adaptive parity, or paper reproduction. |
| Artifact trail | This plan, Claude plan review, blocker ledger, Claude blocker review, repair result, Claude repair review, and final M9 launch-readiness re-audit under `docs/plans`. |

## Skeptical Plan Audit

Status before execution: `PASS_TO_REVIEW`.

- Wrong-baseline risk: the plan explicitly rejects old all-grid/local/operator
  spatial SIR and contract-double M6 evidence as M9 closure.
- Proxy-risk: UKF, memory, finite values, and lower-rung smoke tests can only
  explain or veto; they cannot certify d=18 source-route correctness.
- Missing-stop risk: if a true d=18 source-route fitting pipeline is still
  absent after local repairs, the final token must be a block token, not a
  launch token.
- Environment mismatch: this lane uses CPU-only focused tests unless a GPU
  command is explicitly required and escalated.
- Artifact-risk: every phase has a named result artifact and Claude review.

## Source Anchors To Reopen During Audit

Paper/source operations must be checked before classifying or fixing blockers:

- SIR example settings:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m`
  and `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/sir_austria/*`.
- Full source loop:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m`.
- Preconditioned route:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m`.
- Linear preconditioner:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/tensordot/precond.m`.
- TT/SIRT construction and maps:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/SIRT.m`
  and `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/*.m`.

## Phase A: Audit Existing Blockers

Tasks:

1. Re-read P57-M9 stop artifacts and P56 source-anchor audit.
2. Search the current code/tests for:
   - author SIR model callback availability;
   - fixed TT/SIRT transport construction;
   - fixed TT fitting entry points;
   - retained-object marginalization;
   - preconditioned Algorithm 5 surface;
   - any assembled author-SIR source-route pipeline;
   - stale local/operator/all-grid route usage.
3. Classify each blocker as:
   - `real_m9_launch_blocker`;
   - `local_repairable_blocker`;
   - `already_closed_by_p57`;
   - `non_goal_noise`;
   - `proxy_not_launch_evidence`.
4. Write the blocker ledger.

Output:
`docs/plans/bayesfilter-highdim-zhao-cui-p58-m9-source-route-pipeline-blocker-ledger-2026-06-11.md`

Claude review:
Loop until `VERDICT: AGREE` or max 5 rounds.  If the fifth review has no major
source-faithfulness blocker, accept it and continue.

## Phase B: Fix Agreed Local Blockers

Allowed fixes:

- small source-grounded code assembly that connects existing P57 components;
- tests that prevent proxy promotion or wrong-route launch;
- manifest/readiness helpers that force M9 to stop unless a real author-SIR
  fixed TT/SIRT source-route pipeline is present.

Disallowed fixes:

- substituting old local/operator/all-grid spatial-SIR code;
- promoting contract doubles to author SIR evidence;
- inventing a new rank/operator route as "source faithful";
- claiming d=18 readiness from lower-rung smoke tests.

Expected local repair target:

Build the smallest source-route pipeline preflight gate that proves whether the
repo has the necessary assembled objects for M9:

1. author SIR callback target;
2. fixed TT/SIRT transport objects, not contract doubles;
3. fixed/frozen reference samples and schedules;
4. sequential retained-object carry through
   `source_route_run_sequential_fixed_hmc(...)`;
5. previous retained marginal evidence for `t > 1`;
6. M8 preconditioned route evidence when required;
7. a manifest that cannot be labeled M9-ready unless all required objects are
   present.

If a full d=18 fitting pipeline is still too large for this lane, implement the
preflight/readiness blocker guard and document the remaining exact missing
implementation pieces.

Output:
`docs/plans/bayesfilter-highdim-zhao-cui-p58-m9-source-route-pipeline-repair-result-2026-06-11.md`

Claude review:
Loop until `VERDICT: AGREE` or max 5 rounds.

## Phase C: Re-Audit M9 Launch Readiness

Tasks:

1. Run focused checks for the repaired blocker guard and existing P57 M1/M6/M7/M8
   source-route gates.
2. Re-run searches for an assembled author-SIR d=18 source-route pipeline.
3. Emit one of:
   - `PASS_P58_M9_SOURCE_ROUTE_PIPELINE_READY_FOR_PHASE9_LAUNCH`;
   - `BLOCK_P58_M9_SOURCE_ROUTE_PIPELINE_STILL_MISSING_ASSEMBLY`;
   - `BLOCK_P58_M9_SOURCE_ROUTE_PIPELINE_SOURCE_DRIFT`;
   - `BLOCK_P58_M9_SOURCE_ROUTE_PIPELINE_HUMAN_REQUIRED`.

Output:
`docs/plans/bayesfilter-highdim-zhao-cui-p58-m9-source-route-pipeline-final-readiness-audit-2026-06-11.md`

Claude review:
Loop until `VERDICT: AGREE` or max 5 rounds.

## Execution Commands

CPU-only by default:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m1_author_sir_callback_parity.py tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py tests/highdim/test_p57_m7_source_faithful_rank_ukf_calibration.py tests/highdim/test_p57_m8_preconditioned_algorithm5.py tests/highdim/test_p51_spatial_sir_route_preflight.py
```

Add new focused tests for P58 if Phase B changes code.

## Review Prompt Requirements

Every Claude review must ask:

1. Did Codex check the Zhao-Cui paper/source anchors before classifying or
   fixing blockers?
2. Did Codex accidentally promote a proxy route, old local/operator route, UKF,
   rank memory preflight, or contract double?
3. Is the blocker set complete enough to decide Phase 9 launch readiness?
4. Are stop tokens honest and strong enough?
5. If disagreeing, list the exact missing blocker or source-drift risk.

## Initial Token

`PLAN_P58_M9_SOURCE_ROUTE_PIPELINE_BLOCKER_AUDIT_REPAIR`
