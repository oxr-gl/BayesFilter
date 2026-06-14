# P37-M0 Subplan: P30 Model-Suite Governance And Fixture Contracts

metadata_date: 2026-06-05

parent_plan:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md`

## Purpose

Create the common test registry, fixture schema, traceability updates, and
run-manifest contracts needed before implementing any P30 model-suite tests.
This phase is a guardrail: it prevents later phases from silently changing
model equations, priors, dimensions, reference methods, or claim language.

## Source-Governance Status

- P30 anchors: validation ladder and model equations in the P30 validation
  section.
- Zhao--Cui paper anchors: model-suite sections and algorithms; later phases
  refine exact anchors.
- MATLAB anchors: audited example directories `eg1_kalman`, `eg2_sv`,
  `eg3_sir`, `eg4_predatorprey`, and common model helpers.
- BayesFilter anchors: current `bayesfilter/highdim` package and
  `tests/highdim`.
- Status before implementation: governance/planning only.

## Evidence Contract

Question: can the project define a reproducible, source-governed model-suite
test contract before writing model-specific tests?

Primary pass criteria:

- every model has a registry row with P30 equation labels, paper anchor,
  MATLAB audit anchor, implementation status, test status, and non-claim;
- every planned test has a manifest schema including dtype, seed, dimensions,
  rank/basis, reference method, resource metrics, accuracy metrics, vetoes,
  and clean-room status;
- traceability ledger gains rows for planned executable tests or a result
  ledger explicitly states why the row remains `REFERENCE_ONLY`.

Vetoes:

- missing P30 equation anchor for a model fixture;
- ambiguous dimension convention, especially SV `x_0` versus `x_{1:T}`;
- unversioned fixture schema;
- MATLAB behavior described as BayesFilter evidence before a BayesFilter test
  exists;
- public API, DSGE, HMC, or GPU-production claim.

## Implementation Tasks

1. Add a model-suite registry document or test helper schema with rows:
   `lgssm_exact`, `stochastic_volatility_synthetic`,
   `stochastic_volatility_real_optional`, `spatial_sir`, `predator_prey`,
   `bayesfilter_generic_stress`.
2. Define a fixture manifest with:
   `model_id`, `source_equations`, `paper_anchor`, `matlab_anchor`,
   `parameter_values`, `prior`, `state_dimension`, `parameter_dimension`,
   `horizon`, `basis`, `rank`, `sweeps`, `seed`, `dtype`, `reference_method`,
   `expected_metrics`, `vetoes`, `non_claims`.
3. Define a result manifest with:
   accuracy metrics, resource metrics, finite diagnostics, branch/replay
   status where applicable, and failure classification.
4. Add tests that fail if a model fixture lacks required anchors or if a
   result manifest omits clean-room and non-claim fields.
5. Update the traceability ledger only with planning statuses; do not promote
   unimplemented models.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/validation.py
tests/highdim/test_p30_model_suite_contracts.py
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
docs/plans/*p37*phase0*result*.md
```

Forbidden writes:

```text
bayesfilter/__init__.py
third_party/audit/**
```

## Planned Commands

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py \
  tests/highdim/test_phase0_contracts.py \
  tests/highdim/test_p30_model_suite_contracts.py

git diff --check
```

## Exit Criteria

- registry and manifest schema tests pass;
- no top-level public API exposure;
- traceability ledger marks unimplemented model tests as `REFERENCE_ONLY` or
  `BLOCKED_UNVALIDATED`, not as passed evidence;
- Claude or result-ledger review confirms no unsupported claims.

