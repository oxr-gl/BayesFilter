# Review Loop: Row 173 Proposal-Likelihood Wiring Probe

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

Claude status: `ACCEPT`.

- Claude finding: No findings.
- Codex classification: `ACCEPT`.
- Codex evidence: The plan has a bounded row/time scope, fixed float64
  executable FilterFlow comparator, explicit pass criterion, veto diagnostics,
  CPU-only and trusted-Claude controls, forbidden write boundaries, and clear
  non-claims. It separates local proposal-likelihood VJP reproduction from
  full row-gradient closure.
- Control added or rebuttal: No patch required.

Plan review disposition: accepted for execution.

## Result Review

### Round 1

Claude status: `REJECT`.

- Claude finding: The result overstates the plan question by saying fresh
  wiring reproduces the local official VJP in general, while the JSON only
  supports `proposal_ll_to_proposed_particles`; fresh variants still have a
  `proposal_ll_to_proposal_mean` delta of `28.749898405961705`.
- Codex classification: `ACCEPT`.
- Codex evidence: The accepted plan requires recording both
  `proposal_ll_to_proposed_particles` and `proposal_ll_to_proposal_mean` or
  fresh proposal mean. The JSON had `proposal_ll_to_proposed_particles_delta`
  equal to `0.0` for fresh variants, but the local-gradient rows showed
  `proposal_ll_to_proposal_mean` delta `28.749898405961705`, so the h2 wording
  was too broad.
- Control added or rebuttal: Patched
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_proposal_likelihood_wiring_probe_tf.py`
  so full local proposal-likelihood VJP matching requires both
  proposed-particle and proposal-mean terms. Added explicit
  `fresh_proposed_particles_vjp_matches_filterflow`,
  `fresh_proposal_mean_vjp_matches_filterflow`, and
  `fresh_full_local_vjp_matches_filterflow` fields. The classifier now maps a
  proposed-particles-only match to `blocked_or_vetoed` rather than h2/h3.

- Claude finding: The runner's comparator logic hard-coded local VJP match to
  `_proposal_ll_to_proposed_particles_delta`, narrower than the accepted plan.
- Codex classification: `ACCEPT`.
- Codex evidence: `_compare_sources` previously used only
  `_proposal_ll_to_proposed_particles_delta` for
  `fresh_local_vjp_matches_filterflow`, and `_interpret_source` used that
  value to classify h2/h3.
- Control added or rebuttal: Added `_proposal_ll_to_proposal_mean_delta` and
  revised `_interpret_source` to require both local terms before h2/h3.

- Claude finding: The review-loop artifact still said result review pending,
  so there was no recorded Codex classification or execution-gate closure.
- Codex classification: `ACCEPT`.
- Codex evidence: This section was previously `Pending.`
- Control added or rebuttal: Added this Round 1 result-review ledger with
  explicit Codex classifications and controls.

Round 1 disposition: patch required; resubmit after rerunning the result
artifact and verification checks.

### Round 2

Claude status: `REJECT`.

- Claude finding: The corrected raw evidence is consistent with
  proposed-particles VJP matching while proposal-mean VJP still differs, but
  the artifact labels this clean negative outcome as `blocked_or_vetoed`
  despite all veto controls being clear.
- Codex classification: `ACCEPT`.
- Codex evidence: The JSON has `all_vetoes_clear: true`, no comparator drift,
  finite tensors, scalar/proposal-likelihood value gates passing, and helper
  boundary not material. The plan's `blocked_or_vetoed` examples are comparator
  drift, CPU-only violation, non-finite tensors, missing reference, and other
  execution/governance blockers, not a clean scientific negative result.
- Control added or rebuttal: Patch the plan, runner, result, and report to add
  an explicit clean negative classification:
  `h5_fresh_wiring_reproduces_proposed_particles_vjp_only`. This classification
  records that fresh wiring reproduces the `proposal_ll_to_proposed_particles`
  VJP but not the full local proposal-likelihood VJP because
  `proposal_ll_to_proposal_mean` remains mismatched.

- Claude finding: The decision table's next action is misleading because
  "repair blocker or veto" is not the right next action after a clean negative
  localization.
- Codex classification: `ACCEPT`.
- Codex evidence: `_next_action` returned the generic blocker action for
  `blocked_or_vetoed`, while the evidence points to tracing the remaining
  proposal-mean/global source.
- Control added or rebuttal: Add a dedicated `_next_action` branch for
  `h5_fresh_wiring_reproduces_proposed_particles_vjp_only`.

Round 2 disposition: patch required; resubmit after rerunning the result
artifact and verification checks.

### Round 3

Claude status: `ACCEPT`.

- Claude finding: No findings. Claude accepted that the updated plan/result
  now treat the observed outcome as explicit clean negative
  `h5_fresh_wiring_reproduces_proposed_particles_vjp_only`, keep
  `all_vetoes_clear: true`, limit the claim to proposed-particles VJP
  reproduction, preserve the unresolved proposal-mean/local-VJP mismatch, and
  recommend tracing that remaining proposal-mean difference.
- Codex classification: `ACCEPT`.
- Codex evidence: The current JSON records
  `fresh_proposed_particles_vjp_matches_filterflow: true`,
  `fresh_proposal_mean_vjp_matches_filterflow: false`,
  `fresh_full_local_vjp_matches_filterflow: false`, `all_vetoes_clear: true`,
  and decision
  `filterflow_float64_row_173_proposal_likelihood_wiring_h5_fresh_wiring_reproduces_proposed_particles_vjp_only`.
- Control added or rebuttal: No patch required.

Result review disposition: accepted after 3 Claude rounds.
