# P75 Phase 8 Subplan: Source-Guided Square-Root Prefit Implementation

metadata_date: 2026-06-18
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE8
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase7-ukf-source-guided-initializer-design-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Implement one opt-in `source_guided_prefit` initializer mode and run only a
tiny same-draw diagnostic to test whether nonconstant source-guided prefit
improves the geometry of \(h_\theta\) beyond random and calibrated-constant
initialization.

## Entry Conditions Inherited From Phase 7

Phase 8 may begin only if:

- Phase 7 design result exists;
- Phase 7 selects exactly one implementation target;
- this subplan exists;
- local planning checks pass;
- Claude returns `VERDICT: AGREE` for the Phase 7 result and this subplan, or
  fixable issues have been patched and re-reviewed.

## Required Artifacts

Phase 8 must produce:

- implementation diffs limited to:
  - `bayesfilter/highdim/stochastic_density_training.py`;
  - `scripts/p75_stochastic_density_training_pilot.py`;
  - `tests/highdim/test_p75_stochastic_density_training.py`;
- tiny diagnostic JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-source-guided-prefit-smoke-2026-06-18.json`;
- Phase 8 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase8-source-guided-prefit-implementation-result-2026-06-18.md`;
- a Phase 9 decision/handoff subplan;
- updated execution and Claude review ledgers.

## Required Checks/Tests/Reviews

Implementation checks:

```bash
python -m py_compile bayesfilter/highdim/stochastic_density_training.py scripts/p75_stochastic_density_training_pilot.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p75_stochastic_density_training.py
```

Tiny diagnostic command, to be finalized only after implementation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --target-pilot --compare-init-modes --include-source-guided-prefit --degree 1 --rank 1 --batch-size 32 --batches 2 --prefit-steps 5 --max-seconds 180 --seed 7501 --output docs/plans/bayesfilter-highdim-zhao-cui-p75-source-guided-prefit-smoke-2026-06-18.json
```

Diff hygiene:

```bash
git diff --check -- bayesfilter/highdim/stochastic_density_training.py scripts/p75_stochastic_density_training_pilot.py tests/highdim/test_p75_stochastic_density_training.py docs/plans/bayesfilter-highdim-zhao-cui-p75-phase8-source-guided-prefit-implementation-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-source-guided-prefit-smoke-2026-06-18.json
```

Review:

- Claude read-only review of the implementation diff, tiny diagnostic JSON,
  Phase 8 result, and Phase 9 subplan;
- loop to convergence or max 5 rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does a bounded source-guided square-root prefit improve the tiny P75 target-smoke geometry beyond random and calibrated-constant initialization without audit leakage or numerical failure? |
| Exact baseline/comparator | Same-draw random and calibrated-constant arms from the same command. |
| Primary pass/fail criterion | The prefit arm must complete all declared prefit and density-objective steps with finite losses, gradients, normalizers, and parameters, must avoid audit leakage, and must improve the frozen primary geometry diagnostic over calibrated constant on identical audit draws. |
| Frozen primary geometry diagnostic | Use holdout `rms_relative` as primary if finite in all compared arms; if it is unavailable, block rather than switch metrics after seeing outputs. |
| Diagnostics that can veto | Any audit-data use for initialization/prefit/stopping/hyperparameters; nonfinite terms; runner exception; wall-clock cap before one prefit and one objective step; source-faithfulness overclaim; lower-gate or validation claim; larger pilot launch. |
| Explanatory only | Replay residuals, line residuals, loss traces, gradient norms, rho range, normalizer, runtime, exact residual magnitudes, whether audit gates still block. |
| What will not be concluded | No lower-gate repair, validation readiness, HMC readiness, scaling, source-faithful Zhao--Cui parity, rank/sample policy, or larger-pilot authorization. |
| Artifact preserving result | Tiny diagnostic JSON, Phase 8 result note, ledgers, Claude review. |

## Implementation Requirements

The implementation must:

- add a prefit loss to `TrainableFunctionalTT` equivalent to
  \[
      \frac{\sum_i w_i(h_\theta(z_i)-y_i)^2}
           {\sum_i w_i y_i^2+\epsilon}
      +\lambda_{\rm pre}\|\theta-\theta_{\rm const}\|_2^2
  \]
  or a documented equivalent with fixed scale floor;
- add a prefit step using `tf.GradientTape` and finite-gradient checks;
- keep TensorFlow/TensorFlow Probability as the differentiable backend;
- add an opt-in runner mode that starts from calibrated constant and applies
  prefit only to training-eligible source-route batches;
- record prefit step count, prefit loss trace, guide provenance, and
  `uses_audit_data=false`;
- keep random and calibrated-constant arms available;
- preserve default P72/P73/P75 behavior unless the new opt-in flags are used.

## Forbidden Claims/Actions

- Do not run the degree 2/rank 4/batch 1024/up-to-500 pilot.
- Do not run validation, HMC, scaling, GPU, or rank promotion.
- Do not use audit holdout, replay, or line samples for initialization,
  prefit, stopping, or hyperparameter selection.
- Do not claim UKF truth, source-faithful Zhao--Cui, lower-gate repair, or
  validation readiness.
- Do not change the primary geometry diagnostic after seeing outputs.
- Do not edit unrelated files or default source-route behavior.

## Exact Next-Phase Handoff Conditions

Phase 9 may begin only if:

- Phase 8 result exists;
- tiny diagnostic JSON exists and is valid;
- local checks pass;
- the result classifies the prefit arm as mechanism pass or block under the
  frozen evidence contract;
- Phase 9 subplan exists and either plans a bounded next diagnostic or writes
  a stop handoff;
- Claude returns `VERDICT: AGREE`, or a blocker is escalated to the user.

## Stop Conditions

Stop before implementation if:

- Claude finds the Phase 7 design or this subplan incoherent;
- the implementation would require a full Gaussian-to-TT projection;
- the implementation would require GPU, network, package installation, or
  outside-repo writes.

Stop during implementation if:

- focused unit tests fail in a way not attributable to the new opt-in surface;
- prefit uses or can use audit data;
- the command would exceed the tiny CPU-only bounds;
- the prefit implementation changes P72/P73 defaults.

Stop after execution if:

- the prefit arm fails numerical/provenance checks;
- the JSON cannot support the frozen primary comparison;
- Claude identifies a material blocker that cannot be repaired within five
  review rounds.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit because it compares only
same-draw arms, freezes holdout RMS relative as the primary geometry
diagnostic before running, forbids larger pilots and downstream claims, and
keeps the implementation opt-in and limited to the surfaces needed by the
Phase 7 design.
