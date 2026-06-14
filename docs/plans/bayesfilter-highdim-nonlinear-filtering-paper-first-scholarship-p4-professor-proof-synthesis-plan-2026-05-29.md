# P4 Professor-Proof Derivation And Industrial Synthesis Plan

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T/P1U literature ledgers, P2R rewrite artifacts, P3
industrial defect synthesis artifacts, `ch33`--`ch37`, `docs/references.bib`,
`docs/main.tex`, `docs/main.pdf`, and `docs/main.log`.

what_is_not_concluded: This plan does not conclude NAWM readiness, production
readiness, posterior accuracy, HMC convergence, tensor-method validation,
transport-method validation, broad GPU/XLA readiness, default readiness,
machine-certified proof validity, or exhaustive literature completeness.

## Purpose

The high-dimensional nonlinear filtering block is now paper-first and
industrial in tone, but it still has three review risks:

1. several derivations remain proof sketches rather than professor-proof
   derivations;
2. MathDevMCP evidence is diagnostic and must not be represented as
   certification;
3. `ch33`--`ch36` do not yet feed `ch37` strongly enough for the synthesis to
   feel earned.

P4 is a focused derivation-and-synthesis pass.  It strengthens the local
mathematics, records derivation obligations, adds defects passed forward from
each method chapter, upgrades the synthesis architecture, and adds one
controlled industrial-style worked example.  It does not rewrite the entire
literature survey and it does not add production claims.

The synthesis is lane-general but source-local.  Sparse grids, tensor methods,
transport maps, and HMC are treated because they are the inspected
high-dimensional nonlinear filtering families in this lane.  The architecture
does not claim to exhaust all possible high-dimensional methods.  Any method
outside the inspected source-supported families may be kept as defect-only,
background, omission-risk, or future work rather than promoted into a synthesis
proposition.

## Skeptical Plan Audit

The plan passes the pre-execution audit with the following guardrails.

- Wrong baseline risk: the baseline is not a weak particle filter or a
  marketing comparison.  The baseline is the exact filtering recursion and a
  block-local Gaussian scaffold used as a diagnostic object.
- Proxy metric risk: citation counts, venue rank, training loss, ESS, rank,
  runtime, finite smoke tests, and layout warnings are never promotion criteria
  for posterior accuracy or production readiness.
- Missing stop condition risk: stop if any chapter edit would require
  unsupported theorem claims, quarantined/retracted sources, production-code
  edits, DPF-lane edits, or unbounded literature expansion.
- Hidden assumption risk: every new proposition must state assumptions or be
  weakened to a diagnostic contract.
- Stale context risk: P1U source blockers remain active for Savostyanov-specific
  maxvol quasioptimality, Stroud/Genz/Smolyak originals, and Knothe priority.
  The rewrite must stay source-local to inspected alternatives.
- Source-support leakage risk: blocked originals, metadata-only records, and
  quarantined workshop sources may appear only as omission-risk or boundary
  context.  They may not support equations, theorem-level claims, worked-example
  decisions, or synthesis propositions.
- Environment mismatch risk: no GPU/CUDA or production benchmark is part of P4.
- Artifact adequacy risk: the deliverables are chapter text, derivation ledgers,
  MathDevMCP audit ledgers, Claude review ledgers, rebuilt PDF, and validation
  commands.  These artifacts answer the stated question better than smoke tests
  would.

## Evidence Contract

Scientific question: Can the high-dimensional nonlinear filtering block be made
more credible to skeptical former academics by expanding core derivations,
making method defects explicit before synthesis, and adding a controlled
industrial-style example without overclaiming?

Baseline or comparator: the P3 chapters and result note, which already contain
paper-first exposition and industrial defect calculus but still report compact
proof sketches, diagnostic-only MathDevMCP status, and compact `ch33`--`ch36`.

Primary pass criterion: each priority derivation obligation is either expanded
in the text, classified honestly in the P4 ledger, or weakened/removed; each of
`ch33`--`ch36` has a `Defects Passed To Synthesis` section; `ch37` contains an
explicit synthesis-contract architecture and a controlled worked example;
every major rewritten claim and every synthesis proposition has a claim-support
ledger entry tied to inspected technical source anchors or project derivation;
Claude accepts or remaining issues are minor after the bounded loop.

Veto diagnostics:

- unsupported theorem-level claim;
- quarantined/retracted source used as support;
- MathDevMCP diagnostic represented as certification;
- missing assumptions for a new proposition;
- HMC/tensor/transport/NAWM/production readiness overclaim;
- undefined citation/reference blocker in the rebuilt PDF;
- edit outside the allowed write set.

Explanatory diagnostics only: citation counts, venue rank, PDF layout warnings,
runtime impressions, method elegance, and local algebra checks that cover only
one equality.

Artifacts: this plan; `p4-derivation-obligation-ledger`; `p4-mathdevmcp-audit-ledger`;
`p4-industrial-worked-example-ledger`; `p4-claude-review-ledger`;
`p4-professor-proof-synthesis-result`; edited `ch33`--`ch37`; rebuilt
`docs/main.pdf`.

