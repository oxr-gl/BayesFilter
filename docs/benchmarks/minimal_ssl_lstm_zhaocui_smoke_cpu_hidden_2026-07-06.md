# Minimal SSL-LSTM Zhao-Cui Smoke

- Status: `passed`
- Primary filter: `zhaocui_fixed`
- Primary role: `promotion_criterion_for_minimal_mechanics_smoke`
- Comparator role: `fixed_sgqf_and_svd_ukf_are_mechanics_comparators_only`
- Dimensions: latent `1`, hidden `1`, observation `1`, horizon `2`
- Log likelihood: `-1.3969803149874547`
- Score norm: `1.6251569331205422`
- FD max abs error: `8.616574120878795e-11`
- FD passed: `True`
- Determinism passed: `True`

## Comparator Rows

| filter | role | score finite | log likelihood | score norm |
| --- | --- | --- | --- | --- |
| fixed_sgqf | mechanics_comparator_descriptive_only | True | -1.514549865972079 | 1.735676436384646 |
| svd_ukf | mechanics_comparator_descriptive_only | True | -1.5143464314470754 | 1.7355295124178867 |

## Nonclaims

- minimal scalar mechanics smoke only
- CPU-hidden debug artifact only
- not HMC convergence evidence
- not posterior correctness evidence
- not a method ranking or superiority claim
- not source-faithful SSL-LSTM Zhao-Cui parity evidence
- not GPU/XLA production-readiness evidence
- not default-readiness evidence
- not LEDH evidence

## Artifact Paths

- Plan: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-master-program-2026-07-06.md`
- Subplan: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase1-harness-subplan-2026-07-06.md`
- Result: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase1-harness-result-2026-07-06.md`
