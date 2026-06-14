# Filtering Value/Gradient Benchmark Gap-Closure Visible Gated Execution Runbook

Date: 2026-06-10

## Status

`VISIBLE_EXECUTION_CONTINUED_WITH_SOURCE_PAPER_SCOPE_REPAIR`

## 2026-06-11 Source-Paper Scope Amendment

The runbook has been launched in the current Codex dialogue.  Codex remains the
visible supervisor and executor; Claude remains read-only reviewer.

The old P44-inclusive P1/P7/P8 roster is preserved as historical provenance for
the earlier diagnostic gap-closure pass.  It is not the promoted source-paper
benchmark scope.

Future promoted source-paper benchmark execution must use:

- blocker-closure plan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-blocker-closure-plan-2026-06-11.md`;
- source-paper scope contract:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`;
- source-paper scope summary:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-summary-2026-06-11.md`.

P44 cubic, P44 quadratic, and P44 tanh-transition diagnostic rows are excluded
from promoted source-paper numeric tables.  Exact Zhao--Cui paper/code values
are the test values for the promoted source-paper rows.  Lower-rung and
project-only fixtures may remain as engineering diagnostics only when labeled
as such.

Generalized SV is amended to be a synthetic benchmark row: use the
Zhao--Cui reported/estimated `svmodels` parameter values as the truth vector and
generate benchmark data from those values.  SP500 returns are not the benchmark
data for that row.  Numeric generalized-SV execution remains blocked until the
estimated parameter vector is extracted, digitized, or regenerated from the
author pipeline; author-code defaults and BayesFilter native fixture values are
not valid substitutes.

The numeric source-paper benchmark remains blocked until accepted source values,
synthetic data or real-data contracts, reviewed evaluators, and value/score/
curvature/stochastic uncertainty tables exist:

```text
BLOCK_FILTER_BENCH_SOURCE_PAPER_NUMERIC_RUN_PENDING
```

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution;
- detached overnight shell supervisors.

Execution must remain visible in the current dialogue.  Each material phase must
be prechecked, executed, assessed, reviewed, repaired if needed, and advanced
only after the phase gate passes.

## Program

Master program:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-closure-master-program-2026-06-10.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-claude-review-ledger-2026-06-10.md`

Visible execution runbook:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-gated-execution-runbook-2026-06-10.md`

Execution ledger:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-execution-ledger-2026-06-10.md`

