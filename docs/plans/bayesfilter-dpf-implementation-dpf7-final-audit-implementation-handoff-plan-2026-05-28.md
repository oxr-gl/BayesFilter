# Plan DPF7: Final Audit And Implementation Handoff

## Date

2026-05-28

## Lane Boundaries And Ordering

- DPF0-A must precede DPF0, and every later phase must preserve that ordering
  evidence.
- No implementation or production handoff is allowed if any earlier phase used
  forbidden lanes, vendored student code, or student work as authority.
- Do not edit production `bayesfilter/` code in this phase.
- Do not edit vendored student files and do not execute student code.
- Do not read or edit the high-dimensional nonlinear filtering lane.

## Evidence Contract

Question: Is the DPF implementation planning lane ready to hand off to
implementation, production patch planning, or a structured blocker?

Baseline/comparator: DPF0-A through DPF6 results, review logs, verification
commands, and unresolved-risk registers.

Primary criterion: every phase has a reviewed result or structured blocker, and
the next action is unambiguous.

Veto diagnostics: missing review evidence; unresolved core discrepancy; missing
source support; production move without DPF6 acceptance; overclaimed
scientific/HMC/posterior readiness.

Explanatory diagnostics: optional implementation candidates and benchmark
summaries.

What will not be concluded: no scientific validity, production readiness, or HMC
validity beyond explicitly accepted ledgers.

## Exact Inputs

- all phase plans and outputs matching `docs/plans/bayesfilter-dpf-implementation-*.md`;
- Claude review records embedded in:
  - `docs/plans/bayesfilter-dpf-implementation-master-program-2026-05-28.md`;
  - each `docs/plans/bayesfilter-dpf-implementation-dpf*-*-plan-2026-05-28.md`;
  - each phase result file matching `docs/plans/bayesfilter-dpf-implementation-dpf*-result-2026-05-28.md`;
- verification-output summaries embedded in each phase result file matching
  `docs/plans/bayesfilter-dpf-implementation-dpf*-result-2026-05-28.md`;
- unresolved-risk sections embedded in each result, register, or final audit
  file matching `docs/plans/bayesfilter-dpf-implementation-*.md`.

## Outputs

- `docs/plans/bayesfilter-dpf-implementation-final-audit-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-handoff-2026-05-28.md`;
- optional structured blocker register.

## Skeptical Plan Audit Checklist

- Does every phase have a result or blocker?
- Are review iterations recorded?
- Are unresolved objections visible?
- Are implementation, production, and experimental next actions separated?
- Are non-implications preserved?

## Execution Steps

1. Audit phase artifacts and review logs.
2. Audit ledgers and unresolved risks.
3. Decide handoff label.
4. Write final audit and handoff.

## Review Protocol

Claude Code Opus 4.7 max effort, read-only, `ACCEPT`/`REJECT`, max 5 iterations.

## Verification Commands

```bash
rg -n "DPF0-A|DPF0|DPF1|DPF2|DPF3|DPF4|DPF5|DPF6|DPF7|not concluded|unresolved|student work as authority|high-dimensional" docs/plans/bayesfilter-dpf-implementation-*.md
rg -n "Do not read.*high-dimensional|Do not import high-dimensional|Student artifacts are comparison-only|never correctness authority|not authority|vendored student" docs/plans/bayesfilter-dpf-implementation-*.md
git diff --check
git status --short --branch
```

## Stop Conditions

- any phase artifact is missing;
- final status would hide unresolved risks;
- handoff would imply production/HMC readiness without evidence;
- any earlier phase used forbidden lanes, vendored student code, or student
  work as authority.

## What Must Not Be Concluded

DPF7 is a handoff/audit phase.  It does not validate an implementation that has
not been built and tested.

## Review Record

- Claude Code reviewer: `claude-opus-4-7`, `--effort max`.
- Iteration 1: `REJECT`; required tighter verification naming and explicit
  ordering/forbidden-lane handoff block.
- Iteration 2: `REJECT`; required exact review/verification/unresolved-risk
  artifact locations and explicit forbidden-lane verification.
- Iteration 3: `ACCEPT`.
- Codex audit: agreed with rejected findings, patched this plan, and accepted
  the iteration-3 result.
