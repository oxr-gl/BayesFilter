# P8h Master Program: OT-Resampled Algorithm 1 LEDH Repair

Date: 2026-06-15

Status: `CLOSED_PHASE10_BOUNDARY_REVIEWED`

## Scope

This program supersedes the P8g no-resampling-centered execution path for the
serious DPF/LEDH value, gradient, GPU, and HMC-diagnostic lane. Zhao-Cui and
monograph rewrite work are out of scope.

Phase 1 governance reset records the route roles as follows: P8g
no-resampling/fixed-randomness artifacts are historical graph, kernel,
shape, and gradient-plumbing diagnostics only; classical categorical
resampling is an ESS/debug comparator and not a pathwise-gradient route; the
active serious candidate is the OT-resampled Algorithm 1 route below, pending
future design, implementation, value, gradient, GPU, and HMC gates.

The intended serious route is:

`Li-Coates Algorithm 1 UKF LEDH + PF-PF correction + Corenflos differentiable OT/Sinkhorn or annealed-transport resampling on trusted GPU`.

The per-particle covariance lifecycle is part of Li-Coates Algorithm 1. The
BayesFilter integration task is to specify and test OT auxiliary-state carry for
Algorithm 1 covariances, because Corenflos transports particles/weights but does
not by itself define how extra UKF covariance state is carried through the
transport map.

## Existing Evidence Consumed

- P8g G0 trusted GPU probe passed and was reviewed.
- P8g G2b scalar-SV graph no-resampling route passed finite/parity/speed smoke
  checks, but it is demoted here to graph/kernel sanity evidence only.
- P8g G3 fixed-randomness no-resampling gradient evidence remains diagnostic
  only and is not the serious DPF gradient route.
- P8g G4 particle tuning produced a reviewed relative-ESS blocker for the
  no-resampling scalar-SV route.
- Historical LEDH-PFPF-OT/Sinkhorn/annealed-transport tests are historical
  scaffolding. They motivate the repair but do not by themselves close the
  Algorithm 1 covariance-state integration gap.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can BayesFilter replace the no-resampling P8g serious route with a documented, GPU-capable, gradient-bearing Corenflos OT-resampled Algorithm 1 LEDH route? |
| Baseline/comparator | P8g no-resampling scalar-SV graph artifacts, historical LEDH-PFPF-OT/Sinkhorn tests, current Algorithm 1 UKF covariance lifecycle implementation, and Corenflos-style OT resampling components. |
| Primary pass criterion | Every phase either passes its declared gate with artifacts and review, or writes a blocker result preserving claim boundaries and handoff state. |
| Veto diagnostics | Treating no-resampling as the serious route; calling OT auxiliary-state carry a new filter claim; claiming stochastic categorical-resampling gradients; missing covariance carry diagnostics; GPU results outside trusted context; HMC readiness before value and gradient gates pass; Claude used as execution authority. |
| Explanatory diagnostics | ESS, MC SE, runtime, transport residuals, finite-difference deltas, gradient norms, CPU/GPU comparisons, HMC smoke diagnostics. |
| Not concluded | Production readiness, stochastic PF marginal-score correctness, exact nonlinear likelihood correctness, categorical-resampling gradient correctness, generic high-dimensional LEDH readiness, or final filter ranking. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
|---|---|---|---|
| 0 | LaTeX documentation and governance correction | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase0-latex-governance-correction-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase0-latex-governance-correction-result-2026-06-15.md` |
| 1 | Governance reset | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase1-governance-reset-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase1-governance-reset-result-2026-06-15.md` |
| 2 | Algorithm and evidence contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase2-algorithm-design-contract-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase2-algorithm-design-contract-result-2026-06-15.md` |
| 3 | Scalar-SV GPU OT implementation | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase3-scalar-sv-gpu-ot-implementation-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase3-scalar-sv-gpu-ot-implementation-result-2026-06-15.md` |
| 4 | Local checks and integration diagnostics | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase4-local-checks-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase4-local-checks-result-2026-06-15.md` |
| 5 | Value/filtering tuning | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-result-2026-06-15.md` |
| 6 | OT gradient checks | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-result-2026-06-16.md` |
| 7 | GPU performance and scaling | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-result-2026-06-16.md` |
| 8 | Tier-0 HMC execution smoke | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-diagnostic-tiers-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-tier0-smoke-result-2026-06-16.md` |
| 9 | Closeout and artifact refresh | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase9-closeout-artifact-refresh-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase9-closeout-artifact-refresh-result-2026-06-16.md` |
| 10 | Repo hygiene and commit-boundary review | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase10-repo-hygiene-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase10-repo-hygiene-result-2026-06-16.md` |
| 11 | Closure status sync | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase11-closure-sync-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase11-closure-sync-result-2026-06-16.md` |

## Terminal State

P8h is closed through Phase 10 with reviewed repo-hygiene and commit-boundary
evidence. Phase 11 is a status-sync-only gate that may refresh stale top-level
handoff fields; it does not add numerical, GPU, HMC, tuning, or scientific
evidence. No commit or push was performed.

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

- Any phase requires a package install, network fetch, credential, or destructive
  filesystem/git action not already approved.
- A GPU/CUDA/TensorFlow GPU command would run without trusted escalation.
- Claude/Codex review fails to converge after five rounds for the same blocker.
- A result would need changed pass/fail criteria after seeing outcomes.
- A phase would mutate unrelated dirty user work.
- Commit or push scope cannot be isolated from unrelated Zhao-Cui, monograph,
  or user worktree changes.
- A result tries to claim HMC readiness, stochastic PF marginal-gradient
  correctness, or final filter ranking before the declared gates pass.
