# P88 Phase 2A Subplan: P88-Named Runner/Manifest Repair

Date: 2026-06-27

Status: `DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

## Phase Objective

Resolve the Phase 2 runner-identity blocker without fitting, training, GPU
execution, or TensorFlow degree-comparator computation. Add a minimal P88-named
degree-comparator preflight/fit artifact identity path to the existing guarded
runner surface so Phase 2 can later launch exact reviewed P88 commands instead
of reusing P86 path-bound commands.

This phase is a no-fit implementation and test repair only. It may prepare a
P88-named no-fit preflight manifest and exact guard coverage, including one
CPU-hidden runner invocation solely to emit the no-fit JSON manifest, but it
must not execute the future degree-comparator fit or treat the manifest
generation as scientific/runtime evidence.

## Entry Conditions Inherited From Previous Phase

- Phase 1 closed reviewed with the degree-convergence protocol frozen.
- Phase 2 blocker subplan closed reviewed and selected blocker-resolution
  planning, not fitting.
- Current execution is blocked by
  `BLOCK_P88_PHASE2_P86_PATH_BOUND_RUNNER_GUARD` because the Phase 6Y
  degree-comparator preflight command, fit command, expected preflight output,
  expected fit output, and fit-argument lookup are bound to P86 artifact paths.
- P87 baseline remains `D18_SOURCE_ROUTE_EXECUTION_ONLY`.
- `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE` remains blocked until a reviewed Phase
  2 degree-convergence result passes.
- `D18_CORRECTNESS_CANDIDATE`, HMC readiness, production readiness, GPU
  readiness, and default-policy changes remain out of scope.

## Required Artifacts

- This reviewed subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2a-p88-named-runner-manifest-repair-subplan-2026-06-27.md`
- Implementation target:
  `scripts/p86_author_lagrangep_phase5_budget_fit.py`
- Focused test target:
  `tests/highdim/test_p86_phase5_budget_preflight.py`
- P88 no-fit preflight artifact path to reserve:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json`
- P88 future fit artifact path to reserve but not create in Phase 2A:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json`
- Phase 2A result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2a-p88-named-runner-manifest-repair-result-2026-06-27.md`
- Refreshed Phase 2 execution subplan or exact command manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-subplan-2026-06-27.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-visible-execution-ledger-2026-06-27.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-claude-review-ledger-2026-06-27.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-visible-stop-handoff-2026-06-27.md`

## Required Checks/Tests/Reviews

Before implementation:

```bash
rg -n "BLOCK_P88_PHASE2_P86_PATH_BOUND_RUNNER_GUARD|reserved_preflight_output_path_status|reserved_fit_output_path_status|PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT|PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_OUTPUT|_requested_output" scripts/p86_author_lagrangep_phase5_budget_fit.py docs/plans/bayesfilter-highdim-zhao-cui-p88-phase1-degree-convergence-protocol-result-2026-06-27.md docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-subplan-2026-06-27.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p88*.md
```

Claude read-only bounded review of this subplan is required before code edits.

