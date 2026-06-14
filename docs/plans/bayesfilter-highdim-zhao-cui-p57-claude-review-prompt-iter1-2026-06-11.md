# P57 Claude Review Prompt Iteration 1

You are Claude Code Opus max-effort acting as a read-only critical reviewer.
Do not edit files.  Review the P57 planning artifacts for source-faithfulness,
logical completeness, and drift risk.

Files to review:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-source-faithful-rank-ukf-repair-master-program-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-subplan-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-subplan-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m2-fixed-ttsirt-transport-contract-subplan-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m3-proposition2-marginalization-subplan-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m4-source-kr-cdf-maps-subplan-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m5-proposal-density-retained-sampling-subplan-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m6-sequential-fixed-hmc-source-loop-subplan-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m7-source-faithful-rank-ukf-calibration-subplan-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m8-preconditioned-algorithm5-subplan-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m9-spatial-sir-validation-ladder-subplan-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m10-p30-doc-claim-reconciliation-subplan-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m11-integration-closeout-subplan-2026-06-11.md`

Context files:

- `docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-claude-review-2026-06-10.md`
- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/rank_budget.py`
- `bayesfilter/highdim/ukf_scout.py`
- author source under `third_party/audit/zhao_cui_tensor_ssm_p10/source`

Please return:

1. `VERDICT: ACCEPT` or `VERDICT: REVISE`.
2. Material blockers, ordered by severity.
3. Missing phases or wrong phase ordering.
4. Any place the plan still lets UKF/rank-budget/local-route artifacts close a
   source-faithful claim.
5. Any place proposal density, retained marginalization, KR/CDF maps,
   preconditioning, or source model parity is under-specified.
6. Whether this is a real implementation plan or only governance repair.
7. Concrete edits required for convergence.

