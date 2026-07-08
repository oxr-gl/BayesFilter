# Clean XLA JIT Visible Stop Handoff

Date: 2026-07-02

Status: `OWNER_ACCEPTED_WITH_FD_WAIVER`

Current status:

- The bounded clean-XLA fixture program is accepted and promoted by owner
  direction on 2026-07-03.
- The original preregistered Phase 7 same-scalar FD gate did not pass for
  `log_obs_noise_scale`; this is preserved as an explicit waiver, not rewritten
  as a pass.
- The route/GPU/repeat/HLO evidence passed for the tiny full-route fixture:
  `T=1`, `N=16`, one seed, TF32 enabled, `transport_ad_mode="full"`.

Historical note: visible execution initially stopped before Phase 0 because the required
Claude read-only launch review did not return a verdict.  After user challenge,
Codex reran the probe ladder.  Health probe passed, fixed-path read hung, and a
bounded embedded mini-packet review returned `VERDICT: AGREE`.  A fresh health
probe later returned `CLEAN_XLA_CURRENT_PROBE_OK`, confirming Claude is
responsive and fixed-path review hangs should be handled by prompt repair.

Blocker artifact:

- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-launch-review-blocker-2026-07-02.md`

Phase 0 inventory passed and wrote:

- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase0-inventory-target-freeze-result-2026-07-02.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-guardrails-subplan-2026-07-02.md`

Implementation edits and GPU/XLA tests have now been made and recorded in the
phase artifacts below.  No HMC-readiness, exact nonlinear likelihood
correctness, all-model validation, or broad scientific correctness claim is
made.

Phase 1 added a static audit and tests only.  The audit correctly reports the
current route as `FAIL_CURRENT_ROUTE`; this is guardrail evidence, not a clean
XLA pass.

Phase 2 fixed randomness tensorization passed.  The manual score route no
longer contains the Python seed loop or `tf.random.stateless_normal`; the audit
still correctly reports `FAIL_CURRENT_ROUTE` because RK4, manual time-scan, and
Sinkhorn findings remain.

Phase 3 RK4 loop hygiene passed.  RK4 forward aux capture and reverse VJP now
use TensorFlow loop state, with independent RK4 primal/aux/tape-VJP parity.
The audit still correctly reports `FAIL_CURRENT_ROUTE` because manual time-scan
and Sinkhorn findings remain.

Phase 4 manual scan hygiene passed.  The live manual route now uses
`tf.while_loop` and `TensorArray` for forward/reverse time recursion, with zero
focused parity difference against the pre-edit fixture and the retained
Python-record reference.

Phase 5 streaming Sinkhorn loop hygiene passed.  The targeted stopped-key
potential value helper, total-route potential value helper, and stopped-key VJP
helper now use TensorFlow loop state for Sinkhorn step iteration and VJP state
storage.  Focused Phase 5 parity against the pre-edit fixture had overall max
absolute difference `0.0`.

The static audit still reports `FAIL_CURRENT_ROUTE` because
`SINK-STOPPED-VALUE-KEY` and `SINK-STOPPED-VJP-KEY` remain true.  Those
stopped-key helpers are partial-derivative helpers.  It is wrong to call their
outputs scores unless missing total terms are included elsewhere and verified.

Phase 6 proved on the tiny trusted GPU/XLA fixture that the compiled route uses
`transport_ad_mode="full"` and routes through
`_filterflow_manual_streaming_finite_transport_total_vjp`, not the stabilized
stopped-key route.  Outputs were finite, on GPU, XLA compiled, one concrete
function was reused, and HLO while markers were present.

Phase 7 then ran same-scalar numerical validation on the same tiny fixture.
GPU placement, finiteness, route manifest, repeat determinism, and HLO
watchpoint passed.  The preregistered FD sentinel failed narrowly only for
`log_obs_noise_scale`: closest absolute error `0.10050010681152344` versus
predeclared tolerance `0.09968621826171875`.

Owner acceptance:

- The owner approved accepting and promoting this result as closed enough and
  not worth extra repair effort.
- Machine-readable artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase7-numerical-validation-2026-07-02.json`
  now records `promoted_by_owner_acceptance=true`,
  `primary_pass=false`, and an explicit owner-acceptance waiver block.
- Result artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase7-numerical-validation-result-2026-07-02.md`
  records `OWNER_ACCEPTED_WITH_FD_WAIVER`.

Next action:

- Treat the bounded clean-XLA fixture as promoted with the FD-waiver caveat.
- Do not claim that the original FD gate passed.
- Do not claim HMC readiness, exact nonlinear likelihood correctness, all-model
  validation, or that stopped-key partial derivatives are scores.
