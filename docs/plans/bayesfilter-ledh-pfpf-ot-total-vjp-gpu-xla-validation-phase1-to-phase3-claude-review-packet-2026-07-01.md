# Claude Review Packet: Total-VJP GPU/XLA Phase 1 To Phase 3

Status: `READY_FOR_REVIEW`

## Role Contract

Codex is supervisor and executor.  Claude is read-only reviewer only.  Claude
must not edit files, run experiments, launch agents, or change state.

## Question

Check whether Phase 1 is properly closed as passed, Phase 2 is properly skipped
as not needed, and Phase 3 is safe to launch as the next material GPU/XLA
particle ladder.

## Scope

Review only these files:

- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase0-route-inventory-result-2026-07-01.md`
  - static dispatch proof inherited by Phase 1 and Phase 3.
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-subplan-2026-07-01.md`
  - reviewed Phase 1 gate.
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-result-2026-07-01.md`
  - Phase 1 close record.
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-2026-07-01.json`
  - Phase 1 machine-readable output.
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase2-harness-repair-result-2026-07-01.md`
  - skipped Phase 2 close record.
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-particle-ladder-subplan-2026-07-01.md`
  - next subplan.
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-visible-execution-ledger-2026-07-01.md`
  - execution ledger.

Out of scope:

- judging HMC readiness;
- posterior correctness;
- exact nonlinear likelihood correctness;
- production/default promotion;
- code edits.

## Evidence

Commands actually run:

| Command | Exit | Key output | Artifact |
| --- | ---: | --- | --- |
| `bash scripts/run_total_vjp_gpu_xla_phase1_smoke.sh` | 0 | TensorFlow created `/device:GPU:0`; XLA compiled `manual_reverse_seed_microbatch_value_score`; JSON status `pass` | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-2026-07-01.json` |
| Phase 1 JSON gate script | 0 | `PHASE1_JSON_GATE_PASS` | console output recorded in Phase 1 result |

Phase 1 key JSON values:

- `status`: `pass`
- `primary_pass`: `true`
- `device`: `/GPU:0`
- `output_devices`: both `/job:localhost/replica:0/task:0/device:GPU:0`
- `compiler.mode`: `xla`
- `compiler.jit_compile`: `true`
- `transport.gradient_mode`: `manual_streaming_finite_sinkhorn_stopped_scale_keys`
- `transport.transport_ad_mode`: `full`
- `objective`: `-36.1256103515625`
- `gradient_values`: `[-9.37370777130127, 3.432502508163452, 4.548910617828369]`
- `gradient_finite`: `true`
- `gradients_connected`: `true`
- `monte_carlo_gradient_noise_mcse_finite`: `true`
- `elapsed_seconds`: `48.501640795962885`

Important inherited fact:

- Phase 0 statically proved that the legacy selector name
  `manual_streaming_finite_sinkhorn_stopped_scale_keys`, when paired with
  `transport_ad_mode="full"`, dispatches to
  `_filterflow_manual_streaming_finite_transport_total_vjp`.  Therefore the
  legacy selector name is not being treated as the derivative claim.

## Pass/Block Criteria

Pass if all hold:

- Phase 1 result satisfies the Phase 1 subplan gate.
- Phase 2 skip is justified because Phase 1 used the existing harness
  successfully.
- Phase 3 subplan states required objective, entry conditions, artifacts,
  checks/tests/reviews, evidence contract, forbidden claims/actions, exact
  next-phase handoff conditions, and stop conditions.
- Phase 3 ladder commands preserve trusted GPU, float32/TF32, manual-reverse
  XLA, streaming transport, `transport_ad_mode="full"`, and route metadata
  gates.
- The plan does not claim HMC readiness, posterior correctness, exact nonlinear
  likelihood correctness, or production promotion.

Block if any hold:

- Phase 1 result does not actually prove GPU/XLA full-route smoke success.
- Phase 2 skip hides a required harness repair.
- Phase 3 subplan lacks a material stop condition or uses a wrong baseline.
- Phase 3 can advance despite CPU fallback, missing XLA, nonfinite outputs, or
  `transport_ad_mode!="full"`.
- The packet or artifacts use the stopped partial derivative as a correctness
  baseline.

## Known Limitations

- Phase 1 is tiny: `N=16`, `T=1`, two seeds.
- Phase 3 is a viability/scaling ladder, not a finite-difference agreement
  test.
- `N=1000` is conditional and should be skipped if earlier memory/runtime is
  unsafe.

## Nonclaims

Even if this review passes, do not conclude:

- HMC direction validity;
- posterior correctness;
- exact nonlinear likelihood score correctness;
- production/default promotion;
- that the stopped partial derivative route is a score.

## Requested Verdict

Findings first if any.  End with exactly:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
