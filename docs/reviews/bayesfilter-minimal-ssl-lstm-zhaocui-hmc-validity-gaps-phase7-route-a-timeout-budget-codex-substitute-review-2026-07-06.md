# Codex Substitute Review: Phase 7 Route A Timeout Budget

Date: 2026-07-06

Reviewer: Codex visible substitute review

Claude status: unavailable for this private repository lane because external
review would transmit private repository context.

Reviewed artifacts:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-frozen-step-trajectory-timeout-handoff-subplan-2026-07-06.md`
- `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py`

## Proposed Route

Use `route_a_timeout_budget`: rerun the existing public staged tuner with only
these differences from the final Phase 6 rerun:

- output artifact paths move to Phase 7 names;
- public tuning output directory moves to a Phase 7 directory;
- `public_timeout_budget_s` is increased from `90.0` seconds to `300.0`
  seconds through a narrow CLI override.

## Skeptical Audit

| Risk | Status | Note |
| --- | --- | --- |
| Wrong baseline | `PASS` | Baseline is the final Phase 6 artifact with `phase6_public_timeout_soft_deadline`. |
| Proxy promoted to promotion criterion | `PASS` | The rerun can only produce handoff/blocker evidence, not posterior validity. |
| Missing stop condition | `PASS` | Existing tuner hard vetoes remain active; timeout remains a hard veto. |
| Unfair comparison | `PASS` | This is not a comparator/ranking phase. |
| Hidden assumption | `PASS` | The only assumption is that the prior stop was budget-limited; the artifact can falsify that. |
| Environment mismatch | `PASS` | CPU-hidden diagnostic remains explicit; no GPU/XLA claim is allowed. |
| Artifact mismatch | `PASS` | Existing JSON/Markdown/public tuning artifacts answer the timeout handoff question. |
| Private mechanics exposure | `PASS` | The public artifact policy remains unchanged. |
| Unsupported source-faithful claim | `PASS` | No source-faithful work is performed. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the frozen-step trajectory stage complete when the public timeout budget is enlarged while all other reviewed target/tuning settings remain unchanged? |
| Baseline/comparator | Final Phase 6 CPU-hidden rerun with public timeout `90.0` seconds and hard veto `phase6_public_timeout_soft_deadline`. |
| Primary pass criterion | A valid structured Phase 7 artifact either reaches a non-promoting final-kernel handoff candidate or records a new precise blocker. |
| Veto diagnostics | Runtime exception, invalid artifact, nonfinite target/value/score, proxy divergence substitution, private mechanics exposure, unsupported zero-divergence claim, or unsupported correctness/readiness/ranking claim. |
| Explanatory only | Runtime, timeout fields, stage statuses, repair triggers, candidate counts, and private event count. |
| Not concluded | Zero divergences, posterior correctness, HMC convergence, ranking, superiority, readiness, source-faithful Zhao-Cui parity, dimensional generality, or LEDH evidence. |

## Verdict

`VERDICT: AGREE`

The route is consistent with the Phase 7 subplan and may be executed as a
bounded CPU-hidden diagnostic.
