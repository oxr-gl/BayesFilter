# Phase 0 Subplan: Program Launch And Inherited-Boundary Freeze

Date: 2026-06-29

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Launch the governed actual-SV single-target correction program, verify that the
master/contract/runbook/ledger artifacts are internally coherent, freeze the
inherited authority set, and draft the Phase 1 single-target-contract result
path before any implementation or test rewrite phase is permitted.

## Entry Conditions Inherited From Previous Phase

- User requested a governing master program plus explicit phase subplans to
  prevent drift.
- 2026-06-26, 2026-06-28, and 2026-06-29 actual-SV reset/derivation/chapter
  artifacts already exist and must be treated as inherited anchors.  For Phase 0,
  the minimum inherited anchor set is:
  - `docs/plans/bayesfilter-actual-transformed-sv-sgqf-planning-error-reset-memo-2026-06-26.md`
  - `docs/plans/bayesfilter-actual-transformed-sv-sgqf-value-semantics-bug-fix-plan-2026-06-26.md`
  - `docs/plans/bayesfilter-actual-sv-single-target-lane-reset-memo-2026-06-28.md`
  - `docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md`
  - `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
  - `docs/chapters/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex`
  - `docs/chapters/ch28_nonlinear_ssm_validation.tex`
- No implementation, test rewrite, benchmark rerun, runtime, GPU, or HMC phase
  is authorized at launch.
- Claude may review only; Codex remains supervisor and executor.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-actual-sv-single-target-master-program-2026-06-29.md`
- Single-target contract:
  `docs/plans/bayesfilter-actual-sv-single-target-contract-2026-06-29.md`
- Visible runbook:
  `docs/plans/bayesfilter-actual-sv-single-target-visible-gated-execution-runbook-2026-06-29.md`
- Execution ledger:
  `docs/plans/bayesfilter-actual-sv-single-target-visible-execution-ledger-2026-06-29.md`
- Claude review ledger:
  `docs/plans/bayesfilter-actual-sv-single-target-claude-review-ledger-2026-06-29.md`
- Stop handoff:
  `docs/plans/bayesfilter-actual-sv-single-target-visible-stop-handoff-2026-06-29.md`
- Phase 0 result:
  `docs/plans/bayesfilter-actual-sv-single-target-phase0-program-launch-result-2026-06-29.md`
- Phase 1 subplan draft:
  `docs/plans/bayesfilter-actual-sv-single-target-phase1-single-target-contract-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
test -f docs/plans/bayesfilter-actual-transformed-sv-sgqf-planning-error-reset-memo-2026-06-26.md
test -f docs/plans/bayesfilter-actual-transformed-sv-sgqf-value-semantics-bug-fix-plan-2026-06-26.md
test -f docs/plans/bayesfilter-actual-sv-single-target-lane-reset-memo-2026-06-28.md
test -f docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md
test -f docs/plans/bayesfilter-actual-sv-single-target-master-program-2026-06-29.md
test -f docs/plans/bayesfilter-actual-sv-single-target-contract-2026-06-29.md
test -f docs/plans/bayesfilter-actual-sv-single-target-visible-gated-execution-runbook-2026-06-29.md
test -f docs/plans/bayesfilter-actual-sv-single-target-visible-execution-ledger-2026-06-29.md
test -f docs/plans/bayesfilter-actual-sv-single-target-claude-review-ledger-2026-06-29.md
test -f docs/plans/bayesfilter-actual-sv-single-target-visible-stop-handoff-2026-06-29.md
test -f docs/plans/bayesfilter-actual-sv-single-target-phase0-program-launch-subplan-2026-06-29.md
test -f docs/plans/bayesfilter-actual-sv-single-target-phase1-single-target-contract-subplan-2026-06-29.md
test -f docs/plans/bayesfilter-actual-sv-single-target-phase0-program-launch-result-2026-06-29.md || true
rg -n "single-target|same-target|wrong scalar|tests passed but wrong question|KSC|diagnostic|surrogate" docs/plans/bayesfilter-actual-sv-single-target-*.md
git diff --check -- docs/plans/bayesfilter-actual-sv-single-target-*.md
```

Claude review is required for:

- master program,
- single-target contract,
- visible runbook,
- Phase 0 result,
- Phase 1 subplan draft.

No runtime, TensorFlow, pytest, benchmark, GPU/CUDA, HMC, package/network,
release, CI, or default-policy command is authorized in Phase 0.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the governed artifact family coherent enough to freeze the inherited actual-SV single-target boundary and start Phase 1 contract execution safely? |
| Baseline/comparator | 2026-06-26 reset/bug-fix artifacts, 2026-06-28 single-target reset, 2026-06-29 derivation/chapter artifacts, and repo master-program patterns. |
| Primary criterion | Phase 0 passes if all required launch artifacts exist, inherited anchors are enumerated correctly, anti-drift vetoes are explicit, local document checks pass, and Claude review converges with `VERDICT: AGREE`. |
| Veto diagnostics | Missing inherited anchor; missing launch artifact; absent scalar-before-implementation rule; absent tests-passed-but-wrong-question veto; blurred KSC/actual-SV separation; Claude nonconvergence; any attempt to start runtime or implementation work. |
| Explanatory diagnostics | Naming consistency, artifact linkage, and local grep coverage. |
| Not concluded | No scalar contract pass, no code/test/benchmark classification, no route decision, no value or gradient validation. |
| Artifact | Phase 0 result and visible execution ledger. |

## Forbidden Claims/Actions

- Do not claim the launch artifacts settle the scalar contract by themselves.
- Do not start implementation, test rewrite, benchmark, runtime, GPU, or HMC
  work in Phase 0.
- Do not treat older two-lane history as equal authority to the current
  single-target reset and derivation artifacts.
- Do not let Claude authorize execution or weaken the contract boundaries.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only if:

- all launch artifacts exist;
- all veto-diagnostic checks pass;
- any non-blocking note in the Phase 0 result is explanatory only and does not
  relax a veto condition, artifact requirement, or authority-order requirement;
- inherited authority order is written clearly in the master program;
- Claude review converges with `VERDICT: AGREE` for the launch package;
- Phase 1 subplan exists and includes objective, inherited entry conditions,
  artifacts, checks/reviews, evidence contract, forbidden claims/actions,
  handoff conditions, and stop conditions.

## Stop Conditions

- Any inherited anchor is missing or contradicted.
- The master/contract/runbook disagree on the governing scalar or route classes.
- The launch package lacks the explicit anti-drift vetoes.
- Claude review does not converge after five rounds for the same blocker.
- Continuing would require runtime, package/network, release/default, or
  unrelated dirty-worktree mutation.

## End-Of-Phase Requirements

1. Run the allowed local checks.
2. Write the Phase 0 result / close record.
3. Draft or refresh the Phase 1 subplan.
4. Review the launch package and Phase 1 subplan for consistency, boundary
   safety, and anti-drift completeness.
