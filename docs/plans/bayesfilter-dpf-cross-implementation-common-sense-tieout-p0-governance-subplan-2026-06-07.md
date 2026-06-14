# P0 Governance And Scope Subplan

metadata_date: 2026-06-07
parent_program: `bayesfilter-dpf-cross-implementation-common-sense-tieout-plan-2026-06-06.md`

## Phase Question

Is the BayesFilter-vs-FilterFlow tie-out campaign governed by an explicit
no-oracle, no-premature-student, evidence-first contract before any additional
execution occurs?

## Evidence Contract

Primary comparator:

- the written master program and phase subplans.

Primary pass criterion:

- the master program states phase order, veto diagnostics, non-claims, student
  deferral, and closure gates clearly enough that an executor cannot treat
  student outputs, TT, paper tables, BayesFilter, or FilterFlow as an oracle.

Veto diagnostics:

- any active command block includes student-repository execution;
- any phase lacks a declared scalar/comparator/exit gate;
- any phase treats agreement as filtering correctness;
- any phase lacks mismatch classification rules.

Explanatory diagnostics:

- cross-links to existing results and runner names.

Non-claims:

- P0 does not execute numerical tests;
- P0 does not close any BayesFilter/FilterFlow model surface.

## Work Items

1. Upgrade the flat plan to a phased master program.
2. Add subplans P0--P6.
3. Run Claude review on the master program and subplans until convergence or
   five rounds.
4. Record review findings and patches in the master review ledger.

## Exit Gate

P0 exits when the master program and subplans pass local markdown hygiene,
Claude has no material blockers or all material blockers are patched, and the
student phase is explicitly terminal-only.
