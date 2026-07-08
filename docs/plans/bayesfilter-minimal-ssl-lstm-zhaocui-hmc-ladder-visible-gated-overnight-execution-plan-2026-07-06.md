# Minimal SSL-LSTM Zhao-Cui HMC Ladder Visible Gated Overnight Execution Plan

Date: 2026-07-06

## Status

`PHASE4_PASSED_PHASE5_DEFERRED_READY_FOR_CLOSEOUT`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This is an overnight-style gated plan, but it is not a detached launch. Do not
use `codex exec`, `overnight_gated_launch.sh`, `setsid`, `nohup`, detached
`tmux`, backgrounded phase runners, or copied-workspace execution unless the
user explicitly approves a separate detached-supervisor boundary.

## Quiet Visible Execution Pattern

For nontrivial commands, predeclare log paths and structured artifacts, redirect
full stdout/stderr to logs, and report only exit status plus bounded summaries.

Recommended log root:

- `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_ladder_2026-07-06/`

## Program

Master program:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-master-program-2026-07-06.md`

Review bundle:

- `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase0-review-bundle-2026-07-06.md`

Execution ledger:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-visible-execution-ledger-2026-07-06.md`

Stop handoff:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-visible-stop-handoff-2026-07-06.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance, fixture freeze, and review setup | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase0-governance-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase0-governance-result-2026-07-06.md` |
| 1 | Minimal HMC target adapter bridge | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase1-target-adapter-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase1-target-adapter-result-2026-07-06.md` |
| 2 | CPU-hidden HMC canary | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase2-cpu-hidden-canary-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase2-cpu-hidden-canary-result-2026-07-06.md` |
| 3 | Repair loop and retest gate | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase3-repair-loop-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase3-repair-loop-result-2026-07-06.md` |
| 4 | Short replicated debug ladder | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase4-short-replicated-ladder-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase4-short-replicated-ladder-result-2026-07-06.md` |
| 5 | Optional trusted GPU/XLA bridge | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase5-optional-gpu-xla-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase5-optional-gpu-xla-result-2026-07-06.md` |
| 6 | Closeout and reset memo | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase6-closeout-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase6-closeout-result-2026-07-06.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the scalar SSL-LSTM `zhaocui_fixed` target pass staged HMC mechanics gates with structured artifacts? |
| Baseline/comparator | Completed minimal smoke artifact and existing BayesFilter `run_full_chain_tfp_hmc`/Phase 7 launch-smoke pattern. |
| Primary pass criterion | Each executed phase passes its hard-veto screen and preserves evidence boundaries. |
| Veto diagnostics | Nonfinite target value/score, invalid HMC metadata, runtime crash, nonfinite samples, invalid artifact, unsupported claims, wrong scalar fixture, or evidence-class mismatch. |
| Explanatory diagnostics | Runtime, score norm, initial log prob, acceptance rate, finite counts, and later predeclared short-ladder diagnostics. |
| Not concluded | Posterior correctness, HMC convergence, ranking, method superiority, source-faithful parity, GPU/XLA production readiness, default readiness, or LEDH result. |
| Artifacts | `docs/plans`, `docs/reviews`, `docs/benchmarks`, quiet logs, ledger, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| TensorFlow/TFP backend | Repo policy | Default BayesFilter backend | Non-TF target path leaks in | Source scan | Required |
| Scalar dimensions | User request and smoke result | Minimal HMC ladder | Accidentally tests larger Phase 7 fixture | Artifact fixture fields | Locked |
| `zhaocui_fixed` first | User request | Main lane under test | Comparator evidence mistaken for promotion | Candidate-role labels | Locked |
| `run_full_chain_tfp_hmc` | Existing HMC API | Smallest local HMC runner already used by SSL-LSTM Phase 7 | Invented runner semantics | Phase 1 adapter tests | Locked |
| CPU-hidden canary first | Debug safety | Avoid premature GPU claim | CPU result mislabeled as GPU evidence | Run manifest | Debug-only |
| `num_results=2` | Existing Phase 7 smoke | Smallest launch canary | Misread as convergence evidence | Nonclaims and metric roles | Convenience |
| `num_burnin_steps=1` | Existing Phase 7 smoke | Smallest launch canary | Misread as tuning adequacy | Nonclaims and metric roles | Convenience |
| `num_leapfrog_steps=1` | Existing Phase 7 smoke | Smallest launch canary | Step path too weak for inference | Nonclaims and metric roles | Convenience |
| `step_size=1e-5` | Existing Phase 7 smoke | Conservative mechanics probe | Too small to indicate sampler usefulness | Nonclaims and later ladder | Hypothesis |
| Non-JIT Phase 1/2 path | Explicit debug exception | Smallest CPU-hidden local mechanics probe | Misread as default XLA/HMC evidence | Run manifest and nonclaims | Debug/reference exception |
| Claude review | User request | Material plan review | External/private context denied by approval reviewer | Recorded local Codex substitute review | Active fallback |

## Skeptical Plan Audit

Before executing each phase, Codex must check wrong baselines, proxy promotion,
missing stop conditions, unfair comparisons, hidden assumptions, stale context,
environment mismatch, and artifact mismatch. If a material flaw appears, revise
or write a blocker before running commands.

## Visible State Machine

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands in this conversation.
3. `ASSESS_GATE`: compare outputs to criteria/vetoes and write result.
4. `PASS_REVIEW`: use Claude read-only review only after approval.
5. `REPAIR_LOOP`: patch visibly, rerun focused checks, retry review up to five
   rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after gate passes; stop on human-required
   blocker.

## Claude Review Gate Shape

If external Claude review becomes approved later, use a bounded review gate
similar to:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/ubuntu/python/BayesFilter \
  --review-name minimal-ssl-lstm-zhaocui-hmc-ladder-phase0-review \
  --bundle /home/ubuntu/python/BayesFilter/docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase0-review-bundle-2026-07-06.md \
  --model opus \
  --effort max \
  --probe-effort low \
  --timeout-seconds 180 \
  --probe-timeout 90 \
  --max-retries 1 \
  --allow-bounded-fallback
```

For this Phase 0 gate, the approval reviewer rejected external Claude review
because it would transmit private repository context to an external service.
Do not work around that denial. Use a fresh local Codex substitute review and
record the fallback. If a future approved Claude review is used, Claude silence
is not approval; if the material review fails, send a tiny probe, redesign the
prompt if Claude is alive, and use local substitute review only when Claude is
unavailable or denied.

## Human-Required Approval Boundaries

Immediate review status:

- Claude review gate through
  `bash /home/ubuntu/python/claudecodex/scripts/claude_review_gate.sh` was
  requested and denied for private-context transfer risk.
- Active review path is local Codex substitute review.

Later approval only if a later phase reaches that boundary:

- trusted GPU/CUDA/XLA execution;
- detached overnight launcher;
- package installation or network fetch;
- long HMC runs beyond the reviewed short debug ladder;
- public API, model-file, package metadata, or default-policy changes.

## Human-Required Stop Conditions

Stop if continuing would require package installation, network fetch,
credentials, destructive git/filesystem action, model-file edits, default-policy
changes, public API commitments, unapproved Claude/GPU/long/detached execution,
or a scientific/source-faithfulness claim the evidence does not support.

## Final Visible Handoff

When execution completes or stops, write final phase reached, final status,
result artifacts, review trail, tests/benchmarks actually run, unresolved
blockers, what was not concluded, and safest next human decision.