## Claim-Support Mapping Requirement

P4 must maintain a claim-support update inside the derivation obligation ledger
or result artifact.  Each major rewritten claim must be assigned one of:

- `PRIMARY_TECHNICAL_SUPPORT`;
- `PROJECT_DERIVATION`;
- `SURVEY_CONTEXT_ONLY`;
- `SOURCE_GAP_BLOCKER`;
- `QUARANTINED`;
- `REMOVE_OR_WEAKEN`.

The support field must name the inspected source section/equation/theorem/proof
or the P4 project derivation.  No abstract, introduction, conclusion, citation
count, venue rank, metadata record, blocked original, or quarantined source may
serve as theorem support.

## Allowed Writes

- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
- `docs/main.pdf`
- `docs/references.bib` only if a required cited source is missing
- `docs/source_map.yml` only if provenance changes
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p4-*`

Forbidden writes include production `bayesfilter/`, DPF implementation lane,
student-baseline files, controlled-DPF files, public APIs, and `.local_sources/`
commits.

Any new theorem-level, algorithm-level, or worked-example decision claim must
be supported by an inspected source anchor already recorded in the P1R--P1U
ledgers or by a project derivation recorded in the P4 claim-support material.
Blocked and quarantined sources are forbidden as claim support.

## Stop Conditions

Stop and report `BLOCKED` or `PARTIAL_READY_WITH_BLOCKERS` if:

- a priority derivation cannot be made honest without a missing source;
- Claude identifies a major unsupported claim that cannot be repaired within
  the five-iteration cap;
- LaTeX cannot build the PDF;
- new undefined citations/references remain in the high-dimensional block;
- MathDevMCP failures are being tempted into false certification language;
- the required edits would leave the high-dimensional lane.

## Derivation Obligation Ledger Schema

Each row records:

`obligation_id`, `chapter`, `label_or_location`, `claim`, `support_status`,
`classification`, `assumptions_needed`, `planned_action`, `text_status`,
`mcp_status`, `source_anchor`, `remaining_gap`.

Allowed classifications:

- `FULL_DERIVATION_READY`
- `PROOF_SKETCH_ONLY`
- `SOURCE_THEOREM_ONLY`
- `MCP_UNVERIFIED`
- `NEEDS_ASSUMPTIONS`
- `REMOVE_OR_WEAKEN`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

Priority obligations:

- filtering recursion and likelihood identities;
- predictive score identity;
- Zakai/KS/DMZ and pathwise robust DMZ transformations;
- Gaussian projection, covariance update, and quadrature exactness;
- particle-collapse/log-weight variance;
- transport change-of-variables and support correction;
- TT rank, mass, positivity, and PSD semantic failures;
- HMC same-scalar and Jacobian target contracts;
- synthesis propositions in `ch37`.

The initial `ch37` proposition obligations are:

| obligation_id | planned proposition | support mode | required assumptions | veto/repair rule |
|---|---|---|---|---|
| `P4-SYN-1` | block-local Gaussian scaffold is a diagnostic baseline, not a truth model | `PROJECT_DERIVATION` plus source-local Gaussian projection/Kalman support | finite second moments, nonsingular innovation block, declared block partition | weaken if stated as accuracy or production readiness |
| `P4-SYN-2` | sparse-grid/high-degree cubature is promoted only after local active dimension is bounded | `PROJECT_DERIVATION` plus Jia/Julier/Arasaratnam/Singh source-local rules | smooth local block map, bounded block dimension, checked point budget | remove if it implies global sparse-grid default |
| `P4-SYN-3` | TT/TN filters require rank stability and probability/covariance semantic checks | `PROJECT_DERIVATION` plus Oseledets, Oseledets--Tyrtyshnikov, Zhao--Cui, Menzen source anchors | stable rank diagnostic, density mass/positivity checks or PSD/factor checks | weaken if it implies general TT validation |
| `P4-SYN-4` | transports are useful only with correction/Jacobian/support auditability | `PROJECT_DERIVATION` plus Rosenblatt, Parno, Hoffman, Spantini 2022 source anchors | differentiable/invertible or source-specific deterministic map, finite Jacobian, support coverage | remove if it relies on quarantined Spantini 2016 workshop paper |
| `P4-SYN-5` | HMC is downstream of the scalar filter target contract | `PROJECT_DERIVATION` plus Neal/NUTS/Betancourt/RMHMC/NeuTra source anchors | finite scalar value, gradient of same scalar, valid transform/Jacobian | weaken if it claims convergence or exact posterior for approximate filter |
| `P4-SYN-6` | performance claims are invalid until defect vetoes pass | `PROJECT_DERIVATION` from preceding diagnostic contracts | explicitly declared validity gates and performance metric | remove if speed is treated as validity evidence |
| `P4-SYN-7` | useful non-novel synthesis is acceptable when every handoff exports a diagnostic | `PROJECT_DERIVATION` and industrial contract reasoning | each component's residual is observable and used by the next stage | weaken if presented as academic novelty |

Every row above must be copied or summarized in the P4 derivation/claim-support
ledger with final text status and any MathDevMCP status.

## MathDevMCP Obligation-Splitting Protocol

Do not ask MathDevMCP to certify broad industrial propositions.  Split
obligations into narrow checks:

- algebraic equalities, such as lognormal moment ratios;
- covariance PSD counterexamples;
- Gaussian projection residual covariance identities;
- change-of-variable identities at symbolic/scalar level;
- finite-difference scalar-gradient parity identities;
- score/log-normalizer identities under declared dominated differentiation.

Record statuses as:

- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

The chapter text must state that MathDevMCP diagnostics are audit aids rather
than theorem certification.

## Chapter Rewrite Scope

### `ch33`

Add fuller derivations for the Bayes prediction/update recursion, likelihood
factorization, predictive score identity, and scalar-target boundary.  Add
`Defects Passed To Synthesis`: exact target versus approximate target,
normalization/mass, source-local PDE assumptions, and likelihood contract.

### `ch34`

Expand the affine Gaussian projection proof into a stepwise derivation, add a
quadratic one-dimensional example showing Gaussian projection can be exact for
linear observations and biased for nonlinear likelihoods, and add `Defects
Passed To Synthesis`: projection bias, quadrature remainder, PSD/factor
failure, block dimension, and point-count controls.

### `ch35`

Replace the particle-collapse proof sketch with a fuller lognormal/ESS
calculation and add semantic failure derivations for transport support and
tensor/covariance compression.  Add `Defects Passed To Synthesis`: particle
collapse, correction/support, TT rank/positivity/mass, square-root PSD gates,
and map monotonicity/Jacobian auditability.

### `ch36`

Expand same-scalar and Jacobian-target derivations.  Add a scalar parity
diagnostic and `Defects Passed To Synthesis`: value-gradient mismatch, invalid
transforms/support, approximate filter target, diagnostics-before-speed, and
acceleration limits.

### `ch37`

Upgrade the synthesis into a synthesis-contract architecture chapter.  Add
propositions and proof sketches for block scaffold, sparse-grid diagnostic
promotion, tensor viability, transport auditability, HMC downstream use,
performance claims after defect vetoes, and useful non-novel composition.  Add
one stylized macro-finance worked example with explicit dimensional variables
and no NAWM/production claim.

## Controlled Industrial-Style Worked Example Scope

The example must be stylized and analytically transparent:

- block state vector split into macro, financial, latent-volatility, and
  measurement blocks;
- nonlinear observation such as a logistic/stress measurement or quadratic
  risk indicator;
- Gaussian scaffold equations and innovation/PSD diagnostics;
- particle-collapse calculation using an effective observation dimension;
- sparse-grid local diagnostic on a bounded block;
- TT/transport/HMC scoping decision tied to rank, support/Jacobian, and
  same-scalar diagnostics;
- explicit statement that the example is not NAWM validation, client model
  validation, posterior accuracy evidence, production readiness, or validated
  method selection.

## Claude Review Loop

Plan review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-p4-professor-proof-plan-review-iter<N> --model sonnet --effort high "<bounded hostile plan review prompt>"
```

