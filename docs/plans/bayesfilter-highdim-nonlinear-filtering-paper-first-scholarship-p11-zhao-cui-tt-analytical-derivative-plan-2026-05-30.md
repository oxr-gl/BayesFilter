# P11 Plan: Zhao-Cui TT Analytical Derivative

metadata_date: 2026-05-30

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports."
- Zhao-Cui companion code audit snapshot at `third_party/audit/zhao_cui_tensor_ssm_p10/source`.
- P10 Zhao-Cui filtering-scalar and gradient-feasibility ledgers.

what_is_not_concluded:
- No complete analytical derivative for the adaptive stochastic companion code.
- No HMC readiness.
- No production BayesFilter implementation.
- No posterior accuracy or paper-figure replication claim.
- No default-method recommendation.
- No permission to copy third-party code into production modules.

## Purpose

Derive the analytical derivative of the Zhao-Cui tensor-train sequential
filtering scalar at the strongest honest scope: a fixed-branch squared-TT/SIRT
normalizer.  The result must be a standalone LaTeX derivation note that a
future implementation phase can follow, while explicitly separating this
fixed-branch derivative from the adaptive TT-cross/rank/stochastic branches of
the companion code.

## Skeptical Plan Audit

The tempting mistake is to claim that because the code reports
`logmarginal_likelihood`, it already has an analytical HMC gradient.  It does
not.  The companion code builds TT/SIRT approximations through random samples,
TT-cross/ALS updates, rank truncation, QR/SVD operations, defensive constants,
ESS-triggered reapproximation, and model-specific transformations.  Those are
branch-changing operations unless explicitly frozen or smoothed.

The correct target is therefore:

\[
  \widehat\ell_T^{\rm TT}(\alpha)
  =
  \sum_{t=1}^T
  \left\{
  \log \widehat z_t(\alpha)-c_t(\alpha)
  \right\},
\]

where \(\alpha\) is an external model parameter, all TT branch choices are
fixed, \(\widehat z_t\) is the squared-TT/SIRT normalizer, and \(c_t\) is the
stabilizing constant shift used by the declared scalar.  If a future
implementation freezes \(c_t\) numerically instead of recomputing it, the
derivative drops the \(-\dot c_t\) term and the scalar must be named
accordingly.

## Evidence Contract

Question:
Can the Zhao-Cui fixed-branch TT/SIRT filtering scalar be differentiated
analytically enough that a future Codex implementation could build a
same-scalar gradient prototype without further literature research?

Baseline/comparator:
- P9 fixed sparse-grid Gaussian projection derivative, which already has a
  declared approximate scalar and analytical score.
- P10 Zhao-Cui scalar extraction and Octave smoke, which identify the
  normalizer but do not implement its derivative.

Primary pass criterion:
- A LaTeX derivation note gives a complete fixed-branch gradient contract for
  the squared-TT normalizer, including target density, square-root density,
  TT core sensitivities, mass-matrix normalizer contraction, stabilizing
  constant, recursive dependence on the previous filtering approximation, and
  the final score.

Veto diagnostics:
- derivative silently ignores TT-core dependence on \(\alpha\);
- derivative treats adaptive rank/cross/rounding choices as smooth without a
  fixed-branch assumption;
- derivative loses the reported scalar by dropping `log(sirt.z)-const`;
- source/code anchors are vague;
- Claude finds a major missing term;
- MathDevMCP contradicts a narrow algebraic identity.

Explanatory diagnostics:
- MathDevMCP tool limits on function-valued or tensor-valued obligations;
- unimplemented terms required by a future prototype;
- finite-difference checks proposed but not run.

Artifact preserving result:
- `docs/plans/...p11-zhao-cui-tt-analytical-derivative-note-2026-05-30.tex`
- compiled PDF beside the note;
- P11 derivation, MathDevMCP, Claude review, and result ledgers.

## Allowed Writes

- New P11 files under `docs/plans/`.
- No edits to production `bayesfilter/`.
- No edits to DPF, student-baseline, controlled-DPF, or unrelated dirty files.
- No commits.

## Derivation Scope

The note must derive:
- notation separating external parameter \(\alpha\) from Zhao-Cui's learned
  parameter coordinate \(\vartheta\);
- exact unnormalized joint filtering density \(q_t\);
- reference-coordinate potential \(V_t(u;\alpha)\);
- square-root density
  \(\psi_t(u;\alpha)=\exp[-V_t(u;\alpha)/2]\);
- fixed-branch TT representation
  \(\phi_t(u;\alpha)=G_{t,1}(u_1;\alpha)\cdots G_{t,D}(u_D;\alpha)\);
- fixed interpolation/ALS linearized core equations;
- normalizer contraction through mass matrices;
- derivative
  \(\dot z_t = 2\langle \phi_t,\dot\phi_t\rangle_M+\dot\tau_t\);
- final score
  \[
    \partial_i\widehat\ell_T^{\rm TT}
    =
    \sum_t
    \left\{
    \frac{\partial_i\widehat z_t}{\widehat z_t}
    -
    \partial_i c_t
    \right\};
  \]
- recursive dependence of \(q_t\) on the previous approximate filter;
- operations that remain fixed-branch obligations rather than completed code.

## MathDevMCP Protocol

Use MathDevMCP only for narrow algebraic obligations:
- derivative of \(\log z-c\);
- derivative of squared normalizer \(\int \phi^2+\tau\);
- product-rule identity for TT core product;
- normalized-density derivative if feasible.

Statuses:
- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

Do not claim broad machine certification.

## Claude Review Loop

Run Claude plan review and execution review with bounded hostile prompts:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p11-zhao-cui-tt-derivative-<plan|exec>-review-iter<N> \
  --model sonnet --effort high "<bounded hostile review prompt>"
```

Claude must output `ACCEPT` or `REJECT` first.  Codex audits Claude and patches
only if Codex agrees.  Maximum five iterations.  Stop for major derivative,
same-scalar, source-anchor, or unsupported-claim blockers.

## Validation

- Compile the standalone LaTeX note with `latexmk`.
- Run `git diff --check` on new P11 files.
- Confirm no accidental production-code edits.
- Record all validation commands in the result ledger.
