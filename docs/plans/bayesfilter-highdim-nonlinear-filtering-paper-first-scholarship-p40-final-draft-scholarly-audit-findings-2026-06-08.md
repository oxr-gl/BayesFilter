# P40 Final-Draft Scholarly Audit Findings

Date: 2026-06-08

## Audit target

- Primary review object:
  - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p40-fixed-sgqf-expanded-companion-note-2026-06-08.tex`
- Comparator/provenance only:
  - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p39-fixed-sgqf-expanded-companion-note-2026-06-07.tex`

## Sources consulted

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-source-support-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p8-ch34-source-anchor-ledger-2026-05-30.md`
- `.local_sources/highdim_nonlinear_filtering/Sparse-grid quadrature nonlinear filtering Jia(11).pdf`
- `.local_sources/highdim_nonlinear_filtering/adaptive_sparse_grid_gauss_hermite_1803.09272.pdf`
- `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf`
- user-provided page images from Jia 2012 pp. 331--338 showing the SGQ univariate-point construction, Algorithm 1, Theorem 3.2, Proposition 3.1, and Proposition 3.2

## What is not concluded

- This audit does not prove every derivation formally.
- MathDevMCP output is diagnostic evidence, not blanket certification.
- Codex agreement is second-opinion evidence, not mathematical proof.
- A passing subsection does not imply exact nonlinear filtering correctness, production readiness, or universal superiority over non-Gaussian filtering lanes.

## Evidence contract

### Question
Is the current p40 note ready for final draft submission under a skeptical scholarly audit?

### Review dimensions
- mathematical accuracy
- derivation consistency
- notation consistency
- logic correctness
- original-paper matching

### Primary promotion criterion
Every major block must have an explicit verdict, source-backed claims must match the cited papers or be demoted to local derivation status, and no unresolved blocker may remain in the same-scalar, gradient, algorithm-order, or conclusion/readiness language.

### Veto diagnostics
The note is **not** ready for final draft submission if any of the following remain:
- corrupted or mathematically ambiguous displayed equations in a load-bearing block;
- mismatch between same-scalar contract, analytical gradient, and FD audit;
- source-backed claim not traceable to the cited paper;
- unresolved notation or object drift across value/gradient/algorithm blocks;
- unresolved hostile second-opinion blocker;
- conclusion language stronger than the audited evidence.

## Decision table

| Item | Status |
| --- | --- |
| Decision | `NOT_READY_FOR_FINAL_DRAFT_SUBMISSION` |
| Primary criterion status | Failed: multiple unresolved block-level blockers remain |
| Veto diagnostics status | Failed |
| Main uncertainty | Whether the gradient/algorithm blocks can be repaired without changing the intended fixed-scalar contract |
| Next justified action | Repair the documented blockers in p40, then rerun the same block-by-block scholarly audit |
| What is not being concluded | No claim that FixedSGQF is mathematically unsalvageable; the current draft is simply not yet submission-ready |

## Global verdict dashboard

| Block | Scope | Claude verdict | Codex second opinion | MathDevMCP status | Main issue |
| --- | --- | --- | --- | --- | --- |
| A | object contract / approximation boundary | `BLOCKER` | `REVISE` | N/A | low-interaction plausibility argument overreaches after dense coordinate transform |
| B | exact recursion / Gaussian projection | `BLOCKER` | `CONDITIONAL PASS` | `prop:p31-affine-projection` -> `MCP_UNVERIFIED_HUMAN_REVIEWED` | missing independence/zero-mean assumptions for noise and filtering factorization |
| C | quadrature / tensor / sparse-grid construction | `BLOCKER` | `REVISE` | `eq:p31-smolyak-coeff` -> `MCP_INCONCLUSIVE_NEEDS_ASSUMPTION` | 3D cloud-count inconsistency and source over-identification of the level-2 rule |
| D | toy merged clouds | `BLOCKER` | `REVISE` | N/A | 3D narrative says full 27-point tensor picture collapses directly to six points, which misstates the sparse-grid construction path |
| E | value path | `PASS` | `PASS` | N/A | no blocker found |
| F | worked numeric oracle | `PASS` | `PASS` | N/A | internally consistent |
| G | same-scalar contract | `PASS_WITH_NOTES` | `PASS WITH MINOR PRECISION NOTES` | `eq:p31-fixed-scalar` -> `MCP_UNVERIFIED_HUMAN_REVIEWED` | scalar-defining objects and derivative metadata should be separated more explicitly |
| H | analytical gradient | `BLOCKER` | `BLOCKER` | `eq:p32-gradient-chain` -> `MCP_INCONCLUSIVE_NEEDS_ASSUMPTION`; `eq:p31-chol-derivative` -> `MCP_UNVERIFIED_HUMAN_REVIEWED`; `prop:p31-innovation-score` -> `MCP_UNVERIFIED_HUMAN_REVIEWED` | malformed derivation-ledger TeX and dependency-order error for `\dot C_t^-` |
| I | boxed / implementation / end-to-end algorithms | `BLOCKER` | `BLOCKER` | N/A | algorithm order evaluates the log likelihood before the innovation-branch veto |
| J | finite-difference same-scalar audit | `PASS_WITH_NOTES` | `PASS` | `eq:p31-central-diff` -> `MCP_UNVERIFIED_HUMAN_REVIEWED` | notation between `\mathcal B` and `\mathfrak B` should be made explicit |
| K | validation / comparison / source map / inventory / conclusion | `BLOCKER` | `BLOCKER` | N/A | conclusion and readiness language outrun the documented evidence; validation models D/E are incomplete specs |

## Per-block findings

### Block A — object contract / approximation boundary
Scope: lines ~118--447.

**Verdict:** `BLOCKER`

**Findings**
- The exact-vs-approximate hierarchy is mostly well separated and does not falsely claim exact nonlinear filtering.
- The main mathematical problem is the plausibility argument around `eq:p32-low-interaction-map`: low interaction in physical coordinates does **not** automatically imply low interaction in standardized quadrature coordinates after `x = m + C\xi` if `C` is dense.
- The block should either:
  1. restate the assumption directly in standardized `\xi`-coordinates, or
  2. require structured/sparse/block-local covariance factors.
- Minor notation issue: `eq:p31-innovation-loglik-opening` introduces `v_t` and bare `\ellhat_t` before the local value-path definitions make that usage feel anchored.

**Codex second opinion**
- `REVISE`; same main blocker: the low-interaction argument overreaches after the coordinate map.

### Block B — exact recursion and Gaussian projection
Scope: lines ~457--675.

**Verdict:** `BLOCKER`

**Findings**
- The filtering recursion and affine Gaussian projection are mathematically standard and mostly correct.
- However, the block states only marginal Gaussian laws for `\eta_t` and `\varepsilon_t`. To justify:
  - `p_\theta(x_t\mid x_{t-1})`,
  - `g_\theta(y_t\mid x_t)`,
  - `S_t = R_\theta + \operatorname{Cov}(Z_t)`, and
  - the usual prediction/update factorization,
  the note should explicitly state that the process and observation noises are zero-mean, mutually independent, time independent in the intended sense, and independent of the state/past conditional on the model.
- The affine projection proposition is correct, but the optimal intercept `a = m_t^- - C_{xz,t}S_t^{-1}\bar z_t` is only implicit through centering.

**Source match**
- The block aligns with Jia 2012 Section 2 / the Gaussian approximation setup, modulo notation.
- The Gaussian-projection proposition itself is a local project derivation, not a source theorem.

**MathDevMCP**
- `prop:p31-affine-projection` returned `unverified:missing_assumption`, specifically asking for invertibility/solve assumptions and shape constraints.
- This supports the human finding that assumptions need to be made explicit.

**Codex second opinion**
- `CONDITIONAL PASS`, with the same blocker on missing independence/regularity assumptions.

### Block C — quadrature / tensor / sparse-grid construction
Scope: lines ~758--1747.

**Verdict:** `BLOCKER`

**Findings**
- The tensor-product and Smolyak-band exposition is generally strong and pedagogically clearer than the source.
- Two submission-blocking issues remain:
  1. **3D cloud-count inconsistency.** Earlier p40 language describes a seven-point merged cloud including the zero-weight center, while later the fixed stored cloud semantics prune zero-weight nodes and the 3D toy cloud keeps only the six axis points. The note must distinguish clearly between:
     - merged distinct nodes before zero-weight pruning, and
     - final stored cloud after pruning.
  2. **Overstatement of the source status of the level-2 univariate rule.** The user-provided Jia 2012 pp. 331--333 show that for level-2 SGQ, the three-point family is tunable through `\hat p_1`; `\hat p_1 = \sqrt 3` is the GHQ special case, not the unique source-mandated level-2 rule. The note should say explicitly that its chosen `I_2` is the GHQ specialization used for the present note and for the UKF/level-2 bridge.
- Minor formal issue: `eq:p32-normal-moments` should make the `j=0` convention explicit.

**Source match**
- The band translation and Smolyak coefficients match Jia 2012 Eq. (26)--(29).
- Algorithm-1-style duplicate accumulation is correctly captured as a dictionary/merge construction.
- The exactness/UKF-relation discussion is directionally correct but should be more careful about the specific univariate-rule choice used to identify the UT/UKF subset.

**MathDevMCP**
- `eq:p31-smolyak-coeff` returned `inconclusive`, mainly because the obligation needs smaller symbolic pieces or human review.
- This is diagnostic only; it does not refute the equation.

**Codex second opinion**
- `REVISE`, with the same two blockers.

### Block D — toy merged clouds
Scope: lines ~1749--1898.

**Verdict:** `BLOCKER`

**Findings**
- The 2D and 3D arithmetic is correct:
  - 2D origin weight: `-1 + 2/3 + 2/3 = 1/3`
  - 3D origin weight: `-2 + 2/3 + 2/3 + 2/3 = 0`
- The narrative is the problem. The text says the full 27-point tensor-product picture collapses to six axis points, but the actual sparse-grid construction does **not** begin from the full `(2,2,2)` tensor rule. It begins from the signed combination of `(1,1,1)`, `(1,1,2)`, `(1,2,1)`, and `(2,1,1)`, i.e. 10 raw contributions, then merges/prunes.
- This should be rewritten as:
  - full tensor product = 27-point comparator picture,
  - sparse-grid signed combination = 10 raw contributions,
  - merged/pruned fixed cloud = 6 stored nodes.

**Codex second opinion**
- `REVISE`, same blocker.

### Block E — value path
Scope: lines ~1900--2017.

**Verdict:** `PASS`

**Findings**
- Prediction and observation stages are mathematically consistent with the earlier Gaussian projection contract.
- The use of `Q_\theta` and `R_\theta` as additive analytic noise terms is consistent with the report-wide additive-noise convention.
- The observation cross-covariance uses the predictive cloud correctly.
- The runtime order is coherent, though the prose should keep making clear that positive-definiteness is checked before using `\log\det` and `S_t^{-1}` in any implementation.

**Codex second opinion**
- `PASS`.

### Block F — worked one-step numeric oracle
Scope: lines ~2018--2296.

**Verdict:** `PASS`

**Findings**
- The numeric oracle is internally consistent across value, derivative, and propagation quantities.
- The branch, cloud, and scalar reuse story is coherent.
- This block is one of the strongest pieces of the note and should be preserved.

**Codex second opinion**
- `PASS`.

### Block G — saved scalar and same-scalar contract
Scope: lines ~2297--2398.

**Verdict:** `PASS_WITH_NOTES`

**Findings**
- The same-scalar contract is conceptually coherent and precise enough to support the FD logic later.
- One precision improvement is recommended: separate clearly the objects that define the **value scalar** from derivative-only metadata/routines included for the gradient lane.
- The present text is not mathematically wrong; it is just more entangled than necessary.

**MathDevMCP**
- `eq:p31-fixed-scalar` returned `unverified`, mainly because differentiability assumptions and formalization boundaries are not fully encoded.
- This is consistent with the fact that the equation is a semantic contract, not a backend-friendly algebraic identity.

**Codex second opinion**
- `PASS WITH MINOR PRECISION NOTES`.

### Block H — analytical gradient
Scope: lines ~2399--2809.

**Verdict:** `BLOCKER`

**Findings**
- This is the highest-risk block and the main current submission blocker.
- Two hard issues remain:
  1. **Malformed TeX in `eq:p32-derivation-ledger`.** The displayed equation is visibly corrupted (`ext{factor derivative}`, broken row endings, broken superscript on `\dot\ellhat_t^{\rm FSGQ}`). This is unacceptable in a load-bearing gradient section.
  2. **Dependency-order mistake.** The ledger says the factor stage yields both `\dot C_{t-1}` and `\dot C_t^-` before prediction yields `\dot P_t^-`. But `\dot C_t^- = DC(P_t^-)[\dot P_t^-]` depends on `\dot P_t^-`, so the ledger order is wrong.
- Outside that hotspot, the surrounding prediction sensitivities, observation sensitivities, innovation score, and posterior propagation formulas are mostly coherent.
- There is also a smaller notation consistency issue: the section briefly drops the `^{\rm FSGQ}` superscript on the one-step score in places where the same-scalar identity matters.

**Source match**
- This block is BayesFilter-local derivation, not Jia-source theorem support.
- It must therefore survive on internal derivational coherence plus the FD contract, not on citation alone.

**MathDevMCP**
- `eq:p32-gradient-chain`: `inconclusive`
- `eq:p31-chol-derivative`: `unverified`
- `prop:p31-innovation-score`: `unverified`
- The common pattern was missing explicit assumptions, larger-than-backend obligations, and need for human formalization. This does **not** refute the formulas, but it reinforces that the block must be cleaned and manually defended carefully.

**Codex second opinion**
- `BLOCKER`, same two main issues.

### Block I — boxed / implementation / end-to-end algorithms
Scope: lines ~2811--3119.

**Verdict:** `BLOCKER`

**Findings**
- The main drift is execution order around the innovation covariance.
- In the value path, the accepted runtime order is:
  1. form `\bar z_t, S_t, C_{xz,t}`,
  2. veto if the innovation branch fails,
  3. then form `v_t, \ellhat_t^{\rm FSGQ}, K_t`.
- But in Block I, the algorithm text computes `\ellhat_t^{\rm FSGQ}` from `\eqref{eq:p31-fsgq-loglik}` before the innovation-branch veto is applied. Since that formula uses `\log\det S_t` and `S_t^{-1}`, it should only be evaluated on the accepted SPD branch.
- This is a serious algorithm-order inconsistency and must be corrected.
- Secondary note: if the value path explicitly symmetrizes covariances before branch checks, the algorithm block should be equally explicit about how the dotted covariances are interpreted relative to that symmetrization map.

**Codex second opinion**
- `BLOCKER`, same main issue.

### Block J — finite-difference same-scalar audit
Scope: lines ~3121--3294.

**Verdict:** `PASS_WITH_NOTES`

**Findings**
- The FD protocol does test the same fixed scalar, provided the same saved branch identity is enforced exactly as written.
- The main non-blocking issue is notation: the block alternates between `\mathcal B` and `\mathfrak B` and should say once, explicitly, that `\mathfrak B` is the implementation-level branch-identity record for the saved branch metadata used by the scalar.

**MathDevMCP**
- `eq:p31-central-diff` returned `unverified`, largely because the equation is a semantic diagnostic contract rather than a small algebraic identity.

**Codex second opinion**
- `PASS`.

### Block K — validation / comparison / source map / inventory / conclusion
Scope: lines ~3295--end.

**Verdict:** `BLOCKER`

**Findings**
- The source map is mostly well bounded and does a good job separating Jia-backed material from BayesFilter-local derivation.
- Two blockers remain:
  1. **Validation models D/E are incomplete mathematical specifications.**
     - Model D omits the law and independence structure of `\varepsilon_{t,j}` and leaves dimensions for some objects implicit.
     - Model E gives only an observation equation, without a full state/predictive specification.
     - Since the section calls these “mathematical specifications for future code tests,” they should be complete enough to instantiate.
  2. **Conclusion overclaim.** The note currently says FixedSGQF is “implementation-ready” and “sufficiently thorough and persuasive to justify approval.” That exceeds the evidence actually documented in the note, especially while the gradient and algorithm-order blockers remain unresolved.
- Recommended downgrade:
  - “mathematically specified for implementation and audit”
  - “candidate lane deserving further implementation and validation review”

**Source match**
- The adaptive sparse-grid discussion is acceptable as a BayesFilter interpretive restriction rather than a Singh theorem claim.
- The TT comparison language is acceptable at a high level, but should remain clearly framed as method-class positioning rather than source-proved ranking.

**Codex second opinion**
- `BLOCKER`, same issues.

## Blocker register

The current p40 draft is **not ready** for final draft submission because the following blockers remain:

1. **Block A:** low-interaction plausibility argument overreaches after dense coordinate transformation.
2. **Block B:** missing noise independence / zero-mean assumptions needed for the displayed filtering factorization and covariance identities.
3. **Block C:**
   - 3D merged-cloud count is not handled consistently across “merged” vs “stored/pruned” cloud semantics.
   - level-2 univariate rule is presented too strongly as source-mandated rather than as the GHQ specialization used here.
4. **Block D:** 3D narrative misstates the construction path by speaking as if the six-point cloud comes directly from collapsing the full 27-point tensor rule.
5. **Block H:**
   - corrupted displayed derivation ledger,
   - wrong dependency order for `\dot C_t^-`.
6. **Block I:** algorithm-order drift computes the log likelihood before the innovation-branch veto.
7. **Block K:**
   - incomplete validation model specifications D/E,
   - conclusion/readiness language stronger than the audited evidence supports.

## Non-blocking issues

- Unify bare `\ellhat_t` vs `\ellhat_t^{\rm FSGQ}` in the gradient-related blocks.
- State the `j=0` convention explicitly in the normal-moment formula.
- Clarify `\mathcal B` vs `\mathfrak B` once in the FD section.
- Consider separating scalar-defining metadata from gradient-only metadata in the saved-branch section.
- Normalize label-prefix narration where `p31`, `p38`, and `p39` labels coexist inside p40, especially in the 3D toy material.

## MathDevMCP audit summary

Representative MathDevMCP outcomes:
- `prop:p31-affine-projection` -> `unverified` due to missing invertibility/shape assumptions.
- `eq:p31-smolyak-coeff` -> `inconclusive` due to backend limits / need for smaller obligations.
- `eq:p31-chol-derivative` -> `unverified` due to missing assumptions and need for manual formalization.
- `prop:p31-innovation-score` -> `unverified` due to missing shape/assumption constraints.
- `eq:p31-fixed-scalar` -> `unverified` because the contract is semantic and assumption-heavy.
- `eq:p32-gradient-chain` -> `inconclusive` due to backend scope limits.
- `eq:p31-central-diff` -> `unverified` for the same reason: it is a semantic diagnostic contract, not a bounded algebraic identity.

Interpretation:
- These outputs did **not** produce a direct contradiction to the core equations.
- They did provide useful evidence about where assumptions are missing or where the note is relying on human-level derivation rather than machine-checkable obligations.
- In particular, they reinforce the need to repair and sharpen Blocks B, G, H, and J rather than treating those blocks as already hardened.

## Second-opinion review summary

Per-block hostile second opinions were obtained with Codex for Blocks A--K. The most important convergences were:
- agreement on the Block A low-interaction overreach;
- agreement on Block C’s 3D-cloud and level-2-rule issues;
- agreement that Block H is not release-ready because of the malformed derivation ledger and the `\dot C_t^-` dependency-order error;
- agreement that Block I drifts from the accepted innovation-veto order;
- agreement that Block K overclaims readiness.

No Codex review contradicted the current main blocker diagnosis.

## Final submission decision

**Decision:** `NOT_READY_FOR_FINAL_DRAFT_SUBMISSION`

### Why
The note is already strong in its overall object separation, value recursion, and worked oracle, but it still has unresolved mathematical/logic blockers in:
- the approximation-plausibility argument,
- the state-space/noise assumption layer,
- the 3D sparse-grid exposition,
- the analytical gradient ledger,
- the implementation-order algorithm,
- and the conclusion/readiness language.

### Next justified action
Repair the specific blockers above inside the p40 note, then rerun this same audit workflow:
1. structural/math review,
2. narrow MathDevMCP checks on load-bearing labels,
3. per-block hostile second opinion,
4. updated findings note with a new final verdict.

At present, the justified readiness label is **not** `P40_FINAL_DRAFT_SCHOLARLY_AUDIT_PASS`.
