# Contract E Visible Gated Execution Runbook

Date: 2026-06-28

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_PENDING_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

If detached overnight execution is needed later, stop and write a separate
detached-supervisor plan.  This runbook is for visible, recoverable execution
inside the current conversation.

## Program

Master program:

- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-residual-affine-testing-master-program-2026-06-28.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-claude-review-ledger-2026-06-28.md`

Execution ledger:

- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-visible-execution-ledger-2026-06-28.md`

Stop handoff:

- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-visible-stop-handoff-2026-06-28.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance, math anchors, and route inventory | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase0-governance-inventory-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase0-governance-inventory-result-2026-06-28.md` |
| 1 | Moment-level Contract E diagnostic | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-result-2026-06-28.md` |
| 2 | LGSSM value gate | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-result-2026-06-28.md` |
| 3 | LGSSM gradient gate | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-result-2026-06-28.md` |
| 4 | SIR same-scalar FD diagnostic | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase4-sir-fd-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase4-sir-fd-result-2026-06-28.md` |
| 5 | SV and nonlinear extension diagnostic | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase5-sv-nonlinear-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase5-sv-nonlinear-result-2026-06-28.md` |
| 6 | GPU/XLA/TF32 chunked stress ladder | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase6-gpu-xla-stress-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase6-gpu-xla-stress-result-2026-06-28.md` |
| 7 | Final audit and closeout | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase7-closeout-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase7-closeout-result-2026-06-28.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Contract E become a viable moment-preserving differentiable reset candidate for LEDH-PFPF-OT? |
| Baseline/comparator | Existing barycentric reset, no-OT weighted arm, exact Kalman only for LGSSM, and same-scalar 13-point FD for nonlinear gradients. |
| Primary pass criterion | Each phase passes its artifact/check/review gate, with final closeout supporting either rejection, blocker, or promotion only to a next evidence program. |
| Veto diagnostics | Wrong comparator, missing FD SE, missing MCSE, nonfinite values, support-rank failure, conditioning veto, hidden `transport_ad_mode=full`, Python loops in XLA-critical paths, untrusted GPU evidence, or unsupported claims. |
| Explanatory diagnostics | Runtime, memory, Sinkhorn residuals, covariance trace ratios, condition spectra, residual noise scale, central FD sanity checks, per-seed scatter. |
| Not concluded | No posterior correctness, HMC readiness, production readiness, default-policy change, or claim that the full Contract E hybrid is already established literature. |
| Artifacts | Master, subplans/results, ledger, review ledger, stop handoff, JSON/Markdown diagnostics. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| GPU/XLA/TF32 for material LEDH runs | `AGENTS.md` and project policy | This is the default production target for LEDH-PFPF-OT evidence. | Sandbox can hide GPU; CPU result misreported as GPU. | Escalated `nvidia-smi` and TF GPU probe before GPU claims. | planned |
| CPU-hidden smoke for small wiring checks | `AGENTS.md` | Fast, sandbox-safe smoke can catch syntax/wiring without GPU claims. | CUDA chatter misread as GPU evidence. | Set GPU-hiding env before framework import and label CPU-only. | planned |
| LGSSM exact Kalman comparator | Linear-Gaussian model theory and existing repo tests | Exact value/gradient oracle exists only for LGSSM. | Illegally reused for SIR/SV. | Comparator split in every phase contract. | frozen |
| 13-point FD regression | User directive and prior testing discipline | Reduces noisy central-difference failure. | Central FD promoted accidentally. | Phase veto if central FD is primary evidence. | frozen |
| No full transport autodiff | Prior memory diagnosis and user directive | `transport_ad_mode=full` is memory explosive. | Full dense AD sneaks back in. | `rg` audit and route manifest. | frozen |
| Exact chunks where possible | N10000 chunk tuning results | Avoid padding and improve GPU/XLA behavior. | Nondivisible particle counts cause padding/timing artifacts. | Phase 6 manifest records N/chunk divisibility. | planned |

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
   - Advance only after the current phase gate passes.
   - A classified failure is not a pass.  It must either be repaired and rerun
     inside the current phase or written as a blocker handoff.
   - Stop and write the handoff if a human-required blocker appears.

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

## Claude Read-Only Review Template

Use Claude only as a reviewer.  The prompt must say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review exact paths only:
- <phase result / blocker plan / implementation diff / final decision>

You may inspect only the named paths and line ranges. Do not traverse the repo
or request whole-file context unless the prompt explicitly names it.

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

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.

## Launch Protocol

After the master program and this runbook pass local checks and bounded Claude
review, Codex launches Phase 0 visibly in this conversation.  "Launch" means:

1. append the first execution-ledger entry;
2. perform Phase 0 prechecks;
3. write the Phase 0 result or blocker;
4. review/repair the next subplan before advancing.

No detached overnight supervisor is authorized by this visible runbook.

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
