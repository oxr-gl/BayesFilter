# P23 Zhao--Cui Chemist And Implementation Gap-Closure Result

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P22 integrated readable companion and fixed-branch gradient note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive branches.
- No HMC convergence claim.
- No production implementation readiness claim.
- No executable prototype claim.
- No empirical validation on BayesFilter target models.
- No default-method recommendation.

## Status

Decision: `P23_EXECUTION_REVIEW_ACCEPTED`.

P23 was produced as a P22-preserving expansion.  It copies the P22
mathematical spine and adds eleven chemist-reader and implementation-engineer
gap closures.  It does not edit chapters, production code, DPF lane,
student-baseline, controlled-DPF, public APIs, or earlier P20/P21/P22
artifacts.

## What Codex Inspected

- P23 plan, note, PDF, eleven-gap ledger, P22 preservation ledger, review
  ledger, discrepancy report, and result artifact.
- P22 baseline TeX/PDF for line and page count guardrails.
- LaTeX build log for the P23 PDF.
- PDF text for P23 section and anchor presence.
- Git status/diff scope for allowed-write checks.
- Scholarly-literature-audit policy and review protocol.

## P22 Gaps Addressed

P23 adds exact-anchor gap closures for:

- threaded nonlinear example: P23-E1--P23-E13;
- rank-count plausibility: P23-RANK1--P23-RANK6;
- deterministic fixed-rank sweep protocol: P23-SWEEP1--P23-SWEEP8 and
  P23-SWEEP1a--P23-SWEEP1h;
- worked two-dimensional KR construction: P23-KR2-1--P23-KR2-11 and
  P23-KR2-8a--P23-KR2-8e;
- operational KR construction: P23-KROPS1--P23-KROPS10;
- preconditioning flattening and example callback: P23-PREC1--P23-PREC11;
- domain-selection policy: P23-DOM1--P23-DOM7;
- stabilization defaults: P23-STAB1--P23-STAB9;
- multidimensional retained-filter derivation: P23-MD1--P23-MD9 and
  P23-MD4a--P23-MD4e;
- Proposition 2 dependency graph and conditioning caveat:
  P23-GDAG1--P23-GDAG8 and P23-GDAG2a;
- saved branch manifest: P23-MAN1--P23-MAN7.

## Count Validation

| Artifact | Method used | P22 | P23 | Status |
|---|---:|---:|---:|---|
| TeX lines | `wc -l` | 4815 | 5966 | `PASS` |
| PDF pages | `pdfinfo` | 55 | 67 | `PASS` |

The count guardrail is satisfied: P23 is longer than P22 in TeX line count and
not shorter in PDF page count.

## Build Status

PDF build status: `PASS`.

Command:

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.tex
```

Result:

- P23 PDF produced beside the note.
- Final P23 PDF page count: 67.
- Build log contains underfull hbox warnings only.
- No undefined references, undefined citations, overfull boxes, missing files,
  fatal errors, or rerun blockers were found by the validation scan.

## Validation Commands Run

```bash
wc -l docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-note-2026-06-02.tex docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.tex
pdfinfo docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p22-zhao-cui-integrated-readable-companion-note-2026-06-02.pdf
pdfinfo docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.pdf
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-plan-2026-06-02.md docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.tex docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-eleven-gap-ledger-2026-06-02.md docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-p22-preservation-ledger-2026-06-02.md docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-claude-review-ledger-2026-06-02.md docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-discrepancy-report-2026-06-02.md docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-result-2026-06-02.md
rg -n -e 'LaTeX Warning:' -e 'Citation .* undefined' -e 'Reference .* undefined' -e 'undefined references' -e 'Overfull' -e 'Missing file' -e 'Emergency stop' -e 'Fatal' -e '^!' docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.log
pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.pdf -
rg -q '^metadata_date:' docs/plans/*p23-zhao-cui*.md
rg -q '^seed_papers:' docs/plans/*p23-zhao-cui*.md
rg -q '^what_is_not_concluded:' docs/plans/*p23-zhao-cui*.md
git status --short
```

## Claude Review History

Plan review:

- Iteration 1: `REJECT`; Codex classified 8 findings as `ACCEPT` and patched
  plan controls.
- Iteration 2: `REJECT`; Codex classified 3 findings as `ACCEPT` and patched
  preservation/gap auditability controls.
- Iteration 3: `ACCEPT`; Codex independently agreed.

Execution review:

- Iteration 1: `REJECT`; Codex classified all 8 findings as `ACCEPT`.
  Patches added P23-SWEEP1a--P23-SWEEP1h, P23-KR2-8a--P23-KR2-8e,
  P23-PREC10--P23-PREC11, P23-MD4a--P23-MD4e, P23-GDAG2a, P23-GDAG8, and
  related ledger controls.
- Iteration 2: `REJECT`; Codex classified all 3 findings as `ACCEPT`.
  Patches updated the stale result/review/discrepancy state and final count
  validation numbers.
- Iteration 3: `ACCEPT`; Codex independently agreed.

Codex audit classifications summary:

- Plan review accepted findings: 11 `ACCEPT`, 0 `PARTIAL`, 0 `DISPUTE`,
  0 `CLARIFY`.
- Execution review accepted findings so far: 11 `ACCEPT`, 0 `PARTIAL`,
  0 `DISPUTE`, 0 `CLARIFY`.
- No unresolved Claude/Codex disagreements are recorded.

## Files Changed

P23 source and result artifacts:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-plan-2026-06-02.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-note-2026-06-02.pdf`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-eleven-gap-ledger-2026-06-02.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-p22-preservation-ledger-2026-06-02.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-claude-review-ledger-2026-06-02.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-discrepancy-report-2026-06-02.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p23-zhao-cui-chemist-implementation-gap-closure-result-2026-06-02.md`

P23 LaTeX build byproducts also exist beside the note:

- `.aux`, `.fdb_latexmk`, `.fls`, `.log`, `.out`, `.toc`

Known unrelated dirty/untracked files exist elsewhere in the repository,
especially DPF/student-baseline material and `.local_sources`; they were not
edited for P23.

## Residual Chemist-Reader Gaps

Decision: `LOW_TO_MODERATE_RESIDUAL_RISK`.

P23 is much more teachable than P22 because it adds a threaded example, a 2D KR
worked example, explicit preconditioning substitution, and step-by-step
fixed-branch derivative flow.  Remaining risk is that a chemistry chair may
still need oral guidance for tensor-train rank intuition and the first pass
through square-root TT mass contractions.  The document now contains the
mathematics needed for that teaching, but it is still a dense 67-page technical
note.

## Residual Implementation-Engineer Gaps

Decision: `LOW_TO_MODERATE_RESIDUAL_RISK`.

The document is now sufficient for a minimal mathematical implementation plan
of a squared-TT sequential filter and fixed-branch derivative, excluding
production optimization.  Remaining implementation risks are numerical:
conditioning of ridge solves, rank growth, bridge quality, CDF monotonicity,
and finite-difference branch equality.  P23 records diagnostics for these
risks but does not provide executable code or empirical success evidence.

## Final Probability Estimate

Estimated probability that P23 passes a skeptical mixed
chemistry/numerical/implementation panel: `0.74`, conditional on the panel
evaluating this as a mathematical companion/specification rather than as a
production implementation or empirical validation package.
