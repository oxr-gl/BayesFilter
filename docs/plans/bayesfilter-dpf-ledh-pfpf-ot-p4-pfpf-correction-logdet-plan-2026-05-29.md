# P4 Plan: PF-PF Correction And Log-Det

Date: 2026-05-29

## Decision

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: can the implementation form proposal-corrected PF-PF weights for the
LEDH map with explicit pre-flow density, target density, and forward log-det?

Baseline/comparator: DPF3 PF-PF object contract.

Pass criterion: result artifact records
`log p(y|x1) + log p(x1|ancestor) - log q0(x0|ancestor) + log|det DPhi(x0)|`
with finite diagnostics and sign convention.

Veto diagnostics: missing `q0`, missing target transition density, missing
forward log-det, singular map, non-finite corrected weights, or wrong sign.

Not concluded: exact nonlinear filtering, posterior correctness, HMC readiness,
production readiness.

## Inputs

- DPF3 PF-PF spec.
- P1-P3 result artifacts.

## Outputs

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p4-pfpf-correction-logdet-result-2026-05-29.md`

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-*-2026-05-29.md`
- `experiments/dpf_implementation/tf_tfp/flows/`
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`

## Forbidden Write Set

Production code, vendored code, monograph chapters, high-dimensional lane
artifacts, and NumPy algorithm implementations.

## Skeptical Audit Checklist

Check stale context, wrong default architecture, bootstrap-proposal overclaim,
OT-resampling overclaim, missing stop conditions, hidden production drift,
monograph drift, vendored-code contamination, high-dimensional-lane
contamination, and artifact fitness.

## Stop Conditions

Stop if proposal and target densities cannot be evaluated in TF/TFP, if the
flow map is not invertible on the fixture, or if corrected weights are not
finite.

## Verification Commands

- targeted runner diagnostics once implementation exists;
- `rg -n "corrected log weight|log\\|det|q0|target" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p4-*-2026-05-29.md`

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to max five
iterations with Codex audit.

## What Must Not Be Concluded

No production, HMC, posterior, NAWM-scale, monograph, or exact nonlinear
filtering claim.
