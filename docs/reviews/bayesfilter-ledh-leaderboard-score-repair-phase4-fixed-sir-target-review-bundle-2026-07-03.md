# Claude Read-Only Review Bundle

Date: 2026-07-03
Review name: `bayesfilter-ledh-leaderboard-score-repair-phase4-fixed-sir-target`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

READ-ONLY REVIEW ONLY.  Do not edit files, run commands, launch agents, or
change state.

Claude is not execution authority and cannot approve scientific-claim,
runtime, GPU, model-file, product, funding, or human-boundary crossings.

## Objective

Review the Phase 4 fixed SIR target classification.

The result says:

- fixed spatial SIR main row is `no_free_theta_value_only`;
- parameterized SIR log-scale row is scoped component evidence only;
- no LEDH SIR score row is admitted;
- Phase 5 should exclude fixed SIR from score repair.

## Artifacts To Inspect

Inspect only these bounded local paths:

- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase4-fixed-sir-score-target-result-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase5-nonlinear-adapter-admission-subplan-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-visible-execution-ledger-2026-07-03.md`
- `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py`
- `bayesfilter/highdim/models.py`
- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-ledger-2026-07-03.json`

Relevant anchors recorded in the result:

- fixed SIR dataset has `truth_theta_coordinate = "no_free_theta"` and
  `truth_theta = []` in
  `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py:214-225`;
- `SpatialSIRSSM.parameter_dim()` returns `0` in
  `bayesfilter/highdim/models.py:705-706`;
- parameterized SIR has `sir_log_scale_theta` and three parameters in
  `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py:228-255`
  and `bayesfilter/highdim/models.py:935-945`;
- current LEDH-inclusive leaderboard records fixed SIR LEDH as
  `executed_value_only_score_blocked` and parameterized SIR LEDH as
  `scoped_component_status_only`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the fixed spatial SIR main row have a score target, or is it value-only by definition? |
| Baseline/comparator | Current July 3 fixed SIR main row and parameterized SIR scoped component row. |
| Primary criterion | If fixed SIR has no free theta and parameterized SIR is scoped only, Phase 4 must classify fixed SIR as value-only and admit no LEDH score. |
| Veto diagnostics | Invented parameterization for fixed SIR, scoped parameterized score promoted to full observed-data score, any LEDH SIR score admitted, Phase 5 reintroduces fixed SIR as score target. |
| Not concluded | No future parameterized full-row target decision, no SIR HMC readiness, no Zhao-Cui source-faithfulness claim. |

## Local Checks Already Run

- Phase 4 text check passed.
- SIR row JSON status check passed.
- `git diff --check` passed for Phase 4 result, Phase 5 subplan, and ledger.

## Pass Criteria

Return `VERDICT: AGREE` only if all are true:

- fixed SIR main row is correctly classified as no-free-theta value-only;
- parameterized SIR log-scale row is kept scoped and not promoted;
- no LEDH SIR score row is admitted;
- Phase 5 correctly excludes fixed SIR from score repair;
- the Phase 3 LGSSM blocker is preserved.

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
