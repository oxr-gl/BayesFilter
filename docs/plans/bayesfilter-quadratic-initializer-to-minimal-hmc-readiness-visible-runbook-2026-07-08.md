# BayesFilter Quadratic Initializer To Minimal HMC Readiness Visible Runbook

Date: 2026-07-08

## Status

`DRAFT_VISIBLE_RUNBOOK`

## Role Contract

Codex is supervisor and executor. Claude review is not used unless the user
explicitly approves external transfer after the prior approval rejection.

This is a visible runbook. Do not use detached supervisors, `codex exec`,
`overnight_gated_launch.sh`, background HMC launches, package installs, commits,
or pushes inside the HMC-readiness phases unless a later explicit human
instruction asks for that.

## Program

Master program:

- `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-master-program-2026-07-08.md`

Execution ledger:

- `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-visible-ledger-2026-07-08.md`

Stop handoff:

- `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-stop-handoff-2026-07-08.md`

## Phase Index

| Phase | Name | Subplan | Required result |
| --- | --- | --- | --- |
| 0 | Coordinate and mass convention audit | `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-phase0-coordinate-audit-subplan-2026-07-08.md` | `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-phase0-coordinate-audit-result-2026-07-08.md` |
| 1 | Initializer artifact smoke | TBD after Phase 0 | TBD |
| 2 | HMC geometry initialization smoke | TBD after Phase 1 | TBD |
| 3 | Bounded mechanics smoke | TBD after Phase 2 | TBD |
| 4 | Closeout | TBD after Phase 3 or blocker | TBD |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the committed quadratic initializer safely feed the minimal SSL-LSTM HMC mechanics path without coordinate mismatch? |
| Baseline/comparator | Existing minimal Phase 5 path and committed initializer API. |
| Primary pass criterion | Phase gates pass in order: coordinate audit, finite/SPD initializer, geometry initialization, bounded mechanics smoke. |
| Veto diagnostics | HMC launch before audit, coordinate mismatch, nonfinite target/gradient, non-SPD mass, unsupported HMC readiness/posterior claim. |
| Explanatory diagnostics | 1.57 heuristic relation, implementation target trajectory, eigen summaries, condition numbers, source labels. |
| Not concluded | HMC readiness, posterior correctness, sampler convergence, default readiness, Zhao-Cui source faithfulness. |

## Phase Execution Rule

Before each phase:

- restate the evidence contract;
- run a skeptical audit;
- stop if the artifact would not answer the phase question.

After each phase:

- run required checks;
- write a result note;
- draft or refresh the next subplan;
- do not promote diagnostics across claim boundaries.

## Human-Required Stop Conditions

Stop if continuing would require:

- HMC runtime before Phase 0/1/2 gates pass;
- GPU/default-policy evidence;
- package installation or network fetch;
- destructive git operations;
- external Claude review after the prior approval rejection;
- changing pass/fail criteria after seeing results.
