# P91 Visible Gated Execution Runbook

Date: 2026-06-29

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_PENDING_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only. Claude is not an execution authority
and cannot authorize crossing human, runtime, model-file, funding,
product-capability, default-policy, or scientific-claim boundaries.

This runbook is visible and recoverable inside the current conversation. It
must not launch a detached or nested agent. Do not use `codex exec`, detached
overnight launchers, `setsid`, `nohup`, detached `tmux`, background phase
runners, or copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-score-identity-hmc-gpu-production-master-program-2026-06-29.md`

Claude review ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-claude-review-ledger-2026-06-29.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-visible-execution-ledger-2026-06-29.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-visible-stop-handoff-2026-06-29.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Production contract reframe | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase0-production-contract-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase0-production-contract-result-2026-06-29.md` |
| 1 | Score contract freeze | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-result-2026-06-29.md` |
| 2 | Batched value/score API | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-result-2026-06-29.md` |
| 3 | FD consistency | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-result-2026-06-29.md` |
| 4 | Score-identity validation | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-result-2026-06-29.md` |
| 5 | GPU/XLA JIT capability | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-result-2026-06-29.md` |
| 6 | CPU/GPU/batched benchmark | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-result-2026-06-29.md` |
| 7 | HMC readiness smoke | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-result-2026-06-29.md` |
| 8 | Packaging, CI, release notes | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase8-packaging-release-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase8-packaging-release-result-2026-06-29.md` |
| 9 | Final production decision | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can visible gated execution pursue Zhao-Cui SIR d18 production under the P91 score-identity, FD, batched API, GPU/XLA-HMC, and benchmark standard without repeating P90 overclaim/blocker mistakes? |
| Baseline/comparator | P90 final blocked decision plus owner P91 amendments. |
| Primary pass criterion | Execution advances phase by phase only after reviewed subplans/results and exact upstream pass artifacts; final production promotion requires every P91 production gate to pass. |
| Veto diagnostics | Score identity treated as exact-likelihood proof, FD treated as oracle, GPU treated as universally fastest, batched benchmark treated as scientific validity, missing caveats, branch/setup drift, NaN/Inf, unreviewed runtime/GPU/HMC/package/default crossing, or unsupported production claim. |
| Explanatory diagnostics | FD step ladder, score z-scores, compile/run time, memory, HMC smoke diagnostics, and optional Hessian/sandwich notes. |
| Not concluded | No production readiness, exact likelihood correctness, posterior correctness, universal GPU superiority, default-policy change, root-solving validity, or Hessian/information equality at launch. |
| Artifacts | P91 master, runbook, ledgers, subplans, phase results, validation/benchmark manifests, release-note draft, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Score identity is primary scientific gate | User owner direction, 2026-06-29 | Matches high-dimensional estimating-equation use without demanding impossible oracle gradient/root solve. | Mistakenly claimed exact likelihood truth. | Phase 0 contract caveat. | owner decision |
| FD remains necessary engineering gate | User owner direction, 2026-06-29 | HMC needs gradient of implemented scalar to be internally consistent. | FD treated as truth oracle. | Phase 3 evidence contract. | owner decision |
| GPU/XLA capability required for HMC-facing target | User owner direction, 2026-06-29 | HMC production target must compile and run in trusted GPU/XLA context. | Non-escalated GPU failure or CPU fallback misread. | Phase 5 trusted GPU check. | owner decision |
| CPU/GPU speed is model-specific | User owner direction, 2026-06-29 | Avoids claiming GPU is always faster. | Universal GPU default claim. | Phase 6 benchmark table. | owner decision |
| Batched route required | User owner direction, 2026-06-29 | Score identity and HMC throughput need batch-capable value/score. | Batched route diverges from single route. | Phase 2 parity tests. | owner decision |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and,
for material phases, in the execution ledger. Check wrong baselines, proxy
metrics promoted to pass criteria, missing stop conditions, unfair
comparisons, hidden assumptions, stale context, environment mismatch, and
commands whose artifacts would not answer the phase question.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
2. `REVIEW_SUBPLAN`
   - Confirm the current phase subplan has one-path Claude `VERDICT: AGREE`.
   - Confirm exact upstream result artifacts required by the subplan exist.
   - Rerun review if a subplan materially changes.
3. `EXECUTE_MINIMAL`
   - Run only commands authorized by that reviewed subplan.
   - Preserve unrelated dirty worktree changes.
4. `ASSESS_GATE`
   - Compare outputs against primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
   - For material runtime, GPU/XLA, HMC, benchmark, score-identity, FD,
     packaging, release-note, or final-decision phases, the result artifact
     must include or link the exact command run, environment/trusted-context
     status, output artifact paths, decision table or pass/veto status, and
     run manifest needed for review.
5. `PASS_REVIEW`
   - Send material phase results/repairs/final decisions to Claude as one-path
     read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
6. `REPAIR_LOOP`
   - Patch fixable issues visibly.
   - Rerun focused checks.
   - Loop Claude review up to five rounds for the same blocker.
7. `ADVANCE_OR_STOP`
   - Advance only after the current gate passes.
   - Stop and write handoff if a true blocker appears.

## Claude Read-Only Review Template

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: Check
consistency, correctness, feasibility, artifact coverage, boundary safety, and
whether this artifact repeats P90/P91 mistakes. End with VERDICT: AGREE or
VERDICT: REVISE.
```

If Claude does not respond, Codex may run a tiny read-only responsiveness probe
only through the same visible review mechanism. The probe must not launch a
detached or nested agent, must not widen permissions or scope beyond ordinary
Claude read-only review, and must not be treated as substantive review. If the
probe succeeds, narrow the material prompt.

## Human-Required Stop Conditions

Stop if continuing would require a project-direction decision not already in
the reviewed plan, package installation, network fetch, credentials,
destructive git/filesystem action, pass/fail criteria changes after seeing
results, default-policy change, unrelated dirty-worktree modification,
interpreting GPU results without trusted-context evidence, or continuing after
five non-convergent Claude review rounds.

Human approval is not required for ordinary reviewed document repairs, local
artifact checks, or bounded Claude agreement loops. Claude agreement is enough
for document-only subplan/result review but cannot authorize runtime,
scientific, product, funding, model-file, release, or default-policy
boundaries.

Phase 8 packaging/CI/release-note work is artifact-preparation only unless a
reviewed subplan and required human authorization explicitly approve a package,
release, CI-service mutation, or default-policy action. Phase 9 final
production decision is an evidence/recommendation artifact only; it cannot by
itself release, publish, mutate CI, change defaults, or cross a product-policy
boundary. If final promotion requires one of those actions, P91 must stop with
the recommendation and request the required human authorization.

## Final Visible Handoff

When execution completes or stops, write final phase reached, status, result
artifacts, Claude review trail, checks/benchmarks run, unresolved blockers,
what was not concluded, and safest next action.
