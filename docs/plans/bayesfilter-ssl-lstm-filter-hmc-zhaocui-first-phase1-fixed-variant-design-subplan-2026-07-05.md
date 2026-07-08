# Phase 1 Subplan: Fixed-Variant Design And Classification Ledger

Date: 2026-07-05

Status: `DRAFT_NEXT_PHASE_AFTER_PHASE0_REVIEW`

## Phase Objective

Design the first admissible `zhaocui_fixed` SSL-LSTM route as a deterministic,
fixed-branch, analytic-score adapter candidate, and write the classification
ledger needed before implementation.

This phase must decide what Phase 2 is allowed to build. It must not write
adapter code.

## Entry Conditions Inherited From Previous Phase

- Phase 0 source-anchor governance result exists.
- Phase 0 classified the first SSL-LSTM Zhao-Cui route as a clean-room fixed
  variant, not source-faithful SSL-LSTM parity.
- The master program and visible gated runbook are active.
- LEDH remains deferred to a separate future program.
- The existing Phase 4 blocker remains true until a real `zhaocui_fixed`
  adapter is designed and implemented.
- Claude read-only review, Codex substitute review, or explicit user exception
  must clear the Phase 0/Phase 1 boundary before Phase 1 execution.

## Required Artifacts

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase1-fixed-variant-design-result-2026-07-05.md`
- A fixed-variant design ledger with:
  - state, parameter, and target-shape inheritance from the SSL-LSTM protocol;
  - every proposed branch/sample/rank/basis/schedule/randomness choice;
  - route classification for each choice as `source_faithful`,
    `fixed_hmc_adaptation`, `extension_or_invention`, or local
    SSL-LSTM implementation substrate;
  - analytic gradient design obligations;
  - finite-difference testing plan;
  - artifact schema fields and nonclaims.
- A Phase 2 implementation subplan refreshed from the Phase 1 result.
- Optional bounded Phase 1 review bundle if the design contains material
  choices beyond the Phase 0 bundle.

## Required Checks, Tests, And Reviews

- Re-open the source anchors before writing the result:
  - `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43`
  - `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:46-124`
  - `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:132-135`
  - `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:24-47`
- Re-open the local SSL-LSTM protocol and SGQF/UKF adapter scaffold.
- Verify by static inspection that the Phase 1 design does not require
  `GradientTape`, `tf.py_function`, NumPy implementation logic, adaptive
  target-path randomness, or hidden branch selection.
- Verify that SGQF/UKF are comparators and reusable local derivative substrate
  only, not promotion criteria for Zhao-Cui.
- Run document hygiene checks after writing the result and next subplan:
  `git diff --check -- <Phase 1 result and Phase 2 subplan>`.
- Run a forbidden-claims scan over the Zhao-Cui-first plan/result artifacts for
  source-faithful SSL-LSTM parity, LEDH implementation, target autodiff, and
  HMC success claims.
- Use Claude read-only review for material design claims if available; if Claude
  stalls, use the tiny-probe protocol and a fresh Codex substitute review as
  allowed by the runbook and user direction.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact fixed-variant `zhaocui_fixed` adapter design is narrow enough for Phase 2 to implement without overclaiming source-faithful parity? |
| Baseline/comparator | Phase 0 source ledger, Phase 3 SGQF/UKF adapters, Phase 2 SSL-LSTM protocol, Zhao-Cui author source anchors, and the Phase 4 blocker. |
| Primary pass criterion | A complete design ledger exists and classifies every proposed route choice; the design preserves deterministic target evaluation and an analytic first-order score obligation. |
| Veto diagnostics | Any unclassified route choice, unbounded source-faithfulness claim, hidden adaptive randomness, target-path autodiff requirement, LEDH leakage, or implementation step before design closure. |
| Explanatory diagnostics | Design residual risks, expected finite-difference checks, route mismatch notes, and artifact-schema notes. |
| Not concluded | No implementation success, HMC readiness, posterior correctness, method superiority, source-faithful parity, SGQF/UKF sufficiency, or LEDH result. |
| Result artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase1-fixed-variant-design-result-2026-07-05.md` |

## Planned Design Questions

Phase 1 must answer these questions explicitly:

1. What is the fixed target surface?
   - It must use the Phase 1/2 Gaussian additive SSL-LSTM parameterization and
     `SSLLSTMStaticConfig` shape contract.
2. What is Zhao-Cui-inspired and source anchored?
   - At minimum, weighted recentering and the fixed replay idea may be tied to
     `computeL` and `full_sol.reapprox`.
3. What is clean-room SSL-LSTM implementation?
   - SSL-LSTM transitions, observations, parameter derivatives, priors, and
     value/score wrappers are BayesFilter code, not author source.
4. What is frozen before target evaluation?
   - Seeds, reference samples, resampling quantiles, affine frames, ranks,
     basis choices, schedule lengths, tolerances, and any support/regularization
     choices must be fixed in a manifest.
5. How is the analytic gradient obtained?
   - The result must specify the manual chain rule surface and the required
     tensors for Phase 2. It may use finite differences only as tests.
6. What is the minimal implementation surface?
   - The result must identify the smallest new module/test set needed and avoid
     public API/default-policy changes.
7. What is the first failure mode to detect?
   - Non-finite value/score, branch manifest drift, analytic/finite-difference
     mismatch, or schema invalidity must block implementation promotion.

## Forbidden Claims And Actions

- Do not implement the adapter in Phase 1.
- Do not claim source-faithful SSL-LSTM Zhao-Cui parity.
- Do not claim paper-scale Zhao-Cui validity.
- Do not use or plan `GradientTape`, `tf.py_function`, or NumPy logic as the
  target score path.
- Do not bring LEDH, manual VJP streaming OT, Gibbs, Particle Gibbs,
  conditional SMC, or latent-path MCMC into this phase.
- Do not use SGQF/UKF success as a pass criterion for Zhao-Cui.
- Do not change public APIs, defaults, model files, package metadata, or
  unrelated dirty worktree files.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only when:

- Phase 1 result exists and says `PASSED` or a narrower reviewed pass token;
- every design choice is classified and anchored or explicitly labeled as
  clean-room/local substrate;
- analytic score obligations are specific enough to implement without autodiff;
- deterministic manifest fields are specified;
- finite-difference and repeatability tests are specified;
- Phase 2 subplan exists and has been reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety;
- no review blocker remains unresolved after the allowed repair loop.

## Stop Conditions

- The design cannot avoid target-path autodiff.
- The design needs an unapproved method family beyond a fixed-HMC adaptation or
  clean-room SSL-LSTM local implementation.
- Source anchors cannot support even the bounded fixed-variant inspiration
  claimed by the design.
- Phase 2 implementation would require package installation, network fetch,
  destructive action, public API/default change, or model-file edit not already
  approved.
- Claude and Codex, or Codex and substitute reviewer, do not converge after
  five rounds for the same material design blocker.

## End-Of-Phase Protocol

1. Run the required local checks.
2. Write the Phase 1 result/close record.
3. Draft or refresh the Phase 2 implementation subplan.
4. Review Phase 2 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
5. If material design claims remain, send a bounded review bundle to Claude or
   run the runbook-approved substitute review path.
