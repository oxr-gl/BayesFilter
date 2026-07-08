# P86 Phase 6U Subplan: Zhao-Cui L1 Tuning Default Policy

Date: 2026-06-25

Status: `REVIEWED_READY_FOR_IMPLEMENTATION`

## Phase Objective

Promote L1 regularization with explicit L1 weight tuning to the default
Zhao-Cui training-base procedure going forward, after the reviewed Phase 6T
diagnostic showed that lower LR plus L1 repaired the rank-5 training pathology.

This phase changes the Zhao-Cui lane policy and runner metadata/tests. It does
not hard-code a single nonzero L1 scalar as the global P75 default and does not
claim production readiness or final rank convergence.

## Entry Conditions Inherited From Previous Phase

- Phase 6T L1 support and no-fit preflight were reviewed:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-result-2026-06-25.md`.
- The approved Phase 6T single diagnostic completed and was reviewed:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-diagnostic-result-2026-06-25.md`.
- Phase 6T rank-5 holdout residual improved to `0.03973471699747935`, versus
  Phase 6S rank-5 `9.553783177487691` and rank-4 `0.22090990401849483`.
- Phase 6T is promising diagnostic evidence only. It is not final rank
  convergence, not production readiness, and not a tuned hyperparameter
  selection ledger.
- Owner directive: L1 regularization with L1 weight tuning should be default
  for Zhao-Cui.

## Skeptical Plan Audit

Potential flaws checked before execution:

- Wrong default target: the default should apply to Zhao-Cui training-base
  procedure, not all P75/P86-independent trainer users.
- Proxy promotion: the Phase 6T residual improvement supports changing the
  default procedure, but it does not close rank convergence or production.
- Missing stop conditions: this phase must stop after policy/code/docs/tests
  and Claude review; no new fitting command is required.
- Unfair comparison: L1 weight tuning must preserve validation/audit
  separation and treat `l1_weight=0` as an allowed comparator arm inside the
  tuning grid.
- Hidden assumption: the selected scalar may vary by rank, basis, dimension,
  LR, seed, and target. Defaulting the procedure is safer than defaulting a
  single fixed scalar.
- Environment mismatch: local checks are CPU-hidden and code/doc only. They
  are not GPU evidence.
- Artifact mismatch: the policy must be visible in governance docs, runner
  payloads, and tests so future agents do not silently return to fixed
  `l1_weight=0` decisions.

Audit result: proceed with policy/metadata/test implementation only. Do not
run new fitting, grid, HMC, LEDH, GPU, or production commands in this phase.

## Required Artifacts

- Phase 6U subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6u-l1-default-policy-subplan-2026-06-25.md`
- Phase 6U result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6u-l1-default-policy-result-2026-06-25.md`
- Phase 6U reset memo:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6u-l1-default-policy-reset-memo-2026-06-25.md`
- Updated governance:
  `AGENTS.md`
- Updated runner/tests:
  `scripts/p86_author_lagrangep_phase5_budget_fit.py`
  `tests/highdim/test_p86_phase5_budget_preflight.py`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md`

## Required Checks / Tests / Reviews

- Add a visible Zhao-Cui default regularization policy payload in the P86
  runner:
  - L1 weight tuning required for future Zhao-Cui training-base decisions;
  - validation holdout may select/veto candidates;
  - audit cloud remains reserved and not used for tuning;
  - `l1_weight=0` remains an allowed comparator arm, not the unreviewed final
    default;
  - selected L1 value requires a reviewed tuning/selection ledger.
- Include the policy payload in future runner-generated Zhao-Cui preflight
  metadata. Do not retroactively edit or regenerate reviewed historical Phase
  6T JSON artifacts solely to add the new policy field.
- Add focused tests asserting the runner policy payload and future Phase 6U+
  preflight path expose the owner-directed default procedure.
- Update `AGENTS.md` with the Zhao-Cui lane default-policy directive.
- Run local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p86_phase5_budget_preflight.py
git diff --check -- AGENTS.md scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6u-l1-default-policy-subplan-2026-06-25.md docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6u-l1-default-policy-result-2026-06-25.md docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6u-l1-default-policy-reset-memo-2026-06-25.md docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md
```

- Claude read-only bounded review is required on this subplan before
  implementation.
- Claude read-only bounded review is required on the result after execution.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the Zhao-Cui lane safely promote L1 regularization with L1 weight tuning to the default training-base procedure without overclaiming Phase 6T as final convergence or production evidence? |
| Baseline/comparator | Reviewed Phase 6S failure, reviewed Phase 6T L1 diagnostic improvement, and owner directive. |
| Primary criterion | Governance, runner metadata, and tests state that Zhao-Cui training-base decisions require L1 weight tuning under validation/audit separation. |
| Veto diagnostics | Global P75 scalar default changed; fixed `l1_weight=1e-9` treated as universally selected; audit cloud used for tuning; Phase 6T overclaimed as production/rank convergence; ALS revived; new fitting command executed. |
| Explanatory diagnostics | Phase 6T improvement ratios, candidate L1 grid, LR grid, validation/audit policy, exact Phase 6U to Phase 6V handoff. |
| Not concluded | No final selected L1 scalar, no rank convergence, no posterior correctness, no HMC readiness, no LEDH comparison, no GPU performance, no production readiness. |
| Artifact | Phase 6U result and reset memo. |

## Forbidden Claims / Actions

- Do not change global `P75TrainableTTConfig.l1_weight` from `0.0`.
- Do not claim `1e-9` is universally optimal.
- Do not claim Phase 6T alone closes rank convergence.
- Do not run new fitting, grid, GPU, HMC, LEDH, or production commands.
- Do not use audit data for tuning.
- Do not revive ALS training.
- Do not claim source-faithful TT-cross training.

## Exact Next-Phase Handoff Conditions

After Phase 6U passes, the next governed phase should be a Phase 6V
convergence-selection subplan that can run only after exact human approval. It
should compare at least:

- `LR=0.0003, l1_weight=0.0`;
- `LR=0.0003, l1_weight=1e-9`;
- one or more nearby L1 values if the reviewed plan authorizes them.

That later phase must write a reviewed selection/convergence ledger before
Phase 7 correctness/HMC/production work can reopen.

## Stop Conditions

Stop if:

- Claude requests a material revision that cannot be fixed within five review
  loops;
- the policy cannot be encoded without changing unrelated P75 defaults;
- local tests fail and are not immediately fixable;
- the policy wording would imply production readiness, final convergence, or
  universal optimality of one L1 scalar;
- implementing the policy requires a new run or approval outside this phase.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the code/test portion of the required local checks;
2. write the Phase 6U result and reset memo;
3. run the required `git diff --check` including all Phase 6U docs and the
   Claude review ledger;
4. review the result with Claude;
5. hand off to a separate reviewed Phase 6V convergence/selection subplan before any
   further fitting approval.
