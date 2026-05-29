# P9 Ch34 Implementability And Fixed-SGQF Gradient Plan

Date: 2026-05-30

metadata_date: 2026-05-30

seed_papers: P8 rewritten `ch34`, P8 source/gradient/anchor/MCP/Claude ledgers,
Julier--Uhlmann 1997, Arasaratnam--Haykin 2009, Jia--Xin--Cheng 2012,
Jia--Xin--Cheng 2013, Singh et al. 2018, `ch18_svd_sigma_point.tex`, local
source cache under `.local_sources/highdim_nonlinear_filtering/`, and the
scholarly literature audit policy.

what_is_not_concluded: This plan does not conclude exact posterior accuracy,
HMC convergence, production readiness, NAWM readiness, GPU/XLA readiness,
default readiness, broad machine-certified mathematics, or exhaustive
literature coverage.  Source-scope boundaries are not counted as P9 blockers
unless they block the requested implementability standard.

## Objective

Rewrite only `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex` so
the GHQF, SGQF, and ASGHF sections pass this implementability test:

> If the chapter is given to Codex alone, Codex should be able to implement the
> algorithm and the selected analytical gradient for a high-dimensional
> nonlinear state-space model without opening the papers again.

The selected high-dimensional approximate likelihood target is a fixed-index
sparse-grid Gauss--Hermite Gaussian projection filter.  Tensor-product GHQF is
the transparent reference construction.  ASGHF is an adaptive offline
grid-selection mechanism and becomes HMC-usable only after the selected index
set, nodes, and weights are frozen.

## Skeptical Plan Audit

The P8 text improved source fidelity but still fails the real blocker.  A
reader can see what GHQF, SGQF, and ASGHF are, but cannot implement a full
filter step or an algorithm-specific score recursion without reconstructing
missing details.  The wrong plan would add more explanatory paragraphs while
leaving the algorithm unspecified.  P9 therefore makes pseudocode, inputs,
outputs, node/weight construction, moment equations, fixed-branch diagnostics,
and the fixed-SGQF score recursion the primary acceptance criteria.

The plan also avoids a hidden baseline error: tensor-product GHQF is not the
high-dimensional proposal.  It is the reference from which sparse-grid
replacement is explained.  The high-dimensional target is fixed SGQF, and ASGHF
is a way to choose a grid before freezing it.

## Evidence Contract

- Question: Can `ch34` now specify GHQF, fixed SGQF, ASGHF grid selection, and
  the fixed-SGQF approximate likelihood gradient at implementation level?
- Baseline: P8 `ch34`.
- Primary pass criterion: a hostile reviewer can answer yes to all four
  implementability questions: GHQF filter step, SGQF grid construction/filter
  step, ASGHF adaptive grid selection plus frozen-grid filtering, and fixed-SGQF
  likelihood score recursion.
- Veto diagnostics: missing node/weight construction, missing prediction/update
  recursion, missing likelihood scalar, missing gradient state recursion,
  unclear HMC label, source claim unsupported by checked anchor, or PDF/citation
  build blocker.
- Explanatory diagnostics: layout warnings, nonblocking typography warnings,
  and source-history scope notes.
- Artifact: this plan, rewritten `ch34`, P9 ledgers, Claude review ledger,
  MathDevMCP ledger, P9 result note, and rebuilt `docs/main.pdf`.

## Allowed Writes

- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/main.pdf`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p9-ch34-*`

No other chapter should be edited unless a broken reference forces a narrow
coordination patch, in which case the result ledger must record it.

## Stop Conditions

Stop as `BLOCKED` or `PARTIAL_READY_WITH_BLOCKERS` if any of the following
remain after five Claude iterations:

- GHQF, fixed SGQF, or ASGHF cannot be implemented from the chapter alone.
- The fixed-SGQF approximate likelihood gradient recursion is missing or only
  generic.
- HMC admissibility labels imply exact likelihood, convergence, or live
  adaptive-branch validity.
- A cited technical construction lacks checked source support or a project
  derivation.
- LaTeX cannot build `docs/main.pdf`, or the new P9 material is absent from PDF
  text.

## Rewrite Scope

### Tensor-Product GHQF

Add an implementable construction:

- input dimensions, model maps, Gaussian mean/covariance, covariance factor,
  one-dimensional rule size, process/observation noise;
- standard-normal one-dimensional Gauss--Hermite nodes and weights;
- tensor product multi-index and combined weights;
- transformed nodes \(\chi^{(r)}=m+C\xi^{(r)}\);
- prediction moments for \(x_t=f_\theta(x_{t-1})+u_t\);
- observation moments for \(z_t=h_\theta(x_t)\);
- innovation likelihood scalar and Gaussian update;
- pseudocode for one GHQF step;
- \(s^b\) point-count veto and diagnostic/reference HMC label.

