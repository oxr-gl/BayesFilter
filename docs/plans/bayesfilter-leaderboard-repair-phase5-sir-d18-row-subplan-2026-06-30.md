# Phase 5 subplan: spatial SIR d18 parameterized observed-data row

Date: 2026-06-30

Status: `DRAFT_REVIEW_READY`

## Phase Objective

Upgrade the SIR d18 leaderboard entry from scoped local complete-data component evidence to a properly parameterized observed-data likelihood row, or record the exact remaining blocker.

## Entry Conditions Inherited From Previous Phase

- Phase 4 closed with predator-prey cells either honestly T20-aligned or precisely blocked; no Phase 4 predator-prey value/score status is an SIR d18 prerequisite.
- P91 artifacts remain available as component evidence, not full observed-data leaderboard evidence.
- The program has agreed that a score row requires free `theta`.
- The existing source-scope SIR row had no free theta; Phase 5 must create a new parameterized observed-data row contract before any score row can execute.

## Required Artifacts

- SIR d18 parameter contract: free theta, fixed nuisance values, transforms, data generation, and observed-data target.
- Row-admission contract for the observed-data leaderboard cell: free `theta`, observed-data target, finite value/score requirements, calibration gate, blocker semantics, and nonclaims.
- Evaluator code and tests if implementation proceeds.
- Expected-score calibration manifest across generated observed-data datasets if a full score is emitted; this is not a per-dataset score-zero manifest.
- Updated leaderboard JSON/Markdown row artifact, or a blocked/no-row artifact that keeps P91 as sidecar only:
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`
- GPU/XLA smoke manifest only if the Phase 5 result makes an HMC/GPU-readiness claim, using trusted GPU context.
- Phase result:
  `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-result-2026-06-30.md`
- Refreshed Phase 6 subplan.

## Required Checks, Tests, Reviews

- Parameterized likelihood contract review before implementation.
- Finite value and finite score if implemented.
- Multi-replicate expected-score calibration at true `theta_0` if a full observed-data score row is admitted:
  - minimum 10 independently generated observed-data datasets at the same `theta_0`;
  - compute one score vector per dataset at `theta_0`;
  - for every score component, require all finite values and `abs(mean_score_j) <= 2 * sample_sd_j`;
  - if `sample_sd_j == 0`, require `abs(mean_score_j) == 0` for that component or mark the calibration inconclusive/blocked;
  - record `abs(mean_score_j) / (sample_sd_j / sqrt(n))` as advisory precision, not as the owner-requested veto unless a later reviewed plan changes the gate.
  Individual dataset scores are not required to be zero.
- FD consistency as necessary but not sufficient.
- CPU/GPU/XLA checks only in trusted context where claimed; GPU/XLA is non-required for row admission unless the claim being made depends on GPU/HMC-readiness.
- Claude review of parameter contract and result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the SIR d18 row be turned into a real observed-data likelihood/score row? |
| Baseline/comparator | Observed-data leaderboard row-admission contract: declared free `theta`, observed-data target definition, finite value/score, and expected-score calibration. P91 local complete-data evidence is boundary context/sidecar evidence only, not a promotion comparator. |
| Primary criterion | Either the observed-data row-admission contract passes, including free `theta`, finite value/score, and expected-score calibration, or the row remains blocked with a precise missing contract/evaluator/calibration item while preserving P91 as scoped sidecar only. |
| Veto diagnostics | No free theta; complete-data component called full filtering likelihood; expected-score calibration failure or inconclusive calibration; nonfinite value/score; untrusted GPU/XLA claim. |
| Explanatory diagnostics | FD residuals, per-seed score distribution, CPU/GPU timing. |
| Not concluded | No exact likelihood proof, no posterior/HMC convergence, no broad production claim unless separate gates pass. |
| Artifact | Parameter contract, tests/manifests, regenerated leaderboard, Phase 5 result. |

## Forbidden Claims And Actions

- Do not treat P91 local complete-data closure as full observed-data filtering closure.
- Do not create a score row without a free parameter vector.
- Do not solve `score(theta)=0` as a required gate; expected-score calibration at true theta is the high-dimensional consistency diagnostic here.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 if:

- SIR row-admission criteria pass and the row is parameterized/executed with finite value/score plus passing expected-score calibration, or the row is blocked with an exact missing contract/evaluator/calibration item.
- P91 sidecar boundaries remain visible in the leaderboard.

## Stop Conditions

Stop if:

- The SIR target contract requires a scientific/product decision not already in the plan.
- Full observed-data likelihood cannot be specified without changing model assumptions.
- Expected-score calibration is inconclusive or fails and no reviewed repair can be completed within the phase.
- GPU/XLA trusted execution is unavailable but would be required for the claim being made.

## End-of-Subplan Protocol

1. Run required local checks.
2. Write Phase 5 result/close record.
3. Draft or refresh Phase 6 subplan.
4. Review Phase 6 subplan for generalized-SV target safety.
