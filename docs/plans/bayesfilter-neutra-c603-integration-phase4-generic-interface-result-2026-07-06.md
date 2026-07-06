# BayesFilter NeuTra c603 Integration Phase 4 Result

Date: 2026-07-06

## Status

`DRAFT`

## Purpose

This note records the generic interface boundary suggested by the c603 import
and mechanics work. It is a design artifact, not a claim that BayesFilter now
supports every nonlinear SSM.

## Interface Boundary Suggested by the Evidence

The c603 work supports a layered separation:

1. `SSMTargetContract` and `FilterProgram` describe the target and filter
   identity.
2. `FrozenTransportBinding` names a frozen transport and binds it to a target
   signature.
3. `load_frozen_neutra_artifact` and
   `finalize_dense_iaf_neutra_artifact_payload` remain the acceptance gates for
   NeuTra payload materialization.
4. `GenericSSMPosteriorAdapter` is the right place for batch-native posterior
   composition over an explicit target contract.
5. `FixedTransportValueScoreAdapter` and
   `bind_fixed_transport_hmc_mechanics` are the right place for mechanics-only
   transport binding without promoting HMC claims.

## What c603 Does Support

- a reviewed frozen-transport import path;
- explicit target-signature binding;
- explicit separation of transport payload, filter authority, and mechanics
  checks;
- CPU-only local verification of the bridge.

## What c603 Does Not Support

- arbitrary nonlinear SSM support;
- universal HMC readiness;
- posterior convergence;
- production default changes;
- claims about unreviewed filters or targets.

## Recommended Interface Pattern

For future work, BayesFilter should keep three contracts distinct:

- target contract: what model, chart, prior, and filter program are being
  described;
- transport contract: what frozen transport is being loaded and to which target
  signature it binds;
- mechanics contract: what fixed-transport value/score binding is being
  exercised under CPU-only or trusted GPU conditions.

That separation matches the code already in the repo and keeps the evidence
gates local to the operation they are meant to justify.

## Nonclaims

- not a full API redesign;
- not a training or HMC result;
- not a production promotion;
- not a claim that c603 covers all nonlinear SSM cases.

## Next Action

Treat this as the close record for the c603 integration program. Any further
interface extension should begin as a separate program with its own evidence
contract and review gates.
