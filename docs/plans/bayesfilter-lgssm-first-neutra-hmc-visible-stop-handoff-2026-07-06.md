# BayesFilter LGSSM-First NeuTra/HMC Visible Stop Handoff

Date: 2026-07-06

## Status

`PHASE11_READY`

## Current Phase

Phase 11 frozen GPU-trained affine payload packaging and loader/mechanics
validation.

## Current Evidence

- User approved the LGSSM-first sequence:
  LGSSM -> simple nonlinear non-DSGE SSM -> multi-filter targets -> DSGE/c603
  stress later.
- Owner directive received on 2026-07-07: future BayesFilter NeuTra training is
  GPU by default/requirement, while external sample generation should use
  multicore CPU parallelism.  The Phase 6 CPU-only affine training artifact is
  a historical bounded smoke/integration fixture, not the future serious
  NeuTra training route.
- c603 import/real-target blocker artifacts remain historical stress-context
  evidence, not the foundation.
- Draft LGSSM-first master program, phase subplans, visible runbook, execution
  ledger, stop handoff, and launch review bundle have been created.
- Phase 0 local checks passed.
- Claude launch review was policy-rejected as external-service data
  exfiltration risk; a fresh Codex read-only substitute review returned
  `VERDICT: AGREE`.
- Phase 1 read-only inventory result, refreshed Phase 2 subplan, and Phase 1
  review bundle have been written.
- Phase 1 local checks passed after one shell quoting defect was discarded and
  rerun safely.
- Phase 1 substitute Codex review returned `VERDICT: AGREE` with the caveat
  that it was artifact-consistency and boundary-safety review, not independent
  source-line verification.
- Phase 2 precheck and skeptical audit have passed.
- Phase 2 added a testing helper and focused tests for a generic LGSSM adapter.
- Phase 2 local checks passed:
  - 8 focused LGSSM adapter tests;
  - 23 adjacent generic target-builder and QR compact loglikelihood tests;
  - CPU-only signature probe;
  - `py_compile`;
  - `git diff --check`.
- TensorFlow emitted CUDA initialization warnings during the CPU-only signature
  probe despite `CUDA_VISIBLE_DEVICES=-1`; this is environment noise, not GPU
  evidence.
- Phase 2 substitute Codex review returned `VERDICT: AGREE`.
- Phase 3 precheck and skeptical audit have passed.
- Phase 3 tiny CPU-only HMC mechanics smoke completed with 8 finite samples and
  0 nonfinite samples against the Phase 2 rank-2 generic LGSSM adapter.
- Phase 3 did not run a long or decision-making HMC validation and did not make
  posterior/convergence claims.
- Phase 4 subplan has been refreshed as deterministic target/reference
  validation first; longer or decision-making HMC posterior validation remains
  outside current approval.
- Phase 3 substitute Codex review returned `VERDICT: AGREE`.
- Phase 4 precheck and skeptical audit have passed.
- Phase 4 deterministic target/reference validation passed on a 625-point grid:
  value residual `0.0`, selected finite-difference score residual
  `4.7978010453419984e-11`.
- Phase 5 subplan has been refreshed as fixed identity/affine transport
  mechanics only; no training or DSGE/c603 import.
- Phase 4 substitute Codex review returned `VERDICT: AGREE`.
- Phase 5 precheck and skeptical audit have passed.
- Phase 5 fixed transport mechanics tests passed:
  - 4 focused LGSSM fixed-transport tests;
  - 12 adjacent frozen artifact/fixed-transport binding regression tests.
- Phase 6 subplan has been refreshed as a training approval/request gate; no
  training is authorized or run yet.
- Phase 5 substitute Codex review returned `VERDICT: AGREE`.
- Phase 6 approval request and stop result have been written.
- User approved crossing the Phase 6 training boundary on 2026-07-07 with
  message `I approve`.
- Approval is interpreted as the conservative default: CPU-only tiny learned
  affine transport training, fixed seed/budget, frozen payload load,
  mechanics/reference checks, and no GPU/dense-IAF/long-HMC/default/scientific
  claim crossing.
- Phase 6 execution subplan and review bundle were written.
- Phase 6 execution subplan substitute Codex review returned
  `VERDICT: AGREE`.
