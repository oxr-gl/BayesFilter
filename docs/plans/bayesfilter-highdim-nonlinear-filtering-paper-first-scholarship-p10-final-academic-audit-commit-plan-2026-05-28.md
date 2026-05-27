# P10 Final Critical Academic Review, Audit, And Commit Plan

## Objective

Perform the final academic-panel review and commit only if the rewritten block
is a serious paper-first scholarly artifact.

## Inputs

- P0-P9 result notes.
- Rewritten chapters.
- `docs/main.pdf`.
- Claude hostile review outputs.
- ResearchAssistant and MathDevMCP evidence records.

## Final Academic-Panel Questions

1. Does the block read like a monograph rather than an internal audit memo?
2. Are the required papers actually explained with equations and algorithms,
   not name-dropped?
3. Are derivations sufficient for a skeptical former professor?
4. Are synthesis propositions meaningful and defensible?
5. Are industrial limits explicit without becoming unsupported pessimism?
6. Are all no-overclaim boundaries preserved?

## Mandatory Final Hostile Review Loop

Launch Claude Code as a read-only final academic-panel reviewer.  Claude must
output `ACCEPT` or `REJECT` first.  Reject on any major source-fidelity,
derivation, citation, synthesis, PDF readability, or overclaim blocker.  Loop up
to 10 iterations.  On iteration 10, accept only minor editorial issues; stop for
any remaining major scholarly defect.

## Paper-By-Paper Completeness Audit

Before commit, produce an audit table with one row per required paper:

- P1 support class and local artifact path;
- inspected technical sections/equations/theorems/algorithms;
- chapter subsections consuming the paper;
- claims supported;
- derivations/proofs built from the source;
- unresolved blockers or forbidden claims.

No commit is allowed if a major chapter claim lacks a corresponding
`LOCAL_FULL_TEXT_CHECKED` row or explicit blocker.

## Final Validation

- `git diff --check`
- `python -c "import yaml; yaml.safe_load(open('docs/source_map.yml')); print('source_map ok')"`
- LaTeX build succeeds.
- No undefined citations/references for the rewritten block.
- Staged paths are allowed only.

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- final accepted chapter/PDF/source-map/bibliography files from the global
  allowed write set.

## Commit Policy

Commit only if the final audit passes:

`Rewrite high-dimensional nonlinear filtering chapters from primary literature`

## Stop Conditions

- Stop if any major source-fidelity, derivation, citation, synthesis, or PDF
  blocker remains.
- Stop if source intake is incomplete.
- Stop if unrelated dirty files would need staging.

## What Must Not Be Concluded

Even after commit, the chapters may define a research program and academic
synthesis only.  They do not validate BayesFilter production behavior,
posterior accuracy, NAWM readiness, HMC convergence, tensor-rank adequacy, or
GPU/XLA performance.
