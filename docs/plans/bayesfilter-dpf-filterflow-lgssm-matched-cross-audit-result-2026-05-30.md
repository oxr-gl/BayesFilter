# Result: Filterflow LGSSM Matched Cross-Audit Rerun

## Decision

`current_fixed_sinkhorn_red_flag_filterflow_style_not_matched`

The patched external filterflow implementation now executes and is a usable
reference comparator.  The previous `pykalman` environment blocker is resolved
for this local external branch.

The matched audit does not prove BayesFilter OT-DPF correctness, but it sharply
narrows the issue:

- exact Kalman values align between patched filterflow/pykalman and the
  BayesFilter TF Kalman convention to `7.262e-08`;
- BayesFilter bootstrap PF matches filterflow PF within the filterflow Monte
  Carlo band at all three theta values;
- BayesFilter current scaled fixed-Sinkhorn OT-DPF matches filterflow
  RegularisedTransform within the filterflow Monte Carlo band for epsilons
  `0.5` and `0.75`, but epsilon `0.25` is vetoed by the stricter BayesFilter
  Sinkhorn residual gate;
- the audit-only BayesFilter attempt to mirror filterflow's annealed transport
  is outside the filterflow Monte Carlo band and must not be treated as a
  faithful implementation.

## Artifacts

- Plan:
  `docs/plans/bayesfilter-dpf-filterflow-lgssm-matched-cross-audit-plan-2026-05-30.md`
- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py`
- Report:
  `experiments/dpf_implementation/reports/dpf-filterflow-lgssm-matched-cross-audit-2026-05-30.md`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_lgssm_matched_cross_audit_2026-05-30.json`

## Claude Review

Plan review:

| Iteration | Status | Codex audit |
| --- | --- | --- |
| 1 | `ACCEPT` | Accepted. Minor watch item recorded: BayesFilter uses the same fixed observation path but independent algorithmic random streams, not bitwise-identical randomness. |

Result review:

| Iteration | Status | Codex audit |
| --- | --- | --- |
| 1 | `ACCEPT` | Accepted. Claude confirmed the executable filterflow comparison, fixed observation path, Kalman alignment, PF match, fixed-Sinkhorn partial match/veto, failed audit-only transport lane, and lane boundaries. |

## Evidence Contract Status

Question: after patching external filterflow, does BayesFilter's experimental
TF/TFP OT-DPF reproduce filterflow's Section-5.1-style LGSSM likelihood-error
behavior under the same fixed observation path and core settings?

Answer: partially, with red flags.

Primary comparator: patched external filterflow branch
`bayesfilter-py311-compat`, upstream base
`5d8300ba247c4c17e1a301a22560c24fd0670bfe`.

Primary scalar: `(estimated log likelihood - exact Kalman log likelihood) / T`
over 100 filter realizations.

Comparison protocol:

- same fixed filterflow observation path;
- same initial particle cloud from filterflow's Section-5.1-style driver;
- `T=150`, `N=25`, theta grid `0.25`, `0.5`, `0.75`;
- filterflow `NeffCriterion(0.5, True)`;
- filterflow `RegularisedTransform(epsilon=eps, scaling=0.9,
  convergence_threshold=1e-3)`;
- BayesFilter algorithmic randomness fixed but not bitwise matched to
  filterflow.

## Key Results

Kalman alignment:

| Metric | Value |
| --- | ---: |
| max absolute log-likelihood delta | `7.26172402210068e-08` |
| alignment status | pass |

PF calibration:

| theta | delta: BayesFilter PF minus filterflow PF | within filterflow SD |
| --- | ---: | --- |
| 0.25 | `0.00430025` | true |
| 0.50 | `-0.00361567` | true |
| 0.75 | `0.0180054` | true |

Current BayesFilter scaled fixed-Sinkhorn versus filterflow RegularisedTransform:

| epsilon | theta | BayesFilter status | delta | within filterflow SD |
| --- | --- | --- | ---: | --- |
| 0.25 | 0.25 | `veto` | N/A | N/A |
| 0.25 | 0.50 | `veto` | N/A | N/A |
| 0.25 | 0.75 | `veto` | N/A | N/A |
| 0.50 | 0.25 | `executed` | `-0.0230692` | true |
| 0.50 | 0.50 | `executed` | `-0.0238741` | true |
| 0.50 | 0.75 | `executed` | `-0.0270404` | true |
| 0.75 | 0.25 | `executed` | `-0.0227490` | true |
| 0.75 | 0.50 | `executed` | `-0.0235046` | true |
| 0.75 | 0.75 | `executed` | `-0.0215067` | true |

Audit-only BayesFilter filterflow-style annealed transport attempt:

| epsilon | theta | delta | within filterflow SD |
| --- | --- | ---: | --- |
| 0.25 | 0.25 | `-0.468069` | false |
| 0.25 | 0.50 | `-0.609093` | false |
| 0.25 | 0.75 | `-0.430393` | false |
| 0.50 | 0.25 | `-0.423157` | false |
| 0.50 | 0.50 | `-0.557500` | false |
| 0.50 | 0.75 | `-0.444220` | false |
| 0.75 | 0.25 | `-0.402691` | false |
| 0.75 | 0.50 | `-0.557986` | false |
| 0.75 | 0.75 | `-0.461825` | false |

## Interpretation

The earlier conclusion that filterflow could not execute is stale.  With the
local compatibility branch, filterflow runs and BayesFilter can be compared
directly on the same observation path.

The large alarm that "OT fails" is not supported in the broad sense:
BayesFilter's existing scaled fixed-Sinkhorn relaxed path agrees with
filterflow RegularisedTransform within the filterflow Monte Carlo band for
`epsilon=0.5` and `epsilon=0.75`.  The remaining concrete problem is narrower:
`epsilon=0.25` fails the BayesFilter residual gate, and the audit-only attempt
to reproduce filterflow's annealed transport semantics is wrong or incomplete.

## Red Flags

| ID | Status | Meaning |
| --- | --- | --- |
| `fixed_sinkhorn_match` | `bayesfilter_veto_or_missing` | current fixed Sinkhorn cannot be credited for epsilon `0.25` because the residual gate vetoes it |
| `filterflow_style_transport_match` | `outside_filterflow_mc_band` | the audit-only annealed transport implementation is not faithful |
| `random_stream` | `not_bitwise_matched` | same observations and initial cloud; algorithmic streams fixed but independent |

## Verification

Executed:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_lgssm_matched_cross_audit_tf
```

Output:

```text
current_fixed_sinkhorn_red_flag_filterflow_style_not_matched
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_lgssm_matched_cross_audit_tf --validate-only
```

Status: pass.

NumPy/import-boundary check on the runner:

```bash
rg -n "import numpy|from numpy|student_dpf_baselines|vendor|highdim|NAWM|DSGE" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py
```

Status: no matches.  The external filterflow subprocess dynamically imports
NumPy as comparison/reference code; the BayesFilter runner itself has no NumPy
implementation import.

## What Is Not Concluded

- No production readiness.
- No public API readiness.
- No HMC readiness.
- No posterior correctness.
- No general nonlinear-SSM validity.
- No claim that finite relaxed OT is categorical PF.
- No claim that the local patched filterflow branch is untouched upstream code.

## Next Recommended Action

Do not chase broad OT failure.  The next smallest useful artifact is a
component-level comparison of filterflow `transport_from_potentials` and the
BayesFilter audit-only annealed transport on one saved particle/log-weight
state.  That should isolate whether the mismatch is in epsilon annealing,
potential normalization, transport matrix orientation, or the final weight/log
likelihood convention.
