# Minimal SSL-LSTM Zhao-Cui Smoke Visible Gated Execution Runbook

Date: 2026-07-06

## Status

`COMPLETED_VISIBLE_EXECUTION_WITH_CODEX_SUBSTITUTE_REVIEWS`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

## Quiet Visible Execution Pattern

For nontrivial commands, predeclare log paths and structured artifacts, redirect
full stdout/stderr to logs, and report only exit status plus bounded summaries.

Recommended log root:

- `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_smoke_2026-07-06/`

## Program

Master program:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-master-program-2026-07-06.md`

Review bundle:

- `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase0-review-bundle-2026-07-06.md`

Execution ledger:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-visible-execution-ledger-2026-07-06.md`

Stop handoff:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-visible-stop-handoff-2026-07-06.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance, fixture freeze, and review setup | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase0-governance-fixture-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase0-governance-fixture-result-2026-07-06.md` |
| 1 | Minimal smoke harness and artifact writer | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase1-harness-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase1-harness-result-2026-07-06.md` |
| 2 | Local checks and comparator mechanics | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase2-local-checks-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase2-local-checks-result-2026-07-06.md` |
| 3 | Optional launch-smoke bridge | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase3-launch-smoke-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase3-launch-smoke-result-2026-07-06.md` |
| 4 | Closeout and reset memo | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase4-closeout-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase4-closeout-result-2026-07-06.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the scalar SSL-LSTM `zhaocui_fixed` mechanics be run and preserved as a reproducible smoke artifact? |
| Baseline/comparator | Existing minimal adapter test fixture; `fixed_sgqf` and `svd_ukf` as mechanics comparators only. |
| Primary pass criterion | Structured artifact and focused checks pass for scalar `zhaocui_fixed` with finite deterministic value/score and FD agreement. |
| Veto diagnostics | Nonfinite target, nondeterminism, target autodiff/NumPy, FD mismatch, invalid schema, unsupported claims, wrong fixture dimensions, or LEDH leakage. |
| Explanatory diagnostics | Runtime, score norm, FD residual, reference sample count, comparator rows, and launch-smoke telemetry if used. |
| Not concluded | Posterior correctness, HMC convergence, ranking, method superiority, source-faithful parity, GPU/XLA production readiness, default readiness, or LEDH result. |
| Artifacts | `docs/plans`, `docs/benchmarks`, `docs/reviews`, ledger, logs. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- |
| TensorFlow/TFP backend | Repo policy | Default BayesFilter backend | Non-TF target path leaks in | Forbidden-source scan | Required |
| Scalar dimensions | User request | Minimal smoke | Accidentally tests nonminimal harness only | Static config/artifact fields | Locked |
| Horizon `2` | Existing minimal test fixture | Smallest useful two-step transition/observation path | Too small for scientific interpretation | Nonclaims and closeout | Convenience |
| `zhaocui_fixed` first | User request and July 5 state | Main lane under test | Comparator evidence mistaken for promotion | Candidate-role labels | Locked |
| CPU-hidden local debug first | Safety/cheap diagnostic | Avoids premature GPU claim | CPU result mistaken for production evidence | Run manifest | Debug-only |
| Claude review | User request | Material subplan review | External review unavailable in this workspace | Recorded substitute-review fallback | Resolved via Codex substitute reviews |

## Skeptical Plan Audit

Before executing any phase, Codex must check wrong baselines, proxy promotion,
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

After user approval, use a bounded review gate similar to:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/ubuntu/python/BayesFilter \
  --review-name minimal-ssl-lstm-zhaocui-phase0-review \
  --bundle /home/ubuntu/python/BayesFilter/docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase0-review-bundle-2026-07-06.md \
  --model opus \
  --effort max \
  --probe-effort low \
  --timeout-seconds 180 \
  --probe-timeout 90 \
  --max-retries 1 \
  --allow-bounded-fallback
```

Claude silence is not approval. If the material review fails, send a tiny
probe. If the probe responds, redesign the prompt/bundle. If the probe fails,
use a Codex substitute review and record the fallback.

## Human-Required Stop Conditions

Stop if continuing would require package installation, network fetch,
credentials, destructive git/filesystem action, model-file edits, default-policy
changes, public API commitments, unapproved Claude/GPU/long/detached execution,
or a scientific/source-faithfulness claim the evidence does not support.
