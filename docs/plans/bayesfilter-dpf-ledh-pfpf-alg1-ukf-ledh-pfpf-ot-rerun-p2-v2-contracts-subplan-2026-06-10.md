# P2 Subplan: V2 Algorithm 1 Contract Replacement

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_OPUS_MAX_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the old V2 `LEDH-PFPF-OT` contract lane be replaced with Algorithm 1 UKF contracts for every V2 model row? |
| Baseline/comparator | Old V2 contract lane defines coverage; current contracts must bind Algorithm 1 route identifiers, model callbacks, scalar, seeds, particle counts, pseudo-time schedule, UKF parameters, and optional extension resampling separately. |
| Primary pass criterion | A frozen contract artifact exists for every V2 row, with status `RUNNABLE_ALG1`, `N/A_NOT_APPLICABLE`, or `BLOCKED_REQUIRES_ADAPTER`, and with all mandatory route fields, thresholds, scalar definitions, and core/extension fields declared before P3/P4. |
| Veto diagnostics | Silent row drop; old route id; missing covariance lifecycle fields; OT labelled as Algorithm 1 core; scalar or gradient object unspecified; tolerance set after results. |
| Explanatory diagnostics | Callback availability matrix, old-vs-new contract delta, shape/dtype checks. |
| Not concluded | No values, gradients, or performance ranking. |

## V2 Rows

Carry the old V2 row list exactly:

1. `lgssm_2d_h25_rich`
2. `sv_1d_h18_rich`
3. `range_bearing_4d_h20_rich`
4. `structural_ar1_quadratic_h16`
5. `spatial_sir_j3_rk4`
6. `predator_prey_rk4`

## Planned Runner

If no suitable replacement exists, implement:

`experiments/dpf_implementation/tf_tfp/runners/run_v2_ledh_pfpf_alg1_ukf_contracts_tf.py`

The old runner `run_v2_ledh_pfpf_ot_contracts_tf.py` may be read as scaffolding
only and must not provide current route identifiers.

## Contract Schema Requirements

Each V2 contract row must include the mandatory Algorithm 1 route fields from
the master program, value/gradient scalar definitions, comparator status,
value/gradient tolerances or `N/A` reasons, minimum seed count, particle
ladder, core-vs-extension resampling fields, and allowed final statuses for
P3/P4.

## Planned Command

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_ledh_pfpf_alg1_ukf_contracts_tf
```

## Required Artifacts

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_alg1_ukf_contracts_2026-06-10.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-alg1-ukf-contracts-2026-06-10.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p2-v2-contracts-result-2026-06-10.md`

## Exit Criteria

P2 passes when all six V2 rows have reviewed contract statuses and P3/P4 can
only consume the frozen P2 contract artifact.
