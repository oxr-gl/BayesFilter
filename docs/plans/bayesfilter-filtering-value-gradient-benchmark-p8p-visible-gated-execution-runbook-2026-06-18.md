# P8p Visible Gated Execution Runbook

Date: 2026-06-18

## Status

`LAUNCHED_PHASE0_PASSED_PHASE1_NEXT`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

This runbook is for visible, recoverable execution inside the current
conversation.

## Program

Master program:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-sir-d18-gradient-hmc-master-program-2026-06-18.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-claude-review-ledger-2026-06-18.md`

Execution ledger:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-visible-execution-ledger-2026-06-18.md`

Stop handoff:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-visible-stop-handoff-2026-06-18.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and target boundary | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase0-governance-target-boundary-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase0-governance-target-boundary-result-2026-06-18.md` |
| 1 | Parameterized SIR objective contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase1-parameterized-sir-objective-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase1-parameterized-sir-objective-result-2026-06-18.md` |
| 2 | Fixed-randomness gradient smoke implementation | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-result-2026-06-18.md` |
| 3 | Central finite-difference validation | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3-finite-difference-validation-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3-finite-difference-validation-result-2026-06-18.md` |
| 4 | Full-horizon SIR d18 gradient probe | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase4-full-horizon-gradient-probe-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase4-full-horizon-gradient-probe-result-2026-06-18.md` |
| 5 | Chunk and precision stability | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase5-chunk-precision-stability-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase5-chunk-precision-stability-result-2026-06-18.md` |
| 6 | Multi-seed gradient stability and particle ladder | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase6-multiseed-gradient-ladder-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase6-multiseed-gradient-ladder-result-2026-06-18.md` |
| 7 | Tiny HMC mechanics smoke | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase7-hmc-mechanics-smoke-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase7-hmc-mechanics-smoke-result-2026-06-18.md` |
| 8 | Closeout and reset memo | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase8-closeout-reset-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase8-closeout-reset-result-2026-06-18.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the current batched streaming LEDH-PFPF-OT SIR d18 route support finite, connected, repeatable gradients on an explicit fixed-randomness diagnostic theta target, and then pass a tiny HMC mechanics smoke without overstating posterior validity? |
| Baseline/comparator | P8o fixed-parameter value-only SIR d18 route for entry and shape/runtime provenance; same fixed-randomness target under central finite differences for local diagnostic comparison; small precision/chunk variants for stability. |
| Primary pass criterion | Each phase passes its declared gate with artifacts and review, or writes a blocker preserving exact P8p boundary state.  Final P8p pass requires gradient and HMC-mechanics gates, not merely value-only filtering. |
| Veto diagnostics | Nonfinite/disconnected gradients; categorical resampling in theta target; random streams changing between theta evaluations; GPU outside trusted context; finite differences promoted to stochastic PF score proof; posterior convergence, NUTS, production, exact-likelihood, or Zhao-Cui TT/SIRT claims. |
| Explanatory diagnostics | Gradient norms, FD residuals, seed variability, chunk/precision deltas, Sinkhorn residuals, ESS, runtime, GPU memory, HMC acceptance, tiny-chain traces. |
| Not concluded | Stochastic PF marginal-gradient correctness, exact nonlinear likelihood correctness, posterior convergence, NUTS readiness, tuned HMC readiness, production/default readiness, Zhao-Cui TT/SIRT parity, MATLAB parity, filter ranking, or cross-model default policy. |
| Artifacts | P8p master program, subplans/results, execution ledger, Claude review ledger, JSON/CSV diagnostics, and stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Use P8o as value-only entry evidence | P8o result artifact | Establishes SIR d18 batched route viability without overclaiming gradients | P8o accidentally treated as gradient/HMC proof | Phase 0 boundary result | baseline |
| Use three global log-scale theta | User discussion plus current fixed SIR row | Small target is debug-friendly and HMC-mechanics relevant | Theta target mistaken for scientific posterior model | Phase 1 contract nonclaims | hypothesis |
| Freeze initial and process random streams | HMC gradient requirement | Common random numbers make the objective deterministic for AD/FD/HMC mechanics | Random streams vary with theta, invalidating FD and HMC mechanics | Phase 2 repeatability smoke | required |
| Use relaxed Sinkhorn OT only | Existing DPF route and gradient requirement | Keeps resampling differentiable | Categorical resampling disconnects or invalidates gradient path | Phase 2 route audit | required |
| Add explicit per-theta connectivity diagnostic | Current streaming score helper zero-fills unconnected gradients | Prevents masked disconnected gradients from looking valid | Broken theta path appears as zero gradient | Phase 2 raw/auxiliary connectivity check plus FD sensitivity | required |
| Run GPU claims only in trusted context | AGENTS.md GPU policy | Sandbox can hide CUDA/GPU | False GPU failure or false placement claim | Escalated TensorFlow GPU probes/runs | required |

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

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- mutating unrelated Zhao-Cui fixed-branch or monograph work;
- interpreting GPU/special hardware results without trusted-context evidence;
- treating the current zero-filled score helper as sufficient connectivity
  evidence without a separate per-theta connectivity diagnostic;
- runtime projection from a smaller gate showing that the next run would exceed
  the declared budget;
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
