# P81 Route Correction: Zhao-Cui Analytical Derivative Is The Comparator

Date: 2026-06-22

Status: ROUTE_CORRECTION_REQUIRED_BEFORE_LEDHPFPFOT_COMPARISON

## Purpose

This note corrects the P81 continuation boundary before any
LEDH-PFPF-OT-versus-Zhao-Cui SIR d=18 gradient comparison.

The Zhao-Cui comparator for SIR gradient validation must be the implemented
analytical fixed-branch derivative route.  TensorFlow autodiff, including
`tf.autodiff.ForwardAccumulator` JVPs, is diagnostic-only and must not be
promoted to the primary candidate/comparator route.

## Skeptical Plan Audit

The previous P81 wording can be misread as making a
`ForwardAccumulator`/JVP-backed route the primary candidate.  That is the wrong
baseline for an LEDH-PFPF-OT gradient comparison if the intended comparator is
the Zhao-Cui analytical derivative.

Therefore, before running LEDH-PFPF-OT SIR gradient tests, any plan must first
name and verify the analytical Zhao-Cui derivative route.  If the only
available route in a proposed command is an autodiff/JVP route, the plan must
stop with a route-selection blocker rather than proceed.

This correction does not run a numerical experiment, change defaults, use GPU,
or claim new validation evidence.  It only records the comparator boundary.

## Current Checkout Evidence To Reconcile

The checkout contains the fixed-branch analytical score plumbing in
`bayesfilter/highdim/filtering.py`, including:

- `scalar_nonlinear_fixed_design_tt_score_path`;
- `multistate_nonlinear_fixed_design_tt_score_path`;
- fixed-branch derivative propagation through fitted TT cores;
- `analytic_score`, `total_score`, and finite-difference rows storing
  `analytic_gradient=total_score`.

However, the current P81 text and diagnostics also mention
`tensorflow_forward_accumulator_for_model_log_density` for local model
log-density directional derivatives.  That use must be classified as
diagnostic or as an implementation detail that needs replacement/route audit
before being used as the primary Zhao-Cui comparator.

## Binding Rule For The LEDH-PFPF-OT SIR Gradient Plan

Use the Zhao-Cui analytical derivative route as the comparator.

Autodiff/JVP may be used only for:

- diagnostic finite-difference or directional-derivative checks;
- isolated model-term sensitivity probes;
- sanity checks that do not define the promoted comparator;
- debugging a suspected analytic-route implementation bug.

Autodiff/JVP must not be used as:

- the primary Zhao-Cui SIR gradient candidate;
- the comparator for LEDH-PFPF-OT gradient agreement;
- evidence of analytical derivative correctness by itself;
- evidence for HMC readiness, posterior validity, or production readiness.

## Required Next Step

Before Phase 6-style LEDH-PFPF-OT comparison, write or patch the subplan so it
explicitly records:

1. the analytical Zhao-Cui derivative function/path used;
2. the exact theta convention and parameter order;
3. whether any local derivative component still calls TensorFlow autodiff/JVP;
4. if such a call remains, why it is diagnostic-only or why the plan stops;
5. the finite-difference diagnostic role and branch-hash stability checks;
6. the LEDH-PFPF-OT comparator budget, seeds, and veto diagnostics.

If the fully analytical SIR local derivative route cannot be located in the
current checkout, stop with `BLOCK_ANALYTICAL_ROUTE_NOT_SELECTED` and repair or
locate that route before comparing against LEDH-PFPF-OT.
