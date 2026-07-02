# Phase R8 Execution Subplan: Phase 3 Material Manual Route Integration

Date: 2026-06-29

Status: `DRAFT_FOR_REVIEW`

## Phase Objective

Move the verified fixed-ridge Contract E manual LGSSM reverse-scan route into
the Phase 3 gradient diagnostic so that `--gate-mode material` can be guarded
by a real no-outer-tape manual score path rather than the current
`tf.GradientTape` diagnostic.

R8 may replace the material blocker only if the material script uses the shared
manual route, same-scalar finite-difference parity passes on a reviewed tiny
fixture, and static audits prove the material score path has no outer tape.

## Entry Conditions Inherited From R7

- R5 one-step Contract E fixed-ridge reset/transport/normalization VJP
  composition passed same-scalar FD.
- R6 two-step time reverse scan passed same-scalar FD.
- R7 tiny LGSSM route passed same-scalar FD for all three LGSSM parameters.
- The Phase 3 diagnostic still blocks material mode with:
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`.

## Required Artifacts

- This executable R8 subplan reviewed with Claude before implementation.
- A Phase 3 script route label/config for the fixed-ridge manual route,
  expected label:
  `score_route=manual_likelihood_reverse_scan_no_autodiff`.
- An explicit fixed-ridge scalar route in
  `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py`.
  The material/manual score path must use the fixed-ridge helper
  `contract_e_cholesky_ridge_reset_fixed_ridge`; branchy ridge escalation may
  remain available only as a diagnostic value route.
- A no-outer-tape manual score path that records and replays all required
  forward state: particles, prior means, transition noises, LEDH flow aux,
  corrected weights, normalized/floored weights, transport charts, transport
  matrices, residual noises, fixed ridge, floor masks, and reset diagnostics.
- A tiny Phase 3 material-route test or diagnostic mode matching R7 scope:
  `state_dim=1`, `time_steps=2`, `num_particles=4`, `seed_count=1`,
  `dtype=float64`, CPU-hidden, deterministic/frozen seeds and noises, central
  FD step `1.0e-5`, `rtol=5.0e-4`, `atol=1.0e-5`.
- A CPU-hidden tiny execution of the real Phase 3 material entrypoint, or a
  pytest that invokes that exact entrypoint with `--gate-mode material` and
  verifies the material/manual route label in the emitted artifact.  Helper
  parity alone is insufficient for blocker replacement.
- Updated static audits that:
  - fail if material mode still routes through outer `tf.GradientTape`;
  - fail if material manual score uses branchy ridge escalation;
  - fail if material manual score contains generic autodiff APIs:
    `tf.GradientTape`, `.gradient(`, `.jacobian(`, `batch_jacobian`,
    `ForwardAccumulator`, `tf.gradients`, or `tf.compat.v1.gradients`;
  - fail if `transport_ad_mode="full"` appears in the material route; and
  - preserve the blocker unless the verified material route is actually wired.
- R8 result / close record.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before implementation.
- Bounded Claude read-only plan review before edits.
- Focused CPU-hidden local checks after implementation:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest \
  tests/test_contract_e_phase3_material_manual_route.py \
  tests/test_contract_e_phase3_r7_lgssm_manual_route.py \
  tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py \
  tests/test_contract_e_phase3_r5_manual_reverse_integration.py \
  tests/test_contract_e_cholesky_ridge_reset.py \
  tests/test_contract_e_phase3_gradient_route_audit.py -q
python -m py_compile \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  docs/benchmarks/contract_e_reset_tf.py \
  tests/test_contract_e_phase3_material_manual_route.py
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  --device-scope cpu \
  --num-particles 4 \
  --seed-count 1 \
  --time-steps 2 \
  --state-dims 1 \
  --settings 0.55:2 \
  --contract-e-reset-factorization cholesky-ridge \
  --chol-ridge-abs 0.75 \
  --chol-ridge-rel 0 \
  --chol-ridge-max-attempts 1 \
  --gate-mode material \
  --fd-steps 1e-5,1e-5,1e-5 \
  --no-xla \
  --output /tmp/contract_e_phase3_r8_tiny_material.json
git diff --check -- \
  docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r8-material-script-manual-route-execution-subplan-2026-06-29.md \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  tests/test_contract_e_phase3_material_manual_route.py \
  tests/test_contract_e_phase3_gradient_route_audit.py
```

- Bounded Claude read-only implementation/result review before declaring Phase
  3 unblocked.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the verified fixed-ridge manual route become the actual Phase 3 material score path? |
| Baseline/comparator | Same-scalar central FD on the material/shared fixed-ridge helper under frozen tiny fixture conditions. |
| Primary pass criterion | The real Phase 3 material entrypoint executes the fixed-ridge manual route on the tiny fixture, material/shared manual score matches same-scalar FD for all three LGSSM parameters within `rtol=5.0e-4`, `atol=1.0e-5`, and material route static audit shows no outer tape. |
| Veto diagnostics | Hidden outer `tf.GradientTape`, disallowed generic autodiff API in material manual score, branchy ridge reset in material score, route label mismatch, stale blocker/audit contradiction, missing replay state, nonfinite values/cotangents, branch replay change, or `transport_ad_mode="full"`. |
| Explanatory diagnostics | Per-time increments, row/column transport residuals, reset covariance/mean residuals, ridge diagnostics, cotangent norms, Kalman deltas. |
| Not concluded | Full Phase 3 statistical pass at `T=10,N>=64`, exact Kalman agreement, SIR/SV correctness, HMC readiness, production readiness, GPU/XLA/TF32 readiness, or broad scientific validity. |
| Artifact preserving result | R8 result note plus focused pytest/static-audit output. |

## Forbidden Claims And Actions

- Do not unblock Phase 3 from R8 plan convergence alone.
- Do not replace the blocker unless the actual Phase 3 material entrypoint
  executes the fixed-ridge manual route, emits the expected route label, passes
  same-scalar FD on the tiny fixture, and passes no-outer-tape/generic-autodiff
  audits.  If any of those checks do not pass, preserve or replace with a
  documented blocker.
- Do not compare a fixed-ridge manual score to a branchy-ridge FD scalar.
- Do not claim exact Kalman agreement, nonlinear correctness, or production
  readiness from the tiny material-route gate.
- Do not run GPU/XLA/material full-size jobs unless a later reviewed plan
  authorizes them.

## Skeptical Plan Audit

- Wrong-scalar risk: the current Phase 3 script uses branchy
  `contract_e_cholesky_ridge_reset` for the cholesky-ridge value path, while
  R4-R7 certify only the fixed-ridge smooth chart VJP.  Mitigation: R8 must add
  a distinct fixed-ridge material/manual score route and audit that FD and
  manual evaluations share it.
- Proxy-promotion risk: tiny FD parity can prove route wiring but not full
  Phase 3 statistical validity.  Mitigation: R8 may unblock the material route
  only as a route gate; the full `T=10,N>=64` Phase 3 evidence remains a later
  run.
- Hidden-autodiff risk: `_make_compiled_value_and_gradient` currently wraps the
  scalar in `tf.GradientTape`.  Mitigation: R8 must add/route through a manual
  value-and-score helper, audit the material score route for exact disallowed
  generic autodiff APIs, and execute the real CLI material entrypoint on a tiny
  fixture so helper-level parity cannot mask wiring failure.
- Environment risk: R8 checks are CPU-hidden and tiny.  No GPU/XLA/TF32
  inference is allowed.
- Artifact adequacy: if implemented as planned, the new test and audit directly
  prove the material route transition from taped diagnostic to manual score
  route on the smallest reviewed fixture.

The plan is executable after Claude review because it states the exact scalar
route, fixture, tolerances, commands, blocker rule, and stop conditions.

## Exact Next-Phase Handoff Conditions

Advance beyond R8 only if:

- Claude plan review converges;
- the material/shared manual score helper is implemented;
- same-scalar FD parity passes for all three tiny LGSSM parameters;
- the real Phase 3 material entrypoint executes on the tiny fixture and emits
  the expected manual route label;
- static route audit proves material mode has no outer `tf.GradientTape`;
- focused local checks pass;
- Claude implementation/result review converges; and
- R8 result explicitly states whether Phase 3 is route-unblocked or still
  blocked.

If route-unblocked, the next phase must run the reviewed full Phase 3 material
statistical gate separately.  If not route-unblocked, the next phase must
document the remaining blocker and smallest discriminating repair.

## Stop Conditions

Stop and write an R8 blocker result if:

- the material script cannot share the fixed-ridge scalar without changing the
  route;
- material score requires outer `tf.GradientTape` or generic autodiff to pass;
- branchy ridge escalation cannot be separated from the fixed-ridge manual
  route;
- same-scalar FD parity fails after one focused repair attempt;
- required replay state cannot be captured without scalar drift; or
- Claude review does not converge after five rounds for the same blocker.
