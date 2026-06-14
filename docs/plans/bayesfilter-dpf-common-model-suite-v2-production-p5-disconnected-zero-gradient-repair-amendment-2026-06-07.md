# DPF Common Model Suite V2 P5 Disconnected Zero-Gradient Repair Amendment

metadata_date: 2026-06-07
phase: P5
status: REVIEWED_PASS

## Blocker Classification

blocker_type: `FIXABLE_PRE_EXECUTION_GRADIENT_CONTRACT_CLARIFICATION`

The P5 skeptical audit found a pre-result implementation hazard. Some P1
gradient knobs are physical transition-scale parameters, such as `sigma` in
the stochastic-volatility and structural AR(1) rows. Under the frozen P1 path
contract, transition innovations are fixed additive state increments, and the
P5 scalar is the fixed-branch sum of predictive log normalizers. That scalar
does not include transition log densities and does not use standardized
transition noise. Therefore these transition-scale knobs can be mathematically
inactive for this fixed-branch scalar.

TensorFlow may report the AD gradient of such an inactive variable as `None`.
For P5 this must not be treated as either a missing derivative or a hidden
success. The correct local derivative of a constant scalar with respect to an
inactive physical knob is zero, but only if the central finite-difference
self-check is also zero within the declared tolerance.

## Proposed Repair

1. Keep the frozen P1 fixtures, scalar, branch, ancestor indices, tolerances,
   and P5 ready/block classifications unchanged.
2. Do not remove required knobs from P5, and do not promote the blocked SIR row.
3. In both BayesFilter and FilterFlow adapter outputs, convert an AD `None`
   gradient to explicit `0.0` only when the same-implementation central
   finite-difference gradient for that knob is within the declared
   finite-difference tolerance of zero.
4. Record the knob name in a `disconnected_zero_gradient_knobs` field for that
   implementation and cell.
5. Treat any `None` gradient with nonzero finite-difference evidence as a veto,
   not as a match.
6. Preserve the non-claim that this is not a stochastic-filter gradient,
   transition-density gradient, differentiable-resampling gradient, or proof of
   scientific validity.

## Why This Is Not A Scientific-Contract Change

The amendment does not change the scalar, branch, fixtures, tolerances,
parameter values, comparator, or P1 ready/block table. It only makes explicit
how to encode the derivative of an inactive variable under the already frozen
fixed-additive-innovation scalar. The finite-difference veto remains the guard:
zero AD is accepted only when the same scalar is numerically flat under central
finite differences.

## Implementation Scope

- Patch only
  `experiments/dpf_implementation/tf_tfp/runners/run_common_model_suite_v2_gradients_tf.py`.
- Update the P5 subplan pre-execution audit note to cite this amendment if
  Claude passes it.
- Do not touch `.localsource/filterflow`.
- Do not run student implementations.

## Required Review Question

Claude should decide whether this amendment is acceptable as a P5
pre-execution repair, or whether it is a material scientific-contract change
requiring human intervention.
