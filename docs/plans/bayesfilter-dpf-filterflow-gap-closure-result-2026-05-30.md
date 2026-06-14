# Result: Filterflow Gap Closure For OT-DPF Audit

## Decision

`filterflow_style_transport_matched`

The actionable filterflow implementation gap is closed for the bounded LGSSM
Section-5.1-style audit.  After correcting the BayesFilter experimental
filterflow-style transport mirror, the outer matched audit agrees with patched
filterflow `RegularisedTransform` within the filterflow Monte Carlo band for
all `3 x 3` epsilon/theta cells.

This is not an exact paper-table reproduction claim and not a production
BayesFilter claim.  It is a matched executable-code audit against patched local
filterflow.

## Artifacts

- Plan:
  `docs/plans/bayesfilter-dpf-filterflow-gap-closure-plan-2026-05-30.md`
- Result:
  `docs/plans/bayesfilter-dpf-filterflow-gap-closure-result-2026-05-30.md`
- Patched experimental matched-audit runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py`
- New gap-closure runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_gap_closure_tf.py`
- Report:
  `experiments/dpf_implementation/reports/dpf-filterflow-lgssm-gap-closure-2026-05-30.md`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_lgssm_gap_closure_2026-05-30.json`

## Claude Review

Plan review:

| Iteration | Status | Codex audit |
| --- | --- | --- |
| 1 | `ACCEPT` | Accepted. Claude noted two watch items: record filterflow branch/commit/runtime status in the result and ensure the patched path is exercised by the new gap-closure runner. Both are satisfied. |

Result review:

| Iteration | Status | Codex audit |
| --- | --- | --- |
| 1 | `REJECT` | Accepted as artifact bookkeeping, not a technical rejection. Claude confirmed the transport correction and outer audit result, but required the result note to record all verification commands and replace the pending review row. |
| 2 | `ACCEPT` | Accepted. Claude confirmed the prior bookkeeping rejection items are resolved and found no remaining blocking overclaim or lane contamination. |

## What Changed

Only experimental audit code was changed.  Production `bayesfilter/`, `tests/`,
monograph chapters, high-dimensional-lane files, vendored student code, and
`.localsource/filterflow` source were not edited.

The corrected BayesFilter experimental filterflow-style mirror now follows the
component audit:

- `transport_from_potentials` adds `logw` on the column axis:
  `log_weights[:, None, :]`;
- epsilon annealing starts from coordinate range squared on the scaled cloud;
- the loop uses filterflow-style `reduce_all` continuation semantics;
- row residual means row sums near one;
- column residual means column sums near `N * source_weight`.

## Evidence Contract Status

Question: can the actionable filterflow gaps be closed by using patched
filterflow as executable reference, correcting the BayesFilter experimental
filterflow-style mirror, and rerunning the matched LGSSM audit?

Answer: yes for the executable LGSSM likelihood-error audit.

Primary comparator: patched external filterflow branch
`bayesfilter-py311-compat`, upstream base
`5d8300ba247c4c17e1a301a22560c24fd0670bfe`.

Primary scalar: `(estimated log likelihood - exact Kalman log likelihood) / T`
over 100 filter realizations.

## Gap-Closure Ledger

| Gap | Status | Evidence |
| --- | --- | --- |
| filterflow executable | closed | branch `bayesfilter-py311-compat`, commit `5d8300ba247c4c17e1a301a22560c24fd0670bfe`, compatibility diff recorded |
| paper/code setting ledger | partially closed | executable filterflow settings recorded; exact paper-table reproduction not claimed due paper/code covariance ambiguity |
| Kalman alignment | closed | max absolute log-likelihood delta `7.26172402210068e-08` |
| PF calibration | closed | BayesFilter PF within filterflow Monte Carlo band for all three theta rows |
| corrected filterflow-style transport | closed | within filterflow Monte Carlo band for all nine epsilon/theta rows |
| fixed-Sinkhorn small epsilon | still open | fixed-Sinkhorn lane still vetoes epsilon `0.25`; corrected paper-style transport succeeds |
| gradient/smoothness replication | still open | not run in this result |

## Key Results

Corrected BayesFilter filterflow-style transport versus filterflow
`RegularisedTransform`:

| epsilon | theta | delta: BayesFilter minus filterflow | within filterflow SD |
| --- | --- | ---: | --- |
| `0.25` | `0.25` | `-0.023084778353450908` | true |
| `0.25` | `0.50` | `-0.01648339600894788` | true |
| `0.25` | `0.75` | `-0.026786881508458538` | true |
| `0.50` | `0.25` | `-0.02257354792724442` | true |
| `0.50` | `0.50` | `-0.01578594426991098` | true |
| `0.50` | `0.75` | `-0.01991125303908503` | true |
| `0.75` | `0.25` | `-0.02234524495463308` | true |
| `0.75` | `0.50` | `-0.01617954702220281` | true |
| `0.75` | `0.75` | `-0.018249484269697858` | true |

BayesFilter PF versus filterflow PF:

| theta | delta: BayesFilter minus filterflow | within filterflow SD |
| --- | ---: | --- |
| `0.25` | `0.00430025` | true |
| `0.50` | `-0.00361567` | true |
| `0.75` | `0.0180054` | true |

Current fixed-Sinkhorn lane:

- epsilons `0.5` and `0.75` remain within the filterflow Monte Carlo band;
- epsilon `0.25` still vetoes under the fixed-Sinkhorn residual gate;
- this is no longer a blocker for the filterflow-style reproduction because the
  corrected paper-style annealed transport lane succeeds for epsilon `0.25`.

## Interpretation

The main filterflow gap was an audit-mirror implementation error, not a
mathematical failure of Corenflos/filterflow OT resampling on LGSSM.  The
component audit identified the wrong log-weight axis, and the outer rerun
confirms that correcting the filterflow-style transport semantics closes the
likelihood-level mismatch against executable filterflow.

The remaining filterflow-side work is narrower:

- an exact paper-table reproduction still needs a paper/code setting
  reconciliation artifact;
- gradient/smoothness replication remains a separate DPF evidence gap;
- the fixed-target Sinkhorn lane remains a BayesFilter design/numerics gap at
  epsilon `0.25`, but it is not the paper-style filterflow transport.

## Verification

Executed:

```bash
git -C .localsource/filterflow status --short --branch
```

Output:

```text
## bayesfilter-py311-compat
 M scripts/base.py
 M scripts/simple_linear_common.py
 M scripts/simple_linear_smoothness.py
