# P8 Plan: Final Audit And Handoff

Date: 2026-05-28

## Evidence Contract

Question: after P0-P7, is the experimental OT-DPF lane in a clean handoff state
with caveats, review records, verification, and next action recorded?

Comparator: master-program final acceptance criteria.

Primary criterion: final audit records files changed, phase statuses, Claude
iterations, commands, verification, caveats, unresolved risks, and next action.

Veto diagnostics: missing result artifact, failed required verification,
unresolved major blocker hidden as success, forbidden write, or overclaim.

Explanatory-only diagnostics: runtime and proxy metric summaries.

What will not be concluded: no production/API readiness, HMC readiness,
posterior correctness, learned/neural OT promotion, banking/model-risk use, or
monograph validity.

## Skeptical Plan Audit Checklist

Check stale context, wrong baseline, proxy overclaim, missing stop conditions,
hidden production drift, monograph drift, vendored-code contamination,
high-dimensional-lane contamination, and artifact fitness.

## Inputs

- P0-P7 plans and result artifacts.
- LGSSM, range-bearing, and gradient JSON/report artifacts.
- Git status and verification output.

## Outputs

- `experiments/dpf_implementation/reports/dpf-ot-final-audit-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-implementation-p8-final-audit-and-handoff-result-2026-05-28.md`

## Implementation Scope

Write final audit/handoff only.  No new experiments.

Read-only import-boundary scans over `bayesfilter/` and `tests/` are explicitly
allowed for verification because they do not edit those forbidden write-set
paths and are required to detect accidental student/vendored imports.  This
does not authorize writing under `bayesfilter/` or `tests/`.

## Stop Conditions

Stop if required verification fails in a way that invalidates the result or if
a phase result is missing without a structured blocker.

## Verification Commands

```bash
rg -n "student_dpf_baselines|advanced_particle_filter|2026MLCOE|experiments\\.student|experiments/student|vendor" bayesfilter tests experiments/dpf_implementation
python -m py_compile <touched Python files>
python -m experiments.dpf_implementation.runners.run_lgssm_ot_dpf --validate-only
python -m experiments.dpf_implementation.runners.run_range_bearing_ot_dpf --validate-only
python -m experiments.dpf_implementation.runners.run_gradient_checks --validate-only
git diff --check
git status --short --branch
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or
five iterations as in the master program.  This exact command is intentional
per user requirement; if unavailable, stop rather than substitute.

## What Must Not Be Concluded

P8 handoff may authorize only the next experimental step, not production,
posterior, HMC, banking/model-risk, or monograph claims.

## Review Record

- Iteration 1: `REJECT` as part of bundle review; patched reviewer-gate wording
  and clarified read-only `bayesfilter/` and `tests/` verification scans.
- Iteration 2: `ACCEPT`.
