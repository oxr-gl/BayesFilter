# Result: Filterflow Final Gaps Closure For OT-DPF Audit

## Decision

`final_gaps_closed_unconditional_fixed_sinkhorn_compute_gap_identified`

The three remaining filterflow audit gaps are now either closed as bounded
evidence or converted into explicit risks:

- the Section 5.1 paper/code setting ledger is closed, with one material
  transition-covariance ambiguity recorded;
- the filterflow smoothness/gradient path executes on a bounded CPU-only
  bootstrap-proposal smoke run with finite GradientTape gradients, but the
  likelihood/gradient magnitudes are large relative to Kalman finite
  differences, so this is finite-gradient evidence, not agreement evidence;
- the BayesFilter fixed-target Sinkhorn epsilon `0.25` veto is localized to an
  unconditional computation on the initial cloud before ESS masking, plus an
  iteration-budget issue at the old 100-iteration diagnostic budget.

No production, public API, posterior, HMC, or general nonlinear-SSM readiness is
concluded.

## Artifacts

- Plan:
  `docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-plan-2026-05-30.md`
- Result:
  `docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-result-2026-05-30.md`
- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_final_gaps_closure_tf.py`
- Report:
  `experiments/dpf_implementation/reports/dpf-filterflow-final-gaps-closure-2026-05-30.md`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_final_gaps_closure_2026-05-30.json`

## Claude Review

Plan review:

| Iteration | Status | Codex audit |
| --- | --- | --- |
| 1 | `REJECT` | Accepted. Claude found inconsistent smoothness blocker semantics, underspecified executable Claude protocol, incomplete forbidden-write checks, and an uncapped Sinkhorn ladder. |
| 2 | `ACCEPT` | Accepted. Claude confirmed the blocker semantics, exact/elevated Claude protocol, forbidden-write checks, capped Sinkhorn ladder, and overclaim controls. |

Result review:

| Iteration | Status | Codex audit |
| --- | --- | --- |
| 1 | `PENDING` | To be reviewed after this result note is written. |

## Files Changed

New BayesFilter-owned experimental audit files:

- `docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-plan-2026-05-30.md`
- `docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-result-2026-05-30.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_final_gaps_closure_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-final-gaps-closure-2026-05-30.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_final_gaps_closure_2026-05-30.json`

No production `bayesfilter/`, `tests/`, monograph chapter, vendored student,
or high-dimensional lane file was edited by this task.

## Gap Ledger

| Gap | Status | Evidence | Remaining risk |
| --- | --- | --- | --- |
| Section 5.1 paper/code settings | `closed_with_transition_covariance_ambiguity_recorded` | Paper text, supplement, and `simple_linear_comparison.py` were reconciled. Most settings match. A bounded rerun showed the paper Table 1 scale matches executable filterflow's `I_2` convention, not `0.5 I_2`. | The paper/supplement `0.5 I_2` statement is likely a typo or notation mismatch; BayesFilter reproduction audits should use executable filterflow's `I_2` convention and keep the discrepancy recorded. |
| Filterflow smoothness/gradient | `closed_bounded_gradient_smoke_with_severe_unreconciled_magnitude_risk` | CPU-only bounded `simple_linear_smoothness` wrapper executed with finite likelihoods and finite gradients on a `4 x 4` mesh, `T=100`, `N=25`, epsilon `0.25`, bootstrap proposal. | Severe scalar/randomness/gradient-magnitude differences versus Kalman finite differences remain; this is not a full Figure 1 or Table 4 reproduction. |
| Fixed-target Sinkhorn epsilon `0.25` | `epsilon_0.25_unconditional_nontriggered_budget_gap` | On the exact matched-audit initial cloud, ESS is `25` for all rows, so no resampling would trigger. The old 100-iteration unconditional fixed-Sinkhorn computation has max residual `1.2399e-4`; 500 iterations reduces it to `5.1381e-6`. | This diagnoses the BayesFilter fixed-target lane only. It does not make fixed-target Sinkhorn paper-equivalent to filterflow's annealed transport. |

## Key Results

Paper/code setting reconciliation:

- matched: state dimension `2`, transition mean `diag(theta_1, theta_2)x`,
  observation covariance `0.1 I_2`, `T=150`, `N=25`, 100 realizations, epsilon
  grid `0.25, 0.5, 0.75`;
- code-specific: `NeffCriterion(0.5, True)`, `scaling=0.9`,
  `convergence_threshold=1e-3`;
- resolved reproduction choice with recorded source discrepancy: transition
  covariance is `0.5 I_2` in paper/supplement text but `I_2` in executable
  filterflow `simple_linear_comparison.py`; a bounded direct rerun showed the
  published Table 1 scale is consistent with the executable `I_2` convention,
  not `0.5 I_2`, so the paper text is likely a typo or notation mismatch.

Smoothness/gradient smoke:

