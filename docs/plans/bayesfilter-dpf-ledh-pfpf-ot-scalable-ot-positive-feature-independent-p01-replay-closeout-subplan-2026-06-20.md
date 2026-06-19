# PF-I1 Subplan: Independent Replay And Closeout

Date: 2026-06-20
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-master-program-2026-06-20.md`

## Phase Objective

Rerun the positive-feature downstream hard screen as an independent-lane replay,
write independent JSON/Markdown artifacts, and close the current-agent
positive-feature lane as viable or blocked under its own evidence contract.

## Entry Conditions Inherited From Previous Phase

- PF-I0 entry audit passed.
- The current lane owns only positive-feature Sinkhorn semantic replacement.
- Peer low-rank artifacts are not required for PF-I1.
- No ranking/default/scientific claim is authorized.

## Required Artifacts

- Harness:
  `docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py`
- Test:
  `tests/test_wave4_positive_feature_validation.py`
- Independent JSON result:
  `docs/benchmarks/scalable-ot-positive-feature-independent-validation-2026-06-20.json`
- Independent Markdown result:
  `docs/benchmarks/scalable-ot-positive-feature-independent-validation-2026-06-20.md`
- Closeout result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-closeout-result-2026-06-20.md`

## Required Checks, Tests, And Reviews

Local checks:

```bash
python -m py_compile docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py tests/test_wave4_positive_feature_validation.py experiments/dpf_implementation/tf_tfp/resampling/positive_feature_transport_tf.py
pytest -q tests/test_positive_feature_transport_tf.py tests/test_wave4_positive_feature_validation.py
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py --mode full --program-id positive_feature_independent_lane --pass-status POSITIVE_FEATURE_INDEPENDENT_VALIDATION_PASSED_HARD_SCREEN_NO_RANKING --fail-status POSITIVE_FEATURE_INDEPENDENT_VALIDATION_FAILED_HARD_SCREEN --report-title "Positive-Feature Independent Validation" --plan-path docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-p01-replay-closeout-subplan-2026-06-20.md --result-path docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-closeout-result-2026-06-20.md --next-evidence-needed "future coordinator comparison or larger filtering/posterior/HMC validation only after independent lane closeouts" --output docs/benchmarks/scalable-ot-positive-feature-independent-validation-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-positive-feature-independent-validation-2026-06-20.md
python -m json.tool docs/benchmarks/scalable-ot-positive-feature-independent-validation-2026-06-20.json
```

Review:

- Codex skeptical audit before interpreting the independent replay.
- Claude review is not required unless the replay fails in a way that would
  require a material repair or the closeout would make a material claim beyond
  the evidence contract.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the positive-feature Sinkhorn semantic-replacement lane remain viable under an independent replicated downstream resampling hard screen? |
| Baseline/comparator | Exact weighted input estimates are the downstream reference.  Naive uniform-no-transport and dense-reference deltas are explanatory only. |
| Primary pass criterion | Focused tests and official independent diagnostic exit 0; hard vetoes are empty; transported particles are finite and shape-valid; output log weights are normalized; features/scalings are finite and positive; residual and moment thresholds pass; required manifest fields point to independent-lane artifacts. |
| Veto diagnostics | Missing entry artifacts, nonfinite output or diagnostics, nonpositive features, shape mismatch, log-weight normalization residual above `1.0e-10`, residual threshold failure, moment screen threshold failure, missing manifest field, unsupported claim, peer dependency, or official command failure. |
| Explanatory diagnostics | Naive estimator errors, candidate-vs-naive deltas, wall time, per-fixture/per-seed rows, feature count, epsilon, and residual magnitudes. |
| Not concluded | No ranking, speedup, superiority, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, or broad scalable-OT selection. |
| Artifact preserving result | Independent JSON/Markdown diagnostics and closeout result. |

## Forbidden Claims And Actions

- Do not compare against the peer lane.
- Do not wait for peer artifacts.
- Do not promote candidate-vs-naive deltas, dense deltas, or runtime into
  ranking/speedup evidence.
- Do not change thresholds after seeing results.
- Do not edit public exports/defaults, Phase 1 fixtures, Phase 3 schema,
  peer-lane artifacts, or unrelated files.

## Exact Next-Phase Handoff Conditions

If PF-I1 passes, the positive-feature lane is independently closed as viable
for later validation only.  The next justified action is either:

- wait for the peer low-rank independent closeout, then plan a separate
  coordinator comparison; or
- create a new human-approved positive-feature-only validation program for
  larger filtering/posterior/HMC evidence.

## Stop Conditions

Stop and write a blocker result if the diagnostic fails due to an unfixable
candidate hard veto, an unsupported claim cannot be repaired, or a repair would
require changing thresholds, package installation, network fetch, GPU evidence,
public/default/API edits, or peer-lane edits.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write the independent closeout result.
3. Review final claims for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
