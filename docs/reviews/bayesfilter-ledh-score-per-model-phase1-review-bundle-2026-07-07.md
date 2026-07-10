# Phase 1 Result / Phase 2 LGSSM Subplan Review Bundle

metadata_date: 2026-07-07
review_scope: `score_phase1_phase2_handoff`

## Role Contract

Claude is read-only reviewer only.

Do not edit files, run experiments, launch agents, approve policy boundaries,
or change state.

Codex remains supervisor and executor.

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```

## Objective

Review whether Phase 1 safely adds the LEDH score artifact schema and whether
the Phase 2 LGSSM subplan is sufficient before LGSSM score admission work.

## Fixed Paths To Review

- `docs/plans/bayesfilter-ledh-score-per-model-phase1-score-schema-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-phase2-lgssm-subplan-2026-07-07.md`
- `bayesfilter/highdim/ledh_score_contract.py`
- `tests/highdim/test_ledh_score_contract_phase1.py`

Do not review the whole repo.

## Phase 1 Summary

Phase 1 added a score artifact validator and tests. The validator accepts only
score artifacts tied to an admitted value artifact with matching:

- row id;
- target scalar;
- target output tensor field;
- target observation policy;
- theta coordinate system;
- parameter names/order.

It also requires:

- `score_target_kind = realized_finite_N_ledh_log_likelihood_estimator`;
- `value_score_route_status = same_route_value_score`;
- finite score vector;
- allowed no-tape provenance;
- explicit false flags for `uses_gradient_tape`,
  `uses_forward_accumulator`, and `uses_stopped_partial_derivative`;
- correctness status pass;
- full `N=10000` memory gate for admitted rows.

Local checks:

- compile check passed;
- focused schema tests: `19 passed, 2 warnings`;
- combined value/schema replay: `22 passed, 2 warnings`;
- diff hygiene passed.

Repair:

- the first schema run rejected approved `no_autodiff` route names because of
  an overbroad forbidden substring; this was repaired while preserving explicit
  tape/ForwardAccumulator/stopped-partial vetoes.

## Phase 2 Specific Risk

The admitted LGSSM value artifact uses:

```text
num_particles = 10000
```

The active LGSSM score runner still contains a stale constant:

```text
FULL_ROW_NUM_PARTICLES = 1000
```

The Phase 2 subplan therefore requires a preflight repair or explicit override
before any full LGSSM score artifact can be admitted. A raw runner artifact is
not enough; the final score artifact must pass the Phase 1 schema against:

```text
docs/plans/ledh-phase2-lgssm-forward-scalar-artifact-2026-07-07.json
```

## Review Questions

1. Does Phase 1 enforce score/value same-target identity strongly enough before
   model score work?
2. Does the Phase 1 repair preserve the no-tape ban while allowing approved
   `no_autodiff` route labels?
3. Does Phase 2 correctly treat the stale LGSSM `N=1000` full-row identity as a
   blocker/preflight repair rather than as admissible evidence?
4. Does Phase 2 require the score artifact to validate against the admitted
   N=10000 value artifact before admission?
5. Are Phase 2 stop and handoff conditions sufficient?

## Pass Criteria

Return `VERDICT: AGREE` only if:

- Phase 1 is internally consistent and boundary-safe;
- Phase 2 is safe to execute before LGSSM score admission;
- no score/scientific/runtime boundary is crossed; and
- no fixable blocker remains in the plan.

Return `VERDICT: REVISE` if any material issue remains.
