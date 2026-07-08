# P86 Phase 6W Subplan: Same-Policy Rank And Degree Convergence Reentry

Date: 2026-06-25

Status: `REVIEWED_READY_FOR_NO_FIT_IMPLEMENTATION`

## Phase Objective

Reopen Phase 6 rank/degree convergence only under the reviewed Zhao-Cui
training-base default procedure:

```text
L1 regularization with explicit L1 weight tuning is the default Zhao-Cui
training-base procedure.
```

Phase 6W must create a same-policy rank convergence gate after Phase 6V. It
must not treat the old Phase 5 rank-4 artifact as a same-policy lower rung
because Phase 5 used a different optimizer schedule and did not run the
reviewed L1-selection protocol. Phase 6W may first implement only a no-fit
preflight/guard that freezes exact rank-4 lower-rung commands and the reuse
status of the Phase 6V selected rank-5 candidate. Any new fit still requires
exact human approval.

## Entry Conditions Inherited From Previous Phase

- Phase 6S rank convergence remains reviewed blocked:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank-convergence-result-2026-06-25.md`.
- Phase 6U policy is reviewed: L1 tuning is the default Zhao-Cui
  training-base procedure, not a global scalar default:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6u-l1-default-policy-result-2026-06-25.md`.
- Phase 6V selected the rank-5 zero-L1 comparator under the reviewed
  deterministic margin rule:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-convergence-result-2026-06-25.md`.
- The Phase 6V selected rank-5 artifact is:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-rank5-lr3e-4-l1-0-fit-2026-06-25.json`.
- The Phase 6V best observed positive-L1 arm did not clear the required
  margin over zero-L1; this does not revoke L1 tuning as the default
  procedure.
- Phase 7 remains blocked until a later reviewed same-policy rank/degree gate
  passes or is explicitly reframed with owner approval.
- ALS training remains historical/buggy/stale and must not be revived.
- No exact human approval exists yet for any Phase 6W fitting command.

## Skeptical Plan Audit

Potential flaws checked before execution:

- Wrong baseline: the Phase 5 rank-4 artifact is not a same-policy lower rung
  for Phase 6V because LR, train-step policy, adaptive scheduler, and L1
  selection policy differ. Phase 6W must freeze a same-policy rank-4 lower rung
  before making rank convergence claims.
- Proxy-promotion: validation/holdout residuals may pass, select, or veto
  candidates only under the stated contract. They cannot establish posterior
  correctness, HMC readiness, KR closure, production readiness, or
  source-faithful TT-cross training.
- Missing stop conditions: Phase 6W stops before fitting unless a reviewed
  no-fit preflight exists and exact human approval is given for every fit.
- Unfair comparisons: rank-4 lower-rung candidates must use the same target,
  basis, domain, measure convention, optimizer backend, cloud roles, LR
  schedule, validation/audit separation, and L1-selection rule as the selected
  rank-5 candidate, differing only in rank and rank-implied sample floor.
- Hidden assumptions: selecting zero-L1 in Phase 6V means no positive scalar
  cleared the margin in that grid; it does not mean future Zhao-Cui training
  can skip L1 tuning.
- Environment mismatch: planned Phase 6W preflight/checks are CPU-hidden local
  diagnostics. They are not GPU, XLA-GPU, scale, or production evidence.
- Artifact mismatch: a Phase 6W result without exact commands, selected-arm
  rationale, validation/audit separation, nonclaim boundaries, and a Phase 7
  handoff/blocker cannot reopen Phase 7.

Audit result: draft and review a no-fit Phase 6W preflight/guard first. Do not
run any new fit until exact human approval is obtained.

## Required Artifacts

