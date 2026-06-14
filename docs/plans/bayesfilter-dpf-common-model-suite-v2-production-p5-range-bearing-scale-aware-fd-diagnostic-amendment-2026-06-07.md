# DPF Common Model Suite V2 P5 Range-Bearing Scale-Aware FD Diagnostic Amendment

metadata_date: 2026-06-07
phase: P5
status: REVIEWED_PASS_FOR_DIAGNOSTIC_ONLY

## Blocker Classification

blocker_type: `P5_BLOCKED_FOLLOW_UP_DIAGNOSTIC_PENDING_REVIEW`

P5 remains blocked under the frozen primary evidence contract. The
`range_bearing_4d_h20_rich` row failed the primary AD-vs-central-FD veto at
step `1e-5`, with max discrepancy about `1.1556379445210041e-4` on
`sigma_bearing`, above the frozen tolerance `5e-5`.

The explanatory FD ladder showed monotone convergence toward the AD gradient
as the step decreased, with the same pattern for BayesFilter and FilterFlow.
This supports, but does not prove, the hypothesis that the failure is a
single-step finite-difference resolution issue for a positive scale parameter.

## Question

For the range-bearing row only, can a reviewed scale-aware diagnostic establish
that the AD gradient is locally consistent with finite differences without
changing the frozen P5 scalar, fixtures, branch, ancestor indices, parameter
values, row classification, or original primary veto status?

## Evidence Contract

Primary status:

- P5 remains `BLOCKED`; this follow-up cannot promote P5 to P6.
- The original `1e-5` FD veto remains recorded as failed.
- This diagnostic is explanatory evidence for a later human/reviewed decision,
  not a pass criterion for the current P5 gate.

Diagnostic criteria:

- Run only `range_bearing_4d_h20_rich` under the same frozen P5 scalar and
  branch.
- Evaluate symmetric central finite differences over a scale-aware positive
  parameter step ladder, including `[1e-5, 3e-6, 1e-6, 3e-7, 1e-7]`, without
  clipping or reparameterizing the physical scale.
- Record whether the AD-vs-FD discrepancy decreases with smaller valid steps
  and whether both BF and FF show identical diagnostic behavior.
- Add an optional complex-step or high-precision analytic diagnostic only if it
  can be implemented without changing the scalar or requiring new dependencies.

Veto diagnostics:

- Any change to scalar, fixtures, branch, ancestor indices, parameter values,
  or P1 classifications.
- Any attempt to promote P5 based on this diagnostic alone.
- Any clipping, one-sided FD substitution, or log-scale reparameterization
  unless separately reviewed.
- Any `.localsource/filterflow` mutation.
- Any student implementation command.

Non-claims:

- No P5 pass.
- No stochastic resampling or stochastic-filter gradient claim.
- No scientific correctness claim.
- No student repository claim.

## Planned Implementation Scope

- Patch only the P5 runner if needed to add smaller explanatory ladder steps
  for the existing range-bearing diagnostic.
- Preserve all existing artifacts and append/update the P5 result with an
  explicit BLOCK decision and diagnostic interpretation.
- Add a P5 Claude review ledger recording the BLOCK and the diagnostic outcome.

## Stop Conditions

- If Claude decides this is a scientific-contract change, stop for human
  intervention.
- If the smaller-step ladder is unstable or contradicts AD, keep P5 blocked and
  stop for human scientific review.
- If any required infrastructure is unavailable, keep P5 blocked.

## Required Review Question

Claude should decide whether this focused diagnostic is allowed under the
gated self-recovery plan, and whether it can be executed without weakening the
P5 evidence contract.
