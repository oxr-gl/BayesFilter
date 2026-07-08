# Minimal SSL-LSTM Zhao-Cui HMC Next Visible Gated Execution Runbook

Date: 2026-07-06

## Status

`MASTER_PROGRAM_COMPLETE`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

If detached overnight execution is later requested, stop and write a separate
detached-supervisor plan. This runbook is for visible, recoverable execution
inside the current conversation.

## Quiet Visible Execution Pattern

For commands that may produce large stdout/stderr, full output is an artifact,
not chat content.

Required pattern:

1. Predeclare log path and structured artifact path in the phase subplan or
   ledger.
2. Redirect full stdout/stderr to a log file for TensorFlow, CUDA, HMC, longer
   pytest, and review-gate commands.
3. Print only bounded summaries: exit status, artifact paths, pass/fail fields,
   and at most the last 20-40 log lines on failure.
4. Preserve logs and structured artifacts in phase result records.

Recommended log roots:

- `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_next_2026-07-06/`
- `.claude_reviews/` for Claude gate logs.

## Program

Master program:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-program-master-2026-07-06.md`

Execution ledger:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-visible-execution-ledger-2026-07-06.md`

Stop handoff:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-visible-stop-handoff-2026-07-06.md`

Initial review bundle:

- `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase0-phase1-review-bundle-2026-07-06.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and review setup | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase0-governance-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase0-governance-result-2026-07-06.md` |
| 1 | Internal reusable adapter surface | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase1-internal-adapter-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase1-internal-adapter-result-2026-07-06.md` |
| 2 | CPU regression through internal surface | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase2-cpu-regression-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase2-cpu-regression-result-2026-07-06.md` |
| 3 | Trusted GPU/XLA runtime smoke | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase3-gpu-xla-smoke-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase3-gpu-xla-smoke-result-2026-07-06.md` |
| 4 | Longer sampler-diagnostics ladder design | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase4-longer-diagnostics-design-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase4-longer-diagnostics-design-result-2026-07-06.md` |
| 5 | Longer sampler-diagnostics execution | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase5-longer-diagnostics-execution-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase5-longer-diagnostics-execution-result-2026-07-06.md` |
| 6 | Closeout and reset memo | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase6-closeout-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase6-closeout-result-2026-07-06.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the minimal scalar `zhaocui_fixed` HMC mechanics path be made reusable internally and then exercised under runtime and sampler-diagnostic gates without overstating evidence? |
| Baseline/comparator | Completed CPU-hidden minimal ladder harness and artifacts. |
| Primary pass criterion | Each phase passes its hard-veto screen, writes required artifacts, and keeps claims within the phase evidence class. |
| Veto diagnostics | Nonfinite value/score, shape drift, target-path NumPy/autodiff bridge, invalid artifact, runtime exception, nonfinite HMC samples, unapproved GPU/long-run boundary, unsupported source/scientific/default claim, failed review convergence, or missing handoff. |
| Explanatory diagnostics | Runtime, score norm, initial log prob, acceptance rate, sampler metadata, device provenance, TF32/XLA settings, and dirty-worktree summaries. |
| Not concluded | Posterior correctness, HMC convergence, statistical ranking, method superiority, source-faithful parity, public API/package readiness, default readiness, GPU/XLA production readiness, or LEDH result. |
| Artifacts | Master program, phase subplans/results, review bundles/logs, visible ledger, stop handoff, runtime JSON/Markdown artifacts, and quiet logs. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| TensorFlow/TFP implementation | Repo policy | BayesFilter algorithmic default | NumPy/autodiff bridge enters target path | Forbidden-token scans | Required |
| Internal module first | Predecessor benchmark-only harness | Reduces duplication before runtime evidence | Premature public API claim | No top-level export unless reviewed | Required |
| CPU regression before GPU | Engineering evidence ladder | Isolates extraction drift | CPU evidence mislabeled as default | Debug-reference labels | Required |
| GPU/XLA smoke after extraction | Repo default target and user branch | Runtime-path signal only | Misread as convergence/readiness | Trusted provenance and nonclaims | Boundary-gated |
| Longer diagnostics after smoke | Evidence discipline | Stronger sampler evidence needs stable target | Descriptive metrics ranked | Inference-status table | Boundary-gated |
| Claude read-only review | User request | Independent material-plan audit | No response/private-context denial | Probe/gate status and local fallback | Attempt required |

## Skeptical Plan Audit

Before each phase, Codex records a skeptical audit in the ledger. Check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If a material flaw appears, revise the plan or write a blocker result before
running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands in the current conversation.
3. `ASSESS_GATE`: compare outputs to criteria and veto diagnostics.
4. `PASS_REVIEW`: send material plans/results/diffs to read-only Claude review
   if available; otherwise use a fresh visible read-only Codex review in this
   current human-mediated session and record why. This fallback must not use
   `codex exec`, detached agents, copied workspaces, or background supervisors.
5. `REPAIR_LOOP`: patch visibly, rerun focused checks, retry material review up
   to five rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after the current phase gate passes; stop on
   human-required blocker.

## Claude Read-Only Review Command

Use compact bundles, not whole files:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/ubuntu/python/BayesFilter \
  --review-name bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase0-phase1-review \
  --bundle /home/ubuntu/python/BayesFilter/docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase0-phase1-review-bundle-2026-07-06.md \
  --model opus \
  --effort max \
  --probe-effort low \
  --timeout-seconds 180 \
  --probe-timeout 90 \
  --max-retries 1 \
  --allow-bounded-fallback
```

If Claude does not respond, send only the tiny probe through the review gate.
If Claude is alive, revise the prompt/bundle. If Claude is unavailable or the
approval reviewer denies the external review, replace the review with a fresh
visible read-only Codex review in the current human-mediated session and record
that this is weaker than full Claude review. Do not use `codex exec`, detached
agents, copied workspaces, or background supervisors for the fallback review.

## Human-Required Stop Conditions

Stop if continuing would require:

- package installation, network fetch, or credentials;
- destructive git/filesystem action;
- public API/default-policy change;
- model-file edit;
- unapproved trusted GPU/CUDA/XLA command;
- unreviewed long sampler run;
- changing pass/fail criteria after seeing results;
- crossing a source-faithfulness/scientific-claim boundary;
- continuing after five review rounds fail to converge.
