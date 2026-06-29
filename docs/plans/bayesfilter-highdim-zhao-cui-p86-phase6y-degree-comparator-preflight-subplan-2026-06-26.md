# P86 Phase 6Y Subplan: Degree Comparator Preflight

Date: 2026-06-26

Status: `DRAFT_PENDING_CLAUDE_REVIEW`

## Phase Objective

Implement a no-fit degree-comparator preflight for P86 after Phase 6W rank
convergence passed and Phase 6X repaired configurable Lagrangep basis setup.

The phase objective is to freeze exact degree-comparator commands and
artifacts without running degree fits. The preflight must make basis order and
element count explicit setup-static fields, classify non-default bases as
`extension_or_invention`, and preserve all rank/degree/Phase 7 boundaries.

## Entry Conditions Inherited From The Previous Phase

- Phase 6W same-policy rank convergence passed:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-degree-convergence-result-2026-06-26.md`.
- Phase 6W selected the rank-4 zero-L1 comparator under the reviewed
  deterministic margin rule.
- Phase 6V selected the rank-5 zero-L1 comparator under the reviewed
  deterministic margin rule.
- Phase 6X configurable-basis runner repair passed focused local checks:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6x-configurable-basis-runner-repair-result-2026-06-26.md`.
- Default author setup remains `Lagrangep(4,8)` plus `AlgebraicMapping(1)`.
- Non-default Lagrangep order/elements are setup comparator extensions, not
  source-faithful author routes.
- L1 tuning remains the default Zhao-Cui training-base procedure.
- ALS training remains historical/buggy/stale and must not be revived.
- No exact degree-comparator fit review agreement exists yet.

## Skeptical Plan Audit

Potential flaws to check before implementation:

- Wrong baseline: the author default `Lagrangep(4,8)` is the reference degree
  setup. Any `order != 4` or `num_elems != 8` comparator must be labeled as an
  extension.
- Proxy-promotion: validation or holdout residuals from future degree fits can
  select or veto under a reviewed rule only; they do not establish posterior
  correctness, HMC readiness, KR closure, or production readiness.
- Missing stop conditions: this phase is no-fit. It stops after writing and
  testing the preflight artifact unless later Claude agreement is recorded for
  the exact frozen fit commands.
- Unfair comparison: degree arms must keep target, dimension, rank, optimizer,
  train/holdout/audit cloud roles, L1 procedure, LR schedule, seeds, and
  serialization policy comparable except for the declared basis setup and
  sample floor implied by the basis dimension.
- Hidden assumption: an order-3 comparator is a lower-degree diagnostic, not
  evidence that order 4 is source-faithful enough for production.
- Artifact mismatch: a preflight result must preserve Phase 7 as blocked
  until a reviewed degree result exists or the owner explicitly reframes the
  degree gate.

If this audit fails during implementation, patch this subplan or write a
blocker result before running commands.

## Required Artifacts

- Phase 6Y subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-subplan-2026-06-26.md`
- Phase 6Y no-fit preflight JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-2026-06-26.json`
- Phase 6Y no-fit preflight/guard result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-result-2026-06-26.md`
- Reserved future order-3 lower-degree comparator output path. This file must
  not be created in Phase 6Y; the path is frozen only inside the no-fit
  preflight JSON and later Claude-agreement execution handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-26.json`
