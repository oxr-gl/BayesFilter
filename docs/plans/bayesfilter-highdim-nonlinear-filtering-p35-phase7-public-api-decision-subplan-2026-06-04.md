# P35 Phase 7 Subplan: Public API Decision

metadata_date: 2026-06-04

parent_plan:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-plan-2026-06-03.md`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- This phase does not automatically expose public API symbols.
- This phase does not claim the method is default for high-dimensional
  filtering.
- This phase does not replace existing SVD-CUT, sigma-point, or Kalman APIs.

## Evidence Contract

Question: after internal implementation and validation, should the Zhao--Cui
fixed-branch squared-TT lane become a documented BayesFilter API surface?

Promotion criteria:
- Phases 0--6 have result ledgers with no unresolved blockers;
- exact small-model value and score gates pass;
- deterministic replay gates pass for fit, value, and score;
- stress/performance result notes identify a defensible operating envelope;
- docs state fixed-branch derivative scope and adaptive non-claims;
- existing public API tests pass.

Veto diagnostics:
- unresolved measure/branch/score/performance blocker;
- public API would expose unstable branch internals;
- user-facing docs imply adaptive derivative or exact nonlinear likelihood;
- existing v1 public API regression.

## Planned File Ownership

Allowed writes only if Phase 7 approves API exposure:

```text
bayesfilter/__init__.py
bayesfilter/highdim/__init__.py
tests/test_v1_public_api.py
tests/highdim/test_public_api_highdim.py
docs/plans/*p35-phase7*result*.md
```

No API exposure is allowed in Phases 0--6.

## API Decision Options

### Option A: Keep Internal

Use when tests pass but operating envelope is too narrow or stress performance
is not yet persuasive.

Expose no top-level symbols.  Keep imports under `bayesfilter.highdim`.

### Option B: Experimental Internal API

Use when exact tests pass and limited stress models are useful, but the method
is not ready for stable public API.

Expose only `bayesfilter.highdim` symbols.  Do not add to top-level
`bayesfilter.__all__`.

### Option C: Stable Public API

Use only after strong validation and review.

Candidate public symbols must be minimal, for example:

```text
TFFixedBranchSquaredTTFilterConfig
TFFixedBranchSquaredTTFilterResult
tf_fixed_branch_squared_tt_log_likelihood
tf_fixed_branch_squared_tt_score
```

Names must include `fixed_branch` or equivalent scope language so users cannot
mistake the derivative for the adaptive Zhao--Cui algorithm.

## Documentation Requirements

Any public or experimental docs must state:

- measure convention;
- fixed-branch scalar definition;
- branch manifest and hash role;
- exact small-model validation status;
- stress-model validation status;
- failure exits;
- non-claims about adaptive derivatives and exact nonlinear likelihood.

## Review Requirements

Before Option B or C:

1. Codex code review for API stability and test evidence.
2. Claude hostile review for overclaiming and hidden branch assumptions.
3. Public API test update review.
4. Clean-room contamination audit result.

## Exit Criteria

- API decision result note is written.
- Existing `tests/test_v1_public_api.py` passes or is intentionally updated.
- No top-level public export is added unless Option C is explicitly approved.
