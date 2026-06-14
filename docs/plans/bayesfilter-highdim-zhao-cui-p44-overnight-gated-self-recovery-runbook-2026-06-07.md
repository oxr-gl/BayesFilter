# P44 Overnight Gated Self-Recovery Runbook

metadata_date: 2026-06-07
phase: P44-overnight

## Parent Plans

- P44 master program:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-cut4-zhaocui-cross-model-master-program-2026-06-07.md`
- P44 Claude plan review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-cut4-zhaocui-cross-model-claude-review-ledger-2026-06-07.md`
- P42 gradient/likelihood validation rules:
  `docs/plans/bayesfilter-highdim-zhao-cui-p42-gradient-likelihood-validation-rules-2026-06-07.md`
- P43 SV value/gradient result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p43-sv-value-gradient-cut4-zhaocui-result-2026-06-07.md`

## Current Checkpoint

- P44 master program exists with subplans M0--M8.
- P44 plan review converged at Claude iteration 2 with
  `PASS_P44_PLAN_GOVERNANCE`.
- No P44 implementation phase has passed yet. Cycle 3 successfully launched
  P44-M0, but the phase worker stopped after writing a plan and asking for
  approval, so that attempt produced no phase pass.
- Current repair checkpoint: Cycle 4 must verify the autonomous-execution
  prompt and gate-hardening repairs before relaunch.
- Next execution gate after relaunch: P44-M0 target-governance matrix.

## Purpose

Govern an overnight or unattended execution of the full P44 program. Codex is
the visible supervisor and executor. Claude is a read-only reviewer for plans,
repairs, and code/governance evidence. Codex may repair fixable implementation
or plan-gate blockers, but only inside this state machine:

```text
phase plan -> skeptical audit -> Claude plan/recovery review -> implementation
-> local evidence -> evidence audit -> result note -> Claude code/governance
review -> traceability/update -> next phase
```

The run stops only when Codex cannot recover under the runbook and Claude, as
read-only reviewer, agrees the remaining issue requires human scientific,
target-definition, governance, license, or infrastructure intervention.

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_RUNBOOK_REVIEW`.

Main drift risk: an overnight agent may continue after a failure by weakening a
tolerance, changing a fixture, replacing the baseline, skipping dense/Kalman
reference checks, or reclassifying diagnostic evidence as correctness evidence.
This runbook blocks that drift by requiring an explicit Claude pass for every
phase progression and every repair amendment.

Risks checked:

- wrong baselines: LGSSM remains exact Kalman governed; nonlinear same-target
  phases need dense/refined references before promotion;
- proxy metrics: wall time, finite values, point counts, fit residuals, and
  plots remain explanatory unless the phase contract says otherwise;
- target mismatch: M0 target-governance matrix is mandatory before M1--M8;
- missing stop conditions: long or expanded runs require wall-time/resource
  caps and pre-mortems before execution;
- unfair comparisons: CUT4 and Zhao--Cui are compared only on matched data,
  target, parameterization, horizon, and uncertainty model;
- stale context: P42/P43 nonclaims remain active until a later phase supplies
  stronger evidence.

## Evidence Contract

Question: can Codex supervise and execute P44 overnight, repair fixable failures
with Claude read-only review, and stop only for non-fixable human-intervention
blockers while preserving P42/P44 target and gradient governance?

Baseline/comparator:

- phase-specific baselines in P44-M0--M8;
- exact Kalman for LGSSM;
- dense/refined quadrature for same-target nonlinear fixtures;
- diagnostic-only nonclaim rows for SIR, predator-prey, and generalized SV
  until a shared target is defined.

Primary promotion criterion:

- each phase reaches a result note and Claude code/governance review with an
  explicit phase pass token before the next phase starts.

Veto diagnostics:

- target mismatch used as equality evidence;
- gradients compared in different parameterizations;
- finite values used as correctness proof;
- CUT4 treated as nonlinear ground truth;
- factorized panels called coupled multivariate TT;
- tolerance, fixture, baseline, dense reference, or target changed without a
  reviewed repair amendment;
