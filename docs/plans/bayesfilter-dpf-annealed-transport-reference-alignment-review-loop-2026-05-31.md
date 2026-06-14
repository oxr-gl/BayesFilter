# Review Loop: OT-DPF Reference Alignment And Annealed Transport

## Purpose

This artifact records Claude Code review rounds and Codex-supervisor
classifications for
`docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-plan-2026-05-31.md`
and
`docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-result-2026-05-31.md`.

## Protocol

Claude command:

```bash
claude -p --model claude-opus-4-7 --effort max
```

For every Claude finding, Codex classifies it as:

- `ACCEPT`: materially correct; patch required.
- `PARTIAL`: directionally correct but needs a different or narrower patch.
- `DISPUTE`: incorrect, over-scoped, inconsistent with policy, or would weaken
  governance.
- `CLARIFY`: cannot evaluate without more evidence or human direction.

Accepted or partially accepted findings require an exact control/patch record.
Disputed findings require a concise rebuttal with file/section evidence and
must be included in the next Claude prompt.

## Plan Review Rounds

### Round 1

Claude status: `ACCEPT`

Codex-supervisor audit: Codex independently agrees that the plan enforces the
required governance controls and execution order.

| Finding | Codex classification | Codex rationale | Control added |
| --- | --- | --- | --- |
| Plan covers reference hierarchy, patched executable filterflow reference, fixed-target demotion, executable `I_2`, TF/TFP lane, and write boundaries. | `ACCEPT` | The cited plan sections explicitly encode these controls. | None; accepted as already controlled. |
| Plan specifies annealed transport, gradient scalar contract, LEDH contract, nonlinear ladder, stop conditions, and verification. | `ACCEPT` | The plan contains concrete contracts and stop conditions for each required phase. | None; accepted as already controlled. |
| Phase order matches the requested seven-gap sequence. | `ACCEPT` | The phase order maps to reference policy, component extraction, LGSSM match, gradient contract, LEDH, nonlinear ladder, verification, and result review. | None; accepted as already controlled. |
| Claude and Codex-supervisor review protocols are explicit. | `ACCEPT` | The plan and this ledger require classification, rebuttal handling, and five-round stop rules. | None; accepted as already controlled. |
| Minor note: review-loop artifact was empty before first review. | `ACCEPT` | This was expected before the first review. | This Round 1 ledger entry records the review outcome. |

## Result Review Rounds

### Round 1

Claude status: `REJECT`

Codex-supervisor audit: Codex independently agrees with the two governance
findings and partially agrees with the gradient wording finding. The result
artifact needs a status patch and stronger wording for the gradient mismatch.

| Finding | Codex classification | Codex rationale | Control added |
| --- | --- | --- | --- |
| Result review loop incomplete because result artifact and review-loop ledger still said pending/not run. | `ACCEPT` | The plan requires result review plus Codex classification before final acceptance; the artifacts still had pre-review placeholders. | Patched result artifact and this ledger to record Round 1 `REJECT` and Codex classification. |
| Final result claimed acceptance/no blockers before result review completion. | `ACCEPT` | The acceptance statement was premature until Claude result review and Codex classification were recorded. | Patched decision/status to `REVIEW_ROUND_1_REJECT_PATCHED_FOR_RESUBMISSION` before resubmitting. |
| Gradient evidence is caveated, but "scale risk" wording understates a huge mismatch. | `PARTIAL` | The result already forbids gradient agreement claims, but the risk wording should explicitly say severe/unreconciled gradient magnitude mismatch. | Patched result wording from scale risk to severe unreconciled gradient mismatch risk. |
| Positive checks for fixed-target demotion, executable filterflow/`I_2`, TF-only component, LGSSM match, bounded LEDH/nonlinear caveats, and lane boundaries. | `ACCEPT` | Codex agrees these controls are present and no patch is required. | None; accepted as already controlled. |

### Round 2

Claude status: `REJECT`

Codex-supervisor audit: Codex independently agrees. The result text had
stronger gradient-risk wording, but the gradient subsection still displayed
the old soft decision string.

| Finding | Codex classification | Codex rationale | Control added |
| --- | --- | --- | --- |
| Gradient-contract subsection still carries stale `annealed_transport_gradient_contract_scale_risk_recorded` label, inconsistent with severe unresolved mismatch wording. | `ACCEPT` | The displayed decision string could weaken governance by preserving the old softer wording. | Patched result/report/summary JSON to use `annealed_transport_gradient_contract_severe_unreconciled_magnitude_risk_recorded` as the reported status. |
| All other requested controls are present. | `ACCEPT` | Codex agrees with the positive checks. | None; accepted as already controlled. |

