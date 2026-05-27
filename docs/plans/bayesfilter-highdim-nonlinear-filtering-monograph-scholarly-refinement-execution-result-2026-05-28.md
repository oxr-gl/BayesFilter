# High-Dimensional Nonlinear Filtering Scholarly Refinement Execution Result

Date: 2026-05-28

## Scope

Lane: high-dimensional nonlinear filtering monograph only.

Active master program:
`docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-master-program-2026-05-27.md`.

The execution rewrites and integrates chapters `ch33`--`ch37` as a scholarly
monograph block.  It does not execute the DPF implementation lane, edit
student-baseline files, edit controlled-DPF files, edit production
`bayesfilter/`, change public APIs, run GPU commands, run network/API source
intake, or run long HMC chains.

## Skeptical Plan Audit

Result: pass to execute bounded document refinement.

Audit findings before execution:

- Wrong baselines: no new numerical promotion was planned; BayesFilter P8 rows
  are used only as execution diagnostics.
- Proxy metrics: smoke rows, ESS, training loss, and point-count diagnostics
  are explicitly barred from becoming posterior accuracy, sampler convergence,
  or production evidence.
- Missing stop rules: strengthened master/subplans include source, derivation,
  section/page review, PDF, and no-overclaim blockers.
- Unfair comparisons: the candidate ranking is framed as evidence-building
  priority, not a method-performance leaderboard.
- Stale context: `docs/main.pdf` was stale and `docs/main.tex` did not include
  the new chapters before this execution.
- Hidden source gaps: tensor-train/tensor-network and some sparse-grid claims
  are retained as source-gap blockers unless supported by checked primary
  sources.
- PDF integration risk: integration into `docs/main.tex` and a fresh
  `docs/main.pdf` build are required before final acceptance.

## Codex Inspected

