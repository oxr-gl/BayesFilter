# Wave 3 Result: Comparative/Downstream Smoke

Date: 2026-06-19
Supervisor/executor: Codex

## Status

`WAVE3_DOWNSTREAM_SMOKE_COMPLETED_BOTH_CANDIDATES_PASSED_HARD_VETO_NO_RANKING`

## Result Summary

Wave 3 completed the planned no-ranking downstream/common smoke.  The Wave 2
candidate artifacts passed audit, and both candidates produced finite,
shape-valid, normalized transported particles on the shared deterministic smoke
fixtures without hard vetoes.

This is a hard-veto smoke only.  It is not an algorithm ranking or a default
selection.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the two Wave 2 candidates pass a common deterministic downstream smoke harness without hard vetoes, while preserving diagnostic-only boundaries? |
| Baseline/comparator | Wave 2 final merge and Wave 2 candidate JSON artifacts; shared deterministic fixtures for hard-veto smoke only. |
| Primary criterion | Passed. Wave 2 JSON artifacts validate; Wave 3 harness/test/diagnostic commands exited 0; both candidates produced finite transported particles with valid shapes and normalized output weights; final result preserves no-ranking/non-default boundaries. |
| Veto diagnostics | None fired. |
| Explanatory diagnostics | Moment deltas from input, wall time, candidate-specific residual metadata, and fixture shapes. |
| Not concluded | No speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or scientific superiority. |

## Phase Results

| Phase | Status | Artifact |
| --- | --- | --- |
| W3-0 launch review | `W3_0_LAUNCH_REVIEW_PASSED` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p00-launch-review-result-2026-06-19.md` |
| W3-1 artifact audit | `W3_1_ARTIFACT_AUDIT_PASSED` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p01-artifact-audit-result-2026-06-19.md` |
| W3-2 downstream smoke | `W3_2_DOWNSTREAM_SMOKE_PASSED_NO_RANKING` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p02-downstream-smoke-result-2026-06-19.md` |

## Checks Run

```bash
python -m py_compile docs/benchmarks/scalable_ot_wave3_downstream_smoke.py tests/test_wave3_downstream_smoke.py
pytest -q tests/test_wave3_downstream_smoke.py::test_wave3_artifact_audit_passes_existing_wave2_outputs
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave3_downstream_smoke.py --mode artifact-audit --output docs/benchmarks/scalable-ot-wave3-artifact-audit-2026-06-19.json --markdown-output docs/benchmarks/scalable-ot-wave3-artifact-audit-2026-06-19.md
pytest -q tests/test_wave3_downstream_smoke.py
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave3_downstream_smoke.py --mode smoke --output docs/benchmarks/scalable-ot-wave3-downstream-smoke-2026-06-19.json --markdown-output docs/benchmarks/scalable-ot-wave3-downstream-smoke-2026-06-19.md
```

Observed:

- launch syntax check: passed;
- artifact audit pytest: `1 passed`;
- artifact audit diagnostic: exited 0;
- full smoke pytest: `2 passed`;
- downstream smoke diagnostic: exited 0.

## Diagnostic Artifacts

- Artifact audit JSON:
  `docs/benchmarks/scalable-ot-wave3-artifact-audit-2026-06-19.json`
- Artifact audit Markdown:
  `docs/benchmarks/scalable-ot-wave3-artifact-audit-2026-06-19.md`
- Downstream smoke JSON:
  `docs/benchmarks/scalable-ot-wave3-downstream-smoke-2026-06-19.json`
- Downstream smoke Markdown:
  `docs/benchmarks/scalable-ot-wave3-downstream-smoke-2026-06-19.md`

## Smoke Summary

| Metric | Value | Role |
| --- | ---: | --- |
| hard vetoes | `[]` | hard veto |
| rows | `4` | hard-veto context |
| max mean delta from input | `1.239000e-01` | explanatory |
| max variance delta from input | `1.659154e-01` | explanatory |
| max wall time seconds | `8.784064e-02` | explanatory |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for artifact audit and deterministic downstream smoke. |
| Statistically supported ranking | None.  No uncertainty analysis or replicated comparison was run. |
| Descriptive-only differences | Moment deltas, wall time, residual metadata, and fixture-specific rows are descriptive only. |
| Default-readiness | Not assessed and not claimed. |
| Next evidence needed | A new reviewed comparative/downstream validation plan with baseline ladder and uncertainty requirements before any ranking or default discussion. |

## Post-Run Red Team

Strongest alternative explanation: the deterministic smoke fixtures are too
small and too benign to reveal downstream filtering failure modes.

What would overturn this result: a replay finds nonfinite outputs, shape/log
weight failures, invalid Wave 2 artifacts, or a hidden interpretation that
promotes explanatory moment/runtime deltas into ranking evidence.

Weakest evidence point: no stochastic replication, posterior diagnostic,
filtering benchmark, or uncertainty analysis was run.

## Non-Claims

- No speedup claim.
- No ranking claim.
- No posterior correctness claim.
- No HMC readiness claim.
- No public API readiness claim.
- No production or default readiness claim.
- No dense Sinkhorn equivalence claim.
- No broad scalable-OT selection claim.
- No scientific superiority claim.

## Close Record

Wave 3 is complete.  No automatic next phase is launched.
