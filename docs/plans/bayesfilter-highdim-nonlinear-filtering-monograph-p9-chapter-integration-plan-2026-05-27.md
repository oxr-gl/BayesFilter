# P9 Monograph Chapter Integration Plan

## Question

Do the chapter drafts form a coherent, reviewer-grade nonlinear filtering block?

## Evidence Contract

Baseline:

- P1-P8 outputs.
- Existing BayesFilter chapter conventions.

Primary criterion:

- The draft chapters are self-contained, use BayesFilter notation, include
  assumptions, algorithms, derivations, evidence boxes, limitations, and claim
  ledgers.
- Every chapter includes a per-claim source/evidence ledger, theorem or lemma
  provenance where applicable, unresolved-claim register, and "what is not
  concluded" section.
- For scholarly readiness, every chapter section must pass hostile local review
  and every rendered PDF page must pass page-by-page review.  The chapters must
  be included in `docs/main.tex`, LaTeX must build, and `docs/main.pdf` must
  contain chapters 33--37.

Veto diagnostics:

- Chapters rely on undefined production readiness.
- Chapters cite nonexistent BayesFilter evidence.
- Chapters introduce unsupported mathematical or empirical claims.
- A section survives only because it is conservative while remaining thin,
  uncited, underived, algorithmically vague, or practically irrelevant.
- `docs/main.tex` omits any of chapters 33--37, LaTeX fails to build, or the
  PDF text does not contain the new chapters.
- Rendered pages contain broken references, unreadable tables, equation
  discontinuities, or orphan claims not supported by the surrounding section.

Explanatory diagnostics:

- Source-map entries and MathDevMCP derivation audits, after mandatory gates are
  satisfied.

Non-implications:

- Passing the original P9 draft gate does not mean the chapters are
  publication-final.  Passing the scholarly P9 gate means only that the chapter
  block is ready for external skeptical review, not that its methods are
  validated.

Artifacts:

- Chapter drafts `ch33` through `ch37`.
- Integrated `docs/main.tex`.
- Built `docs/main.pdf` containing the new chapters.
- Section-review ledger and page-review ledger.
- `docs/source_map.yml` entry.

## Chapter Gates

Each chapter must have:

- scoped chapter claim;
- assumptions;
- definitions and notation where needed;
- at least one algorithm or decision table when algorithmic content is present;
- source/evidence ledger;
- unresolved-claim register;
- "what is not concluded" section;
- explicit connection to P8 diagnostics only where the P8 chapter-use
  restriction allows it.

## Section/Page Hostile Review Protocol

For each section, Claude Code reviews read-only as a hostile scholarly reviewer
and must output `ACCEPT` or `REJECT`.  Codex audits the review and patches if it
agrees.  Repeat up to 10 iterations per section.  On iteration 10, accept only
minor editorial residue; any unresolved source, derivation, evidence,
algorithm, complexity, industrial-relevance, or overclaim issue is a blocker.

After LaTeX build, repeat the same max-10 loop for rendered PDF pages or stable
page ranges.  Page review checks layout, references, table readability,
equation continuity, citation visibility, and orphan claims.

## Stop Rules

Stop P9 with a blocker if any chapter lacks the chapter gates or contains a
claim that cannot be source-supported, derived, or downgraded.

Stop P9 scholarly refinement with a blocker if any section/page fails the
hostile review loop within 10 iterations, if PDF integration fails, or if any
chapter remains safe but thin under the scholarly acceptance gates.

## Exit Label

`P9_CHAPTERS_ACCEPTED` if the block is coherent and conservative.

`P9_SCHOLARLY_CHAPTERS_ACCEPTED` only if the integrated PDF chapter block
passes section-level and page-level hostile review and contains enough
substance for skeptical external review.
