# P2 Subplan: Fixed-SGQF Accepted-Path and Failure Ladder

metadata_date: 2026-06-14
phase: P2
status: DRAFT_REVIEW_READY

## Date

2026-06-14

## Governing Master Program

This phase executes under:

```text
docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md
```

## Purpose

P2 closes G2 and G4 by broadening accepted-path validation and later-time /
later-stage failure coverage.

## Scope

P2 owns:

- multidimensional accepted-path rows expected to pass cleanly;
- later-time failures after one or more accepted steps;
- stage-specific failure rows for declared SGQF stages;
- diagnostics-contract checks on `time_index`, `stage`, `reason`, and payload
  fields.

P2 does not own:

- dense-reference accuracy ranking;
- score-vs-FD promotion evidence except where needed to preserve branch context.

## Governing Constraints

1. Contract rows may intentionally fail and still pass the phase.
2. The objective is faithful branch/failure recording, not numerical closeness.
3. If a stage such as `carried_covariance` is claimed reachable, the phase must
   produce a direct row or write a blocker explaining why it is not reachable on
   the attempted fixture ladder.
4. Later-time failures must not be compressed into generic “failure happened”
   summaries; time index is part of the contract.

## Evidence Contract

Question:

Does the fixed-SGQF lane preserve its declared branch and failure semantics on
multidimensional accepted paths and later-time failure fixtures?

Primary pass criterion:

- at least one multidimensional accepted-path row passes cleanly;
- later-time failures are recorded with correct stage and time index;
- each attempted failure stage is either covered directly or blocked explicitly.

Veto diagnostics:

- a later-time failure row reports only the first-step state;
- a failure stage label is inferred without testing;
- diagnostics payloads are not preserved at the failure site.

Explanatory-only diagnostics:

- accepted-step count;
- branch hash;
- per-stage failure frequency;
- dimensionality of accepted fixtures.

What will not be concluded:

- no numerical-accuracy claim from contract rows alone;
- no general stability theorem.

## Stage Ladder

Attempt direct rows for:

- `previous_covariance`
- `predictive_covariance`
- `innovation_covariance`
- `carried_covariance` when reachable

The phase result must say which were covered directly and which were blocked.

## Execution Steps

1. Reuse existing failure-fixture patterns from current SGQF contract tests.
2. Add one or more multidimensional accepted-path fixtures that are expected to
   pass.
3. Add fixtures that fail after at least one accepted step.
4. Attempt stage-specific failure construction, including carried-covariance.
5. Verify diagnostics payload and time-index reporting.
6. Write a contract-focused result note with explicit pass/block labels.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-fixed-sgqf-p2-accepted-path-and-failure-ladder-result-2026-06-14.md`
- Phase review ledger:
  `docs/plans/bayesfilter-fixed-sgqf-p2-claude-review-ledger-2026-06-14.md`

## Stop Rules

Stop if:

- a failure row cannot be made deterministic enough for contract testing;
- a claimed stage is not actually surfaced by the implementation and the phase
  would need to invent a label;
- accepted-path rows require changing the branch semantics being tested.

## Exit Criteria

P2 exits with `PASS_P2_FIXED_SGQF_ACCEPTED_PATH_AND_FAILURE_LADDER_READY_FOR_P5`
only if it records both successful accepted-path rows and later-stage/time
contract evidence durably.
