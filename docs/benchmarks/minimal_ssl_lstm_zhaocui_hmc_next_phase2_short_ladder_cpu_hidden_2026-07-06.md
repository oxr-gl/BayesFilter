# Minimal SSL-LSTM Zhao-Cui HMC Ladder Phase 4 Short Ladder

- Status: `passed`
- Artifact role: `short_replicated_debug_ladder`
- Filter: `zhaocui_fixed`
- All predeclared seeds passed: `True`

## Candidate Rows

| seed | status | hard vetoes | acceptance rate | nonfinite samples | sample shape |
| --- | --- | --- | --- | --- | --- |
| [20260706, 2401] | passed | none | 1.0 | 0 | [2, 24] |
| [20260706, 2402] | passed | none | 1.0 | 0 | [2, 24] |
| [20260706, 2403] | passed | none | 1.0 | 0 | [2, 24] |

## Decision Table

| field | value |
| --- | --- |
| decision | short debug ladder hard-veto classification only |
| primary_criterion_status | passed |
| veto_diagnostic_status | no hard veto for predeclared seeds |
| main_uncertainty | tiny seed ladder cannot assess convergence, posterior correctness, ranking, or default readiness |
| next_justified_action | write Phase 4 result and review Phase 5 boundary |
| what_is_not_being_concluded | No HMC convergence, posterior correctness, R-hat/ESS, ranking, GPU/XLA readiness, default readiness, source-faithful parity, or LEDH result. |

## Inference Status

| field | value |
| --- | --- |
| hard_veto_screen | passed |
| statistically_supported_ranking | not_claimed |
| descriptive_only_differences | Per-seed acceptance/runtime differences are descriptive only. |
| default_readiness | not_checked |
| next_evidence_needed | Longer reviewed sampler diagnostics before any convergence, posterior, ranking, or default-readiness claim. |

## Nonclaims

- Phase 4 short replicated debug ladder only
- CPU-hidden non-JIT debug/reference exception only
- not HMC convergence evidence
- not R-hat or ESS evidence
- not posterior correctness evidence
- not a method ranking or superiority claim
- not source-faithful SSL-LSTM Zhao-Cui parity evidence
- not GPU/XLA production-readiness evidence
- not default-readiness evidence
- not LEDH evidence

## Artifact Paths

- Plan: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-master-program-2026-07-06.md`
- Subplan: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase4-short-replicated-ladder-subplan-2026-07-06.md`
- Result: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase4-short-replicated-ladder-result-2026-07-06.md`
