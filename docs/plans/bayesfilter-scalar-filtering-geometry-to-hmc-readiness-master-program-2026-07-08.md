# BayesFilter Scalar Filtering Geometry To HMC Readiness Master Program

Date: 2026-07-08
Status: `DRAFT_READY_FOR_PHASE0_REVIEW`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer if available and policy-permitted; Codex substitute review if Claude is unavailable or external review is blocked by trusted-context/private-context policy

## Objective

Turn the passed identifiable scalar SSL-LSTM complete-data oracle geometry diagnostic into a bounded HMC-readiness ladder for the scalar filtering-likelihood target.

The program is deliberately narrow. It asks whether the current TensorFlow/TFP scalar filtering-likelihood path can produce a finite local geometry, a regularized SPD mass matrix in the correct whitened coordinate system, and small HMC mechanics/smoke artifacts. It does not ask whether the sampler has converged, whether posterior inference is correct, or whether any Zhao-Cui source-faithfulness gap is closed.

## Current Evidence Anchor

The immediate predecessor artifact is:

- `docs/plans/bayesfilter-identifiable-ssl-lstm-oracle-geometry-test-result-2026-07-08.md`
- `docs/benchmarks/identifiable_ssl_lstm_oracle_geometry_cpu_hidden_2026-07-08.json`

