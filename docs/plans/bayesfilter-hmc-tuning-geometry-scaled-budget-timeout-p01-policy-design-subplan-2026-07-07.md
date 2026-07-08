# Phase 1 Subplan: Central Geometry-Scaled Budget And Progress Policy Design

Date: 2026-07-07

Status: `DRAFT_PHASE_SUBPLAN`

## Phase Objective

Design one BayesFilter-owned policy that derives HMC tuning sample budgets,
attempt budgets, progress/stall rules, and emergency wall-clock caps from model
dimension, mass/covariance geometry, stage role, observed throughput, and
meaningful repair progress.

## Entry Conditions

- Phase 0 result is `PASSED_WITH_REPAIR_TARGETS`.
- Active path is BayesFilter `hmc_kernel_tuning.py`.
- No active NUTS path was found.
- MacroFinance-local HMC tuning authority was not found in the checked CCMA
  path.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-p01-policy-design-result-2026-07-07.md`
- Updated ledger:
  `docs/plans/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-visible-execution-ledger-2026-07-07.md`
- Phase 2 implementation subplan draft.

## Required Checks

- Review active payloads and dataclasses around:
  `_HMCAttemptBudgetPolicy`, `_default_attempt_budget_policy`,
  `_public_budget_policy_factory`, `_public_bootstrap_config`,
  `HMCStagedTimeoutPolicy`, and progress payload helpers.
- Identify what mass/covariance information is already available in
  `PrecomputedMassArtifact` payloads without exposing private arrays.
- Check public payload redaction requirements before proposing any event fields.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What central policy should replace scattered sample/time constants? |
| Baseline/comparator | Phase 0 inventory of current split policies and literal constants. |
| Primary pass criterion | Result specifies policy inputs, formulas, public rationale payloads, tests, and implementation touch points without adding new arbitrary active defaults. |
| Veto diagnostics | Design uses NUTS; design creates MacroFinance-owned tuning logic; design treats smoke counts as tuning evidence; design cannot stop no-progress runs; design kills slow-but-progressing runs by hard timeout; design leaks private mass/sample/kernel mechanics. |
| Explanatory diagnostics | Candidate formulas, role labels, caps, uncertainty intervals, geometry metrics, and event names. |
| Not concluded | No implementation correctness, no tuned CCMA result, no posterior convergence, no sampler superiority, no production readiness. |

## Design Requirements

The design must separate:

- sample budget: how much evidence each stage needs;
- progress monitor: whether declared work is moving;
- emergency cap: generous machine protection only.

The design must include:

- dimension `d`;
- covariance/mass condition number `kappa`;
- effective dimension `d_eff = (sum(lambda))^2 / sum(lambda^2)`;
- regularization pressure: eigenvalue floor/clipping and shrinkage indicators;
- stage role: smoke, diagnostic, tuning evidence, verification;
- acceptance uncertainty using a binomial/Wilson-style interval or an explicit
  conservative equivalent;
- adaptive doubling when uncertainty overlaps a decision boundary, subject to
  stage role and cap;
- attempt rule: at least 5 attempts for serious/default tuning and extension
  toward 10 only while meaningful repair progress is present;
- timing rule: expected stage duration from observed throughput and planned
  work, no-progress stall detection from missing events/completed batches, and
  a generous emergency cap recorded as machine protection.

## Forbidden Claims And Actions

- Do not implement code in Phase 1.
- Do not claim formulas are statistically optimal.
- Do not claim any sample count proves posterior convergence.
- Do not expose private mass matrices, samples, candidate grids, or step sizes
  in public artifacts.
- Do not add or recommend NUTS.

## Skeptical Plan Audit

- Wrong baseline: Phase 1 uses Phase 0 inventory, not old docs.
- Proxy metric risk: acceptance screens remain tuning diagnostics only; Phase 1
  must not make them posterior-validity criteria.
- Missing stop condition: no-progress and emergency-cap stops must be explicit.
- Hidden assumption: condition number alone is not geometry.  Design must also
  use effective dimension and regularization pressure, and leave room for
  acceptance uncertainty.
- Environment mismatch: design only writes docs; implementation is Phase 2.
- Artifact mismatch: result must specify implementation touch points and tests,
  not just prose.

## BayesFilter Usage Audit

All generic policy design belongs in BayesFilter.  MacroFinance may request a
named policy or pass model dimensions/geometry through BayesFilter but must not
derive tuning budgets locally.

## No-NUTS Audit

The design must remain fixed-trajectory HMC.  NUTS may appear only as a
forbidden/non-default reference in documentation.

## Next-Phase Handoff Conditions

Advance to Phase 2 only if the Phase 1 result names:

- new or modified BayesFilter dataclasses/helpers;
- exact source sections to edit;
- public/private payload rules;
- tests to add/update;
- acceptance-uncertainty and geometry-scaling formulas;
- timing/progress policy formulas and emergency cap semantics.

## Stop Conditions

Stop if no public-safe geometry summary can be obtained from existing artifacts,
if the design requires MacroFinance-local tuning derivation, if policy formulas
depend on raw private mass arrays in public payloads, or if review finds the
new formulas are just renamed magic numbers without provenance.
