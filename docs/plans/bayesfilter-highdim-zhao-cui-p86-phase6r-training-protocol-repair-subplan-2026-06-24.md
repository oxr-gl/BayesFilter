# P86 Phase 6R Subplan: Training Protocol Repair

Date: 2026-06-24

Status: `DRAFT_READY_FOR_LOCAL_IMPLEMENTATION_PENDING_REVIEW`

## Phase Objective

Repair the Phase 6 rank-convergence training protocol so a higher-rank
comparator cannot be treated as converged merely because it hit a fixed
optimizer-step budget.

Phase 6R adds plateau-aware telemetry, validation/holdout monitoring,
learning-rate reduction on plateau, max-step/max-time exhaustion status, and
trained-core serialization for replay. It prepares a future rank-5 rerun, but
does not authorize one.

## Entry Conditions Inherited From Previous Phase

- P86 Phase 6 is reviewed-blocked:
  `BLOCK_P86_PHASE6_RANK_DEGREE_CONVERGENCE_NOT_ESTABLISHED_REVIEWED`.
- The rank-5 comparator artifact completed mechanically, but its logged loss
  was still decreasing at the final logged step.
- The old fixed-step protocol used Adam with `learning_rate=0.001`, no
  scheduler, no plateau detector, no early stopping, and no trained-core
  serialization.
- ALS remains historical/buggy for fixed-variant Zhao-Cui and must not be used
  for repaired training.
- Degree convergence remains blocked until a reviewed configurable-basis path
  exists.

## Required Artifacts

- This subplan.
- Runner implementation changes in:
  `scripts/p86_author_lagrangep_phase5_budget_fit.py`
- Focused tests in:
  `tests/highdim/test_p86_phase5_budget_preflight.py`
- Phase 6R implementation result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-training-protocol-repair-result-2026-06-24.md`
- Optional approval request artifact if a future smoke/rerun is prepared. It
  must be marked blocked until a dedicated guarded Phase 6R smoke command is
  implemented:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-training-protocol-repair-approval-request-2026-06-24.md`

## Required Checks / Tests / Reviews

- Add local helper tests for plateau classification, LR-drop accounting,
  max-step exhaustion status, and trained-core serialization metadata.
- Run CPU-hidden focused tests:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p86_phase5_budget_preflight.py tests/highdim/test_p86_author_lagrangep_fit_smoke_runner.py tests/highdim/test_p86_downstream_author_route_wiring.py tests/highdim/test_p86_lagrangep_mass_integral.py tests/highdim/test_p86_algebraic_measure_contract.py`
- Run `python -m py_compile` on the runner and test file.
- Run `git diff --check` on touched files.
- Claude read-only bounded review is required for the Phase 6R result before
  any repaired rank-5 fit is requested.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the P86 runner distinguish optimizer convergence from fixed-budget exhaustion and preserve trained state for reviewed replay/convergence diagnostics? |
| Baseline/comparator | Current Phase 6 fixed-step Adam protocol and reviewed rank-5 undertraining diagnosis. |
| Primary criterion | Focused tests pass and the runner can emit scheduler/plateau status, validation monitor records, stop reason, and serialized trained-core metadata without executing an unapproved fit. |
| Veto diagnostics | Loss-only promotion; validation/audit cloud used for tuning without being labeled; max-step exhaustion recorded as convergence; missing core serialization; ALS route reuse; unapproved fit/GPU/HMC/LEDH/scale command. |
| Explanatory diagnostics | Learning-rate history, best validation residual/objective, plateau windows, LR drop count, final-loss deltas, checkpoint core hashes, runtime and memory estimates. |
| Not concluded | No repaired rank-5 convergence, no degree convergence, no posterior correctness, no HMC readiness, no LEDH comparison, no scale claim, and no production readiness. |
| Artifact | Phase 6R result and any future approval request. |

## Forbidden Claims / Actions

- Do not rerun rank 5, run a training smoke, or execute any parameter-training
  command without exact human approval.
- Do not claim convergence from decreasing training loss.
- Do not claim overfitting absence from one holdout split alone.
- Do not use the audit cloud for LR scheduling or early stopping.
- Do not use ALS training.
- Do not run GPU, HMC, LEDH, d=50/d=100, detached, or long commands.
- Do not promote Zhao-Cui SIR to production.

## Exact Next-Phase Handoff Conditions

After Phase 6R implementation review, the next action may be one of:

- stop with repaired tooling and an exact approval request for a tiny scheduler
  smoke;
- after approval, run only the exact tiny scheduler smoke command;
- after smoke review, draft a separate exact-command plan for a rank-5 adaptive
  training rerun.

No future rank-convergence interpretation is allowed until a reviewed repaired
fit artifact exists and trained-core replay/functional diagnostics are run on
frozen validation/audit clouds.

## Stop Conditions

Stop if:

- plateau/LR-drop semantics cannot be tested without running a fit;
- trained-core serialization would require unsafe artifact size or an
  unreviewed storage format;
- validation and audit cloud roles cannot be kept separate;
- any command would train parameters without exact approval;
- Claude and Codex do not converge after five review rounds for a material
  issue.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 6R result / close record;
3. if appropriate, draft an exact command approval request for a tiny
   scheduler smoke;
4. review the result and approval request for consistency, correctness,
   feasibility, artifact coverage, boundary safety, and stop conditions.