```

```bash
git -C .localsource/filterflow rev-parse HEAD
```

Output:

```text
5d8300ba247c4c17e1a301a22560c24fd0670bfe
```

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_gap_closure_tf.py
```

Status: pass.

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_transport_component_audit_tf --validate-only
```

Status: pass.

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_lgssm_gap_closure_tf
```

Output:

```text
filterflow_style_transport_matched
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_lgssm_gap_closure_tf --validate-only
```

Status: pass.

```bash
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_lgssm_gap_closure_2026-05-30.json >/dev/null
```

Status: pass.

```bash
rg -n "import numpy|from numpy|student_dpf_baselines|vendor|highdim|NAWM|DSGE" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_gap_closure_tf.py
```

Status: no matches.  The external filterflow subprocess dynamically imports
NumPy as reference/comparison code; BayesFilter-owned audit implementation code
does not import NumPy.

```bash
rg -n "[ \t]+$" docs/plans/bayesfilter-dpf-filterflow-gap-closure-plan-2026-05-30.md docs/plans/bayesfilter-dpf-filterflow-gap-closure-result-2026-05-30.md experiments/dpf_implementation/reports/dpf-filterflow-lgssm-gap-closure-2026-05-30.md experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_gap_closure_tf.py
```

Status: no matches.

```bash
git diff --check
```

Status: pass.

```bash
git status --short -- bayesfilter tests docs/chapters
```

Status: no matches.

```bash
git status --short --branch
```

Status: branch `main...origin/main [behind 2]`, with unrelated dirty/untracked
files preserved.  Relevant new/changed gap-closure files are under
`docs/plans/` and `experiments/dpf_implementation/`.

## What Is Not Concluded

- No production readiness.
- No public API readiness.
- No posterior correctness.
- No HMC readiness.
- No general nonlinear-SSM validity.
- No gradient/smoothness replication.
- No exact paper-table reproduction.
- No claim that finite relaxed OT is categorical PF.
- No claim that patched filterflow is untouched upstream code.

## Next Recommended Action

Create a dedicated filterflow paper-reproduction ledger that reconciles the
paper Section 5.1 text/table settings against `simple_linear_comparison.py`,
then run the filterflow gradient/smoothness experiment as the next executable
external-code comparator.
