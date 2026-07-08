# Phase 6 Subplan: Closeout And Next-Dimensional Handoff

Date: 2026-07-08
Status: `DRAFT_READY_FOR_REVIEW`
Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
Phase 5 result: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase5-replicated-scalar-hmc-result-2026-07-08.md`

## Phase Objective

Close the scalar filtering geometry-to-HMC readiness runbook by summarizing passed gates, remaining gaps, and next justified work. This phase writes documentation only. It does not run new HMC, change defaults, claim convergence, or promote the scalar diagnostic beyond its evidence class.

## Entry Conditions Inherited From Phase 5

- Phase 5 final artifact reports `replicated_diagnostic_passed: true`.
- Phase 5 passed only a replicated finite-telemetry screen, not convergence or posterior validation.
- Native divergence telemetry remains not exposed by this TFP kernel path and must not be treated as zero divergences.
- Large finite log-accept tails were observed descriptively and should be retained as caution for any longer validation.
- All artifacts are CPU-hidden debug/reference evidence, not GPU/XLA production evidence.

## Required Artifacts

- Phase 6 subplan: this file.
- Phase 6 review bundle: `docs/reviews/scalar-filtering-geometry-hmc-phase6-closeout-review-bundle-2026-07-08.md`
- Phase 6 result: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase6-closeout-result-2026-07-08.md`
- Reset memo: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-reset-memo-2026-07-08.md`
- Updated execution ledger: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-visible-execution-ledger-2026-07-08.md`

## Required Checks, Tests, Reviews

- Local Codex substitute review of this Phase 6 closeout subplan because Claude review is policy-blocked for private repository context transfer.
- `git diff --check`
- Optional documentation sanity check by reading the result/reset memo for forbidden claims before final response.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exactly has the scalar filtering geometry-to-HMC readiness runbook established, and what remains open before stronger HMC claims? |
| Baseline/comparator | Phase 0-5 subplans/results and benchmark artifacts. |
| Primary criterion | Closeout result and reset memo accurately separate passed engineering gates from unsupported scientific/runtime claims. |
| Veto diagnostics | Any posterior correctness, convergence, zero-divergence, tuned-kernel, default-readiness, GPU/XLA-readiness, source-faithful Zhao-Cui, or sampler-superiority claim unsupported by the runbook. |
| Explanatory diagnostics | Summary of passed gates, finite telemetry, log-accept caution, CPU-hidden scope, and next suggested work. |
| Not concluded | No new scientific or runtime readiness claim beyond the runbook's finite-telemetry diagnostics. |
| Preserving artifact | Phase 6 closeout result, reset memo, and ledger entry. |

## Forbidden Claims And Actions

- Do not claim posterior correctness, HMC convergence, tuned-kernel readiness, zero divergences, sampler superiority, statistical ranking, default readiness, GPU/XLA readiness, package/public API readiness, or Zhao-Cui source-faithfulness.
- Do not run new experiments or edit implementation code in Phase 6.
- Do not change Phase 0-5 pass/fail criteria after seeing results.
- Do not install packages, fetch network resources, edit model files, or perform destructive git/filesystem actions.

## Exact Final Handoff Conditions

The runbook can close only if:

- Phase 6 subplan review has no unresolved material blocker.
- `git diff --check` passes.
- Phase 6 result and reset memo preserve all non-claims and evidence boundaries.
- Ledger is updated with the final closeout entry.

If closeout review finds unsupported claims, patch the closeout artifacts and rerun focused review/checks before final response.

## Stop Conditions

- Phase 6 subplan review returns unresolved `REVISE`.
- Closeout artifacts contain unsupported scientific/runtime/default/source-faithfulness claims.
- Required `git diff --check` fails and cannot be repaired within documentation scope.
- Continuing would require new experiments, package installation, network fetch, credentials, default-policy change, model-file edit, destructive git/filesystem action, or unsupported claim.

## Skeptical Audit

- Wrong baseline: Phase 6 summarizes Phase 0-5 artifacts only.
- Proxy metric risk: finite telemetry, acceptance, and log-accept values remain finite-telemetry diagnostics only.
- Missing stop conditions: unsupported claims trigger repair before closeout.
- Unfair comparison: no ranking or method comparison occurs.
- Hidden assumptions: scalar success may not transfer to higher dimensions or Zhao-Cui source-faithful routes.
- Stale context: Phase 5 log-accept caution and native divergence unavailability must be retained.
- Environment mismatch: CPU-hidden diagnostics are not GPU/XLA production evidence.
- Artifact adequacy: closeout/result/reset memo answer what was established and what remains open.

Audit result: `PASS_WITH_BOUNDARIES_PENDING_REVIEW`. Execute only after Phase 6 subplan review.
