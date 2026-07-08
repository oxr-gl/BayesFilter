# Phase R9 Execution Subplan: Full Phase 3 Material Statistical Gate

Date: 2026-06-29

Status: `REVIEWED_EXECUTING_STAGE_B`

## Phase Objective

Generalize the R8 tiny material manual route to the reviewed Phase 3 LGSSM
scope and decide whether the full Phase 3 material blocker can be responsibly
removed.

R9 must not replace
`PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION` unless the
actual Phase 3 material entrypoint uses the no-autodiff manual score route,
passes same-scalar finite-difference checks, and emits evidence against the
exact Kalman LGSSM comparator under a reviewed run manifest.

## Entry Conditions Inherited From R8

- The real Phase 3 material entrypoint executes the tiny fixed-ridge manual
  route.
- Tiny material same-scalar FD passed for all three LGSSM parameters.
- Material route audits show no outer `tf.GradientTape` or generic autodiff in
  the material score path.
- The full material gate remains blocked with:
  `PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION`.

## Required Artifacts

- This executable R9 subplan reviewed with Claude before implementation.
- A generalized fixed-ridge material manual route in
  `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py` that
  supports `state_dim in {1,2}`, `time_steps=10`, `seed_count=10`, and the
  reviewed particle count without using the outer taped wrapper.
- A staged material run:
  - Stage A: `D=1,T=10,N=16,seed_count=3`, CPU-hidden, FP64, no XLA, same-route
    material entrypoint, central FD parity on all three parameters.
  - Stage B: `D=1,2,T=10,N=64,seed_count=10`, CPU-hidden FP64, no XLA, same
    manual material entrypoint, central FD parity on all three parameters, and
    exact Kalman value/gradient comparison.
- A static audit proving material mode dispatches through the manual route and
  that the taped wrapper is not reachable for material mode.
- Separate Stage A and Stage B run manifests, static no-autodiff audit evidence,
  and a result note with an explicit retain/remove blocker rationale tied to
  the criteria below.
- Each run manifest must record: git commit or `dirty-worktree` status, exact
  command, conda/python environment if known, CPU/GPU visibility and TensorFlow
  logical devices, TensorFlow version, TF32 status, XLA status, random seed
  schedule, `state_dims`, `time_steps`, `num_particles`, `seed_count`,
  `settings`, ridge policy, reset factorization, score route, route label, FD
  steps, output artifact path, wall time, gate status, and nonclaims.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before implementation.
- Bounded Claude read-only plan review before edits.
- Focused local checks:

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
git diff --check -- \
  docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r9-full-material-statistical-gate-execution-subplan-2026-06-29.md \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  tests/test_contract_e_phase3_material_manual_route.py \
  tests/test_contract_e_phase3_gradient_route_audit.py
```

- Stage A material command after implementation:

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  --device-scope cpu \
  --num-particles 16 \
  --seed-count 3 \
  --time-steps 10 \
  --state-dims 1 \
  --settings 0.55:2 \
  --contract-e-reset-factorization cholesky-ridge \
  --chol-ridge-abs 0.75 \
  --chol-ridge-rel 0 \
  --chol-ridge-max-attempts 1 \
  --gate-mode material \
  --fd-steps 1e-5,1e-5,1e-5 \
  --no-xla \
  --output /tmp/contract_e_phase3_r9_stage_a_material.json
```

- Stage B command is specified here for review, but must not be executed until
  Stage A passes and the result note justifies the selected device/particle
  count.

Stage B command, if Stage A passes:

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  --device-scope cpu \
  --num-particles 64 \
  --seed-count 10 \
  --time-steps 10 \
  --state-dims 1 2 \
  --settings 0.55:2 \
  --contract-e-reset-factorization cholesky-ridge \
  --chol-ridge-abs 0.75 \
  --chol-ridge-rel 0 \
  --chol-ridge-max-attempts 1 \
  --gate-mode material \
  --fd-steps 1e-5,1e-5,1e-5 \
  --no-xla \
  --output /tmp/contract_e_phase3_r9_stage_b_material.json
