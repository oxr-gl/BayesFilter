# BayesFilter NeuTra Real Target HMC Smoke Phase 1 Review Bundle

Date: 2026-07-06

## Role Contract

READ-ONLY REVIEW ONLY.

Codex is supervisor/executor. Claude is read-only reviewer only. Do not edit
files, run commands, launch agents, approve boundary crossings, or review the
whole repository.

## Review Scope

Primary review: review exactly these two paths:

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase1-target-authority-inventory-result-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase2-real-target-adapter-subplan-2026-07-06.md`

Use the cited paths only as provenance if needed. Do not inspect unrelated
files.

If you cannot inspect both files within the timeout, use the self-contained
summary below and judge only whether the classification and next-phase boundary
are obviously unsafe.

## Review Question

Is the Phase 1 `design_only` classification coherent and fail-closed, and is
the refreshed Phase 2 subplan a safe next step that does not authorize HMC,
GPU, training, synthetic-target promotion, or unreviewed dsge_hmc runtime
authority?

## Evidence Summary

- Prior c603 import validation loaded the frozen dense-IAF transport against
  target signature
  `8f5caae87797898bd8d4f0c795246f5103e3535e247a49e5ebf01217ece20d07`.
- Prior c603 mechanics validation used a synthetic quadratic base adapter.
- BayesFilter has `GenericSSMPosteriorAdapter`, but it requires explicit
  `prior_log_prob_and_grad` and `filter_log_likelihood_and_grad` callables.
- BayesFilter has a batch SVD sigma-point value/score kernel with a
  `tf_principal_sqrt_ukf` backend, but Phase 1 did not find the live c603
  Rotemberg model/prior wrapper in BayesFilter code.
- The dsge_hmc handoff script names the missing bridge pieces:
  `model.rotemberg_second_order_svd_bayesfilter_model_and_derivatives`,
  `tf_batched_svd_sigma_point_value_and_score_custom_gradient`, and
  `model.log_prior_value_and_score_analytical_batch`.

## Classification Rule To Review

Phase 1 classifies the current state as `design_only`.

- It is not `bridgeable_real_target_adapter` because the live BayesFilter repo
  does not contain the c603 Rotemberg prior/model/filter value-score callable.
- It is not terminal `blocked_missing_real_target_authority` because the c603
  handoff contains exact source anchors, preflight evidence, target metadata,
  and callable names needed to plan a reviewed BayesFilter port/reconstruction
  attempt.
- It is `design_only` because Phase 2 may attempt only the smallest
  source-anchored adapter-authority bridge and must stop fail-closed if that
  bridge cannot be built without invented fields or unreviewed runtime
  dependencies.

Phase 2 explicitly forbids real-target mechanics, HMC, GPU/CUDA, training,
package installation, git operations, synthetic-target promotion, and live
`dsge_hmc` runtime imports as BayesFilter authority.

## Pass/Revise Criteria

Return `VERDICT: AGREE` only if:

- `design_only` is the right fail-closed classification from the stated
  evidence;
- Phase 2 is correctly scoped as an adapter-authority bridge or blocker phase;
- no unsupported HMC, posterior, production, or scientific claim is present;
- no synthetic target is promoted to real target evidence;
- no unreviewed dsge_hmc runtime import is authorized.

Return `VERDICT: REVISE` if:

- the classification should instead be `bridgeable_real_target_adapter` or
  `blocked_missing_real_target_authority`;
- Phase 2 would permit an unsafe boundary crossing;
- any required artifact, check, stop condition, or nonclaim is missing.

End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
