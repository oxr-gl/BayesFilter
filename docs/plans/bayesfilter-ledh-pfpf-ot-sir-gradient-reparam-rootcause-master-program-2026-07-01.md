# SIR Gradient Reparameterization Root-Cause Master Program

Date: 2026-07-01

Status: `DRAFT_FOR_CLAUDE_REVIEW`

## Role Contract

Codex in this conversation is the supervisor and executor.

Claude is a read-only reviewer only.  Claude may inspect exact repo paths but
must not edit files, run commands, launch agents, approve boundary changes, or
authorize scientific claims.

## Objective

Systematically test whether the SIR `log_kappa_scale` / `log_nu_scale`
gradient discrepancy is caused by scalar parametrization, regional aggregation,
infection-vs-recovery geometry, the manual RK4 transition score, the transport
adjoint / stopped-scale-key boundary, or centered process-noise
representation.

The program is diagnostic.  It does not propose a production reparameterization
until the score route is understood.

## Entry Evidence

Current completed artifacts:

- Raw budget-10 SIR gate:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-2026-06-30.md`
- Physics/whitening result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparameterization-diagnostic-result-2026-07-01.md`
- Whitened JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-whitened-budget10-2026-07-01.json`

Observed signal:

- Observation-noise direction is comparatively stable.
- Global kappa/nu directions are problematic.
- The dominant whitened discrepancy direction is approximately
  `-0.9666 log_kappa_scale + 0.2562 log_nu_scale`.
- Score covariance is highly anisotropic, so score whitening is diagnostic only.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which part of the SIR dynamic-parameter score explains the budget-10 manual-score vs FD mismatch? |
| Baseline/comparator | Existing raw, physics, and whitened budget-10 GPU/XLA/TF32 artifacts with fixed seeds `81120..81124`, `T=3`, `N=64`, Sinkhorn budget 10. |
| Primary criterion | Each phase must produce an artifact that either passes its stated local check or narrows the next root-cause target without changing the baseline route. |
| Veto diagnostics | CPU-only material route, non-XLA material route, TF32 disabled for material LEDH route, changed seeds/theta/budget without documentation, missing chain-rule checks, unsupported HMC/scientific claim, exit 137 without blocker record. |
| Explanatory diagnostics | Per-region score/FD tables, projected MCSE, component decompositions, regional rho/tau geometry, RK4 sensitivity residuals, non-centered route deltas, runtime/memory traces. |
| Not concluded | No HMC readiness, posterior correctness, SIR gradient correctness, production default, or global reparameterization claim. |
| Artifacts | Phase subplans/results, visible ledger, Claude review ledger, JSON diagnostics under `docs/plans`. |

## Phase Index

| Phase | Name | Objective | Subplan | Result |
| --- | --- | --- | --- | --- |
| 0 | Scope and route freeze | Freeze baselines, code paths, and exact questions before implementation. | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase0-scope-route-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase0-scope-route-result-2026-07-01.md` |
| 1 | Regional kappa expansion | Test exact chain-rule expansion from one scalar kappa scale to region-level kappa scores. | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase1-regional-kappa-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase1-regional-kappa-result-2026-07-01.md` |
| 2 | Regional orthogonal kappa/nu | Test regional epidemic-growth and time-scale directions after Phase 1. | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase2-regional-orthogonal-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase2-regional-orthogonal-result-2026-07-01.md` |
| 3 | RK4 sensitivity audit | Audit the manual RK4 transition derivative against sensitivity equations/autodiff local checks. | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-result-2026-07-01.md` |
| 4 | Transport adjoint and stopped-scale-key audit | Audit the manual transport reverse wrapper after Phase 3 clears transition algebra. | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-result-2026-07-01.md` |
| 5 | Synthesis and handoff | Decide the smallest justified repair or next discriminating diagnostic. | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase5-synthesis-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase5-synthesis-result-2026-07-01.md` |

## Phase Dependencies

1. Phase 1 may implement diagnostic-only code only after Phase 0 confirms the
   current scalar code path and artifact baseline.
2. Phase 2 must not run until Phase 1 verifies or falsifies the regional
   chain-rule relation.
3. Phase 3 can start early only if Phase 1 identifies transition/RK4 terms as
   the likely mismatch; otherwise it follows Phase 2.
4. Phase 4 must be refreshed from Phase 3 evidence.  After Phase 3 passes,
   the active Phase 4 gate is the transport-adjoint / stopped-scale-key audit;
   non-centered process-noise diagnostics remain possible later work rather
   than the next automatic branch.
5. Phase 5 must separate implementation bugs, numerical/tuning failures, and
   evidence against a parametrization hypothesis.

## Repair Loop

For any material blocker:

1. Write the blocker in the current phase result or a focused blocker note.
2. Identify the smallest repair that preserves the phase evidence contract.
3. Review material repair plans with Claude read-only, max five rounds for the
   same blocker.
4. Apply the repair visibly.
5. Rerun focused local checks, then rerun only the necessary material command.
6. If the same blocker remains after five review rounds, stop for human
   direction.

## Anticipated Approvals

Already covered by user policy in this thread:

- Bounded Claude read-only review of repo artifacts.
- Sending exact repo paths to Claude for read-only review.

Commands still requiring trusted/escalated execution by policy:

- `bash scripts/claude_worker.sh ...` for bounded read-only Claude review in
  the current visible conversation.  This is a reviewer subprocess, not a
  detached supervisor or execution authority.
- Any TensorFlow GPU/XLA/TF32 material diagnostic.
- `nvidia-smi` or other GPU status probes.

No package installation, network data fetch, detached supervisor, destructive
git operation, or default-policy change is authorized by this plan.

## Stop Conditions

Stop if:

- Phase subplan review does not converge after five Claude rounds for the same
  blocker.
- Continuing requires changing the scientific question or pass/fail criteria
  after seeing results.
- Continuing requires package installation, data fetch, credentials, detached
  execution, or destructive filesystem/git action.
- A material GPU command cannot be run in trusted context.
- A phase result cannot preserve the nonclaims listed above.
