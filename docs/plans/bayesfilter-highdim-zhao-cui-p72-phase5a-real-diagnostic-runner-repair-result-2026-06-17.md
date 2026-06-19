# P72 Phase 5a Result: Real Diagnostic Runner Repair

metadata_date: 2026-06-17
status: PHASE5A_REPAIRED_REAL_DEFAULT_RUNNER_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5a-real-diagnostic-runner-repair-subplan-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-skeptical-audit-blocker-result-2026-06-17.md
smoke_artifact: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5a-runner-smoke-2026-06-17.json
phase5_artifact: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Is the P72 script now capable of producing a real bounded diagnostic JSON rather than schema-only or smoke-only output? |
| Baseline/comparator | The Phase 4 schema-only script, the Phase 5 skeptical-audit blocker, and Claude's Phase 5a implementation R1 finding that the default path still emitted smoke rather than real bounded rows. |
| Primary criterion | The default no-flag command must execute real bounded Phase 5 rows, while `--schema-only` and `--smoke-only` remain explicit non-Phase-5 paths. Each real row must emit structured gate evidence or an explicit structured skip/block, not a top-level row exception for known gate failures. |
| Veto diagnostics | Default command still schema-only or smoke-only, audit data enters training, missing direct targets, missing normalizer/provenance/line/condition/rank gates, threshold drift, source-faithfulness overclaim, or known normalizer-floor failure escaping only as a top-level exception row. |
| Decision | Phase 5a runner repair is implemented and locally checked; pending Claude read-only review. |
| Not concluded | No repaired lower-gate pass, no d18 validation, no HMC readiness, no scaling or rank/degree promotion. |

## Repair Summary

- `scripts/p72_support_certified_lower_gate_diagnostic.py` keeps
  `--schema-only` as the explicit schema path and `--smoke-only` as a tiny
  implementation check.
- The default no-flag command now calls `p72_phase5_payload(...)` and executes
  the bounded real Phase 5 rows.
- `_normalizer_terms(...)` now catches `NORMALIZER_FLOOR_EXCEEDED` from the
  transport density normalizer and passes it to the P72 normalizer gate as
  structured diagnostic evidence.
- `p72_full_normalizer_gate(...)` now treats a recorded
  `normalizer_exception` as a normalizer veto.
- If step 1 has a normalizer exception that prevents forming an admissible
  retained object, the row now records a structured step-2 skip:
  `prior_step_gate_blocked_no_retained_object`.
- Known gate failures therefore remain blocks, but they no longer erase the
  available step evidence behind a top-level row exception.

## Local Checks

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
- Warnings were TensorFlow Probability `distutils` deprecation warnings.

Passed:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p72_support_certified_lower_gate_diagnostic.py --output docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json
```

Result:

- status: `P72_PHASE5_SUPPORT_CERTIFIED_LOWER_GATE_BLOCKED`
- gate summary: `overall_status = block`
- `phase5_diagnostic_executed = true`
- `smoke_only_not_phase5_evidence = false`
- `schema_only_sentinel_present = false`

Passed:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json
```

Sentinel/exception absence check:

```bash
rg -n "exception_type|p72_phase5_row_exception_fail_closed|schema_only_sentinel_present.*true|smoke_only_not_phase5_evidence.*true" docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json
```

Result:

- exit code `1`;
- no matches;
- interpreted as pass evidence because the real artifact must not contain the
  old fail-closed exception row, schema-only sentinel, or smoke-only marker.

## Boundary Notes

- No thresholds or seeds were changed.
- Audit data was not used for coefficient selection.
- No `bayesfilter/highdim/fitting.py` edit was made for Phase 5a.
- No source-faithfulness claim was made for P72 guard/audit/line gates.
- The real Phase 5 diagnostic still blocks both bounded rows.  This is a
  diagnostic result, not a repaired lower-gate success.

## Handoff

Claude agreed this Phase 5a repair together with the Phase 5 diagnostic result
and artifact.  Phase 5 closes as a blocked real diagnostic, and the next
subplan is a root-cause plan, not validation or promotion.
