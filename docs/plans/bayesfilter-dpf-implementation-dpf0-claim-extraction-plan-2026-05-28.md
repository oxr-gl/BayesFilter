# Plan DPF0: Monograph And Literature Claim Extraction

## Date

2026-05-28

## Lane Boundaries And Prerequisite

- DPF0 may start only after DPF0-A records a nonblocking handoff.
- Student documents and reports may inform discrepancy context only; they are
  not authority for implementation obligations.
- Do not read or edit the high-dimensional nonlinear filtering lane.
- Do not edit vendored student files or execute student code.
- Do not edit production `bayesfilter/` code.

## Evidence Contract

Question: What implementation obligations follow from the DPF monograph and
cited literature after DPF0-A discrepancy adjudication?

Baseline/comparator: DPF monograph claims, DPF0-A ledger, `docs/references.bib`,
`docs/source_map.yml`, and local source summaries when available.

Primary criterion: every implementation obligation has claim status, assumptions,
source/proof support, required tests, and non-implications.

Veto diagnostics: unresolved DPF0-A blocker; unsupported theorem-like claim;
student claim used as authority; HMC/posterior validity smuggled into
implementation obligations.

Explanatory diagnostics: related student implementation ideas and existing
controlled-baseline metrics.

What will not be concluded: no code readiness, API readiness, production
readiness, HMC readiness, or performance ranking.

## Exact Inputs

- `docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-ledger-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-result-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf0a-doc-patch-register-2026-05-28.md`;
- `docs/chapters/ch19_particle_filters.tex`;
- `docs/chapters/ch19b_dpf_literature_survey.tex`;
- `docs/chapters/ch19c_dpf_implementation_literature.tex`;
- `docs/chapters/ch19d_dpf_hmc_dsge_macrofinance_assessment.tex`;
- `docs/chapters/ch19e_dpf_hmc_target_suitability.tex`;
- `docs/chapters/ch19f_dpf_debugging_crosswalk.tex`;
- `docs/chapters/ch32_diff_resampling_neural_ot.tex`;
- `experiments/dpf_monograph_evidence/reports/dpf-monograph-research-evidence-note.md`;
- `experiments/dpf_monograph_evidence/reports/linear-gaussian-recovery-result.md`;
- `experiments/dpf_monograph_evidence/reports/affine-flow-pfpf-result.md`;
- `experiments/dpf_monograph_evidence/reports/resampling-sinkhorn-result.md`;
- `experiments/dpf_monograph_evidence/reports/learned-ot-residual-result.md`;
- `experiments/dpf_monograph_evidence/reports/hmc-value-gradient-result.md`;
- `docs/references.bib`;
- `docs/source_map.yml`.

## Outputs

- `docs/plans/bayesfilter-dpf-implementation-dpf0-claim-ledger-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf0-implementation-obligations-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf0-result-2026-05-28.md`.

## Skeptical Plan Audit Checklist

- Did DPF0-A pass or identify only nonblocking patch recommendations?
- Are the DPF0-A artifacts current and present at the exact paths above?
- Does the DPF0-A result explicitly say `DPF0 may start: yes`?
- Did any input drift into the high-dimensional nonlinear filtering lane?
- Are student documents prevented from becoming source authority?
- Is every equation/algorithm obligation traceable?
- Are theorem, heuristic, diagnostic, and engineering-choice claims separated?
- Are differentiability and likelihood validity kept separate?
- Are posterior/HMC claims excluded or gated?

## Execution Steps

1. Extract claim clusters from monograph chapters and evidence reports.
2. Attach source/proof status.
3. Translate only accepted monograph/literature or explicitly marked
   engineering-choice claims into implementation obligations; do not use student
   documents as authority.
4. Mark uncertain claims as blockers or future review items.
5. Write result with next phase decision.

## Review Protocol

This plan must be reviewed by Claude Code with:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Claude must output `ACCEPT` or `REJECT`. Codex audits the review and loops up
to 5 iterations, accepting the fifth version only for user inspection with
unresolved risks recorded.

## Verification Commands

```bash
rg -n "DPF0 may start: yes" docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-result-2026-05-28.md
rg -n "blocked|unsupported|implementation obligation|not concluded" docs/plans/bayesfilter-dpf-implementation-dpf0-*.md
git diff --check
git status --short --branch
```

## Stop Conditions

- DPF0-A blocker remains open;
- DPF0-A result does not explicitly say `DPF0 may start: yes`;
- a needed source cannot be identified;
- student documents would be needed as authority;
- the high-dimensional nonlinear filtering lane would need to be read or edited;
- implementation obligations require production code before DPF6.

## What Must Not Be Concluded

DPF0 does not conclude that any implementation is correct, differentiable,
fast, production-ready, or HMC-valid.

## Review Record

- Claude Code reviewer: `claude-opus-4-7`, `--effort max`.
- Iteration 1: `REJECT`; required fuller skeptical audit, exact review command,
  and explicit student-nonauthority execution boundary.
- Iteration 2: `REJECT`; required auditable DPF0-A prerequisite outcome check.
- Iteration 3: `ACCEPT`.
- Codex audit: agreed with rejected findings, patched this plan, and accepted
  the iteration-3 result.
