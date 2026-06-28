# P00 Governance And Launch Review Subplan

Date: 2026-06-24

Status: `REVIEW_CONVERGED_READY_FOR_P00_EXECUTION`

## Phase Objective

Verify that the model-suite promotion master program, visible runbook,
ledgers, stop handoff, and provisional P01-P08 subplans are complete,
consistent, safe, and locally checkable before any model-suite runtime is
launched.

P00 is local-check-only except for Claude read-only review. It does not run GPU
benchmarks, HMC/autodiff runtime, package/API changes, default-policy changes,
or model-file edits.

## Entry Conditions Inherited From Previous Phase

- User requested a master program with phase subplans, repair loop, Claude
  read-only review, and visible gated execution runbook.
- Current working directory is `/home/ubuntu/python/BayesFilter`.
- BayesFilter policy applies: TensorFlow/TFP GPU/XLA default; no NumPy in
  BayesFilter-owned algorithmic paths; evidence contracts and skeptical audit
  required.
- Completed bounded actual-SIR d18 result exists:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-result-2026-06-24.md`.
- No approval is inherited for GPU model-suite runtime, HMC runtime,
  package/API changes, public default changes, package installs, network
  fetches, destructive git operations, or scientific claims.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-master-program-2026-06-24.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-visible-gated-execution-runbook-2026-06-24.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-claude-review-ledger-2026-06-24.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-visible-execution-ledger-2026-06-24.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-visible-stop-handoff-2026-06-24.md`
- P00 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p00-governance-result-2026-06-24.md`
- Provisional P01-P08 subplans under `docs/plans`.

## Required Checks, Tests, And Reviews

- File-existence check for all required program artifacts and P00-P08 subplans.
- Required-field scan for every subplan:
  - phase objective;
  - entry conditions inherited from previous phase;
  - required artifacts;
  - required checks/tests/reviews;
  - evidence contract;
  - forbidden claims/actions;
  - exact next-phase handoff conditions;
  - stop conditions.
- Boundary scan for unsupported promotion, HMC, public API, package default,
  posterior correctness, statistical superiority, dense equivalence, or
  scientific-validity claims.
- Syntax checks for existing harnesses expected in early phases:
  - `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py`
  - `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`
  - `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py`
- P01 executable-surface audit before P00 can pass:
  - locate a concrete LGSSM exact-Kalman low-rank LEDH harness/validator, or
    record `P01_HARNESS_MISSING_REQUIRES_IMPLEMENTATION_SUBPLAN`;
  - if missing, refresh P01 as an implementation-before-runtime subplan with
    an explicit write set and focused tests;
  - verify the P01 harness or planned harness contract can emit exact Kalman
    metrics for filtered means, variances, and log likelihood for the pinned
    P01 cases and seeds.
- Focused local tests:
  - `tests/test_low_rank_ledh_pfpf_efficiency.py`
  - `tests/test_actual_sir_low_rank_route_validation.py`
  - `tests/test_actual_sir_low_rank_tuning_grid.py`
- Claude Opus/max read-only review of master program, runbook, P00, and P01
  subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the model-suite promotion program safe, complete, and review-converged enough to launch P01 after P00 closeout? |
| Baseline/comparator | Completed actual-SIR d18 bounded result and current low-rank/streaming harness surfaces. |
| Primary pass criterion | Required artifacts exist, required subplan sections are present, local checks pass, boundary scan passes, Claude review converges, and P00 result preserves nonclaims. |
| Veto diagnostics | Missing artifact, missing subplan section, unsupported claim, stale comparator, failed local check, unapproved runtime/default/API/HMC/science boundary, or Claude nonconvergence. |
| Explanatory diagnostics | Current git status, discovered harness inventory, and warning text from local tests. |
| Not concluded | No model-suite promotion, algorithm correctness, speedup, posterior correctness, HMC readiness, public API readiness, package default readiness, statistical superiority, or scientific validity. |
| Artifact | P00 result, review ledger, execution ledger, and refreshed P01 subplan if needed. |

## Skeptical Pre-Execution Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: P00 audits plans only and anchors to the completed actual-SIR d18 bounded result. |
| Proxy metric promoted | Guarded: P00 interprets no runtime metrics. |
| Missing stop conditions | Guarded by required-section and boundary scans. |
| Unfair comparison | Guarded: no comparison is run in P00. |
| Hidden assumptions | Guarded: P00 must distinguish exact LGSSM reference, synthetic LGSSM-shaped evidence, and actual-SIR target evidence. |
| Stale context | Guarded: P00 runs source/artifact inventory before P01. |
| Environment mismatch | Guarded: P00 makes no GPU claim. |
| Artifact mismatch | Guarded: P00 file-existence check names every required artifact. |

Audit conclusion: P00 may proceed as local document/source checks and Claude
read-only review after this draft passes local syntax checks.

## Forbidden Claims And Actions

- Do not claim model-suite promotion, broad default readiness, posterior
  correctness, HMC readiness, statistical superiority, dense Sinkhorn
  equivalence, public API readiness, package-level readiness, or scientific
  validity.
- Do not run GPU model-suite benchmarks in P00.
- Do not let P00 pass into P01 runtime unless the P01 exact-Kalman harness and
  validator are concretely identified or P01 is refreshed as an approved
  implementation-before-runtime phase.
- Do not run HMC/autodiff runtime in P00.
- Do not change public API, package metadata, default policy, model files, or
  dependencies.
- Do not use Claude as an executor or authority.
- Do not send whole large files to Claude; ask Claude to read named artifacts
  and focus on relevant sections.

## Exact Next-Phase Handoff Conditions

P00 hands off to P01 only if:

- local artifact checks pass;
- required-section and boundary scans pass;
- P01 exact-Kalman executable surface is identified, or P01 is explicitly
  refreshed as a harness implementation subplan with no runtime until that
  implementation passes focused checks;
- focused syntax/tests pass or failures are clearly irrelevant and recorded;
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
- Local checks fail in a way that invalidates the planned early harnesses.
- No concrete path exists to create a P01 exact-Kalman harness without
  unapproved code/model-file/default/API changes.
- Claude review finds a material issue that does not converge within five
  rounds for the same blocker.
- Continuing would require GPU runtime, HMC runtime, package/API/default
  change, model-file edit, network fetch, package install, destructive git
  operation, or scientific claim not authorized by the reviewed plan.

## End-Of-Subplan Procedure

1. Run required local checks.
2. Write P00 result or blocker result.
3. Draft or refresh P01 subplan.
4. Review P01 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
5. If material, send P01 to Claude read-only review and record the verdict.