- long-run resource cap or pre-mortem missing;
- Claude review exhausted five iterations without an explicit pass;
- any phase result/review pass token lacks the current run id;
- phase review-loop counts are accepted from a manifest without matching
  machine-parseable phase review-ledger records;
- the worker attempts to edit the phase gate or launch preflight as a repair
  route from inside the worker-writable launch workspace;
- a planning-only phase response is treated as progress;
- Codex and Claude agree the fix requires a human scientific/target decision.

Explanatory-only diagnostics:

- wall time, point count, fit residual, holdout residual, condition number,
  branch hash, rank, basis order, quadrature order, paired error summaries, and
  trajectory plots.

What will not be concluded:

- no HMC readiness;
- no Tier-2 likelihood/score variance claim;
- no Tier-3 Hamiltonian/leapfrog claim;
- no production analytic score API;
- no paper-scale Zhao--Cui reproduction;
- no exact native SIR/predator-prey/generalized-SV claim from closure tests.

## Phase Queue

| Order | Phase | Subplan | Required pass token |
| --- | --- | --- | --- |
| 0 | P44-M0 | `bayesfilter-highdim-zhao-cui-p44-phase0-target-governance-subplan-2026-06-07.md` | `PASS_P44_M0_CODE_GOVERNANCE` |
| 1 | P44-M1 | `bayesfilter-highdim-zhao-cui-p44-phase1-lgssm-subplan-2026-06-07.md` | `PASS_P44_M1_CODE_GOVERNANCE` |
| 2 | P44-M2 | `bayesfilter-highdim-zhao-cui-p44-phase2-cubic-additive-gaussian-subplan-2026-06-07.md` | `PASS_P44_M2_CODE_GOVERNANCE` |
| 3 | P44-M3 | `bayesfilter-highdim-zhao-cui-p44-phase3-quadratic-observation-subplan-2026-06-07.md` | `PASS_P44_M3_CODE_GOVERNANCE` |
| 4 | P44-M4 | `bayesfilter-highdim-zhao-cui-p44-phase4-nonlinear-transition-subplan-2026-06-07.md` | `PASS_P44_M4_CODE_GOVERNANCE` |
| 5 | P44-M5 | `bayesfilter-highdim-zhao-cui-p44-phase5-spatial-sir-diagnostic-subplan-2026-06-07.md` | `PASS_P44_M5_CODE_GOVERNANCE` |
| 6 | P44-M6 | `bayesfilter-highdim-zhao-cui-p44-phase6-predator-prey-diagnostic-subplan-2026-06-07.md` | `PASS_P44_M6_CODE_GOVERNANCE` |
| 7 | P44-M7 | `bayesfilter-highdim-zhao-cui-p44-phase7-generalized-sv-target-subplan-2026-06-07.md` | `PASS_P44_M7_CODE_GOVERNANCE` |
| 8 | P44-M8 | `bayesfilter-highdim-zhao-cui-p44-phase8-integration-closeout-subplan-2026-06-07.md` | `PASS_P44_M8_CODE_GOVERNANCE` |

## State Machine

Each phase must run:

```text
READY
  -> PHASE_PLAN_CONFIRMED
  -> SKEPTICAL_AUDIT_RECORDED
  -> CLAUDE_PLAN_OR_REPAIR_REVIEW_PASS
  -> IMPLEMENTED
  -> LOCAL_EVIDENCE_RUN
  -> EVIDENCE_AUDIT_RECORDED
  -> RESULT_NOTE_WRITTEN
  -> CLAUDE_CODE_GOVERNANCE_PASS
  -> TRACEABILITY_UPDATED_OR_NONCLAIM_RECORDED
  -> PHASE_PASS
```

Failure transition:

```text
LOCAL_EVIDENCE_RUN or EVIDENCE_AUDIT_RECORDED
  -> BLOCKER_CLASSIFIED
  -> REPAIR_PLAN_AMENDMENT
  -> CLAUDE_REPAIR_REVIEW_PASS
  -> REPAIR_IMPLEMENTED
  -> LOCAL_EVIDENCE_RUN
```

Stop transition:

```text
BLOCKER_CLASSIFIED
  -> HUMAN_INTERVENTION_REQUIRED
```

## Blocker Classification

Fixable without human intervention:

