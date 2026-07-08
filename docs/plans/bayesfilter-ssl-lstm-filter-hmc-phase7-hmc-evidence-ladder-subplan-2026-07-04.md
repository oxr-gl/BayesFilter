# Phase 7 Subplan: HMC Mechanics And Evidence Ladder

Date: 2026-07-04

Status: `DRAFT_READY_FOR_PRECHECK`

## Phase Objective

Run the gated HMC evidence ladder on admitted SSL-LSTM filter adapters, classify
hard vetoes first, and interpret invariant estimation metrics with statistical
humility.

The first launch tier is a bounded HMC mechanics smoke. It may only classify
hard vetoes, verify the HMC target path, and record artifact validity. It must
not be treated as convergence, ranking, or replicated-evidence success.

## Entry Conditions Inherited From Previous Phase

- Phase 6 passed local checks and wrote the shared benchmark runner, smoke
  artifact, data manifest, metric roles, and artifact schema.
- Candidate adapters have admitted, failed, or blocked status.
- GPU/XLA is the production-like target unless a reviewed debug/reference
  exception is recorded.

## Required Artifacts

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase7-hmc-evidence-ladder-result-2026-07-04.md`
- Run manifests with git commit, command, environment, CPU/GPU status, data
  version, seeds, wall time, output paths, plan file, and result file.
- HMC diagnostic JSON/Markdown artifacts for the launch smoke, then warmup,
  short-chain, and replicated evidence runs only if the prior tier authorizes
  them.
- Decision table separating hard vetoes, viable candidates, descriptive-only
  differences, statistical ranking status, default-readiness status, and next
  evidence needed.
- Inference-status table separating hard veto screens from descriptive-only
  differences.
- Refreshed Phase 8 subplan.

## Required Checks, Tests, And Reviews

- Pre-run evidence contract recorded for each serious run.
- HMC hard veto diagnostics: divergence, non-finite log prob/grad, R-hat/ESS
  gate, acceptance pathologies, and invalid artifact.
- Invariant metrics computed only after sampler diagnostic vetoes pass.
- Multi-seed or uncertainty evidence required before any ranking claim.
- The launch smoke uses one tiny fixed-kernel run per admitted candidate and is
  a repair/localization gate only.
- The Phase 6 smoke artifact is benchmark-only and cannot be promoted to HMC
  convergence evidence.
- Claude read-only review for result interpretation and nonclaims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which admitted filter-HMC adapters remain viable for SSL-LSTM estimation under the shared benchmark? |
| Baseline/comparator | Shared Phase 6 benchmark with identical data, prior, HMC runtime, seeds, and budget for every admitted candidate. |
| Primary pass criterion | Launch tier: every admitted candidate receives a hard-veto classification and the artifact records that convergence, ranking, and invariant-metric promotion are not concluded. Full Phase 7 evidence later requires at least one candidate to pass hard HMC vetoes and meet predeclared invariant metric thresholds under a replicated tier. |
| Veto diagnostics | Divergences beyond threshold, non-finite values/gradients, R-hat/ESS failure, invalid artifacts, missing run manifest, or criteria changed after results. |
| Explanatory diagnostics | Runtime, acceptance, descriptive metric differences, posterior summaries, and mass conditioning. |
| Not concluded | Method superiority without uncertainty evidence, exact posterior correctness, parameter identifiability, production readiness, or default policy changes. |
| Result artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase7-hmc-evidence-ladder-result-2026-07-04.md` |

## Forbidden Claims And Actions

- Do not rank viable stochastic candidates using descriptive diagnostics alone.
- Do not treat passing a hard screen as superiority.
- Do not interpret invariant metrics if HMC hard veto diagnostics fail.
- Do not change thresholds after seeing results.
- Do not run untrusted GPU commands and treat failures as machine evidence.
- Do not use the Phase 6 smoke artifact as a substitute for HMC evidence.
- Do not describe a launch-smoke pass as full Phase 7 success.
- Do not compute or interpret R-hat/ESS from the launch smoke.

## Exact Next-Phase Handoff Conditions

Phase 8 may start only when:

- every candidate has a hard-veto classification;
- viable candidates and blocked/failed candidates are separated;
- statistical ranking status is explicitly recorded;
- result notes state what failed, what repair it triggers, and what is not being
  concluded;
- Phase 6 smoke artifact and Phase 7 run manifests are both available for
  review;
- Phase 8 subplan is refreshed for closeout and reset memo.

## Stop Conditions

- Serious HMC runs require approval for compute, GPU trust, package install, or
  environment setup not already granted.
- The benchmark artifact is invalid or corrupted.
- Sampler diagnostics invalidate interpretation for all candidates and the
  planned repair path is outside scope.
- Claude and Codex do not converge on result interpretation after five rounds.

## End-Of-Phase Protocol

1. Run only predeclared HMC ladder commands.
2. Write the Phase 7 result/close record with decision and inference-status
   tables.
3. Draft or refresh the Phase 8 subplan.
4. Review Phase 8 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
