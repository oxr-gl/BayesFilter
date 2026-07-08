# Minimal SSL-LSTM Zhao-Cui HMC Next Phase 5 Longer GPU/XLA Ladder

- Status: `passed`
- Artifact role: `trusted_gpu_xla_longer_hard_veto_diagnostics`
- Filter: `zhaocui_fixed`
- Trusted approval recorded: `True`
- CUDA_VISIBLE_DEVICES: `0`
- GPU devices: `['/physical_device:GPU:0']`
- All predeclared seeds passed: `True`
- Native divergence statuses: `['not_exposed_by_kernel']`
- Native divergence interpretation: `native divergence status 'not_exposed_by_kernel' is telemetry unavailability, not zero divergences`

## Candidate Rows

| seed | status | hard vetoes | acceptance rate | divergence status | nonfinite samples | sample shape | runtime s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [20260706, 5101] | passed | none | 1.0 | not_exposed_by_kernel | 0 | [8, 24] | 9.56123704300262 |
| [20260706, 5102] | passed | none | 1.0 | not_exposed_by_kernel | 0 | [8, 24] | 8.645765050998307 |
| [20260706, 5103] | passed | none | 1.0 | not_exposed_by_kernel | 0 | [8, 24] | 8.664164752990473 |

## Decision Table

| field | value |
| --- | --- |
| decision | longer GPU/XLA hard-veto diagnostic only |
| primary_criterion_status | passed |
| veto_diagnostic_status | no hard veto for predeclared seeds |
| main_uncertainty | Modest fixed-kernel ladder cannot assess convergence, posterior correctness, ranking, default readiness, or production readiness. |
| next_justified_action | write Phase 5 result and close out Phase 6 |
| what_is_not_being_concluded | No HMC convergence, posterior correctness, R-hat/ESS, ranking, default readiness, production readiness, source-faithful parity, public API/package readiness, or LEDH result. |

## Inference Status

| field | value |
| --- | --- |
| hard_veto_screen | passed |
| statistically_supported_ranking | not_claimed |
| descriptive_only_differences | Acceptance, runtime, and sample summaries are descriptive only. |
| convergence | not_checked |
| default_readiness | not_checked |
| native_divergence_telemetry | not_exposed_by_kernel |
| next_evidence_needed | Longer chains, convergence diagnostics, posterior/reference checks, and uncertainty-aware replication before convergence, ranking, or readiness claims. |

## Hard Vetoes

- none

## Nonclaims

- Phase 5 longer trusted GPU/XLA hard-veto diagnostic ladder only
- not HMC convergence evidence
- not R-hat or ESS evidence
- not posterior correctness evidence
- not a method ranking or superiority claim
- not source-faithful SSL-LSTM Zhao-Cui parity evidence
- not GPU/XLA production-readiness evidence
- not default-readiness evidence
- not public API or package readiness evidence
- not LEDH evidence

## Artifact Paths

- Plan: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-program-master-2026-07-06.md`
- Subplan: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase5-longer-diagnostics-execution-subplan-2026-07-06.md`
- Result: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase5-longer-diagnostics-execution-result-2026-07-06.md`
