# P85 Phase 3 Result: Implementation And Test Matrix Review

Date: 2026-06-23

Status: `PASS_P85_PHASE3_IMPLEMENTATION_TEST_MATRIX`

## Phase Objective

Freeze the exact implementation surface, file list, tests, and command contract
before changing BayesFilter code.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are the planned code edits and tests narrow enough to implement the Phase 2 design without touching unrelated work? |
| Baseline/comparator | Phase 2 design and current local basis/source-route tests. |
| Primary criterion | Phase 3 freezes exact files, expected behaviors, tests, and CPU-hidden commands for Phase 4. |
| Veto diagnostics | Unbounded file list; missing regression tests; hidden default-policy change; no dirty-worktree assessment; no exact commands. |
| Explanatory diagnostics | Diff-risk assessment, API export list, expected manifest payload examples. |
| Not concluded | No implementation correctness, no source repair, no fit quality. |
| Artifact | This Phase 3 result and refreshed Phase 4 subplan. |

## Skeptical Plan Audit

Phase 3 audit passed with a narrowed implementation envelope:

- Wrong-baseline risk is controlled. The planned edits address Phase 2 setup
  configuration and P84 Phase 1 basis/domain parity only.
- Proxy-promotion risk is controlled. Phase 4 tests may prove unit-level
  config/evaluation behavior only; they cannot prove fit quality, filtering
  correctness, XLA performance, or production readiness.
- Dirty-worktree risk is material. `bayesfilter/highdim/filtering.py` is dirty
  and is therefore excluded from Phase 4 edits.
- Hidden-assumption risk is controlled by keeping full fitting/transport over
  algebraic `Lagrangep` out of Phase 4. Existing defensive-density and
  filtering helpers assume bounded basis-domain lengths.
- Environment risk is controlled by requiring CPU-hidden TensorFlow test
  commands.

## Dirty-Worktree Assessment

Focused status check:

```text
 M bayesfilter/highdim/filtering.py
```

Candidate files inspected for Phase 4 were clean unless listed above; this
inspection list is not the approved edit list:

- `bayesfilter/highdim/bases.py`
- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_bases.py`
- `tests/highdim/test_p59_author_sir_36d_target_fit.py`

Phase 4 must not edit `bayesfilter/highdim/filtering.py` unless a new reviewed
subplan and human approval expand the file list.

## Approved Phase 4 File List

Phase 4 may edit only:

- `bayesfilter/highdim/bases.py`
- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/__init__.py`
- new test file `tests/highdim/test_p85_configurable_basis_domain.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-subplan-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-result-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-subplan-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-execution-ledger-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-stop-handoff-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p85-claude-review-ledger-2026-06-23.md`

No other code file is approved by Phase 3.

## Approved Phase 4 Implementation Behaviors

Phase 4 may implement:

1. Setup-spec dataclasses or equivalent immutable objects:
   - `DomainMapSpec`;
   - `BasisSpec`;
   - `ProductBasisSpec`.
2. Domain-map objects or helpers for:
   - bounded interval `[-1,1]`;
   - algebraic map with `scale=1`.
3. A BayesFilter-owned piecewise Lagrange basis object for author-style
   `Lagrangep(order, num_elems)`:
   - no third-party MATLAB code copying;
   - `basis_dim = num_elems * order + 1`;
   - for `Lagrangep(4,8)`, `basis_dim = 33`;
   - local-node construction must be documented as BayesFilter-owned and tied
     to author anchors.
4. `ProductBasis` generalization only to the minimal basis protocol:
   - `basis_dim`;
   - `dtype`;
   - `evaluate(points)`;
   - `mass_matrix(measure)`;
   - `integral_vector(measure)`;
   - `manifest_payload()`.
5. Builder/helper functions for:
   - legacy bounded Legendre diagnostic setup;
   - author SIR algebraic `Lagrangep(4,8)` setup manifest/config.
6. Manifest fields in P59/P85 source-route surfaces that distinguish:
   - `source_faithful`/`sir_config`;
   - `local_gap`/`diagnostic_legendre_route`;
   - XLA/static setup fields;
   - nonclaims.

## Explicit Phase 4 Non-Behaviors

Phase 4 must not:

