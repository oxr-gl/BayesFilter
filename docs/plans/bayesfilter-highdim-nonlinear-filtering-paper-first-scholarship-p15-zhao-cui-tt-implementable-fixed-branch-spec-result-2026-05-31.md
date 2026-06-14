# P15 Implementable Fixed-Branch Spec Result

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," FoCM 2022.
- P10-P14 BayesFilter Zhao-Cui TT artifacts.

what_is_not_concluded:
- No posterior accuracy claim.
- No global derivative claim for adaptive TT-cross or rank-changing code.
- No HMC convergence claim.
- No production BayesFilter implementation.
- No default-method recommendation.
- No numerical validation on the target high-dimensional model.

## Decision

`P15_ACCEPTED_FIXED_BRANCH_IMPLEMENTABILITY_SPEC`

## Artifacts

- Note: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-note-2026-05-31.tex`
- PDF: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-note-2026-05-31.pdf`
- Reference example: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-fixed-branch-minimal-example-2026-05-31.py`
- Ledgers: P15 `*.md` files under `docs/plans/`.

## Claude History

- Plan iter1: `REJECT`; Codex classified all six findings `ACCEPT` and patched plan.
- Plan iter2: `ACCEPT`.
- Execution iter1: `REJECT`; Codex classified all five findings `ACCEPT` and patched note, example, and ledgers.
- Execution iter2: `ACCEPT`.

## MathDevMCP Status

- `MCP_VERIFIED`: normalized-density algebra and defensive marginal mass identity.
- `MCP_TOOL_LIMIT` / `MCP_UNVERIFIED`: derivative notation and symbolic-assumption substitution forms.
- Overall: broad TT filtering proof is human-derived, not machine-certified.

## Reference Example

Two-step scalar nonlinear filtering example passed same-scalar finite-difference parity:

```text
ell=-0.569442222488
grad=-1.00473154806
min_parity_relerr=7.604872e-12
P15_REFERENCE_EXAMPLE_PASS
```

The example carries the saved step-1 filter and derivative evaluator into step 2.

## Validation Commands Run

```text
python docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-fixed-branch-minimal-example-2026-05-31.py
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-note-2026-05-31.tex
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-*
pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-note-2026-05-31.pdf - | rg -n "Fixed-Rank Ridge ALS|Mass Matrices|Marginalization In Squared-TT Form|Same-scalar|Minimal Runnable Example|prefix|suffix|two-step|saved filter"
rg -n "undefined|Rerun|Warning: Citation|Warning: Reference|Label\(s\) may have changed" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-note-2026-05-31.log
```

## Residual Risks

- Fixed-branch specification only; no adaptive TT-cross/rank-changing derivative.
- Same-scalar parity and derivation do not prove posterior accuracy.
- Toy example is low-dimensional and rank-one; it does not show high-dimensional robustness.
- Literature metadata and forward snowballing were not freshly queried; no literature completeness claim.

## Panel Probability Estimate

Estimated probability that this P15 note passes a skeptical mixed numerical/chemistry panel as a self-contained fixed-branch implementation specification: `0.72`.
