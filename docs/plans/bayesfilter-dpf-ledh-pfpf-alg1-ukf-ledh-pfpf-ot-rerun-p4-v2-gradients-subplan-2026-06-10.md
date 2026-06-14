# P4 Subplan: V2 Algorithm 1 Gradient Replacement

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_OPUS_MAX_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | For V2 rows with valid gradient estimands, do Algorithm 1 UKF fixed-branch gradients execute finitely and compare to valid references or diagnostics? |
| Baseline/comparator | P2 contracts, P3 value scalars, exact LGSSM score where available, and declared approximation gradients only when same scalar and parameterization are proven. |
| Primary pass criterion | Each runnable gradient row declares scalar, parameterization, branch-freeze policy, and fixed-branch score; finite gradients and uncertainty are reported without value-to-gradient promotion. |
| Veto diagnostics | Gradient scalar differs from value scalar; old implementation route; finite differences as sole promotion gate; branch decisions unrecorded; stochastic and fixed-branch scores mixed. |
| Explanatory diagnostics | AD/FD local residuals, cosine similarity, coordinate errors, runtime, branch hashes. |
| Not concluded | No stochastic-resampling gradient correctness and no HMC readiness. |

## Planned Runner

`experiments/dpf_implementation/tf_tfp/runners/run_v2_ledh_pfpf_alg1_ukf_gradients_tf.py`

## Required Row Fields

Every gradient row must carry mandatory Algorithm 1 route fields,
core/extension resampling fields, scalar and parameterization identifiers,
branch-freeze policy, gradient tolerance/certification band, seed count,
particle ladder, gradient error summaries, uncertainty, and per-row manifest
link.

## Planned Command

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_ledh_pfpf_alg1_ukf_gradients_tf
```

## Required Artifacts

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_alg1_ukf_gradients_2026-06-10.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-alg1-ukf-gradients-2026-06-10.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p4-v2-gradients-result-2026-06-10.md`

## Exit Criteria

P4 passes when gradient rows are executed, diagnostic-only, N/A, or blocked
with reviewed reasons and no value metric is used as a gradient promotion.
