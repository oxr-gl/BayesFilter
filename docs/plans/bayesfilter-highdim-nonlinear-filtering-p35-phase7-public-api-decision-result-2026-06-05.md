# P35 Phase 7 Result: Public API Decision

metadata_date: 2026-06-05
phase: Phase 7 public API decision
git_commit: 7ccb9c3

## Skeptical Plan Audit

Status: PASS_TO_PLAN_REVIEW.

The material risk in Phase 7 is overexposure. Phases 0--6 validated important
internal pieces: measure conventions, branch manifests, basis/TT algebra,
squared densities, fixed fitting, exact LGSSM value gates, derivative
components, finite-difference diagnostics, and bounded stress-smoke manifests.
They did not validate a stable end-to-end score API, DSGE readiness, GPU
readiness, HMC readiness, or adaptive Zhao--Cui differentiability.

The original Phase 7 subplan says public promotion requires exact small-model
value and score gates plus deterministic replay for fit, value, and score. The
score part remains unresolved. Therefore a stable top-level public API would
misrepresent the evidence.

Decision before implementation: select Option B,
`EXPERIMENTAL_SUBPACKAGE_ONLY`. Keep highdim symbols explicit under
`bayesfilter.highdim`; do not edit top-level `bayesfilter/__init__.py`; do not
add stable wrappers named `tf_fixed_branch_squared_tt_score`; and add tests that
guard against accidental top-level exposure and human-facing overclaims.

## Evidence Contract

Question: what API surface can be honestly exposed after Phase 0--6, given the
unresolved end-to-end score API?

Baseline/comparator:
- existing v1 top-level public API must remain unchanged;
- `bayesfilter.highdim` subpackage imports must remain explicit;
- candidate stable symbols must be rejected unless they include fixed-branch
  scope and have corresponding validation evidence.

Primary pass criteria:
- `tests/test_v1_public_api.py` remains green;
- no highdim top-level symbols are exported before explicit Option C approval;
- `bayesfilter.highdim` remains importable as an explicit experimental
  subpackage;
- tests enforce that candidate stable public names include fixed-branch scope
  language;
- docs/result ledger do not claim adaptive derivative, exact nonlinear
  likelihood, DSGE readiness, HMC readiness, GPU readiness, or end-to-end score
  readiness.

Veto diagnostics:
- any top-level `bayesfilter.__all__` highdim symbol;
- any wrapper or doc claim implying adaptive Zhao--Cui derivative support;
- any claim that Phase 6 stress smoke proves large-scale scalability;
- any existing v1 public API regression;
- any forbidden production backend/source reference in highdim code/tests.

Explanatory-only diagnostics:
- count of explicit subpackage exports;
- Phase 0--6 prior pass counts;
- Claude review wording.

What will not be concluded:
- no stable top-level highdim public API;
- no score API readiness;
- no DSGE/HMC/GPU readiness;
- no adaptive-branch derivative support;
- no default-method recommendation.

## Planned File Ownership

Allowed writes for this Option B decision:

```text
bayesfilter/highdim/__init__.py
tests/highdim/test_public_api_highdim.py
docs/plans/*p35-phase7*result*.md
docs/plans/*p35-phase7*claude-review-ledger*.md
```

Explicitly avoided:

```text
bayesfilter/__init__.py
tests/test_v1_public_api.py
```

Those files may be read and tested but should not be modified under Option B.

## Intended Decision

decision_status: `EXPERIMENTAL_SUBPACKAGE_ONLY`

Rationale:
- Phase 0--6 have enough internal evidence for explicit subpackage use by
  implementation developers.
- The end-to-end score API remains unresolved, so stable public top-level
  wrappers would be premature.
- The branch manifest and replay contracts are still part of the mathematical
  safety story and should remain explicit rather than hidden behind a polished
  stable API.

## Planned Tests

Add `tests/highdim/test_public_api_highdim.py` with:

- `test_existing_v1_public_api_symbols_preserved`
- `test_no_highdim_top_level_symbols_before_phase7_option_c`
- `test_experimental_subpackage_import_is_explicit_only`
- `test_stable_public_symbols_include_fixed_branch_scope_language`
- `test_public_docs_do_not_claim_adaptive_derivative`

## Planned Validation

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py \
  tests/highdim/test_public_api_highdim.py

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py \
  tests/highdim/test_phase0_contracts.py \
  tests/highdim/test_bases.py \
  tests/highdim/test_tt_algebra.py \
  tests/highdim/test_squared_tt_density.py \
  tests/highdim/test_transport.py \
  tests/highdim/test_fixed_branch_fit.py \
  tests/highdim/test_failure_exits.py \
  tests/highdim/test_filtering_kalman_exact.py \
  tests/highdim/test_fixed_branch_derivatives.py \
  tests/highdim/test_scaling_smoke.py \
  tests/highdim/test_public_api_highdim.py

git diff --check

rg -n "^\s*(import|from)\s+(numpy|jax|torch)\b|matlab|octave|tensor-ssm-paper-demo|zhao_cui_tensor_ssm_p10" \
  bayesfilter/highdim tests/highdim
```

## Results

Plan review:
- Claude worker `highdim-zhao-cui-phase7-plan-review-iter1` returned
  `PASS_PLAN_TO_IMPLEMENTATION`.
- Review finding: `EXPERIMENTAL_SUBPACKAGE_ONLY` is the strongest option
  supported by the current evidence because the end-to-end score API remains
  unresolved.

Files changed:
- `tests/highdim/test_public_api_highdim.py`
- this result ledger
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase7-public-api-decision-claude-review-ledger-2026-06-05.md`

Files deliberately not changed:
- `bayesfilter/__init__.py`
- `tests/test_v1_public_api.py`

Validation:
- Phase 7 public API gate:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_public_api_highdim.py`
  returned `7 passed, 2 warnings in 2.77s`.
- Phase 0--7 CPU suite plus public API guardrail:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_failure_exits.py tests/highdim/test_filtering_kalman_exact.py tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_scaling_smoke.py tests/highdim/test_public_api_highdim.py`
  returned `108 passed, 2 warnings in 6.16s`.
- `git diff --check`: pass, no output.
- forbidden backend/source scan over `bayesfilter/highdim tests/highdim`: pass,
  no matches.

Primary pass criterion status: PASS.

Veto diagnostics status:
- no top-level highdim symbols were added to `bayesfilter.__all__`;
- explicit `bayesfilter.highdim` subpackage import remains available;
- candidate stable names are required to include fixed-branch scope language;
- docs/result ledger explicitly records the non-claims;
- existing v1 public API tests passed;
- forbidden backend/source scan passed.

Decision: `EXPERIMENTAL_SUBPACKAGE_ONLY`.

Termination reason: stable top-level highdim API is blocked by unresolved
end-to-end score validation; explicit subpackage use is allowed for internal
implementation and further gates.

Stop condition triggered: `score_api_unresolved_for_stable_top_level_api`.

What is not concluded:
- no stable top-level highdim public API;
- no end-to-end score API readiness;
- no DSGE readiness;
- no HMC readiness;
- no GPU readiness;
- no adaptive Zhao--Cui derivative support;
- no large-scale scalability claim.

Next justified action: create a dedicated end-to-end fixed-branch score API
gate before any HMC, DSGE, or stable public API promotion.
