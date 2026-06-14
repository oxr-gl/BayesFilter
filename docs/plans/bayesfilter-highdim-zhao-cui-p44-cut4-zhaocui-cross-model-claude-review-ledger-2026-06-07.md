# P44 Claude Review Ledger: CUT4--Zhao-Cui Cross-Model Program

metadata_date: 2026-06-07
phase: P44

## Plan Review Iteration 1

status: `BLOCKED_P44_PLAN_GOVERNANCE`

Reviewer summary:
- M0 target matrix needed explicit schema columns for target identity,
  reference route, parameterization, claim class, and
  factorized-product-versus-coupled structure.
- M1 LGSSM needed exact Kalman as the governing reference rather than allowing
  dense reference as an alternative.
- M2 needed an explicit downgrade rule when visible CUT4 quadrature error
  exceeds same-target tolerances.
- M3 needed a concrete resource/point-count cap and stronger symmetric-mode
  coverage requirements.
- M5 needed equality blocked by default unless a matched shared closure target
  is identified.
- M7 generalized SV needed an operational target-definition table before
  governing value/gradient work.
- The master program needed long-run stop conditions and pre-mortem
  requirements for later nonlinear phases.

Patch response:
- Updated M0 schema, M1 baseline rule, M2 downgrade rule, M3 cap and
  multimodality gate, M5 equality blocker, M7 target-definition table, and
  master long-run execution requirements.

## Plan Review Iteration 2

status: `PASS_P44_PLAN_GOVERNANCE`

Reviewer summary:
- The iteration-1 blockers were resolved.
- The P44 plan now requires an explicit M0 target-governance schema with target
  identity, reference route, parameterization, claim class, and
  factorized-product-versus-coupled structure.
- LGSSM now uses exact Kalman as the governing baseline.
- Same-target nonlinear phases now include downgrade/stop rules for visible
  CUT4 error, missing dense-reference coverage, resource caps, and long-run
  pre-mortems.
- Diagnostic-only SIR, predator-prey, and generalized-SV phases now block
  equality/native-model claims by default unless a shared target is explicitly
  specified and reviewed.

Verdict: `PASS_P44_PLAN_GOVERNANCE`
