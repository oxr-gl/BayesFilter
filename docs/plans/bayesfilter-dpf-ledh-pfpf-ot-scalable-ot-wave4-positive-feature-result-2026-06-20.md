# W4-2 Result: Current Positive-Feature Lane

Date: 2026-06-20
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-master-program-2026-06-20.md`

## Status

`WAVE4_POSITIVE_FEATURE_VALIDATION_PASSED_HARD_SCREEN_NO_RANKING`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the positive-feature Sinkhorn semantic-replacement lane remain viable under replicated deterministic downstream resampling screens? |
| Baseline/comparator | Exact weighted input estimates were the downstream reference.  Naive uniform-no-transport estimates were recorded as explanatory only. |
| Primary criterion | Passed. Focused tests and official diagnostic exited 0; hard vetoes were empty; transported particles were finite and shape-valid; output log weights were normalized; features/scalings were finite and positive; residual and moment thresholds passed; required manifest fields were present. |
| Veto diagnostics | None fired. |
| Explanatory diagnostics | Naive estimator errors, candidate-vs-naive deltas, wall time, per-fixture/per-seed rows, feature count, epsilon, and residual magnitudes. |
| Not concluded | No ranking, speedup, superiority, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, or broad scalable-OT selection. |

## Checks Run

```bash
python -m py_compile docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py tests/test_wave4_positive_feature_validation.py
pytest -q tests/test_wave4_positive_feature_validation.py
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py --mode full --output docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.md
python -m json.tool docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.json
```

Observed:

- py_compile passed;
- focused tests: `2 passed`;
- official diagnostic exited 0;
- JSON parsed successfully.

TensorFlow emitted a CUDA no-device line during the CPU-scoped diagnostic even
with `CUDA_VISIBLE_DEVICES=-1`.  This is recorded as environment noise from a
deliberate CPU-scoped run, not GPU evidence.

## Diagnostic Artifacts

- JSON:
  `docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.json`
- Markdown:
  `docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.md`

## Summary

| Metric | Value | Role |
| --- | ---: | --- |
| rows | `9` | hard-veto context |
| hard vetoes | `0` | hard veto |
| max candidate weighted mean error | `2.220446e-16` | hard veto |
| max candidate weighted second moment error | `5.218177e-01` | hard veto |
| max transport residual | `3.079331e-05` | hard veto |
| max wall time seconds | `3.913630e-02` | explanatory |
| ranking statistically supported | `False` | inference status |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Current positive-feature lane remains viable for later validation. | Passed hard screen. | No vetoes fired. | This is a replicated resampling-step moment screen, not full filtering/posterior/HMC validation. | Wait for peer low-rank lane artifacts, then run W4-3 final merge. | No ranking, default, speedup, posterior correctness, HMC readiness, public API readiness, or dense equivalence. |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for current positive-feature lane. |
| Statistically supported ranking | None.  This lane does not compare against the peer lane. |
| Descriptive-only differences | Naive uniform errors, candidate-minus-naive deltas, per-seed rows, and wall time. |
| Default-readiness | Not assessed and not claimed. |
| Next evidence needed | Peer low-rank Wave 4 result and final merge artifact audit. |

## Run Manifest

| Field | Value |
| --- | --- |
| git commit | `b4156c4b0cbfdc443440fc6df4b6044e09040abb` |
| command | `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py --mode full --output docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.md` |
| Python | `3.13.13` |
| TensorFlow | `2.20.0` |
| device scope | CPU-scoped; GPU hidden with `CUDA_VISIBLE_DEVICES=-1` |
| fixtures | `weighted_curve`, `bimodal_tail`, `high_dim_low_rank` |
| seeds | `101`, `202`, `303` |
| wall time | `0.230608` seconds in JSON manifest |
| plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p02-current-positive-feature-validation-subplan-2026-06-20.md` |
| result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-positive-feature-result-2026-06-20.md` |
| output artifacts | JSON and Markdown diagnostic artifacts listed above |

## Post-Run Red Team

Strongest alternative explanation: the moment screen is too limited to reveal
filtering or posterior failures that would appear in a longer downstream
filtering benchmark.

What would overturn this result: replay with the same contract finds nonfinite
outputs, shape/log-weight failures, residual failures, moment threshold
failures, missing required manifest fields, or unsupported claims.

Weakest evidence point: no peer comparison, paired uncertainty analysis, full
filtering benchmark, posterior validation, HMC diagnostic, or public/default API
assessment was run.

## Next-Phase Review

W4-3 subplan exists and was reviewed during launch.  It is consistent with the
W4-2 result, but W4-3 cannot start until the peer low-rank lane writes its
required artifacts.

