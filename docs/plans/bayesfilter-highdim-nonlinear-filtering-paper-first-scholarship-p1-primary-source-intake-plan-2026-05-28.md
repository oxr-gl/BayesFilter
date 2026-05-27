# P1 Primary-Source Intake And Citation Ledger Plan

## Objective

Build a primary-source ledger for the required papers.  This phase decides
whether chapter execution is allowed or blocked pending source intake.

## Inputs

- Required URL list in the master program.
- `docs/references.bib`.
- `docs/source_map.yml`.
- ResearchAssistant MCP local summaries and source records, read-only.
- Any local source packages already present in `.research/` or local paper
  caches.

## Source-Support Classes

- `LOCAL_FULL_TEXT_CHECKED`: primary text is locally available and technical
  sections/equations have been inspected.
- `LOCAL_SUMMARY_ONLY`: ResearchAssistant summary exists, but no technical
  full-text inspection was performed.
- `METADATA_ONLY`: title/URL known, no technical support.
- `NEEDS_NETWORK_INTAKE`: source must be fetched from the exact public URL.
- `PAYWALL_OR_ACCESS_BLOCKED`: source cannot be inspected without access.

## Work

1. Query ResearchAssistant for each required paper.
2. Search local source caches and `docs/references.bib`.
3. Create a citation ledger with the required schema:
   - title and authors;
   - stable URL, DOI, arXiv id, or journal landing page;
   - support class;
   - local artifact path for full text or source package;
   - inspected technical section numbers;
   - inspected equation, theorem, proposition, algorithm, table, and appendix
     identifiers where available;
   - intended chapter consumers;
   - claims allowed from the paper;
   - claims forbidden or unresolved blockers.
4. If any required paper is not `LOCAL_FULL_TEXT_CHECKED`, create a bounded
   source-intake request listing exact URLs and stop execution before chapter
   rewrite.
5. Add bibliography entries only after primary source identity is checked; do
   not invent bib metadata from memory.

## Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-primary-source-ledger-2026-05-28.md`
- Optional source-intake approval request note under the same prefix.

## Stop Conditions

- Stop if source text is unavailable for any paper required by a chapter rewrite.
- Stop if network access is needed; ask the user for approval for exact URLs.
- Stop if only abstracts or metadata are available for a theorem-level claim.

## Verification

- ResearchAssistant MCP query log recorded in result note.
- `rg` checks for bibliography keys after any bib update.
- `git diff --check`

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- `docs/references.bib` only after full-text identity is checked.

No chapter, PDF, source-map, production, DPF, student-baseline, or
controlled-DPF edits are authorized by P1 unless a separate reviewed source
identity update explicitly permits them.

## What Must Not Be Concluded

P1 does not summarize papers from abstracts.  It only records source status and
permits or blocks later derivation work.
