# P0 Plan: Scope And Default Architecture

Date: 2026-05-29

## Decision

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: does this lane clearly designate TF/TFP LEDH-PF-PF with finite
Sinkhorn/entropic OT as the default experimental DPF architecture while keeping
bootstrap OT-DPF as comparator only?

Baseline/comparator: existing TF/TFP OT-DPF handoff and DPF3 PF-PF spec.

Pass criterion: result artifact records the default architecture, write
boundaries, NumPy/student/highdim import gates, and caveats.

Veto diagnostics: ambiguous default, NumPy implementation allowance, production
write need, vendored/highdim contamination, or bootstrap OT-DPF promoted as
large-model default.

Not concluded: production readiness, NAWM-scale readiness, HMC readiness,
posterior correctness, monograph validity.

## Inputs

- `AGENTS.md`
- `CLAUDE.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf3-flow-pfpf-spec-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p8-final-audit-handoff-result-2026-05-28.md`

## Outputs

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p0-scope-default-architecture-result-2026-05-29.md`

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-*-2026-05-29.md`

## Forbidden Write Set

Production `bayesfilter/`, `tests/`, vendored code, monograph chapters,
high-dimensional lane artifacts, and existing implementation modules.

## Skeptical Audit Checklist

Check stale context, wrong default architecture, bootstrap-proposal overclaim,
OT-resampling overclaim, missing stop conditions, hidden production drift,
monograph drift, vendored-code contamination, high-dimensional-lane
contamination, and artifact fitness.

## Stop Conditions

Stop if the repo policy does not support TF/TFP default implementation, if
Claude exact-model review is unavailable, or if making the default statement
would require editing forbidden files.

## Verification Commands

- `rg -n "default experimental DPF|LEDH-PF-PF|bootstrap proposal" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-*-2026-05-29.md`
- `git status --short --branch`

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`.  Claude returns
`ACCEPT` or `REJECT`; Codex audits findings; loop to max five iterations.

## What Must Not Be Concluded

Do not conclude production/API readiness, monograph correctness, HMC readiness,
posterior correctness, NAWM-scale readiness, or student agreement.
