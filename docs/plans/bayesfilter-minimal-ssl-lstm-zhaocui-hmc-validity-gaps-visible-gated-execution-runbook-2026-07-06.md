# Minimal SSL-LSTM Zhao-Cui HMC Validity Gaps Visible Gated Execution Runbook

Date: 2026-07-06

## Status

`PHASE2_PASSED_PHASE3_REVIEW_PENDING`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested execution supervisor. Do not
use `codex exec`, `overnight_gated_launch.sh`, `setsid`, `nohup`, detached
`tmux`, backgrounded phase runners, or copied-workspace execution. If detached
overnight execution is requested later, stop and write a separate detached plan.

## Quiet Visible Execution Pattern

For commands that may produce large stdout/stderr, full output is an artifact,
not chat content.

Required pattern:

1. Predeclare log path and structured artifact path in the phase subplan or
   ledger.
2. Redirect full stdout/stderr to a log file for TensorFlow, CUDA, HMC, long
   tests, benchmarks, and Claude review commands.
3. Prefer commands that write JSON/Markdown/result artifacts directly.
4. After execution, summarize only exit status, artifact paths, pass/fail
   fields, and at most the last 20-40 log lines on failure.
5. Preserve logs and structured artifacts in phase result records.

## Program

Master program:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-master-program-2026-07-06.md`

Execution ledger:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-visible-execution-ledger-2026-07-06.md`

Stop handoff:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-visible-stop-handoff-2026-07-06.md`

Initial review bundle:

- `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase0-phase1-review-bundle-2026-07-06.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and review setup | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase0-governance-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase0-governance-result-2026-07-06.md` |
| 1 | Scalar posterior/reference oracle design | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase1-scalar-oracle-design-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase1-scalar-oracle-design-result-2026-07-06.md` |
| 2 | Minimal oracle implementation and checks | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase2-oracle-implementation-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase2-oracle-implementation-result-2026-07-06.md` |
| 3 | Longer HMC convergence diagnostics | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-longer-hmc-diagnostics-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-longer-hmc-diagnostics-result-2026-07-06.md` |
| 4 | Native divergence telemetry investigation | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase4-divergence-telemetry-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase4-divergence-telemetry-result-2026-07-06.md` |
| 5 | HMC tuning and mass-matrix ladder design | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase5-tuning-mass-ladder-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase5-tuning-mass-ladder-result-2026-07-06.md` |
| 6 | Minimal dimensional lift design | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase6-dimensional-lift-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase6-dimensional-lift-result-2026-07-06.md` |
| 7 | Source-faithful Zhao-Cui anchor track | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-source-faithful-track-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-source-faithful-track-result-2026-07-06.md` |
| 8 | Comparator and readiness boundary plan | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase8-comparator-readiness-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase8-comparator-readiness-result-2026-07-06.md` |
| 9 | Closeout and reset memo | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase9-closeout-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase9-closeout-result-2026-07-06.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the minimal scalar `zhaocui_fixed` HMC path be moved from launch/hard-veto evidence toward posterior/sampler validity evidence without overstating claims? |
| Baseline/comparator | Completed `hmc-next` closeout and Phase 5 GPU/XLA hard-veto artifact. |
| Primary pass criterion | Each phase passes its hard-veto screen or writes a blocker/result record with no evidence-class upgrade. |
| Veto diagnostics | Wrong baseline, proxy metrics promoted to validity, missing stop condition, unreviewed long/GPU runtime, unsupported source-faithful claim, unsupported convergence/posterior/ranking/readiness claim, invalid artifact, or review nonconvergence. |
| Explanatory diagnostics | Runtime, acceptance, sample summaries, grid/reference summaries, finite checks, R-hat/ESS only when computed under a reviewed phase, and dirty-worktree summaries. |
| Not concluded | HMC convergence, posterior correctness, ranking/superiority, source-faithful parity, default readiness, production readiness, public API/package readiness, or LEDH evidence unless a later phase explicitly earns that claim. |
| Artifacts | Ledger, phase results, review bundles/logs, runtime JSON/Markdown artifacts, quiet logs, reset memo, and stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Use completed `hmc-next` as baseline | Existing closeout | Avoid stale CPU-only baseline | Treat short hard-veto pass as validity evidence | Phase 0 review bundle | Required |
| Start with scalar oracle | Gap analysis | Posterior correctness is highest-leverage missing evidence | Longer chains before target validation | Phase 1 oracle design review | Required |
| Keep oracle CPU/reference separate from GPU runtime | Evidence discipline | Reference checks need independence from HMC runtime | CPU reference mislabeled as production route | Artifact roles/nonclaims | Required |
| Delay long HMC runs | Research workflow | Long runs need reviewed evidence contract | Runtime spend without validity question | Human approval gate | Required |
| Delay source-faithful claims | Zhao-Cui policy | Requires paper and author-source anchors | Ungrounded faithful language | Phase 7 anchor gate | Required |
| Keep adapter internal | Previous closeout | No API/readiness evidence yet | Public export implies readiness | Public export scan in relevant phase | Required |

## Skeptical Plan Audit

Before each phase, Codex records a skeptical audit in chat and, for material
phases, in the execution ledger. Check wrong baselines, proxy metrics promoted
to pass criteria, missing stop conditions, unfair comparisons, hidden
assumptions, stale context, environment mismatch, and commands whose artifacts
would not answer the phase question.

Initial audit: `PASS_WITH_BOUNDARIES`. The plan starts with governance and a
scalar reference-oracle design. It does not run a long HMC command before a
reviewed evidence contract exists.

## Visible State Machine

Each phase proceeds through `PRECHECK`, `EXECUTE_MINIMAL`, `ASSESS_GATE`,
`PASS_REVIEW`, `REPAIR_LOOP`, and `ADVANCE_OR_STOP`. Advance only after the
current phase gate passes.

## Claude Read-Only Review Command

Use compact bundles through:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/ubuntu/python/BayesFilter \
  --review-name <review-name> \
  --bundle /home/ubuntu/python/BayesFilter/docs/reviews/<bundle>.md \
  --probe-timeout 90 \
  --timeout-seconds 180 \
  --max-retries 1 \
  --allow-bounded-fallback
```

Run the gate with trusted/escalated permissions. If Claude/probe is unavailable
or external review is blocked, record the reason and use a fresh visible
read-only Codex substitute review. Do not treat silence, timeout, or fallback
agreement as proof of correctness.

## Human-Required Stop Conditions

Stop if continuing would require package installation, network fetch,
credentials, destructive git/filesystem action, public API/default-policy
change, model-file edit, unreviewed trusted GPU/XLA runtime, unreviewed long
HMC run, source-faithful/scientific claim boundary crossing, or continuing
after five review rounds fail to converge.
