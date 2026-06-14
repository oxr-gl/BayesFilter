# Review Loop: Row 173 Proposal/Update Adjoint-Topology Probe

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

Claude status: `REJECT`.

- Claude finding: Evidence contract lacks an explicit pass criterion for when
  the probe has answered the BayesFilter-vs-float64-FilterFlow difference-audit
  question.
- Codex classification: `ACCEPT`.
- Codex evidence: The plan listed diagnostics and hypothesis labels, but did
  not state the rule that converts successful diagnostics into an answered
  probe.
- Control added or rebuttal: Added a `Pass criterion` section requiring all
  veto diagnostics to pass and requiring the result to classify the row-173
  target-time-93 gradient mismatch into one listed hypothesis outcome, or an
  explicitly bounded multi-hypothesis classification when supported.

- Claude finding: The `claude -p` review command is not constrained to
  trusted/escalated cross-agent execution as required by governance.
- Codex classification: `ACCEPT`.
- Codex evidence: `AGENTS.md` requires Claude Code commands to run with
  elevated or trusted permissions and treats non-escalated Claude failures as
  sandbox evidence only.
- Control added or rebuttal: Added a control under the Claude command requiring
  trusted/escalated cross-agent execution and forbidding non-escalated Claude
  hangs, auth failures, or missing output from being treated as substantive
  reviews.

Round 1 disposition: patched and resubmitted.

### Round 2

Claude status: `ACCEPT`.

- Claude finding: No findings.
- Codex classification: `ACCEPT`.
- Codex evidence: The patched result now avoids the rejected broad h3
  log-prob-gradient claim and classifies the evidence as
  `h4_downstream_update_topology`, specifically a proposal-likelihood
  wiring/topology difference: direct/fresh distribution log-prob gradient
  probes match, while the official proposal-likelihood path into proposed
  particles differs. Vetoes are clear and non-claims remain explicit.
- Control added or rebuttal: No patch required.

Result review disposition: accepted.

### Round 3

Claude status: `ACCEPT`.

- Claude finding: No findings.
- Codex classification: `ACCEPT`.
- Codex evidence: After Claude round 2 accepted, Codex corrected one stale
  decision-table wording string from `two probe times` to `one probe time` in
  the runner, JSON, report, and result artifacts to match `PROBE_TIMES=(43,)`.
  The numerical evidence, decision, hypothesis classification, and non-claims
  were unchanged.
- Control added or rebuttal: No patch required.

Final result review disposition: accepted.

### Round 2

Claude status: `ACCEPT`.

- Claude finding: No findings.
- Codex classification: `ACCEPT`.
- Codex evidence: The patched plan now has a pass criterion, explicit
  trusted/escalated Claude execution control, bounded row/time scope,
  CPU-only controls, comparator governance, forbidden-write controls, stop
  conditions, and clear non-claims.
- Control added or rebuttal: No patch required.

Plan review disposition: accepted for execution.

## Result Review

### Round 1

Claude status: `REJECT`.

- Claude finding: `h3_log_prob_gradient_contract` is not adequately supported
  as phrased. The decisive mismatch is `proposal_ll_to_proposed_particles`,
  while `fresh_dist_log_prob_to_proposed_particles` matches and
  `proposal_dist_log_prob_to_proposed_particles` is zero on both sides. The
  evidence supports a narrower BayesFilter-vs-FilterFlow proposal-likelihood
  wiring/topology difference, not a generic local log-prob gradient contract
  difference. Claude accepted the stop-gradient ablations as explanatory only
  and the CPU-only/path-boundary/non-claim controls as sufficient.
- Codex classification: `ACCEPT`.
- Codex evidence: The result JSON shows the max local gradient delta at
  `proposal_ll_to_proposed_particles` with BayesFilter max `0.0` and
  FilterFlow max `28.749898405961705`, while the fresh distribution local
  gradient agrees and the direct sampled distribution log-prob local gradient
  is zero on both sides. Therefore the broad h3 label overstates the exact
  localized mechanism.
- Control added or rebuttal: Patch the runner/result language to classify the
  result as `h4_downstream_update_topology` with reason
  `proposal_likelihood_wiring_topology`, and preserve the direct local-gradient
  rows as the evidence. Do not claim a generic log-prob gradient-contract
  mismatch.

Round 1 disposition: patched and resubmitted.
