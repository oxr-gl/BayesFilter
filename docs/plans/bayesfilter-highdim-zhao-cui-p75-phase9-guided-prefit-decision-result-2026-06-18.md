# P75 Phase 9 Result: Guided Prefit Decision And Next Handoff

metadata_date: 2026-06-18
status: PHASE9_DECISION_PASSED_CLAUDE_AGREE_READY_FOR_PHASE10
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase9-guided-prefit-decision-subplan-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase8-source-guided-prefit-implementation-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | What should P75 do after source-guided prefit passes a tiny mechanism test but audit-line still blocks? |
| Exact baseline/comparator | Phase 8 same-draw random, calibrated-constant, and source-guided-prefit arms. |
| Primary criterion | Satisfied locally by selecting a bounded next diagnostic: a small capacity/sample/prefit-step ladder under Phase 10. |
| Diagnostics that can veto | No lower-gate repair claim is made; the audit-line block is preserved; no large pilot is launched or authorized; no validation/HMC/scaling/source-faithfulness claim is made. |
| Explanatory only | Holdout/replay residual magnitudes, line residual magnitudes, prefit loss, rho range, gradient norm, runtime. |
| What is not concluded | No lower-gate repair, validation readiness, HMC readiness, scaling, source-faithfulness, or final rank/sample policy. |
| Artifact preserving result | This result, Phase 10 subplan, ledgers, Claude review. |

## Phase 8 Evidence Classification

Phase 8 established three useful but limited facts:

1. Random initialization remains unusable in this 36-dimensional target-pilot
   smoke:
   \[
      \rho_{\max}=10^{-8},\qquad
      \|\nabla \mathcal L\|\approx 8.66\times 10^{-9}.
   \]

2. Calibrated constant initialization escapes the defensive floor:
   \[
      \rho_{\max}=0.07108014879268504,\qquad
      \|\nabla \mathcal L\|=5.837615542844192.
   \]

3. Source-guided prefit is a working opt-in mechanism and slightly improves
   the frozen holdout RMS-relative criterion:
   \[
      0.9568899680347903
      \quad\longrightarrow\quad
      0.949791415738309.
   \]

The third improvement is small.  It is enough to keep `source_guided_prefit`
as an opt-in mechanism, but it is not enough to justify the large pilot or any
claim that the fixed-variant lower gate has been repaired.

## Blocking Evidence Preserved

All Phase 8 arms still have audit status `block` with `audit_line_veto`.
Representative line residuals remain large:

| Arm | line residual RMS | audit status |
| --- | ---: | --- |
| random | `67.78305872004482` | `block` |
| calibrated constant | `67.64689532762196` | `block` |
| source-guided prefit | `67.67056944530965` | `block` |

Therefore Phase 9 cannot select validation, HMC, scaling, rank promotion, or
the large degree-2/rank-4/batch-1024/500-batch pilot as an immediate action.

## Decision

Proceed to a bounded Phase 10 diagnostic ladder that tests whether the small
Phase 8 improvement becomes material under slightly more capacity and data.
The ladder must remain small enough to be a diagnostic, not the large pilot.

The selected next diagnostic should vary only reviewed knobs:

- degree: `1` and `2`;
- rank: `1` and `2`;
- batch size: `32` and `64`;
- prefit steps: `0`, `5`, and `10`, with `0` representing the calibrated
  constant arm rather than a prefit arm;
- density-objective batches: `2` and `4`;
- CPU-only execution;
- identical density-training and audit draws across arms within each row;
- audit data excluded from initialization, prefit, training, stopping, and
  hyperparameter selection.

The ladder's primary output should be a decision table, not a promotion.  It
may nominate a later reviewed pilot only if the small ladder shows a material
and stable improvement in the frozen diagnostics while audit-line behavior is
understood.  It cannot authorize the large run by itself.

## Large-Pilot Boundary

The degree-2/rank-4/batch-1024/500-batch pilot remains outside Phase 9 and
outside Phase 10.  It may be proposed only as a future human decision after a
separate reviewed plan.  Phase 9 documentation review does not authorize it.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Run a small Phase 10 capacity/sample/prefit-step diagnostic ladder | Satisfied locally: Phase 8 mechanism pass is correctly classified and next action is bounded | Audit-line still blocks; large pilot remains forbidden | Whether rank/degree/sample/prefit-step increases make the prefit improvement material or reveal a different blocker | Draft and review Phase 10 subplan before any new run | No lower-gate repair, validation/HMC readiness, scaling, source-faithfulness, final rank/sample policy, or large-pilot authorization |

## Local Checks Passed

```text
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p75-source-guided-prefit-smoke-2026-06-18.json >/tmp/p75_phase9_json_check.txt
status: passed

rg -n "source_guided_prefit|audit_line_veto|lower-gate|validation|large pilot|large-pilot|degree-2/rank-4|Phase 10|10 percent|same-draw|human" docs/plans/bayesfilter-highdim-zhao-cui-p75-phase9-guided-prefit-decision-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase10-capacity-sample-ladder-subplan-2026-06-18.md >/tmp/p75_phase9_rg_check.txt
status: passed with expected governance and boundary hits

git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p75-phase9-guided-prefit-decision-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase10-capacity-sample-ladder-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-claude-review-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
status: passed
```

## Skeptical Plan Audit

The Phase 9 decision passes the skeptical audit locally because it uses Phase
8 as the actual baseline, keeps audit-line as a veto against repair claims,
selects a bounded diagnostic rather than the large pilot, and does not promote
holdout improvement or training loss into validation evidence.
