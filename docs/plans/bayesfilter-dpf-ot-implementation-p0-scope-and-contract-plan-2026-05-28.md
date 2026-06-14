# P0 Plan: Scope And Evidence Contract

Date: 2026-05-28

## Evidence Contract

Question: can this lane define a bounded, experimental OT-DPF implementation
contract that is narrow enough to execute without production, monograph,
vendored, or high-dimensional-lane drift?

Comparator: accepted DPF implementation handoff and DPF1-DPF5 specs.

Primary criterion: this plan records the allowed write set, exact DPF variant,
model ladder, stop rules, verification commands, and non-implications before
implementation starts.

Veto diagnostics: missing lane boundary, missing stop rules, student/vendored
authority, proxy overclaim, production drift, or missing review command.

What will not be concluded: no implementation, numerical, gradient, production,
posterior, HMC, or monograph validity.

## Skeptical Plan Audit Checklist

- stale context;
- wrong baseline;
- proxy overclaim;
- missing stop conditions;
- hidden production drift;
- monograph drift;
- vendored-code contamination;
- high-dimensional-lane contamination;
- artifact answers the phase question.

## Inputs

- DPF implementation master program and handoff from 2026-05-28.
- DPF1, DPF2, DPF4, and DPF5 specs.
- Existing SV smoke plan/result as style and boundary precedent.

## Outputs

- `docs/plans/bayesfilter-dpf-ot-implementation-p0-scope-and-contract-result-2026-05-28.md`

## Implementation Scope

No code implementation.  P0 only writes the result note.

## Stop Conditions

Stop if the exact Claude reviewer command is unavailable, the allowed write set
is insufficient, or any required artifact would need a forbidden write.

## Verification Commands

```bash
git status --short --branch
rg -n "high-dimensional|student work as authority|production readiness|HMC readiness|posterior correctness" docs/plans/bayesfilter-dpf-ot-implementation-*.md
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`.  Claude reviews
read-only and returns `ACCEPT` or `REJECT`; Codex audits, patches if needed, and
loops up to five iterations.  The exact non-portable reviewer command is
intentional because it is a user requirement; if unavailable, stop rather than
substitute.

## What Must Not Be Concluded

P0 does not validate any code, numerical result, gradient, or production path.

## Review Record

- Iteration 1: `REJECT` as part of bundle review; patched reviewer-gate wording.
- Iteration 2: `ACCEPT`.
