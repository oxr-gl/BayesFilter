# PF-I1 Closeout Result: Positive-Feature Independent Lane

Date: 2026-06-20
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-master-program-2026-06-20.md`

## Status

`POSITIVE_FEATURE_INDEPENDENT_VALIDATION_PASSED_HARD_SCREEN_NO_RANKING`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the positive-feature Sinkhorn semantic-replacement lane remain viable under an independent replicated downstream resampling hard screen? |
| Baseline/comparator | Exact weighted input estimates were the downstream reference.  Naive uniform-no-transport and dense-reference deltas remain explanatory only. |
| Primary criterion | Passed. Focused tests and official independent diagnostic exited 0; hard vetoes were empty; transported particles were finite and shape-valid; output log weights were normalized; features/scalings were finite and positive; residual and moment thresholds passed; manifest paths point to independent-lane artifacts. |
| Veto diagnostics | None fired. |
| Explanatory diagnostics | Naive estimator errors, candidate-vs-naive deltas, wall time, per-fixture/per-seed rows, feature count, epsilon, and residual magnitudes. |
| Not concluded | No ranking, speedup, superiority, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, or broad scalable-OT selection. |

## Checks Run

```bash
python -m py_compile docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py tests/test_wave4_positive_feature_validation.py experiments/dpf_implementation/tf_tfp/resampling/positive_feature_transport_tf.py
pytest -q tests/test_positive_feature_transport_tf.py tests/test_wave4_positive_feature_validation.py
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py --mode full --program-id positive_feature_independent_lane --pass-status POSITIVE_FEATURE_INDEPENDENT_VALIDATION_PASSED_HARD_SCREEN_NO_RANKING --fail-status POSITIVE_FEATURE_INDEPENDENT_VALIDATION_FAILED_HARD_SCREEN --report-title "Positive-Feature Independent Validation" --plan-path docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-p01-replay-closeout-subplan-2026-06-20.md --result-path docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-closeout-result-2026-06-20.md --next-evidence-needed "future coordinator comparison or larger filtering/posterior/HMC validation only after independent lane closeouts" --output docs/benchmarks/scalable-ot-positive-feature-independent-validation-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-positive-feature-independent-validation-2026-06-20.md
python -m json.tool docs/benchmarks/scalable-ot-positive-feature-independent-validation-2026-06-20.json
```

Observed:

- `py_compile`: passed.
- Focused tests: `4 passed`.
- Official independent diagnostic: exited 0.
- JSON parse: passed.
- TensorFlow emitted a CUDA no-device line during the deliberate CPU-scoped
  diagnostic with `CUDA_VISIBLE_DEVICES=-1`; this is recorded as environment
  noise, not GPU evidence.

## Diagnostic Artifacts

- JSON:
  `docs/benchmarks/scalable-ot-positive-feature-independent-validation-2026-06-20.json`
- Markdown:
  `docs/benchmarks/scalable-ot-positive-feature-independent-validation-2026-06-20.md`

## Summary

| Metric | Value | Role |
| --- | ---: | --- |
| rows | `9` | hard-veto context |
| hard vetoes | `0` | hard veto |
| max candidate weighted mean error | `2.220446e-16` | hard veto |
| max candidate weighted second moment error | `5.218177e-01` | hard veto |
| max transport residual | `3.079331e-05` | hard veto |
| max wall time seconds | `3.731838e-02` | explanatory |
| ranking statistically supported | `False` | inference status |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Positive-feature lane independently remains viable for later validation. | Passed hard screen. | No vetoes fired. | This is still a replicated resampling-step moment screen, not full filtering/posterior/HMC validation. | Wait for peer low-rank independent closeout or create a new human-approved positive-feature-only larger validation plan. | No ranking, default, speedup, posterior correctness, HMC readiness, public API readiness, production readiness, dense equivalence, or broad scalable-OT selection. |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for current positive-feature lane. |
| Statistically supported ranking | None.  This independent lane does not compare against the peer lane. |
| Descriptive-only differences | Naive uniform errors, candidate-minus-naive deltas, per-seed rows, dense-reference context, and wall time. |
| Default-readiness | Not assessed and not claimed. |
| Next evidence needed | Future coordinator comparison or larger filtering/posterior/HMC validation only after independent lane closeouts. |

## Run Manifest

| Field | Value |
| --- | --- |
| git commit | `1d1b05923e0b1fa6c400de7c45b4dd02284cf88c` |
| command | `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py --mode full --program-id positive_feature_independent_lane --pass-status POSITIVE_FEATURE_INDEPENDENT_VALIDATION_PASSED_HARD_SCREEN_NO_RANKING --fail-status POSITIVE_FEATURE_INDEPENDENT_VALIDATION_FAILED_HARD_SCREEN --report-title "Positive-Feature Independent Validation" --plan-path docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-p01-replay-closeout-subplan-2026-06-20.md --result-path docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-closeout-result-2026-06-20.md --next-evidence-needed "future coordinator comparison or larger filtering/posterior/HMC validation only after independent lane closeouts" --output docs/benchmarks/scalable-ot-positive-feature-independent-validation-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-positive-feature-independent-validation-2026-06-20.md` |
| Python | `3.13.13` |
| TensorFlow | `2.20.0` |
| device scope | CPU-scoped; GPU hidden with `CUDA_VISIBLE_DEVICES=-1` |
| fixtures | `weighted_curve`, `bimodal_tail`, `high_dim_low_rank` |
| seeds | `101`, `202`, `303` |
| wall time | `0.224453` seconds in JSON manifest |
| plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-p01-replay-closeout-subplan-2026-06-20.md` |
| result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-closeout-result-2026-06-20.md` |
| output artifacts | JSON and Markdown diagnostic artifacts listed above |

## Post-Run Red Team

Strongest alternative explanation: the hard screen checks a resampling-step
moment contract, not full filtering, posterior agreement, HMC mechanics, or
runtime scaling.

What would overturn this result: replay under the same contract finds nonfinite
outputs, shape/log-weight failures, residual failures, moment threshold
failures, missing manifest fields, or unsupported claims.

Weakest evidence point: no peer comparison, no paired uncertainty analysis, no
full filtering benchmark, no posterior validation, no HMC diagnostic, and no
public/default API assessment were run.

## Close Record

The current-agent positive-feature Sinkhorn semantic-replacement lane is
independently closed as viable for later validation under the stated hard
screen.  This closeout does not wait for peer low-rank artifacts and does not
authorize a shared comparison.  A separate coordinator program should be
created only after both independent lane closeouts exist.
