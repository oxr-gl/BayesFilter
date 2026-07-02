# Phase 2 Subplan: Contract E LGSSM value gate

Date: 2026-06-28

Status: `PHASE2_HANDOFF_REVIEW_AGREE_READY_TO_EXECUTE`

## Phase Objective

Test whether a Contract E reset arm both reduces the LGSSM value gap relative
to the old barycentric reset and matches exact Kalman value within stated Monte
Carlo uncertainty on 1d and 2d T=10 fixtures.

## Entry Conditions Inherited From Previous Phase

- Phase 1 moment algebra and conditioning gates have passed, either directly or
  after reviewed same-phase repair and focused rerun.
- Phase 1 result close review has returned `VERDICT: AGREE`, and Phase 1 is
  recorded as `PHASE1_PASSED` in
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-result-2026-06-28.md`.
  The close-review provenance is recorded in
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-claude-review-ledger-2026-06-28.md`
  under "Phase 1 Result Close Review Round 5".
- This Phase 2 handoff subplan must receive a separate bounded review
  `VERDICT: AGREE` before Phase 2 execution starts.
- Contract E diagnostic parameters \(\rho,\tau\), spectral floor policy, and
  condition-number thresholds are recorded.
- Frozen LGSSM fixture:
  `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py` with \(T=10\),
  state dimensions \(1\) and \(2\), \(\theta=(0.72,\log 0.22,\log 0.30)\),
  initial covariance \(0.7I\), and the deterministic observation function
  `_observations`.
- Frozen seed schedule: `SEED_COUNT=10`, seed indices `9100..9109`,
  initial particle stateless seeds `[seed, 17]`, and transition-noise stateless
  seeds `[seed, 29]`, exactly matching `_stateless_seeded_normals_batch`.
- Frozen value scalar: the transition-first LGSSM log marginal likelihood
  accumulator used by the current manual harness,
  `log_likelihood = sum_t incremental_t`, where each `incremental_t` is the
  log normalizer returned by `core_ledh._normalize_log_weights` after the LEDH
  proposal correction at time \(t\).  The exact Kalman comparator is the FP64
  value returned by `tf_batched_kalman_value_and_score` through
  `_kalman_value_and_score` for the same observation convention.

## Required Artifacts

- LGSSM reset diagnostic script:
  `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py`
  This exact file is the first implementation artifact to create during Phase
  2 execution; it is not expected to exist before the Phase 2 handoff subplan
  has passed review.
- JSON LGSSM value diagnostic:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-2026-06-28.json`
- Markdown LGSSM value diagnostic:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-2026-06-28.md`
- Phase 2 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-result-2026-06-28.md`
- Refreshed Phase 3 LGSSM gradient subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-subplan-2026-06-28.md`

## Required Checks, Tests, And Reviews

- Compile/check changed diagnostic files.
- Run a tiny CPU-hidden wiring smoke.
- Run the material LGSSM value diagnostic in trusted GPU/XLA context if it
  claims GPU evidence.
- Bounded Claude review of the Phase 2 result and refreshed Phase 3 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does Contract E restore enough second-moment behavior that LGSSM value comparisons to exact Kalman become meaningful? |
| Baseline/comparator | Exact Kalman value; no-OT weighted LEDH arm; old barycentric OT reset.  A diagnostic affine-restored barycentric arm is explanatory only and may not be used as a pass/fail comparator. |
| Primary pass criterion | For 1d and 2d T=10 fixtures, Contract E mean value is within two reported MC standard errors of exact Kalman, and Contract E absolute Kalman-value error is smaller than the old barycentric OT reset absolute error on each fixture. |
| Veto diagnostics | Nonfinite value, missing MCSE, hidden CPU-as-GPU evidence, wrong reset arm, failed covariance restoration, missing seed list, or old barycentric route accidentally labeled Contract E. |
| Explanatory diagnostics | Runtime, Sinkhorn residuals, covariance trace ratios, condition spectra, per-seed values, no-OT and old-OT deltas. |
| Not concluded | No gradient correctness, no SIR/SV correctness, no production readiness. |
| Artifact | LGSSM value JSON/Markdown plus Phase 2 result. |

