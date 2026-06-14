# P57 Visible Gated Overnight-Style Execution Runbook

Date: 2026-06-11

## Status

`VISIBLE_EXECUTION_IN_PROGRESS`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

This is an overnight-style gated plan, but execution remains visible and
recoverable in the current Codex conversation.  The plan is not launched by
this document.

Allowed reviewer tool exception:

- Codex may invoke the bounded non-interactive Claude worker wrapper only for
  read-only review prompts.
- Claude worker calls must not execute phases, edit files, run experiments, or
  supervise recovery.
- If Claude does not respond, Codex must run a minimal probe.  If the probe
  responds, Codex must treat the original prompt as the problem, split it, and
  retry a smaller read-only review.  A stalled Claude review prompt is not a
  reason to stop the whole program.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-source-faithful-rank-ukf-repair-master-program-2026-06-11.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-claude-review-ledger-2026-06-11.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-visible-execution-ledger-2026-06-11.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-visible-stop-handoff-2026-06-11.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact | Required token |
| --- | --- | --- | --- | --- |
| P57-M0 | Governance And Source-Anchor Lock | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md` | `PASS_P57_M0_GOVERNANCE_SOURCE_ANCHOR` or `BLOCK_P57_M0_GOVERNANCE_SOURCE_ANCHOR` |
| P57-M1 | Author Model Callback Parity | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-result-2026-06-11.md` | `PASS_P57_M1_AUTHOR_MODEL_CALLBACK_PARITY` or `BLOCK_P57_M1_AUTHOR_MODEL_CALLBACK_PARITY` |
| P57-M2 | FixedTTSIRT Transport Contract | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m2-fixed-ttsirt-transport-contract-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m2-fixed-ttsirt-transport-contract-result-2026-06-11.md` | `PASS_P57_M2_FIXED_TTSIRT_TRANSPORT_CONTRACT` or `BLOCK_P57_M2_FIXED_TTSIRT_TRANSPORT_CONTRACT` |
| P57-M3 | Proposition-2 Marginalization | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m3-proposition2-marginalization-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m3-proposition2-marginalization-result-2026-06-11.md` | `PASS_P57_M3_PROPOSITION2_MARGINALIZATION` or `BLOCK_P57_M3_PROPOSITION2_MARGINALIZATION` |
| P57-M4 | Source KR/CDF Maps | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m4-source-kr-cdf-maps-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m4-source-kr-cdf-maps-result-2026-06-11.md` | `PASS_P57_M4_SOURCE_KR_CDF_MAPS` or `BLOCK_P57_M4_SOURCE_KR_CDF_MAPS` |
| P57-M5 | Proposal Density And Retained Sampling | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m5-proposal-density-retained-sampling-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m5-proposal-density-retained-sampling-result-2026-06-11.md` | `PASS_P57_M5_PROPOSAL_DENSITY_RETAINED_SAMPLING` or `BLOCK_P57_M5_PROPOSAL_DENSITY_RETAINED_SAMPLING` |
| P57-M6 | Full Sequential Fixed-HMC Source Loop | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m6-sequential-fixed-hmc-source-loop-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m6-sequential-fixed-hmc-source-loop-result-2026-06-11.md` | `PASS_P57_M6_SEQUENTIAL_FIXED_HMC_SOURCE_LOOP` or `BLOCK_P57_M6_SEQUENTIAL_FIXED_HMC_SOURCE_LOOP` |
| P57-M7 | Source-Faithful Rank And UKF Calibration | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m7-source-faithful-rank-ukf-calibration-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m7-source-faithful-rank-ukf-calibration-result-2026-06-11.md` | `PASS_P57_M7_SOURCE_FAITHFUL_RANK_UKF_CALIBRATION` or `BLOCK_P57_M7_SOURCE_FAITHFUL_RANK_UKF_CALIBRATION` |
| P57-M8 | Preconditioned Algorithm 5 Route | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m8-preconditioned-algorithm5-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m8-preconditioned-algorithm5-result-2026-06-11.md` | `PASS_P57_M8_PRECONDITIONED_ALGORITHM5` or `BLOCK_P57_M8_PRECONDITIONED_ALGORITHM5` |
| P57-M9 | Spatial SIR Validation Ladder | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m9-spatial-sir-validation-ladder-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m9-spatial-sir-validation-ladder-result-2026-06-11.md` | `PASS_P57_M9_SPATIAL_SIR_VALIDATION_LADDER` or `BLOCK_P57_M9_SPATIAL_SIR_VALIDATION_LADDER` |
| P57-M10 | P30 Documentation And Claim Reconciliation | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m10-p30-doc-claim-reconciliation-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m10-p30-doc-claim-reconciliation-result-2026-06-11.md` | `PASS_P57_M10_P30_DOC_CLAIM_RECONCILIATION` or `BLOCK_P57_M10_P30_DOC_CLAIM_RECONCILIATION` |
| P57-M11 | Integration Closeout | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m11-integration-closeout-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m11-integration-closeout-result-2026-06-11.md` | `PASS_P57_M11_INTEGRATION_CLOSEOUT` or `BLOCK_P57_M11_INTEGRATION_CLOSEOUT` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the reviewed P57 master program be executed visibly, phase by phase, so BayesFilter repairs Zhao-Cui source-route transport, marginalization, proposal correction, sequential loop, rank/UKF calibration, preconditioning, spatial SIR validation, and P30 claim reconciliation without drifting into invented routes? |
| Baseline/comparator | P57 master program and subplans; P56 source-anchor audit; Zhao-Cui paper/source anchors; P57 Claude review ledger; project governance in `AGENTS.md`. |
| Primary pass criterion | Every phase either emits its required pass/block token with result artifacts and Claude read-only review, or stops with a human-required blocker after the repair loop.  Source-faithful claims require the phase gates and claim-to-phase matrix in P57-M11. |
| Veto diagnostics | Missing source/paper anchors; local/operator/all-grid route promoted to source-faithful; UKF promoted to truth; old `R_eff` rank route used as final selector; proposal denominator not tied to `eval_pdf(sirt,r)` semantics; previous retained marginalization skipped; rank or branch choices mutate inside likelihood; proxy metrics promoted to correctness. |
| Explanatory diagnostics | Static audits, focused CPU-only pytest, compile checks, source-anchor ledgers, low-dimensional analytic tie-outs, same-route rank convergence, UKF scout manifests, replay diagnostics, finite value/gradient checks, memory forecasts, and Claude reviews. |
| Not concluded | No HMC readiness, d=50/d=100 correctness, adaptive TT-cross parity, S&P 500 reproduction, smoothing support, or source-faithful spatial SIR success unless the corresponding P57 phase and claim gate explicitly passes. |
| Artifacts | P57 visible execution ledger, phase results, manifests, implementation diffs, P30 update, Claude review trail, final stop handoff, and closeout. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Codex is visible supervisor/executor | User instruction and template | Keeps execution recoverable and inspectable. | Detached agent hides state and cannot recover safely. | No detached commands in runbook. | Required |
| Claude is read-only reviewer | User instruction and template | Independent critique without uncontrolled edits. | Claude edits files, runs experiments, or launches agents. | Prompt says read-only; Codex inspects diff/status. | Required |
| P57 supersedes P52/P53 for source-faithful claims | P57 master program and P56 audit | Old route-rank work was tied to local/operator route. | Old `R_eff`/UKF route closes the wrong claim. | M0/M7 claim checks. | Reviewed |
| `BLOCK_SOURCE_UNGROUNDED` is binding | P57 master, P56 audit, user governance correction | Prevents source drift. | Agent invents substitute algorithm. | Each phase must cite paper/source anchors. | Required |
| CPU-only by default | `AGENTS.md` GPU policy and ordinary phase needs | Avoids sandbox GPU ambiguity and keeps tests reproducible. | GPU claims from blocked sandbox. | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`. | Default |
| TensorFlow/TFP for differentiable implementation | `AGENTS.md` backend policy | BayesFilter-owned gradient-bearing code must use TF/TFP unless reviewed exception. | NumPy prototype promoted to implementation. | Static backend checks in implementation phases. | Project policy |
| Repair loop continues for fixable blockers | User instruction and template | Avoids stopping for no valid reason. | Infinite churn or criteria drift. | Five Claude-review-round limit per blocker. | Required |

## Skeptical Plan Audit

Initial audit status: `RUNBOOK_DRAFT_AUDIT_PASS_NOT_LAUNCHED`.

The reviewed P57 master program is a valid execution target, but execution must
not begin until the user approves the anticipated Claude and local validation
commands listed below.  The runbook follows the visible template and does not
start a detached supervisor.

Before executing any phase, Codex must record a skeptical audit in chat and in
the execution ledger for material phases.

Check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the phase plan or write a blocker
note before running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites and dependency gates.
   - Restate the phase evidence contract in chat and ledger.
   - Confirm the command set is covered by user approvals.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
   - The result artifact must emit exactly one required pass or block token
     from the phase index.
4. `PASS_REVIEW`
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan.
   - Get Claude review when material.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Write a blocker result.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes, the required phase pass
     token appears in the result artifact, and Claude returns
     `VERDICT: AGREE`.
   - If a block token appears, enter `REPAIR_LOOP` for fixable blockers or
     write the visible stop handoff for human-required blockers.
   - Stop and write the handoff if a human-required blocker appears.

## Continuation Rule

A clean phase boundary is not a stop condition.  After a phase passes focused
validation and Claude read-only review, Codex must immediately advance to the
next unpassed phase in this same visible supervisor/executor conversation.

Routine phase completion must update the execution ledger, but it must not be
recorded as a stop.  The stop handoff is reserved for true stop states:

- a human-required blocker from the stop-condition list;
- Claude/Codex non-convergence after five review rounds for the same blocker;
- a context or tool interruption that prevents safe continuation;
- an explicit user pause/stop request;
- a required approval that was not already anticipated in this runbook;
- final completion of P57-M11.

If no true stop state exists, continue the phase index in order:
P57-M0 -> P57-M1 -> P57-M2 -> P57-M3 -> P57-M4 -> P57-M5 -> P57-M6 ->
P57-M7 -> P57-M8 -> P57-M9 -> P57-M10 -> P57-M11.

## Invalid Stop Reasons

Codex must not stop merely because:

- a test failed but the failure is local and fixable;
- Claude requested a concrete revision;
- a result artifact needs metadata, a token, a manifest, or wording repair;
- a command selected the wrong test subset;
- an unrelated dirty worktree file exists;
- a first Claude prompt stalls but a narrower read-only prompt can be tried;
- a phase completed normally and the next phase exists;
- a source-faithfulness issue is fixable by reading the author source and
  patching the implementation or plan.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default backend or numerical policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.

## Claude Read-Only Review Template

Use Claude only as reviewer.  The prompt must say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review:
- <phase result / blocker plan / implementation diff / final decision>

Check:
- wrong baseline;
- proxy metrics promoted to pass criteria;
- missing stop condition;
- unfair comparison;
- hidden assumption;
- stale context;
- environment mismatch;
- unsupported claim;
- artifact mismatch;
- source/paper anchor mismatch;
- route drift from Zhao-Cui SIRT/IRT retained-object semantics.

End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

Codex must preserve the review artifact and inspect whether Claude actually
remained read-only.

## Claude Nonresponse Protocol

For any Claude review:

1. If the first review prompt does not respond in a reasonable window, do not
   assume Claude is unavailable.
2. Run a minimal read-only probe through the same approved Claude worker.
3. If the probe responds, classify the original prompt as malformed or too
   large, split it into smaller read-only review prompts, and retry.
4. If the probe also fails, record a Claude-access blocker in the execution
   ledger and stop only if the review is required for a material phase gate.

## Anticipated Approval Requests

For smooth visible execution of the whole P57 program, ask the user to approve
the following before launch:

1. Escalated `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh`
   for read-only Claude Opus review prompts, blocker-plan reviews, small
   Claude probes, and final closeout review.
2. CPU-only local validation commands:
   - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q ...`
   - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q <focused tests>`
3. Static inspection and hygiene commands:
   - `rg ...`
   - `sed -n ...`
   - `git status --short ...`
   - `git diff --check ...`
   - `git diff --stat ...`
4. File edits inside `/home/chakwong/BayesFilter` using Codex `apply_patch`
   for P57 implementation, tests, result artifacts, ledgers, and P30 LaTeX
   documentation updates.
5. CPU-only TensorFlow/TensorFlow Probability imports and focused tests under
   the same CPU-hiding environment.

No anticipated approval is requested for:

- network fetches;
- package installation;
- GPU tests or benchmarks;
- detached execution;
- destructive git commands;
- broad interactive `claude`;
- broad `python` or `bash` approvals outside the narrow commands above.

If any of those become necessary, Codex must stop and ask for separate approval.

## Pre-Launch State

`NOT_LAUNCHED`.

No P57 execution phase has started under this runbook.  The next safe action,
after user approval, is P57-M0 `PRECHECK`.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- tests/benchmarks actually run;
- unresolved blockers;
- what was not concluded;
- safest next human decision, if any.