### Fixed SGQF

Add an implementable construction:

- nested univariate levels \(I_\ell\);
- tensor component rule \(I_{\mathbf i}\);
- difference rule \(\Delta_{\mathbf i}\);
- fixed sparse-grid index set \(\mathcal I_{b,L}\);
- signed combined node/weight dictionary after duplicate-node merging;
- replacement of tensor-product GHQ moments by sparse-grid moments;
- PSD stabilization and signed-weight diagnostics;
- pseudocode for constructing a fixed sparse grid and running one filter step;
- HMC label `HMC_ADMISSIBLE_FIXED_APPROXIMATE_TARGET`.

### ASGHF

Add an implementable construction:

- admissible active/old index sets;
- forward neighbors and backward-neighbor admissibility;
- local error indicator and cost indicator;
- tolerance and maximum-point controls;
- pseudocode for offline adaptive grid selection;
- pseudocode for frozen-grid filtering after adaptation;
- explicit statement that live adaptive ASGHF is not a smooth HMC target.

### Fixed-SGQF Analytical Gradient

Keep the generic deterministic-quadrature score as a lemma, then add the full
selected-algorithm recursion:

- fixed sparse-grid standardized points/weights are part of the scalar;
- prediction sensitivities \(\dot m_t^-\), \(\dot P_t^-\);
- differentiable covariance factor convention \(P_t^-=C_t^-C_t^{-\top}\) and
  \(\dot C_t^-\) as supplied by Cholesky/SVD/custom square-root differentiation;
- point sensitivities \(\dot\chi_t^{(r,i)}\);
- transition sensitivities and prediction moment sensitivities;
- observation sensitivities, \(\dot{\bar z}_t\), \(\dot S_t\), \(\dot C_{xz,t}\);
- likelihood-only score using \(\dot v_t\) and \(\dot S_t\);
- posterior mean/covariance sensitivity only as optional propagation state for
  the next time step, not required to differentiate the current likelihood
  contribution if the next prediction sensitivities are supplied directly by the
  recursion.

## P9 Ledgers To Produce

- `...p9-ch34-implementability-ledger-2026-05-30.md`
- `...p9-ch34-fixed-sgqf-gradient-ledger-2026-05-30.md`
- `...p9-ch34-hmc-admissibility-ledger-2026-05-30.md`
- `...p9-ch34-source-anchor-ledger-2026-05-30.md`
- `...p9-ch34-mathdevmcp-ledger-2026-05-30.md`
- `...p9-ch34-claude-review-ledger-2026-05-30.md`
- `...p9-ch34-implementability-gradient-result-2026-05-30.md`

Each ledger must contain `metadata_date`, `seed_papers`, and
`what_is_not_concluded`.

## MathDevMCP Protocol

Use MathDevMCP only for narrow algebraic checks:

- scalar or matrix-style Gaussian innovation score identities where encodable;
- fixed-weight quadrature derivative linearity;
- sparse-grid linear-combination identity;
- one-dimensional affine GHQ transform identity;
- selected scalar substitutions used in the fixed-SGQF score.

Record `MCP_VERIFIED`, `MCP_UNVERIFIED`, `MCP_INCONCLUSIVE`,
`MCP_TOOL_LIMIT`, or `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`.  Do not claim broad
chapter certification.

## Claude Review Loop

Plan review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p9-ch34-implementability-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Execution review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p9-ch34-implementability-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile academic/industrial implementability review prompt>"
```

Claude must output `ACCEPT` or `REJECT` first.  Codex audits Claude.  If Claude
rejects and Codex agrees, patch and resubmit.  Loop to convergence or max 5.
Accept iteration 5 only if remaining issues are minor editorial/layout issues.

## PDF And Validation

After rewrite and review:

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/main.tex
git diff --check
rg -n "Citation .*undefined|Reference .*undefined|There were undefined references|Rerun to get cross-references right|Label\\(s\\) may have changed|undefined citations" docs/main.log
pdftotext docs/main.pdf - | rg -n "fixed sparse-grid|ConstructFixedSparseGrid|RunFixedSparseGridFilterStep|SelectAdaptiveSparseGrid|HMC_ADMISSIBLE_FIXED_APPROXIMATE_TARGET"
git status --short .local_sources .localsource docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex docs/main.pdf docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p9-ch34-*
```

Validation must confirm no undefined citation/reference/rerun blockers, P9
sections present in the PDF, `.local_sources/` unstaged and untracked, and only
allowed files intentionally changed.
