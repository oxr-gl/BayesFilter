# P89 Visible Gated Overnight Execution Plan

Date: 2026-06-28

Status: `P89_VISIBLE_RUNBOOK_REVIEWED_AGREE`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only. Claude is not an execution authority
and cannot authorize crossing human, runtime, model-file, funding,
product-capability, default-policy, or scientific-claim boundaries.

This runbook is visible and recoverable inside the current conversation. It
must not launch detached or nested agents. Do not use:

- `codex exec`;
- detached overnight supervisor scripts;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p89-production-promotion-master-program-2026-06-28.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p89-claude-review-ledger-2026-06-28.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p89-visible-execution-ledger-2026-06-28.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p89-visible-stop-handoff-2026-06-28.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance bootstrap and P88 inheritance | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase0-governance-inheritance-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase0-governance-inheritance-result-2026-06-28.md` |
| 1 | Target manifest and same-scalar branch contract | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase1-target-manifest-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase1-target-manifest-result-2026-06-28.md` |
| 2 | Same-target source-backed value bridge design | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase2-value-bridge-design-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase2-value-bridge-design-result-2026-06-28.md` |
| 3 | Value bridge implementation and validation ladder | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase3-value-bridge-validation-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase3-value-bridge-validation-result-2026-06-28.md` |
| 4 | Source-route analytical derivative design | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase4-derivative-design-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase4-derivative-design-result-2026-06-28.md` |
| 5 | Analytical derivative implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase5-derivative-implementation-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase5-derivative-implementation-result-2026-06-28.md` |
| 6 | FD validation of same-scalar analytical gradient | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase6-fd-gradient-validation-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase6-fd-gradient-validation-result-2026-06-28.md` |
| 7 | HMC readiness gate | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase7-hmc-readiness-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase7-hmc-readiness-result-2026-06-28.md` |
| 8 | GPU/XLA production execution gate | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase8-gpu-xla-production-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase8-gpu-xla-production-result-2026-06-28.md` |
| 9 | Training policy, packaging, CI, and docs gate | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase9-production-packaging-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase9-production-packaging-result-2026-06-28.md` |
| 10 | Final production promotion decision | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase10-final-production-decision-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase10-final-production-decision-result-2026-06-28.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Zhao-Cui SIR d18 be promoted to production level through a value-first, same-scalar, source-backed ladder? |
| Baseline/comparator | P88 `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE`; later same-target source-backed bridge; later FD of the exact same scalar; later HMC/GPU diagnostics only after value and gradient gates. |
| Primary pass criterion | Each stronger claim passes only through its reviewed phase gate; final production readiness requires all phase gates 1-10 to pass. |
| Veto diagnostics | Wrong target, FD of wrong scalar, proxy metrics promoted to correctness, rank/degree promoted to production, stale ALS training, audit tuning, JVP/autodiff promoted as source-route analytical derivative, GPU/HMC/production before reviewed protocol. |
| Explanatory diagnostics | Value residuals, gradient residuals, FD step-size curves, HMC diagnostics, GPU/XLA compile/runtime/memory, validation/holdout/audit curves. |
| Not concluded | Any stronger claim than the last reviewed closed phase. |
| Artifacts | Master, subplans/results, ledgers, target/bridge/derivative/runtime manifests, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| P88 label is baseline | P88 reviewed closeout | Avoids reopening rank/degree evidence | Rank/degree promoted to correctness | Phase 0 grep over P88 closeout | binding |
| Value bridge before gradient | P88 blockers and user target | Prevents matching gradient of wrong scalar | FD appears good for proxy scalar | Phase 1 same-scalar manifest | binding |
| FD is diagnostic only | Scientific coding policy | FD checks local gradient consistency, not source correctness | FD promoted to correctness proof | Phase 6 evidence contract | binding |
| Claude read-only review | User request and repo policy | Independent boundary review without execution authority | Claude edits/runs or broad prompt stalls | one-path bounded prompts | binding |
| Basis/order/rank are setup-static for XLA | P88/P86 lessons and XLA constraints | Stable compile contracts need static structure | runtime basis change causes retrace or invalid comparison | Phase 1 manifest fields | binding |
| L1 tuning default | P86/P88 lessons | Avoids overfitting and rank-5 tuning mistakes | zero-L1 treated as default production policy | training policy checks | binding |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and, for
material phases, in the execution ledger.

Check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the plan or write a blocker note
before running the phase.

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
   - Send material phase results, repairs, implementation summaries, or final
     decisions to Claude as read-only review using the mandatory one-path
     bounded prompt rule below.
   - Claude must review a single artifact path that contains the bounded
     question, citations, and diff summary when needed. Do not send open-ended
     repo diffs, broad file lists, pasted code bundles, or repo-wide review
     prompts.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, patch the same subplan visibly when possible.
   - Get Claude review when material.
   - Rerun focused checks.
   - Write a blocker result if the gate cannot pass.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a true human-required blocker appears.

## Mandatory Claude Read-Only Review Rule

Every Claude interaction must be read-only, one-path bounded, and
non-authorizing unless a later reviewed subplan explicitly tightens the scope
further. The mandatory prompt shape is:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude does not respond, Codex must run a tiny escalated probe that is
read-only, non-substantive, and not allowed to widen context. The probe may ask
only whether Claude is responsive; it must not ask for substantive review,
repo-wide context, edits, commands, or execution. If the probe responds, the
material prompt is the problem; redesign it narrower, record the probe and
retry. Do not broaden context on the first retry.

## Approval And Boundary Contract

This user request authorizes:

- creating and editing P89 artifacts under `docs/plans`;
- local artifact-only commands such as `rg`, `sed`, and `git diff --check`;
- bounded Claude Opus max-effort read-only review with trusted/escalated
  permissions.

No additional human approval is expected for those actions. Stop and ask only
for true blockers, such as:

- package installation, network fetch, credentials, or environment setup;
- destructive git/filesystem action;
- changing default policy;
- crossing runtime, GPU/CUDA, HMC, production, package/network, model-file, or
  scientific-claim boundaries not already authorized by a reviewed subplan;
- continuing after five non-convergent Claude review rounds.

Runtime-crossing commands, including but not limited to long diagnostics,
training/fitting, FD ladders, TensorFlow/JAX/PyTorch imports, HMC/samplers,
GPU/CUDA probes, GPU/CUDA jobs, production benchmarks, and production-route
commands, require an exact reviewed subplan with commands, runtime budget,
device/CPU mode, artifact paths, stop conditions, and review evidence. GPU/CUDA
commands also require trusted/escalated permissions. None are authorized by
Phase 0.

Phase 10 cannot itself flip production/default-policy state. It may write a
final recommendation/evidence artifact only. Any actual product/default-policy
promotion, release action, or default-route change requires separate explicit
human authorization after the reviewed Phase 10 result.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- tests/benchmarks actually run;
- unresolved blockers;
- what was not concluded;
- safest next action.