- implementation bug with unchanged target and tolerance;
- missing test fixture metadata;
- missing result-note field;
- missing guardrail command;
- local reference refinement too weak but fixable by a predeclared stronger
  reference inside resource caps;
- Claude-requested wording/nonclaim repair.

Requires reviewed repair amendment before continuing:

- fixture change;
- tolerance change;
- baseline/reference change;
- parameterization change;
- target-label change;
- new resource cap or long-run expansion;
- switching a phase from same-target to diagnostic-only.

Human-intervention stop:

- incompatible target interpretations;
- no feasible reference route under declared resources;
- license/governance uncertainty;
- infrastructure access unavailable after trusted rerun;
- Claude blocks five reviewed repair iterations without pass;
- Codex and Claude both classify the issue as requiring a scientific decision.

## Review Loop Rules

- Claude plan, repair, and code/governance reviews are read-only. Claude may
  inspect files and command outputs supplied by Codex, but must not implement
  phase work, edit artifacts, mutate code, launch experiments, or act as the
  phase executor.
- Claude read-only reviews require explicit pass tokens.
- Five review iterations without pass never create launch, implementation,
  repair, promotion, or next-phase authority.
- Max-five exhaustion writes a stop note and result ledger entry.
- A phase may not continue after a blocker until the amended plan receives
  explicit Claude pass.
- Phase code/governance and repair review iteration counts must be corroborated
  by machine-parseable review records in the phase Claude review ledger. The
  gate must reject duplicate, decreasing, reset, or out-of-range iteration
  histories and must require the latest bounded record to contain the expected
  pass token.

## Execution Artifacts

Required per phase:

- phase result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase{n}-{phase-slug}-result-2026-06-07.md`
- phase Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase{n}-{phase-slug}-claude-review-ledger-2026-06-07.md`
- both phase artifacts must include the exact current `run_id` and their
  latest status/verdict line must equal the required phase pass token;
