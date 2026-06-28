# Visible Stop Handoff: Fixed-Policy Promotion-Stress

Date: 2026-06-23

Status: `STOPPED_AFTER_P01_OPTIONAL_HIGH_N_PAIRED_MEAN_VETO`

Stop condition:

- P01 launched optional `N=8192,T=20`, seed `82921`, because predeclared entry
  conditions were met.
- The artifact was valid but aggregate status was `FAIL` due to
  `paired:paired_log_likelihood_mean_abs_delta`.
- Observed paired mean/max delta was `6.96771240234375`; mean threshold was
  `5.0`.

Final reached phase:

- P04 closeout.

Final status:

- `FIXED_POLICY_PROMOTION_STRESS_FAILED_OR_REPAIR_NEEDED`

Required artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p01-replicated-high-n-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p04-closeout-result-2026-06-23.md`

What was not concluded:

- no default readiness;
- no statistical ranking;
- no posterior correctness;
- no HMC readiness;
- no broad rejection of Nystrom.

Safest next action:

- Create a separate reviewed diagnostic/repair lane for the `N=8192` paired
  mean drift, or explicitly restrict the current fixed policy to lower-N
  viability without default-promotion claims.