Stop handoff:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-stop-handoff-2026-06-10.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact | Required token |
| --- | --- | --- | --- | --- |
| P0 | Benchmark Contract And Gap Lock | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p0-contract-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p0-contract-result-2026-06-10.md` | `PASS_FILTER_BENCH_P0_CONTRACT` or `BLOCK_FILTER_BENCH_P0_CONTRACT` |
| P1 | Target Registry And Reference Taxonomy | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p1-target-registry-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p1-target-registry-result-2026-06-10.md` | `PASS_FILTER_BENCH_P1_TARGET_REGISTRY` or `BLOCK_FILTER_BENCH_P1_TARGET_REGISTRY` |
| P2 | Unified Filter Adapter Protocol | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p2-adapter-protocol-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p2-adapter-protocol-result-2026-06-10.md`; concrete adapter schema/interface artifact | `PASS_FILTER_BENCH_P2_ADAPTER_PROTOCOL` or `BLOCK_FILTER_BENCH_P2_ADAPTER_PROTOCOL` |
| P3 | Reference Oracle Wiring | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p3-reference-oracles-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p3-reference-oracles-result-2026-06-10.md` | `PASS_FILTER_BENCH_P3_REFERENCE_ORACLES` or `BLOCK_FILTER_BENCH_P3_REFERENCE_ORACLES` |
| P4 | Deterministic Filter Wiring | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p4-deterministic-filters-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p4-deterministic-filters-result-2026-06-10.md` | `PASS_FILTER_BENCH_P4_DETERMINISTIC_FILTERS` or `BLOCK_FILTER_BENCH_P4_DETERMINISTIC_FILTERS` |
| P5 | DPF Filter Wiring And Supersession Guard | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p5-dpf-filters-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p5-dpf-filters-result-2026-06-10.md` | `PASS_FILTER_BENCH_P5_DPF_FILTERS` or `BLOCK_FILTER_BENCH_P5_DPF_FILTERS` |
| P6 | Gradient Semantics And Status Taxonomy | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p6-gradient-semantics-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p6-gradient-semantics-result-2026-06-10.md` | `PASS_FILTER_BENCH_P6_GRADIENT_SEMANTICS` or `BLOCK_FILTER_BENCH_P6_GRADIENT_SEMANTICS` |
| P7 | Preflight Matrix Coverage | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p7-preflight-matrix-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p7-preflight-matrix-result-2026-06-10.md` | `PASS_FILTER_BENCH_P7_PREFLIGHT_MATRIX` or `BLOCK_FILTER_BENCH_P7_PREFLIGHT_MATRIX` |
| P8a | Synthetic-Truth Benchmark Contract Preflight | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-synthetic-truth-runner-subplan-2026-06-11.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-synthetic-truth-runner-result-2026-06-11.md` | `PASS_FILTER_BENCH_P8_SYNTHETIC_TRUTH_CONTRACT` and `BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING` |
| P8b | Numeric Benchmark Execution And Tables | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-master-plan-2026-06-11.md` plus a 2026-06-12 execution update before launch | reviewed value, componentwise score, curvature/status, failure, and stochastic uncertainty artifacts | `PASS_P8_B7_NUMERIC_BENCHMARK_RUNNER` and `PASS_P8_B8_REVIEWED_CLOSEOUT`, or `BLOCK_P8_B7_NUMERIC_BENCHMARK_RUNNER` |
| P9 | Integration Closeout | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p9-closeout-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p9-closeout-result-2026-06-11.md` | `PASS_FILTER_BENCH_P9_CLOSEOUT` or `BLOCK_FILTER_BENCH_P9_NUMERIC_BENCHMARK_PENDING` |
| Source-paper scope repair | Source-Paper Benchmark Blocker Closure | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-blocker-closure-plan-2026-06-11.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-blocker-closure-result-2026-06-11.md`; source-paper scope JSON/CSV/Markdown | `PASS_FILTER_BENCH_SOURCE_PAPER_BLOCKER_CLOSURE` and `BLOCK_FILTER_BENCH_SOURCE_PAPER_NUMERIC_RUN_PENDING` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Codex visibly execute the reviewed filtering value/gradient benchmark gap-closure master program, with Claude as read-only reviewer, without hidden detachments or unexplained stops? |
| Baseline/comparator | Reviewed master program, phase subplans, P30/P43/P44/P50/P51/P53 ledgers, current Algorithm 1 UKF LEDH-PFPF route, LGSSM Kalman oracle, and declared dense/transformed/mixture references. |
| Primary pass criterion | P0-P9 each emit required result artifacts with pass/block tokens, no phase advances through a failed gate, the repair loop resolves fixable blockers or records a real human-required blocker, and the final closeout decision is reviewed. |
| Veto diagnostics | Detached execution; old LEDH-PFPF-OT used as current evidence; exactness imposed outside LGSSM; stale scalar-only Zhao-Cui blocker used to suppress a benchmarkable row; DPF invalid gradients hidden; frozen roster or manifests missing; Claude review skipped for material phases. |
| Explanatory diagnostics | Focused tests, import checks, schema validation, dense lower-rung tie-outs, MC standard errors, ESS/resampling diagnostics, runtime metadata, and Claude findings. |
| Not concluded | This runbook does not by itself rank algorithms, certify DPF gradients, certify HMC/Bayesian-estimation readiness, or claim GPU performance.  P8a contract success is not P8 numeric completion. |
| Artifacts | Runbook, visible execution ledger, stop handoff, phase result notes, registry/schema JSON, benchmark output matrices, run manifests, and Claude review records. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible execution in this dialogue | User request and template | Recovers state in the conversation and avoids isolated workspace drift | Hidden detached process produces opaque failure | Confirm no `codex exec`, no launcher, no background supervisor | reviewed |
| Codex supervisor/executor | User request and reviewed master program | Keeps implementation and gate decisions in one visible thread | Claude or another process edits or supervises | Claude prompts say read-only; inspect artifacts after review | reviewed |
| Claude read-only reviewer | User request and cross-agent policy | Critical review without delegating execution | Claude prompt too large, hangs, or edits state | If no response, run small probe; if probe works, shorten/split prompt | reviewed |
| CPU-only default validation | `AGENTS.md` GPU policy | Avoids sandbox-misleading GPU failures for ordinary tests | Accidental GPU import/result interpreted incorrectly | Set `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp` before TF/TFP tests | reviewed |
| Exactness is cell-level | Master program | Allows approximate filters on non-Gaussian rows without overclaim | Surrogate or approximate row becomes truth | Require reference type, comparator labels, row class, reason codes | reviewed |
| Frozen roster before full benchmark | Claude-reviewed P7/P8 repairs | Prevents silent matrix holes and coverage drift | Registry changes make incomplete matrix look complete | P7/P8 manifest validates expected row/column roster | reviewed |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and in
the visible execution ledger.  The audit must check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the phase plan or write a blocker
note before running implementation, benchmark, or long diagnostic commands.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan and latest execution ledger.
   - Confirm prerequisite phase tokens and artifacts.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
   - Record the skeptical plan audit.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed to answer the
     phase question.
   - Preserve unrelated dirty worktree changes.
   - Use `apply_patch` for manual file edits.
