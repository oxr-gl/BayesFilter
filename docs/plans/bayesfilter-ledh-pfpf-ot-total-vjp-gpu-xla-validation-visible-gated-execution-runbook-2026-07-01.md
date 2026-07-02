# Visible Gated Execution Runbook: Total-VJP GPU/XLA Validation

Date: 2026-07-01

## Status

`COMPLETE`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-master-program-2026-07-01.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-claude-review-ledger-2026-07-01.md`

Execution ledger:

- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-visible-execution-ledger-2026-07-01.md`

Stop handoff:

- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-visible-stop-handoff-2026-07-01.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Route And Artifact Inventory | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase0-route-inventory-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase0-route-inventory-result-2026-07-01.md` |
| 1 | Tiny GPU/XLA Full-Route Smoke | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-result-2026-07-01.md` |
| 2 | Harness Repair If Needed | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase2-harness-repair-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase2-harness-repair-result-2026-07-01.md` |
| 3 | Material Particle Ladder | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-particle-ladder-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-particle-ladder-result-2026-07-01.md` |
| 4 | HMC-Direction Diagnostic Gate | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-result-2026-07-01.md` |
| 5 | Final Decision | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase5-final-decision-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase5-final-decision-result-2026-07-01.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the corrected total-derivative route run and remain viable under trusted GPU/XLA/TF32, and what next action is justified? |
| Baseline/comparator | CPU float64 same-finite-scalar repair artifact; later same-route GPU/XLA rungs. |
| Primary pass criterion | Each phase passes its reviewed gate; Phase 1 must prove actual GPU/XLA full-route execution before any ladder. |
| Veto diagnostics | CPU fallback, XLA missing, route not full, stopped partial route treated as score, nonfinite outputs, OOM, unsupported claims. |
| Explanatory diagnostics | Runtime, compile time, memory, MCSE, gradient norm, historical stopped-route comparison. |
| Not concluded | No HMC readiness or production promotion unless a later reviewed phase supports it and the user approves any policy change. |
| Artifacts | Phase results, JSON outputs, Claude ledger, execution ledger, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| GPU/XLA/TF32 target | Repo `AGENTS.md` default target | This is the production-direction lane for LEDH-PFPF-OT | CPU sandbox failure misread as GPU failure | trusted `nvidia-smi`, TensorFlow GPU placement | reviewed by Phase 0 |
| Full total-derivative route | CPU repair result 2026-07-01 | This is the corrected score target for active transport | stopped route accidentally reused | Phase 0 static dispatch proof plus JSON route metadata must say `transport_ad_mode="full"` | hypothesis |
| Tiny smoke before ladder | Research workflow policy | Prevents long run before route is proven | tiny pass overclaimed | nonclaims in Phase 1 result | reviewed by Phase 1 |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and in
the ledger for material phases.  Check wrong baselines, proxy metrics,
missing stop conditions, unfair comparisons, hidden assumptions, stale context,
environment mismatch, and commands whose artifacts would not answer the phase
question.

## Visible State Machine

For each phase:

1. `PRECHECK`
2. `EXECUTE_MINIMAL`
3. `ASSESS_GATE`
4. `PASS_REVIEW`
5. `REPAIR_LOOP`
6. `ADVANCE_OR_STOP`

Follow the template in
`/home/chakwong/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`.

## Plain-Language Gate

Every result must state:

- target computed;
- derivative classification;
- what passed;
- what failed or was not checked;
- what remains unsupported.

Do not use soft language to hide a mismatch.

## Claude Read-Only Review Template

Claude prompts must be bounded and must end with exactly:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```

If Claude does not respond, first run a small probe.  If the probe responds,
the prompt is the problem; redesign it.

## Human-Required Stop Conditions

Stop if continuing would require package installation, network fetch,
credentials, destructive git action, changing pass/fail criteria after seeing
results, changing repository default policy, or continuing after five failed
Claude review rounds for the same blocker.