- Phase 6W subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-degree-convergence-subplan-2026-06-25.md`
- Phase 6W no-fit preflight JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-preflight-2026-06-25.json`
- Phase 6W no-fit preflight/guard result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-preflight-guard-result-2026-06-25.md`
- Phase 6W exact-command approval request before any fit:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-approval-request-2026-06-25.md`
- Reserved same-policy rank-4 lower-rung candidate outputs:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-0-fit-2026-06-25.json`
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-3e-10-fit-2026-06-25.json`
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-1e-9-fit-2026-06-25.json`
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-3e-9-fit-2026-06-25.json`
- Phase 6W rank-convergence ledger after approved fits:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-ledger-2026-06-25.json`
- Phase 6W result / close record:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-degree-convergence-result-2026-06-25.md`
- Phase 6W degree convergence executable-vs-blocked handoff note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-degree-convergence-handoff-2026-06-25.md`
- Refreshed Phase 7 correctness bridge subplan or blocker handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase7-correctness-bridge-subplan-2026-06-24.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md`
- Updated visible execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md`

## Required Checks / Tests / Reviews

Before any fit:

- Add a Phase 6W no-fit preflight/guard mode that writes the exact rank-4
  lower-rung protocol and validates the Phase 6V selected rank-5 artifact for
  reuse.
- Freeze same-policy rank-4 lower-rung candidate arms:
  - target dimension `36`;
  - fit rank `4`;
  - training samples `364320` from `max(20 * P_theta, 5000)`;
  - holdout samples `65536`;
  - audit samples `65536`, reserved and not used for tuning;
  - optimizer `training_base_optimizer` / Adam;
  - batch size `4096`;
  - prefit steps `0`;
  - train steps `512`;
  - learning rate `0.0003`;
  - adaptive scheduler:
    `validation_check_every=16`, `plateau_patience=4`,
    `plateau_min_delta=1e-6`, `lr_reduction_factor=0.5`,
    `min_learning_rate=1e-6`, `early_stop_after_lr_drops=4`;
  - `l2_weight=1e-8`;
  - `logz_anchor_weight=0.0`;
  - serialized trained cores;
  - cloud roles separated exactly as Phase 6V.
- Rank-4 candidate L1 grid:
  - `l1_weight=0.0`;
  - `l1_weight=3e-10`;
  - `l1_weight=1e-9`;
  - `l1_weight=3e-9`.
- Rank-4 L1 selection rule must match Phase 6V:
  after vetoes, the lowest final holdout residual wins only if it improves
  over the rank-4 `l1_weight=0.0` comparator by at least
  `max(0.005, 0.05 * rank4_zero_l1_holdout)`; otherwise select the rank-4
  zero-L1 comparator if it passes all vetoes.
- Adjacent rank-stability criterion must be frozen in the no-fit preflight:
  after rank-4 selection and Phase 6V rank-5 reuse validation, rank
  convergence passes only if
  `abs(rank5_selected_holdout - rank4_selected_holdout) <= max(0.005, 0.05 * rank4_selected_holdout)`.
  A larger rank-5 improvement or regression means rank convergence is not yet
  established; it may justify a later reviewed rank-6 or model-selection
  diagnostic, but Phase 6W itself must not treat a large improvement as a
  pass.
- Preserve the audit cloud as reserved; it may not select or tune L1.
- Reuse the Phase 6V selected rank-5 artifact only if protocol equivalence
  passes for route, target, basis, domain, measure convention, optimizer,
  scheduler, cloud roles, selected L1 rule, serialization, finite diagnostics,
  runtime/memory, and nonclaim boundaries.
- Add focused tests for:
  - Phase 6W preflight command and candidate commands are frozen;
  - rank-4 parameter count/sample floor equals the reviewed formula;
  - Phase 6V selected rank-5 reuse validation rejects drift in artifact path,
    selected L1, route, scheduler, cloud roles, finite statuses, or
    serialization;
  - exact guards reject changes in output path, rank, samples, LR,
    L1/L2/logZ weights, scheduler, cloud seeds, and serialization;
  - Phase 6W metadata records that Phase 5 rank 4 is historical context, not a
    same-policy lower rung.
- Run CPU-hidden local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p86_phase5_budget_preflight.py
git diff --check -- scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-degree-convergence-subplan-2026-06-25.md docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-preflight-2026-06-25.json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-preflight-guard-result-2026-06-25.md docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-approval-request-2026-06-25.md docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-degree-convergence-handoff-2026-06-25.md docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-degree-convergence-result-2026-06-25.md docs/plans/bayesfilter-highdim-zhao-cui-p86-phase7-correctness-bridge-subplan-2026-06-24.md docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md
```

- Claude read-only bounded review is required on this subplan before
  implementation.
- Claude read-only bounded review is required on the no-fit preflight/guard
  result before requesting exact fitting approval.
- After approved fits complete, Claude read-only bounded review is required on
  the Phase 6W result before Phase 7 can be reopened.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Under the reviewed Zhao-Cui L1-tuning default procedure, do same-policy rank-4 and rank-5 author Lagrangep candidates pass the Phase 6 rank-convergence gate, and is degree convergence executable or explicitly blocked? |