- run author algebraic `Lagrangep` through full source-route fitting;
- update `filtering.py`, `squared_tt.py`, `tt.py`, or `fitting.py`;
- claim production fitting support for algebraic `Lagrangep`;
- claim HMC/derivative readiness;
- claim KR closure;
- claim XLA performance;
- remove existing `no AlgebraicMapping(1) parity claim` from legacy diagnostic
  fit-data manifests unless replaced by a reviewed route-specific distinction.

## Downstream Compatibility Boundary

Existing downstream helpers assume bounded domains in several places:

- `bayesfilter/highdim/squared_tt.py:59-68` multiplies domain lengths for
  reference-density normalizers.
- `bayesfilter/highdim/squared_tt.py:390-392` constructs default grids from
  `basis.domain.left` and `basis.domain.right`.
- `bayesfilter/highdim/filtering.py:2884-2911` assumes bounded interval domains
  for quadrature and uniform reference-weight density.
- `bayesfilter/highdim/transport.py:620` returns reciprocal domain length.

Because `AlgebraicMapping(1)` represents an unbounded physical domain mapped to
reference `[-1,1]`, Phase 4 may expose config/evaluation/unit manifests but
must block full fitting/transport until a later reviewed phase generalizes the
density and mapping conventions.

## Required Tests

Phase 4 must add or update tests that check:

- `DomainMapSpec` payload for bounded interval and algebraic scale;
- algebraic map formula and inverse at representative points;
- `BasisSpec` payload for Legendre and `Lagrangep(4,8)`;
- `Lagrangep(4,8)` basis dimension is 33;
- `ProductBasisSpec` replication to dimension 36 gives a 36-entry
  `basis_dim_tuple` of 33s;
- legacy P59 author-SIR prep still passes and still records the legacy
  diagnostic nonclaim;
- an author SIR basis/domain config manifest exists and is classified as
  `source_faithful`/`sir_config`;
- legacy bounded Legendre route is classified as
  `local_gap`/`diagnostic_legendre_route`, not `source_faithful`;
- no runtime tensor-controlled basis-family switching is advertised.

Phase 4 should prefer unit tests over fitting tests.

## Exact Phase 4 Commands

Allowed CPU-hidden commands:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p85_configurable_basis_domain.py
```

Regression command:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p59_author_sir_36d_target_fit.py
```

Hygiene command:

```bash
git diff --check -- bayesfilter/highdim/bases.py bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p85_configurable_basis_domain.py docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-subplan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-result-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-subplan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-execution-ledger-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-stop-handoff-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-claude-review-ledger-2026-06-23.md
```

No GPU, fitting ladder, HMC, LEDH, d=50/d=100, or long command is authorized.

## Required Phase 4 Review

Before Phase 5, Phase 4 must obtain bounded Claude read-only review of either:

- the Phase 4 result, if it contains enough diff and test summary detail; or
- a single exact diff/result artifact produced for Phase 4.

Claude cannot authorize widening the file list, running fitting, or claiming
production readiness.

## Local Checks

Phase 3 local checks passed:

- Dirty-worktree focused status was recorded.
- Existing tests and API patterns were scanned.
- Existing source-route manifest surfaces were inspected.
- Bounded-domain downstream assumptions were identified.
- No code edits or runtime TensorFlow tests were run.

## Decision

Phase 3 passes:

```text
PASS_P85_PHASE3_IMPLEMENTATION_TEST_MATRIX
```

Phase 4 may begin only within the approved file list and command list above.

## Next-Phase Handoff

Phase 4 may begin using:

- `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-subplan-2026-06-23.md`

The Phase 4 subplan is refreshed by this result: its "expected checks" are now
the exact commands listed above, and its implementation scope is bounded by the
approved file list.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Pass Phase 3 implementation/test matrix. | PASS: exact files, behaviors, tests, commands, and downstream blocks are frozen. | PASS: dirty `filtering.py` excluded; no fitting/GPU/HMC/LEDH scope; no production claim. | Whether a narrow `bases.py`/`source_route.py` implementation can expose enough author config without downstream fitting support. | Implement Phase 4 within the frozen envelope. | No implementation correctness, P84 repair, fit quality, correctness, XLA performance, or production readiness. |
