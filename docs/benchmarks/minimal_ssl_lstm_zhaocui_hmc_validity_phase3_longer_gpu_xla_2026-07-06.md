# Minimal SSL-LSTM Zhao-Cui HMC Validity Phase 3 Longer Diagnostic

- Status: `passed`
- Promotion screen: `failed`
- Artifact role: `longer_hmc_convergence_reference_diagnostic`
- Filter: `zhaocui_fixed`
- CUDA_VISIBLE_DEVICES: `0`
- GPU devices: `['/physical_device:GPU:0']`
- XLA/JIT: `True` / `True`
- Chain count: `4`
- Draws per chain: `64`
- Burn-in per chain: `32`
- HMC error: `None`
- Not-run reason: `None`
- Sample shape: `[64, 4, 24]`
- Samples all finite: `True`

## Promotion Screen

- R-hat passed: `False`
- R-hat max: `2083851.3177999416`
- ESS passed: `False`
- ESS min: `4.000003545362901`
- Reference check passed: `True`
- Reference max abs error: `4.440892098500626e-16`
- Reference max rel error: `3.210361025909055e-16`
- Continuation vetoes: `[]`
- Promotion vetoes: `['split_rhat_threshold_failed', 'ess_threshold_failed', 'native_divergence_telemetry_not_exposed']`

## Inference Status

| field | value |
| --- | --- |
| artifact_validity | passed |
| minimal_sampler_promotion_screen | failed |
| hard_veto_screen | no continuation veto |
| statistically_supported_ranking | not_claimed |
| descriptive_only_differences | Acceptance, runtime, trace summaries, and sample summaries are descriptive only. |
| default_readiness | not_checked |
| posterior_correctness | not_established |
| next_evidence_needed | Native divergence telemetry investigation and tuning/mass diagnostics before any broader convergence or readiness claim. |

## Decision Table

| field | value |
| --- | --- |
| decision | valid_artifact_continue_to_phase4 |
| primary_criterion_status | passed |
| veto_diagnostic_status | promotion vetoes: split_rhat_threshold_failed, ess_threshold_failed, native_divergence_telemetry_not_exposed |
| main_uncertainty | This is a modest fixed-kernel diagnostic on a minimal target; it does not establish full posterior correctness or broad HMC convergence. |
| next_justified_action | write Phase 3 result and refresh Phase 4 divergence telemetry subplan |
| what_is_not_being_concluded | No full posterior correctness, broad HMC convergence, ranking, default readiness, production readiness, source-faithful parity, public API/package readiness, or LEDH result. |

## Native Divergence

- Divergence status: `not_exposed_by_kernel`
- Divergence count: `None`
- Interpretation: `native divergence status 'not_exposed_by_kernel' is telemetry unavailability, not zero divergences`

## Nonclaims

- Phase 3 modest longer HMC diagnostic only
- minimal scalar-dimension zhaocui_fixed target only
- not full posterior correctness evidence
- not broad HMC convergence evidence
- not a method ranking or superiority claim
- not source-faithful SSL-LSTM Zhao-Cui parity evidence
- not GPU/XLA production-readiness evidence
- not default-readiness evidence
- not public API or package readiness evidence
- not LEDH evidence

## Artifact Paths

- Plan: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-master-program-2026-07-06.md`
- Subplan: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-longer-hmc-diagnostics-subplan-2026-07-06.md`
- Result: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-longer-hmc-diagnostics-result-2026-07-06.md`
