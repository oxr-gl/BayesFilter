# Monograph Target/Gradient and OT Math Audit Subplan

**Date:** 2026-06-19  
**Program ID:** `bayesfilter-monograph-target-gradient-and-ot-math-audit-subplan-2026-06-19.md`

## Purpose

This subplan governs the current narrow mathematical-audit pass on the BayesFilter
monograph after the high-dimensional restart/cutover stream has already been
stabilized and canonically promoted.

The purpose is not to reopen chapter topology or the high-dimensional cutover.
It is to tighten mathematically material claim/contract language in a small set
of chapters where the broad monograph audit found real risk of mismatch between:
- exact target vs approximate target,
- value scalar vs derivative scalar,
- theorem-strength vs heuristic-strength wording,
- continuous-measure theorem language vs empirical-cloud implementation language.

## Parent governance

This subplan inherits anti-drift discipline from:
- `docs/plans/bayesfilter-highdim-monograph-restart-execution-master-program-2026-06-18.md`

It does **not** replace that program.  It is a narrow execution subplan for the
current mathematical-audit cleanup pass.

## Scope

### In scope
- `docs/chapters/ch03_hmc_target_requirements.tex`
- `docs/chapters/ch04_bayesfilter_api.tex`
- `docs/chapters/ch13_custom_gradient_wrappers.tex`
- `docs/chapters/ch14_derivative_validation.tex`
- `docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex`
- `docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex`

### Out of scope
- monograph topology changes,
- new chapter additions/splits/merges,
- production code changes,
- broad rewrite of low-risk chapters,
- full proof completion for the Hessian/factor-derivative appendices,
- reopening the high-dimensional canonical cutover judgment.

## Chapter-by-chapter status at subplan start

### Already addressed in the current pass
- `ch03`: invalid-region fallback gradients tightened to obey same-scalar HMC logic.
- `ch13`: custom-gradient same-scalar contract rewritten in sampler coordinates.
- `ch14`: derivative validation rewritten to compare the full sampler-coordinate target.
- `ch38`: particle-collapse section downgraded from theorem-strength to heuristic-strength wording.

### Remaining live target
- `ch32e`: Brenier-map and Monge-gap claims still need stronger assumption and computational-status language.

## Evidence contract

### Question
Are Brenier-map and Monge-gap claims in `ch32e` stated with assumptions and
computational-status language strong enough to be mathematically defensible?

### Baseline / comparator
- the current `ch32e` text,
- the chapter’s cited OT/Brenier interpretation,
- the monograph’s same-scalar and target-contract discipline already established
  in `ch03`, `ch13`, and `ch14`.

### Primary pass criterion
The chapter no longer states theorem-strength claims without the needed
assumptions, and no training objective is described more strongly than its
computational definition justifies.

### Veto diagnostics
The pass is not successful if any of the following remain true after the edit:
1. continuous-measure Brenier-map theorem language is still written as if it
   automatically applies to arbitrary empirical finite-cloud transport problems,
2. the chapter still blurs continuous-measure theorem language and empirical-cloud
   implementation language without warning,
3. an approximate Monge-gap training objective is still written as if it were the
   exact mathematical objective without computational qualification,
4. the chapter implies direct learned maps are already production-ready,
   HMC-ready, or equivalent to retained-teacher EOT acceleration.

### What will not be concluded
This pass will **not** conclude:
- that direct learned maps are production-ready,
- that direct learned maps are HMC-safe,
- that Brenier/ICNN structure is exact for arbitrary finite-cloud empirical OT,
- that Monge-gap training is exact rather than surrogate unless separately proven.

## Execution steps

1. Write this subplan.
2. Tighten `ch32e` in three places:
   - Brenier-map viewpoint assumptions,
   - ICNN/direct-map theorem-vs-implementation language,
   - Monge-gap computational-status language.
3. Rebuild `docs/main.tex`.
4. Record a short result note under `docs/plans`.

## Success criteria

This subplan is successful when:
1. the subplan exists and clearly scopes the pass,
2. `ch32e` explicitly states the assumptions behind Brenier-map language,
3. `ch32e` clearly distinguishes continuous-measure theorem language from
   empirical-cloud implementation language,
4. `ch32e` clearly states that practical Monge-gap training uses an approximate
   or surrogate estimator unless otherwise proven,
5. `docs/main.tex` builds successfully,
6. the resulting open mathematical issues are reduced to lower-priority
   proof-support/provenance items rather than active claim-risk items.

## Expected artifacts

- governing subplan:
  - `docs/plans/bayesfilter-monograph-target-gradient-and-ot-math-audit-subplan-2026-06-19.md`
- result note:
  - `docs/plans/bayesfilter-monograph-target-gradient-and-ot-math-audit-result-2026-06-19.md`
