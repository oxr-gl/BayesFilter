# BayesFilter LGSSM-First NeuTra/HMC Phase 6 Training Execution Subplan

Date: 2026-07-07

## Phase Objective

Train and freeze a tiny CPU-only learned affine-diagonal NeuTra-style transport
for the validated LGSSM target, then reload it through the existing frozen
transport path and rerun mechanics/reference checks.

This phase is a first learned-transport integration gate. It is not dense IAF
training, not GPU training, not long HMC validation, and not a posterior or
production-readiness claim.

## Entry Conditions Inherited From Previous Phase

- Phase 5 fixed identity/affine transport mechanics passed.
- Phase 5 bounded substitute review returned `VERDICT: AGREE`.
- User approved crossing the Phase 6 training boundary on 2026-07-07 with
  message: `I approve`.
- Approval is interpreted according to the recorded conservative default:
  CPU-only first, one tiny bounded LGSSM training run, fixed seed, strict
  wall-time bound, frozen artifact load/mechanics/reference checks, and no HMC
  convergence or sampler-superiority claim.
- GPU training is not approved.
- Dense IAF training is not approved.

## Required Artifacts

- Training helper/test code:
  `bayesfilter/testing/lgssm_neutra_training_tf.py`
- Focused tests:
  `tests/test_lgssm_neutra_training_tf.py`
- Training artifact directory:
  `docs/plans/artifacts/lgssm-neutra-training-2026-07-07/`
- Training state JSON:
  `docs/plans/artifacts/lgssm-neutra-training-2026-07-07/lgssm_affine_neutra_training_state_seed20260707.json`
- Frozen transport payload JSON:
  `docs/plans/artifacts/lgssm-neutra-training-2026-07-07/lgssm_affine_neutra_payload_seed20260707.json`
- Validation JSON:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-validation-2026-07-07.json`
- Bounded training/validation log:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-validation-2026-07-07.log`
- Phase 6 execution result:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-execution-result-2026-07-07.md`
- Refreshed Phase 7 subplan:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase7-simple-nonlinear-ssm-subplan-2026-07-06.md`

## Training Configuration

| Field | Value |
| --- | --- |
| Device | CPU-only via `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import. |
| Transport family | Learned affine-diagonal transport using schema `bayesfilter.neutra.frozen_affine_diag.v1`. |
| Target | Phase 2 generic LGSSM adapter. |
| Target signature | `290a91d2a8f90d5b29243965b258b1ec6fd965aa46ffca69dcb78f7fa1ecabcb` |
| Seed | `20260707` |
| Steps | `80` |
| Batch size | `64` |
| Learning rate | `0.03` |
| Objective | Reverse-KL-style reparameterized loss: minimize `mean(-(log p(T(z)) + log|det dT/dz|))` for standard-normal `z`. |
| Initialization | Shift at Phase 2 LGSSM initial parameters and raw scale `log(0.25)` in both coordinates. |
| Wall-time bound | Must remain a short visible run; stop and write blocker if it becomes slow or unstable. |

## Required Checks/Tests/Reviews

- Local code tests:
  - `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_lgssm_neutra_training_tf.py -q`
  - `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_lgssm_fixed_transport_mechanics_tf.py tests/test_lgssm_generic_target_adapter_tf.py -q`
- Training/validation command must:
  - set `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import;
  - write training state and frozen payload JSON;
  - reload frozen payload with `load_frozen_neutra_artifact`;
  - check target signature equality;
  - check transformed mechanics value/score finite;
  - rerun deterministic LGSSM base target/reference validation or an equivalent
    direct base-adapter/source-fixture residual check;
  - record initial/final training loss as explanatory only.
- Bounded read-only review before executing training.
- Bounded read-only review after Phase 6 result before moving to Phase 7.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter train a tiny CPU-only affine NeuTra-style transport for the validated LGSSM target, freeze it, reload it, and pass mechanics/reference checks? |
| Baseline/comparator | Phase 5 synthetic fixed transports, Phase 4 deterministic LGSSM reference target, and the existing frozen affine-diagonal NeuTra loader. |
| Primary criterion | Frozen learned affine payload is written, loads with the Phase 4 target signature, transformed mechanics are finite, target-reference residual checks pass, and no hidden GPU/long-HMC/training expansion occurs. |
| Veto diagnostics | Nonfinite training loss, missing artifact, target-signature mismatch, artifact load failure, nonfinite mechanics, target/reference residual failure, GPU use, long HMC, dense IAF claim, or training loss promoted to posterior correctness. |
| Explanatory diagnostics | Initial/final training loss, learned shift/raw scale, runtime, payload hash, mechanics value/score, grid/reference diagnostics. |
| Not concluded | Dense IAF quality, HMC convergence, posterior correctness, sampler superiority, generic nonlinear SSM validity, production readiness, default-policy change, or scientific validity. |
| Artifact | Training state, frozen payload, validation JSON/log, Phase 6 execution result. |

## Forbidden Claims/Actions

- Do not use GPU.
- Do not train dense IAF.
- Do not run long or decision-making HMC.
- Do not import DSGE/c603 transports.
- Do not change package dependencies or environment.
- Do not claim learned transport quality beyond this affine mechanics gate.
- Do not claim posterior correctness, HMC convergence, sampler superiority,
  production readiness, default-policy change, or scientific validity.

## Exact Next-Phase Handoff Conditions

Phase 7 may begin only if:

- the Phase 6 learned affine transport artifact is written and reloads;
- target signature matches the Phase 4 LGSSM target;
- transformed mechanics and deterministic reference checks pass;
- Phase 6 result records nonclaims;
- bounded review returns `VERDICT: AGREE`.

If Phase 6 fails, write a blocker result and do not proceed to nonlinear SSM.

## Stop Conditions

Stop if training becomes slow, loss becomes nonfinite, artifact load fails,
target signatures mismatch, mechanics/reference checks fail, GPU is required,
dense IAF is needed, or review does not converge after five rounds.

## Phase Close Duties

At close:

1. run required local checks;
2. run bounded training/validation only if pre-training review agrees;
3. write Phase 6 execution result;
4. draft or refresh Phase 7 subplan;
5. review Phase 6 result and Phase 7 handoff for consistency, correctness,
   feasibility, artifact coverage, and boundary safety.
