# P86 Phase 1 Subplan: Lagrangep Mass And Integral Implementation

Date: 2026-06-24

Status: `REVIEWED_READY_FOR_IMPLEMENTATION`

## Phase Objective

Implement and test author-anchored one-dimensional `LagrangePiecewiseBasis1D`
mass matrices and integral vectors for the reference-domain `Lagrangep` basis,
without changing fitting defaults or claiming production readiness.

## Entry Conditions Inherited From Previous Phase

- Phase 0 passed and recorded the P86 source, approval, and XLA boundaries.
- P85 author setup representation exists.
- P85 deliberately leaves `LagrangePiecewiseBasis1D.mass_matrix()` and
  `.integral_vector()` blocked.
- No fitting, GPU, HMC, LEDH, long, scale, or production command is authorized.

## Required Artifacts

- Implementation diff limited to `bayesfilter/highdim/bases.py`,
  `bayesfilter/highdim/__init__.py` only if export changes are necessary, and
  focused tests under `tests/highdim/`.
- Focused test file:
  `tests/highdim/test_p86_lagrangep_mass_integral.py`
- Phase 1 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase1-lagrangep-mass-integral-result-2026-06-24.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md`
- Refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase2-algebraic-measure-contract-subplan-2026-06-24.md`

## Required Checks / Tests / Reviews

- Source-anchor inspection of `LagrangeRef.m`, `Piecewise.m`, and
  `Lagrangep.m`.
- Phase 1 result must record exact author anchors and local mapping:
  - `LagrangeRef.m:27-45` for local nodes, Jacobi(1,1) interior points, and
    barycentric weights;
  - `LagrangeRef.m:46-62` for local exact mass and local integral weights;
  - `Piecewise.m:24-35` for default `[-1,1]` piecewise grid and element size;
  - `Lagrangep.m:18-33` for global node assembly and global-to-local index
    mapping;
  - `Lagrangep.m:34-52` for unweighted mass, unweighted integral weights,
    normalized mass, and normalized integral weights;
  - the exact local BayesFilter methods and tests that implement each rule.
- Closed-form analytical micro-baseline:
  - order `1`, one element on `[0,1]` has local basis functions `1-x` and `x`;
  - exact local mass is `[[1/3, 1/6], [1/6, 1/3]]`;
  - exact local integral vector is `[1/2, 1/2]`;
  - after lifting to the default `[-1,1]` reference domain with one element,
    `REFERENCE_LEBESGUE` mass is `[[2/3, 1/3], [1/3, 2/3]]`;
  - `REFERENCE_MEASURE` mass divides the default `[-1,1]` Lebesgue mass by
    `2`;
  - `REFERENCE_LEBESGUE` integral vector is `[1, 1]`, and
    `REFERENCE_MEASURE` integral vector is `[1/2, 1/2]`.
- CPU-hidden focused tests for:
  - local `[0,1]` Lagrange basis integrals;
  - global `order=4`, `num_elems=8` cardinality and node interpolation;
  - mass symmetry and positive definiteness;
  - constant-function integral consistency;
  - `REFERENCE_MEASURE` versus `REFERENCE_LEBESGUE` scaling behavior;
  - no change to Legendre behavior.
- Exact CPU-hidden test command after implementation:
  `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p86_lagrangep_mass_integral.py tests/highdim/test_p85_configurable_basis_domain.py`
- If the focused test path changes, this subplan must be patched and rereviewed
  before execution.
- `git diff --check -- bayesfilter/highdim/bases.py tests/highdim docs/plans/bayesfilter-highdim-zhao-cui-p86*.md`
- Claude read-only bounded review of the Phase 1 result artifact. The result
  artifact must explicitly name the changed paths and line ranges that Claude
  may inspect under the one-path prompt rule. A prose-only summary is not
  sufficient for Phase 1 implementation review.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does BayesFilter provide source-anchored `Lagrangep` mass and integral operations matching the author one-dimensional reference-domain assembly? |
| Baseline/comparator | Author `LagrangeRef.m`, `Piecewise.m`, `Lagrangep.m`, the closed-form order-1 analytical micro-baseline, and P85 local `NotImplementedError` provenance blocker. |
| Primary criterion | Focused CPU-hidden tests pass for exact mass/integral semantics and no Legendre regression; result cites author and local anchors. |
| Veto diagnostics | Missing source anchors; non-symmetric or non-positive mass; wrong basis cardinality; wrong measure scaling; copying third-party code without review; broad production claim. |
| Explanatory diagnostics | Matrix entries, eigenvalue floor, integral sum, interpolation identity, diff summary. |
| Not concluded | No algebraic physical-measure correctness, fit quality, downstream wiring, correctness bridge, HMC readiness, or production readiness. |
| Artifact | Phase 1 result, tests, and implementation diff. |

## Forbidden Claims / Actions

- Do not run fitting, GPU, HMC, LEDH, d=50/d=100, or long commands.
- Do not claim the algebraic route is fit-ready from 1D mass/integral alone.
- Do not change fitting defaults or production metadata.
- Do not reopen, satisfy, or cross any P84 downstream approval gate. P84 Phase
  2 fitting remains blocked after Phase 1 unless later P86 phases and exact
  approvals say otherwise.
- Do not touch unrelated dirty files, especially `bayesfilter/highdim/filtering.py`.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if:

- `LagrangePiecewiseBasis1D.mass_matrix()` and `.integral_vector()` are
  implemented or precisely blocked;
- focused CPU-hidden tests pass or the blocker result explains why not;
- Phase 1 result records author/local anchors and non-claims;
- Phase 2 subplan is refreshed and reviewed.

## Stop Conditions

Stop if:

- author source semantics cannot be mapped to the local basis without an
  unapproved invention;
- tests show mass/integral instability that cannot be repaired locally;
- code edits would require modifying unrelated dirty files;
- Claude and Codex do not converge after five review rounds.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 1 result / close record;
3. draft or refresh the Phase 2 subplan;
4. review the Phase 2 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
