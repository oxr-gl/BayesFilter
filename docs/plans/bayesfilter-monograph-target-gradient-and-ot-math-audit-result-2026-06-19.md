# Math-audit result: target/gradient and OT claim-tightening pass

**Date:** 2026-06-19  
**Artifact ID:** `bayesfilter-monograph-target-gradient-and-ot-math-audit-result-2026-06-19.md`

## Governing subplan

This result note closes the pass governed by:
- `docs/plans/bayesfilter-monograph-target-gradient-and-ot-math-audit-subplan-2026-06-19.md`

Parent governance remained:
- `docs/plans/bayesfilter-highdim-monograph-restart-execution-master-program-2026-06-18.md`

## What was tightened

### 1. HMC same-scalar target/gradient contract
Updated:
- `docs/chapters/ch03_hmc_target_requirements.tex`
- `docs/chapters/ch13_custom_gradient_wrappers.tex`
- `docs/chapters/ch14_derivative_validation.tex`

Main corrections:
- invalid-region fallback gradients are now required to be the exact derivative
  of the returned fallback scalar,
- constant low-density fallbacks are now explicitly required to have zero
  gradient,
- custom-gradient and validation language is now anchored to the full
  sampler-coordinate target rather than only a likelihood-only scalar,
- likelihood-only derivatives are now treated explicitly as component-level
  backend checks unless prior and transform-Jacobian terms are included.

### 2. Heuristic-vs-theorem discipline in the high-dimensional defect calculus
Updated:
- `docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex`

Main corrections:
- the particle-collapse section title was downgraded from theorem-strength to a
  log-weight-dispersion warning,
- the proposition and proof were reframed as a heuristic defect calculus rather
  than a general theorem of exponential collapse.

### 3. Brenier / Monge-gap claim discipline
Updated:
- `docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex`

Main corrections:
- the Brenier-map viewpoint now explicitly states that the classical theorem is a
  continuous-measure result with nontrivial assumptions,
- the chapter now distinguishes that theorem language from finite empirical-cloud
  implementation language,
- Monge-gap training is now stated as a practical surrogate/approximate objective
  unless the OT reference term estimator is specified more strongly.

## Verification

Rebuilt successfully:
- `docs/main.tex`

Result:
- `docs/main.pdf` builds cleanly after the math-audit edits.

## Pass/fail judgment against subplan criteria

### Passed
- The subplan was created and used as the governing artifact for this pass.
- `ch03/ch13/ch14` now state the HMC same-scalar contract more consistently.
- `ch38` no longer states the local particle-collapse warning more strongly than
  justified by its derivation.
- `ch32e` now states Brenier and Monge-gap claims with more explicit assumption
  and computational-status caveats.
- The monograph still compiles cleanly.

### Remaining outside the scope of this narrow pass
- full proof completion for Hessian/factor-derivative appendices,
- deeper symbolic verification of all nonlinear validation Jacobians,
- continuous-time Zakai/DMZ convention sharpening if a later pass wants to make
  the PDE side more theorem-complete,
- any broader direct-map OT benchmarking or implementation validation.

## Final judgment

This narrow math-audit pass removed the three highest-risk claim-discipline
mismatches identified in the first broad audit:
1. HMC same-scalar target/gradient inconsistency,
2. heuristic-vs-theorem mismatch in the particle-collapse warning,
3. under-specified Brenier / Monge-gap assumption language.

The monograph may still contain lower-priority proof-support or provenance gaps,
but the specific mathematically material claim-risk items targeted by this pass
have been tightened and are no longer active blockers at the same severity.
