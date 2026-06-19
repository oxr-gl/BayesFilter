# W3-1 Subplan: Artifact Audit

Date: 2026-06-19
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-master-program-2026-06-19.md`

## Phase Objective

Verify that the two Wave 2 JSON artifacts exist, validate under the Phase 3
schema, preserve expected statuses and transport-object kinds, and are suitable
inputs for a common downstream smoke.

## Entry Conditions Inherited From Previous Phase

- W3-0 launch review passed.
- Wave 2 final merge exists and records both lanes diagnostic-only passed.
- W3-1 does not run downstream smoke; it only audits artifacts.

## Required Artifacts

- Wave 2 low-rank JSON:
  `docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.json`
- Wave 2 positive-feature JSON:
  `docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.json`
- Artifact audit JSON:
  `docs/benchmarks/scalable-ot-wave3-artifact-audit-2026-06-19.json`
- Artifact audit Markdown:
  `docs/benchmarks/scalable-ot-wave3-artifact-audit-2026-06-19.md`
- W3-1 result.
- W3-2 subplan.

## Required Checks, Tests, And Reviews

Local checks:

```bash
python -m py_compile docs/benchmarks/scalable_ot_wave3_downstream_smoke.py tests/test_wave3_downstream_smoke.py
pytest -q tests/test_wave3_downstream_smoke.py::test_wave3_artifact_audit_passes_existing_wave2_outputs
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave3_downstream_smoke.py --mode artifact-audit --output docs/benchmarks/scalable-ot-wave3-artifact-audit-2026-06-19.json --markdown-output docs/benchmarks/scalable-ot-wave3-artifact-audit-2026-06-19.md
```

Review:

- Codex skeptical audit before commands.
- Claude review only if artifact audit fails for a material planning/contract
  reason or if result wording changes evidence boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the two Wave 2 JSON artifacts present, schema-valid, status-consistent, and suitable for W3-2 smoke? |
| Baseline/comparator | Wave 2 final merge and the two Wave 2 JSON artifacts. |
| Primary pass criterion | Audit command exits 0 with status `PASS`, `WAVE3_ARTIFACT_AUDIT_PASSED`, empty hard vetoes, and Phase 3 schema validation for both candidate records. |
| Veto diagnostics | Missing JSON, missing candidate record, schema validation failure, unexpected Wave 2 status, non-empty Wave 2 hard vetoes, wrong transport kind, or materialized transport-object mismatch. |
| Explanatory diagnostics | Schema warnings and source/semantic class fields. |
| Not concluded | No downstream validity, no ranking, no default selection, no speedup/posterior/HMC/API/production readiness. |
| Artifact preserving result | Audit JSON/Markdown and W3-1 result. |

## Forbidden Claims And Actions

- Do not run W3-2 smoke in this phase.
- Do not edit Wave 2 artifacts to make the audit pass.
- Do not rank candidates or interpret metrics as superiority.

## Exact Next-Phase Handoff Conditions

W3-2 may begin only if artifact audit passes, W3-1 result exists, and W3-2
subplan passes Codex consistency/boundary review.

## Stop Conditions

Stop if artifacts are missing/invalid and cannot be repaired by rerunning
already reviewed Wave 2 commands without changing boundaries, or if continuing
would require editing shared schema/baseline or making a forbidden claim.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write W3-1 result.
3. Draft or refresh W3-2 subplan.
4. Review W3-2 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