```

Stage B artifact acceptance must include:

- `gate.status=passed`;
- `score_route=manual_likelihood_reverse_scan_no_autodiff`;
- no outer tape diagnostic in material mode;
- `same_scalar_fd.status=pass` for each state dimension and parameter;
- finite value and score means;
- for each state dimension, mean value within `2 * MCSE` of exact Kalman if
  MCSE is positive;
- for each parameter and state dimension, mean score within `2 * MCSE` of exact
  Kalman if MCSE is positive;
- reset covariance residual no larger than `5.0e-4`; and
- no ridge failures.
- Bounded Claude read-only implementation/result review before blocker removal.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the full Phase 3 LGSSM material gate run through the no-autodiff fixed-ridge Contract E manual route? |
| Baseline/comparator | Same-scalar FD on the actual material scalar; exact FP64 Kalman LGSSM value/gradient after route parity passes. |
| Primary pass criterion | Stage A passes same-scalar FD and no-autodiff route audits; Stage B passes the concrete artifact acceptance checks listed above before CPU FP64 blocker removal. |
| Veto diagnostics | Outer taped material route, generic autodiff API in material score, branchy reset fallback, scalar mismatch, failed FD parity, nonfinite values/scores, branch replay failure, exact Kalman failure, wrong device/precision claim, or missing run manifest. |
| Explanatory diagnostics | Per-time increments, transport residuals, reset residuals, ridge diagnostics, MCSE/SD, Kalman deltas, FD slopes and residuals. |
| Not concluded | SIR/SV correctness, HMC readiness, production readiness, GPU/XLA/TF32 readiness, or broad scientific validity. |
| Artifact preserving result | R9 result note plus JSON/markdown output artifacts from material commands. |

## Forbidden Claims And Actions

- Do not remove the full material blocker after Stage A alone.
- Do not compare manual scores to FD from a different scalar or ridge policy.
- Do not use exact Kalman agreement as a substitute for same-scalar FD route
  validation.
- Do not claim GPU/XLA/TF32 readiness from CPU-hidden runs.
- If Stage B passes on CPU-hidden FP64 only, remove at most the CPU FP64
  full-material route blocker.  GPU/XLA/TF32 material readiness must remain a
  later reviewed device gate.
- Do not revert to outer `tf.GradientTape` to make the full material route
  pass.

## Skeptical Plan Audit

- Wrong-scope risk: R8's tiny route could pass while generalized `T=10` state
  retention is incomplete.  Mitigation: Stage A exercises `T=10` before Stage B.
- Wrong-scalar risk: fixed-ridge manual score could be compared to branchy reset
  FD.  Mitigation: all material stages freeze `chol_ridge_rel=0`,
  `chol_ridge_abs=0.75`, `chol_ridge_max_attempts=1`, and audit branchy reset
  absence in the material score route.
- Proxy-promotion risk: Stage A is a route-scaling gate only.  Mitigation: full
  blocker removal requires Stage B.
- Environment risk: CPU-hidden evidence cannot support GPU/XLA claims.
  Mitigation: a CPU FP64 Stage B pass may unblock only CPU FP64 material
  evidence; trusted GPU/XLA/TF32 remains a later gate.
- Artifact adequacy: commands and tests preserve route labels, same-scalar FD,
  blocker status, and device/precision manifest evidence.

This plan passes the skeptical audit after Claude review because it separates
route scaling, statistical validation, and production/device claims.

## Exact Next-Phase Handoff Conditions

Remove or replace the full material blocker only if:

- Stage A passes;
- Stage B is reviewed, executed, and passes;
- material mode audits prove no outer `tf.GradientTape`;
- same-scalar FD and exact Kalman checks both pass;
- Claude implementation/result review converges; and
- R9 result explicitly records whether the blocker is removed only for CPU FP64
  material evidence or retained entirely.

If Stage A passes but Stage B is not run, hand off to R10 with the full blocker
still active.  If Stage A fails, write a blocker result with the smallest
discriminating repair.

## Stop Conditions

Stop and write an R9 blocker result if:

- generalized material route cannot replay required state without changing the
  scalar;
- Stage A same-scalar FD fails after one focused repair attempt;
- material score requires outer `tf.GradientTape` or generic autodiff;
- branchy reset cannot be separated from the fixed-ridge material score; or
- Claude review does not converge after five rounds for the same blocker.
