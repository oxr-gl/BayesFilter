# Phase P0 Subplan: Accuracy-Time Leaderboard Contract Freeze

metadata_date: 2026-06-24
status: DRAFT_PENDING_LOCAL_CHECKS_AND_BOUNDED_REVIEW
master_program: docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md
phase: P0
executor: Claude Code
reviewer: read-only bounded reviewer only

## Phase Objective

Freeze the accuracy/time leaderboard contract before any new comparison result is
interpreted as evidence. P0 defines the exact metrics, timing protocol,
two-lane table boundaries, rankable-vs-status-only row policy, and nonclaims.

P0 is a planning/governance gate only. It does not claim a leaderboard result,
does not rank algorithms, and does not treat preflight or runner matrices as
performance evidence.

## Entry Conditions Inherited From Previous Phase

- The two-lane master program exists at
  `docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md`.
- The fixed-SGQF promotion closeout and reset memo exists at
  `docs/plans/bayesfilter-fixed-sgqf-promotion-closeout-and-two-lane-comparison-reset-memo-2026-06-23.md`.
- The benchmark governance backbone exists and has been refreshed with
  two-lane comparison metadata.
- No prior phase result is required because P0 is the intake/freeze phase.

## Required Artifacts

- Phase P0 result:
  `docs/plans/bayesfilter-two-lane-filter-comparison-p0-accuracy-time-contract-freeze-result-2026-06-24.md`
- Refreshed Phase P1 subplan:
  `docs/plans/bayesfilter-two-lane-filter-comparison-p1-lowdim-lane-eligibility-subplan-2026-06-24.md`
- Any visible execution ledger / stop-handoff note if the program later adds one.

## Required Checks, Tests, And Reviews

Local checks before writing the P0 result:

```bash
rg -n "two-lane|CUT4|actual transformed SV|KSC surrogate|diagnostic-only|not performance evidence|autodiff" \
  docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md \
  docs/plans/bayesfilter-two-lane-filter-comparison-p0-accuracy-time-contract-freeze-subplan-2026-06-24.md -S

git diff --check -- \
  docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md \
  docs/plans/bayesfilter-two-lane-filter-comparison-p0-accuracy-time-contract-freeze-subplan-2026-06-24.md
```

Context-loading checks:
- verify that P0 explicitly freezes:
  - the accuracy metric(s),
  - the time metric(s),
  - warmup / repeat / seed policy,
  - CPU/GPU and dtype policy,
  - low-dimensional and high-dimensional table boundaries,
  - rankable vs status-only rows,
  - blocker row treatment,
  - nonclaims.

Bounded review:
- A read-only bounded review is required after the P0 result and P1 subplan are written.
- The review packet must be exact-path and limited to:
  - the master program,
  - this P0 subplan,
  - the P0 result,
  - the P1 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the accuracy/time leaderboard contract frozen tightly enough that later tables can be interpreted without target-mixing, timing-policy drift, or proxy-metric promotion? |
| Baseline/comparator | The two-lane master program, the reset memo, and the refreshed governance JSON backbone. |
| Primary pass criterion | The P0 result fixes the exact table families, metrics, timing protocol, rankability rules, veto diagnostics, and nonclaims, and the P1 subplan inherits those rules exactly. |
| Veto diagnostics | One merged leaderboard, missing timing policy, CUT4 allowed in high-dimensional tables, actual and surrogate SV merged, SGQF autodiff treated as promoted score evidence, or blocker rows omitted from output policy. |
| Explanatory diagnostics | Local artifact scans, wording audit, and bounded review verdict. |
| Not concluded | No numeric ranking, no accuracy winner, no time winner, no default-policy change, no HMC readiness, no production-readiness claim. |
| Artifact preserving result | P0 result plus the refreshed P1 subplan. |

## Forbidden Claims And Actions

- Do not claim a leaderboard winner from P0.
- Do not run long comparison executions in P0.
- Do not let one scalar combined score silently replace separate accuracy and timing tables.
- Do not allow actual transformed SV and KSC surrogate SV in one ranking table.
- Do not allow CUT4 into the high-dimensional lane.

## Exact Next-Phase Handoff Conditions

Advance to P1 only if the P0 result explicitly freezes:
- accuracy metric definitions,
- timing metric definitions,
- warmup/repeat policy,
- seed policy for stochastic methods,
- CPU/GPU and dtype policy,
- low-dimensional rankable rows,
- high-dimensional governed rows,
- blocker/status-only output rules,
- nonclaims and veto diagnostics.

## Stop Conditions

Stop with a blocked P0 result if:
- one merged leaderboard is still being implied,
- the time metric is not frozen precisely enough,
- row rankability is not explicit,
- blocked rows are not given a durable output contract,
- or the review finds a target-mixing ambiguity that cannot be patched cleanly.
