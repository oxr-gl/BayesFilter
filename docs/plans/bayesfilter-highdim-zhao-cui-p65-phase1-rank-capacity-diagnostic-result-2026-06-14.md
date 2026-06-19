# P65 Phase 1 Result: One-Factor Rank/Capacity Diagnostic

metadata_date: 2026-06-14
status: REPAIR_TARGET_IDENTIFIED
phase: 1
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Phase 1 identified the bounded repair target.  Under the fixed P64 branch, the
nominal high branch passes P59 assembly but its fitted square-root TT is
essentially zero, so the squared-TT transport is defensive-only.

The current evidence supports this repair target:

`BLOCK_P65_HIGH_RANK_FIXED_ALS_ZERO_SQRT_TT`

Phase 1 did not prove the causal mechanism.  Phase 2 must therefore be a
bounded repair-mechanism phase for this blocker, not a broad implementation
launch and not a stop caused by lack of a target.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Which single factor first prevents high-rank defensive-only collapse? |
| Baseline/comparator | Phase 0 full P64 tuple: `sample_count=1`, `fit_sample_count=2`, low `(degree=0, rank=1)`, high `(degree=1, rank=2)`. |
| Primary diagnostic criterion | Passed as a target-localization diagnostic: no tested one-factor row prevented high defensive-only collapse, and the repair target was narrowed to the high-rank fitted square-root TT becoming zero or near-zero. |
| Veto diagnostics | No target/order/axis, defensive `tau`, artificial fit-data, threshold, or hidden adaptive reselection drift was used. |
| Not concluded | No bug fix, no default change, no d=18 correctness, no rank convergence theorem, no adaptive Zhao--Cui parity. |

## Rows Executed

All rows used CPU-only execution with `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`.
TensorFlow emitted CUDA-registration/cuInit chatter despite CPU hiding; this was
treated as environment noise because no GPU evidence was requested.

### Baseline

Parameters:

```json
{
  "sample_count": 1,
  "fit_sample_count": 2,
  "low_fit_degree": 0,
  "high_fit_degree": 1,
  "low_fit_rank": 1,
  "high_fit_rank": 2
}
```

Result:

- status: `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE`;
- blockers: `candidate_high_defensive_only_transport`,
  `log_marginal_delta_threshold_exceeded`,
  `normalizer_increment_delta_threshold_exceeded`;
- high defensive-only steps: `[1, 2]`;
- high fitted square-root normalizers: `[0.0, 0.0]`;
- low fitted square-root normalizers:
  `[0.2998106156394979, 0.9999999900000001]`;
- high defensive `tau`: `[1e-08, 1e-08]`;
- local clipping fraction for high fit data: `[0.0, 0.0]`;
- source push ESS for high fit data:
  `[1.889244468079848, 1.561405695592051]`.

### Fit-Data Capacity Rows

The retained sample count, degrees, ranks, target order, previous-marginal axes,
defensive convention, and P60 thresholds were held fixed.  Only
`fit_sample_count` changed.

| `fit_sample_count` | status | high defensive-only steps | high fitted square-root normalizers | high fit local clipping | high fit source ESS |
| --- | --- | --- | --- | --- | --- |
| 3 | `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE` | `[1, 2]` | `[0.0, 0.0]` | `[0.0, 0.0]` | `[2.719946357958794, 2.2210152800269247]` |
| 4 | `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE` | `[1, 2]` | `[0.0, 0.0]` | `[0.0, 0.0]` | `[3.567872838121165, 3.7094657178156036]` |
| 6 | `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE` | `[1, 2]` | `[0.0, 0.0]` | `[0.0, 0.0]` | `[5.438749263792016, 4.887057411819914]` |

Interpretation: increasing source-pushed fit-data capacity through the reviewed
small ladder does not prevent high-rank defensive-only collapse.  This is not a
proof that fit-data capacity can never matter; larger rows would require a new
execution plan because each row costs roughly two to three minutes.

### Degree/Rank Tuple Screen

Claude review required this row family to be interpreted only as a tuple-level
screen, not as isolated evidence for degree alone or rank alone.

Parameters:

