# P86 Visible Gated Execution Runbook

Date: 2026-06-24

Status: `BLOCK_P86_ZHAO_CUI_SIR_NOT_PRODUCTION_PROMOTED_REVIEWED`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

This is an overnight-ready gated plan in the sense that every phase, repair
loop, artifact, and stop condition is explicit. It is not a detached overnight
supervisor.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p86-author-lagrangep-downstream-repair-master-program-2026-06-24.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-stop-handoff-2026-06-24.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
|---|---|---|---|
| 0 | Scope, source, approval, and XLA freeze | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase0-scope-source-xla-freeze-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase0-scope-source-xla-freeze-result-2026-06-24.md` |
| 1 | Lagrangep mass and integral implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase1-lagrangep-mass-integral-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase1-lagrangep-mass-integral-result-2026-06-24.md` |
| 2 | Algebraic measure convention contract | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase2-algebraic-measure-contract-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase2-algebraic-measure-contract-result-2026-06-24.md` |
| 3 | Downstream author-route wiring | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase3-downstream-author-route-wiring-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase3-downstream-author-route-wiring-result-2026-06-24.md` |
| 4 | Tiny author-route fit smoke | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-result-2026-06-24.md` |
| 5 | Budget-compliant fit | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-result-2026-06-24.md` |
| 6 | Rank and degree convergence | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-result-2026-06-24.md` |
| 7 | Correctness bridge | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase7-correctness-bridge-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase7-correctness-bridge-result-2026-06-24.md` |
| 8 | KR and transport closure | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase8-kr-transport-closure-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase8-kr-transport-closure-result-2026-06-24.md` |
| 9 | Derivative and HMC readiness | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase9-derivative-hmc-readiness-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase9-derivative-hmc-readiness-result-2026-06-24.md` |
| 10 | LEDH comparator and scale stress | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase10-ledh-scale-stress-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase10-ledh-scale-stress-result-2026-06-24.md` |
| 11 | Production decision and reset memo | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase11-production-decision-reset-subplan-2026-06-24.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase11-production-decision-reset-result-2026-06-24.md` |

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can P86 safely close or block the author algebraic Lagrangep downstream gaps needed before Zhao-Cui SIR production promotion can even be considered? |
| Baseline/comparator | P85 setup-only author config, P84 production gates, author source anchors, and current local highdim code. |
| Primary pass criterion | Each phase yields a reviewed pass or precise blocker; production promotion requires all mandatory gates and owner approval. |
| Veto diagnostics | Missing anchors, proxy-promotion, unapproved fitting/GPU/HMC/LEDH/long commands, dynamic XLA basis switching, unsupported production/scientific claims. |
| Explanatory diagnostics | Source inventories, unit checks, CPU-hidden smokes, fit manifests, convergence ledgers, bridge residuals, KR diagnostics, derivative/sampler/comparator/scale manifests. |
| Not concluded | No production readiness, correctness, HMC readiness, LEDH superiority, d=50/d=100 scaling, or default-policy change from planning alone. |
| Artifacts | Master program, subplans/results, ledgers, JSON manifests, handoff, reset memo. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
|---|---|---|---|---|---|
| Author `Lagrangep(4,8)` with `AlgebraicMapping(1)` | Author SIR script | It is the author SIR route P85 made configurable | Treating setup identity as fit/correctness evidence | Phase 0 source/claim freeze | `baseline` |
| Reference-domain mass/integral first | `LagrangeRef.m`, `Piecewise.m`, `Lagrangep.m` | It isolates exact basis assembly before algebraic Jacobian semantics | Silent normalization/Jacobian mismatch | Phase 1 exact 1D checks | `hypothesis_pending_phase1` |
| Algebraic measure contract before fit | `AlgebraicMapping.m` and local measure enums | Fitting must know whether densities live in reference or physical coordinates | Correct-looking fit under wrong measure | Phase 2 convention ledger | `hypothesis_pending_phase2` |
| Setup-static basis/domain choices | P85 XLA contract | Avoid runtime Python dispatch inside compiled numerical paths | Recompile/retrace surprises or invalid graph assumptions | Phase 2 and Phase 3 static-field checks | `reviewed_from_p85` |
| CPU-hidden local tests for early phases | Project GPU policy | Local unit/smoke tests do not need GPU evidence | Accidental GPU initialization or overclaim | `CUDA_VISIBLE_DEVICES=-1` command manifests | `pending_exact_command` |

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
     decisions to Claude as read-only one-path reviews.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, patch the same subplan or result visibly.
   - Rerun focused checks.
   - Repeat Claude review only for material issues.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
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

Use the smallest exact path that can answer the gate:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude does not respond, run a small read-only probe. If the probe responds,
the prompt is considered the problem; redesign the bounded prompt and retry.

## Human-Required Stop Conditions

Stop if continuing would require:

- a product or scientific claim not already in the reviewed plan;
- package installation, network fetch, credentials, remote access, or
  environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- fitting, HMC, LEDH, d=50/d=100, or long runtime commands without exact
  approval;
- continuing after Claude and Codex do not converge after five review rounds.

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
