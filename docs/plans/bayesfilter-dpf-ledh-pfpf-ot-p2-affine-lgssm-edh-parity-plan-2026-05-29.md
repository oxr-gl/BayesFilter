# P2 Plan: Affine LGSSM EDH Parity

Date: 2026-05-29

## Decision

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: does the finite-step LEDH affine map reduce to the linear-Gaussian
local posterior map for the LGSSM fixture?

Baseline/comparator: TF/TFP Kalman/LGSSM equations and local one-step Gaussian
conditioning.

Pass criterion: result artifact records a deterministic parity gate comparing
EDH map mean/covariance/log-det against local Gaussian conditioning formulas.

Veto diagnostics: non-finite covariance, Cholesky failure, residual above fixed
tolerance, or unrecorded log-det convention.

Not concluded: full filtering correctness, nonlinear correctness, or production
readiness.

## Inputs

- `experiments/dpf_implementation/tf_tfp/fixtures/lgssm_tf.py`
- `experiments/dpf_implementation/tf_tfp/references/kalman_lgssm_tf.py`
- P1 math contract result.

## Outputs

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p2-affine-lgssm-edh-parity-result-2026-05-29.md`

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-*-2026-05-29.md`
- `experiments/dpf_implementation/tf_tfp/flows/`

## Forbidden Write Set

Production code, vendored code, monograph chapters, high-dimensional lane
artifacts, and existing comparator code unless needed by a later reviewed phase.

## Skeptical Audit Checklist

Check stale context, wrong default architecture, bootstrap-proposal overclaim,
OT-resampling overclaim, missing stop conditions, hidden production drift,
monograph drift, vendored-code contamination, high-dimensional-lane
contamination, and artifact fitness.

## Stop Conditions

Stop if LGSSM linearization is not exactly `C`, if local posterior formulas are
ambiguous, or if parity requires changing fixture/reference semantics.

## Verification Commands

- targeted parity command from P5/P6 once implementation exists;
- `rg -n "affine|parity|log_det|Kalman" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p2-*-2026-05-29.md`

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to max five
iterations with Codex audit.

## What Must Not Be Concluded

No nonlinear, HMC, posterior, production, NAWM-scale, or monograph claim.
