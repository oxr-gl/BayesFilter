# BayesFilter SSL-LSTM Filter-HMC Master Program

Date: 2026-07-04

Status: `PHASE0_DRAFT_UNDER_REVIEW`

## Objective

Build and test whether HMC over parameters can estimate a Gaussian additive
state-space LSTM target using BayesFilter filtering algorithms as differentiable
value/score engines. The target is the filter-induced posterior
`log p(theta | y) = log p(theta) + log L_filter(theta)` for a declared filter,
not Particle Gibbs, conditional SMC, or latent-path MCMC.

The user-provided literature source is arXiv:1711.11179. This master program
does not yet claim a checked equation-level implementation of that paper.
Phase 1 must inspect the technical model and inference sections before code is
written.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can HMC using analytic or manual-VJP filter scores estimate a Gaussian additive SSL-LSTM in invariant predictive and latent-state terms? |
| Mechanism under test | Fixed SGQF, UKF, fixed-variant Zhao-Cui, and LEDH streaming-OT manual VJP adapters feeding a shared HMC posterior contract. |
| Estimand | Posterior over SSL-LSTM parameters under each declared filter likelihood, plus posterior predictive and decoded latent-state functionals. |
| Non-identifiability handling | Do not use parameter-by-parameter matching as the primary criterion. Use invariant metrics: heldout predictive log score, decoded trajectory RMSE after alignment, posterior predictive calibration, and HMC diagnostics. |
| Baseline/comparator | Shared synthetic SSL-LSTM fixtures; affine-Gaussian reference fixtures only for implementation sanity; same HMC runtime and metric harness across all filter adapters. |
| Expected failure modes | Non-identifiability, non-finite filter values, wrong gradients, broken fixed-branch assumptions, poor HMC geometry, LEDH transport VJP mismatch, Zhao-Cui source-anchor gaps, and insufficient uncertainty evidence for rankings. |
| Promotion criterion | A candidate adapter remains viable only if value/score checks, fixed-shape contract checks, HMC mechanics, and invariant estimation metrics all pass the declared gates. |
| Promotion veto | Non-finite value/score, failed finite-difference score check beyond tolerance, failed adapter contract, HMC divergences beyond the declared veto, invalid benchmark artifact, or unsupported source/gradient claim. |
| Continuation veto | Missing required source inspection, inability to build deterministic fixed score path, unavailable manual VJP route for LEDH after planned repairs, corrupted artifacts, or a boundary requiring human approval. |
| Repair trigger | A veto that is localized to implementation, tuning, fixture scale, or artifact schema triggers the next planned repair phase rather than rejection of the research direction. |
| What must not be concluded | No exact SSL posterior claim, no parameter identifiability claim, no claim that SGQF/UKF are sufficient before the shared benchmark, no method ranking without uncertainty evidence, no Zhao-Cui author-faithfulness claim without paper and author-source anchors. |

## Global Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific question | Whether filter-HMC can estimate SSL-LSTM targets in invariant terms under a Gaussian additive noise model. |
| Exact baseline/comparator | The comparator is the same SSL-LSTM synthetic data, prior, HMC runtime, and invariant metric suite across candidate filters; affine-Gaussian Kalman sanity fixtures are implementation checks only. |
| Primary pass/fail criterion | The full program passes only if at least one candidate has valid fixed value/score evidence, HMC mechanics without veto, and invariant estimation metrics meeting predeclared thresholds on replicated fixtures. |
| Veto diagnostics | Non-finite values/gradients, gradient check failure, shape/signature mismatch, HMC divergence/R-hat/ESS veto, invalid source-anchor claim, invalid LEDH VJP evidence, missing artifacts, or changed criteria after seeing results. |
| Explanatory diagnostics | Runtime, acceptance rate inside non-veto ranges, descriptive metric differences, posterior summaries, mass-matrix conditioning, transport iteration counts, and local score-error histograms. |
| Not concluded | Statistical superiority, default readiness, exact likelihood correctness, parameter recovery, broad SSL-LSTM generalization, production API readiness, or Zhao-Cui source-faithfulness unless later artifacts specifically prove those claims. |
| Preserved artifacts | Phase subplans and results under `docs/plans`, structured JSON/Markdown benchmark artifacts under reviewed paths, Claude review logs under `.claude_reviews`, and final reset memo. |

## Skeptical Plan Audit

The initial audit passes for Phase 0 only because no scientific run or code
change is launched yet. The material risks are explicitly deferred into gates:

- Wrong baseline: the plan forbids comparing only against a weak baseline and
  requires a shared harness across candidates.
