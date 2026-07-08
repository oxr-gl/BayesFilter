# SSL-LSTM Phase 7/8 Review Bundle

Date: 2026-07-05
Review name: `ssl-lstm-phase7-phase8-final-boundary-review`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority. This review is advisory only.

## Objective

Review the Phase 7 launch-smoke result and Phase 8 closeout for consistency,
artifact coverage, and claim-boundary safety. The review must preserve that the
program reached a launch-smoke boundary only, not a replicated HMC evidence
boundary.

## Artifacts To Inspect

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase7-hmc-evidence-ladder-subplan-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase7-hmc-evidence-ladder-result-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase7-hmc-evidence-ladder-result-2026-07-04.json`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase8-closeout-reset-boundary-subplan-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase8-closeout-reset-boundary-result-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase8-reset-memo-2026-07-04.md`
- `docs/benchmarks/benchmark_ssl_lstm_filter_hmc_phase7.py`
- `tests/test_ssl_lstm_phase7_hmc_smoke.py`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the Phase 7 launch-smoke result and Phase 8 closeout accurately preserve the runbook boundary after the admitted adapters completed tiny fixed-kernel HMC launch runs? |
| Baseline/comparator | The Phase 7 subplan, Phase 7 JSON/Markdown result, Phase 8 subplan/result, Phase 7 runner, and focused Phase 7 smoke test. |
| Primary criterion | Phase 7/8 must classify every candidate, preserve `fixed_sgqf` and `svd_ukf` as launch-smoke passed only, preserve `zhaocui_fixed` and `ledh_streaming_ot` as blocked/status-only, and avoid convergence, ranking, posterior-correctness, parameter-identifiability, GPU-readiness, or default-readiness claims. |
| Veto diagnostics | Any unsupported HMC convergence claim, ranking/superiority claim, native-divergence-as-zero-divergence claim, Phase 6 proxy metric promotion, hidden production/default-readiness claim, missing blocked-candidate status, or review/execution authority transfer. |
| Explanatory diagnostics | Acceptance rate, finite tiny-chain samples, finite initial value/score, runtime, trace availability, dirty worktree summary, and artifact index completeness. |
| Not concluded | Method superiority, exact posterior correctness, parameter identifiability, filter sufficiency, HMC convergence, R-hat/ESS validity, GPU/XLA readiness, default policy change, or source-faithful Zhao-Cui/LEDH completion. |

## Forbidden Claims

- Do not treat the launch-smoke pass as a replicated HMC evidence pass.
- Do not treat unavailable native divergence telemetry as zero divergences.
- Do not rank `fixed_sgqf` and `svd_ukf` from acceptance, runtime, or finite
  samples.
- Do not treat Phase 6 heldout predictive log score as the Phase 7 primary
  criterion.
- Do not claim Zhao-Cui fixed or LEDH streaming-OT implementation completion.
- Do not authorize future longer HMC tiers; those require a separately reviewed
  plan.

## Review Questions

1. Are the Phase 7 result claims and nonclaims consistent with the Phase 7
   subplan, JSON artifact, runner, and smoke test?
2. Does Phase 8 close the program at the correct launch-smoke boundary without
   claiming convergence, ranking, posterior correctness, source-faithfulness, or
   default readiness?
3. Are all candidates classified with the intended boundary: `fixed_sgqf` and
   `svd_ukf` launch-smoke passed only; `zhaocui_fixed` and
   `ledh_streaming_ot` blocked/status-only?
4. Is there any unsupported scientific, runtime, or authority claim that should
   be revised before final closeout?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
