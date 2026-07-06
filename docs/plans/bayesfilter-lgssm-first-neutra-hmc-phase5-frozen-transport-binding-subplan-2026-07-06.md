# BayesFilter LGSSM-First NeuTra/HMC Phase 5 Subplan

Date: 2026-07-06

## Phase Objective

Add identity/affine fixed-transport binding mechanics for the validated LGSSM
target while preserving target signatures and chain-rule evidence. This phase
does not train NeuTra and does not import DSGE/c603 transports.

## Entry Conditions Inherited From Previous Phase

- Phase 4 LGSSM reference validation passed.
- Target signature and adapter manifest are stable.
- Phase 4 review passed or a fixable blocker was visibly repaired.
- No training, GPU, long HMC, or transport import approval has been granted.

## Required Artifacts

- Focused identity/affine transport mechanics tests or smoke artifact.
- Phase 5 result:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase5-frozen-transport-binding-result-2026-07-06.md`
- Phase 5 review bundle.
- Refreshed Phase 6 subplan.

## Required Checks/Tests/Reviews

- Identity transport equals base target.
- Affine fixed transport chain-rule checks against finite differences and/or
  direct base-adapter chain rule.
- Target-signature mismatch rejection.
- CPU-only execution with `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import if
  TensorFlow is imported.
- Review before any training.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can fixed transports bind to the validated LGSSM target without changing target identity or hiding chain-rule errors? |
| Baseline/comparator | Phase 4 LGSSM target and existing fixed-transport mechanics helpers. |
| Primary criterion | Transported value/score matches base chain rule on probes and rejects mismatched signatures. |
| Veto diagnostics | Signature mismatch accepted, nonfinite transformed values/scores, fallback authority promoted, HMC/training hidden, GPU use, or DSGE/c603 transport import. |
| Explanatory diagnostics | Transport hash, manifest hash, probe residuals. |
| Not concluded | Learned NeuTra quality, HMC convergence, posterior correctness, production readiness. |
| Artifact | Phase 5 result and tests/logs. |

## Forbidden Claims/Actions

- Do not train NeuTra.
- Do not claim HMC readiness from mechanics.
- Do not use GPU without approval.
- Do not import c603 or other DSGE transport payloads.
- Do not run HMC sampling except a single mechanics value/score call through
  existing mechanics helpers if explicitly needed by the checked path.

## Exact Next-Phase Handoff Conditions

Phase 6 may begin only if fixed-transport binding passes and training approval
is obtained or explicitly requested. Without training approval, Phase 6 must be
refreshed as a training-approval/request plan or a stop handoff.

## Stop Conditions

Stop if chain-rule checks fail, signatures mismatch, or training/GPU approval
is required but absent.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 5 result;
3. draft or refresh Phase 6 subplan;
4. review Phase 6 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