- Proxy promotion: smoke tests and finite-difference checks can admit a lane but
  cannot prove estimation success.
- Missing stop conditions: every phase subplan has stop conditions and handoff
  gates.
- Unfair comparison: Phase 6 must lock shared data, prior, HMC runtime, seeds,
  metrics, and compute budget before metrics are interpreted.
- Hidden assumptions: Gaussian additive noise, fixed shapes, fixed filter
  randomness, and analytic/manual gradients are made explicit.
- Stale context: Phase 1 must inspect the paper and current local code before
  implementation.
- Environment mismatch: GPU/XLA is the production target, but CPU-only small
  checks are allowed only as debug/reference exceptions and must be labeled.
- Artifact mismatch: every phase must name the result file that answers its
  question before commands run.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Planning, governance, and review launch | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase0-planning-governance-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase0-planning-review-result-2026-07-04.md` |
| 1 | SSL-LSTM model, parameterization, and estimand | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase1-ssl-model-estimand-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase1-ssl-model-estimand-result-2026-07-04.md` |
| 2 | Shared value/score protocol and diagnostics | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase2-value-score-protocol-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase2-value-score-protocol-result-2026-07-04.md` |
| 3 | Fixed SGQF and UKF analytic adapters | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase3-sgqf-ukf-analytic-adapters-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase3-sgqf-ukf-analytic-adapters-result-2026-07-04.md` |
| 4 | Zhao-Cui fixed analytic adapter | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase4-zhaocui-fixed-analytic-adapter-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase4-zhaocui-fixed-analytic-adapter-result-2026-07-04.md` |
| 5 | LEDH streaming-OT manual VJP adapter | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase5-ledh-streaming-ot-manual-vjp-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase5-ledh-streaming-ot-manual-vjp-result-2026-07-04.md` |
| 6 | Shared benchmark runner and invariant metrics | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase6-benchmark-runner-invariant-metrics-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase6-benchmark-runner-invariant-metrics-result-2026-07-04.md` |
| 7 | HMC mechanics and evidence ladder | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase7-hmc-evidence-ladder-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase7-hmc-evidence-ladder-result-2026-07-04.md` |
| 8 | Closeout, reset memo, and boundary decision | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase8-closeout-reset-boundary-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase8-closeout-reset-boundary-result-2026-07-04.md` |

## Global Repair Loop

1. Codex is supervisor and executor.
2. Claude is read-only reviewer only.
3. For a material blocker, Codex writes a focused blocker note or patches the
   same subplan visibly.
4. Codex runs the narrow local checks needed for the repair.
5. Codex sends only a bounded review bundle or path-limited prompt to Claude.
   If Claude fails to return a material verdict, Codex performs a separate
   local read-only substitute review on the same bounded bundle and records the
   fallback in the review ledger before any phase advance.
6. If Claude returns `VERDICT: REVISE`, or if the Codex substitute review
   finds a material issue, Codex classifies each finding as material, already
   covered, out of scope, or human-boundary.
7. For the same blocker, loop at most five Claude review rounds; the Codex
   substitute review is a fallback, not an extra Claude round.
8. If the blocker converges, continue to the next phase. If it does not
   converge after five rounds or the substitute review still finds a blocker,
   write the stop handoff and ask for direction.

## Anticipated Approvals

- Immediate approval: run the Claude review gate through
  `bash /home/ubuntu/python/claudecodex/scripts/claude_review_gate.sh` with
  model `opus` and effort `max`, read-only.
- Fallback approval: if Claude fails to return a material verdict, run a
  separate Codex read-only substitute review on the same bounded bundle; do
  not widen scope or treat the fallback as execution authority.
- Future approval if not already covered by local rules: GPU/XLA HMC benchmark
  wrappers once Phase 6/7 creates or identifies stable commands.
- Future human approval: any network fetch, package install, model-file edit,
  default-policy change, public API change, destructive git/filesystem action,
  or scientific/default-readiness claim outside the reviewed evidence contract.

## Current Boundaries

- Do not implement Particle Gibbs, conditional SMC, or Gibbs as an alternative
  inference route.
- Do not use automatic differentiation as the target gradient path for the
  requested adapters. Finite differences may be used only as independent checks.
- Do not use existing LEDH GradientTape score helpers as final target evidence;
  Phase 5 must build or verify the manual VJP streaming-OT path.
- Do not let SGQF or UKF skip the same benchmark that tests Zhao-Cui and LEDH.
- Do not touch unrelated dirty worktree changes.
