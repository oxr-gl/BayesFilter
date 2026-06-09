# Claude Review: BayesFilter-MacroFinance Stage 2 Post-Implementation

Date: 2026-06-09

Reviewer: Claude Code, read-only reviewer

## Scope

Read-only post-implementation review for Stage 2, the precomputed MAP and mass
artifact.

Claude was instructed not to edit files, create files, run tests or
experiments, launch agents, run Codex, start supervisors, commit, push, or
change repository state.

## Review Result

No material issues found.

- `PrecomputedMassArtifact` carries an explicit `position_role`; the
  MacroFinance compatibility test uses
  `position_role="diagnostic_center_not_map"` rather than relabeling the
  matched-DGP center as a MAP.
- Persisted adapter signatures reject process-local identity patterns and are
  rechecked against `stable_adapter_signature(adapter)` during consumption.
- Covariance source and matrix-used-for-square-root are required nonempty
  fields and are asserted in BayesFilter and MacroFinance tests.
- Only `factor_orientation="row_right_transpose"` is accepted, and the artifact
  enforces `factor @ factor.T == covariance` before use.
- Hessian/covariance factories exist and are covered; `build_latent_transform()`
  feeds the Stage 1 `LatentAffineHMCTransform` without changing orientation
  authority.
- `PrecomputedMassArtifact` is exported through `bayesfilter.inference` and the
  top-level package with public API coverage.
- The MacroFinance compatibility test consumes the existing matched-DGP
  initialization artifact, reconstructs the BayesFilter artifact from
  `Sigma_phi_reg` and `L`, validates it against the real adapter, and checks
  transform parity without changing target, data, or priors.

## Verdict

VERDICT: PROCEED
