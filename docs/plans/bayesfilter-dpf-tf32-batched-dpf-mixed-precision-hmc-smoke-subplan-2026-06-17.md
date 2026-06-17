# Mixed-Precision HMC Smoke Subplan - 2026-06-17

## Objective

Test the sensible mixed-precision boundary for experimental LEDH-PFPF-OT:
HMC state, step size, leapfrog bookkeeping, and MH diagnostics remain FP64,
while the DPF likelihood/score computation may run in FP32/TF32 internally and
return value/score tensors cast back to the HMC state dtype.

## Entry Conditions

- Phase 6 closeout exists with status
  `PHASE_6_CLOSEOUT_GUARDRAILS_PASSED`.
- Phase 5 recorded that direct GPU TF32 full-chain HMC mechanics was blocked
  by dtype plumbing, not by a sampler veto.
- No public/default/HMC-readiness claim has been made.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the HMC runner remain FP64 while a DPF adapter computes target value/score internally in FP32/TF32 and returns FP64-compatible tensors to TFP HMC? |
| Baseline/comparator | Phase 5 CPU FP64 HMC mechanics smoke and the previously failed GPU TF32 smoke log. |
| Primary pass criterion | Tiny GPU0 mixed-precision HMC mechanics smoke exits 0 with finite initial value/score, finite samples, finite target log prob, finite log accept ratios, and MH trace present. |
| Veto diagnostics | Non-finite value/score, samples, target log prob, or log accept ratios; missing MH trace; wrong trusted GPU placement; unsupported default/HMC/posterior claim. |
| Explanatory diagnostics | Acceptance rate, runtime, and short-chain trace values. |
| What will not be concluded | No HMC readiness, posterior correctness, chain convergence, TF32 superiority, production/default readiness, or full FP32 HMC mechanics claim. |
| Artifact preserving result | JSON/Markdown smoke artifact and this plan/result pair. |

## Skeptical Audit

- Wrong baseline: this plan tests mixed-precision target computation, not full
  FP32 HMC state mechanics.
- Proxy metric risk: acceptance and runtime are explanatory only.
- Missing stop condition: any non-finite HMC diagnostic or missing MH trace
  blocks passage.
- Unfair comparison: no ranking against FP64 or FP32-no-TF32 is claimed here.
- Hidden assumption: the adapter must cast internally to its computation dtype;
  HMC must see FP64-compatible value/score tensors.
- Environment mismatch: GPU evidence must run in trusted GPU context.
- Artifact adequacy: the smoke JSON must record HMC state dtype separately
  from DPF target computation dtype.

## Required Artifacts

- This subplan.
- Mixed-precision result:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-mixed-precision-hmc-smoke-result-2026-06-17.md`.
- GPU0 JSON/Markdown artifacts under `docs/benchmarks/`.
- Full command log under `docs/benchmarks/logs/`.

## Required Checks

1. Run focused Python tests for HMC/value-score dtype boundary.
2. Run CPU FP32-no-TF32 mixed-precision smoke as a cheap plumbing check.
3. Run trusted GPU0 FP32/TF32 mixed-precision smoke.
4. Run `git diff --check`.

## Forbidden Claims

- Do not claim HMC readiness.
- Do not claim posterior correctness or convergence.
- Do not claim production/default/public API readiness.
- Do not claim TF32 superiority.
- Do not claim full FP32 HMC mechanics.

## Stop Conditions

Stop and write a blocker if the target boundary cannot cast value/score back
to FP64 without changing shared HMC semantics, if GPU placement fails in
trusted context, or if any required hard-veto diagnostic is non-finite.
