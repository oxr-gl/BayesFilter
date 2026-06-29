# P86 Phase 6T Subplan: L1 Regularization Tuning Guard

Date: 2026-06-25

Status: `REVIEWED_READY_FOR_IMPLEMENTATION`

## Phase Objective

Add explicit, auditable regularization controls for the P86 training-base
route, then freeze a no-fit Phase 6T diagnostic protocol for rank-5
regularization tuning after the reviewed Phase 6S rank-convergence blocker.

This phase may implement L1 objective regularization and expose L1/L2/logZ
weights in the guarded runner. It may write a preflight artifact and approval
request for a future bounded tuning diagnostic. It must not run the expensive
rank-5 tuning grid or claim rank convergence.

## Entry Conditions Inherited From Previous Phase

- Phase 6S rank convergence is reviewed blocked:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank-convergence-result-2026-06-25.md`.
- The adaptive rank-5 artifact is mechanically admissible after classifier
  repair but numerically much worse than the rank-4 lower rung.
- Rank-5 validation residual worsened across the adaptive run, and the
  normalizer collapsed relative to rank 4.
- ALS training is historical/buggy/stale for fixed-variant Zhao-Cui and must
  not be revived.
- Any training-route work must use `training_base_optimizer`,
  `TrainableFunctionalTT`, `P75ObjectiveBatch`, and Adam.
- No human approval exists for a long rank-5 tuning sweep.

## Skeptical Plan Audit

Potential flaws checked before execution:

- Wrong baseline: the baseline remains the reviewed rank-4 lower rung plus the
  reviewed Phase 6S adaptive rank-5 failure, not a new convenient weak
  comparator.
- Proxy promotion: validation residual may tune candidate regularization and
  veto overfitting, but cannot establish rank convergence, posterior
  correctness, HMC readiness, or production readiness.
- Missing stop conditions: this phase stops after local implementation checks,
  no-fit preflight, result record, and Claude execution review unless an exact
  future command receives explicit human approval.
- Unfair comparison: any future tuning command must preserve route, target,
  rank, basis, domain, measure, train/holdout/audit cloud separation, and audit
  non-tuning boundaries.
- Hidden assumptions: worsening validation is only consistent with
  under-regularization/overfitting; it may also be optimizer sensitivity,
  normalizer pathology, initialization sensitivity, or evidence against this
  fixed training-base route.
- Environment mismatch: local implementation checks are CPU-hidden. They are
  not GPU or production evidence.
- Artifact mismatch: if the preflight does not freeze regularization weights,
  LR schedule, seeds, cloud roles, output paths, and nonclaims, it cannot
  support a governed tuning request.

Audit result: proceed with implementation and no-fit tuning preflight only.
Do not run the long rank-5 tuning diagnostic in this phase.

## Required Artifacts

- Phase 6T subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-subplan-2026-06-25.md`
- Phase 6T no-fit tuning preflight JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-preflight-2026-06-25.json`
- Reserved future Phase 6T diagnostic output path:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-diagnostic-2026-06-25.json`
- Phase 6T result / close record:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-result-2026-06-25.md`
- Phase 6T approval request for the future tuning command, only if local checks
  and Claude execution review pass:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-approval-request-2026-06-25.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md`

## Required Checks / Tests / Reviews

- Add `l1_weight` to `P75TrainableTTConfig` in
  `bayesfilter/highdim/stochastic_density_training.py`.
- Validate `l1_weight` as a finite nonnegative scalar.
- Add `l1_weight * sum(abs(core))` to `TrainableFunctionalTT._regularization`.
- Emit `l1_weight` in `config_payload`.
- Add focused P75 unit tests for:
  - config payload includes `l1_weight`;
  - negative/nonfinite/non-scalar `l1_weight` is rejected;
  - objective regularization includes the expected L1 contribution.
- Expose guarded runner CLI weights:
  - `--l1-weight`;
  - `--l2-weight`;
  - `--logz-anchor-weight`.
- Preserve old defaults: `l1_weight=0.0`, `l2_weight=1e-8`,
  `logz_anchor_weight=0.0`.
- Freeze Phase 6T candidate command fields including regularization weights,
  LR schedule, rank, samples, cloud seeds, output path, and serialization.
- Add focused P86 tests for:
  - Phase 6T command string is frozen;
  - Phase 6T no-fit preflight records regularization grid metadata and audit
    non-tuning;
  - exact guard accepts the frozen command;
  - exact guard rejects drift in `l1_weight`, `l2_weight`, and
    `logz_anchor_weight`.
