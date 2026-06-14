# DPF Common Model Suite V2 P5 Range-Bearing FD Veto Repair Amendment

metadata_date: 2026-06-07
phase: P5
status: REVIEWED_PASS

## Blocker Classification

blocker_type: `FIXABLE_NUMERICAL_DIAGNOSTIC_BLOCKER_PENDING_REVIEW`

The first P5 evidence run produced:

- BF/FF scalar agreement: exact within recorded precision for every executed
  row.
- BF/FF AD-gradient agreement: exact within recorded precision for every
  executed row.
- SIR remained `CONTRACT_BLOCKED` as required.
- AD-vs-central-FD veto failed only for `range_bearing_4d_h20_rich`, with max
  FD discrepancy about `1.1556379445210041e-4` on `sigma_bearing` at the frozen
  FD step `1e-5`.

The result is a legitimate P5 block under the current evidence contract. It
must not be promoted by tolerance relaxation or by ignoring finite differences.

## Hypothesis

The range-bearing FD veto is likely a finite-difference diagnostic resolution
issue rather than a BF/FF implementation disagreement, because both
implementations produce identical AD gradients and identical central-FD
gradients at the same step. The bearing-noise gradient is large and the
log-likelihood curvature in a small positive scale parameter can make a single
FD step misleading.

This is only a hypothesis. It does not pass P5.

## Proposed Repair

1. Preserve all frozen fixtures, scalar definitions, branch semantics,
   ancestor indices, parameter values, P1 classifications, and pass/fail
   tolerances.
2. Add an explanatory finite-difference ladder for every executed P5 knob using
   steps `[1e-3, 3e-4, 1e-4, 3e-5, 1e-5, 3e-6, 1e-6]`.
3. Keep the original `1e-5` FD check and tolerance as the primary P5 veto unless
   a separate reviewed amendment explicitly changes the evidence contract.
4. Record ladder results under `explanatory_only_fields` and per-cell metrics.
5. Classify `range_bearing_4d_h20_rich` as a reviewed FD diagnostic blocker if
   the primary `1e-5` veto remains failed.
6. If the ladder shows a stable near-zero AD-vs-FD discrepancy at other steps,
   the next action is to write a separate evidence-contract amendment for a
   scale-aware FD diagnostic or an analytic second-order diagnostic, not to
   silently pass P5.
7. If the ladder does not show stability, keep P5 blocked and investigate the
   range-bearing gradient formula.

## Why This Is Not A Tolerance Relaxation

This amendment does not change the primary FD tolerance or the primary FD step.
It only adds an explanatory diagnostic ladder to distinguish numerical FD
resolution from a real derivative problem. P5 remains blocked unless a later
reviewed amendment changes the evidence contract or the primary check passes
without tolerance relaxation.

## Implementation Scope

- Patch only
  `experiments/dpf_implementation/tf_tfp/runners/run_common_model_suite_v2_gradients_tf.py`
  to record explanatory FD ladders.
- Update the P5 result/ledger to state that the current run is blocked pending
  diagnosis if the primary veto remains failed.
- Do not touch `.localsource/filterflow`.
- Do not run student implementations.

## Required Review Question

Claude should decide whether adding an explanatory FD-step ladder is an
acceptable self-recovery diagnostic under the gated plan, or whether this
requires human intervention before any further P5 action.
