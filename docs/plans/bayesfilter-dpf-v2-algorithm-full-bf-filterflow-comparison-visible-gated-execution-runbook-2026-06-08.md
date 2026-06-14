# DPF V2 Algorithm Full BF/FilterFlow Visible Gated Execution Runbook

Date: 2026-06-08

## Status

`COMPLETE_PASS_FULL_COMPARISON`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `scripts/dpf_v2_algorithm_full_comparison_live_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

All phase execution must be visible in this dialogue. The chat transcript,
ledger, phase result artifacts, and stop handoff are the recovery mechanism.

If the user wants detached overnight execution, stop and write a separate
detached-supervisor plan. This runbook is for visible, recoverable execution
inside the current conversation.

## Supersession Of Detached Route

This runbook supersedes the prior live/detached launch route as the active
execution mechanism:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-live-gated-execution-plan-2026-06-07.md`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-live-gated-execution-human-risk-acceptance-amendment-2026-06-08.md`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-live-gated-execution-launch-compatibility-amendment-2026-06-08.md`

Those files remain historical records only. They are not authorization to use
the live supervisor scripts for this execution.

The earlier live attempt produced incidental P0 artifacts after the user intent
was misunderstood. Those artifacts may be read as context, but they do not mean
visible execution has begun. A phase can pass under this runbook only after
Codex performs the visible state machine for that phase in this conversation.

