# P76 Phase 3 Subplan: Opt-In UKF Initializer Implementation

metadata_date: 2026-06-18
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE3
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase2-implementation-surface-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Implement the opt-in TensorFlow UKF initializer
`ukf_whitened_gaussian_sqrt_projection_v1` and focused CPU-only tests.  The
implementation must produce finite TT cores from UKF scout moments and must be
usable as initial cores for `TrainableFunctionalTT`.

## Entry Conditions Inherited From Phase 2

Phase 3 may begin only if:

- Phase 2 result exists;
- Phase 2 names exact files, functions, tests, and commands;
- Phase 2 preserves TensorFlow/TensorFlow Probability as the default
  implementation backend;
- Phase 2 forbids source-route prefit as \(h_0\);
- Phase 2 local checks pass;
- Claude agrees Phase 2 and this subplan are consistent, or repairable issues
  are patched and re-reviewed.

Claude's non-blocking Phase 2 refinement is binding for implementation: the
focused tests must explicitly assert that `time_index == 1` uses
`mean_path[0]` and `covariance_path[0]` for the previous block.

## Required Artifacts

Phase 3 must produce:

- implementation module:
  `bayesfilter/highdim/ukf_initializer.py`;
- focused tests:
  `tests/highdim/test_p76_ukf_initializer.py`;
- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase3-optin-ukf-initializer-implementation-result-2026-06-18.md`;
- reviewed Phase 4 smoke subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-subplan-2026-06-18.md`;
- updated execution and Claude review ledgers;
- updated runbook Phase Index.

## Required Checks/Tests/Reviews

Local checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/ukf_initializer.py tests/highdim/test_p76_ukf_initializer.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p76_ukf_initializer.py tests/highdim/test_p75_stochastic_density_training.py
rg -n "square_root_prefit|source_guided_prefit|source-route prefit" bayesfilter/highdim/ukf_initializer.py tests/highdim/test_p76_ukf_initializer.py
git diff --check -- bayesfilter/highdim/ukf_initializer.py tests/highdim/test_p76_ukf_initializer.py docs/plans/bayesfilter-highdim-zhao-cui-p76-phase3-optin-ukf-initializer-implementation-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
```

Review:

- Claude read-only review of implementation diff, Phase 3 result, and Phase 4
  subplan;
- loop to convergence or max 5 rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can the Phase 1 UKF initializer be implemented as an opt-in TensorFlow surface with focused contract tests? |
| Exact baseline/comparator | Phase 2 named surface and current `ukf_scout.py` / `stochastic_density_training.py`. |
| Primary criterion | Implementation and focused tests pass CPU-only checks, produce finite cores, preserve manifests/nonclaims, and avoid source-route prefit. |
| Diagnostics that can veto | Nonfinite cores; invalid covariance handling; missing degree guard; source-prefit call path; audit leakage; default export/change; GPU use; tests fail. |
| Explanatory only | Exact coefficient values, finite log-density values, manifest summaries, test runtime. |
| What will not be concluded | No lower-gate repair, no validation/HMC readiness, no large mini-batch pilot, no scaling claim. |
| Artifact preserving result | Code diff, test output, Phase 3 result, Phase 4 subplan, ledgers, Claude review. |

## Forbidden Claims/Actions

- Do not edit files outside the Phase 3 edit boundary.
- Do not export the module from `bayesfilter/highdim/__init__.py`.
- Do not use NumPy as the implementation backend.
- Do not run GPU/CUDA.
- Do not run a training pilot beyond focused CPU-only tests.
- Do not call `square_root_prefit_step`, `square_root_prefit_objective`, or
  `source_guided_prefit` from the initializer.
- Do not claim the initializer works empirically or repairs the lower gate.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only if:

- Phase 3 result exists;
- Phase 4 smoke subplan exists;
- CPU-only compile/tests pass or a precise blocker is written;
- the initializer result manifest records `source_route_prefit_used: false`
  and `audit_data_used: false`;
- no default behavior changed;
- Claude agrees, or a blocker is escalated.

## Stop Conditions

Stop if:

- TensorFlow implementation cannot compute projection coefficients without a
  backend exception;
- `UKFScoutResult` lacks enough information for adjacent moments;
- covariance stabilization cannot be made finite and SPD for focused tests;
- focused tests require GPU/CUDA, package installation, network, or a default
  behavior change;
- the only passing implementation route uses source-route prefit;
- Claude identifies a material blocker that cannot be repaired within five
  rounds.

## Skeptical Plan Audit

Phase 3 answers only whether the UKF initializer can be implemented and tested
as an opt-in surface.  It cannot promote the initializer to a validation,
HMC-readiness, or lower-gate repair claim.
