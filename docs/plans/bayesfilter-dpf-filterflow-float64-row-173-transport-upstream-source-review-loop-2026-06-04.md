# Review Loop: Row 173 Transport-Upstream Source Probe

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

Execution gate: implementation may not begin until every Claude plan finding
has a recorded Codex classification and either:

- Claude returns `ACCEPT` and Codex independently records `ACCEPT`; or
- round 5 is reached with no major blocker, accepted only for user inspection.

Per-finding ledger template for each round:

- Claude finding: `<verbatim or concise summary>`
- Codex classification: `ACCEPT | PARTIAL | DISPUTE | CLARIFY`
- Codex evidence: `<file/section evidence>`
- Control added or rebuttal: `<exact patch/control, or rebuttal carried into
  next Claude prompt>`

### Round 1

Claude status: `ACCEPT`

Findings:

- None.

Codex-supervisor audit:

- `ACCEPT`: Codex independently agrees the plan has a clear evidence contract,
  comparator policy, allowed/forbidden write set, skeptical pre-execution
  audit, bounded phase order, stop conditions, verification commands, and
  explicit Claude/Codex review gate before execution.

## Result Review

### Round 1

Claude status: `ACCEPT`

Findings:

- None.

Codex-supervisor audit:

- `ACCEPT`: Codex independently agrees the final regenerated result satisfies
  the accepted evidence contract. The runner compares forward tensors
  elementwise at times 43 and 52, separates first adjoint divergence from
  dominant adjoint contributors, preserves the difference-audit boundary, and
  records clear non-implications. The formal classification is conservative:
  `h2_downstream_adjoint_topology_mismatch`, with proposal/update adjoints
  recorded as dominant explanatory contributors at time 43 rather than as the
  formal first-difference classification.
