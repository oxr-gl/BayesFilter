# Phase 0 Subplan: Governance And Review Setup

Date: 2026-07-06

Status: `PASSED`

## Phase Objective

Establish the validity-gaps master program, visible runbook, review path,
evidence contract, and Phase 1 scalar-oracle design gate without running any
new HMC, GPU/XLA, source-faithfulness, or long diagnostic command.

## Entry Conditions Inherited From Previous Phase

- Completed `hmc-next` closeout exists at
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase6-closeout-result-2026-07-06.md`.
- Completed reset memo exists at
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-reset-memo-2026-07-06.md`.
- Phase 5 hard-veto artifact exists at
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.json`.

## Required Artifacts

- Master program.
- Visible gated execution runbook.
- Visible execution ledger.
- Visible stop handoff.
- Phase 0 result.
- Phase 1 scalar-oracle design subplan.
- Compact Phase 0/1 review bundle.

## Required Checks, Tests, Reviews

- Read the local Claude review-gate guide and visible runbook template.
- Check predecessor closeout/reset/artifact existence.
- Compile/import check for existing minimal target/harness/tests.
- Claim-boundary scan over new plan/review files.
- `git diff --check`.
- Material read-only review through Claude review gate when allowed, otherwise
  documented fresh visible Codex substitute review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the validity-gaps program staged with the correct baseline and sufficient review/runtime/scientific boundaries before Phase 1 oracle design? |
| Baseline/comparator | Completed `hmc-next` closeout, reset memo, and Phase 5 hard-veto artifact. |
| Primary pass criterion | Required planning artifacts exist, skeptical audit passes, local checks pass, review path is recorded, and no plan text promotes hard-veto mechanics evidence into validity claims. |
| Veto diagnostics | Missing predecessor artifact, wrong baseline, unreviewed long/GPU runtime command, unsupported posterior/convergence/ranking/readiness/source-faithful claim, missing stop condition, invalid review path, or review nonconvergence. |
| Explanatory diagnostics | Artifact inventory, dirty-worktree summary, review status, and local check outputs. |
| Not concluded | Posterior correctness, HMC convergence, R-hat/ESS, ranking, source-faithful parity, default readiness, production readiness, public API readiness, or LEDH result. |

## Forbidden Claims And Actions

Do not run HMC, GPU/XLA, long diagnostics, source-faithful work, package
installation, network fetch, public API/default changes, or model-file edits in
Phase 0. Do not claim scientific validity from plan existence.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 1 only if:

- Phase 0 local checks pass;
- material review returns `VERDICT: AGREE` or a documented fallback review
  converges;
- Phase 1 subplan is present and reviewed for boundary safety;
- no human-required boundary is crossed.

## Stop Conditions

Stop if predecessor artifacts are missing, review cannot converge after five
rounds for the same blocker, the baseline is wrong, or Phase 1 would require a
runtime/scientific boundary not yet reviewed.
