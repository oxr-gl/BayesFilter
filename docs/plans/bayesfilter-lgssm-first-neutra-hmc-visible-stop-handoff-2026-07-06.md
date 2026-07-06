# BayesFilter LGSSM-First NeuTra/HMC Visible Stop Handoff

Date: 2026-07-06

## Status

`PHASE7_READY`

## Current Phase

Phase 7 simple nonlinear non-DSGE SSM target design/execution.

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
- No GPU job, dense IAF training, long HMC, package installation, detached
  execution, or git operation has been run in this LGSSM-first program.

## Current Execution Gate

Phase 7 may begin under:

- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase7-simple-nonlinear-ssm-subplan-2026-07-06.md`

Phase 7 must start with model/filter semantics for a simple BayesFilter-owned
nonlinear non-DSGE SSM, preserve target-signature and finite value/score gates,
and avoid hidden training/long-HMC/DSGE/c603 crossings.  If Phase 7 or a later
phase introduces learned NeuTra training, it must follow the GPU NeuTra policy;
external sample generation should be planned as multicore CPU work.

## Stop Conditions To Preserve

Stop before unreviewed GPU/CUDA jobs, dense IAF training, additional learned
transport training, long HMC sampling, package installation, destructive
filesystem action, git commit/push, detached execution, default-policy change,
live DSGE/c603 runtime target authority, or unsupported scientific/product
claims.  Do not run serious NeuTra training on CPU except for explicitly
reviewed tiny smoke/reference exceptions.

## Resume Instructions

If interrupted, resume by reading:

1. `docs/plans/bayesfilter-lgssm-first-neutra-hmc-master-program-2026-07-06.md`
2. `docs/plans/bayesfilter-lgssm-first-neutra-hmc-visible-gated-execution-runbook-2026-07-06.md`
3. `docs/plans/bayesfilter-lgssm-first-neutra-hmc-visible-execution-ledger-2026-07-06.md`
4. the current phase subplan.

Then rerun the latest required local checks before advancing phases.
