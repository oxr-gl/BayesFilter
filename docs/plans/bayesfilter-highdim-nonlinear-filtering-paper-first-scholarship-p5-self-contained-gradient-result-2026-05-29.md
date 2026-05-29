# P5 Self-Contained Exposition And Analytical-Gradient Result

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T/P1U/P2R/P3/P4 high-dimensional nonlinear filtering
artifacts, P5 plan and ledgers, `ch33`--`ch37`, `docs/references.bib`,
`docs/main.tex`, `docs/main.log`, `docs/main.pdf`, MathDevMCP diagnostics, and
Claude review results.

what_is_not_concluded: This result does not conclude production readiness,
NAWM readiness, posterior accuracy, HMC convergence, tensor-method validation,
transport-method validation, GPU/XLA readiness, default readiness,
machine-certified proof validity, continuous-time/PDE adjoint validity, or
exhaustive literature coverage.

## Decision

`READY_FOR_USER_REVIEW_WITH_RESIDUAL_LIMITS`.

The P5 pass materially reduces the two risks named by the user: the chapters
are more self-contained for a mixed numerical panel, and the HMC chapter now
has an analytical gradient derivation tied to the state-space likelihood
sensitivity recursion.  The block is still a compact monograph block, not a
textbook-length filtering treatment or a machine-certified theorem file.

## Codex Inspection

Codex inspected:

- `ch33`--`ch37`;
- P1R/P1S/P1T/P1U/P2R/P3/P4 artifacts and P4 derivation/MathDevMCP ledgers;
- `docs/references.bib`;
- `docs/main.tex`, `docs/main.log`, and `docs/main.pdf`;
- the scholarly literature audit policy and Codex skill;
- the dirty worktree state, including unrelated DPF/student-baseline artifacts
  outside the P5 write scope.

## Plan And Execution Summary

Created:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p5-self-contained-gradient-plan-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p5-self-contained-exposition-ledger-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p5-analytical-gradient-derivation-ledger-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p5-mathdevmcp-audit-ledger-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p5-claude-review-ledger-2026-05-29.md`

Executed:

- self-contained object/role paragraphs in `ch33`--`ch37`;
- exact discrete-time likelihood-gradient sensitivity recursion in `ch33`;
- analytical transformed HMC potential-gradient derivation in `ch36`;
- scalar Gaussian hand-computable gradient example in `ch36`;
- approximate-filter gradient contract in `ch33`, `ch36`, and `ch37`;
- PDF rebuild and rendered-text validation.

## Chapter Changes

`ch33` now defines the conditional filtering law, normalizer, likelihood scalar,
and derivative object before the method discussion.  It adds a full
discrete-time likelihood-gradient derivation:

- prediction sensitivity;
- normalizer gradient;
- likelihood gradient as \(\sum_t\nabla_\theta Z_t/Z_t\);
- normalized update sensitivity;
- assumptions and continuous-time/PDE boundary.

`ch34` now states that Gaussian and quadrature filters operate on a projected
moment pair and Gaussian-weighted expectations.  It explicitly separates exact
conditional-law target, moment-closure approximation, diagnostic role, and
industrial relevance.

`ch35` now separates empirical particle measures, transport/coupling objects,
and tensor representations.  It clarifies that finite ensembles, fitted maps,
and low-rank formats remain approximations unless correction, support, rank,
mass, positivity, PSD, and likelihood/score gates are visible.

`ch36` now derives the HMC potential gradient analytically from
\(\theta=\tau(q)\), the likelihood gradient, the prior gradient, and the
Jacobian term.  It adds the proposition-level HMC gradient contract, a scalar
Gaussian likelihood-gradient example, and a clear approximate-filter gradient
section.

`ch37` now adds a reader-facing synthesis map and repeats the key
anti-overclaim rule: approximate-filter gradients support only the declared
approximate scalar and are not exact posterior or exact likelihood gradients
without exact correction.

## MathDevMCP Status

MathDevMCP verified only small algebra:

- log-normalizer derivative algebra;
- quotient-rule normalization algebra;
- scalar Gaussian HMC-gradient sign simplifications.

Typed label audits for `prop:bf-hd-likelihood-sensitivity` and
`prop:bf-hd-hmc-gradient-contract` were `MCP_UNVERIFIED` / typed-review only.
The broad integral sensitivity recursion and HMC target contract remain
human-reviewed project derivations, not machine-certified proofs.

## Claude Review History

- Plan iter 1, `highdim-p5-self-contained-gradient-plan-review-iter1`:
  `REJECT`.  Codex agreed and repaired the plan.
- Plan iter 2, `highdim-p5-self-contained-gradient-plan-review-iter2`:
  `ACCEPT`.
- Content/ledger iter 1,
  `highdim-p5-self-contained-gradient-block1-review-iter1`: `ACCEPT`.

No fifth-iteration override was used.

## PDF Build Status

Command:

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/main.tex
```

Result: success.  `docs/main.pdf` exists with 262 pages and was rebuilt on
2026-05-29 at 19:04:10 HKT.

No undefined citation/reference/rerun blockers were found by the log scan.
Rendered PDF text contains:

- `Analytical Likelihood-Gradient And Filtering Sensitivities`;
- `Discrete-time likelihood sensitivity recursion`;
- `Analytical HMC Gradient From The Filtering Likelihood`;
- `HMC gradient contract for a state-space likelihood`;
- `Approximate-Filter Gradients`;
- the `reader-facing synthesis map`.

Remaining warnings are layout/editorial warnings, mostly underfull/overfull
boxes in tables and section headings.  They are not citation/reference or PDF
build blockers.

## Validation Commands

```bash
git diff --check
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/main.tex
rg -n "undefined|Citation .* undefined|Reference .* undefined|There were undefined|Rerun to get cross-references|Rerun to get outlines" docs/main.log
pdftotext docs/main.pdf - | rg -n "Analytical Likelihood-Gradient|Analytical HMC Gradient|Approximate-Filter Gradients|Discrete-time likelihood sensitivity recursion|HMC gradient contract|reader-facing synthesis map"
pdfinfo docs/main.pdf
git status --short -- docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex docs/main.pdf docs/references.bib docs/source_map.yml docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p5-* .local_sources
git ls-files --others --exclude-standard .local_sources | sed -n '1,40p'
```

## Residual Scholarly Gaps

- The sensitivity recursion is professor-readable under dominated
  differentiation assumptions, but not a measure-theoretic appendix.
- MathDevMCP did not certify broad propositions.
- Continuous-time/PDE likelihood-gradient or adjoint formulas remain outside
  this pass.
- The Meng 2026 correlated-noise arXiv source remains a provisional obstacle
  marker and will draw scrutiny until stronger published support exists.
- The chapters are more self-contained, but still compact relative to a full
  textbook treatment for every numerical discipline.
- Layout warnings remain.
- The wider worktree contains unrelated dirty DPF/student-baseline and
  references artifacts; P5 did not stage or commit anything.

## Probability Estimate

Estimated probability of passing a skeptical mixed numerical former-academic
panel as a serious academic/industrial monograph block: `0.78--0.84`.

This estimate is conditional on the panel accepting explicit residual limits:
human-reviewed rather than machine-certified derivations, no production or NAWM
claims, and compact rather than textbook-length exposition.