| Baseline/comparator | Lower rung: new Phase 6W same-policy rank-4 L1-selection result. Stronger rung: Phase 6V selected rank-5 artifact if reuse validation passes. Phase 5 rank 4 is historical context only. |
| Primary criterion | Rank convergence can pass only if both rungs pass mechanical vetoes, rank-4 L1 selection follows the same deterministic Phase 6V rule, Phase 6V selected rank 5 passes reuse validation, and adjacent holdout stability satisfies `abs(rank5_selected_holdout - rank4_selected_holdout) <= max(0.005, 0.05 * rank4_selected_holdout)`. A larger rank-5 improvement or regression blocks same-policy rank convergence rather than passing it. Degree convergence can pass only if a reviewed configurable-basis execution path exists; otherwise it remains blocked/out of scope. |
| Veto diagnostics | Exact-command drift, missing same-policy lower rung, mismatched route/basis/domain/measure/backend/cloud roles/scheduler, audit tuning, nonfinite diagnostics, fallback route, inactive normalizer, runtime/memory breach, using Phase 5 as same-policy lower rung, unsupported Phase 7/production/HMC/source-faithful TT-cross claim, or missing Claude/human approval boundary. |
| Explanatory diagnostics | Rank deltas, selected L1 per rung, fit/holdout residuals, normalizers, validation traces, best/final validation ratios, runtime/memory, and whether positive L1 clears any predeclared margin. |
| Not concluded | No posterior correctness, KR closure, HMC readiness, LEDH comparison, GPU performance, d50/d100 scale claim, production readiness, or source-faithful author TT-cross training claim. |
| Artifact | Phase 6W preflight, candidate JSON outputs, rank-convergence ledger, result record, Claude review ledger, and execution ledger. |

## Forbidden Claims / Actions

- Do not run any Phase 6W fit before exact human approval of the frozen
  commands.
- Do not use Phase 5 rank 4 as the same-policy lower rung.
- Do not tune on the audit cloud.
- Do not use audit-cloud results to select L1 or rank.
- Do not revive ALS training.
- Do not change route, basis, domain, target, measure convention, cloud roles,
  optimizer backend, scheduler, or output paths while calling arms comparable.
- Do not skip L1 tuning because Phase 6V selected zero-L1.
- Do not declare a universal L1 scalar default.
- Do not claim Phase 7 is open from the no-fit preflight.
- Do not claim production readiness, posterior correctness, HMC readiness, KR
  closure, LEDH superiority, GPU performance, d50/d100 scaling, or
  source-faithful author TT-cross training.

## Exact Next-Phase Handoff Conditions

Phase 7 may be refreshed only if:

- the Phase 6W no-fit preflight/guard passes local checks;
- Claude agrees the Phase 6W no-fit implementation/result is boundary-safe;
- the user approves exact Phase 6W fitting commands before execution;
- all approved candidate fits complete or are recorded with precise blockers;
- the Phase 6W ledger selects same-policy rank-4 and rank-5 rungs without
  audit tuning;
- rank convergence passes the predeclared primary criterion and no veto fires;
- degree convergence is either resolved under a reviewed configurable-basis
  path or explicitly carried as a bounded blocker;
- Claude agrees the Phase 6W result avoids production/HMC/source-faithful
  TT-cross overclaims.

If rank convergence remains blocked, Phase 7 must remain blocked unless the
owner explicitly reframes the gate.

## Stop Conditions

Stop if:

- Claude requests a material subplan or result revision that cannot be fixed
  within five review loops;
- the no-fit preflight/guard cannot freeze candidate commands exactly;
- the Phase 6V selected rank-5 artifact fails reuse validation;
- exact human approval for new fit commands is absent;
- any fit exceeds approved runtime/memory or produces nonfinite diagnostics;
- audit-cloud data would be needed for tuning or selection;
- results require changing criteria after seeing outputs;
- continuing would require GPU evidence, HMC, LEDH, package installation,
  remote access, default-policy change, production promotion, or a scientific
  claim outside this phase.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 6W result or blocker;
3. write the exact Phase 6W degree convergence executable-vs-blocked handoff
   note;
4. draft or refresh the Phase 7 correctness bridge subplan or blocker handoff;
5. review the next subplan for consistency, correctness, feasibility,
   artifact coverage, boundary safety, and approval needs;
6. request Claude read-only bounded review of material results and repair
   visibly if review finds a fixable problem.

## Subplan Review History

Claude read-only bounded review converged after two iterations:

- Iteration 1 returned `VERDICT: REVISE` because the degree-convergence
  executable-vs-blocked artifact was under-specified and the explicit final
  diff-check list omitted Phase 6W preflight/approval artifacts.
- Codex patched the subplan to add the exact degree handoff path,
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-degree-convergence-handoff-2026-06-25.md`,
  pin the refreshed Phase 7 subplan path, and include Phase 6W
  preflight/approval/result/handoff artifacts in the final diff-check list.
- Iteration 2 returned `VERDICT: AGREE`.

Current reviewed gate:

```text
REVIEWED_READY_FOR_NO_FIT_IMPLEMENTATION
```
