# Actual-SIR Nystrom Visible Gated Execution Runbook

Date: 2026-06-24

Status: `G1_READY_VISIBLE_EXECUTION`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.  Claude may review material subplans or
boundary decisions, but cannot edit files, run experiments, launch agents,
authorize default promotion, or cross human/product/scientific boundaries.

This visible runbook must not launch detached execution with `codex exec`,
`overnight_gated_launch.sh`, `setsid`, `nohup`, detached `tmux`, backgrounded
phase runners, or copied-workspace execution.

## Quiet Visible Execution Pattern

For TensorFlow/GPU benchmark commands:

1. predeclare JSON, Markdown, and log paths in the subplan;
2. redirect full stdout/stderr to the log file;
3. inspect structured JSON after each command;
4. report only exit status, artifact paths, pass/fail fields, and bounded log
   tails on failure;
5. stop on malformed or missing artifacts before interpreting metrics.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-governed-gap-execution-master-program-2026-06-24.md`

Governance plan:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-evidence-governance-and-gap-plan-2026-06-24.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-visible-execution-ledger-2026-06-24.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-visible-stop-handoff-2026-06-24.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| G1 | Broader `N=8192` fixed-policy replication | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g1-n8192-broader-replication-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g1-n8192-broader-replication-result-2026-06-24.md` |
| G2 | Repair selection or scope decision | To be drafted after G1 | To be drafted after G1 |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the restricted fixed-policy Nystrom route show repeated `N=8192` paired-threshold failures beyond the known hard seed? |
| Baseline/comparator | Same-artifact compiled streaming TF32 actual-SIR route. |
| Primary pass/classification criterion | Complete valid seed-panel artifacts for seeds `82924..82931`, then classify by predeclared failure count. |
| Veto diagnostics | Missing/malformed artifacts, wrong policy metadata, missing trusted GPU/TF32 evidence, nonfinite outputs, residual hard veto, comparator failure, timeout. |
| Explanatory diagnostics | Runtime, warm ratio, ESS, residual magnitudes below threshold, paired delta magnitudes, factor/scaling diagnostics. |
| Not concluded | No statistical failure probability, no default readiness, no ranking, no HMC readiness, no posterior correctness. |
| Artifacts | G1 JSON/Markdown/log artifacts, execution ledger, G1 result, refreshed G2 subplan or blocker. |

## Skeptical Plan Audit Requirement

Before any benchmark run, Codex must verify:

- baseline is the compiled streaming TF32 route in the same paired artifact;
- no runtime/ESS/proxy metric is promoted to a pass criterion;
- stop conditions are explicit;
- comparison uses the same model, seeds, dtype, TF32 mode, transport policy,
  route request, and policy metadata;
- old quarantined runtime artifacts are not used as speed evidence;
- command artifacts answer the G1 question.

## Forbidden Claims/Actions

- Do not claim default readiness.
- Do not claim HMC readiness.
- Do not claim posterior correctness.
- Do not claim statistical ranking or statistical failure probability.
- Do not tune rank, epsilon, solver, thresholds, chunks, model, or seeds inside
  G1.
- Do not launch repair until G1 writes a result with a valid handoff condition.

## Stop Conditions

- Trusted GPU unavailable for required GPU rows.
- Any launched row times out.
- Required JSON, Markdown, or log artifact is missing.
- JSON artifact is malformed or missing required metadata.
- Fixed-policy metadata, comparator route, dtype, TF32 mode, or selected GPU
  evidence mismatches the subplan.
- Continuing would require tuning, threshold changes, default-policy decisions,
  or unsupported claims.

## Advancement Rule

Advance from G1 only after:

- local artifact checks pass;
- G1 result/close record exists;
- G2 subplan or blocker is drafted;
- boundary claims are audited locally;
- material review is complete if G1 opens repair, scope restriction, or default
  decision boundaries.