| Metric | Value |
| --- | ---: |
| finite likelihoods | `true` |
| finite gradients | `true` |
| likelihood RMSE vs Kalman finite-diff surface | `323944` |
| gradient RMSE vs Kalman finite-diff surface | `1.44488e+08` |
| gradient max absolute delta | `5.11229e+08` |
| gradient cosine vs Kalman finite difference | `0.889557` |
| gradient sign agreement | `0.9375` |

Fixed-target Sinkhorn diagnosis on exact matched-audit initial cloud:

| epsilon | budget 100 residual | budget 500 residual | interpretation |
| ---: | ---: | ---: | --- |
| `0.25` | `1.23991e-4` | `5.13809e-6` | old residual veto reproduced on non-triggered initial rows; budget 500 clears tolerance |
| `0.5` | `2.29360e-9` | `5.55112e-17` | clears tolerance by budget 100 |
| `0.75` | `5.55112e-17` | `5.55112e-17` | clears tolerance by budget 100 |

The exact matched-audit initial cloud had `initial_ess_min=25`,
`initial_ess_max=25`, and `initial_resampling_triggered_any=false`.

## Interpretation

The earlier LGSSM mismatch should not be interpreted as a mathematical failure
of Corenflos/filterflow OT resampling.  The paper-style annealed
filterflow transport had already matched executable filterflow in the prior
gap-closure result.

The remaining fixed-target Sinkhorn issue is now narrower: the BayesFilter
experimental fixed-target branch computed Sinkhorn even on rows where ESS would
not trigger resampling.  On those non-triggered initial rows, epsilon `0.25`
needs more than the old 100 iterations to meet the residual gate.  The correct
next implementation action is to avoid unconditional fixed-Sinkhorn work on
non-triggered rows and keep paper-style annealed transport separate from the
fixed-target diagnostic branch.

The smoothness run proves the patched filterflow gradient path can execute
under the local Python 3.11 compatibility environment and produce finite
gradients.  It does not prove the bounded run reproduces the published vector
field or learning table, and the scale diagnostics deserve follow-up.

## Verification

Executed:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_final_gaps_closure_tf.py
```

Status: pass.

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_final_gaps_closure_tf
```

Output:

```text
final_gaps_closed_unconditional_fixed_sinkhorn_compute_gap_identified
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_final_gaps_closure_tf --validate-only
```

Status: pass.

```bash
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_final_gaps_closure_2026-05-30.json >/dev/null
```

Status: pass.

```bash
rg -n "import numpy|from numpy|student_dpf_baselines|vendor|highdim|NAWM|DSGE" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_final_gaps_closure_tf.py
```

Status: no matches.  The runner uses dynamic `np = __import__("numpy")` only
inside external filterflow subprocess scripts as reference/comparison code.

```bash
rg -n "[ \t]+$" docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-plan-2026-05-30.md experiments/dpf_implementation/reports/dpf-filterflow-final-gaps-closure-2026-05-30.md experiments/dpf_implementation/tf_tfp/runners/run_filterflow_final_gaps_closure_tf.py
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
git status --short -- docs/chapters .localsource/filterflow third_party experiments/controlled_dpf_baseline
```

Status: reports pre-existing unrelated dirty/untracked paths:

```text
 M experiments/controlled_dpf_baseline/README.md
?? .localsource/filterflow/
?? experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-final-archive-result.md
?? third_party/
```

```bash
git status --short -- docs/plans | rg -n "highdim|NAWM|DSGE|student|controlled_dpf"
```

Status: reports pre-existing unrelated student/highdim plan artifacts; no new
artifact from this task is in those lanes.

```bash
git status --short --branch
```

Status: branch `main...origin/main [behind 2]`, with broad pre-existing dirty
and untracked files preserved.  New files from this task are listed above.

## Unresolved Risks

- The transition covariance discrepancy should remain recorded, but for
  reproduction we should follow executable filterflow's `I_2` convention because
  it matches the published Table 1 scale; the paper/supplement `0.5 I_2`
  statement is likely a typo or notation mismatch.
- The bounded smoothness smoke has finite gradients but very large magnitude
  differences versus Kalman finite differences.  It should not be treated as a
  clean gradient-agreement result.
- Fixed-target Sinkhorn remains a BayesFilter design/numerics branch, not the
  Corenflos/filterflow paper-style annealed transport path.
- The local filterflow checkout is patched for Python 3.11 compatibility and is
  not pristine upstream source.

## Blockers

No execution blocker remains for the bounded final-gaps audit.  The remaining
items are scoped risks requiring follow-up plans if we want stronger evidence.

## Next Recommended Action

Patch the BayesFilter experimental fixed-target Sinkhorn comparator so it does
not compute Sinkhorn on rows where ESS does not trigger resampling, and add a
small regression artifact proving epsilon `0.25` no longer vetoes from
non-triggered initial rows.  Keep that separate from the paper-style annealed
filterflow transport path.
