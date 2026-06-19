# P76 Phase 5 Result: Mini-Batch Pilot Decision

metadata_date: 2026-06-18
status: CLAUDE_AGREE_PHASE6_APPROVAL_REQUIRED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase5-minibatch-pilot-decision-subplan-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-result-2026-06-18.md
phase: 5
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Scope

Phase 5 decides what Phase 4 permits.  It does not run a mini-batch pilot,
edit implementation code, change defaults, use GPU/CUDA, or claim that the
original fitting problem is fixed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does the tiny UKF-initializer smoke justify drafting a bounded mini-batch pilot plan? |
| Exact baseline/comparator | Phase 4 smoke JSON and P75 historical negative context; this is not a live ladder. |
| Primary criterion | State stop/repair/draft-pilot decision, preserve nonclaims and approval boundaries, and draft a safe Phase 6 subplan if justified. |
| Veto diagnostics | Missing or failed Phase 4 smoke artifact; treating smoke as lower-gate repair; resurrecting random, calibrated constant, or source-route prefit as live repairs; launching a pilot; changing defaults; audit-data leakage. |
| Explanatory only | Phase 4 tiny loss, gradient norm, rho range, normalizer, log-density range, and runtime provenance. |
| Not concluded | No generalization, no lower-gate repair, no validation/HMC readiness, no final rank/sample policy. |

## Phase 4 Gate Assessment

Phase 4 passed its smoke criterion after the R2 provenance repair:

- the smoke JSON parses;
- initializer cores are finite;
- one tiny CPU-only density train step is finite;
- `finite_total_loss`, `finite_gradient_norm`, `finite_rho_theta`,
  `finite_normalizer`, and `finite_log_density` are all true;
- `source_route_prefit_used`, `audit_data_used`, and
  `default_behavior_changed` are false;
- the run manifest records actual runtime provenance, including
  `python_executable`, `argv`, `python_argv`, and the CPU-only environment
  snapshot.

Claude R3 returned `VERDICT: AGREE` that Phase 4 closes its provenance
blocker and that Phase 5 may begin as a decision/planning phase only.

## Critical Planning Finding

The Phase 4 smoke shows only that the P76 initializer can build finite cores
and interact with the trainable density mechanics.  It does not answer the
real scientific-engineering question: whether UKF-initialized stochastic
density training generalizes on the author-SIR fixed-variant target under
fresh training batches and audit-separated holdout/replay diagnostics.

There is also a frame mismatch risk.  The existing P75 target pilot generates
training batches in a source-route recentered frame.  The P76 mathematical
contract defines a UKF-whitened frame.  A valid Phase 6 pilot cannot merely
insert P76 cores into the old P75 pilot while keeping the old source-route
frame.  The training points, target values, basis coordinates, and initializer
cores must all live in the same UKF-derived local coordinate frame, or the run
would test a mismatched object.

The current source-route diagnostic generator can reuse an arbitrary
`SourceRouteCoordinateFrame`.  Therefore Phase 6 should first implement and
test a UKF-frame bridge for author-SIR step 1, then use that same frame for
fresh training batches and holdout/replay diagnostics.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Draft a bounded Phase 6 pilot subplan | Passed: Phase 4 mechanics and provenance are accepted, and the missing question now requires fresh-batch training in the UKF frame | No Phase 5 veto fired because no pilot was launched and no failed-method ladder was revived | The UKF frame may have poor support coverage; clipping or nonfinite targets may block before training | Draft Phase 6 as implementation-plus-bounded-pilot planning, with a hard UKF-frame tieout before training and separate approval before execution | No lower-gate repair, no validation/HMC readiness, no scaling, no final rank/sample policy |

## Required Phase 6 Direction

Phase 6 should be a bounded implementation/pilot phase, not a live comparison
against the failed P75 methods.

Required Phase 6 elements:

- add an opt-in `ukf_initializer` mode or dedicated P76 pilot entrypoint;
- build a `SourceRouteCoordinateFrame` from the P76 UKF moments for the
  author-SIR step-1 adjacent target;
