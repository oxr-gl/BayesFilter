# SSL-LSTM Phase 7 HMC Launch Smoke

- Schema: `ssl_lstm.filter_hmc.phase7_hmc_smoke.v1`
- Status: `PHASE7_LAUNCH_SMOKE_PASSED`
- Tier: `launch_smoke`
- Git commit: `f98be292faabf3d1728f876ad211a70ac1ddf98c`
- Device scope: `cpu`
- JIT compile: `False`

## Candidate Status

| filter | status | hard vetoes | target scope |
| --- | --- | --- | --- |
| fixed_sgqf | passed_launch_smoke | none | ssl_lstm_filter_hmc:fixed_sgqf:phase7_launch_smoke |
| svd_ukf | passed_launch_smoke | none | ssl_lstm_filter_hmc:svd_ukf:phase7_launch_smoke |
| zhaocui_fixed | passed_launch_smoke | none | ssl_lstm_filter_hmc:zhaocui_fixed:phase7_launch_smoke |
| ledh_streaming_ot | blocked | missing_manual_vjp_streaming_ot_score_path | None |

## Decision Table

| field | value |
| --- | --- |
| decision | launch smoke classification only |
| primary_criterion_status | launch_smoke_artifact_written |
| veto_diagnostic_status | no launch hard veto for admitted filters |
| main_uncertainty | tiny fixed-kernel smoke cannot assess convergence, R-hat/ESS, ranking, or invariant estimation quality |
| next_justified_action | write Phase 7 result and decide whether to plan a longer replicated HMC tier |
| what_is_not_being_concluded | No method superiority, no exact posterior correctness, no parameter identifiability, no production/default readiness, and no full Phase 7 replicated-evidence pass. |

## Inference Status

| field | value |
| --- | --- |
| hard_veto_screen | passed_for_admitted_launch_smoke |
| statistically_supported_ranking | not_claimed |
| descriptive_only_differences | not_interpreted |
| default_readiness | not_checked |
| next_evidence_needed | Phase 7 warmup/short-chain replicated tier with predeclared R-hat/ESS and uncertainty evidence before any ranking |

## Hard Veto Summary

| filter | vetoes |
| --- | --- |
| fixed_sgqf | none |
| svd_ukf | none |
| zhaocui_fixed | none |
| ledh_streaming_ot | missing_manual_vjp_streaming_ot_score_path |

## Nonclaims

- launch-tier HMC mechanics smoke only
- not a sampler convergence claim
- not R-hat or ESS evidence
- not posterior correctness evidence
- not filter sufficiency evidence
- not parameter-recovery evidence
- not a ranking claim
- not default-readiness evidence
- Phase 6 heldout predictive log score remains explanatory proxy only
