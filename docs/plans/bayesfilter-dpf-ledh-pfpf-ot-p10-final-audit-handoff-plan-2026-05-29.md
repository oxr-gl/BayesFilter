# P10 Plan: Final Audit And Handoff

Date: 2026-05-29

## Decision

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: is the experimental TF/TFP LEDH-PF-PF-OT lane ready for handoff as
the default experimental DPF architecture, with bootstrap OT-DPF demoted to
comparator/component baseline?

Baseline/comparator: all P0-P9 results and prior TF/TFP OT-DPF handoff.

Pass criterion: final audit records phase status, Claude review iterations,
files changed, variant implemented, LGSSM/range-bearing/gradient outcomes,
verification commands, caveats, unresolved risks, and next action.

Veto diagnostics: missing phase result, failed required verification,
unauthorized edits, NumPy implementation import, student/vendored/highdim
contamination, or evidence overclaim.

Not concluded: production/API readiness, HMC readiness, posterior correctness,
NAWM-scale readiness, banking/model-risk claim, monograph claim.

## Inputs

- Master program.
- P0-P9 result artifacts.
- `experiments/dpf_implementation/reports/dpf-ledh-pfpf-ot-tf-tfp-*-2026-05-29.md`
- JSON outputs under `experiments/dpf_implementation/reports/outputs/`.

## Outputs

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p10-final-audit-handoff-result-2026-05-29.md`

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-*-2026-05-29.md`

## Forbidden Write Set

Production code, vendored code, monograph chapters, high-dimensional lane
artifacts, and unrelated dirty files.

## Skeptical Audit Checklist

Check stale context, wrong default architecture, bootstrap-proposal overclaim,
OT-resampling overclaim, missing stop conditions, hidden production drift,
monograph drift, vendored-code contamination, high-dimensional-lane
contamination, and artifact fitness.

## Stop Conditions

Stop or write blocker if any required verification fails in a way that
invalidates the result, if unresolved reviewer objection is major, or if the
default architecture statement would be misleading.

## Verification Commands

- `rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp`
- `rg -n "student|vendored|highdim|ch33|ch34|ch35|ch36|ch37" experiments/dpf_implementation/tf_tfp`
- `python -m py_compile` over touched Python files.
- targeted LGSSM, range-bearing, and gradient runners plus validate-only and reproducibility checks.
- `python -m json.tool` over new JSON outputs.
- lane-scoped trailing whitespace check.
- `git diff --check`
- `git status --short --branch`

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to max five
iterations with Codex audit.

## What Must Not Be Concluded

No production/API readiness, HMC readiness, posterior correctness,
NAWM-scale readiness, banking/model-risk claim, or monograph claim.
