# Review Loop: Row 173 BayesFilter Carryover Split Probe

## Plan Review Round 1

Command:

```bash
claude -p --model claude-opus-4-7 --effort max 'Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-plan-2026-06-05.md plus AGENTS.md and CLAUDE.md read-only. Review whether the plan is adequate to test the current row-173 BayesFilter carryover/identity residual split hypotheses under BayesFilter-vs-local-float64-FilterFlow difference-audit governance. Check evidence contract, exact inputs/outputs, lane boundaries, CPU-only controls, stop conditions, non-conclusions, decision rule, and Claude/Codex finding-classification rules. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.'
```

Claude status: `ACCEPT`

Claude summary:

> The evidence contract is adequately specified, exact reproducibility controls
> are materially present, lane boundaries and CPU-only controls are explicit,
> the ordered decision rule is usable, and the Claude/Codex
> finding-classification rules are explicit. No material missing control rises
> to `REJECT`.

Codex-supervisor classification:

- No material findings. `ACCEPT`.

Plan patch status after round 1: no patch required.

## Result Review Round 1

Command:

```bash
claude -p --model claude-opus-4-7 --effort max 'Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-result-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-plan-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-review-loop-2026-06-05.md, and experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_bayesfilter_carryover_split_tf.py read-only. Review whether the result follows the accepted plan, uses the decision rule correctly, preserves difference-audit governance, records exact inputs/fingerprints, lane-boundary and CPU-only controls, and avoids non-concluded claims. Pay special attention to whether the h3 carried-log-weight classification is valid under the ordered rule given that target_transport_log_weights_stop_gradient also collapses the full-recorded-state/log-weight residual but does not reduce same_tape_identity_residual or same_tape_post_state_identity_residual. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.'
```

Claude status: `REJECT`

Finding and Codex classification:

- `ACCEPT`: the `h3` carried-log-weight label follows the accepted ordered
  rule, but the result did not explicitly record why `h2` did not fire even
  though `target_transport_log_weights_stop_gradient` collapses the
  full-recorded-state/log-weight fields. Without that explicit rationale, the
  result could be misread as target-transport evidence.

Patch status:

- Added `ordered_rule_audit` to the runner result payload and report.
- The audit records that `target_transport_log_weights_stop_gradient` does not
  materially reduce `same_tape_identity_residual` or
  `same_tape_post_state_identity_residual`, so `h2` does not fire under the
  accepted rule.
- The audit also records that target-transport stopping does collapse
  `same_tape_full_recorded_state_residual` and
  `same_tape_pre_log_weights_carryover_vjp` as explanatory-only log-weight
  evidence.

## Result Review Round 2

Command:

```bash
claude -p --model claude-opus-4-7 --effort max 'Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-result-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-plan-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-review-loop-2026-06-05.md, and experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_bayesfilter_carryover_split_tf.py read-only. Review whether the patched result now follows the accepted plan, uses the ordered decision rule correctly, explicitly records why h2 did not fire despite target_transport_log_weights_stop_gradient collapsing full-recorded-state/log-weight fields, preserves difference-audit governance, records exact inputs/fingerprints, lane-boundary and CPU-only controls, and avoids non-concluded claims. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.'
```

Claude status: `ACCEPT`

Claude summary:

> The patched result follows the accepted ordered rule. The previously missing
> rationale is explicit: `ordered_rule_audit` records that
> `target_transport_log_weights_stop_gradient` does not materially reduce the
> two `h2` fields, while its collapse of full-recorded-state/log-weight fields
> is explanatory only. Difference-audit governance, CPU-only controls, lane
> boundaries, run manifest fields, and non-conclusions are preserved.

Codex-supervisor classification:

- No material findings. `ACCEPT`.

Result patch status after round 2: no further patch required.
