# P86 Phase 6S Subplan: Adaptive Rank-5 Preflight And Guard

Date: 2026-06-25

Status: `REVIEWED_READY_FOR_NO_FIT_PREFLIGHT_GUARD_EXECUTION`

## Phase Objective

Create a dedicated no-fit preflight and exact-command guard for a future
adaptive rank-5 same-route Zhao-Cui SIR comparator rerun, after the reviewed
Phase 6R tiny adaptive-training smoke.

This phase must make the future rank-5 rerun executable and auditable, but it
must not run the long rank-5 fit. The phase ends by writing an approval-ready
exact command or by blocking if the command/guard/evidence contract cannot be
made coherent.

## Entry Conditions Inherited From Previous Phase

- P86 Phase 6 remains a reviewed blocker:
  `BLOCK_P86_PHASE6_RANK_DEGREE_CONVERGENCE_NOT_ESTABLISHED_REVIEWED`.
- The old fixed-budget rank-5 comparator artifact exists but is
  protocol-incomplete for convergence interpretation because it stopped at max
  fixed steps while the loss was still dropping:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank5-comparator-fit-2026-06-24.json`.
- Phase 6R training protocol repair passed reviewed:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-training-protocol-repair-result-2026-06-24.md`.
- Phase 6R tiny adaptive scheduler smoke passed reviewed:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-tiny-adaptive-training-smoke-result-2026-06-25.md`.
- ALS training is historical/buggy/stale for fixed-variant Zhao-Cui and must
  not be revived.
- Any future fitting must use the training-base route:
  `training_base_optimizer`, `TrainableFunctionalTT`, `P75ObjectiveBatch`, and
  Adam.
- No human approval exists for any long adaptive rank-5 rerun.

## Skeptical Plan Audit

Potential flaws checked before execution:

- Wrong baseline: the old rank-5 artifact is not a failed scientific
  comparator; it is an undertrained/protocol-incomplete comparator.
- Proxy promotion: validation residual may drive LR reduction and veto
  overfitting, but it is not a production criterion or posterior correctness
  proof.
- Missing stop conditions: the phase must stop before running the long
  adaptive fit and must block if exact guard tests fail.
- Unfair comparison: the future adaptive rank-5 rerun must preserve the same
  route, target, rank, basis, domain, measure, cloud separation, and audit
  non-tuning boundary as the old Phase 6 comparator.
- Hidden assumptions: more parameters already have a larger training floor
  (`20 * P_theta`), but more optimization steps are needed; this phase freezes
  a max-step ceiling plus validation plateau policy instead of treating a fixed
  step count as convergence.
- Environment mismatch: the future command remains CPU-hidden/non-production
  unless a later reviewed GPU plan changes the execution target.
- Artifact mismatch: if the preflight JSON does not include the exact command,
  adaptive protocol, validation policy, serialization policy, output path, and
  nonclaims, it cannot answer the stated question.

Audit result: proceed with a no-fit preflight/guard implementation only. Do not
run the long adaptive rank-5 rerun in this phase.

## Required Artifacts

- Phase 6S subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-adaptive-rank5-preflight-guard-subplan-2026-06-25.md`
- Phase 6S no-fit preflight JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-preflight-2026-06-25.json`
- Reserved future adaptive rank-5 output path:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-comparator-fit-2026-06-25.json`
- Phase 6S result / close record:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-adaptive-rank5-preflight-guard-result-2026-06-25.md`
- Phase 6S approval request, only if local checks and Claude review pass:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-adaptive-rank5-approval-request-2026-06-25.md`
- Updated visible execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md`

## Required Checks / Tests / Reviews

- Implement a new guarded Phase 6S preflight path in
  `scripts/p86_author_lagrangep_phase5_budget_fit.py`.
- Add focused tests in `tests/highdim/test_p86_phase5_budget_preflight.py`
  covering:
  - frozen adaptive rank-5 command string;
  - no-fit preflight JSON schema/status;
  - adaptive-training protocol fields;
  - validation holdout separate from audit cloud;
  - trained-core serialization required;
  - exact guard accepts the frozen adaptive command;
  - exact guard rejects drift in every frozen command-defining parameter,
    including output path, preflight path, target dimension, fit rank, training
    sample count, holdout sample count, audit sample count, optimizer batch
    size, prefit steps, train steps, learning rate, max seconds, memory cap,
    train/holdout/audit seed policy, adaptive-training flag, validation check
    interval, plateau patience, plateau minimum delta, LR reduction factor,
    minimum learning rate, early-stop LR-drop limit, and trained-core
    serialization flag.
- Run CPU-hidden local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p86_phase5_budget_preflight.py tests/highdim/test_p86_author_lagrangep_fit_smoke_runner.py tests/highdim/test_p86_downstream_author_route_wiring.py tests/highdim/test_p86_lagrangep_mass_integral.py tests/highdim/test_p86_algebraic_measure_contract.py
git diff --check -- scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-adaptive-rank5-preflight-guard-subplan-2026-06-25.md
```

