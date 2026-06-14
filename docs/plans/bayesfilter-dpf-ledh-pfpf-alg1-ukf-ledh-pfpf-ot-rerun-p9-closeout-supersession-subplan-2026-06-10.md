# P9 Subplan: Integration Closeout And Supersession Ledger

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_OPUS_MAX_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | After P0-P8, is every previous LEDH-PFPF-OT-related test either redone with Algorithm 1 UKF or explicitly classified? |
| Baseline/comparator | P0 rerun registry and P1-P8 result artifacts. |
| Primary pass criterion | A closeout ledger indexes every old lane, every replacement artifact, every remaining blocker, and the exact non-claims. |
| Veto diagnostics | Old LEDH row still cited as current evidence; missing phase result; unresolved row without blocker; unsupported superiority or default claim; Claude review not converged. |
| Explanatory diagnostics | Summary tables for value, gradient, blocked adapters, N/A rows, and historical-only rows. |
| Not concluded | No production default, no HMC readiness, no universal superiority, and no claim for rows still blocked. |

## Required Closeout Tables

P9 must write:

- old-lane-to-new-disposition table;
- Algorithm 1 value table;
- Algorithm 1 gradient table;
- comparator applicability table;
- blocked adapter table;
- historical-only table;
- run manifest index;
- per-row manifest links;
- seed counts and particle ladders for every stochastic row;
- uncertainty columns, including standard errors or confidence intervals;
- threshold/certification-band status for every promoted row;
- core-vs-extension route class for every Algorithm 1 row;
- Claude review index;
- final non-claims.

## Required Guardrail Rerun

Before closeout, rerun:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_ledh_pfpf_alg1_ukf_tf.py -q
```

## Required Artifacts

- Closeout JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_alg1_ukf_ledh_pfpf_ot_rerun_closeout_2026-06-10.json`
- Closeout Markdown:
  `experiments/dpf_implementation/reports/dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-closeout-2026-06-10.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p9-closeout-supersession-result-2026-06-10.md`

## Exit Criteria

P9 passes when Claude agrees that the old LEDH-PFPF-OT evidence cannot be
accidentally revived and the replacement evidence is bounded by its actual
reruns, blockers, and non-claims.