That result passed a complete-data oracle geometry diagnostic and explicitly named the next justified action as a scalar filtering-likelihood geometry diagnostic. Its caveat is binding here: complete-data oracle geometry is easier than the filtering likelihood.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can a scalar SSL-LSTM filtering-likelihood target produce mechanically valid geometry and short HMC-readiness artifacts after the complete-data oracle geometry pass? |
| Candidate mechanism | Use the existing TensorFlow/TFP SSL-LSTM filtering score path, starting with the deterministic `svd_ukf` branch, then convert accepted local geometry into a regularized SPD HMC mass matrix in the same whitened coordinates. |
| Expected failure mode | Filtering score may be noisy, nonsmooth, nonfinite, poorly identified, or nonquadratic; geometry may be over-conditioned; mass handoff may use the wrong coordinate convention; HMC mechanics may reveal bad energy behavior. |
| Promotion criterion | Each phase writes its required structured artifact, passes hard validity checks, and preserves non-claims. The whole program can only reach `HMC_MECHANICS_READY_FOR_LONGER_VALIDATION`, not posterior correctness. |
| Promotion veto | Accepted non-SPD geometry or mass matrix, coordinate-system mismatch, nonfinite log prob/score, missing provenance, failed local tests, unsupported HMC convergence/default-readiness/scientific claims. |
| Continuation veto | Broken target implementation, invalid artifact schema, unresolved material Claude/Codex review issue, repeated nonfinite values that prevent even the planned repair phase, or a human-required boundary crossing. |
| Repair trigger | Rejected filtering geometry, mass matrix over-condition or coordinate mismatch, mechanics canary energy blow-up, short HMC nonfinite/divergence telemetry, or artifact language that promotes proxy metrics. |
| Explanatory diagnostics | Dense Hessian summaries when feasible, low-rank residuals, score norm, finite sample counts, mass eigen summaries, leapfrog count, step size, trajectory length `L * epsilon`, acceptance, runtime, ESS/R-hat for later short chains. |
| What must not be concluded | No posterior correctness, HMC convergence, sampler superiority, statistical ranking, default readiness, production readiness, public API/package readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and review gate | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase0-governance-subplan-2026-07-08.md` | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase0-governance-result-2026-07-08.md` |
| 1 | Scalar filtering-likelihood geometry target | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-subplan-2026-07-08.md` | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-result-2026-07-08.md` |
| 2 | Geometry-to-mass handoff | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase2-mass-handoff-subplan-2026-07-08.md` | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase2-mass-handoff-result-2026-07-08.md` |
| 3 | HMC mechanics canary | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase3-mechanics-canary-subplan-2026-07-08.md` | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase3-mechanics-canary-result-2026-07-08.md` |
| 4 | Short HMC smoke | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase4-short-hmc-smoke-subplan-2026-07-08.md` | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase4-short-hmc-smoke-result-2026-07-08.md` |
| 5 | Replicated scalar HMC diagnostic | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase5-replicated-scalar-hmc-subplan-2026-07-08.md` | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase5-replicated-scalar-hmc-result-2026-07-08.md` |
| 6 | Closeout and next-dimensional handoff | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase6-closeout-subplan-2026-07-08.md` | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase6-closeout-result-2026-07-08.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the scalar filtering-likelihood path be connected to geometry, mass, and small HMC mechanics artifacts without coordinate or evidence-boundary errors? |
| Scientific question | Only whether the scalar filtering-likelihood target remains mechanically viable for later HMC validation. |
| Exact baseline/comparator | Passed complete-data oracle geometry result plus existing SSL-LSTM filtering score helpers in `bayesfilter/nonlinear/ssl_lstm_sgqf_ukf_adapters.py`; no comparison against a weak or unrelated sampler is used for promotion. |
| Primary pass criterion | Each phase artifact passes its hard checks; Phase 1 accepts or honestly rejects filtering geometry; Phase 2 records a SPD regularized mass in the declared coordinate system; Phase 3/4/5 artifacts preserve HMC-readiness non-claims. |
| Veto diagnostics | Nonfinite value/score accepted, non-SPD or over-conditioned matrix accepted, mass/precision/covariance coordinate mismatch, missing artifact provenance, failed tests, unreviewed default-policy change, unsupported HMC/posterior/scientific claim. |
| Explanatory diagnostics | Residuals, condition numbers, score norms, trajectory length, acceptance, ESS/R-hat, runtime, finite sample ratios, and local optimizer status unless explicitly promoted in a phase subplan. |
| Not concluded | Posterior correctness, sampler convergence, statistical superiority, production/default readiness, GPU/XLA readiness, package/public API readiness, or source-faithful Zhao-Cui behavior. |
| Preserving artifacts | Master program, visible runbook, execution ledger, stop handoff, phase subplans/results, compact review bundles/status, benchmark JSON/Markdown/log artifacts. |

## Default And Assumption Audit

| Choice | Provenance | Classification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Start with `svd_ukf` filtering branch | Existing deterministic analytic adapter and prior benchmark usage | Hypothesis baseline | May differ from later Zhao-Cui/fixed-SGQF route | Phase 1 branch metadata and score finiteness | Pending Phase 1 |
| Four free parameters | Passed oracle diagnostic uses four identifiable parameters | Inherited diagnostic scope | Too easy or not representative | Phase 1 artifact records free names and dimension | Pending Phase 1 |
| Horizon 100-200 | Oracle used horizon 200; smaller may be needed for cheap filtering checks | Convenience range, must be fixed in subplan | Too short for identifiability or too slow for iteration | Phase 1 runtime and finite-score check | Pending Phase 1 |
| Whitened coordinates `theta = center + scale * z` | `fit_low_rank_spd_quadratic_geometry` contract | Binding coordinate convention | Mass matrix accidentally built in original coordinates | Phase 2 coordinate audit | Pending Phase 2 |
| Trajectory heuristic near `L * epsilon ~= 1.57` in whitened space | User diagnostic guidance | Hypothesis diagnostic, not a pass criterion unless Phase 3 says so | Treating a heuristic as correctness proof | Phase 3 records but does not promote | Pending Phase 3 |
| CPU-hidden diagnostics | BayesFilter policy allows debug/reference CPU-hidden runs | Debug/reference exception | Mistaken for GPU/XLA production evidence | Artifact records `CUDA_VISIBLE_DEVICES=-1` | Binding for CPU phases |
| Claude review gate max 5 rounds | User instruction | Governance constraint | Infinite repair loop or false authority transfer | Ledger records review rounds/status | Binding |

## Skeptical Plan Audit

- Wrong baseline: the baseline is the passed oracle geometry plus current filtering score path, not posterior correctness or a production sampler.
- Proxy metric risk: residuals, acceptance, ESS, R-hat, and `L * epsilon` are not promoted beyond their phase contract.
- Stop conditions: each phase must stop for invalid artifacts, unresolved review blockers, nonfinite accepted quantities, coordinate mismatch, or boundary crossings.
- Unfair comparison: no stochastic ranking claim is allowed in this program.
- Hidden assumptions: scalar/four-parameter success may not transfer to higher dimensions; this is recorded as a non-claim.
- Stale context: the plan incorporates the 2026-07-08 oracle result and previous 2026-07-06/07 HMC tuning problems.
- Environment mismatch: CPU-hidden debug runs are allowed only as reference diagnostics and must be labeled.
- Artifact adequacy: the phase artifacts answer readiness mechanics only; they do not answer scientific inference validity.

Audit result: `PASS_WITH_BOUNDARIES`. Phase 0 may proceed to review. Later phases require their dedicated subplans and fresh skeptical audits before execution.

## Review And Repair Policy

Claude may be used only as a read-only reviewer for material plan, subplan, result, and boundary gates. Claude cannot authorize human, runtime, model-file, funding, product, default-policy, or scientific-claim boundaries.

Repair loop:

1. Create or refresh the phase subplan before execution.
2. Run local prechecks and the skeptical audit.
3. For material subplans/results, send a compact review bundle to Claude through the review gate.
4. If review returns `REVISE`, patch visibly and rerun focused checks/review, up to five rounds for the same blocker.
5. If Claude is unavailable, run the required tiny-probe path through the review gate and then write a Codex substitute review only if the gate classifies Claude as unavailable or transport-blocked.
6. If the trusted-context reviewer blocks Claude review because the bundle would transfer private repository context to an external service, do not work around the block. Record the block as `CLAUDE_REVIEW_POLICY_BLOCKED` and use a fresh Codex substitute review, explicitly labeled weaker than Claude review.
7. After each phase, write the result/close record, draft or refresh the next subplan, and review the next subplan before crossing into it.

## Forbidden Claims And Actions

- Do not claim HMC convergence, posterior correctness, posterior/reference agreement, default readiness, GPU/XLA readiness, package readiness, or source-faithful Zhao-Cui behavior.
- Do not change pass/fail criteria after seeing phase results.
- Do not use a failed candidate as evidence against the entire research direction if the next phase is designed as the repair.
- Do not modify unrelated dirty worktree files.
- Do not launch detached/nested agents or overnight workers from this visible runbook.
- Do not install packages, fetch network resources, edit model files, or perform destructive git/filesystem actions without explicit human approval.
