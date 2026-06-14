# P60-3 Subplan: Same-Target Reference Or Bridge

metadata_date: 2026-06-12
status: PLAN_CREATED_NOT_EXECUTED

## Question

What reference evidence is strong enough to call the d=18 author-SIR
source-route result a correctness candidate rather than merely a rank-stable
implementation?

## Preconditions

- P60-1 has `PASS_P60_1_SOURCE_RANK_COMPARATOR_CONTRACT`.
- P60-2 should normally pass before this result is promoted.  If P60-2 is
  blocked, this phase may still audit reference options but must not promote
  correctness.

## Reference Options

P60-3 must audit feasible reference routes before choosing one:

1. same-target author-code bridge:
   - compare BayesFilter outputs to author-code route outputs if a trusted
     MATLAB/Octave execution path exists;
   - this is source-faithful but may be environment-limited.
2. lower-rung dense bridge:
   - build lower-dimensional SIR reductions where dense or high-accuracy
     reference integration is feasible;
   - show that the BayesFilter source-route implementation matches the
     reference on those reductions and that the d=18 route uses the same
     operations.
3. independent Monte Carlo bridge:
   - use a separately reviewed same-target estimator only if it has its own
     evidence contract and uncertainty intervals;
   - it cannot be a convenience proxy.

UKF is diagnostic-only and cannot be selected as the correctness reference.

## Tasks

1. Audit which reference option is feasible in the current environment.
2. Write the chosen reference/bridge contract before executing it.
3. If using author code, record command, environment, source commit/path, and
   output mapping into BayesFilter quantities.
4. If using lower-rung dense references, record the reduction map and prove or
   cite why the same source-route operations are being tested.
5. If using Monte Carlo, record the estimator, uncertainty interval, seeds,
   sample size, diagnostics, and why it is independent enough to be a bridge.
6. Emit a result artifact that either passes the bridge or blocks with the exact
   missing evidence.

## Pass Criteria

`PASS_P60_D18_CORRECTNESS_BRIDGE` requires:

- same-target or explicitly justified lower-rung bridge evidence;
- predeclared tolerances;
- uncertainty treatment where applicable;
- no UKF/memory/finite-value proxy promotion;
- no source-route drift.

## Block Criteria

`BLOCK_P60_D18_CORRECTNESS_BRIDGE` is required if no chosen reference option can
support the correctness-candidate claim.

It is also required if any reference or bridge tolerance, acceptance band, or
uncertainty threshold is widened after observing the reference result.

## Token

`PLAN_P60_3_SAME_TARGET_REFERENCE_BRIDGE`