### Round 3

Claude status: `REJECT`

Codex-supervisor audit: Codex independently agrees. The consolidated report
and summary JSON still had stale soft gradient-risk labels even though the
result artifact and gradient runner were patched.

| Finding | Codex classification | Codex rationale | Control added |
| --- | --- | --- | --- |
| Consolidated report still says `ACCEPTED_WITH_GRADIENT_SCALE_RISK`. | `ACCEPT` | This stale label understates the severe unresolved gradient mismatch. | Patched consolidated report decision to `ACCEPTED_WITH_SEVERE_UNRECONCILED_GRADIENT_MISMATCH_RISK`. |
| Summary JSON nested ledger still says `recorded_scale_gap_not_reconciled`. | `ACCEPT` | This stale label conflicts with the severe gradient decision and could weaken governance. | Patched summary JSON ledger status from the regenerated gradient JSON to severe unresolved mismatch wording. |
| Result artifact and gradient runner/report correctly use severe mismatch wording. | `ACCEPT` | Codex agrees with the positive check. | None; accepted as already controlled. |

### Round 4

Claude status: `REJECT`

Codex-supervisor audit: Codex independently agrees. Claude widened the
consistency check to the prior filterflow gap-closure artifacts and runners.
Those artifacts are part of the active evidence chain for this program, so
stale softer gradient-risk labels there could weaken governance.

| Finding | Codex classification | Codex rationale | Control added |
| --- | --- | --- | --- |
| Prior gap-closure result/report/JSON still use softer gradient scale-risk labels. | `ACCEPT` | The current program depends on those artifacts as inputs and evidence history; stale softer labels conflict with the severe unresolved mismatch policy. | Patch prior gap-closure docs/reports/JSON to severe unreconciled gradient-magnitude wording without changing numerical evidence. |
| Prior smoothness-gradient audit report/JSON still use softer scalar-gap labels. | `ACCEPT` | The smoothness audit is the source of the gradient mismatch and should use the same severe risk wording. | Patch report/JSON labels to severe unreconciled gradient-magnitude wording. |
| Generating runners still encode old soft labels. | `ACCEPT` | Future reruns would regenerate stale labels unless the runners are updated. | Patch runner decision/status strings and interpretations only; no numerical logic changes. |

### Round 5

Claude status: `REJECT`

Codex-supervisor audit: Codex independently agrees with the concrete
bookkeeping findings. The remaining issue is stale status/label propagation in
older generator defaults and their JSON/report outputs, not a new numerical
failure. The protocol maximum of five result-review rounds has been reached, so
downstream acceptance is blocked pending human decision or explicit
authorization for another review round.

| Finding | Codex classification | Codex rationale | Control added |
| --- | --- | --- | --- |
| Prior gap-closure runner/JSON still contain `pending_result_review`. | `ACCEPT` | This is a concrete stale placeholder in the active evidence chain. | Patched `run_filterflow_gap_closure_program_tf.py` to record reconciled prior review status and regenerated the gap-closure report/JSON. |
| Prior full-comparison runner/JSON/report still contain `pending_result_review` and softer gradient warning labels. | `ACCEPT` | Future reruns would reintroduce stale labels and the softer wording understates the unresolved gradient mismatch. | Patched `run_filterflow_full_comparison_tf.py` to record reconciled prior review status and severe unreconciled gradient-magnitude wording, then regenerated the report/JSON. |
| Prior final-gaps runner/report/JSON still contain softer smoothness-gradient scale-warning wording. | `ACCEPT` | The final-gaps artifact is an upstream source for the full comparison; stale wording weakens the severe gradient-risk ledger. | Patched `run_filterflow_final_gaps_closure_tf.py` to emit severe unreconciled gradient-magnitude wording and regenerated the report/JSON. |
| Top-level result/report/summary JSON still imply accepted result-review status. | `ACCEPT` | Claude did not converge to `ACCEPT` within five result-review rounds, so acceptance language is not valid without human decision. | Patched the top-level result, consolidated report, and summary JSON to `BLOCKED_MAX_REVIEW_ROUNDS_REACHED_AFTER_PATCHES` status. |