3. `ASSESS_GATE`
   - Compare outputs against primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
   - Include run manifest for meaningful runs.
4. `PASS_REVIEW`
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan or ledger entry.
   - Get Claude review when material.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Write a blocker result.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the stop handoff if a human-required blocker appears.

## Repair Loop Discipline

Do not stop for fixable issues.

Fixable issues include:

- failed schema validation with clear field repair;
- stale labels or unsupported claims;
- adapter wiring bugs with a focused local fix path;
- missing result metadata or manifest fields;
- failed focused tests where the failure identifies a code or fixture problem;
- Claude `VERDICT: REVISE` findings that name specific fixable flaws;
- oversized Claude prompts that cause no response while a small probe succeeds.

Human-required blockers include:

- package installation, network fetch, credentials, or external runtime setup;
- destructive git/filesystem changes;
- modifying unrelated dirty user work;
- changing pass/fail criteria after seeing results;
- changing backend/default policy;
- GPU/special hardware claims without trusted approval;
- Codex/Claude non-convergence after five review rounds for the same blocker.

## Claude Read-Only Review Protocol

Use this wrapper form for Claude reviews:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name <unique-review-name> \
  --model claude-opus-4-7 \
  --effort max \
  '<prompt>'
```

The prompt must include:

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

Return exactly:
VERDICT: AGREE
or
VERDICT: REVISE
MAJOR:
- ...
MINOR:
- ...
```

Codex must preserve review outputs in the ledger or review artifact and inspect
whether Claude remained read-only.

## Claude Nonresponse Protocol

If Claude does not respond:

1. Wait long enough to distinguish slow review from immediate wrapper failure.
2. Run a minimal trusted probe:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name <probe-name> \
  --model claude-opus-4-7 \
  --effort max \
  'Read-only probe. Reply exactly: PROBE_OK'
```

3. If the probe returns `PROBE_OK`, the issue is the review prompt.  Redesign
   the prompt by:
   - reviewing fewer files;
   - shortening instructions;
   - splitting master, implementation, and result review;
   - asking for only major blockers first.
4. If the probe fails in trusted context, record a Claude availability blocker
   in the ledger and stop only if the phase cannot proceed without review.

Do not declare Claude unavailable merely because a complex prompt stalls.

## Ledger Entry Template

```markdown
### <timestamp> - Phase <P#> - <STATE>

Evidence contract:

- Question:
- Baseline/comparator:
- Primary criterion:
- Veto diagnostics:
- Non-claims:

Skeptical audit:

- Wrong baseline:
- Proxy-promotion risk:
- Stop-condition risk:
- Unfair-comparison risk:
- Hidden-assumption risk:
- Stale-context risk:
- Environment-mismatch risk:
- Artifact-answer risk:

Actions:

- <commands/edits/reviews>

Artifacts:

- <paths>

Gate status:

- <PASSED/BLOCKED/FAILED/IN_PROGRESS>

Next action:

- <next visible step>
```

## Phase Execution Command Policy

Default commands are CPU-only unless a phase explicitly needs trusted GPU
evidence and the user approves it.  For TensorFlow/TFP validation:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q <focused-tests>
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q <paths>
```

For schema and artifact checks:

```text
python -m json.tool <json-file>
git diff --check -- <touched-files>
rg -n <token-or-status> <artifact-paths>
```

Do not run broad test suites or full benchmarks before the phase evidence
contract and skeptical audit are recorded.

## Anticipated Approval Requests

Before launch, ask the user to approve the following for smooth visible
execution:

1. Trusted Claude Code wrapper use for read-only reviews and small probes:
   `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh ...`
2. Focused CPU-only TensorFlow/TFP validation commands with
   `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`.
3. Focused `pytest`, `python -m compileall`, `python -m json.tool`, `rg`, and
   `git diff --check` commands.
4. File edits inside `/home/chakwong/BayesFilter` needed to implement P0-P9,
   preserving unrelated dirty worktree changes.
5. Later full benchmark runs only after P8a passes, stale P8 source-row
   manifests are refreshed, and the P8b numeric evidence contract is restated
   in chat.

No approval is requested here for network fetches, package installation, GPU
runs, detached agents, destructive git operations, or changing benchmark
criteria after seeing results.

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

## Launch Status

Do not launch this runbook until the user explicitly asks to launch after
reviewing the runbook and approvals.
