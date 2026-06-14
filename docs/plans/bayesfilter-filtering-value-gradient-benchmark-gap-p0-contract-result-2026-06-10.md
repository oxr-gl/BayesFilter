# P0 Result: Benchmark Contract And Gap Lock

metadata_date: 2026-06-10
phase: FILTER_BENCH_P0
status: PASS_FILTER_BENCH_P0_CONTRACT
supervisor: Codex
reviewer: Claude Code read-only

## Decision Table

| Field | Decision |
| --- | --- |
| Gate decision | Pass P0. |
| Primary criterion status | Satisfied: exactness is cell-level, non-LGSSM approximate filters are admissible, and reference types are explicit. |
| Veto diagnostic status | Passed: the contract forbids old LEDH-PFPF-OT as current evidence, forbids hiding DPF gradient failures, and forbids imposing exact same-target requirements outside LGSSM. |
| Main uncertainty | P1 must implement the registry without reintroducing stale Zhao-Cui/SV blocker language. |
| Next justified action | Advance to P1 target registry. |
| What is not concluded | No benchmark results, no algorithm ranking, no DPF gradient certification, no Bayesian-estimation readiness. |

## Final Benchmark Question

For each declared model row, fixed observations, fixed parameter vector, fixed
horizon, fixed dimension, and declared reference route, how do the existing
BayesFilter filtering algorithms compare on:

1. log-likelihood or value error;
2. gradient error where the row has a declared reference-gradient route;
3. gradient status where the row does not support a valid gradient comparison;
4. runtime and diagnostics needed to interpret the cell.

The benchmark admits approximate filters on non-Gaussian models.  A filter is
not excluded merely because it is UKF, SVD, CUT4, Zhao-Cui, bootstrap DPF, or
Algorithm 1 UKF LEDH-PFPF on a non-Gaussian row.  Exactness is recorded as a
cell property and reference property, not as a global admission gate.

## Reference Types

| Reference type | Meaning | Promotion boundary |
| --- | --- | --- |
| `exact` | Analytic reference for the row, such as LGSSM Kalman. | May support exact value/gradient error if gradient route is declared. |
| `dense_numerical` | Lower-rung dense quadrature or enumeration reference. | Numerical reference only; must report order/refinement diagnostics. |
| `transformed_actual_nongaussian` | Actual transformed/log-additive non-Gaussian target, including SV log-transform rows. | Not the native raw-y target unless explicitly declared. |
| `gaussian_mixture_surrogate` | Finite Gaussian-mixture approximation or enumeration lane, including KSC-style SV rows. | Surrogate approximation; cannot be silently treated as actual non-Gaussian truth. |
| `diagnostic` | Diagnostic reference or consistency check that explains behavior. | Cannot rank algorithms as correctness evidence. |
| `blocked_only` | Row is recorded only as a blocker/nonclaim. | Cannot produce benchmark pass cells or value/gradient rankings. |

P1 may add aliases, but each alias must map to one of these contract classes and
must preserve exactness/approximation labels in output matrices.

## Required Cell Fields

Every value cell must include:

- `target_id`;
- `registry_row_id`;
- `algorithm_id`;
- `reference_type`;
- `comparator_label`;
- `value`;
- `reference_value` or a reason code;
- `value_error_abs`;
- `value_error_rel` where meaningful;
- `value_status`;
- diagnostics and artifact path.

Every gradient cell must include:

- `gradient`;
- `reference_gradient` or a reason code;
- `gradient_error_abs_norm`;
- `gradient_error_rel_norm` where meaningful;
- `gradient_status`;
- branch/resampling/fixed-branch diagnostic status where relevant.

No matrix may contain a blank hole.  A non-result cell must carry a
machine-readable reason code.

## Gradient Contract

Gradient cells must be honest rather than optimistic:

- valid reference-gradient rows may report numeric gradient errors;
- value-only rows must report `reference_gradient_unavailable` or a more
  specific reason;
- DPF no-resampling or fixed-branch gradients must be labeled diagnostic unless
  a later phase proves a valid gradient route;
- resampling-enabled DPF gradients must not be reported as valid unless a
  reviewed score/gradient estimator is implemented and admitted;
- finite gradients and finite-difference checks are explanatory unless the row
  reference and branch diagnostics support a valid gradient classification.

## Non-Claim Rules

The benchmark must not claim:

- exactness outside LGSSM or another row explicitly labeled `exact`;
- native raw-y SV correctness for transformed or Gaussian-mixture SV rows;
- strict same-target equality for Gaussian-mixture surrogate rows against the
  actual transformed non-Gaussian target;
- source-faithful adaptive Zhao-Cui paper reproduction unless the row explicitly
  has that evidence;
- DPF gradient validity from finite gradients alone;
- Bayesian-estimation readiness from filtering value/gradient comparisons alone.

## LEDH-PFPF-OT Supersession Guard

Historical `LEDH-PFPF-OT` artifacts are superseded for current evidence.  They
may appear only under a `historical_only` or `superseded` label.  The current
DPF particle-flow algorithm row is the reviewed source-faithful Algorithm 1 UKF
LEDH-PFPF route, with route identifiers and no-resampling/resampling gradient
status explicitly reported.

## P0 Gate Assessment

The P0 primary criterion is locally satisfied:

- exactness scope is unambiguous and cell-level;
- approximate filters are admissible on non-LGSSM rows;
- value and gradient cell fields are defined;
- approximation non-claims are explicit;
- old LEDH-PFPF-OT is forbidden as current evidence.

P0 passed Claude read-only review on iteration 2.  The exact pass token is:
`PASS_FILTER_BENCH_P0_CONTRACT`.

## Claude Review Repair Ledger

### Iteration 1

Reviewer: `filter-benchmark-gap-p0-review-iter1`

Verdict: `VERDICT: REVISE`

Major finding:

- The P0 subplan still used stale reference-type names
  `transformed_exact` and `gaussian_mixture_approximation`, conflicting with
  the master/result vocabulary and risking exactness overclaim outside LGSSM.

Minor findings:

- The subplan omitted `blocked_only`.
- The result status used a pending pass-like token instead of a distinct
  pending state.
- The P0 local stop rule was not self-contained.

Repairs:

- P0 subplan now uses `transformed_actual_nongaussian`,
  `gaussian_mixture_surrogate`, and `blocked_only`.
- P0 result status now uses `PENDING_CLAUDE_REVIEW` until Claude agrees.
- P0 subplan now restates the five-iteration review/block rule.

### Iteration 2

Reviewer: `filter-benchmark-gap-p0-review-iter2`

Verdict: `VERDICT: AGREE`

Claude reported no major or minor issues.