- phase evidence manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase{n}-{phase-slug}-evidence-manifest-{run_id}.json`
- the evidence manifest must use schema `p44.phase_evidence.v1` and machine
  record current-run artifact paths, all state-machine evidence-chain states,
  the evidence contract, successful command records, veto-diagnostic status,
  Claude code/governance and repair-loop iteration counts, and long-run
  resource-cap/pre-mortem controls when applicable;
- the phase gate must corroborate the evidence manifest against anchored
  machine-check markers in the phase result note, Claude review ledger, and
  per-command logs; it must not accept uncorroborated manifest assertions;
- required result-note markers include `p44_evidence_manifest`,
  `p44_local_evidence_run`, `p44_evidence_audit`,
  `p44_result_note_substance`, `p44_traceability_or_nonclaim`,
  `p44_command_count`, and `p44_long_run_used`;
- required Claude review-ledger markers include `p44_evidence_manifest`,
  `p44_claude_code_governance_verdict`, and
  `p44_claude_code_governance_iterations`;
- phase Claude review ledgers must include machine-parseable
  `review_cycle`, `review_type: code_governance`, `review_iteration`, and
  `status` or `Verdict` records for the code/governance review; the latest
  bounded code/governance record must equal the phase pass token and its
  iteration must match the evidence manifest's
  `claude_code_governance.iterations`;
- if the evidence manifest reports repair iterations greater than zero, the
  phase review ledger must include a separate machine-parseable
  `review_type: repair` stream with a matching explicit
  `PASS_P44_M{n}_REPAIR_REVIEW` record at the same bounded iteration;
- every manifest command must cite a relative log path whose file contains
  `p44_run_id`, `p44_phase`, `p44_command_index`, and
  `p44_command_exit_code`;
- test files or explicit diagnostic-only blocker note;
- command manifest with git commit, environment, CPU/GPU status, seeds,
  commands, wall time, and output paths.
- phase-specific experiment plan before any command expected to exceed tiny
  local scope, defined as more than five minutes, beyond the subplan's declared
  dimension/horizon/CUT4 cap, or beyond CPU-only local tests.

Run-level artifacts:

- this runbook;
- `docs/plans/bayesfilter-highdim-zhao-cui-p44-overnight-gated-self-recovery-claude-review-ledger-2026-06-07.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p44-overnight-gated-self-recovery-execution-result-2026-06-07.md`
- detached launch log under `docs/plans/logs/`.

## Codex Supervision Contract

Codex must supervise and execute the phase queue directly:

- start at P44-M0 and proceed in queue order;
- treat the user's launch request as prior approval for autonomous execution;
- do not stop after a plan, proposal, checklist, or approval request; a
  planning-only Codex response is a phase failure;
- when a plan or repair amendment is needed, write it as an artifact, run the
  bounded read-only Claude review loop, implement the reviewed repair if it
  passes, and continue to the phase gate;
- do not start P44-M{n+1} unless the prior phase ledger contains the exact
  required pass token listed in the phase queue table and the phase result note
  plus Claude review ledger both carry the current run id;
- preserve unrelated dirty worktree changes;
- use the prelaunch tracked-dirty manifest as a protected path list and do not
  modify those already-dirty tracked files unless a human explicitly
  authorizes it;
- run implementation, experiments, evidence notes, repair amendments, phase
  gates, and stop decisions from this Codex conversation so the user can see
  progress and Codex can recover from fixable blockers;
- use CPU-only commands unless a phase explicitly needs GPU, in which case
  trusted/escalated GPU policy applies;
- create/update phase result and Claude ledgers;
- run Claude only as a read-only reviewer with explicit pass tokens;
- repair fixable blockers only through reviewed amendments;
- never treat edits to `scripts/p44_phase_gate.py`,
  `scripts/p44_overnight_gated_launch.sh`, or
  `scripts/p44_overnight_supervisor.sh` as a phase-local repair route unless
  Codex explicitly patches the runbook/launcher governance and obtains a
  read-only Claude runbook-review pass first;
- run phase gates from the source repository under Codex supervision; do not
  delegate phase gate execution to a detached worker;
- stop with a human-intervention note if max-five review exhaustion or a true
  target/science decision is reached.

## Claude Read-Only Reviewer Contract

Claude review prompts must:

- state that Claude is reviewer only, not implementer or executor;
- prohibit file edits, command execution for phase work, artifact creation, and
  mutation of source, result notes, manifests, or ledgers;
- ask for findings first, then a final exact token;
- require Claude to block on unsupported evidence, stale target assumptions,
  unfair comparisons, missing run id, missing markers, failed diagnostics, or
  manifest/ledger/log inconsistency;
- allow Claude to return pass tokens only when the supplied artifacts satisfy
  the phase contract.

## Detached Launcher Preconditions

The detached launcher is not the primary execution route for the
Codex-supervised run. If it is ever used for a narrow operational subtask, it
must refuse to start unless:

- this runbook review ledger contains `PASS_P44_OVERNIGHT_RUNBOOK`;
- the execution result status is `READY_TO_LAUNCH_AFTER_RUNBOOK_PASS`;
- both launch-preflight files carry the current human-approved review cycle and
  a review iteration no greater than five;
- launch-preflight review-cycle records must be strictly increasing with no
  duplicate or reset iteration numbers;
- the launcher must require `REVIEW_CYCLE` explicitly rather than defaulting to
  a stale review cycle;
- the latest runbook-ledger PASS record and latest execution-result READY
  record for the explicit review cycle must have the same review iteration;
- the dedicated P44 worker settings file exists;
- a prelaunch dirty manifest and tracked-dirty manifest are written to the log
  directory;
- the worker is launched with `CLAUDE_WORKER_PERMISSION_MODE=acceptEdits`, not
  `bypassPermissions`.
- `unshare` mount-namespace isolation is available;
- the run executes in an isolated launch workspace copied from the current tree
  and bind-mounted over the original repository path inside the detached
  namespace, so absolute-path writes to `/home/chakwong/BayesFilter` land in the
  copied workspace rather than the source tree.
- before the launch workspace is bind-mounted over the repository path, the
  launcher copies `scripts/p44_phase_gate.py` into a run-specific trusted gate
  directory outside the launch workspace, makes that directory read-only inside
  the detached mount namespace, passes the trusted gate path and SHA-256 to the
  supervisor, and the supervisor verifies the SHA-256 before every phase gate.