For P0, the visible-route result and JSON artifacts are:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-visible-result-2026-06-08.md`
- `experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_p0_visible_governance_2026-06-08.json`

The inherited P0 artifacts dated 2026-06-07 are historical detached-route
context only.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-master-program-2026-06-07.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-claude-review-ledger-2026-06-07.md`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-reset-memo-2026-06-07.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-visible-execution-ledger-2026-06-08.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-visible-stop-handoff-2026-06-08.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact | Required pass token |
| --- | --- | --- | --- | --- |
| P0 | Governance | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-visible-result-2026-06-08.md` | `PASS_P0_READY_FOR_P1` |
| P1 | Architecture | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p1-architecture-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p1-architecture-result-2026-06-07.md` | `PASS_P1_ARCHITECTURE_READY_FOR_P2` |
| P2 | Bootstrap-OT contracts | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p2-bootstrap-ot-contracts-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p2-bootstrap-ot-contracts-result-2026-06-07.md` | `PASS_P2_BOOTSTRAP_OT_CONTRACTS_READY_FOR_P3` |
| P3 | Bootstrap-OT values | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p3-bootstrap-ot-values-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p3-bootstrap-ot-values-result-2026-06-07.md` | `PASS_P3_BOOTSTRAP_OT_VALUES_READY_FOR_P4` |
| P4 | Bootstrap-OT gradients | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p4-bootstrap-ot-gradients-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p4-bootstrap-ot-gradients-result-2026-06-07.md` | `PASS_P4_BOOTSTRAP_OT_GRADIENTS_READY_FOR_P5` |
| P5 | LEDH-PFPF-OT contracts | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-result-2026-06-07.md` | `PASS_P5_LEDH_PFPF_OT_CONTRACTS_READY_FOR_P6` |
| P6 | LEDH-PFPF-OT values | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p6-ledh-pfpf-ot-values-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p6-ledh-pfpf-ot-values-result-2026-06-07.md` | `PASS_P6_LEDH_PFPF_OT_VALUES_READY_FOR_P7` |
| P7 | LEDH-PFPF-OT gradients | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p7-ledh-pfpf-ot-gradients-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p7-ledh-pfpf-ot-gradients-result-2026-06-07.md` | `PASS_P7_LEDH_PFPF_OT_GRADIENTS_READY_FOR_P8` |
| P8 | Closeout | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p8-closeout-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-closeout-result-2026-06-07.md` | `PASS_FULL_COMPARISON` or `BLOCKED_WITH_REVIEWED_CLASSIFICATION` |

## Required V2 Row Order

Every phase must carry these rows in this exact order:

1. `lgssm_2d_h25_rich`
2. `sv_1d_h18_rich`
3. `range_bearing_4d_h20_rich`
4. `structural_ar1_quadratic_h16`
5. `spatial_sir_j3_rk4`
6. `predator_prey_rk4`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Codex execute the reviewed DPF V2 full algorithm BF/FilterFlow comparison from P0 through P8 visibly in this dialogue, with Claude used only as a critical read-only reviewer, while preserving the master program's no-oracle, no-student, no-FilterFlow-mutation, and fixed-contract gates? |
| Baseline/comparator | BayesFilter and BayesFilter-owned FilterFlow-side adapters execute the same frozen JSON contracts. Neither side is an oracle. |
| Primary pass criterion | Each phase reaches its declared pass token only after the visible state machine is completed in this conversation, required artifacts exist, primary criteria pass, veto diagnostics pass, and Claude returns `VERDICT: AGREE` for material phase results or repairs. |
| Veto diagnostics | `.localsource/filterflow` mutation; student implementation commands or metrics; treating BayesFilter, FilterFlow, students, TT, dense quadrature, paper tables, or simulated truth as oracle; row disappearance; unexecuted required gradient knobs; contract, tolerance, scalar, fixture, branch, OT setting, or gradient-knob changes after seeing results without reviewed amendment; finite differences used as a gradient promotion gate; nonfinite values, densities, transport matrices, PF-PF corrections, Jacobians/logdets, or AD gradients; missing artifact; unsupported full-comparison success; Claude `VERDICT: REVISE` unresolved after five review rounds. |
| Explanatory diagnostics | Dirty worktree status, run time, ESS, filtered moments, RMSE, finite-difference ladders, local linearization residuals, transport residuals, stochastic smoke summaries, and prior incidental detached P0 artifacts. |
| Not concluded | No BayesFilter correctness proof, FilterFlow correctness proof, bootstrap-OT or LEDH-PFPF-OT scientific correctness proof, stochastic resampling distribution claim, gradient-through-random/discrete-branch claim, student implementation claim, TT/SIRT claim, paper-table claim, HMC/DSGE/GPU/scalability/deployment/production-readiness claim. |
| Artifacts | This runbook, visible execution ledger, stop handoff, P0--P8 result artifacts, phase JSON and markdown reports, command output shown in chat, and Claude read-only review entries preserved in the ledger or phase review artifacts. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible in-dialogue execution | User correction on 2026-06-08 and template `visible-gated-execution-runbook-template.md` | The user wants execution observable and recoverable from this dialogue | Codex silently reverts to detached scripts | Check command plan forbids `codex exec`, overnight launcher, detached supervisors, and background phase runners | Active route |
| Claude read-only reviewer | User request and master review pattern | Gives critical review while Codex remains supervisor/executor | Claude edits, launches agents, or changes state | Use read-only prompt and inspect output for state-changing claims | Required |
| Same frozen BF/FF contracts | Master program | Keeps comparison non-oracular and fair | One side gets different fixtures, branches, scalar, masks, or knobs | P2/P5 contract checksum gates and later runtime checksum checks | Required |
| CPU-only TensorFlow unless separate GPU plan exists | AGENTS.md GPU/CUDA policy and P0 subplan | This lane does not need GPU evidence | Hidden GPU initialization or misleading sandbox failure | Set `CUDA_VISIBLE_DEVICES=-1` before TensorFlow imports for CPU-only runs | Required |
| `.localsource/filterflow` no mutation | Master program and P0 hard gate | FilterFlow is comparator source, not an editable implementation target | Accidental local comparator edits change the baseline | Record commit/status before and after material phases | Required |
| Incidental detached P0 is not visible phase completion | User correction and prior run stop state | Prevents a mistaken launch artifact from becoming hidden evidence | P0 is skipped without visible audit or review | Ledger starts as `NOT_STARTED`; P0 must run through visible state machine | Required |

## Skeptical Plan Audit

Status: `PASS_FOR_VISIBLE_RUNBOOK_DRAFT`.

Wrong-baseline risk:

- The route change could accidentally promote old deterministic V2 evidence or
  the incidental detached P0 artifact. Control: the evidence contract states
  those artifacts are explanatory-only unless revalidated through the visible
  state machine.

Proxy-metric risk:

- ESS, RMSE, runtime, finite differences, and smoke summaries could be treated
  as promotion criteria. Control: they remain explanatory-only unless listed as
  a veto diagnostic in a phase subplan or reviewed amendment.

Missing stop-condition risk:

- Visible execution could keep going after an ambiguous blocker because the
  chat is interactive. Control: the state machine stops on missing artifacts,
  unresolved Claude `VERDICT: REVISE`, row disappearance, contract weakening,
  `.localsource/filterflow` mutation, protected user-work mutation, or human
  decision needs.

Unfair-comparison risk:

- BF and FF adapters could use different branch masks, particles, innovations,
  OT settings, scalar definitions, or gradient knobs. Control: P2 and P5 freeze
  contracts before value or gradient phases, and later phases check against
  those frozen contracts.

Hidden-assumption risk:

- Local FilterFlow does not appear to provide native LEDH proposal support.
  Control: P1 and P5 must treat LEDH as BayesFilter-owned FilterFlow-side
  adapter work and must not mutate `.localsource/filterflow`.

Stale-context risk:

- The previous detached launch plan now has misleading `LAUNCH_READY` wording.
  Control: this runbook and the reset memo mark the detached route as
  superseded for this task.

Environment-mismatch risk:

- Non-escalated GPU probes can mislead, while this lane is CPU-only. Control:
  use `CUDA_VISIBLE_DEVICES=-1` before TensorFlow imports and avoid GPU claims.

Artifact adequacy risk:

- Chat output alone could be hard to resume from. Control: each phase appends
  the visible ledger and writes the required phase result artifact; the stop
  handoff is updated before stopping.

Audit decision:

- No material flaw was found in converting the prior detached/live execution
  plan into this visible runbook. The conversion changes only the execution
  mechanism, not the scientific comparison criteria.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed to answer the
     phase question.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
4. `PASS_REVIEW`
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as read-only review.
   - For large phase reviews, split Claude review into bounded read-only
     chunks before the final verdict. Each chunk should inspect one narrow
     question over one to three files, ask for findings first, and end with
     `VERDICT: AGREE` or `VERDICT: REVISE`.
   - The final synthesis prompt should reference the chunk outcomes and only
     the minimum phase artifacts needed to decide the gate. A phase may advance
     only after the final synthesis review returns `VERDICT: AGREE`.
   - If a broad review prompt produces no output but a small probe succeeds,
     classify the issue as review-prompt sizing/usage, not a phase artifact
     failure. Restart review with smaller chunks and record that route in the
     ledger.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan.
   - Get Claude review when material.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Write a blocker result.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Claude Read-Only Review Template

Use Claude only as a reviewer. The prompt must say:

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
- artifact mismatch.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

Codex must preserve the review artifact and inspect whether Claude actually
remained read-only.

## Claude Probe And Chunked Review Rule

This rule is baked into the active visible execution plan after the P2/P5 review
transport issues and is the default Claude review route for P6 and later
material phase gates.

Before any material phase review, Codex should run a minimal read-only Claude
probe that does not ask Claude to inspect the full phase. The probe can
establish whether Claude is responsive in the current VS Code/session/auth
context, but it is not phase evidence and cannot advance a gate.

If a broad multi-file review prompt is silent or hangs while a small probe
works, classify the problem as prompt sizing or review transport, not as a
failure of the phase artifact. Restart the review using bounded chunks:

- one narrow question per chunk;
- one to three files per chunk;
- findings first;
- exact terminal verdict of `VERDICT: AGREE` or `VERDICT: REVISE`;
- final synthesis only after all required chunks agree.

For P6 and later phases, the default bounded review layout is:

1. probe: verify Claude read-only wrapper responsiveness only;
2. implementation/validator chunk: review the runner, frozen-contract
   consumption, local validation, and hard veto enforcement;
3. result/report chunk: review the phase result/report truthfulness and
   non-claim boundaries;
4. final synthesis: use only the chunk outcomes and minimum phase artifacts
   needed for the gate decision.

The phase may advance only after the final synthesis review returns
`VERDICT: AGREE`. Chunk agreement is necessary review support, not a substitute
for final phase agreement.

## Restart From Current Visible Gate

The active restart point is P8 precheck, not the detached launch route and not
a fresh hidden P0--P7 replay. P0 through P7 have already passed under the
visible state machine recorded in the ledger. P7 advanced only after final
Claude synthesis returned `VERDICT: AGREE` and promoted artifacts revalidated.

For this restart:

- keep execution in this dialogue;
- use Claude only through the read-only wrapper;
- run a small Claude probe before P8 material review;
- if the probe works but a broad review is silent, split the review into
  bounded chunks and record the prompt-sizing route in the ledger;
- do not advance from P8 until the local P8 artifact and final Claude
  synthesis review return `VERDICT: AGREE`;
- do not modify `.localsource/filterflow`, run student commands, change the P5
  LEDH contract bundle, change the P5 digest, or use finite differences as a
  promotion gate.

## Ledger Entry Template

```markdown
### <timestamp> - Phase <N> - <STATE>

Evidence contract:

- Question:
- Baseline/comparator:
- Primary criterion:
- Veto diagnostics:
- Non-claims:

Actions:

- <commands/edits/reviews>

Artifacts:

- <paths>

Gate status:

- <PASSED/BLOCKED/FAILED/IN_PROGRESS>

Next action:

- <next visible step>
```

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds;
- running any hidden, detached, or background phase execution.

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