- Reserved default-order reference artifact:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-0-fit-2026-06-25.json`
- Refreshed degree handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-degree-convergence-handoff-2026-06-25.md`
- Updated visible execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md`

## Required Checks / Tests / Reviews

Before implementation:

- Claude one-path read-only bounded review of this subplan must return
  `VERDICT: AGREE`.

Implementation requirements:

- Add a no-fit CLI preflight mode for the degree comparator.
- Freeze `basis_order=3`, `basis_num_elems=8` as the first lower-degree
  comparator arm unless this subplan is visibly patched and reviewed again.
- Keep the default Phase 6W selected rank-4 zero-L1 artifact as the reference
  comparator.
- Compute order-3 basis dimension as `25`.
- Compute rank-4 TT parameter count as `13800`.
- Compute minimum training samples as `276000`.
- Preserve holdout samples `65536` and audit samples `65536`.
- Preserve training-base Adam, learning rate `0.0003`, L2 `1e-8`, logZ anchor
  `0.0`, adaptive scheduler, serialized cores, and validation/audit separation
  used by Phase 6W.
- Freeze exact seeds:
  - run seed `8608`;
  - train prior/process seeds `8303` / `8403`;
  - holdout prior/process seeds `9303` / `9403`;
  - audit prior/process seeds `9313` / `9503`.
- Freeze runtime envelope `max_seconds=7200`.
- Freeze memory envelope `memory_cap_mib=12288`.
- Freeze exact output paths and candidate command strings in the preflight
  artifact.
- Add exact guards for basis order/elements and command/path drift.
- Add focused tests covering:
  - no-fit Phase 6Y preflight command and candidate command;
  - basis classification for order-3 as `extension_or_invention`;
  - parameter count and sample floor;
  - default-order reference artifact validation;
  - exact guard rejection for basis, output, rank, samples, LR, L1/L2/logZ,
    scheduler, seeds, serialization, runtime, and memory drift against the
    exact values frozen above;
  - no Phase 7, HMC, production, or source-faithful non-default claim leakage.

Required local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile bayesfilter/highdim/bases.py bayesfilter/highdim/__init__.py scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p85_configurable_basis_domain.py tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p85_configurable_basis_domain.py tests/highdim/test_p86_phase5_budget_preflight.py
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-2026-06-26.json
git diff --check -- bayesfilter/highdim/bases.py bayesfilter/highdim/__init__.py scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p85_configurable_basis_domain.py tests/highdim/test_p86_phase5_budget_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-subplan-2026-06-26.md docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-2026-06-26.json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-result-2026-06-26.md docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-degree-convergence-handoff-2026-06-25.md docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md
```

After implementation:

- Write the Phase 6Y no-fit result/close record.
- Refresh the next handoff.
- Run Claude one-path read-only bounded review of the Phase 6Y result.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can P86 freeze an executable, no-fit lower-degree Lagrangep comparator preflight without crossing the degree-fit execution boundary? |
| Baseline/comparator | Reference: reviewed Phase 6W selected rank-4 zero-L1 `Lagrangep(4,8)` artifact. Candidate: reserved future lower-degree `Lagrangep(3,8)` rank-4 zero-L1 comparator output path. |
| Primary criterion | Preflight passes only if exact commands and artifacts are frozen, basis setup classification is correct, parameter/sample budgets match the configured basis dimension, default reference validation passes, no fit executes, and all local checks pass. |
| Veto diagnostics | Wrong basis classification, command drift, missing reference artifact, using audit cloud for tuning, ALS revival, nonfinite planned budgets, runtime/memory envelope missing, fit execution before Claude agreement on the frozen command, or unsupported Phase 7/production/HMC/source-faithful claim. |
| Explanatory diagnostics | Basis dimension, TT parameter count, sample floor, command fidelity, selected reference residuals, and planned scheduler settings. |
| Not concluded | No degree convergence, no rank re-litigation, no posterior correctness, no KR closure, no HMC readiness, no GPU performance, no production readiness, and no source-faithful claim for the order-3 comparator. |
| Artifact | Phase 6Y preflight JSON and Phase 6Y result/close record. |

## Forbidden Claims / Actions

- Do not run the degree-comparator fit during this phase.
- Do not describe order-3 or other non-default bases as source-faithful.
- Do not tune on the audit cloud.
- Do not revive ALS training.
- Do not change the L1 tuning default procedure.
- Do not reopen Phase 7 from a no-fit preflight.
- Do not claim degree convergence, production readiness, HMC readiness, KR
  closure, LEDH superiority, GPU performance, d50/d100 scale, or posterior
  correctness.

## Exact Next-Phase Handoff Conditions

The following phase may execute the exact frozen degree-fit command only if:

- Claude agrees this subplan is boundary-safe;
- Phase 6Y no-fit implementation passes local checks;
- the Phase 6Y preflight JSON freezes exact commands and artifacts;
- Claude agrees the Phase 6Y result/close record is accurate;
- the execution handoff quotes the exact frozen commands and output paths.

## Stop Conditions

Stop and write a blocker result if:

- default basis classification drifts from `source_faithful`;
- non-default basis classification drifts from `extension_or_invention`;
- the reference Phase 6W artifact is missing or fails validation;
- exact command/path/basis guard tests fail;
- local checks fail and the failure is not a small fixable implementation bug;
- Claude returns `VERDICT: REVISE` and the issue cannot be fixed within five
  focused review loops;
- any command would execute a degree fit before Claude agreement is recorded
  for the exact frozen command.