- Master program and subplans P0--P10 under
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-*`.
- Existing chapter scaffolds:
  `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`,
  `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`,
  `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`,
  `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`,
  `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`.
- `docs/main.tex`, `docs/preamble.tex`, `docs/references.bib`,
  `docs/source_map.yml`.
- P8 benchmark artifacts:
  `docs/benchmarks/bayesfilter-highdim-nonlinear-filtering-smoke-2026-05-27.json`
  and `.md`.
- Git status, including unrelated dirty DPF/student/controlled-baseline files
  that remain unstaged and outside this lane.

## ResearchAssistant MCP Use

- `ra_workspace_status`: confirmed local read-only ResearchAssistant status.
- `ra_review_list`: identified local review items for NeuTra, RMHMC, learned
  HMC, and normalizing flows, all still `needs_review`.
- `ra_find_paper`: searched local summaries for tensor-train/nonlinear
  filtering, ensemble transport, and sparse-grid filtering; no local paper
  summaries were found for those combined queries.
- `ra_get_paper_summary` for NeuTra: summary available but source extraction
  unavailable and manual review required.  Used only as bounded review material,
  not theorem support.

## MathDevMCP Use

- `doctor`: available LaTeXML, Pandoc, Sage, SymPy, LeanDojo; direct Lean
  version timed out.
- `search_latex`: located the existing likelihood-factorization block in
  `ch33` before rewrite.
- `search_latex`: confirmed the rewritten `bf-highdim-*` labels are indexed.
- `audit_derivation_v2_label`: attempted audits for
  `prop:bf-highdim-likelihood-factorization`,
  `prop:bf-highdim-predictive-score`,
  `prop:bf-highdim-moment-projection`,
  `prop:bf-highdim-transport-correction`, and
  `prop:bf-highdim-same-scalar`.  These audits were diagnostic only:
  bounded symbolic routing could not certify measure-theoretic identities, and
  typed matrix obligations still require human review, explicit invertibility
  or dimension assumptions, or additional formalization.  No chapter claims a
  machine-checked theorem certificate.

## Phase Results

| Phase | Result label | Notes |
| --- | --- | --- |
| P0 | `P0_SCHOLARLY_SCOPE_ACCEPTED` | Strengthened gates used as execution contract. |
| P1 | `P1_SCHOLARLY_SOURCE_ACCEPTED_WITH_GAPS` | Primary sources used where available; tensor/TN sparse gaps kept as blockers. |
| P2 | `P2_FOUNDATIONS_REWRITTEN_AUDIT_LIMITED` | Foundations rewritten; MathDevMCP audit attempts were diagnostic-only, not certification. |
| P3 | `P3_GAUSSIAN_SOURCE_ACCEPTED` | Gaussian/high-order chapter rewritten; sparse-grid material downgraded to source-gap blocker. |
| P4 | `P4_PARTICLE_TRANSPORT_SOURCE_ACCEPTED` | Particle/flow/transport material rewritten with proposal/correction boundaries. |
| P5 | `P5_TENSOR_BLOCKER_SOURCE_ACCEPTED` | Tensor material downgraded to blocker/checklist language because local source support is metadata/source-gap only. |
| P6 | `P6_HMC_REWRITTEN_AUDIT_LIMITED` | HMC chapter rewritten; no HMC convergence, production, or TFP NUTS production claim. |
| P7 | `P7_SYNTHESIS_SOURCE_ACCEPTED` | Candidate ranking split into implementation-near order and source-gated watchlist. |
| P8 | `P8_SCHOLARLY_EVIDENCE_ACCEPTED` | Existing P8 artifact used only as execution metadata; no rerun. |
| P9 | `P9_PDF_BUILT_PAGE_REVIEW_ACCEPTED` | `docs/main.tex` integration complete, `docs/main.pdf` built, and rendered page review accepted. |
| P10 | `P10_FINAL_AUDIT_READY_FOR_COMMIT` | Final validation and path-scoped commit pending at this note revision. |

## Chapter Changes

- `ch33`: expanded exact filtering recursion, likelihood factorization,
  predictive-score identity, approximate posterior boundary, high-dimensional
  failure ledgers, NAWM-like stress discussion, BayesFilter evidence boundary,
  source/evidence ledger, and unresolved-claim register.
- `ch34`: expanded Gaussian projection derivation, second-order EKF sketch,
  sigma-point pseudocode, CUT4 point-growth discussion, block-local algorithm,
  complexity table, and evidence boundary.
- `ch35`: expanded SIR/guided PF algorithms, importance-weight derivation,
  transport correction proposition, ensemble transport diagnostic algorithm,
  TT/TN pilot algorithm, complexity table, and source-gap ledger.
- `ch36`: expanded HMC target/gradient contract, same-scalar proposition,
  fixed-HMC algorithm, NUTS policy, NeuTra/RMHMC/HNN ladders, diagnostics, and
  XLA/GPU boundaries.
- `ch37`: expanded candidate ranking into a multi-criteria table, synthesis
  architecture, decision table, practitioner questions, and source/evidence
  ledger.

## Claude Review History

| Review unit | Iteration | Claude verdict | Codex audit and repair |
| --- | ---: | --- | --- |
| Source/section hostile review | 1 | `REJECT` | Codex agreed.  Repaired by downgrading tensor-train/tensor-network and sparse-grid prose to source-gap blocker/checklist language, splitting the synthesis ranking into implementation-near and source-gated watchlist tables, and reconciling `docs/source_map.yml` with actual source support. |
| Source/section hostile review | 2 | `ACCEPT` | Claude accepted the source-level scholarly repairs. |
| Rendered PDF/page-range review | 1 | `ACCEPT` | Claude accepted the rendered new block as readable, citation/cross-reference clean, and free of unsupported orphan claims.  Residual table-pressure warnings were non-blocking. |
| Final section-granular scholarly review | 1 | `ACCEPT` | Claude accepted all sections in `ch33`--`ch37`, `docs/source_map.yml`, `docs/references.bib`, and this execution note.  One suggested bib-key cross-check for `julier1996general` was verified resolved in `docs/references.bib` and `docs/main.bbl`. |

## Section Review Ledger

The first hostile review bundled the five chapter source files plus source-map
and execution-note context.  Claude identified major section-level blockers in
`ch34`, `ch35`, `ch37`, and `docs/source_map.yml`; Codex agreed and repaired
those blockers before iteration 2.

The final section-granular review accepted:

- `ch33`: claim discipline, SSM contract, prediction/update/likelihood,
  exact-vs-approximate posterior boundary, failure mechanisms, NAWM-like stress,
  evidence boundary, ledgers, and unresolved nonclaims.
- `ch34`: Gaussian projection, derivative filters, sigma-point/cubature,
  point-growth and sparse-grid blocker, block-local algorithm, complexity and
  failure diagnostics, evidence boundary, and industrial stress.
- `ch35`: PF baseline, guided proposals, flow proposals, ensemble transport,
  TT/TN blockers, low-rank observation blocker, complexity and failure
  diagnostics, industrial stress, and literature matrix.
- `ch36`: HMC target/correction, same-scalar condition, plain-HMC failure,
  fixed-HMC baseline, diagnostic-only NUTS policy, NeuTra/RMHMC/HNN ladders,
  diagnostics, XLA/GPU boundary, and evidence ledger.
- `ch37`: evidence-state assumptions, ranking criteria, implementation-near
  order, source-gated watchlist, synthesis architecture, decision table,
  practitioner questions, evidence boundary, and unresolved nonclaims.

## PDF Review Ledger

`docs/main.pdf` was built successfully after integrating `ch33`--`ch37` into
`docs/main.tex`.  `pdftotext` confirmed that the PDF contains the five new
chapter titles.  Claude accepted the rendered page range covering the new block
as readable, with resolved citations/cross-references and no unsupported orphan
claims.  Remaining overfull/underfull warnings are layout polish, not
scholarly-presentation blockers for this lane.

## Commands Run

Recorded incrementally during execution:

- `git status --short`
- `git log --oneline -5`
- `rg --files docs/plans docs/chapters docs/benchmarks`
- `sed -n ...` inspections of plans, chapters, `docs/main.tex`,
  `docs/preamble.tex`, `docs/references.bib`, and `docs/source_map.yml`
- `python -c ...` inspection of the P8 JSON artifact
- ResearchAssistant MCP and MathDevMCP calls listed above
- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` from `docs/`
- `pdftotext docs/main.pdf - | rg "<new chapter titles>"`
- `pdftotext -f 176 -l 202 -layout docs/main.pdf /tmp/highdim_pages_final.txt`
- `pdfinfo docs/main.pdf`
- `rg -n "undefined|Citation.*undefined|Reference.*undefined|Rerun to get cross-references|There were undefined" docs/main.log`
- `rg -n "julier1996general|julier1997new|vandermerwe2004sigma" docs/references.bib docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex docs/main.bbl docs/main.log`
- `rg -n ...` and `nl -ba ...` inspections of Claude-flagged source-gap
  passages in `ch34`, `ch35`, `ch37`, and `docs/source_map.yml`

