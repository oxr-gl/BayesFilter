# LEDH-PFPF-OT LGSSM Value-Decomposition Hypothesis Test Plan

Date: 2026-06-26

## Objective

Localize the source of the LGSSM value gap observed in the N1000/N2000
LEDH-PFPF-OT statistical harness. The immediate question is whether the gap
appears before OT transport, only after OT transport resets the cloud to uniform
weights, or under a specific proposal-density/log-determinant correction.

## Evidence Contract

| Field | Contract |
|---|---|
| Scientific/engineering question | Which value-path component first creates the gap between LEDH-PFPF-OT and the exact FP64 Kalman likelihood on the 1d/2d T=10 LGSSM fixture? |
| Baseline/comparator | FP64 analytic Kalman transition-first likelihood from `tf_batched_kalman_value_and_score`; prior N1000/N2000 LEDH+OT failures from `bayesfilter-ledh-pfpf-ot-lgssm-kalman-n1000-xla-statistical-result-2026-06-26.md`. |
| Candidate arms | Plain no-transport SIS; LEDH flow without OT, preserving corrected weights; LEDH flow plus OT, current route; shifted-observation Kalman convention probe; optional proposal-correction sign probes only if cheap and explicitly labeled diagnostic. The LEDH-without-OT and LEDH+OT arms must share the same pre-OT state, seeds, particles, weights, flow outputs, and corrected log weights through each time step; their first permitted divergence is the transport/reset operation after the same increment is recorded. |
| Primary diagnostic criterion | For each arm and time prefix, compute `z = abs(mean - reference) / max(MCSE, 1e-8)` and also record `abs(mean - reference) / max(seed_sd, 1e-8)`. Treat `z > 2` as a mean-level statistical failure and `abs(delta) > 2 * seed_sd` as a seed-spread failure. The first failing arm/time is the earliest prefix where both tests fail; otherwise mark the evidence as ambiguous. |
| Veto diagnostics | Nonfinite outputs; wrong device/scope record; route using generic autodiff or `transport_ad_mode=full`; no exact arm labels; artifacts missing per-time increments and seed summaries. |
| Explanatory-only diagnostics | Runtime, CUDA duplicate-registration warnings, N sensitivity, row residuals, seed SD, MCSE, and small-N smoke behavior. |
| Not concluded even if localized | No gradient correctness, no SIR correctness, no large-N production validity, no posterior correctness, no HMC readiness, and no proof that LEDH-PFPF-OT is invalid in general. |
| Artifact | JSON and markdown result under `docs/plans/`, plus any focused diagnostic script if needed. |

## Skeptical Plan Audit

| Risk | Audit response |
|---|---|
| Wrong baseline | Use the same FP64 Kalman helper and same observation/parameter fixture as the failing harness. Do not compare against a different LGSSM. |
| Proxy metric becoming promotion criterion | Treat decomposition as localization only. Passing an arm does not certify gradients or production readiness. |
| Missing stop conditions | Stop if an arm is nonfinite, if GPU/XLA route cannot launch under trusted visibility, or if the result lacks per-time increments. |
| Unfair comparison | Keep all particle arms on the same seeds, initial particles, transition noise, parameters, observations, and transition-first convention. |
| Hidden environment mismatch | Record `CUDA_VISIBLE_DEVICES`, TF32 status, dtype, particle count, seed count, time steps, and device scope in the artifact. |
| Artifact would not answer the question | Require seed-level values, mean/SD/MCSE, total and per-time increment deltas, and explicit arm labels. |

Audit verdict: PASS to execute after Claude read-only review of this plan. The
plan is bounded and localizes the value scalar; it does not attempt to fix the
algorithm or interpret gradients.

## Hypotheses Tested

1. **OT reset semantics**: the value gap appears only after replacing the
   weighted cloud with transported particles and uniform weights. This is tested
   by forcing the LEDH-without-OT and LEDH+OT arms to share an identical pre-OT
   path at every time and diverge only in the next-time particle/weight state.
2. **LEDH proposal correction**: the gap appears in the LEDH flow arm before OT,
   implicating proposal density or log-determinant accounting.
3. **Plain particle-count error**: the no-transport SIS arm remains far from
   Kalman, contrary to the previous small diagnostic.
4. **Time-index/comparator mismatch**: per-time increments and explicit shifted
   Kalman convention probes distinguish transition-first, observe-initial-first,
   and one-step-shifted observation alignments.

## Execution Steps

1. Create a focused value-decomposition diagnostic script or test helper that
   reuses the LGSSM fixture from
   `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py`.
2. Run fast local checks:
   - `python -m py_compile <diagnostic-script>`
   - `python -m py_compile tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py`
3. Run the diagnostic under trusted GPU visibility if executing the current
   LEDH+OT route:
   - `BAYESFILTER_TEST_DEVICE_SCOPE=visible`
   - `CUDA_VISIBLE_DEVICES=0`
   - `TF_FORCE_GPU_ALLOW_GROWTH=true`
   - TF32 enabled for LEDH; FP64 only for the Kalman reference.
4. Write JSON and markdown result artifacts with:
   - run manifest;
   - per-arm total value mean/SD/MCSE;
   - per-time increment means;
   - prefix means, SDs, MCSEs, and z-scores against the matching Kalman prefix;
   - shifted-observation/convention probe values;
   - deltas to Kalman;
   - interpretation table.
5. Analyze which hypothesis is strengthened or weakened.

## Stop Conditions

- Claude plan review returns `VERDICT: FAIL` with a material unpatched problem.
- Trusted GPU launch is blocked twice by approval or environment issues.
- Diagnostic output is nonfinite or lacks per-arm/per-time evidence.
- The implementation would require changing production LEDH code before a
  localization result exists.

## Boundary Safety

- Do not modify production LEDH or transport implementation in this phase.
- Do not claim gradient correctness from value decomposition.
- Do not use generic autodiff as a production score route.
- Do not use `transport_ad_mode=full`.
- Do not run non-escalated GPU/CUDA TensorFlow commands.