```json
{
  "sample_count": 1,
  "fit_sample_count": 2,
  "low_fit_degree": 0,
  "high_fit_degree": 0,
  "low_fit_rank": 1,
  "high_fit_rank": 2
}
```

Result:

- status: `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE`;
- high defensive-only steps: `[1, 2]`;
- high fitted square-root normalizers: `[0.0, 0.0]`;
- low fitted square-root normalizers:
  `[0.2998106156394979, 0.9999999900000001]`;
- source invariants preserved.

Interpretation: removing the linear basis component from the high tuple did not
prevent collapse.  This does not isolate rank alone, but it makes a pure
linear-basis explanation unlikely for the current tiny fixed branch.

## Mechanism Diagnostic

A diagnostic reran the baseline comparator and inspected the realized fitted TT
core norms from the branch manifests and density objects.

| Candidate | Step | Degree | Rank | Square-root normalizer | Core norm range | Zero core count | Fit residual | Fit status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| low | 1 | 0 | 1 | `0.2998106156394979` | `[0.5475496531287293, 1.0]` | 0 | `0.4524503441335226` | `OK` |
| low | 2 | 0 | 1 | `0.9999999900000001` | `[0.999999995, 1.0]` | 0 | `4.999999969612645e-09` | `OK` |
| high | 1 | 1 | 2 | `0.0` | `[0.0, 1.459004296685449e-13]` | 32 | `0.710297078373578` | `OK` |
| high | 2 | 1 | 2 | `0.0` | `[0.0, 2.4654500945965524e-13]` | 32 | `1.0` | `OK` |

The high branch is not merely reporting a zero normalizer.  The fitted
square-root TT cores are zero or near-zero after the fixed ALS fit, while the
fit status remains `OK` and condition numbers are reported as benign.

## Interpretation

The author algorithm uses adaptive/random sample generation and rank/basis
selection in the source route.  Our fixed-HMC variant freezes branch choices and
uses tiny deterministic fit-data and retained-sample counts.  Under the tested
fixed variant, the observed failure signature is that the high branch passes
assembly while the realized fitted square-root TT cores are zero or near-zero.
One plausible hypothesis is an underdetermined or otherwise degenerate fixed-ALS
fit at the declared high rank, but Phase 1 has not proved that causal mechanism.
The defensive density then correctly rescues nonzero proposal mass with
`tau=1e-8`, but the branch is defensive-only and fails the P60 gate.

This points to a fixed-variant admissibility or stabilization question, not a
Zhao--Cui defensive-density bug and not a reason to remove or rescale defensive
`tau`.

## Phase 2 Handoff

Do not launch the existing Phase 2 implementation-repair subplan as written,
because it was drafted before the Phase 1 target was known.  Refresh Phase 2
around the concrete repair target:

`BLOCK_P65_HIGH_RANK_FIXED_ALS_ZERO_SQRT_TT`

The refreshed Phase 2 plan must separate the repair target from the unproved
mechanism.  It should test a bounded mechanism and repair this blocker without
changing the target, previous-marginal axes, defensive `tau`, source-pushed fit
data route, or P60 thresholds.

Candidate Phase 2 routes, in increasing scientific risk, are:

- an admissibility guard that detects the zero square-root TT and prevents
  promoting a collapsed high-rank branch; this is useful for fail-closed
  behavior but is not by itself a repair of the high branch;
- a fixed-branch stabilization or initialization rule that prevents the fitted
  square-root tensor from collapsing, with paper/source anchors and mathematical
  documentation before implementation;
- a larger reviewed diagnostic plan if the project wants to test whether
  substantially larger fit-data capacity rescues rank-2 without changing the
  fixed branch.

Forbidden Phase 2 shortcuts:

- do not remove defensive `tau`;
- do not weaken P60 thresholds;
- do not hide defensive-only collapse by changing the gate;
- do not introduce artificial reference-grid fit data;
- do not call an admissibility guard a source-faithful Zhao--Cui repair unless
  paper and author-source anchors are recorded.

## Required Review

Before any implementation patch, run bounded Claude review on this result and
the refreshed Phase 2 subplan.  The review should check whether the blocker
interpretation is supported and whether the proposed Phase 2 target is a guard,
stabilization, or broader diagnostic rather than an unreviewed algorithm change.
