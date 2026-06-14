# Claude P3 Block Review Prompt

You are a read-only hostile academic/industrial reviewer.  Codex is supervisor
and final authority.  Do not edit files.  Do not commit.  Do not run network
tools.

First line of your response must be exactly `ACCEPT` or `REJECT`.

Review these artifacts:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p3-industrial-defect-synthesis-plan-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p3-industrial-defect-synthesis-ledger-2026-05-29.md`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
- `docs/references.bib`

Use the shared scholarly policy:

- `/home/chakwong/python/claudecodex/policies/scholarly-literature-audit-policy.md`

The chapter must satisfy the eight P3 blocks below.  Give a separate
`ACCEPT`/`REJECT` verdict for every block A--H.  Reject the whole artifact if
any block has a major blocker.

## Block A: Derivation Depth And MCP Honesty

Check whether the chapter admits that several derivations are monograph proof
sketches rather than full paper-level derivations, and that MathDevMCP
diagnostics are not machine certification.

## Block B: Likely Defects And Counterexamples

Check whether the chapter mathematically derives likely defects rather than
using vague prose: particle collapse, Gaussian projection loss, tensor rank or
semantic loss, transport target/support failure, and HMC target mismatch.

## Block C: Mitigation Derivations

Check whether each mitigation is tied to a mathematical contract or diagnostic:
ESS/log-weight variance, block-local active dimension, mass/positivity/PSD,
Jacobian/support correction, scalar-gradient parity, and validity-before-speed.

## Block D: Industrial Synthesis Propositions

Check whether the propositions are meaningful and defensible:

- TT methods are viable only when economic block structure induces stable ranks.
- Transport maps are useful only when geometry improves without destroying
  target auditability.
- HMC belongs downstream of a same-scalar likelihood contract.
- Sparse-grid/high-degree cubature belongs first as local diagnostic.
- Non-novel compositions can be industrially superior when every handoff has a
  defect variable and veto.

## Block E: Numerical Problems And Mitigation Equations

Check the numerical table and examples for underflow, innovation conditioning,
PSD loss, tensor density drift, transport support mismatch, and HMC scalar
mismatch.

## Block F: Performance Model Equations

Check the performance table and sparse-grid scaling note.  Reject if it treats
smoke tests, speed, or proxy timing as evidence of posterior accuracy or
production readiness.

## Block G: Literature Coverage And Source-Risk Honesty

Check whether source support is primary-source-grounded, quarantined/retracted
sources are not used, citation counts/venue ranks are not used as truth
evidence, and omitted/source-risk papers are explicit.

## Block H: PDF/Layout/Integration Readiness

Check whether the source is likely to build cleanly in LaTeX and whether layout
or PDF warnings are separated from mathematical/citation blockers.  You cannot
inspect a rendered PDF unless Codex supplies it later, so mark this block
`ACCEPT_WITH_SOURCE_ONLY_LIMIT` if the source is sound but rendered PDF still
needs validation.

## Review Criteria

Reject for:

- unsupported theorem-level claims;
- hidden production, NAWM, HMC convergence, tensor validation, posterior
  accuracy, broad GPU/XLA readiness, or default-readiness claims;
- BayesFilter evidence clutter in the main mathematical flow;
- source-blocked or quarantined papers used as support;
- prose where the user asked for mathematical derivation, counterexample,
  diagnostic variable, or performance equation;
- severe LaTeX integration risks.

If `REJECT`, list findings by severity with path and smallest repair.  If
`ACCEPT`, list residual risks and limits.