Execution review by block or tightly coupled block group:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-p4-professor-proof-block<BLOCK>-review-iter<N> --model sonnet --effort high "<bounded hostile academic/industrial review prompt>"
```

Claude must output `ACCEPT` or `REJECT` first.  Codex audits Claude findings
and remains final authority.  Loop up to five iterations per plan/block.  On
iteration five, accept only if all remaining issues are minor editorial or
layout issues; stop for major derivation, source-support, overclaim, or PDF
blockers.

## Validation Requirements

Run:

```bash
git diff --check
git status --short
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/main.tex
pdftotext docs/main.pdf - | rg -n "Defects Passed To Synthesis|Synthesis Architecture|Controlled Industrial-Style Worked Example|MathDevMCP|Professor-Proof"
rg -n "undefined|Citation .* undefined|Reference .* undefined|There were undefined|Rerun to get cross-references|Rerun to get outlines" docs/main.log
```

Also verify:

- `latexmk` exits successfully;
- undefined citations, undefined references, and unresolved rerun warnings are
  vetoes;
- layout warnings are explanatory only unless they obscure the audited P4
  sections or make mathematical displays unreadable;
- only allowed paths changed intentionally;
- `.local_sources/` remains untracked and unstaged;
- every major derivation obligation has a ledger status;
- the Spantini et al. 2016 decomposable-transport workshop source remains
  quarantined and unused as support;
- source blockers remain explicit where not closed;
- Claude `ACCEPT` or structured blocker is recorded.

## What Must Not Be Concluded

P4 must not conclude that:

- the block is a machine-verified theorem artifact;
- all derivations are paper-length proofs;
- the literature survey is exhaustive;
- any method is validated for NAWM or client models;
- HMC, RMHMC, NUTS, NeuTra, tensor, transport, sparse-grid, or particle methods
  are production-ready defaults;
- posterior accuracy, convergence, GPU/XLA readiness, or industrial deployment
  is established.

The intended conclusion is narrower: the chapters have a stronger,
source-local, derivation-forward, industrially useful defect-and-synthesis
argument ready for user review, with residual gaps explicitly recorded.
