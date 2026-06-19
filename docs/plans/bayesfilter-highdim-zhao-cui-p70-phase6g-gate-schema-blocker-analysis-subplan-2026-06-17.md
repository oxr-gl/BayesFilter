# P70 Phase 6g Subplan: Gate Schema And Blocker Analysis

metadata_date: 2026-06-17
status: DRAFT_FOR_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Repair the P70 Phase 6 gate/reporting schema defects found during the Phase 6f
result audit, then test that the saved Phase 6f artifact is classified for the
right reasons.  Phase 6g may also write a blocker analysis explaining the two
remaining scientific/numerical failures:

- first-row holdout/replay residuals remain enormous despite small fit
  residuals;
- the rank-3 row still reaches a scaled augmented condition-number veto.

Phase 6g is a reporting and blocker-analysis phase.  It must not rerun the
expensive four-row diagnostic, retune thresholds, or unblock Phase 7.

## Entry Conditions Inherited From Phase 6f

Phase 6g may begin only after:

- Phase 6f result exists and is accepted with Claude `VERDICT: AGREE`;
- Phase 6f JSON exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6f-stable-als-diagnostic-rerun-2026-06-16.json`;
- Phase 6f failed with `gate_summary.overall_status = fail`;
- Phase 7 remains blocked;
- the two Phase 6f reporting defects are explicitly known:
  `sqrt_square_normalizer` versus `sqrt_tt_normalizer`, and NumPy scalar
  residual rejection in `_finite_float`.

## Required Artifacts

- this Phase 6g subplan;
- code patch limited to:
  `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py`;
- focused tests limited to:
  `tests/highdim/test_p70_phase6_diagnostic_script.py`;
- a mandatory saved-artifact re-gate output derived from the saved Phase 6f
  JSON only:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6g-saved-phase6f-regate-2026-06-17.json`;
- Phase 6g result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6g-gate-schema-blocker-analysis-result-2026-06-17.md`;
- updates to the P70 execution and Claude review ledgers.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the P70 gate correctly read the existing row schema and finite scalar residuals, so that the saved Phase 6f artifact fails for the actual lower-gate reasons rather than reporting artifacts? |
| Baseline/comparator | Saved Phase 6f JSON and Phase 6f result note. |
| Primary criterion | Focused tests pass, including synthetic pre-serialization NumPy scalar coverage for residuals, and re-gating the saved Phase 6f rows removes `missing_sqrt_tt_normalizer` while preserving failure by holdout/replay normalized residual veto and captured rank-3 condition veto. |
| Veto diagnostics | Any threshold change; any diagnostic rerun; any row/rank/degree/ridge/sweep/initializer change; any Phase 7 command; any claim that the fixed variant works; any source-faithfulness closure for the stable ALS repair. |
| Explanatory only | Raw residual magnitudes, fit residuals, condition summaries, normalizer magnitudes, and blocker hypotheses. |
| Not concluded | No d18 correctness, no rank/degree promotion, no scaling claim, no HMC readiness, no adaptive Zhao--Cui parity, no author-code failure claim, no claim that the original bug is fixed. |
| Artifact preserving result | Phase 6g result note and focused test output. |

## Required Checks, Tests, And Reviews

Before patching:

- skeptical plan audit against wrong baseline, proxy promotion, missing stop
  conditions, hidden threshold changes, and stale artifact assumptions;
- Claude read-only review of this subplan.

After patching:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p70_phase6_diagnostic_script.py
```

Then run a local saved-artifact re-gate that imports the P70 gate and applies it
to the existing Phase 6f JSON rows.  This re-gate is a cheap reporting check,
not a diagnostic rerun.  It must write:

`docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6g-saved-phase6f-regate-2026-06-17.json`.

The saved JSON re-gate can verify the normalizer field-name repair and the
preserved failure outcome.  It cannot by itself prove pre-serialization NumPy
scalar handling, because an already-written artifact may have converted or lost
the original scalar type.  That scalar handling must be proven by focused
synthetic unit tests.

Run:

```bash
git diff --check -- scripts/p70_phase6_rank_channel_normalizer_diagnostic.py tests/highdim/test_p70_phase6_diagnostic_script.py docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6g-gate-schema-blocker-analysis-subplan-2026-06-17.md
```

After the result note is written, ask Claude for a read-only execution/result
review.

## Forbidden Claims And Actions

- Do not rerun `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py` as a
  four-row diagnostic.
- Do not change any Phase 6 gate threshold.
- Do not alter row specs, ranks, degrees, ridge, sweep count, initialization,
  seeds, model, or fit sample counts.
- Do not proceed to Phase 7.
- Do not claim fixed-variant success.
- Do not call stable ALS `source_faithful`; it remains
  `fixed_hmc_adaptation`.
- Do not treat smaller fit residuals or corrected reporting as promotion
  evidence.

## Exact Next-Phase Handoff Conditions

Phase 6g may close only after:

- the focused tests pass;
- saved Phase 6f re-gate confirms `missing_sqrt_tt_normalizer` is removed where
  `sqrt_square_normalizer` is available, and synthetic tests confirm finite
  NumPy scalar residuals are not rejected;
- the saved Phase 6f result still fails by first-row holdout/replay normalized
  residual veto and second-row condition-number veto;
- Phase 6g result is written;
- Claude returns `VERDICT: AGREE` on the execution/result, or a blocker is
  recorded.

The next phase must be a new Phase 6h root-cause subplan if we want to test
scientific/numerical hypotheses for the residual explosion or rank-3
conditioning.  Phase 7 remains blocked.

## Stop Conditions

Stop and write a blocker if:

- Claude rejects this subplan for a material boundary or evidence-contract
  issue that cannot be patched locally;
- focused tests fail for a reason that is not a straightforward test/code
  mismatch;
- the mandatory saved-artifact re-gate cannot be written;
- saved-artifact re-gating changes the overall failure outcome to pass;
- any required repair would require threshold, row, model, or algorithmic
  changes beyond reporting/schema handling;
- a command would require a new expensive diagnostic rerun.

## Skeptical Plan Audit

This plan uses the saved failed Phase 6f artifact as the baseline.  It does not
use fit residual, cleaner schema, or absence of false nonfinite labels as a
promotion criterion.  The pass/fail criterion is purely reporting correctness:
the saved rows must still fail, but for the correct mathematical/numerical
reasons.  No hidden Phase 7 dependency is produced by this phase; Phase 6g can
only hand off to another blocker/root-cause phase.
