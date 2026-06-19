# P72 Phase 5 Result: Repaired Lower-Gate Diagnostic

metadata_date: 2026-06-17
status: P72_PHASE5_SUPPORT_CERTIFIED_LOWER_GATE_BLOCKED_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-subplan-2026-06-17.md
diagnostic_json: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5a-real-diagnostic-runner-repair-result-2026-06-17.md

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Does the support-certified fixed-fit gate reduce the P70 Phase 6h off-cloud/conditioning blocker on bounded diagnostic rows? |
| Baseline/comparator | P70 Phase 6h root-cause probes. |
| Primary criterion | Every bounded row and both time steps must pass residual, line, support, normalizer, provenance, condition/effective-rank, and rank-activity gates, with audit clouds excluded from coefficient selection. |
| Veto diagnostics | Any residual, line, support, normalizer, provenance, condition/effective-rank, rank-activity, schema, or source-faithfulness-overclaim block. |
| Decision | Block.  The repaired runner executed real bounded rows, but both rows failed primary gates. |
| Not concluded | No d18 validation, no HMC readiness, no scaling claim, no rank/degree promotion, and no source-faithful adaptive Zhao--Cui parity claim. |

## Run Manifest

| Field | Value |
| --- | --- |
| Command | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p72_support_certified_lower_gate_diagnostic.py --output docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json` |
| CPU/GPU | CPU-only by intent, `CUDA_VISIBLE_DEVICES=-1`; TensorFlow printed CUDA initialization warnings that are not GPU evidence. |
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json` |
| Wall time | `296.393` seconds recorded in JSON. |
| Git state | Dirty worktree; JSON records head `94069066a70df6f1f0f2b53d32b9d452bd67f891` and dirty status count. |
| Row specs | `rank_candidate_1_2_fit36`: degree 1, rank 2, fit count 36; `rank_stronger_1_3_fit36`: degree 1, rank 3, fit count 36. |

## Diagnostic Findings

The real diagnostic artifact reports:

- `status = P72_PHASE5_SUPPORT_CERTIFIED_LOWER_GATE_BLOCKED`
- `gate_summary.overall_status = block`
- `phase5_diagnostic_executed = true`
- `smoke_only_not_phase5_evidence = false`
- `schema_only_sentinel_present = false`

### `rank_candidate_1_2_fit36`

Step 1 blocks on line and residual gates:

- summary reasons: `line_block`, `residual_rms_veto`,
  `residual_max_veto`;
- residual RMS relative: approximately `157700.3535`;
- residual max relative: approximately `852563.5968`;
- normalizer gate passes;
- condition/effective-rank gate passes;
- guard, holdout, and replay line channels block.

Step 2 blocks on line, condition, and residual gates:

- summary reasons: `line_block`, `condition_effective_rank_block`,
  `residual_rms_veto`;
- residual RMS relative: approximately `35.7120`;
- residual max relative: approximately `193.5279`;
- normalizer gate passes;
- condition/effective-rank gate blocks with
  `p72_condition_admission_veto`;
- maximum condition number: approximately `3.479494444576792e11`;
- holdout line channel blocks.

### `rank_stronger_1_3_fit36`

Step 1 blocks more severely:

- summary reasons: `normalizer_block`, `line_block`,
  `condition_effective_rank_block`, `residual_rms_veto`,
  `residual_max_veto`;
- residual RMS relative: approximately `13136397.6178`;
- residual max relative: approximately `78729308.4401`;
- normalizer gate blocks with `NORMALIZER_FLOOR_EXCEEDED`;
- condition/effective-rank gate blocks with
  `p72_condition_admission_veto`;
- maximum condition number: approximately `4.145755152253643e14`;
- guard, holdout, and replay line channels block.

Step 2 is intentionally not fitted:

- skip reason: `prior_step_gate_blocked_no_retained_object`;
- normalizer gate records
  `prior_step_gate_blocked_no_transport_normalizer`;
- this replaces the earlier top-level row exception with structured gate
  evidence and avoids pretending a valid retained object exists.

## Decision Table

| Decision | Primary Criterion | Veto Diagnostics | Main Uncertainty | Next Justified Action | Not Concluded |
| --- | --- | --- | --- | --- | --- |
| Block Phase 5 | Failed: both rows block | Residual/line failures persist; candidate row step 2 condition fails; stronger row step 1 normalizer and condition fail | Whether the failure is caused by support construction, target scaling, rank/degree/sample budget, line target geometry, or fixed-fit objective mismatch | Draft Phase 6 root-cause subplan focused on discriminating those causes | No validation failure of the adaptive author algorithm; no HMC readiness or scaling claim |

## Checks

Passed:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p72_support_certified_lower_gate_diagnostic.py
```

Passed:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p72_support_certified_lower_gate.py
```

Result:

- `14 passed, 2 warnings`

Passed:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json
```

Passed as sentinel absence:

```bash
rg -n "exception_type|p72_phase5_row_exception_fail_closed|schema_only_sentinel_present.*true|smoke_only_not_phase5_evidence.*true" docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json
```

Result:

- exit code `1`;
- no matches.

## Handoff

Claude agreed that this is a valid blocked diagnostic closeout and that the
structured normalizer exception reports the blocker rather than hiding it.  The
next phase must not validate or promote P72.  It should create a root-cause
plan for the remaining residual/line/conditioning/normalizer failures.
