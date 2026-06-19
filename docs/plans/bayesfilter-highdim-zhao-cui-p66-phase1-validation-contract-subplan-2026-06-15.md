# P66 Phase 1 Subplan: Validation Contract And API Design

metadata_date: 2026-06-15
status: REVIEW_READY_AFTER_PHASE0
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p66-fixed-branch-validation-ladder-master-program-2026-06-15.md
phase: 1
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Design the replacement validation contract and public/local API for P66 before
implementation.  Phase 1 decides what the new result object, manifest fields,
statuses, sample-adequacy rules, and old-P60 sentinel payload should be.

The Phase 1 artifact is a reviewed contract/schema/policy note.  It is not an
experiment result, implementation evidence, convergence evidence, or correctness
evidence.

## Entry Conditions Inherited From Previous Phase

- Phase 0 confirms the P65 baseline and old P60 sentinel gap.
- Phase 0 result demotes `(degree=0, rank=1)` versus `(degree=1, rank=2)` to
  explanatory sentinel status for this target.
- Phase 0 did not change code.
- Phase 0 fresh probe reported high square-root normalizers
  `[1.2197182121566172, 1.6339670649545497]`, high defensive-only steps `[]`,
  and old P60 blockers `log_marginal_delta_threshold_exceeded` and
  `normalizer_increment_delta_threshold_exceeded`.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase1-validation-contract-result-2026-06-15.md`.
- Updated P66 visible ledger and Claude review ledger.
- Refreshed Phase 2 implementation subplan.

## Required Checks/Tests/Reviews

- Inspect current result dataclasses and manifest patterns around P59/P60.
  Treat them as current code exemplars that must be checked against the source
  route and manifest discipline, not as unquestioned authority.
- Draft status taxonomy and sample-adequacy formula.
- Draft API names and result manifest schema.
- Explicitly classify admissibility checks as preconditions/veto diagnostics,
  sample adequacy as permission-to-diagnose, and adjacent ladder stability as
  the only P66 convergence-style diagnostic.
- Define adjacent-ladder comparison invariants: target/source route,
  source-pushed fit-data policy, fixed-HMC metadata, `tau`, initialization,
  sample policy, target/order/axes, previous-marginal axes, and diagnostic
  threshold definitions.
- Bounded Claude review of the contract/design before implementation.
- Local compile check only if docstrings or code comments are touched; otherwise
  no code changes in Phase 1.

The sample-adequacy formula must start from the maximum ALS core column count:

```text
max_core_columns = max_axis ranks[axis] * (degree + 1) * ranks[axis + 1]
diagnostic_min_fit_samples = 2 * max_core_columns
preferred_fit_samples = 4 * max_core_columns
```

This rule is a permission-to-diagnose rule, not evidence of convergence.  It is
an engineering heuristic for the reviewed comparator setup, not a proof of
adequacy, not a convergence threshold, and not portable outside this scoped
validation ladder without renewed review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact contract/schema/policy must constrain the P66 implementation of the replacement validation ladder? |
| Baseline/comparator | Phase 0 CPU-only reproduction of the P65 sentinel state under the pinned tuple and source-route invariants, plus current P59/P60 code/manifest exemplars checked against source-route discipline. |
| Primary pass criterion | A reviewed written contract specifies unambiguous statuses, API surface, result schema, manifest payload, sample-adequacy heuristic, admissibility preconditions, sentinel diagnostics, adjacent rank ladder, adjacent degree ladder, comparison invariants, focused tests, and forbidden claims; this contract is complete enough to constrain Phase 2 implementation. |
| Veto diagnostics | Contract keeps old low/high closeness as primary; thresholds are weakened; sample adequacy is absent or treated as convergence; source-route invariants are optional; statuses conflate admissibility with convergence/correctness; comparator schema remains ambiguous; metrics can still be misread as pass criteria. |
| Explanatory diagnostics | Candidate function names, result dataclasses, status names, expected test rows, runtime cost estimates. |
| Not concluded | No code implementation yet, no d=18 correctness, no adjacent-ladder empirical result. |

## Forbidden Claims/Actions

- Do not implement the new ladder before the contract is reviewed.
- Do not remove old P60 artifacts; preserve them as historical/sentinel
  diagnostics.
- Do not change scientific pass/fail claims after seeing implementation
  results.
- Do not claim adjacent-ladder stability is sufficient for scientific
  correctness.
- Do not let `PASS_FIXED_BRANCH_ADMISSIBLE_NONCOLLAPSED` imply convergence.
- Do not let sample adequacy imply convergence; it only permits a convergence
  diagnostic to be interpreted.
- Do not use P59/P60 manifest patterns as authority without checking they match
  the current source-route invariants and intended manifest discipline.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- the validation contract is reviewed and converged;
- the contract explicitly enumerates comparison invariants:
  - route family and source authority;
  - realized target definition;
  - keep/input axis split;
  - defensive `tau`;
  - initialization and fixed-HMC adaptation metadata;
  - fit-sample budget policy and sample-adequacy rule;
  - diagnostic threshold definitions;
  - admissibility status on both compared branches;
- exact code surfaces to change are identified;
- focused tests to add/update are enumerated;
- adjacent-ladder comparison invariants are explicit;
- Phase 2 is barred from encoding policy beyond the reviewed contract;
- Phase 2 has an implementation evidence contract and stop conditions.

## Stop Conditions

- No coherent sample-adequacy rule can be stated.
- The API would require a broader architectural rewrite than P66 authorizes.
- Current P59/P60 artifacts do not support a clean status taxonomy, comparator
  schema, and invariant set; stop without implementation and write a revised
  contract note.
- Any status remains ambiguous between precondition, convergence diagnostic,
  correctness claim, and explanatory sentinel evidence.
- Claude and Codex do not converge after five rounds for the same design
  blocker.

## End-Of-Subplan Protocol

1. Write Phase 1 result or blocker.
2. Draft or refresh Phase 2 subplan.
3. Review Phase 2 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