- Claude read-only bounded review is required on the subplan before
  implementation.
- Claude read-only bounded review is required on the Phase 6S result before
  requesting approval for the long adaptive rank-5 rerun.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the runner freeze and guard a same-route adaptive rank-5 comparator rerun protocol without executing the fit? |
| Baseline/comparator | Baseline is the reviewed old Phase 6 fixed-budget rank-5 artifact and the reviewed Phase 6R tiny adaptive smoke. Comparator is the future adaptive rank-5 command, not executed in this phase. |
| Primary criterion | A no-fit Phase 6S preflight JSON is written with exact command/path fidelity, same-route rank-5 budget, adaptive-training protocol, validation-monitor policy, trained-core serialization requirement, and approval boundary; focused tests pass. |
| Veto diagnostics | Any command drift; route/basis/domain/measure/backend mismatch; missing adaptive protocol; missing validation holdout; audit cloud used for tuning; missing trained-core serialization; stale ALS route; long fit executed; unsupported convergence/production claim. |
| Explanatory diagnostics | Planned sample count, optimizer batch size, max step ceiling, validation check interval, LR schedule, early-stop rule, memory forecast, runtime cap, seed/cloud policy, and exact output paths. |
| Not concluded | No rank convergence, degree convergence, posterior correctness, KR closure, HMC readiness, LEDH comparison, scale, GPU performance, production readiness, or default-policy change. |
| Artifact | Phase 6S preflight JSON and result record. |

## Candidate Adaptive Rank-5 Protocol To Freeze

The initial candidate command should preserve the old Phase 6 same-route rank-5
data budget and cloud seeds, while replacing fixed-budget exhaustion with a
validation-driven adaptive protocol:

