# Phase 10 Subplan: Bounded GPU NeuTra Training

Date: 2026-07-07

## Phase Objective

Run the first bounded GPU NeuTra optimizer-training gate for one admitted
BayesFilter-owned route, using the Phase 9 GPU preflight harness as the entry
point and preserving strict no-HMC/no-sample-generation boundaries.

This phase may train a small affine-diagonal transport for a selected route and
write a training-state artifact.  It must not claim posterior convergence, HMC
readiness, XLA readiness, default execution readiness, route superiority,
production readiness, or scientific validity.

Because Phase 9 recorded an XLA/JIT blocker, Phase 10 has two admissible paths:

- repair XLA/JIT first under a separate reviewed XLA-repair subplan; or
- run a non-XLA bounded GPU optimizer-training preflight with `jit_compile=false`.

Unless the XLA repair path is explicitly reviewed and passes, Phase 10 must use
the second path and label the result as non-XLA bounded GPU preflight evidence
only.

## Entry Conditions Inherited From Previous Phase

- Phase 9 passed GPU objective/gradient preflight for:
  - `lgssm-static-qr-exact-kalman`;
  - `model-b-svd-ukf-deterministic-loglikelihood`;
  - `model-b-svd-cubature-deterministic-loglikelihood`.
- Trusted GPU evidence exists for TensorFlow `2.19.1` on `/device:GPU:0`.
- CPU training fallback is forbidden for NeuTra training.
- External sample generation remains a separate multicore CPU phase.
- HMC sampling/tuning has not been authorized for Phase 10.
- XLA/JIT is blocked by a TensorFlow fixed-tensor-list-size compile failure and
  must remain outside the Phase 10 primary criterion unless a dedicated
  XLA-repair subplan is reviewed.
- If Phase 10 proceeds before XLA repair, passing Phase 10 cannot support XLA
  readiness, HMC readiness, production readiness, or default execution
  readiness.

## Required Artifacts

- Phase 10 result or blocker:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase10-bounded-gpu-training-result-2026-07-07.md`
- GPU training-state JSON under:
  `docs/plans/artifacts/lgssm-first-neutra-gpu-training-2026-07-07/`
- Optional frozen affine transport payload only if the training-state gate
  passes finite checks and payload loading checks are explicitly included.
- Updated or new test coverage for:
  - CPU-hidden policy checks;
  - artifact schema checks;
  - no-HMC/no-sample-generation flags;
  - finite loss-history checks.

## Required Checks/Tests/Reviews

- Before GPU work, rerun trusted:
  - `nvidia-smi`;
  - TensorFlow GPU visibility probe.
- CPU-safe tests must set `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.
- GPU training command must run under trusted/escalated execution.
- Training command must record:
  - route id;
  - target and adapter signatures;
  - seed;
  - batch size;
  - optimizer;
  - learning rate;
  - step count;
  - GPU device evidence;
  - requested TensorFlow device;
  - physical and logical GPU names;
  - `CUDA_VISIBLE_DEVICES`;
  - `TF_FORCE_GPU_ALLOW_GROWTH`;
  - TensorFlow version;
  - TF32 execution setting;
  - `jit_compile` setting;
  - XLA blocker status;
  - soft-device-placement setting;
  - managed/trusted execution basis;
  - finite loss history;
  - no-HMC and no-sample-generation flags.
- Run `git diff --check` on Phase 10 code and artifacts.
- Bounded read-only review must inspect the Phase 10 result/blocker and Phase
  11 subplan before crossing into HMC or sample-generation work.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter run a bounded GPU NeuTra optimizer-training gate for one admitted non-DSGE route without CPU fallback, HMC, or sample generation? |
| Baseline/comparator | Phase 9 GPU objective/gradient preflight; Phase 6 CPU affine fixture only as a historical schema/mechanics reference, not as execution policy. |
| Primary criterion | Selected route completes the predeclared bounded optimizer steps on GPU with the reviewed XLA policy, emits finite loss history and gradients, and writes a training-state artifact with no CPU fallback. |
| Veto diagnostics | Missing trusted GPU, CPU fallback, nonfinite loss/gradient, optimizer state missing, artifact schema failure, route not admitted by prior phases, hidden HMC, hidden external sample generation, unrecorded TF32/JIT/device provenance, or use of XLA as an unreviewed requirement. |
| Explanatory diagnostics | Initial/final loss, loss curve, gradient norms, runtime, GPU device placement, and route signatures. |
| Not concluded | Transport quality, HMC readiness, posterior correctness, route superiority, dense IAF readiness, production readiness, or scientific validity. |
| Artifact | Phase 10 result/blocker, training-state JSON, focused tests, and Phase 11 subplan. |

## Forbidden Claims/Actions

- Do not run CPU NeuTra training.
- Do not set `CUDA_VISIBLE_DEVICES=-1` for training.
- Do not use CPU fallback if GPU placement fails.
- Do not run HMC sampling, HMC tuning, or sample generation.
- Do not use DSGE/c603.
- Do not train or promote deferred routes.
- Do not require XLA/JIT unless a separate XLA repair subplan is reviewed.
- If proceeding before XLA repair, do not set `jit_compile=true`.
- Do not omit TF32, XLA/JIT, device, or trusted-execution provenance from the
  training artifact.
- Do not claim training loss improvement proves posterior correctness or HMC
  readiness.
- Do not claim default execution readiness from a non-XLA Phase 10 pass.
- Do not rank routes from one bounded training run.

## Exact Next-Phase Handoff Conditions

Phase 11 may begin only if:

- Phase 10 records pass/blocker with a result artifact;
- the training-state JSON is schema-checked and below repository size policy;
- all objective/gradient/loss diagnostics are finite or the blocker explains
  the failure;
- GPU placement evidence is recorded under trusted execution;
- no CPU training fallback, HMC, or sample generation occurred;
- TF32, XLA/JIT, device, and trusted-execution provenance are recorded;
- if `jit_compile=false`, the Phase 11 subplan preserves that no XLA,
  HMC-readiness, production-readiness, or default-execution-readiness claim is
  supported by Phase 10;
- a Phase 11 subplan states whether the next step is frozen-payload loading,
  XLA repair, dense IAF design, or CPU sample-generation separation;
- bounded read-only review agrees with the Phase 11 boundary.

## Stop Conditions

Stop if:

- trusted GPU visibility cannot be established;
- any training tensor falls back to CPU;
- any loss or gradient diagnostic is nonfinite;
- the selected route is not admitted;
- optimizer state or training-state artifact is malformed;
- HMC or sample generation becomes necessary to proceed;
- XLA/JIT is required before the reviewed XLA repair gate;
- TF32, JIT, device, or trusted-execution provenance cannot be recorded;
- review does not converge after five rounds.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 10 result or blocker;
3. draft or refresh the Phase 11 subplan;
4. review the Phase 11 subplan for consistency, correctness, feasibility,
   artifact coverage, GPU/CPU boundary safety, and claim discipline.
