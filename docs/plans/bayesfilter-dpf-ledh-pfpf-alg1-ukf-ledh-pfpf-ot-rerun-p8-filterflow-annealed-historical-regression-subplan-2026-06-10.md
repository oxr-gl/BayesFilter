# P8 Subplan: FilterFlow, Annealed, And Historical Regression Classification

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_OPUS_MAX_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which old FilterFlow-matched, annealed-transport, and source-faithful-repair lanes should be rerun as Algorithm 1 extension evidence, and which should remain historical-only? |
| Baseline/comparator | P1-P7 Algorithm 1 results, old FilterFlow/annealed/source-faithful-repair artifacts, and the supersession closeout. |
| Primary pass criterion | Every old extension or historical lane has one reviewed disposition: `ALG1_EXTENSION_RERUN`, `HISTORICAL_ONLY_NOT_EVIDENCE`, `SCAFFOLDING_ONLY`, or `BLOCKED_REQUIRES_SEPARATE_PLAN`. |
| Veto diagnostics | OT or annealed transport called source Li-Coates Algorithm 1; old auxiliary-flow-only repair rerun as current evidence; mutating `.localsource/filterflow`; same-contract comparison treated as correctness proof. |
| Explanatory diagnostics | Same-contract residuals, runtime, transport residuals, old-vs-new deltas. |
| Not concluded | No FilterFlow correctness proof and no OT-resampling source-faithfulness claim. |

## Old Lanes

- `run_ledh_pfpf_annealed_transport_lgssm_tf.py`;
- `run_filterflow_matched_ledh_pfpf_ot_tf.py`;
- `run_ledh_pfpf_source_faithful_repair_tf.py`;
- reports/outputs beginning `dpf_ledh_pfpf_annealed_transport`,
  `dpf_filterflow_matched_ledh_pfpf_ot`, or
  `dpf_ledh_pfpf_source_faithful_repair`.

## Planned Work

P8 should prefer classification over implementation unless P1-P7 already show
that an extension rerun is low risk and clearly labelled as extension evidence.
If an extension rerun is needed, create a separate reviewed amendment before
running it.

## Required Artifacts

- Classification JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_alg1_ukf_extension_historical_classification_2026-06-10.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-ledh-pfpf-alg1-ukf-extension-historical-classification-2026-06-10.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p8-filterflow-annealed-historical-regression-result-2026-06-10.md`

## Exit Criteria

P8 passes when extension and historical lanes cannot be mistaken for source
Algorithm 1 evidence.

