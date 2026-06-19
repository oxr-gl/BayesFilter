# W3-2 Subplan: Common Downstream Smoke

Date: 2026-06-19
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-master-program-2026-06-19.md`

## Phase Objective

Run both Wave 2 candidates on the same small deterministic fixtures and record
hard-veto downstream smoke status.  This phase detects obvious invalidity; it
does not rank algorithms.

## Entry Conditions Inherited From Previous Phase

- W3-1 artifact audit passed.
- Both Wave 2 JSON records are schema-valid and status-consistent.
- No ranking/default claim is authorized.

## Required Artifacts

- Diagnostic harness:
  `docs/benchmarks/scalable_ot_wave3_downstream_smoke.py`
- Focused tests:
  `tests/test_wave3_downstream_smoke.py`
- Smoke JSON:
  `docs/benchmarks/scalable-ot-wave3-downstream-smoke-2026-06-19.json`
- Smoke Markdown:
  `docs/benchmarks/scalable-ot-wave3-downstream-smoke-2026-06-19.md`
- W3-2 result.
- W3-3 subplan.

## Required Checks, Tests, And Reviews

Local checks:

```bash
pytest -q tests/test_wave3_downstream_smoke.py
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave3_downstream_smoke.py --mode smoke --output docs/benchmarks/scalable-ot-wave3-downstream-smoke-2026-06-19.json --markdown-output docs/benchmarks/scalable-ot-wave3-downstream-smoke-2026-06-19.md
```

Review:

- Codex skeptical audit before commands.
- Claude review is required if smoke fails in a way that needs interpretation
  beyond stated hard vetoes or if result wording changes boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can both candidates produce finite, shape-valid, normalized transported particles on shared deterministic fixtures without hard vetoes? |
| Baseline/comparator | Shared deterministic fixtures.  This is not a ranking comparator. |
| Primary pass criterion | Test and diagnostic command exit 0, status `PASS`, `WAVE3_DOWNSTREAM_SMOKE_PASSED_NO_RANKING`, hard vetoes `[]`, and rows exist for both candidates on each fixture. |
| Veto diagnostics | Nonfinite particles/factors, sign failure, shape mismatch, log-weight normalization failure, artifact audit failure, or diagnostic command failure. |
| Explanatory diagnostics | Moment deltas from input, wall time, candidate-specific residual metadata. |
| Not concluded | No ranking, speedup, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense equivalence, or broad scalable-OT selection. |
| Artifact preserving result | Smoke JSON/Markdown and W3-2 result. |

## Forbidden Claims And Actions

- Do not rank candidates.
- Do not compare wall time or moment deltas as promotion evidence.
- Do not change thresholds after seeing results.
- Do not edit candidate implementations unless a repair subplan is written and
  reviewed.

## Exact Next-Phase Handoff Conditions

W3-3 may begin only if smoke result exists and records pass/fail/blocker under
the predeclared contract, and W3-3 subplan passes Codex review.

## Stop Conditions

Stop if diagnostics fail for a non-repairable hard veto, require package/GPU/
network/public/default/shared-schema boundary, or need a forbidden claim to
interpret.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write W3-2 result.
3. Draft or refresh W3-3 subplan.
4. Review W3-3 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
