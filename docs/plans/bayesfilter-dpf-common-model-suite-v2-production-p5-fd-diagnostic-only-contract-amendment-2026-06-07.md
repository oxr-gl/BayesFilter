# DPF Common Model Suite V2 P5 FD Diagnostic-Only Contract Amendment

metadata_date: 2026-06-07
phase: P5
status: CLAUDE_REVIEWED_PASS_FOR_EXECUTION

## Human Evidence-Contract Decision

The user clarified on 2026-06-07 that finite differences must not be a P5
gate:

```text
Did we use FD as a gate or diagnostic only?  FD should not be a gate.  It is
not numerically stable.
```

This amendment records that correction and prevents a numerically fragile
central finite-difference check from blocking a BF/FF fixed-branch AD-gradient
tie-out when the two implementations agree on the same scalar and the same AD
gradient.

## Problem

The current P5 subplan, runner, result ledger, and Claude ledger treated
same-implementation central finite differences as a primary/veto condition.
That was too strong.  In the range-bearing row, BayesFilter and FilterFlow
matched exactly on the fixed-branch scalar and AD gradients, but both showed the
same central finite-difference discrepancy at the frozen step `1e-5`.  The
explanatory ladder then decreased to about `2.5282474780397024e-8` at `1e-7`.

The old gate therefore blocked P5 because of a finite-difference numerical
resolution issue, not because BF and FF disagreed.

## Corrected P5 Evidence Contract

Primary criterion:

- For every required P1-ready non-blocked gradient knob, BayesFilter and
  executable local float64 FilterFlow-side adapters must match on:
  - the fixed-branch scalar value within declared value tolerance;
  - the AD physical-knob gradient within declared gradient tolerance.
- Executed gradients and scalar values must be finite.
- The SIR row remains `CONTRACT_BLOCKED` unless a reviewed physical-knob
  gradient contract exists.

Veto diagnostics:

- changed knobs, fixtures, scalar, branch, tolerance, comparator, or physical
  parameterization after seeing results;
- parameterization mismatch between BF and FF;
- nonfinite scalar or AD gradient in an executed required row;
- gradient through random or discrete ancestor selection is claimed;
- value match is used to excuse a BF/FF AD-gradient mismatch;
- old v1 source or old artifact names leak into v2 execution;
- student implementation command is executed;
- `.localsource/filterflow` is mutated;
- unclassified BF/FF scalar or AD-gradient mismatch.

Explanatory-only diagnostics:

- central finite-difference gradients;
- AD-vs-FD deltas;
- FD step ladders and decreasing-window behavior;
- FD pass/fail booleans retained for historical interpretability;
- historical disconnected-zero-gradient FD guard records.

The FD diagnostics may nominate follow-up debugging, but cannot by themselves
fail a row or block promotion when BF/FF scalar and AD-gradient equality holds.
The earlier P5 disconnected-zero-gradient repair amendment is superseded to the
extent it used FD-zero or FD-nonzero checks as a promotion or veto condition.
Disconnected or inactive gradient knobs must now be handled by predeclared
contract classification, derivation, or reviewed row/knob exclusion, not by an
FD pass/fail check.

## Implementation Scope

Patch only:

- `experiments/dpf_implementation/tf_tfp/runners/run_common_model_suite_v2_gradients_tf.py`;
- P5 subplan/result/review ledgers under `docs/plans`;
- regenerated P5 JSON and markdown artifacts.

Do not change:

- fixtures, particles, observations, innovations, ancestor indices, resampling
  flags, scalar objective, model equations, parameter values, tolerances, or
  branch semantics;
- `.localsource/filterflow`;
- student implementation artifacts or commands.

## Required Runner Semantics

- Row status `MATCHED` depends on BF/FF scalar equality, BF/FF AD-gradient
  equality, and finite scalar/AD gradients.
- FD fields remain computed and reported in `explanatory_only_fields` and cell
  metrics.
- `finite_difference_self_check_failed` must be renamed or demoted so it is no
  longer a veto diagnostic.
- The previous FD-zero guard for disconnected AD `None` gradients must not
  decide promotion or row status. If an included required knob produces a
  disconnected AD gradient under the frozen scalar, the row must be contract
  classified before promotion unless a derivation or reviewed amendment
  justifies the inactive knob treatment without using FD as the deciding gate.
- The markdown must state explicitly that FD is diagnostic-only and numerically
  fragile.
- Historical P5 blocker text must be superseded, not hidden.

## Skeptical Plan Audit

Status: `PASS_FOR_REVIEW_AS_CONTRACT_CORRECTION_DRAFT`.

This amendment does not claim either implementation is correct.  It only fixes
the P5 comparator question: do BayesFilter and FilterFlow agree with each
other on the same fixed branch and same AD-gradient scalar?  Finite differences
are an unstable same-implementation diagnostic and are not a reliable oracle.
The risk is over-promotion from matching AD code paths; the mitigation is to
keep non-claims explicit and preserve the FD discrepancy as explanatory
evidence.

## Fresh Evidence Required

1. Run Claude review of this amendment to PASS or max five rounds.
2. Patch only the reviewed scope.
3. Rerun:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_gradients_tf
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-mpl python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_gradients_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_gradients_2026-06-07.json
git diff --check
```

4. Run Claude P5 result/governance review.

## Non-Claims

- no filtering-algorithm correctness proof;
- no proof that BayesFilter or FilterFlow is mathematically correct;
- no stochastic-resampling gradient claim;
- no gradient-through-ancestor-selection claim;
- no student repository tie-out claim;
- no TT/SIRT or paper-table claim.