- target dimension: `36`
- fit rank: `5`
- training sample count: `567600`
- holdout sample count: `65536`
- audit sample count: `65536`
- optimizer identity: `training_base_optimizer` with Adam
- optimizer batch size: `4096`
- prefit steps: `0`
- max train steps: `1024`
- learning rate: `0.001`
- validation check interval: every `16` train steps
- plateau patience: `4` validation checks
- plateau minimum improvement: `0.000001`
- LR reduction factor: `0.5`
- minimum learning rate: `0.000001`
- early stop after LR drops: `4`
- serialize trained cores: required
- max seconds: `14400`
- memory cap: `12288` MiB
- train prior seed: `8301`
- train process-noise seed: `8401`
- holdout prior seed: `9301`
- holdout process-noise seed: `9401`
- audit prior seed: `9311`
- audit process-noise seed: `9501`
- output path:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-comparator-fit-2026-06-25.json`

If these parameters fail a focused preflight check or Claude review, patch this
same subplan visibly and rerun focused checks/review. Do not silently swap the
protocol after review.

## Forbidden Claims / Actions

- Do not run the long adaptive rank-5 fit in Phase 6S.
- Do not treat the old fixed-budget rank-5 artifact as scientific evidence
  against the Zhao-Cui route.
- Do not use ALS training, legacy bounded smoke artifacts, or audit data for
  tuning.
- Do not change route, basis, domain, measure convention, target, rank, or
  cloud policy while calling the result a same-route rank-5 comparator.
- Do not claim rank convergence from validation loss, fit residual, or a
  preflight artifact.
- Do not claim production readiness, HMC readiness, LEDH superiority, GPU
  performance, posterior correctness, KR closure, or source-faithful author
  TT-cross training.
- Do not ask for long-run approval until the preflight/guard result is locally
  checked and Claude-reviewed.

## Exact Next-Phase Handoff Conditions

Phase 6T adaptive rank-5 rerun approval may be requested only if:

- the Phase 6S subplan receives `VERDICT: AGREE` or converges after at most
  five review loops;
- the runner writes a Phase 6S no-fit preflight JSON with status ready;
- the exact adaptive command in the preflight matches the runner constant and
  reserved output path;
- focused local checks pass;
- the exact-guard tests cover all frozen command-defining parameters rather
  than only adaptive scheduler fields;
- the Phase 6S result receives Claude `VERDICT: AGREE`;
- the approval request states the exact command and preserves nonclaim
  boundaries.

Phase 7 correctness bridge still may not proceed unless a later reviewed Phase
6 convergence ledger establishes or precisely blocks rank/degree convergence.

## Stop Conditions

Stop if:

- Claude requests a material subplan revision that cannot be fixed within five
  review loops;
- exact same-route adaptive rank-5 command fidelity cannot be implemented;
- focused tests fail and the failure is not immediately fixable;
- preflight JSON cannot represent adaptive protocol and serialization policy;
- any long fitting command is accidentally needed to validate the phase;
- command approval is unavailable for a future long run;
- a claim would depend on validation loss as a production or correctness
  metric.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 6S result / close record;
3. draft or refresh the Phase 6T adaptive rank-5 execution approval request or
   blocker record;
4. review the next subplan/request for consistency, correctness, feasibility,
   artifact coverage, boundary safety, and stop conditions.

## Claude Review Status

Iteration 1 returned `VERDICT: REVISE`.

Summary:

- Claude agreed the subplan is mostly well-scoped and boundary-aware.
- Claude agreed wrong-baseline handling, validation-loss proxy boundaries,
  stop-before-long-fit boundaries, audit-cloud non-tuning, ALS exclusion, and
  nonclaim boundaries are strong.
- Claude requested revision because the exact-guard test list promised exact
  command fidelity but only explicitly listed a subset of frozen parameters.

Patch:

- The required guard tests now require rejection of drift in every frozen
  command-defining parameter, including path, budget, optimizer, seed, adaptive
  scheduler, and serialization fields.

Iteration 2 returned `VERDICT: REVISE`.

Summary:

- Claude agreed the subplan is close and strong on scope, artifacts, evidence
  contract, Phase 6R dependency, and improved guard language.
- Claude requested one more revision because the candidate protocol block did
  not explicitly freeze holdout/audit seeds and optimizer identity at the same
  specificity as other command-defining parameters.

Patch:

- The candidate adaptive rank-5 protocol now explicitly freezes
  `training_base_optimizer` with Adam, train seeds, holdout seeds, and audit
  seeds.

Iteration 3 returned `VERDICT: AGREE`.

Summary:

- Claude agreed the revision resolves the freeze gap from iteration 2.
- Claude agreed the subplan is internally consistent, feasible,
  artifact-complete, and boundary-safe for a no-fit Phase 6S preflight/guard.
- Claude agreed the optimizer route and train/holdout/audit seeds are now
  frozen at the same specificity as the other command-defining fields.
- Claude noted one non-blocking soft spot: the evidence contract mentions a
  memory forecast while the candidate protocol lists a memory cap. Claude did
  not block because the forecast is explanatory and the phase's primary gate
  is exact command fidelity and guardability.

Verdict:

```text
VERDICT: AGREE
```
