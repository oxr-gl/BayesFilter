# P75 Phase 4 Result: Bounded Pilot Run

metadata_date: 2026-06-17
status: PHASE4_TARGET_SMOKE_EXECUTED_BLOCKED_CLAUDE_AGREE_READY_FOR_PHASE5
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase4-bounded-pilot-run-subplan-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-result-2026-06-17.md
next_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase5-result-decision-subplan-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | Can the P75 stochastic density trainer run on real fixed-variant author-SIR step-1 fresh batches with finite objective/gradient and independent fresh-audit diagnostics? |
| Exact baseline/comparator | P73 Phase 5/6 blocked diagnostic as historical failed-scale comparator; no same-schedule ALS superiority claim. |
| Primary criterion | Partially satisfied for execution mechanics only: the tiny target smoke completed two finite optimizer steps and wrote a manifest.  The diagnostic gate blocked on the fresh audit line gate. |
| Veto diagnostics | `audit_line_veto` fired.  The trained density remained at the defensive floor with `rho_min=rho_max=1e-8`, `normalizer=1e-8`, and gradient norms about `8.66e-9`. |
| Explanatory only | Loss trajectory, cross-entropy, gradient norm, parameter delta, runtime, and residual magnitudes. |
| What is not concluded | No lower-gate repair, validation readiness, HMC readiness, scaling claim, source-faithful adaptive Zhao--Cui parity, final rank/sample policy, or degree/rank promotion. |
| Artifact preserving result | `docs/plans/bayesfilter-highdim-zhao-cui-p75-target-smoke-2026-06-17.json`, this result note, ledgers, Claude review. |

## Skeptical Plan Audit

Phase 4 passed the skeptical audit before execution because Phase 3 local
checks and Claude review had converged, the real target smoke was tiny and
CPU-hidden, and the evidence contract made audit vetoes blocking rather than
promotional.

## Command

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --target-pilot --degree 1 --rank 1 --batch-size 16 --batches 2 --max-seconds 180 --output docs/plans/bayesfilter-highdim-zhao-cui-p75-target-smoke-2026-06-17.json
```

The command exited nonzero because the manifest gate summary had
`overall_status=block`, but it completed the requested two optimizer batches
and wrote the result JSON.

## Result Summary

Target smoke manifest:

- `status=P75_TARGET_PILOT_COMPLETED`;
- `phase4_target_pilot_executed=true`;
- `completed_batches=2`;
- `stop_reason=max_batches_completed`;
- `audit_status=block`;
- `audit_reasons=["audit_line_veto"]`;
- `p73_b_optimizer_status=P73_B_OPTIMIZER_BLOCKED_NONLINEAR_OBJECTIVE_NOT_IMPLEMENTED`.

Final objective terms:

- `normalizer=1e-8`;
- `rho_min=1e-8`;
- `rho_max=1e-8`;
- `log_normalizer=-18.420680743952367`;
- `weighted_empirical_cross_entropy=18.420680743952364`;
- `total_loss=1.8731158218926995e-09`;
- `gradient_norm=8.65590982995174e-09`.

Fresh audit diagnostics:

- holdout `rms_relative=1.0`, `max_relative=3.9999999809592586`;
- replay `rms_relative=1.0`, `max_relative=3.113086321753927`;
- line gate `status=block`;
- line gate reasons:
  - `line_max_residual_veto`;
  - `line_rms_residual_veto`;
- line target scale `0.020176609718332184`;
- line residual RMS `13.433258339581773`;
- line residual max absolute `48.138132786642366`;
- line prediction max absolute `2.83890490234991e-48`.

## Interpretation

The target-pilot command surface now reaches real author-SIR step-1 batches and
executes finite TensorFlow optimization steps.  That is useful engineering
evidence.

The scientific/numerical diagnostic is blocked.  The fitted model did not
learn a meaningful square-root TT component on the tiny target smoke.  The
density is dominated by the defensive term \(\tau q_0\), so the normalized
pilot density is essentially the defensive reference density rather than the
fresh target.  In this regime the empirical cross-entropy and `log Z` nearly
cancel and the gradients are too small to move the model meaningfully.

Under the Phase 4 evidence contract, the degree 2/rank 4/batch 1024/up-to-500
run is not launched from this result.  The tiny smoke exposed a blocking
objective/initialization/capacity issue that should be decided in Phase 5
before spending a larger run budget.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Stop before the larger pilot and enter Phase 5 decision analysis | Execution mechanics partially pass: two finite steps and JSON manifest exist | Blocked by `audit_line_veto`; density floor collapse observed | Whether the collapse is caused mainly by initialization scale, degree/rank capacity, objective scaling, defensive weight, or too-small training budget | Analyze the collapse mode and decide whether to patch initialization/objective scaling before any larger pilot | No lower-gate repair, no validation/HMC readiness, no scaling claim, no source-faithful Zhao--Cui claim |

## Local Checks

Passed after the Phase 3 orientation/accounting repair and before the target
smoke:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p75_stochastic_density_training.py
```

Result:

```text
10 passed, 2 warnings
```

Passed:

```text
git diff --check -- scripts/p75_stochastic_density_training_pilot.py tests/highdim/test_p75_stochastic_density_training.py docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-claude-review-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-target-smoke-2026-06-17.json
```

Result:

```text
no output
```

## Claude Review

Claude reviewed the Phase 4 result and Phase 5 subplan and returned
`VERDICT: AGREE`.

Claude agreed that:

- the Phase 4 interpretation is consistent with the JSON;
- execution mechanics partially passed, but the numerical/scientific
  diagnostic is blocked;
- the defensive-floor-collapse reading is supported by
  `rho_min=rho_max=normalizer=1e-8`, tiny gradients, and near-zero line
  predictions;
- stopping before the larger degree 2/rank 4/batch 1024 run is correct under
  the evidence contract;
- the Phase 5 subplan is bounded and safe.

Residual risk: the artifact shows collapse symptoms but does not isolate root
cause among initialization scale, objective scaling, capacity, sample budget,
or target-generation issues.