## PDF Build Status

`docs/main.pdf` exists, was rebuilt on 2026-05-28 after the integration, has
254 pages, and contains the chapter titles:

- `High-Dimensional Nonlinear Filtering Foundations`
- `Gaussian Projection and High-Order Quadrature Filters`
- `Particle, Transport, Tensor-Train, and Tensor-Network Filters`
- `HMC as a Research Program for Nonlinear State-Space Models`
- `Candidate Synthesis for Industrial-Scale Nonlinear Filtering`

The build has no undefined-reference or undefined-citation diagnostics in the
checked log patterns.  It still has overfull/underfull box warnings, including
wide table pressure in the new high-dimensional block.  Rendered page review
accepted those as non-blocking because the extracted pages remain readable and
the warnings do not indicate clipped or corrupted content in the reviewed block.

## Final Audit Status

Pre-commit verdict: `PASS_PENDING_PATH_SCOPED_COMMIT`.

- Every phase P0--P10 has a result label or an explicit pending-to-commit note.
- Every chapter section passed final hostile review or carries an explicit
  source-gap/blocker label.
- The rendered PDF page range for the new block passed hostile review.
- Literature claims are tied to primary citations, local ResearchAssistant
  limitations, BayesFilter artifacts, or explicit source-gap blockers.
- Major equations have assumptions and proof sketches, with MathDevMCP audits
  recorded as diagnostic/inconclusive rather than machine certification.
- Method families have algorithm/exclusion rationale, scaling or memory notes,
  failure diagnostics, industrial stress discussion, and BayesFilter evidence
  links or blockers.
- No production code, DPF implementation lane file, student-baseline file, or
  controlled-DPF file was edited by this lane execution.
- The work does not claim NAWM readiness, HMC convergence, tensor-method
  validation, broad GPU/XLA readiness, posterior accuracy, production default
  readiness, or client switch-over readiness.

## Non-Implications

This execution does not establish NAWM readiness, HMC convergence, tensor-method
validation, broad GPU speedup, broad XLA readiness, posterior accuracy,
production default readiness, or exact nonlinear likelihood evidence for
BayesFilter Models B--C.
