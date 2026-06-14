# P0 Result: Scope And Default Architecture

Date: 2026-05-29

## Decision

`P0_SCOPE_DEFAULT_ARCHITECTURE_ACCEPTED`

## Skeptical Audit

| Check | Status | Notes |
| --- | --- | --- |
| stale context | pass | Read AGENTS/CLAUDE governance, DPF3 PF-PF spec, and prior TF/TFP OT-DPF handoff. |
| wrong default architecture | pass | LEDH-PF-PF-OT is now the default experimental architecture target. |
| bootstrap-proposal overclaim | pass | Bootstrap OT-DPF is explicitly comparator/component baseline only. |
| OT-resampling overclaim | pass | OT remains finite-budget relaxed resampling component only. |
| missing stop conditions | pass | Master and subplans include density/log-det/gradient/verification stop rules. |
| hidden production drift | pass | Production `bayesfilter/` remains forbidden. |
| monograph drift | pass | No monograph edits are authorized. |
| vendored-code contamination | pass | Student/vendored code remains unused and comparison-only. |
| high-dimensional-lane contamination | pass | Separate high-dimensional lane is out of scope. |
| artifact fitness | pass | Scope result answers the default-architecture correction question. |

## Result

The DPF lane default experimental implementation target is
`tf_tfp_ledh_pfpf_with_finite_sinkhorn_ot_resampling`.  Existing TF/TFP
bootstrap OT-DPF remains a comparator and differentiable-resampling component
baseline, not the default large-model DPF architecture.

## Verification

- Claude plan bundle review iteration 1: `ACCEPT`.
- `git status --short --branch` inspected before edits; unrelated dirty files
  were preserved.

## What Is Not Concluded

No production readiness, public API readiness, HMC readiness, posterior
correctness, NAWM-scale readiness, banking/model-risk claim, monograph claim, or
student agreement is concluded.
