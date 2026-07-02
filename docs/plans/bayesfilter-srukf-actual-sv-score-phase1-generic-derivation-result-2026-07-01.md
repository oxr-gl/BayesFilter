# Phase 1 Result: Generic SR-UKF Derivation

Date: 2026-07-01

Status: PASS_PHASE1_GENERIC_DERIVATION

## Objective

Patch the LaTeX document with a generic factor-propagating SR-UKF value and
first-derivative score derivation that does not rely on strict-SPD
principal-square-root derivatives.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the LaTeX state a generic factor-propagating SR-UKF analytical score backend independent of strict-SPD principal-root derivatives? |
| Baseline/comparator | Existing `ch17` square-root contract, `ch12` factor derivative contract, and current `ch18` strict-SPD principal-root section as non-target comparator. |
| Primary criterion | Passed for Phase 1. The derivation defines factor placement, fixed-branch derivatives, signed moment factors, reconstruction contracts, solve-form likelihood/score, filtered-state handoff, and admission boundaries. |
| Veto diagnostics | No principal-root/Sylvester derivative is used as the generic SR-UKF derivative path; no hidden covariance/eigendecomposition score route is admitted; no leaderboard/HMC/exact-likelihood claim is made. |
| Explanatory diagnostics | Detailed QR/update primitive proofs are deferred to `ch12` and must be part of Phase 2 audit. |
| Not concluded | No actual-SV adapter derivation, implementation correctness, numerical correctness, leaderboard admission, or HMC readiness is concluded. |

## LaTeX Artifact

Patched file:

- `docs/chapters/ch17_square_root_sigma_point.tex`

New section:

- `Factor-Propagating SR-UKF Score Contract`

Key labels:

- `sec:bf-srukf-factor-propagating-score-contract`
- `eq:bf-srukf-factor-placement`
- `eq:bf-srukf-factor-placement-first`
- `eq:bf-srukf-weighted-moment-factor`
- `eq:bf-srukf-propagated-point-first`
- `eq:bf-srukf-moment-mean-first`
- `eq:bf-srukf-moment-covariance-first`
- `eq:bf-srukf-factor-reconstruction-first`
- `eq:bf-srukf-innovation-factor`
- `eq:bf-srukf-loglik-solve`
- `eq:bf-srukf-score-first`
- `eq:bf-srukf-gain-first`
- `eq:bf-srukf-filtered-mean-first`
- `eq:bf-srukf-filtered-factor`
- `eq:bf-srukf-filtered-factor-first`
- `sec:bf-srukf-admission-boundary`

## Checks Run

Local checks:

```text
rg -n "eq:bf-srukf-factor-placement|eq:bf-srukf-factor-placement-first|eq:bf-srukf-weighted-moment-factor|eq:bf-srukf-propagated-point-first|eq:bf-srukf-moment-mean-first|eq:bf-srukf-moment-covariance-first|eq:bf-srukf-factor-reconstruction-first|eq:bf-srukf-innovation-factor|eq:bf-srukf-loglik-solve|eq:bf-srukf-score-first|eq:bf-srukf-gain-first|eq:bf-srukf-filtered-mean-first|eq:bf-srukf-filtered-factor|eq:bf-srukf-filtered-factor-first" docs/chapters/ch17_square_root_sigma_point.tex
rg -n "principal|GradientTape|autodiff|SVD|eigenderivative|strict-SPD|exact|HMC|leaderboard|not the generic SR-UKF|must not" docs/chapters/ch17_square_root_sigma_point.tex
git diff --check -- docs/chapters/ch17_square_root_sigma_point.tex
```

Outcome:

- Labels found.
- Forbidden-route and nonclaim language found.
- `git diff --check` passed.

MathDevMCP readiness checks:

- `latex_label_lookup` succeeded for:
  - `eq:bf-srukf-score-first`
  - `eq:bf-srukf-factor-reconstruction-first`
  - `eq:bf-srukf-gain-first`
  - `eq:bf-srukf-factor-placement`
- `typed_obligation_label` returned `status: consistent` for:
  - `eq:bf-srukf-score-first`
  - `eq:bf-srukf-gain-first`
  - `eq:bf-srukf-factor-reconstruction-first`
  - `eq:bf-srukf-factor-placement`

Claude review:

- `docs/plans/bayesfilter-srukf-actual-sv-score-claude-review-ledger-2026-07-01.md`
- Verdict: `VERDICT: AGREE`

## Skeptical Audit Result

- Wrong baseline: avoided by contrasting the generic backend with the current
  KSC strict-SPD principal-root route and historical SVD route.
- Proxy metric promotion: no numerical metric used in Phase 1.
- Missing stop conditions: branch changes, downdate failure, singular innovation
  likelihood without reviewed branch, and forbidden provenance are stop/admission
  blockers.
- Hidden assumptions: fixed rank, pivot, sign, offset, support, and
  update/downdate branch assumptions are stated.
- Environment mismatch: no runtime/GPU command was used.
- Artifact mismatch: the derivation artifact directly answers Phase 1's
  documentation question.

## Phase 2 Handoff

Phase 2 may begin.

Required Phase 2 subplan:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase2-generic-audit-subplan-2026-07-01.md`

Phase 2 must perform the deeper MathDevMCP and Claude audit of the generic
derivation, including the deferred QR/update primitive relationship to `ch12`.

## Stop/Handoff Status

No human-required blocker is present at the end of Phase 1.
