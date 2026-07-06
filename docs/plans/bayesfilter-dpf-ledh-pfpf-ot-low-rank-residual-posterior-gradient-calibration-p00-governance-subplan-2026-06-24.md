# P00 Governance And Launch Review Subplan

Date: 2026-06-24

Status: `DRAFT_REVIEW_PENDING`

## Phase Objective

Verify that the posterior-gradient residual calibration master program,
visible runbook, ledgers, stop handoff, and P01-P07 subplans are complete,
consistent, locally checkable, and safe before any instrumentation or trusted
GPU runtime is launched.

P00 is local-check-only except for Claude read-only review. P00 does not run
GPU benchmarks, HMC/autodiff runtime, package/API changes, default-policy
changes, model-file edits, package installs, network fetches, or scientific
claims.

## Entry Conditions Inherited From Previous Phase

- User requested a gated master program with phase subplans, repair loop,
  Claude read-only review, and a visible execution runbook.
- Current working directory is `/home/ubuntu/python/BayesFilter`.
- BayesFilter policy applies: TensorFlow/TFP GPU/XLA default; no NumPy in
  BayesFilter-owned algorithmic implementation paths; evidence contracts and
  skeptical audit are required.
- P01 model-suite stop exists:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p01-lgssm-kalman-result-2026-06-24.md`.
- No approval is inherited for GPU runtime, HMC runtime, package/API changes,
  public default changes, package installs, network fetches, destructive git
  operations, or scientific claims.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-master-program-2026-06-24.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-visible-gated-execution-runbook-2026-06-24.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-claude-review-ledger-2026-06-24.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-visible-execution-ledger-2026-06-24.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-visible-stop-handoff-2026-06-24.md`
- P00 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p00-governance-result-2026-06-24.md`
- P01-P07 subplans under `docs/plans`.

## Required Checks, Tests, And Reviews

- File-existence check for all required program artifacts and P00-P07 subplans.
- Required-field scan for every subplan:
  - phase objective;
  - entry conditions inherited from the previous phase;
  - required artifacts;
  - required checks/tests/reviews;
  - evidence contract;
  - forbidden claims/actions;
  - exact next-phase handoff conditions;
  - stop conditions.
- Boundary scan for unsupported promotion, HMC, public API, package default,
  posterior correctness, statistical superiority, dense equivalence, product,
  funding, or scientific-validity claims.
- Source-surface inventory for existing low-rank, LGSSM, Kalman, and actual-SIR
  harness paths.
- Syntax checks for existing relevant harnesses:
  - `docs/benchmarks/benchmark_low_rank_ledh_lgssm_kalman_gate.py`
  - `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`
- Claude Opus/max read-only review of the master program, visible runbook,
  P00, and P01 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the residual posterior-gradient calibration program safe, complete, and review-converged enough to launch P01 instrumentation? |
| Baseline/comparator | P01 LGSSM stop artifact, existing low-rank/LGSSM/actual-SIR harness surfaces, and BayesFilter governance. |
| Primary pass criterion | Required artifacts exist, required subplan sections are present, local checks pass, boundary scan passes, Claude review converges, and P00 result preserves nonclaims. |
| Veto diagnostics | Missing artifact, missing subplan field, unsupported claim, stale comparator, failed syntax check, unapproved runtime/default/API/HMC/science boundary, or Claude nonconvergence. |
| Explanatory diagnostics | Current git status, discovered harness inventory, and warning text from local checks. |
| Not concluded | No calibrated threshold, posterior correctness, HMC readiness, package default readiness, public API readiness, statistical superiority, or scientific validity. |
| Artifact | P00 result, review ledger, execution ledger, and refreshed P01 subplan if needed. |

## Skeptical Pre-Execution Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: P00 audits plans only and anchors to P01 stop plus current harness surfaces. |
| Proxy metric promoted | Guarded: P00 interprets no runtime metric and requires residuals to remain proxy diagnostics. |
| Missing stop conditions | Guarded by required-field and boundary scans. |
| Unfair comparison | Guarded: no comparison is run in P00. |
| Hidden assumptions | Guarded: P00 checks that value/gradient/peak meanings are explicit. |
| Stale context | Guarded: P00 inventories current code/doc surfaces before P01. |
| Environment mismatch | Guarded: P00 makes no GPU claim. |
| Artifact mismatch | Guarded: P00 file-existence check names every required artifact. |

Audit conclusion: P00 may proceed as local document/source checks and Claude
read-only review after all subplans are drafted.

## Forbidden Claims And Actions

- Do not claim a calibrated threshold, model-suite promotion, broad default
  readiness, posterior correctness, HMC readiness, statistical superiority,
  dense Sinkhorn equivalence, public API readiness, package readiness, product
  readiness, funding readiness, or scientific validity.
- Do not run GPU benchmarks in P00.
- Do not run HMC/autodiff runtime in P00.
- Do not change public API, package metadata, default policy, model files, or
  dependencies.
- Do not use Claude as executor or authority.
- Do not send whole large files to Claude; ask Claude to read named artifacts
  and focus on relevant sections.

## Exact Next-Phase Handoff Conditions

P00 hands off to P01 only if:

- local artifact checks pass;
- required-section and boundary scans pass;
- relevant source-surface inventory is recorded;
- syntax checks pass or failures are clearly irrelevant and recorded;
- Claude review returns `VERDICT: AGREE` within five rounds for any same
  blocker;
- P00 result is written;
- P01 subplan is refreshed and reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety.

If P00 fails because of a fixable plan issue, patch the same subplan or program
artifact visibly and rerun focused checks. If P00 does not converge, write a
blocker result and stop.

## Stop Conditions

- Missing required artifact or required subplan field that cannot be repaired
  without changing program scope.
- Local checks fail in a way that invalidates planned early instrumentation.
- No concrete path exists to instrument LGSSM value/gradient metrics without
  unapproved package/API/default/model-file changes.
- Claude review finds a material issue that does not converge within five
  rounds for the same blocker.
- Continuing would require GPU runtime, HMC runtime, package/API/default
  change, model-file edit, network fetch, package install, destructive git
  operation, or scientific claim not authorized by the reviewed plan.

## End-Of-Subplan Procedure

1. Run required local checks.
2. Write P00 result or blocker result.
3. Draft or refresh P01 subplan.
4. Review P01 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
5. If material, send P01 to Claude read-only review and record the verdict.
