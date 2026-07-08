# SSL-LSTM Zhao-Cui-First Visible Gated Execution Runbook

Date: 2026-07-05

Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook does not use detached execution. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux`;
- backgrounded phase runners;
- Claude as executor.

## Quiet Visible Execution Pattern

1. Predeclare log paths and structured artifact paths in the phase subplan.
2. Redirect command output to logs for any nontrivial run.
3. Prefer commands that emit JSON or Markdown result artifacts directly.
4. After a command, report only exit status, artifact paths, and bounded failure tails.
5. If Claude review stalls, use a tiny probe before treating Claude as unavailable.

## Program

Master program:

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-master-program-2026-07-05.md`

Review bundle:

- `docs/reviews/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase0-review-bundle.md`

Execution ledger:

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-visible-execution-ledger-2026-07-05.md`

Stop handoff:

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-visible-stop-handoff-2026-07-05.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Source-anchor governance and route classification | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase0-source-anchor-governance-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase0-source-anchor-governance-result-2026-07-05.md` |
| 1 | Fixed-variant design and classification ledger | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase1-fixed-variant-design-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase1-fixed-variant-design-result-2026-07-05.md` |
| 2 | `zhaocui_fixed` adapter implementation | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-zhaocui-fixed-adapter-implementation-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-zhaocui-fixed-adapter-implementation-result-2026-07-05.md` |
| 3 | Focused tests and artifact schema | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase3-tests-and-artifact-schema-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase3-tests-and-artifact-schema-result-2026-07-05.md` |
| 4 | Shared benchmark and launch-smoke integration | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase4-benchmark-and-launch-smoke-integration-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase4-benchmark-and-launch-smoke-integration-result-2026-07-05.md` |
| 5 | Closeout and LEDH deferral handoff | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase5-closeout-and-ledh-deferral-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase5-closeout-and-ledh-deferral-result-2026-07-05.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the Zhao-Cui-first program produce a deterministic analytic SSL-LSTM value/score path and admit it into the shared benchmark/HMC gates? |
| Baseline/comparator | Phase 3 SGQF/UKF adapters, the local Zhao-Cui source-anchor audit bundle, and the shared SSL-LSTM benchmark runner. |
| Primary pass criterion | The `zhaocui_fixed` lane is implemented, finite, schema-valid, and admitted without any false source-faithfulness claim. |
| Veto diagnostics | Missing source anchors, adaptive target-path randomness, autodiff fallback, non-finite score, invalid artifact schema, or claims that outrun the evidence. |
| Explanatory diagnostics | Runtime, finite-difference residuals, branch stability, and HMC launch telemetry. |
| Not concluded | Exact posterior correctness, method superiority, LEDH sufficiency, or source-faithful parity. |
| Artifacts | `docs/plans`, `docs/reviews`, structured benchmark outputs, and phase result/close records. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| TensorFlow / TFP backend | Repo policy | Default BayesFilter backend | NumPy prototype leaks into target path | Import and adapter audit | Required |
| GPU default target | Repo policy | Default production target for serious runs | CPU debug artifact mistaken for production evidence | Run manifest device/JIT fields | Required |
| Zhao-Cui-first scope | User directive | Defer LEDH until Zhao-Cui is unblocked | LEDH work smuggled into the program | Phase index audit | Locked |
| Fixed-variant route | User directive plus source-anchor gate | Need deterministic HMC-compatible scoring | Adaptive randomness remains in the target path | Phase 0 source/classification review | Required |

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the evidence contract in chat.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only the smallest visible commands needed.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the phase criteria and vetoes.
   - Write or update the phase result artifact.
4. `PASS_REVIEW`
   - Send material artifacts to Claude as read-only review using a bounded bundle.
   - If Claude is unresponsive, send a tiny probe.
   - If the probe responds, redesign the prompt/bundle and retry.
   - If the probe fails, run a separate Codex read-only substitute review on the same bounded bundle.
5. `REPAIR_LOOP`
   - Patch the same artifact visibly.
   - Rerun focused checks.
   - Retry review up to five times for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Claude Review Gate Shape

Use a bounded read-only review gate for material subplans and results:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/ubuntu/python/BayesFilter \
  --review-name zhaocui-first-phase0-review \
  --bundle /home/ubuntu/python/BayesFilter/docs/reviews/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase0-review-bundle.md \
  --model opus \
  --effort max \
  --probe-effort low \
  --timeout-seconds 180 \
  --probe-timeout 90 \
  --max-retries 1 \
  --allow-bounded-fallback
```

If the gate returns no verdict, run a tiny probe. If the probe returns, the
prompt or bundle is wrong and must be redesigned. If the probe fails, use a
Codex substitute review for the same bounded bundle and record that fallback.

## Human-Required Stop Conditions

Stop if continuing would require package installation, network fetch, credentials,
destructive git/filesystem action, model-file edits, default-policy changes,
new public API commitments, or a source-faithfulness claim that the evidence
does not support.