After implementation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_p86_phase5_budget_preflight.py -k "p88_phase2 or phase6y_exact_guard or phase6y_cli_writes_no_fit_preflight_without_future_fit" -q
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --p88-phase2-degree-comparator-preflight --output docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json >/tmp/p88_phase2_degree_preflight_json_check.json
test ! -e docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json
rg -n "P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT|P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_OUTPUT|--p88-phase2-degree-comparator-preflight|reserved_preflight_output_path_status|reserved_fit_output_path_status" scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
git diff --check -- scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p88*.md
```

Claude read-only bounded review of the Phase 2A result and refreshed Phase 2
execution subplan is required before any Phase 2 fit command can be considered.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the P86-path-bound degree-comparator runner guard be repaired into a P88-named no-fit artifact path without changing the degree protocol or running a fit? |
| Baseline/comparator | Existing Phase 6Y P86 degree-comparator guard and monkeypatched no-fit test; Phase 1 protocol freeze; Phase 2 blocker subplan. |
| Primary criterion | Focused tests pass and the P88 preflight JSON records P88 preflight and future-fit artifact identities with `reserved_preflight_output_path_status == ok`, `reserved_fit_output_path_status == ok`, `fit_executed == false`, and the future fit artifact absent. |
| Veto diagnostics | Future fit artifact is created; TensorFlow fitting/training or degree-comparator computation executes; P86 artifact path is represented as fresh P88 execution; exact guard accepts wrong output/preflight paths; Phase 2A changes degree convergence criteria after seeing results; ALS training reappears; audit data is used for tuning; non-default basis is called source-faithful. |
| Explanatory diagnostics | P88 command strings, expected-fit-args mapping, no-fit payload status, candidate fit command, path-reservation statuses, test names, diff hygiene. |
| Not concluded | Degree convergence, correctness, derivative readiness, HMC readiness, production readiness, GPU readiness, default-policy readiness, or scientific validity. |
| Artifact | Phase 2A result, P88 no-fit preflight JSON, refreshed Phase 2 execution subplan, ledgers, and stop handoff. |

## Skeptical Audit Before Execution

- Wrong baseline check: compare only against the existing P86 Phase 6Y guard
  surface and P88 Phase 1 protocol, not against old ALS or unrelated branches.
- Proxy metric check: no residual, holdout, validation, or audit metric can pass
  Phase 2A; only path identity and no-fit guard correctness can pass it.
- Stop-condition check: stop if adding P88 artifact identity requires changing
  fit hyperparameters, degree protocol, source-route claims, or runtime policy
  beyond the one CPU-hidden no-fit manifest-generation exception stated here.
- Unfair-comparison check: Phase 2A cannot rank P86 and P88 results because it
  does not run a fit.
- Hidden-assumption check: the future P88 fit command must remain the same
  Phase 1 frozen order-3/rank-4/zero-L1 comparator except for P88 artifact
  names and status labels.
- Stale-context check: rerun the required greps before implementation to ensure
  the guard surface has not drifted.
- Environment mismatch check: the only runner command is CPU-hidden
  `CUDA_VISIBLE_DEVICES=-1` no-fit preflight generation; its runner import may
  load TensorFlow dependencies, but no fitting/training or degree-comparator
  computation is authorized and no GPU/CUDA evidence is interpreted.
- Artifact-answer check: generated JSON must answer path-reservation and
  command-identity questions only.

## Forbidden Claims/Actions

- Do not run `--fit` or any training command in Phase 2A.
- Do not run TensorFlow fitting/training or degree-comparator computation; the
  only permitted runner invocation is CPU-hidden no-fit manifest generation.
- Do not create
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json`.
- Do not change the Phase 1 frozen hyperparameters, basis order, rank, L1 policy,
  sample counts, seeds, plateau policy, or audit split.
- Do not treat P86 artifacts as fresh P88 execution.
- Do not promote `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE`.
- Do not claim correctness, gradient correctness, HMC readiness, production
  readiness, GPU readiness, or default-policy readiness.
- Do not revive historical ALS training.
- Do not use audit data for tuning.
- Do not run GPU, HMC, LEDH, production, package-install, network-fetch, or
  destructive git/filesystem commands.

## Exact Next-Phase Handoff Conditions

Phase 2 can proceed from blocker repair to exact degree-convergence execution
planning only if all are true:

- this subplan receives bounded Claude `VERDICT: AGREE` before implementation;
- focused tests and local checks pass after implementation;
- the P88 no-fit preflight JSON exists and records the P88 preflight/future-fit
  path identities as ready;
- the P88 future fit artifact path remains absent;
- the Phase 2A result is written and reviewed;
- the refreshed Phase 2 execution subplan names exact future fit command(s),
  runtime budget, stop conditions, evidence contract, and review requirements.

If these conditions pass, the next handoff is to:

`docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-subplan-2026-06-27.md`

with status `P88_PHASE2A_REVIEWED_CLOSED_PHASE2_EXECUTION_PLANNING_READY`.

## Stop Conditions

- Claude review does not converge after five rounds for this subplan or result.
- The existing runner guard cannot support P88-named artifact identities without
  broad restructuring.
- The no-fit preflight imports or executes training/fitting unexpectedly.
- The exact guard accepts drifted output paths, preflight paths, frozen
  hyperparameters, sample counts, seeds, or basis settings.
- The future fit artifact is created during Phase 2A.
- Required local checks fail and the fix would exceed this no-fit repair scope.

## End-Of-Phase Requirements

1. Run the required pre-implementation local checks.
2. Send this subplan to bounded Claude read-only review.
3. If review revises, patch this subplan visibly, rerun focused checks, and
   retry review up to five rounds.
4. If review agrees, implement only the no-fit runner/manifest repair and
   focused tests named here.
5. Run all required post-implementation checks.
6. Write the Phase 2A result and refresh the Phase 2 execution subplan, ledgers,
   and stop handoff before final checks.
7. Run final diff hygiene over touched code, tests, and P88 artifacts.
8. Send the Phase 2A result and refreshed Phase 2 execution subplan to bounded
   Claude read-only review.
9. Advance only if reviews agree; otherwise patch the relevant artifact and
   repeat focused checks/review within the five-round cap, or write a blocker
   result and stop.
