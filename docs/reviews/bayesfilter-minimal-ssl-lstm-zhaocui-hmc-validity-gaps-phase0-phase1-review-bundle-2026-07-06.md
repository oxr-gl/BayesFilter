# Review Bundle: Minimal SSL-LSTM Zhao-Cui HMC Validity Gaps Phase 0/1

Date: 2026-07-06

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex is supervisor and executor. Claude is read-only reviewer only.

## Review Scope

Review the compact Phase 0/1 plan summary below for consistency, correctness,
feasibility, artifact coverage, and boundary safety. Do not inspect the whole
repository.

Primary artifacts:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-master-program-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-visible-gated-execution-runbook-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase0-governance-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase1-scalar-oracle-design-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase6-closeout-result-2026-07-06.md`

Context:

- The completed `hmc-next` program established internal adapter mechanics,
  CPU-hidden regression, GPU/XLA launch smoke, and a short GPU/XLA hard-veto
  diagnostic ladder.
- It did not establish posterior correctness, HMC convergence, R-hat/ESS,
  ranking, source-faithful parity, default readiness, production readiness,
  public API/package readiness, or LEDH evidence.
- The new program should start with a scalar posterior/reference oracle design,
  not a longer HMC run.

## Evidence Contract To Audit

| Field | Contract |
| --- | --- |
| Question | Can the minimal scalar `zhaocui_fixed` HMC path be moved from launch/hard-veto evidence toward posterior/sampler validity evidence without overstating claims? |
| Baseline/comparator | Completed `hmc-next` closeout and Phase 5 GPU/XLA hard-veto artifact. |
| Primary pass criterion | Phase 0 correctly stages governance and review; Phase 1 designs an independent scalar posterior/reference oracle and exact Phase 2 implementation handoff without running long HMC. |
| Veto diagnostics | Wrong baseline, proxy metrics promoted to validity, missing stop condition, unreviewed long/GPU runtime, unsupported source-faithful claim, unsupported convergence/posterior/ranking/readiness claim, invalid artifact, or review nonconvergence. |
| Explanatory diagnostics | Artifact inventory, review status, import/compile checks, proposed oracle grid/domain/tolerance design, and dirty-worktree summary. |
| Not concluded | HMC convergence, posterior correctness, R-hat/ESS, ranking/superiority, source-faithful parity, default readiness, production readiness, public API/package readiness, or LEDH evidence. |

## Phase 0 Summary

Objective: establish the new master program, visible runbook, review path,
ledger, stop handoff, and Phase 1 oracle-design gate.

Phase 0 may not:

- run HMC/GPU/XLA/long diagnostics;
- claim posterior correctness or convergence;
- make source-faithful Zhao-Cui claims;
- change public API/default policy;
- edit model files or install packages.

Required checks:

- predecessor closeout/reset/Phase 5 artifact existence;
- compile/import check for existing minimal target/harness/tests;
- claim-boundary scan over new plan/review files;
- `git diff --check`;
- material read-only review.

## Phase 1 Summary

Objective: design an independent scalar posterior/reference oracle for the
minimal `zhaocui_fixed` target.

The Phase 1 design must:

- name the target quantity separately from the reference approximation and
  future HMC comparison surface;
- avoid circularity with the HMC runtime path;
- predeclare grid/domain or other reference strategy;
- predeclare tolerances as reviewed hypotheses unless derived/measured;
- include mass/domain checks and nonfinite checks;
- produce an exact Phase 2 implementation subplan.

Phase 1 is design only. It does not establish posterior correctness.

## Specific Review Questions

1. Is the baseline correct, or is any older CPU-only ladder being used as the
   immediate validity baseline by mistake?
2. Does the plan promote Phase 5 hard-veto/acceptance/runtime/sample evidence
   into posterior correctness, convergence, ranking, or readiness?
3. Does Phase 1 correctly prioritize scalar oracle design before longer HMC?
4. Are stop conditions and next-phase handoff conditions sufficient?
5. Are material numbers/tolerances treated as hypotheses unless provenance is
   provided?
6. Does the plan avoid source-faithful Zhao-Cui language without anchors?
7. Does the plan avoid public API/default-policy/model-file/GPU/long-runtime
   boundaries in Phase 0/1?
8. Are artifacts sufficient to recover after interruption?

Findings first. End with exactly:

VERDICT: AGREE

or

VERDICT: REVISE