## Frozen Phase 2 Execution Contract

- Particles: start with a smoke-size CPU-hidden wiring check, then run the
  material diagnostic with the predeclared particle count below.  If Phase 2
  uses GPU/XLA evidence, it must run under trusted GPU-visible execution.
- Frozen particle ladder:
  - CPU-hidden wiring smoke: `N=64`, `state_dims=[1]`, `settings=[0.5:8]`,
    explanatory only, not promotion evidence;
  - material value gate: `N=1000`, `seed_count=10`, `state_dims=[1,2]`,
    `T=10`, `settings=[0.5:20]`, GPU-visible XLA/TF32 if GPU evidence is
    claimed.
- Reset arms: `ledh_no_ot`, `old_barycentric_ot`, and `contract_e`.  Any
  affine-restored barycentric diagnostic arm is explanatory only and cannot
  satisfy the primary criterion.
- Seed schedule, scalar, exact Kalman comparator, state dimensions, \(T\), and
  old-barycentric route are frozen before results are inspected.  The material
  particle count is frozen at `N=1000` and must not be changed after seeing
  Phase 2 values or MCSE.

## Skeptical Audit And Pre-Mortem

Outcome before execution: `pending_final_handoff_review`.

Known ways the Phase 2 run could mislead us:

- It could pass exact-Kalman agreement because MCSE is large rather than
  because Contract E fixes the reset.  Therefore the primary criterion also
  requires smaller absolute Kalman-value error than old barycentric OT on each
  fixture.
- It could compare different scalars across arms.  Therefore all arms must use
  the frozen transition-first log marginal likelihood accumulator above.
- It could silently tune the particle count, seed schedule, Sinkhorn setting,
  or old-OT baseline after seeing values.  Therefore `N=1000`, seeds
  `9100..9109`, `settings=[0.5:20]`, and comparator arms are frozen before
  execution.
- It could treat a CPU fallback as GPU/XLA evidence.  Therefore any GPU claim
  requires trusted GPU-visible execution; CPU-hidden smoke is wiring-only.
- It could pass value gates while hiding covariance damage.  Therefore failed
  covariance restoration or conditioning diagnostics veto the phase.

Audit conclusion: after this subplan receives bounded `VERDICT: AGREE`, the
Phase 2 evidence contract is sufficiently pinned for execution.  Before that
review passes, Phase 2 must not start.

## Forbidden Claims And Actions

- Do not claim Contract E is generally correct from LGSSM value matching.
- Do not compare SIR/SV to Kalman.
- Do not use `transport_ad_mode=full`.
- Do not run a Python loop inside any XLA-critical implementation path; use
  `tf.while_loop` for compiled loops.
- Do not repair Phase 2 by changing the exact Kalman scalar, seed schedule,
  pass/fail thresholds, comparator set, or old-OT baseline after seeing
  results.  Any such change requires stopping and writing a new reviewed
  blocker/replan artifact.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- Phase 2 result records exact commands, seeds, device status, and MCSE;
- old-OT and Contract E arms are distinguishable in artifacts;
- Contract E passes the Phase 2 primary value gate, or a reviewed repair closes
  Phase 2 as passed after focused reruns;
- the gradient subplan names the exact same scalar and comparator.

If Contract E fails the primary value gate and is not repaired inside Phase 2,
write a blocker result and stop rather than advancing to Phase 3.

## Stop Conditions

Stop if Contract E fails value gates with covariance residual or conditioning
vetoes, if the exact-Kalman comparison misses and cannot be repaired inside
Phase 2, if GPU/XLA access is unavailable for a GPU claim, or if the scalar
cannot be made identical between value and planned gradient routes.

## End-Of-Phase Protocol

Run local checks, write the result, refresh Phase 3, review Phase 3, and repair
bounded review findings before advancing.
