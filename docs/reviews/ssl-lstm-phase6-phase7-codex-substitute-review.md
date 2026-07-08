# Codex Read-Only Substitute Review

Date: 2026-07-04
Review name: `ssl-lstm-phase6-phase7-codex-substitute-review`
Supervisor/executor: Codex
Reviewer: Codex read-only substitute reviewer

## Role Boundary

Codex must not edit files, run mutating commands, launch agents, or approve
boundary crossings.

This review is the user-authorized fallback for the Phase 6/7 bounded bundle
after the Claude review gate did not return a material verdict.

## Objective

Review whether the Phase 6 result and refreshed Phase 7 subplan are internally
consistent, boundary-safe, and correctly handed off.

## Artifacts Inspected

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase6-benchmark-runner-invariant-metrics-result-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase7-hmc-evidence-ladder-subplan-2026-07-04.md`
- `docs/benchmarks/ssl_lstm_filter_hmc_phase6_shared_benchmark_cpu_hidden_2026-07-04.json`
- `docs/benchmarks/ssl_lstm_filter_hmc_phase6_shared_benchmark_cpu_hidden_2026-07-04.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the Phase 6 result claims and the refreshed Phase 7 subplan consistent with the smoke artifact and local checks? |
| Baseline/comparator | The Phase 6 smoke artifact, local compile/tests, and the existing Phase 7 boundary rules. |
| Primary criterion | Phase 6 stays benchmark-only, the proxy metric remains non-primary, blocked rows stay status-only, and Phase 7 does not claim HMC evidence from Phase 6. |
| Veto diagnostics | Any unsupported ranking claim, hidden HMC claim, missing provenance, or Phase 7 handoff drift. |
| Explanatory diagnostics | Artifact paths, metric-role labels, smoke run status, and refresh text. |
| Not concluded | No HMC convergence, no method superiority, no default readiness, no parameter-identifiability claim. |

## Review Findings

- The Phase 6 result is consistent with the smoke artifact: admitted filters are
  `fixed_sgqf` and `svd_ukf`, blocked filters remain status-only, and
  `parameter_matching_primary_criterion` is `false`.
- `heldout_predictive_log_score` is explicitly carried as a filter-likelihood
  proxy and is not promoted to a ranking claim.
- Target-scope provenance is recorded for admitted and blocked filters, which
  satisfies the Phase 6 provenance requirement.
- The refreshed Phase 7 subplan keeps the Phase 6 smoke artifact in the
  benchmark-only lane and does not treat it as HMC evidence.
- No unsupported scientific, runtime, or boundary claim was found in the
  reviewed bundle.

## Verdict

VERDICT: AGREE
