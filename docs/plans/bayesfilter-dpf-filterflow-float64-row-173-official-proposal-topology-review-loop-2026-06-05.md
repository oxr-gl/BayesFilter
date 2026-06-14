# Review Loop: Row 173 Official Proposal-Likelihood Topology Probe

Claude command template:

```bash
claude -p --model claude-opus-4-7 --effort max '<prompt>'
```

For every Claude finding, Codex independently classifies it as `ACCEPT`,
`PARTIAL`, `DISPUTE`, or `CLARIFY`.  Accepted or partially accepted findings
must be patched and the exact control recorded.  Disputed findings must include
a concise rebuttal and be carried into the next Claude prompt.

Execution gate: implementation may not begin until every Claude plan finding is
resolved and either:

- Claude returns `ACCEPT` and Codex independently records `ACCEPT`; or
- round 5 is reached with no major blocker and the remaining discrepancy is
  recorded for human inspection.

## Round 1 Plan Review

Claude status: `REJECT`.

- Claude finding: `proposal_ll_to_sampling_proposal_mean` is
  decision-critical but not in the primary criterion.
- Codex classification: `ACCEPT`.
- Control added: moved `proposal_ll_to_sampling_proposal_mean` into the primary
  criterion and tightened the `h1_internal_node_reconciles_official_vjp`
  decision rule to require zero VJP to sampling proposal mean plus matching
  proposed-particles and internal-likelihood-mean VJPs.

- Claude finding: exact input control is not frozen tightly enough.
- Codex classification: `ACCEPT`.
- Control added: named the canonical upstream JSON/result/code artifacts and
  required the output JSON/report to echo or fingerprint row, times, seeds,
  theta, particles, observations, covariances, ESS/resampling settings,
  transport settings, and FilterFlow comparator fingerprints.

- Claude finding: lane-boundary enforcement is incomplete relative to the
  forbidden lanes.
- Codex classification: `ACCEPT`.
- Control added: added explicit status checks for controlled/student,
  vendored/third-party, highdim, DSGE, and NAWM lane paths/patterns in addition
  to `bayesfilter`, `tests`, `docs/chapters`, and `.localsource/filterflow`.

- Claude finding: Claude/Codex review-finding classification rules are missing.
- Codex classification: `ACCEPT`.
- Control added: added explicit materiality rules for Claude `REJECT` and
  Codex finding classifications, and updated the plan/result review prompts.

## Round 2 Plan Review

Claude status: `ACCEPT`.

- Claude finding: No findings.
- Codex classification: `ACCEPT`.
- Codex evidence: The revised plan now includes `proposal_ll_to_sampling_proposal_mean`
  in the primary criterion, exact canonical input sources and required output
  fingerprints, explicit forbidden-lane status checks, CPU-only controls,
  stop conditions, bounded non-conclusions, and materiality rules for review
  findings.

Plan review disposition: accepted for execution.

## Result Review

Pre-review execution summary:

- Decision:
  `filterflow_float64_row_173_official_proposal_topology_h2_state_object_topology_required`.
- Primary matching variants:
  `likelihood_particles_detached_sampling_mean_at_time_43` and
  `likelihood_particles_detached_sampling_mean_all_times`.
- Matched primary local VJP deltas for the best primary match:
  `proposal_ll_to_proposed_particles = 0.0`,
  `proposal_ll_to_sampling_proposal_mean = 0.0`,
  `proposal_ll_to_internal_likelihood_mean = 0.0`.
- Full gradient gap remains and is worse for the local topology-matching
  variant: best primary match max gap `544.9274396565979`; direct sampled
  distribution max gap `5.302734403676368`.
- Vetoes clear: scalar/proposal-likelihood value gates, resampling flags,
  finiteness, CPU-only parent, comparator drift, and path-boundary manifest.
- Helper-boundary materiality is recorded as explanatory only, not a veto.

## Round 1 Result Review

Claude status: `ACCEPT`.

- Claude finding: No findings.
- Codex classification: `ACCEPT`.
- Codex evidence: The result uses the accepted ordered decision rule, records
  `h2_state_object_topology_required`, keeps `global_gap_remaining: true` as a
  separate non-promoted fact, records CPU-only parent/subprocess controls,
  comparator fingerprints, canonical input metadata, lane-boundary status, and
  bounded non-conclusions.

Result review disposition: accepted after 1 Claude round.