- Run CPU-hidden local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile bayesfilter/highdim/stochastic_density_training.py scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p75_stochastic_density_training.py tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p75_stochastic_density_training.py tests/highdim/test_p86_phase5_budget_preflight.py tests/highdim/test_p86_author_lagrangep_fit_smoke_runner.py tests/highdim/test_p86_downstream_author_route_wiring.py tests/highdim/test_p86_lagrangep_mass_integral.py tests/highdim/test_p86_algebraic_measure_contract.py
git diff --check -- bayesfilter/highdim/stochastic_density_training.py scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p75_stochastic_density_training.py tests/highdim/test_p86_phase5_budget_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-subplan-2026-06-25.md
```

- Claude read-only bounded review is required on this subplan before
  implementation.
- Claude read-only bounded review is required on the Phase 6T result before
  requesting long-run tuning approval.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can P86 expose and guard explicit L1/L2/logZ regularization controls for a future rank-5 training-base tuning diagnostic without running the expensive tuning sweep? |
| Baseline/comparator | Baseline is reviewed Phase 6S: mechanically admissible adaptive rank 5, failed versus reviewed rank 4, with worsening validation and normalizer collapse. |
| Primary criterion | Local implementation checks pass; L1 contributes exactly to the P75 objective regularization; runner payloads and exact guard freeze regularization weights and tuning protocol; no-fit Phase 6T preflight is written. |
| Veto diagnostics | L1 not in config payload; invalid weight accepted; regularization weights silently hard-coded; command drift not guarded; audit cloud used for tuning; ALS route revived; long tuning run executed; unsupported rank-convergence or production claim. |
| Explanatory diagnostics | Planned L1/L2/logZ grid, LR schedule, validation monitor, holdout/audit cloud roles, normalizer diagnostics, trained-core serialization, runtime/memory cap, seed policy. |
| Not concluded | No rank convergence, no best regularization selection, no posterior correctness, no KR closure, no HMC readiness, no LEDH comparison, no GPU performance, no production readiness, and no source-faithful TT-cross training claim. |
| Artifact | Phase 6T preflight JSON and result record. |

## Candidate Phase 6T Diagnostic Protocol To Freeze

The future command should be a single no-grid diagnostic rung that tests whether
explicit L1 regularization changes the rank-5 validation/normalizer pathology
under a conservative LR. It is not a full hyperparameter search.

Candidate future command:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-preflight-2026-06-25.json --target-dimension 36 --fit-rank 5 --training-sample-count 567600 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.000000001 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-diagnostic-2026-06-25.json
```

Candidate tuning grid metadata to record, not execute in this phase:

- `l1_weight`: `0.0`, `1e-10`, `3e-10`, `1e-9`, `3e-9`, `1e-8`
- `learning_rate`: `1e-4`, `3e-4`
- `l2_weight`: hold at `1e-8` initially
- `logz_anchor_weight`: hold at `0.0` initially; escalate to a separate
  normalizer-anchoring diagnostic only if L1/LR does not prevent normalizer
  collapse

## Forbidden Claims / Actions

- Do not run the long Phase 6T diagnostic or any grid/sweep in this phase.
- Do not tune on the audit cloud.
- Do not claim L1 regularization solves rank convergence from local tests,
  validation behavior, or a no-fit preflight.
- Do not change route, basis, domain, target, rank, measure convention, cloud
  policy, or training backend while calling the future run same-route.
- Do not revive ALS training.
- Do not claim production readiness, HMC readiness, LEDH superiority, GPU
  performance, posterior correctness, KR closure, or source-faithful author
  TT-cross training.
- Do not change pass/fail criteria after seeing any diagnostic result.

## Exact Next-Phase Handoff Conditions

A future Phase 6U diagnostic run may be requested only if:

- Claude returns `VERDICT: AGREE` on this subplan, or the subplan converges
  after at most five review loops;
- L1 implementation and runner guard tests pass locally;
- the Phase 6T no-fit preflight JSON has ready status and records the exact
  candidate command;
- the Phase 6T result receives Claude `VERDICT: AGREE`;
- the approval request states the exact command and explicitly preserves
  validation/audit separation and nonclaim boundaries.

Phase 7 correctness/HMC/production work remains blocked unless a later
reviewed convergence ledger passes or precisely reframes rank/degree
convergence.

## Stop Conditions

Stop if:

- Claude requests a material subplan revision that cannot be fixed within five
  review loops;
- L1 cannot be implemented as a scalar TensorFlow penalty without changing the
  training objective contract unexpectedly;
- focused tests fail and the failure is not immediately fixable;
- runner guard fidelity cannot freeze regularization weights;
- no-fit preflight cannot record the tuning protocol and audit non-tuning
  boundary;
- any long fitting command is needed to validate this phase;
- continuing would require new package installation, remote access, GPU
  evidence, or a scientific/product claim outside this phase.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 6T result / close record;
3. draft the Phase 6U exact-run approval request or write a blocker handoff;
4. review the result with Claude for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
