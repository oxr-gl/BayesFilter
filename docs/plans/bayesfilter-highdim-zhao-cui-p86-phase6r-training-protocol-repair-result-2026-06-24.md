# P86 Phase 6R Result: Training Protocol Repair

Date: 2026-06-24

Status: `PASS_P86_PHASE6R_TRAINING_PROTOCOL_REPAIR_REVIEWED_BLOCKED_BEFORE_SMOKE_APPROVAL`

## Current Decision

Phase 6R repaired the runner mechanics that allowed a fixed-step rank-5 fit to
finish without convergence evidence.

The runner now supports:

- adaptive-training protocol fields with defaults off;
- validation/holdout monitor records for scheduler use;
- learning-rate reduction on plateau;
- stop reasons that distinguish scheduler plateau stops from max-step
  exhaustion;
- convergence-status payloads that forbid convergence claims when loss is
  still improving at the max step;
- trained-core serialization metadata and optional values for future replay.

No repaired rank-5 fit, training smoke, GPU command, HMC command, LEDH command,
scale stress, or production-promotion command was run in Phase 6R.

## Implementation Summary

Changed:

- `scripts/p86_author_lagrangep_phase5_budget_fit.py`
- `tests/highdim/test_p86_phase5_budget_preflight.py`

The existing reviewed Phase 5/Phase 6 exact commands remain protected because
adaptive controls default to off and the exact-fit guard still rejects command
drift for those historical artifacts.

## Decision Table

| Field | Status |
|---|---|
| Decision | Phase 6R implementation locally passes for tooling repair only. |
| Primary criterion status | Passed locally: helper tests cover protocol defaults, fixed-budget exhaustion classification, LR reduction on plateau, early-stop status, and trained-core serialization payloads. |
| Veto diagnostic status | No ALS route used; no unapproved training command run; no GPU/HMC/LEDH/scale command run; no convergence or production claim made. |
| Main uncertainty | The repaired protocol has not yet been exercised in a training smoke or rank-5 rerun. Runtime behavior still requires exact command approval and review. |
| Next justified action | Send this result to Claude. If reviewed, request exact human approval for a tiny adaptive-training scheduler smoke. |
| What is not concluded | No rank convergence, degree convergence, posterior correctness, KR closure, HMC readiness, LEDH comparison, scale, GPU performance, or production readiness. |

## Evidence Contract Check

| Contract item | Result |
|---|---|
| Question | The runner can now represent plateau-aware training state and trained-core replay metadata without running an unapproved fit. |
| Baseline/comparator | The fixed-step Phase 6 rank-5 protocol stopped at max steps while logged loss was still dropping. |
| Primary criterion | Local tests and compile checks passed. |
| Veto diagnostics | Max-step exhaustion is classified as non-converged unless a scheduler plateau stop occurs; validation holdout is labeled distinct from audit; core serialization metadata is present. |
| Explanatory diagnostics | Future artifacts can record LR history, validation monitor values, LR drops, final logged-loss deltas, and core hashes/values. |
| Not concluded | No repaired rank-5 convergence claim. |

## Local Checks

Commands:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p86_phase5_budget_preflight.py tests/highdim/test_p86_author_lagrangep_fit_smoke_runner.py tests/highdim/test_p86_downstream_author_route_wiring.py tests/highdim/test_p86_lagrangep_mass_integral.py tests/highdim/test_p86_algebraic_measure_contract.py
git diff --check -- scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-training-protocol-repair-subplan-2026-06-24.md
```

Results:

```text
18 passed, 2 warnings
37 passed, 2 warnings
```

## Future Approval Boundary

A future tiny adaptive-training scheduler smoke may now be requested as an
exact command after Claude review and human approval. The command uses a
dedicated `--phase6r-adaptive-smoke` mode and guard; the existing
`--training-base-smoke` guard remains frozen to the earlier one-step smoke.
Any future smoke must be labeled as a training smoke, not rank convergence
evidence.

A future rank-5 rerun must be a separate exact-command request after the smoke
passes and after the convergence diagnostic/replay contract is refreshed.

## Claude Review Status

Claude read-only bounded review returned `VERDICT: AGREE` twice. Iteration 2
reviewed the revision that added the dedicated guarded
`--phase6r-adaptive-smoke` mode.

Review prompt:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the file itself explicitly asks you to inspect a cited line: docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-training-protocol-repair-result-2026-06-24.md. Do not edit, run commands, launch agents, or review the whole repo. Question: Does this Phase 6R result safely record the training-protocol repair after the Phase 6 undertraining diagnosis, preserve the no-unapproved-fit boundary, include adequate local checks for plateau/LR/core-serialization helper behavior, avoid convergence/production claims, and correctly block any scheduler smoke until a dedicated Phase 6R smoke guard and exact approval exist? End with VERDICT: AGREE or VERDICT: REVISE.
```

Summary:

- Claude agreed the result records the post-Phase-6 undertraining diagnosis and
  tooling repair clearly.
- Claude agreed the no-unapproved-fit boundary is preserved.
- Claude agreed the local checks are appropriate for helper-level
  plateau/LR/core-serialization behavior.
- Claude agreed the result avoids convergence and production claims.
- Claude agreed scheduler smoke is correctly blocked pending a dedicated guard
  and exact approval.

Verdict:

```text
VERDICT: AGREE
```

Second review prompt:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the file itself explicitly asks you to inspect a cited line: docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-training-protocol-repair-result-2026-06-24.md. Do not edit, run commands, launch agents, or review the whole repo. Question: This revision adds a dedicated guarded --phase6r-adaptive-smoke mode after the first review and updates local checks to 37 passed. Does the result still safely record the training-protocol repair, avoid convergence/production claims, preserve the no-unapproved-fit boundary, and correctly state that the tiny scheduler smoke is now guarded but still blocked before exact human approval? End with VERDICT: AGREE or VERDICT: REVISE.
```

Second review summary:

- Claude agreed the revised note still records a tooling/protocol repair, not a
  successful retraining result.
- Claude agreed the no-unapproved-fit boundary is preserved.
- Claude agreed convergence and production claims are avoided.
- Claude agreed the updated `37 passed, 2 warnings` local-check record is
  internally consistent.
- Claude agreed the tiny scheduler smoke is now separately guarded but still
  requires exact human approval before use.

Second review verdict:

```text
VERDICT: AGREE
```
