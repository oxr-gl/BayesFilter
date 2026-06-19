# P8i Master Program: P8h Remaining Gap Closure

Date: 2026-06-16

Status: `PHASE8_CLOSEOUT_READY`

## Scope

P8i is the gated follow-on to the closed P8h OT-resampled Algorithm 1 LEDH
repair. P8h established a documented, GPU-capable, gradient-bearing
short-prefix route and a Tier-0 fixed-kernel HMC execution smoke only. P8i
addresses the remaining limitations without retroactively widening P8h.

Active route inherited from P8h:

`Li-Coates Algorithm 1 UKF LEDH + PF-PF correction + Corenflos-style relaxed Sinkhorn OT resampling + same-transport barycentric covariance carry`

Exact inherited identifiers:

- row alias: `actual_sv`;
- row ID: `zhao_cui_sv_actual_nongaussian_T1000`;
- algorithm ID: `ledh_pfpf_alg1_ukf_current`;
- route variant: `p8h_sv_scalar_graph_ot_resampled_alg1`;
- resampling route: `ot_sinkhorn_barycentric_covariance_carry`;
- coordinate: `canonical_unconstrained`;
- trusted GPU provenance:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md`.

Zhao-Cui high-dimensional fixed-branch work and the broader monograph rewrite
remain out of scope.

## Remaining Gaps

P8i tracks these P8h nonclaims as explicit gaps:

1. full-horizon or longer-prefix particle-count adequacy;
2. longer-horizon OT gradient stability and gradient-scope classification;
3. GPU scaling evidence beyond horizons `4,8`;
4. HMC diagnostic tiers beyond Tier-0 fixed-kernel execution;
5. NUTS readiness;
6. stochastic PF marginal-gradient interpretation;
7. exact nonlinear likelihood boundary and reference tieout;
8. generic high-dimensional LEDH readiness;
9. filter ranking and default sampler policy boundaries.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the P8h route be advanced from short-prefix/Tier-0 feasibility toward longer-horizon filtering and sampler diagnostics without overclaiming scientific or production readiness? |
| Baseline/comparator | Closed P8h Phase 10/11 boundary, P8h Phase 5 Stage 0 tuning, P8h Phase 6 OT-gradient check, P8h Phase 7 GPU profile, and P8h Phase 8 Tier-0 HMC smoke. |
| Primary pass criterion | Each P8i phase either passes its declared gate with artifacts and review, or writes a blocker preserving exact claim boundaries and next handoff. |
| Veto diagnostics | Using P8h Stage 0 `N=5` as full-horizon adequacy; treating AD through relaxed OT as the exact stochastic PF marginal score without a reviewed derivation/estimator contract; claiming posterior convergence or production HMC from short chains; claiming NUTS readiness before HMC tier gates; ranking filters before comparable value/gradient/evidence gates; GPU results outside trusted context; Claude used as execution authority. |
| Explanatory diagnostics | ESS, MC standard error, adjacent-rung stability, transport residuals, runtime, device placement, finite values/gradients, finite-difference residuals, acceptance rate, divergences, ESS/sec, R-hat when available. |
| Not concluded | Production HMC readiness, posterior convergence, valid tuning, NUTS readiness, stochastic PF marginal-gradient correctness, exact nonlinear likelihood correctness, generic high-dimensional LEDH readiness, filter ranking, or default sampler policy unless a later named phase explicitly passes its higher evidence gate. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
|---|---|---|---|
| 0 | Governance and gap ledger | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase0-governance-gap-ledger-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase0-governance-gap-ledger-result-2026-06-16.md` |
| 1 | Longer-prefix particle and value ladder | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-result-2026-06-16.md` |
| 2 | Longer-horizon OT gradient ladder | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-longer-horizon-gradient-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-longer-horizon-gradient-result-2026-06-16.md` |
| 3 | GPU scaling profile | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-result-2026-06-16.md` |
| 4 | HMC Tier-1 and Tier-2 diagnostics | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-tier2-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-tier2-result-2026-06-16.md` |
| 5 | NUTS readiness decision | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase5-nuts-readiness-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase5-nuts-readiness-result-2026-06-16.md` |
| 6 | Stochastic-gradient and likelihood boundary | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase6-gradient-likelihood-boundary-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase6-gradient-likelihood-boundary-result-2026-06-16.md` |
| 7 | Scope, ranking, and default-policy decision | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase7-ranking-policy-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase7-ranking-policy-result-2026-06-16.md` |
| 8 | Closeout, artifact index, and repo boundary | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase8-closeout-boundary-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase8-closeout-boundary-result-2026-06-16.md` |

## Review And Repair Protocol

At the end of each phase:

1. run the phase-required local checks;
2. write the phase result or blocker result;
3. draft or refresh the next phase subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

Claude Opus/max effort may be used only as a read-only reviewer for material
plans, subplans, implementation diffs, and results. Claude is not an execution
authority and cannot authorize crossing human, runtime, model-file, funding,
product-capability, GPU, or scientific-claim boundaries.

If review finds a fixable issue, patch the same subplan visibly and rerun
focused checks. Loop Claude review only for material issues, stopping after
five rounds for the same blocker. If Claude does not respond, probe with a
small prompt; if the probe works, redesign the review prompt.

## Global Stop Conditions

- A phase would require package installation, network fetch, credential, or
  destructive filesystem/git action not already approved.
- A GPU/CUDA/TensorFlow GPU command would run without trusted escalation.
- Claude/Codex review fails to converge after five rounds for the same blocker.
- A result would need changed pass/fail criteria after seeing outcomes.
- A phase would mutate unrelated dirty Zhao-Cui, monograph, or user work.
- A phase would claim production HMC readiness, NUTS readiness, stochastic PF
  marginal-gradient correctness, exact likelihood correctness, final ranking,
  or default policy before its declared evidence gate passes.
- Runtime projection from a smaller gate shows that the next longer run would
  exceed the declared budget; write a blocker instead of forcing the run.
