# P44-M4 Claude Review Ledger: Nonlinear Additive-Gaussian Transition

metadata_date: 2026-06-08
phase: P44-M4
run_id: `p44-codex-supervised-20260608-013203`

p44_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase4-nonlinear-transition-evidence-manifest-p44-codex-supervised-20260608-013203.json`
p44_claude_code_governance_verdict: `PASS_P44_M4_CODE_GOVERNANCE`
p44_claude_code_governance_iterations: `1`

## Repair Review Iteration 1

review_cycle: `1`
review_type: `repair`
review_iteration: `1`
status: `PASS_P44_M4_REPAIR_REVIEW`

Scope:
- Read-only Claude review of the M4 horizon-scope repair after local evidence
  showed that the current Zhao--Cui scalar helper is pinned to exactly two
  observations.

Reviewer summary:
- The amendment narrows the claim boundary instead of weakening observed
  Zhao--Cui evidence: Zhao--Cui still gets `T=2`, dims 1--3 value and score
  checks against dense reference, while `T=4` is made an explicit nonclaim.
- The two-horizon accumulation statement is preserved only for CUT4, where
  both `T=2` and `T=4` are tested against dense reference.
- Refusing to silently extend `scalar_nonlinear_fixed_design_tt_value_path` to
  horizon 4 inside M4 is a safer governed choice.
- Critical caveat: downstream artifacts must preserve the explicit boundary
  that there is no Zhao--Cui `T=4` accumulation claim.

Decision:
- `PASS_P44_M4_REPAIR_REVIEW`

## Code/Governance Review Iteration 1

review_cycle: `1`
review_type: `code_governance`
review_iteration: `1`
status: `PASS_P44_M4_CODE_GOVERNANCE`

Scope:
- Final read-only Claude code/governance review of the M4 subplan, repair
  amendment, focused test, result note, evidence manifest, review ledger, and
  CPU-only command logs.

Reviewer summary:
- Baseline and promotion logic are governed correctly by dense refinement and
  nested `c=0` Kalman tie-out before nonlinear claims.
- The Zhao--Cui `T=4` nonclaim is preserved in the amendment, result note,
  manifest, and executable boundary test.
- No wrong-baseline, proxy-metric, unfair-comparison, hidden-assumption, stale
  context, or artifact/log mismatch blocker remains.
- Minor non-blocking caveat: the subplan's stop-before-nonlinear rule is
  documented rather than encoded as a separate harness stop, but the nested
  linear gate passed, so this does not invalidate closure evidence.

Decision:
- `PASS_P44_M4_CODE_GOVERNANCE`
