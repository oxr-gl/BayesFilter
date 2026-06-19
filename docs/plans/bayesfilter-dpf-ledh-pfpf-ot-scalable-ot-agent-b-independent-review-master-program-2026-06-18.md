# Master Program: Agent B Independent Review Of Reduced-Rank Nystrom

Date: 2026-06-18

## Status

`DRAFT_AGENT_B_INDEPENDENT_REVIEW_MASTER_PROGRAM`

## Program Objective

Execute Plan B in this lane: independently test, validate, and review Agent A's
Phase 11 reduced-rank Nystrom ladder artifacts without editing Agent A-owned
implementation, diagnostic, JSON/Markdown, or result-note files during the
initial independent review pass.

This program does not implement a new OT algorithm, choose a BayesFilter
default, claim speedup, rank algorithms, establish posterior correctness, or
establish HMC/production readiness.

## Inputs

- Agent B parent plan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-agent-b-independent-test-review-harness-plan-2026-06-18.md`
- Required parent context loaded by B0:
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-reboot-reset-memo-2026-06-18.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p10-comparative-decision-result-2026-06-17.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-agent-a-reduced-rank-nystrom-ladder-plan-2026-06-18.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-result-2026-06-17.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p01-baseline-fixture-spec-2026-06-17.md`
  - `docs/benchmarks/scalable_ot_candidate_result_schema.py`
- Agent A Phase 11 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-reduced-rank-nystrom-ladder-result-2026-06-18.md`
- Agent A diagnostic JSON:
  `docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.json`
- Agent A diagnostic Markdown:
  `docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.md`
- Agent A implementation:
  `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| B0 | Intake and readiness gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p00-intake-readiness-subplan-2026-06-18.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p00-intake-readiness-result-2026-06-18.md` |
| B1 | Independent unit-test harness | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p01-independent-unit-test-harness-subplan-2026-06-18.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p01-independent-unit-test-harness-result-2026-06-18.md` |
| B2 | Independent artifact review script | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p02-artifact-review-script-subplan-2026-06-18.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p02-artifact-review-script-result-2026-06-18.md` |
| B3 | Independent review execution | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p03-independent-review-execution-subplan-2026-06-18.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p03-independent-review-execution-result-2026-06-18.md` |
| B4 | Closeout and decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p04-closeout-decision-subplan-2026-06-18.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p04-closeout-decision-result-2026-06-18.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do Agent A's reduced-rank Nystrom artifacts satisfy their declared Phase 11 evidence contract without unsupported claims, unfair comparisons, schema drift, or boundary violations? |
| Baseline/comparator | Agent A's artifacts must use the Phase 1 local dense/streaming TensorFlow comparator pair and every candidate record must use a `baseline_comparator` string beginning `phase1_dense_streaming`. |
| Primary pass criterion | Agent B produces independent tests and artifact-review artifacts that pass, validates all direct top-level Agent A `candidate_records` under the Phase 3 schema, checks required fixture/rank coverage and manifest invariants, and writes an evidence-class-aware review result. |
| Veto diagnostics | Missing Agent A artifact, schema failure, invalid baseline prefix, missing dense-reference errors, missing required fixture/rank, full-rank-only promotion, unsupported source-faithfulness/default/speedup/posterior/ranking claim, or Agent B editing Agent A-owned files during initial review. |
| Explanatory diagnostics | Unit-test timings, review-script coverage fields, runtime/memory proxy presence, per-fixture/rank summaries, source-route wording inventory, and residual-risk notes. |
| Not concluded | No speedup, no production/default readiness, no posterior correctness, no HMC readiness, no statistically supported ranking, and no broad scalable-OT decision. |
| Artifacts | Phase B0-B4 results, standalone parent-required review result `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-nystrom-independent-review-result-2026-06-18.md`, independent test file, independent review script, JSON/Markdown review artifacts, visible execution ledger, stop handoff, and Claude review notes. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| CPU-only TensorFlow checks | BayesFilter GPU policy and Agent B plan | Independent review does not need GPU evidence. | TensorFlow emits GPU warnings despite CPU hiding. | Record `CUDA_VISIBLE_DEVICES=-1` and classify warnings as environment noise. | Reviewed constraint |
| Read-only Agent B posture toward Agent A files | Claude-converged Agent B plan | Preserves independent verification. | Agent B silently fixes Agent A artifact and masks finding. | Phase B0 file-ownership gate and `git status` snapshot. | Reviewed constraint |
| Manifest validation over ad hoc text inspection | Phase 3 schema and Agent A Phase 11 result | Ensures review answers the stated artifact question. | Markdown passes while JSON records drift. | Phase B2 review script validates every direct top-level `candidate_records` entry. | Reviewed constraint |
| Claude as reviewer only | User instruction and runbook template | Keeps Codex responsible for execution and boundaries. | Claude treated as execution authority. | Review prompts say read-only and Codex independently applies findings. | Reviewed constraint |

## Program-Level Stop Conditions

Stop and write a blocker result if:

- Agent A Phase 11 artifacts are absent or structurally unreadable;
- TensorFlow import fails in CPU-only mode and prevents independent tests;
- independent review requires editing Agent A-owned files before the first
  independent verdict;
- a repair would change Agent A's pass/fail criteria after seeing results;
- continuing would require package installation, network access, GPU evidence,
  external OT execution, destructive git/filesystem action, or a default-policy
  change;
- Claude and Codex fail to converge after five review rounds on the same
  material blocker.

## Repair Loop Protocol

For each phase:

1. Run the smallest focused local check that can expose the issue.
2. If the issue is in an Agent B-owned artifact, patch it visibly and rerun the
   focused check.
3. If the issue is in an Agent A-owned artifact, write a finding and stop or
   hand off; do not silently repair Agent A files in the initial review pass.
4. For material subplan/result changes, use Claude as read-only reviewer.
5. Stop after five Claude rounds for the same blocker and write a blocker
   result.

## Final Program Statuses

- `AGENT_B_INDEPENDENT_REVIEW_AGREE`
- `AGENT_B_INDEPENDENT_REVIEW_REVISE_AGENT_A`
- `AGENT_B_INDEPENDENT_REVIEW_BLOCKED`
