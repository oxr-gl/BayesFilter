# Review Loop: Row 173 Previous Log-Weight Jacobian Localization

## Plan Review Iteration 1

Claude command:

```bash
claude -p --model claude-opus-4-7 --effort max 'Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-previous-log-weight-jacobian-localization-plan-2026-06-06.md plus AGENTS.md and CLAUDE.md read-only. Review whether the plan is adequate to localize the row-173 previous-log-weight carry Jacobian mismatch between BayesFilter and local executable float64 FilterFlow under difference-audit governance. Check evidence contract, comparator, exact inputs/outputs, CPU-only controls, lane/write boundaries, stop conditions, primary versus explanatory metrics, decision rule, non-conclusions, and Claude/Codex finding-classification rules. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.'
```

Claude result: `ACCEPT`

Claude rationale summary:

- The evidence contract states the question, local executable float64
  FilterFlow comparator, exact row/time inputs, output artifact, primary
  component-VJP criterion, vetoes, and non-conclusions.
- Comparator, CPU-only, lane-boundary, and exact-I/O controls are materially
  present.
- The plan separates component VJPs as primary evidence from total-gradient
  deltas as explanatory evidence only.
- No material missing control was found that would invalidate the evidence
  contract or review governance.

Codex audit classification: `ACCEPT`

Codex action: no plan patch required before implementation.

## Result Review Iteration 1

Claude command:

```bash
claude -p --model claude-opus-4-7 --effort max 'Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-previous-log-weight-jacobian-localization-result-2026-06-06.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-previous-log-weight-jacobian-localization-plan-2026-06-06.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-previous-log-weight-jacobian-localization-review-loop-2026-06-06.md, experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_previous_log_weight_jacobian_localization_tf.py, and experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_previous_log_weight_jacobian_localization_2026-06-06.json read-only. Review whether the result follows the accepted plan, uses the hypothesis decision rule correctly, preserves BayesFilter-vs-local-executable-float64-FilterFlow difference-audit governance, records exact inputs/fingerprints/artifacts, enforces CPU-only and lane-boundary controls, validates prior unit-upstream evidence, and avoids non-concluded correctness claims. Pay special attention to whether h2_proposal_log_prob_route_differs is justified by raw proposal_ll and signed-sum VJP deltas while the fresh proposal-log-prob route collapses the normalized carry delta. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.'
```

Claude result: `ACCEPT`

Claude rationale summary:

- The result follows the accepted evidence contract, veto structure, ordered
  hypotheses, and non-conclusions.
- CPU-only controls are enforced in the parent and executable FilterFlow
  subprocess, and all recorded CPU manifests pass.
- Difference-audit governance is preserved with clean lane-boundary flags,
  comparator fingerprints recorded initial/final, and no comparator drift.
- Prior unit-upstream evidence is validated through the accepted prior
  decision/classification and recorded digest.
- The `h2_proposal_log_prob_route_differs` classification is justified because
  raw BayesFilter has material `proposal_ll` and signed-sum VJP deltas, while
  the fresh proposal-log-prob route collapses the normalized carry and
  post-update log-weight deltas below tolerance.
- No material missing control was found that would invalidate the evidence
  contract, CPU-only policy, lane governance, reproducibility, ordered decision
  rule, or stated non-conclusions.

Codex audit classification: `ACCEPT`

Codex action: no result patch required.
