# BayesFilter LGSSM-First NeuTra/HMC Phase 6 Training Approval Request

Date: 2026-07-06

## Scope

Phase 6 has reached the first learned NeuTra training boundary. Prior phases
established:

- a generic LGSSM target adapter;
- a tiny plain HMC mechanics smoke;
- deterministic LGSSM target/reference validation;
- fixed identity/affine transport mechanics.

Those gates do not authorize training a learned NeuTra transport.

## Current Decision Point

Training approval is required before any command trains a NeuTra transport,
uses GPU for training, writes learned model artifacts, or runs longer
decision-making HMC around a learned transport.

No training command has been run in this LGSSM-first program.

## Approval Needed

To continue Phase 6 with actual LGSSM NeuTra training, please explicitly decide
the following:

| Field | Needed decision |
| --- | --- |
| Training permission | Approve or reject learned LGSSM NeuTra training. |
| Device | CPU-only or GPU/trusted CUDA execution. |
| Budget | Number of training steps, wall-time bound, and retry policy. |
| Seeds | Fixed seed list or approval for Codex to choose a small seed set. |
| Artifact paths | Whether to store learned artifacts under `docs/plans/`, a generated artifact directory, or another path. |
| Promotion gate | Whether Phase 6 should require only frozen-artifact load/mechanics/reference checks, or also a longer HMC validation phase. |

## Proposed Conservative Default If Approved Later

If approval is granted without more detail, the conservative follow-up plan
should be:

- CPU-only first unless GPU is explicitly approved;
- one tiny LGSSM training run with a fixed seed and strict wall-time bound;
- write a separate reviewed execution subplan before training;
- save a frozen transport artifact with target signature
  `290a91d2a8f90d5b29243965b258b1ec6fd965aa46ffca69dcb78f7fa1ecabcb`;
- immediately reload the frozen artifact with `load_frozen_neutra_artifact`;
- rerun fixed-transport mechanics and deterministic target/reference checks;
- make no HMC convergence, sampler superiority, production, or scientific
  claims.

## Forbidden Until Approval

- No NeuTra training.
- No GPU training.
- No learned model artifact generation.
- No longer or decision-making HMC validation.
- No DSGE/c603 transport import.
- No default-policy change.
- No posterior correctness, production-readiness, sampler-superiority, or
  scientific-validity claim.
