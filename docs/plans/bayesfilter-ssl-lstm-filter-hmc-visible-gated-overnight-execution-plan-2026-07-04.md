# SSL-LSTM Filter-HMC Visible Gated Overnight Execution Plan

Date: 2026-07-04

Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only. Claude cannot authorize crossing human,
runtime, model-file, funding, product-capability, default-policy, public API, or
scientific-claim boundaries.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, detached `tmux`, or copied-workspace supervisors;
- backgrounded phase runners;
- Claude as executor.

This is an overnight-capable visible runbook: execution remains recoverable in
the current conversation and every phase gate writes artifacts before advancing.

## Quiet Visible Execution Pattern

Full command output is an artifact, not chat content.

1. Predeclare log and structured artifact paths in the phase subplan or ledger.
2. Redirect large stdout/stderr to a log file.
3. Prefer commands that write JSON/Markdown result artifacts directly.
4. After a command, report only exit status, artifact paths, pass/fail fields,
   and at most the last 20-40 log lines on failure.
5. Poll bounded status commands instead of streaming long processes.
6. Treat excessive output as an execution-flow defect and write a stop handoff
   if it destabilizes the visible session.

## Program

Master program:

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-master-program-2026-07-04.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-claude-review-ledger-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase0-claude-review-bundle-2026-07-04.md`

Execution ledger:

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-visible-execution-ledger-2026-07-04.md`

Stop handoff:

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-visible-stop-handoff-2026-07-04.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Planning/governance | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase0-planning-governance-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase0-planning-review-result-2026-07-04.md` |
| 1 | SSL model/estimand | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase1-ssl-model-estimand-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase1-ssl-model-estimand-result-2026-07-04.md` |
| 2 | Value/score protocol | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase2-value-score-protocol-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase2-value-score-protocol-result-2026-07-04.md` |
| 3 | SGQF/UKF adapters | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase3-sgqf-ukf-analytic-adapters-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase3-sgqf-ukf-analytic-adapters-result-2026-07-04.md` |
| 4 | Zhao-Cui fixed adapter | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase4-zhaocui-fixed-analytic-adapter-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase4-zhaocui-fixed-analytic-adapter-result-2026-07-04.md` |
| 5 | LEDH manual VJP adapter | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase5-ledh-streaming-ot-manual-vjp-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase5-ledh-streaming-ot-manual-vjp-result-2026-07-04.md` |
| 6 | Shared benchmark | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase6-benchmark-runner-invariant-metrics-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase6-benchmark-runner-invariant-metrics-result-2026-07-04.md` |
| 7 | HMC evidence ladder | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase7-hmc-evidence-ladder-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase7-hmc-evidence-ladder-result-2026-07-04.md` |
| 8 | Closeout | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase8-closeout-reset-boundary-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase8-closeout-reset-boundary-result-2026-07-04.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can visible gated execution build and evaluate HMC plus BayesFilter filtering adapters for SSL-LSTM estimation without crossing the declared boundaries? |
| Baseline/comparator | Same SSL-LSTM fixtures, same priors, same HMC runtime, same metric suite across candidate filters; Kalman/affine fixtures are sanity checks only. |
| Primary pass criterion | Each phase advances only if its result artifact satisfies its own evidence contract and no veto fires. |
| Veto diagnostics | Missing required artifact, failed local check, Claude `REVISE` not repaired within five rounds, non-finite numerical evidence, unsupported source/gradient claim, or human-boundary requirement. |
| Explanatory diagnostics | Runtime, command logs, descriptive metric tables, code coverage notes, and reviewer comments that do not affect the gate. |
| Not concluded | Exact posterior correctness, parameter identifiability, method superiority, production/default readiness, or author-source faithfulness. |
| Artifacts | Files under `docs/plans`, `.claude_reviews`, and later reviewed benchmark output paths. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| TensorFlow/TFP backend | Project AGENTS policy | BayesFilter default implementation backend | NumPy prototype accidentally promoted | Import/backend audit in Phase 2 | Required |
| GPU/XLA production target | Project AGENTS policy | Default execution target for serious paths | CPU debug artifact treated as production evidence | Phase 6/7 manifest records device/JIT/TF32 | Required |
| HMC over parameters | User directive | Test is HMC plus filtering algorithms, not latent-path MCMC | Accidentally diverging to Particle Gibbs/CSMC | Master nonclaims and Phase 7 gate | Locked |
| Invariant estimation metrics | User clarification | SSL-LSTM parameters are non-identifiable | Parameter matching treated as success | Phase 6 metric schema | Required |
| Analytic/manual gradients | User directive | HMC needs deterministic target scores | GradientTape helper used as target path | Phase 2/3/4/5 authority checks | Required |
| Zhao-Cui fixed variant | User directive and project source-anchor gate | Differentiability/HMC requires frozen route | Adaptive randomness or unanchored author claim | Phase 4 source and fixed-branch audit | Required |
| LEDH manual VJP streaming OT | User directive | Target score must follow manual VJP path | Existing autodiff score mistaken as accepted target | Phase 5 VJP evidence gate | Required |

## Skeptical Plan Audit

Before executing any phase, Codex records an audit in the execution ledger. The
audit checks wrong baselines, proxy metrics treated as pass criteria, missing
stop conditions, unfair comparisons, hidden assumptions, stale context,
environment mismatch, and commands whose artifacts would not answer the phase
question.

If the audit finds a material flaw, Codex revises the plan or writes a blocker
note before running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`: read the subplan, confirm prerequisites, restate the evidence
   contract, and append a ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands in this conversation and use
   the smallest diagnostic or implementation needed.
3. `ASSESS_GATE`: compare outputs against the primary criterion and vetoes, then
   write the phase result.
4. `PASS_REVIEW`: send material phase results or next subplans to Claude using a
   bounded read-only review bundle or `claude_review_gate.sh`.
   If Claude fails to return a material verdict, run a separate local Codex
   read-only substitute review on the same bounded bundle and record the
   fallback before advancing.
5. `REPAIR_LOOP`: patch the same subplan or result, rerun focused checks, and
   repeat Claude review at most five rounds for the same blocker. If Claude
   fails to return a material verdict, use one Codex substitute review on the
   same bounded bundle before widening scope.
6. `ADVANCE_OR_STOP`: advance only after the gate passes; otherwise write the
   stop handoff.

## Claude Review Gate Command Shape

Use the hardened review gate for material subplans and results:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/ubuntu/python/BayesFilter \
  --review-name <stable-review-name> \
  --bundle <bounded-bundle-inside-repo> \
  --model opus \
  --effort max \
  --probe-effort low \
  --timeout-seconds 180 \
  --probe-timeout 90 \
  --max-retries 1
```

If Claude does not return a material verdict, inspect the probe status. If the
probe succeeds, redesign the review bundle to be smaller or more explicit and
retry. If the probe fails in a non-trusted context, rerun with trusted/elevated
Claude permissions before treating the failure as real. If Claude still fails
to return a material verdict, do not widen the bundle; run a separate local
Codex read-only substitute review on the same bounded bundle and record the
fallback path in the execution ledger and review ledger.

## Human-Required Stop Conditions

Stop if continuing would require package installation, network fetch, credentials,
destructive git/filesystem operations, model-file edits, default-policy changes,
new public API commitments, broader scientific claims, changing pass/fail
criteria after seeing results, modifying unrelated dirty work, or continuing
after Codex and Claude do not converge after five rounds for the same blocker.

## Final Visible Handoff

The final handoff must include final phase reached, result artifacts, Claude
review trail, tests/benchmarks actually run, unresolved blockers, nonclaims, and
the safest next human decision.
