# Plan DPF6: Production Boundary And API Review

## Date

2026-05-28

## Lane Boundaries

- DPF6 is a classification and API-boundary review only.
- DPF6 does not edit production code; any production movement requires a
  separate future patch plan after this phase.
- Do not edit vendored student files and do not execute student code.
- Do not read or edit the high-dimensional nonlinear filtering lane.

## Evidence Contract

Question: Which, if any, DPF components are ready to move from experiments into
production BayesFilter APIs?

Baseline/comparator: DPF1-DPF5 results, production checklist, package layout,
README conventions, and local test layout. If CI/runtime policy files are not
present, DPF6 records that absence rather than inferring a policy.

Primary criterion: a production-boundary decision identifies components as
production-candidate, experimental-only, blocked, or documentation-only with
required evidence.

Veto diagnostics: missing validation harness evidence; public API instability;
student-derived code; dependency/runtime risk; HMC/posterior/default claims
without separate evidence.

Explanatory diagnostics: benchmark rows and component-level checks.

What will not be concluded: no automatic production patch, no default change,
no public API change unless a separate implementation patch plan follows, and no
production `bayesfilter/` edits occur in DPF6 outputs themselves.

## Exact Inputs

- `docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-result-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf0-result-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf1-result-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf2-result-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf3-result-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf4-result-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf5-result-2026-05-28.md`;
- `docs/chapters/ch32_production_checklist.tex`;
- package/API review targets, read-only in this phase:
  - `bayesfilter/`;
  - `tests/`;
  - `README.md`.
- optional policy/config files only if present at execution time, read-only:
  - `.github/workflows/`;
  - `pyproject.toml`;
  - `setup.cfg`;
  - `tox.ini`;
  - `noxfile.py`.

## Outputs

- `docs/plans/bayesfilter-dpf-implementation-dpf6-production-boundary-decision-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf6-result-2026-05-28.md`;
- optional future production patch plan path if justified.

## Skeptical Plan Audit Checklist

- Is every production candidate backed by validation evidence?
- Are experimental-only components clearly labeled?
- Are dependency, dtype, shape, seed, device, and serialization contracts clear?
- Are public API and default-policy changes blocked unless separately planned?
- Are docs and tests sufficient for any future patch?
- Are production files inspected read-only and left untouched?

## Execution Steps

1. Map validated components to possible API surfaces.
2. Classify each component.
3. Record blockers and required evidence for production movement.
4. Write production-boundary result and optional future patch-plan path only;
   do not edit production code.

## Review Protocol

Claude Code Opus 4.7 max effort, read-only, `ACCEPT`/`REJECT`, max 5 iterations.

## Verification Commands

```bash
rg -n "production|experimental-only|blocked|default|API|not concluded" docs/plans/bayesfilter-dpf-implementation-dpf6-*.md
git diff --check
git status --short --branch
```

## Stop Conditions

- validation evidence is insufficient;
- API change is needed before separate patch planning;
- student code influence cannot be ruled out;
- production edits would be required inside DPF6 itself.

## What Must Not Be Concluded

DPF6 does not itself edit production code or create a production release.

## Review Record

- Claude Code reviewer: `claude-opus-4-7`, `--effort max`.
- Iteration 1: `REJECT`; required concrete package/test/API review targets and
  explicit no-production-edit language.
- Iteration 2: `REJECT`; required CI/runtime policy inputs or narrowed claim
  and explicit DPF6 no-edit non-conclusion.
- Iteration 3: `ACCEPT`.
- Codex audit: agreed with rejected findings, patched this plan, and accepted
  the iteration-3 result.
