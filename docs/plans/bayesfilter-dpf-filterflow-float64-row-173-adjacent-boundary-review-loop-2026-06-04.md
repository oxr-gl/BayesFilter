# Review Loop: Row 173 Adjacent-Boundary Gradient Probe

## Plan Review

### Round 1

Claude command:

```bash
claude -p --model claude-opus-4-7 --effort max 'Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-adjacent-boundary-plan-2026-06-04.md. Review it read-only against AGENTS.md and CLAUDE.md. Output ACCEPT or REJECT first. If REJECT, list findings with exact required controls. Do not edit files.'
```

Claude status: `REJECT`.

Codex-supervisor audit classifications:

- Finding 1, missing artifact field in evidence contract: `ACCEPT`. Added an
  explicit `Artifact:` line naming the result note and JSON output.
- Finding 2, missing expected failure modes section: `ACCEPT`. Added
  `## Expected Failure Modes` separating instrumentation, comparator, JSON,
  diagnostic, and governance failures.
- Finding 3, missing what-would-change-our-mind section: `ACCEPT`. Added exact
  branching rules for cross-VJP reconstruction, active-sample cancellation,
  boundary rejection, and veto diagnostics.
- Finding 4, incomplete manifest planning: `ACCEPT`. Added a runner requirement
  to record full run-manifest fields, including git, command, environment,
  CPU-only status, seeds, wall time, plan, result, and output paths.
- Finding 5, Claude command/trusted execution control: `PARTIAL`. The user
  explicitly requires the exact raw command
  `claude -p --model claude-opus-4-7 --effort max`, so the patch preserves that
  exact command while adding the required trusted/elevated execution control and
  sandbox-failure caveat.

Patch applied: governance controls above were added to the plan.

### Round 2

Claude command:

```bash
claude -p --model claude-opus-4-7 --effort max 'Re-review docs/plans/bayesfilter-dpf-filterflow-float64-row-173-adjacent-boundary-plan-2026-06-04.md read-only after patches. Prior findings were addressed. Note: Codex partially accepted the Claude-command finding because the human explicitly requires the exact command `claude -p --model claude-opus-4-7 --effort max`; the plan now preserves that exact command while requiring trusted/elevated execution and treating non-escalated failures as sandbox evidence only. Output ACCEPT or REJECT first. If REJECT, list only remaining material findings with exact required controls. Do not edit files.'
```

Claude status: `ACCEPT`.

Claude findings: none.

Codex-supervisor audit: `ACCEPT`. I independently agree that the patched plan
now includes artifact preservation, expected failure modes, mind-change
criteria, full manifest requirements, and trusted/elevated Claude execution
while preserving the user-required exact command. No further patch required.

## Result Review

### Round 1

Claude command:

```bash
claude -p --model claude-opus-4-7 --effort max 'Read the following files read-only: docs/plans/bayesfilter-dpf-filterflow-float64-row-173-adjacent-boundary-result-2026-06-04.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-adjacent-boundary-plan-2026-06-04.md, experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_adjacent_boundary_probe_tf.py. Review only whether the result follows the plan, preserves difference-audit governance, records the CPU-only/lane/JSON controls, and supports the stated adjacent-boundary conclusion without overclaiming correctness. Output ACCEPT or REJECT first. If REJECT, list exact required controls. Do not edit files.'
```

Claude status: `ACCEPT`.

Claude findings: none.

Codex-supervisor audit: `ACCEPT`. I independently agree that the result records
the value/direct-theta gates, reconstructs the observed residual through
`post_update_log_likelihoods`, preserves the single-row/time scope, and does not
claim mathematical correctness for either implementation. No patch required.
