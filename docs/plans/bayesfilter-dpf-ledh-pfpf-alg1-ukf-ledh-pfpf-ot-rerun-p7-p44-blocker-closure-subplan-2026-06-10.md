# P7 Subplan: P44/P8 Blocker Closure Replacement

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_OPUS_MAX_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the P44/P8 cells that were `N/A` or blocked for the old DPF LEDH route be filled with Algorithm 1 UKF results, or are precise adapters still missing? |
| Baseline/comparator | P44 model contracts, P5/P6 replacement evidence, exact/approximation references where valid. |
| Primary pass criterion | Every P44/P8 DPF cell formerly tied to `dpf_ledh_pfpf_ot` is filled by an Algorithm 1 result or a precise reviewed blocker. |
| Veto diagnostics | Treating adapter absence as scientific failure; using old implementation result; unsupported comparator row ranked; nonfinite diagnostics; thresholds modified post hoc. |
| Explanatory diagnostics | Missing callback matrix, model/filter support matrix, value/gradient errors, MC intervals, runtime. |
| Not concluded | No P44 universal success and no production default. |

## Required Classification

For each P44/P8 target, record:

- model id;
- state dimension and observation dimension;
- transition density availability;
- observation density availability;
- transition simulator availability;
- observation Jacobian availability;
- UKF prediction/update callback status;
- Algorithm 1 flow-anchor status;
- value scalar and gradient scalar;
- comparator route;
- mandatory Algorithm 1 route fields for replacement rows;
- core/extension resampling fields;
- seed count, particle ladder, and uncertainty if a stochastic row is run;
- per-row run-manifest link;
- final status.

## Planned Runner

`experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p8_p44_alg1_ukf_blocker_closure_tf.py`

## Planned Command

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p8_p44_alg1_ukf_blocker_closure_tf
```

## Required Artifacts

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p8_p44_alg1_ukf_blocker_closure_2026-06-10.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p8-p44-alg1-ukf-blocker-closure-2026-06-10.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p7-p44-blocker-closure-result-2026-06-10.md`

## Exit Criteria

P7 passes when no P44/P8 LEDH-related cell remains unexplained.  A reviewed
implementation blocker is acceptable; a silent `N/A` is not.
