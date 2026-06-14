# Review Loop: Row 173 Transport-Upstream Clipping Hypothesis Probe

## Protocol

Claude command:

```bash
claude -p --model claude-opus-4-7 --effort max
```

For every Claude finding, Codex independently classifies it as `ACCEPT`,
`PARTIAL`, `DISPUTE`, or `CLARIFY`. Accepted or partially accepted findings
must be patched and the exact control recorded. Disputed findings require a
concise rebuttal and must be carried into the next Claude prompt.

## Plan Review

### Round 1

Claude status: `REJECT`

Findings:

1. Forbidden student/vendored lane control is incomplete: the plan used
   `high-dimensional` rather than `highdim`, and the verification `git status`
   command did not check the forbidden student/vendored lanes.
2. Non-conclusion guard did not explicitly forbid concluding global gradient
   agreement.

Codex-supervisor audit:

1. `ACCEPT`: materially correct. Patch added exact `highdim` wording and added
   `experiments/controlled_dpf_baseline` to the forbidden-lane `git status`
   verification command alongside `third_party`.
2. `ACCEPT`: materially correct. Patch added explicit `global gradient
   agreement` to the `What must not be concluded` list.

### Round 2

Claude status: `ACCEPT`

Codex-supervisor audit:

- `ACCEPT`: Codex independently agrees the revised plan now enforces the
  reference hierarchy, write boundaries, evidence contract, stop conditions,
  verification commands, and non-conclusion controls required for this
  target-time transport-upstream clipping difference audit.

## Result Review

### Round 1

Claude status: `REJECT`

Findings:

1. Missing non-implication control: the result omitted the accepted plan's
   `no posterior correctness` guard in the Markdown, JSON
   `non_implications`, `evidence_contract.not_concluded`, and
   `decision_table.not_concluded`.

Codex-supervisor audit:

1. `ACCEPT`: materially correct. Patch added `No posterior correctness is
   concluded.` to `_non_implications()` and added `posterior correctness` to
   the decision-table `not_concluded` string in
   `run_filterflow_float64_row_173_transport_upstream_clipping_probe_tf.py`.

### Round 2

Claude status: `ACCEPT`

Codex-supervisor audit:

- `ACCEPT`: Codex independently agrees the revised result enforces the
  difference-audit boundary and non-implication controls, and that the h3
  classification is supported only for the target-time transport probe:
  raw/clipped upstreams and masks match within tolerance, while target-time
  transport VJP deltas exceed tolerance. The result does not claim full row
  residual reconstruction, global gradient agreement, posterior correctness,
  or production readiness.
