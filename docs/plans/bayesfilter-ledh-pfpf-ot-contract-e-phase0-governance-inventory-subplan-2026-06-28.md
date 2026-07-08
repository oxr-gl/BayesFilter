# Phase 0 Subplan: Contract E governance, math anchors, and route inventory

Date: 2026-06-28

Status: `DRAFT_PENDING_REVIEW`

Master program:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-residual-affine-testing-master-program-2026-06-28.md`

## Phase Objective

Freeze the exact Contract E test target and inventory the current math,
diagnostic, and implementation paths before any implementation edit.

## Entry Conditions Inherited From Previous Phase

This is the entry phase.  The inherited state is:

- Contract E is documented in `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`.
- Prior LGSSM diagnostics support barycentric covariance contraction as the
  leading reset failure.
- The user has requested a gated master program, subplans, Claude review, and
  visible launch.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase0-governance-inventory-result-2026-06-28.md`
- Refreshed Phase 1 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-subplan-2026-06-28.md`
- Execution ledger entry:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-visible-execution-ledger-2026-06-28.md`
- Claude review ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-claude-review-ledger-2026-06-28.md`

## Required Checks, Tests, And Reviews

- Local path/anchor check using `rg` and targeted `sed`.
- Confirm the exact Contract E labels exist in the LaTeX source.
- Confirm existing diagnostic scripts are present.
- Confirm no new implementation command is run in this phase.
- Bounded Claude read-only review of the master program and Phase 0/Phase 1
  subplan paths.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are we about to test the documented Contract E candidate with the right baselines, boundaries, and artifacts? |
| Baseline/comparator | Existing barycentric reset diagnostics and Contract E LaTeX anchors. |
| Primary pass criterion | Phase 0 result records exact Contract E LaTeX path and labels, diagnostic paths, route candidates, forbidden comparators/actions, and a reviewed Phase 1 handoff. |
| Veto diagnostics | Missing Contract E anchors, missing existing diagnostic paths, plan tries to use Zhao-Cui as oracle, plan allows `transport_ad_mode=full`, or plan treats CPU smoke as GPU evidence. |
| Explanatory diagnostics | Current worktree status, existing benchmark/test names, prior diagnostic summaries. |
| Not concluded | No implementation correctness, no value/gradient correctness, no production readiness. |
| Artifact | Phase 0 result plus Claude review ledger. |

## Forbidden Claims And Actions

- Do not claim Contract E works.
- Do not edit production code in Phase 0.
- Do not run GPU, long benchmarks, HMC, training, or nonlinear evidence runs.
- Do not use Zhao-Cui as an oracle for this program.
- Do not use `transport_ad_mode=full` as a planned route.
- Do not send whole files or large code trunks to Claude.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- the master program and Phase 1 subplan pass local anchor checks;
- Phase 0 result records the exact Contract E path and proposition labels:
  `docs/chapters/ch32c_entropic_ot_sinkhorn.tex:886`,
  `prop:bf-eot-positive-spread-gap`,
  `prop:bf-eot-residual-expected-covariance`,
  `prop:bf-eot-residual-support-repair`, and
  `prop:bf-eot-residual-affine-restoration`;
- Claude returns `VERDICT: AGREE` or all material `REVISE` findings are visibly
  patched within five rounds;
- Phase 0 result states the exact Contract E semantic target and Phase 1
  artifact names.

## Stop Conditions

Stop if Contract E anchors cannot be found, existing diagnostics are absent, the
review does not converge after five rounds, or Phase 1 cannot be scoped as a
small moment-level diagnostic.

## End-Of-Phase Protocol

1. Run local path and anchor checks.
2. Write the Phase 0 result.
3. Refresh the Phase 1 subplan if needed.
4. Review Phase 1 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
5. Send bounded exact-path review to Claude.
6. Patch any fixable review issue and rerun focused checks.
