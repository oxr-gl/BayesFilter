# P86 Phase 6U Result: Zhao-Cui L1 Tuning Default Policy

Date: 2026-06-25

Status: `P86_PHASE6U_L1_TUNING_DEFAULT_POLICY_REVIEWED`

## Current Decision

L1 regularization with explicit L1 weight tuning is now the default Zhao-Cui
training-base procedure going forward.

This is a Zhao-Cui lane policy, not a global P75 scalar default. The global
`DEFAULT_L1_WEIGHT` remains `0.0`, and `l1_weight=0.0` remains an allowed
comparator arm inside reviewed tuning grids. Future Zhao-Cui training-base
decisions must use a reviewed L1 tuning/selection protocol before supporting
rank-convergence, HMC, production, or scientific claims.

## Decision Table

| Field | Status |
|---|---|
| Decision | Promote L1 weight tuning to the default Zhao-Cui training-base procedure. |
| Primary criterion status | Passed locally: governance, runner metadata, and tests encode the owner-directed default procedure. |
| Veto diagnostic status | No global P75 scalar drift; no new fitting; no audit tuning; no ALS revival; no Phase 6T overclaim. |
| Main uncertainty | No final selected L1 scalar exists yet; Phase 6V still needs a reviewed convergence/selection subplan and exact-run approvals. |
| Next justified action | Draft Phase 6V convergence/selection subplan comparing `LR=0.0003, l1=0.0` against `LR=0.0003, l1=1e-9` and nearby reviewed arms. |
| What is not being concluded | No final rank convergence, no posterior correctness, no HMC readiness, no LEDH comparison, no GPU performance, no production readiness, and no source-faithful TT-cross training claim. |

## Evidence Contract Check

| Field | Result |
|---|---|
| Question | Can the Zhao-Cui lane safely promote L1 regularization with L1 weight tuning to the default training-base procedure without overclaiming Phase 6T? |
| Baseline/comparator | Reviewed Phase 6S rank-5 failure, reviewed Phase 6T L1 diagnostic improvement, and owner directive. |
| Primary criterion | Passed: `AGENTS.md`, runner policy payloads, and focused tests state that Zhao-Cui training-base decisions require L1 tuning under validation/audit separation. |
| Veto diagnostics | Passed: global P75 scalar default remains `0.0`; no new fitting/grid/GPU/HMC/LEDH command was run; audit remains reserved; ALS remains historical/stale. |
| Explanatory diagnostics | Phase 6T remains promising single-diagnostic evidence; future selected scalar requires a reviewed tuning/selection ledger. |
| Not concluded | No selected scalar, no final convergence, and no production readiness. |
| Artifact | This result and reset memo. |

## Implementation Summary

- Added Zhao-Cui regularization default policy constants to
  `scripts/p86_author_lagrangep_phase5_budget_fit.py`.
- Added `_zhao_cui_regularization_default_policy()` with:
  - default procedure:
    `tune_l1_weight_under_reviewed_validation_audit_split`;
  - scope:
    `zhao_cui_training_base_route_only_not_global_p75_default`;
  - `global_p75_l1_scalar_default`: `0.0`;
  - allowed comparator arm: `0.0`;
  - candidate L1 grid:
    `0.0`, `1e-10`, `3e-10`, `1e-9`, `3e-9`, `1e-8`;
  - validation/audit separation;
  - selection status requiring a reviewed tuning/selection ledger.
- Included the policy payload in runner-generated preflight metadata and
  training config payloads.
- Updated `AGENTS.md` with the Zhao-Cui training regularization default.
- Added tests proving the policy is procedure-level and the global scalar
  default remains zero.

## Local Checks

Commands:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p86_phase5_budget_preflight.py
git diff --check -- AGENTS.md scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6u-l1-default-policy-subplan-2026-06-25.md docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md
```

Results:

```text
py_compile passed
26 passed, 2 warnings
initial git diff --check passed
final doc-inclusive git diff --check passed
```

## Boundary Notes

- No Phase 6T JSON was retroactively regenerated solely for this policy.
- No new fitting, grid, GPU, HMC, LEDH, d=50/d=100, or production command was
  run.
- The Phase 6T diagnostic remains promising evidence only.
- `l1_weight=1e-9` is not declared universally optimal.

## Next Handoff

Phase 6V should be a reviewed convergence/selection subplan. It should compare
at least:

- `LR=0.0003, l1_weight=0.0`;
- `LR=0.0003, l1_weight=1e-9`;
- nearby L1 values only if the reviewed Phase 6V plan authorizes them.

Phase 7 remains blocked until a reviewed selection/convergence ledger supports
reopening it.

## Claude Review Status

Claude read-only bounded review returned `VERDICT: AGREE`.

Review prompt:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the file itself explicitly asks you to inspect a cited line: docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6u-l1-default-policy-result-2026-06-25.md. Do not edit, run commands, launch agents, or review the whole repo. Question: Does this Phase 6U result safely implement the reviewed policy that L1 regularization with L1 weight tuning is the default Zhao-Cui training-base procedure, while preserving that this is not a global P75 scalar default, not a final selected L1 scalar, not rank convergence or production readiness, and that no new fitting/audit tuning/ALS revival occurred? End with VERDICT: AGREE or VERDICT: REVISE.
```

Summary:

- Claude agreed the default is procedural, not a global scalar default.
- Claude agreed `DEFAULT_L1_WEIGHT=0.0` and `l1_weight=0.0` as comparator arm
  are preserved.
- Claude agreed no final selected L1 scalar, rank convergence, production
  readiness, new fitting, audit tuning, or ALS revival is claimed.
- Claude noted the status was review pending before this patch, which is now
  resolved.

Verdict:

```text
VERDICT: AGREE
```
