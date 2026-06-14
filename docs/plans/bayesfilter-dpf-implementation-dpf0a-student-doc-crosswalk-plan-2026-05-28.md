# Plan DPF0-A: Student-Document Crosswalk And Discrepancy Adjudication

## Date

2026-05-28

## Lane Boundaries

- DPF0-A must finish and record a nonblocking handoff before DPF0 starts.
- Student artifacts are comparison-only documents; they are never correctness
  authority.
- Do not edit vendored student files and do not execute student code.
- Do not edit production `bayesfilter/` code.
- Do not read or edit the high-dimensional nonlinear filtering lane.
- Do not edit monograph chapters in this phase; record patch recommendations
  only.

## Evidence Contract

Question:

Do the DPF monograph documents agree with student documents/reports on claims
needed before implementation, and if not, which side should change or be
quarantined?

Baseline/comparator:

- DPF monograph chapters and DPF monograph evidence artifacts;
- student reports/documents and controlled-baseline archive, comparison-only;
- cited literature/source support where available.

Primary criterion:

- Every material discrepancy found in the sampled DPF implementation scope is
  classified with an adjudication label, assumptions, source/proof status, and
  implementation consequence.

Veto diagnostics:

- a discrepancy affects a core implementation obligation and cannot be
  adjudicated or downgraded;
- the audit treats student work as authority;
- the audit claims students are wrong without proof, counterexample, or source
  support;
- the audit modifies monograph chapters rather than recording patch
  recommendations.
- the audit executes student code or edits vendored student files.

Explanatory diagnostics:

- student result metrics, runtime, or qualitative agreement labels;
- implementation examples found in student documents.

What will not be concluded:

- no production readiness;
- no correctness certificate from student agreement;
- no claim that all student code paths were reviewed;
- no HMC/posterior/monograph update without later phases.

## Exact Inputs

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
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-gap-closure-result-2026-05-10.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-hypothesis-closure-result-2026-05-10.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-linear-stress-result-2026-05-10.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-nonlinear-smoke-result-2026-05-10.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-nonlinear-reference-panel-result-2026-05-10.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-mlcoe-particle-gate-result-2026-05-10.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-edh-pfpf-adapter-spike-result-2026-05-11.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-flow-dpf-readiness-review-result-2026-05-11.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-replicated-edh-pfpf-panel-result-2026-05-12.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-full-horizon-edh-pfpf-confirmation-result-2026-05-12.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-full-horizon-edh-pfpf-sensitivity-result-2026-05-12.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-future-work-usability-gates-result-2026-05-15.md`;
- `experiments/student_dpf_baselines/reports/advanced-particle-filter-reproduction-2026-05-10.md`;
- `experiments/student_dpf_baselines/reports/advanced-particle-filter-kernel-pff-reproduction-2026-05-10.md`;
- `experiments/student_dpf_baselines/reports/advanced-particle-filter-kernel-pff-debug-gate-result-2026-05-11.md`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-smoke-result.md`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-fixed-grid-result.md`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-comparison-audit.md`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-final-archive-result.md`;
- student document files under vendored snapshots, including READMEs, docs, and
  notebooks only as documents, with no code execution or edits:
  - `experiments/student_dpf_baselines/vendor/README.md`;
  - `experiments/student_dpf_baselines/vendor/SNAPSHOT.md`;
  - `experiments/student_dpf_baselines/vendor/2026MLCOE/README.md`;
  - `experiments/student_dpf_baselines/vendor/advanced_particle_filter/README.md`;
  - `experiments/student_dpf_baselines/vendor/advanced_particle_filter/docs/amortized_ot_operator.md`;
  - `experiments/student_dpf_baselines/vendor/advanced_particle_filter/notebooks/README.md`;
  - notebook markdown extracted for reading only from
    `experiments/student_dpf_baselines/vendor/advanced_particle_filter/notebooks/`;
- `docs/references.bib`;
- `docs/source_map.yml`.

## Outputs

- `docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-ledger-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-result-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf0a-doc-patch-register-2026-05-28.md`.

The result note must include an explicit ordering gate line:
`DPF0 may start: yes` or `DPF0 may start: no - blocked`.

## Discrepancy Labels

- `consistent`;
- `assumption_mismatch`;
- `student_claim_wrong`;
- `our_doc_wrong_or_incomplete`;
- `unsupported_student_claim`;
- `implementation_only`;
- `blocked_needs_source_review`.

## Skeptical Plan Audit Checklist

- Are we comparing documents/claims rather than implementation source?
- Are student claims kept comparison-only?
- Are vendored student files read-only and never executed?
- Is every "student wrong" label supported by proof, counterexample, or primary
  source?
- Are monograph patch needs recorded rather than silently fixed?
- Are target semantics separated: classical PF, PF-PF, DPF, differentiable
  resampling, learned OT, and HMC?
- Are implementation-only ideas prevented from becoming mathematical claims?
- Are stop conditions clear for unadjudicated core discrepancies?

## Execution Steps

1. Inventory DPF monograph claim clusters:
   classical PF, resampling, particle flow, PF-PF correction, differentiable
   resampling/OT, learned OT, debugging, HMC suitability.
2. Inventory student-document claim clusters from reports, READMEs, docs, and
   notebook markdown without executing code.
3. Match claims by topic and assumptions.
4. Classify each material discrepancy.
5. Record proof/source status and implementation consequence.
6. Write patch recommendations only; do not patch monograph chapters.
7. Write result note and next-action decision; DPF0 may start only if this
   result records no core blocker.

## Review Protocol

This plan must be reviewed by Claude Code with:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Claude must output `ACCEPT` or `REJECT`.  Codex audits the review and loops up
to 5 iterations, accepting the fifth version only for user inspection if needed.

## Verification Commands

```bash
rg -n "student_claim_wrong|our_doc_wrong_or_incomplete|unsupported_student_claim|blocked_needs_source_review" docs/plans/bayesfilter-dpf-implementation-dpf0a-*.md
rg -n "experiments/student_dpf_baselines/vendor" docs/plans/bayesfilter-dpf-implementation-dpf0a-*.md
rg -n "DPF0 may start: yes|DPF0 may start: no - blocked" docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-result-2026-05-28.md
git diff --check
git status --short --branch
```

No Python compile is required unless a future revision edits Python files.

## Stop Conditions

- core discrepancy cannot be classified;
- source support is missing for a categorical mathematical rejection;
- student code must be executed to decide a document discrepancy;
- vendored student files would need edits;
- monograph chapter patching becomes necessary before result recording;
- high-dimensional nonlinear filtering lane would need to be read or edited.

## Review Record

- Claude Code reviewer: `claude-opus-4-7`, `--effort max`.
- Iteration 1: `REJECT`; required explicit vendored-student boundary and DPF0
  ordering gate.
- Iteration 2: `REJECT`; required auditable ordering-gate verification.
- Iteration 3: `ACCEPT`.
- Codex audit: agreed with rejected findings, patched this plan, and accepted
  the iteration-3 result.
