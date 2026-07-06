# Fixed SIR Phase 3 Forward Scalar Artifact

Status: `validated_n10000_same_target_value_admitted`

Source artifact: `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-fixed-sir-value-ladder-N10000-2026-07-03.json`
Canonical JSON artifact: `docs/plans/ledh-phase3-fixed-sir-forward-scalar-artifact-2026-07-07.json`

Target scalar: `observed_data_log_likelihood_estimator`
Reported field: `log_likelihood`
Admission status: `n10000_same_target_value_admitted`
Row id: `zhao_cui_spatial_sir_austria_j9_T20`
Theta coordinate system: `sir_log_scale_theta`
Theta values: `[0.0, 0.0, 0.0]`
Particle count: `10000`
Time steps: `20`
Batch seeds: `[81120, 81121, 81122, 81123, 81124]`

Execution note:

- CPU-hidden normalization only; no model execution or GPU evidence.

Nonclaims:
- not old no_free_theta admission
- not exact nonlinear likelihood correctness evidence
- not Zhao-Cui TT/SIRT source-faithfulness evidence
- not score admission
- not score correctness
- not HMC readiness evidence
- not posterior correctness evidence
- not runtime ranking evidence
