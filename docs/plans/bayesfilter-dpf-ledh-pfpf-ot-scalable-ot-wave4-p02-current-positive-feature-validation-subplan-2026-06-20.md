# W4-2 Subplan: Current Positive-Feature Lane

Date: 2026-06-20
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-master-program-2026-06-20.md`

## Phase Objective

Execute the current-agent positive-feature Sinkhorn lane on replicated
deterministic downstream resampling screens and write a lane close record.

## Entry Conditions Inherited From Previous Phase

- W4-0 launch review has passed local checks and Claude compact review.
- W4-1 peer low-rank task note has been written so the peer lane can execute
  independently while the current lane proceeds.
- Wave 2 positive-feature diagnostic result exists with empty hard vetoes.
- Wave 3 downstream smoke result exists with empty hard vetoes.
- No ranking/default/scientific claim is authorized.
- The peer low-rank lane remains independent and is not an input to W4-2.

## Required Artifacts

- Harness:
  `docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py`
- Test:
  `tests/test_wave4_positive_feature_validation.py`
- Official JSON result:
  `docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.json`
- Official Markdown result:
  `docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-positive-feature-result-2026-06-20.md`
- Updated execution ledger.

## Required Checks, Tests, And Reviews

Local checks:

```bash
python -m py_compile docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py tests/test_wave4_positive_feature_validation.py
pytest -q tests/test_wave4_positive_feature_validation.py
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py --mode full --output docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.md
```

Review:

- Codex skeptical audit before running the official diagnostic.
- Claude read-only review is required only if the diagnostic fails in a way
  that would require a material repair or if the result note makes a material
  interpretation decision.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the positive-feature Sinkhorn semantic-replacement lane remain viable under replicated deterministic downstream resampling screens? |
| Baseline/comparator | Exact weighted input estimates are the downstream reference.  Naive uniform-no-transport estimates are explanatory only. |
| Primary pass criterion | Harness/test/official diagnostic exit 0; hard vetoes are empty; transported particles are finite and shape-valid; output log weights are normalized uniform; features/scalings are finite and positive as applicable; row/column residuals are <= `5.0e-2`; max weighted-mean error is <= `3.0e-1`; max weighted second-moment error is <= `1.0`; manifest contains exact argv, output paths, planned result path, seeds, fixtures, and total wall time. |
| Veto diagnostics | Missing Wave 2/Wave 3 entry artifacts, nonfinite output or diagnostics, nonpositive features, shape mismatch, log-weight normalization residual above `1.0e-10`, residual threshold failure, moment screen threshold failure, missing manifest field, unsupported claim, or official command failure. |
| Explanatory diagnostics | Naive estimator errors, candidate-vs-naive differences, wall time, per-fixture/per-seed tables, feature count, epsilon, and descriptive summaries. |
| Not concluded | No ranking, speedup, superiority, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, or broad scalable-OT selection. |
| Artifact preserving result | Official JSON/Markdown diagnostics and W4-2 phase result. |

## Forbidden Claims And Actions

- Do not compare against the peer lane in W4-2.
- Do not promote candidate-vs-naive deltas into ranking evidence.
- Do not change thresholds after seeing W4-2 results.
- Do not edit public exports/defaults, Phase 1 fixtures, Phase 3 schema, or
  unrelated dirty files.

## Exact Next-Phase Handoff Conditions

W4-3 may begin only if:

- W4-2 checks and official diagnostic pass or a blocker result is written;
- W4-2 result note exists and preserves nonclaims;
- peer low-rank lane artifacts exist;
- W4-3 subplan exists and passes Codex consistency review.

If peer artifacts are absent after W4-2, write a visible stop handoff rather
than running final merge.

## Stop Conditions

Stop and write a blocker result if the current-lane diagnostic fails due to an
unfixable candidate hard veto, an unsupported claim cannot be repaired, or a
repair would require changing thresholds, package installation, network fetch,
GPU evidence, public/default/API edits, or peer-lane edits.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write W4-2 result.
3. Draft or refresh W4-3 subplan.
4. Review W4-3 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.

