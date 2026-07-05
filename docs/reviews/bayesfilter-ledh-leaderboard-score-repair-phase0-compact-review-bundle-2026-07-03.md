# Claude Read-Only Review Bundle

Date: 2026-07-03
Review name: `bayesfilter-ledh-leaderboard-score-repair-phase0-compact-review`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

READ-ONLY REVIEW ONLY.  Do not edit files, run commands, launch agents, or
change state.

## Objective

Review only the Phase 0 launch boundary for the LEDH leaderboard score-repair
runbook.

## Self-Contained Phase 0 Evidence Summary

The current LEDH-inclusive leaderboard closeout says:

- no LEDH leaderboard score row is admitted;
- LGSSM `benchmark_lgssm_exact_oracle_m3_T50` is value-only for LEDH;
- fixed spatial SIR is value-only for LEDH;
- actual SV, KSC SV, predator-prey, and generalized SV are blocked for LEDH;
- Contract E LGSSM is route evidence only and is wrong-target evidence for the
  leaderboard LGSSM row.

The master program defines score as:

- the total derivative of the stated leaderboard log likelihood target with
  respect to the stated parameter coordinates.

It says a derivative that treats parameter-dependent LEDH flow, transport,
proposal, reset, or likelihood quantities as constants is:

- a partial derivative;
- wrong for MLE or HMC score claims unless explicitly declared as a different
  diagnostic quantity.

The runbook states:

- Claude is read-only reviewer only;
- Claude must not edit files, run experiments, launch agents, or change state;
- GPU/CUDA/TensorFlow/XLA commands require trusted or escalated execution;
- runtime ranking against frozen non-LEDH rows is not concluded.

Phase 0 subplan states:

- primary criterion: artifacts must state that score means total derivative and
  no LEDH score row is currently admitted;
- veto diagnostics: Contract E reused as leaderboard score, partial derivative
  allowed as score, Claude given execution authority, or GPU runs planned
  without trusted context;
- next handoff: local path/text checks and Claude review must pass before
  Phase 1.

Local checks already run by Codex:

- required path check: `required_paths_ok 12`;
- score-language check: `score_language_ok`;
- review gate shell syntax check: passed;
- `git diff --check` on new plan/review files: passed.

## Exact Paths

- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-master-program-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-visible-gated-execution-runbook-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase0-launch-boundary-score-meaning-subplan-2026-07-03.md`

## Pass Criteria

Return `VERDICT: AGREE` only if all are true:

- score is defined as total derivative of the stated row likelihood target;
- partial derivative is not allowed to be called a score;
- no current LEDH leaderboard score row is claimed admitted;
- Contract E is blocked as same-target leaderboard score evidence;
- Claude remains read-only reviewer;
- GPU/XLA material runs require trusted/escalated execution;
- Phase 0 has stop conditions and next-phase handoff.

Return `VERDICT: REVISE` if any item fails.

## Required Output

Findings first, concise.  End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
