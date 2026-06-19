# P72 Phase 4 Subplan: Focused Implementation And Unit Tests

metadata_date: 2026-06-17
status: READY_FOR_PHASE4_EXECUTION_AFTER_CLAUDE_R5_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Implement only the Phase 3-authorized P72 support-certified lower-gate
surfaces and focused tests.  Phase 4 must make the repaired path executable
for Phase 5, but it must not run the Phase 5 bounded diagnostic or claim that
the repair works.

## Entry Conditions Inherited From Phase 3

Phase 4 may begin only if:

- Phase 3 result exists and maps every mandatory Phase 2 design element to an
  implementation surface:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-result-2026-06-17.md`;
- this Phase 4 subplan exists and lists exact authorized files/functions/tests;
- local Phase 3 checks passed;
- Claude returns `VERDICT: AGREE` for Phase 3 result and this subplan;
- Phase 2 thresholds remain frozen and unchanged;
- no Phase 5 repaired diagnostic, downstream validation, d18 validation, HMC,
  or GPU diagnostic has run in P72.

## Authorized Edit Surfaces

Phase 4 may edit:

- `bayesfilter/highdim/source_route.py`;
- `bayesfilter/highdim/__init__.py`, only for subpackage-scoped exports of new
  P72 helpers/constants;
- new script `scripts/p72_support_certified_lower_gate_diagnostic.py`;
- new tests `tests/highdim/test_p72_support_certified_lower_gate.py`;
- existing focused tests only if required by changed import/export paths.

Phase 4 is also authorized to write its required non-code artifacts under
`docs/plans`: the Phase 4 result, Phase 5 subplan, execution ledger, and
Claude review ledger.

Conditional edit:

- `bayesfilter/highdim/fitting.py` may be edited only to expose singular-value
  or effective-rank diagnostics already computed by the scaled augmented solve.
  It must not change the objective, solver backend, solver thresholds, default
  backend, or non-P72 behavior.  The existing hard solver-veto compatibility
  threshold remains `1e14`; P72 `kappa_max=1e10` is a wrapper/admission gate.

## Required Artifacts

Phase 4 must produce:

- Phase 4 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-result-2026-06-17.md`;
- implemented P72 helper surfaces and tests;
- local test/check evidence;
- updated execution and review ledgers;
- refreshed Phase 5 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-subplan-2026-06-17.md`.

## Required Implementation Contents

Implementation must include:

- code constants for Phase 2 seeds, thresholds, line fractions, and nonclaims;
- cloud construction preserving `Z_fit`, `Z_guard`, and `Z_audit` roles;
- guard-line augmentation entering training only through `Z_guard`;
- audit-line probes never entering coefficient selection;
- direct target evaluation for every guard, audit, and line point;
- support/clipping coverage diagnostics for fit, guard, holdout, and replay
  clouds;
- fit wrapper using TensorFlow tensors and the existing fixed ALS fitter;
- P72 gate summary covering residual, line, full normalizer, support/clipping,
  provenance, condition, effective-rank, and rank-activity gates;
- diagnostic script schema ready to run Phase 5 and write JSON;
- manifest fields that prove audit data was not used for coefficient
  selection, and that target/frame/shift/cloud/line hashes were recorded.

## Required Checks And Tests

Before code edits:

```bash
git status --short
```

After implementation:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p72_support_certified_lower_gate_diagnostic.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p72_support_certified_lower_gate.py
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py bayesfilter/highdim/fitting.py scripts/p72_support_certified_lower_gate_diagnostic.py tests/highdim/test_p72_support_certified_lower_gate.py docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md
```

If Phase 4 edits an existing focused test file other than the new P72 test,
include that file in the final `git diff --check` command and record the
reason in the Phase 4 result.

Use `CUDA_VISIBLE_DEVICES=-1` because Phase 4 tests are CPU-only focused tests
and are not GPU evidence.

Review:

- Claude read-only review of implementation diff, Phase 4 result, and Phase 5
  subplan.
- If Claude returns `VERDICT: REVISE`, patch visibly and rerun focused checks.
  Stop after five rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Did Phase 4 implement the exact P72 support-certified lower-gate surfaces and focused tests required for Phase 5? |
| Baseline/comparator | Phase 2 design contract, Phase 3 surface map, current P70/P71 fixed-branch implementation, and focused synthetic tests. |
| Primary criterion | Focused tests and local checks pass, implementation covers every mandatory Phase 2 gate, audit clouds are not used for coefficient selection, and Claude agrees the implementation stays inside authorized surfaces. |
| Veto diagnostics | Phase 2 threshold changes; audit cloud enters training; missing line target evaluation; missing support/provenance/full-normalizer gate; lowering the low-level solver veto to `1e10`; NumPy algorithmic backend; downstream diagnostic run; source-faithfulness overclaim; shape/stable-LS/Christoffel candidate added; unrelated refactor. |
| Explanatory only | Runtime estimates, synthetic-test magnitudes, code organization choices, and future refactor notes. |
| Not concluded | No repaired lower-gate pass, no validation, no d18 correctness, no scaling, no HMC readiness, no source-faithfulness closure for guard/stability additions. |
| Artifact preserving result | Phase 4 result, code diff, test output, execution ledger, review ledger, and Phase 5 subplan. |

## Forbidden Claims And Actions

- Do not run Phase 5 repaired diagnostic.
- Do not run downstream validation, d18 validation, HMC, or GPU diagnostics.
- Do not change Phase 2 thresholds or cloud seeds.
- Do not lower the low-level solver condition veto from `1e14` to `1e10`;
  enforce `1e10` only as a P72 wrapper/admission gate.
- Do not use audit clouds or audit-line points for coefficient selection.
- Do not add quarantined shape, derivative, stable-LS, Christoffel, leverage,
  or oversampling logic.
- Do not claim source-faithfulness for P72 guard/audit/line/admission gates.
- Do not edit unrelated files.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only if:

- Phase 4 result exists and records all checks/tests;
- implemented code exposes a runnable P72 diagnostic script;
- focused tests pass;
- local diff check passes;
- Phase 5 subplan exists with a serious-run evidence contract and manifest
  requirements;
- Claude returns `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- implementation requires changing Phase 2 thresholds;
- implementation requires lowering the low-level solver veto rather than
  applying the P72 condition rule as an admission gate;
- target evaluation for guard/audit/line points cannot be implemented without
  unreviewed source-route changes;
- audit/guard separation cannot be proven in manifests or tests;
- TensorFlow implementation cannot be kept without package or backend changes;
- tests reveal a design gap requiring Phase 2/3 revision;
- Claude and Codex do not converge after five review rounds for the same
  blocker;
- the user redirects the lane.

## Skeptical Plan Audit

This implementation phase is narrow because Phase 3 mapped the surfaces.  The
main risk is accidentally treating synthetic tests or schema checks as a
scientific repair.  The phase controls that risk by not running Phase 5 and by
stating that focused tests only prove implementation behavior and gate wiring.