- ensure the `ProductBasis`, training points, target values, and initial TT
  cores share that UKF local frame;
- generate fresh mini-batches with new training seeds;
- reserve audit holdout/replay/line diagnostics for evaluation only;
- record clipping fractions, nonfinite-target checks, loss traces, gradient
  norms, normalizer/rho ranges, and audit residuals;
- block if the UKF frame causes all or near-all local coordinates to clip, if
  target values are nonfinite, or if training uses audit data;
- require separate user approval before running any pilot beyond reviewed
  tiny/local checks.

The failed random, calibrated constant, and source-route prefit methods may
appear only as historical context or optional sentinel checks in a later
reviewed plan.  They must not be the Phase 6 live repair ladder.

## Local Checks

Commands run before Claude review:

```bash
test -s docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json
rg -n "P76_PHASE4_TINY_SMOKE_COMPLETED|finite_total_loss|finite_gradient_norm|finite_rho_theta|finite_normalizer|finite_log_density|source_route_prefit_used|audit_data_used|cpu_only|train_step_count|python_executable|python_argv|environment" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json
rg -n "Decision Table|bounded mini-batch pilot|not lower-gate repair|not validation|not HMC readiness|separate approval" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase5-minibatch-pilot-decision-result-2026-06-18.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p76-phase5-minibatch-pilot-decision-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-stop-handoff-2026-06-18.md
```

Observed status before Claude review:

- Phase 4 artifact exists and required fields are present;
- Phase 5 result contains the required decision and nonclaims;
- Phase 6 subplan contains the UKF-frame tieout, fresh-batch, audit-separation,
  and separate-approval boundaries;
- `git diff --check` passed.

## Phase 6 Handoff

Phase 6 may begin only after Claude agrees this Phase 5 decision and the
Phase 6 subplan are consistent, feasible, and bounded.  If Phase 6 includes a
pilot run, that run still requires the user approval specified in the Phase 6
subplan.

## Claude R1 Review And Repair

Claude R1 returned `VERDICT: REVISE`.

Claude agreed the Phase 5 decision was substantively correct and that Phase 6
properly avoids the old P75 failed-method ladder.  Claude requested two
repairs before Phase 6 could be considered safe:

1. make the UKF-frame bridge check operational rather than narrative;
2. remove the implementation-path ambiguity between editing the P75 pilot and
   creating a dedicated P76 pilot script.

Repairs applied:

- Phase 6 now requires a dedicated
  `scripts/p76_bounded_ukf_minibatch_pilot.py`;
- Phase 6 forbids editing `scripts/p75_stochastic_density_training_pilot.py`;
- Phase 6 requires a `ukf_frame_bridge` JSON block with dimension, frame-hash,
  reconstruction, target-tieout, clipping, finite-target, and blocker fields;
- Phase 6 makes failed bridge status a hard stop before optimizer
  construction or training.

## Claude R2 Review And Repair

Claude R2 returned `VERDICT: REVISE`.

Claude agreed the dedicated-script ambiguity was fixed and that approval,
safety, audit, and failed-method boundaries remain intact.  The remaining
material gap was that the result/ledger repair narrative mentioned
finite-target bridge fields, but the operative Phase 6 subplan did not name
those fields in the required `ukf_frame_bridge` list.

Repair applied:

- Phase 6 now requires `bridge_target_values_finite`,
  `training_target_values_finite`, `audit_target_values_finite`, and
  `nonfinite_target_value_count` in the `ukf_frame_bridge` block;
- Phase 6 makes those fields part of the pass rule:
  all finite flags must be true and `nonfinite_target_value_count == 0`.

## Claude R3 Review

Claude R3 returned `VERDICT: AGREE`.

Claude agreed:

- the R2 finite-target repair is operative in the Phase 6 subplan;
- the finite-target fields are part of the bridge pass computation;
- Phase 5 result and ledgers consistently record the same repair;
- no boundary regression was found for separate approval, CPU-only/no-GPU,
  no defaults, no network, no detached execution, audit separation, or the
  ban on failed-method live ladders.

Phase 5 is closed.  Phase 6 is reviewed as a subplan but not launched.