- Phase 6 tiny CPU-only learned affine NeuTra-style LGSSM training ran with
  seed `20260707`, 80 steps, batch size 64, and learning rate `0.03`.
- Phase 6 validation passed:
  - target signature
    `290a91d2a8f90d5b29243965b258b1ec6fd965aa46ffca69dcb78f7fa1ecabcb`;
  - frozen artifact signature
    `1dd62839f84dd01d1a27e1d53c13a7b1c9e4c50018ea40e00dd9b59a7ac57d65`;
  - transport hash
    `7eb3a38153506667bf8807d35e8469a0674fe5262194fb3183c44dbc55716926`;
  - reference value/score residuals `0.0` and `0.0`;
  - validation JSON `passed: true`.
- Phase 6 execution result was reviewed by a fresh Codex substitute reviewer
  and returned `VERDICT: AGREE`.
- Phase 6 result is
  `PASSED_LEARNED_AFFINE_LGSSM_NEUTRA_MECHANICS_GATE`.
- Phase 7 simple nonlinear non-DSGE SSM target adapter gate passed.
- Phase 8 same-target multi-filter gate passed for deterministic SVD-UKF and
  SVD cubature routes, while CUT4 and principal-square-root UKF remain
  deferred.
- Phase 9 GPU NeuTra objective/gradient preflight passed under trusted GPU
  execution for the LGSSM QR route and the two admitted simple nonlinear
  routes.  The Phase 9 XLA/JIT probe remains blocked by TensorFlow's fixed
  tensor-list-size compile failure.
- Phase 10 bounded GPU affine NeuTra optimizer training passed for
  `lgssm-static-qr-exact-kalman` with seed `20260707`, 12 steps, batch size
  `16`, learning rate `0.03`, TF32 enabled, and `jit_compile=false`.
- Phase 10 artifact:
  `docs/plans/artifacts/lgssm-first-neutra-gpu-training-2026-07-07/lgssm_static_qr_exact_kalman_affine_neutra_gpu_training_state_seed20260707.json`.
- Phase 10 target signature:
  `290a91d2a8f90d5b29243965b258b1ec6fd965aa46ffca69dcb78f7fa1ecabcb`.
- Phase 10 adapter signature:
  `0a48b43d2750cad5b452708f7619a1119a259231d8955769809460f256575a97`.
- Claude bounded read-only review returned `VERDICT: AGREE` for the Phase 10
  result and Phase 11 subplan, after a small Phase 11 adapter-signature
  handoff/veto wording patch.
- No dense IAF training, long HMC, HMC sampling/tuning, external sample
  generation, package installation, detached execution, DSGE/c603 runtime use,
  XLA readiness claim, production/default-readiness claim, or scientific claim
  has been made in this Phase 10 closeout.

## Current Execution Gate

Phase 11 may begin under:

- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase11-frozen-gpu-affine-payload-subplan-2026-07-07.md`

Phase 11 must package the Phase 10 GPU-trained affine parameters into the
existing frozen affine NeuTra artifact schema and run loader/mechanics checks.
It must not run new training, HMC sampling/tuning, external sample generation,
dense IAF training, XLA repair, DSGE/c603, production/default promotion, or
scientific promotion.

## Stop Conditions To Preserve

Stop before unreviewed GPU/CUDA jobs, dense IAF training, additional learned
transport training, HMC sampling/tuning, external sample generation, package
installation, destructive filesystem action, detached execution, default-policy
change, live DSGE/c603 runtime target authority, XLA-readiness claims, or
unsupported scientific/product claims.  Do not run serious NeuTra training on
CPU except for explicitly reviewed tiny smoke/reference exceptions.

## Resume Instructions

If interrupted, resume by reading:

1. `docs/plans/bayesfilter-lgssm-first-neutra-hmc-master-program-2026-07-06.md`
2. `docs/plans/bayesfilter-lgssm-first-neutra-hmc-visible-gated-execution-runbook-2026-07-06.md`
3. `docs/plans/bayesfilter-lgssm-first-neutra-hmc-visible-execution-ledger-2026-07-06.md`
4. the current phase subplan.

Then rerun the latest required local checks before advancing phases.
