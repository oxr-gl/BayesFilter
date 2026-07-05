# P85 Phase 4 Subplan: Minimal Configurable Basis/Domain Implementation

Date: 2026-06-23

Status: `DRAFT_PENDING_PHASE3_REVIEW`

## Phase Objective

Implement the minimal reviewed BayesFilter-owned setup configuration surface for
legacy Legendre bounded diagnostics and author-style `Lagrangep(4,8)` plus
`AlgebraicMapping(1)` configuration.

## Entry Conditions Inherited From Previous Phase

- Phase 3 has frozen exact files, tests, and commands in
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase3-implementation-test-matrix-result-2026-06-23.md`.
- Phase 4 code edits are approved by the reviewed Phase 3 result.
- CPU-hidden TensorFlow commands are exact and recorded.
- P84 Phase 2 fitting remains blocked.

## Required Artifacts

- Code changes limited to:
  - `bayesfilter/highdim/bases.py`;
  - `bayesfilter/highdim/source_route.py`;
  - `bayesfilter/highdim/__init__.py`;
  - `tests/highdim/test_p85_configurable_basis_domain.py`;
  - `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-subplan-2026-06-23.md`;
  - `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-result-2026-06-23.md`;
  - `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-subplan-2026-06-23.md`;
  - `docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-execution-ledger-2026-06-23.md`;
  - `docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-stop-handoff-2026-06-23.md`;
  - `docs/plans/bayesfilter-highdim-zhao-cui-p85-claude-review-ledger-2026-06-23.md`.
- Targeted tests limited to the Phase 3 test matrix.
- Phase 4 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-result-2026-06-23.md`
- Test logs or command summaries recorded in the result.
- Refreshed Phase 5 subplan.

## Required Checks / Tests / Reviews

Required checks:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p85_configurable_basis_domain.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p59_author_sir_36d_target_fit.py
```

```bash
git diff --check -- bayesfilter/highdim/bases.py bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p85_configurable_basis_domain.py docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-subplan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-result-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-subplan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-execution-ledger-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-stop-handoff-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-claude-review-ledger-2026-06-23.md
```

Claude read-only review is required for the implementation diff or Phase 4
result before Phase 5.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the local code expose a setup-configurable basis/domain surface that can represent author and legacy diagnostic routes distinctly? |
| Baseline/comparator | Phase 2 design, Phase 3 implementation matrix, and previous Legendre-only behavior. |
| Primary criterion | Targeted CPU-hidden tests pass; manifests distinguish basis/domain configs; legacy diagnostic tests remain compatible or are explicitly updated. |
| Veto diagnostics | TensorFlow GPU use without escalation; dynamic runtime basis dispatch inside compiled paths; missing manifest identity; third-party code copying; source-faithfulness overclaim. |
| Explanatory diagnostics | Basis dimensions, domain-map sample formulas, branch hashes, test output. |
| Not concluded | No fit quality, no posterior correctness, no production readiness, no XLA performance claim. |
| Artifact | Phase 4 result, code diff, and test summaries. |

## Forbidden Claims / Actions

- Do not copy third-party MATLAB code into BayesFilter production modules.
- Do not edit `bayesfilter/highdim/filtering.py`, which is dirty and outside
  the reviewed Phase 4 file list.
- Do not run author algebraic `Lagrangep` through full source-route fitting.
- Do not run fitting, validation ladders, GPU, HMC, LEDH, d=50/d=100, or long
  commands.
- Do not make the author basis route the default.
- Do not claim production readiness or P84 Phase 2 readiness from tests alone.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only if:

- targeted Phase 4 tests pass or a precise blocker is written;
- implementation diff is reviewed;
- manifest behavior needed for classification is available;
- CPU-only status is recorded for any TensorFlow test.

## Stop Conditions

Stop if:

- tests fail in a way that suggests design mismatch;
- implementation requires unreviewed file edits;
- TensorFlow attempts GPU execution in a CPU-hidden test;
- Claude review finds a material issue that cannot be patched within five
  rounds.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 4 result / close record;
3. draft or refresh the Phase 5 subplan;
4. review the Phase 5 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
