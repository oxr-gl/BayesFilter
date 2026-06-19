# Agent B Plan: Independent Test And Review Harness For Reduced-Rank Nystrom

Date: 2026-06-18

## Agent Role

Agent B owns independent tests, artifact validation, and review of Agent A's
reduced-rank Nystrom ladder.  Agent B is a skeptical verifier, not the primary
implementation owner.

Agent B must not silently rewrite Agent A's implementation or result artifacts.
During the initial independent review pass, Agent B is read-only on Agent
A-owned files.  If Agent B finds a bug, it must first write a finding with
file/line evidence, a minimal reproducer, and the affected gate.  Any repair to
Agent A-owned files may occur only in a clearly logged follow-up
handoff/amendment after the independent verdict is recorded.

## Objective

Independently determine whether Agent A's reduced-rank Nystrom ladder artifacts
answer their stated evidence contract and preserve the Phase 10 non-claims.

Agent B does not select a production/default algorithm.  Agent B does not rank
Nystrom against semantic-replacement lanes and does not treat runtime/memory
proxies as promotion evidence before validity gates pass.

## Required Context To Load First

Read these files before writing tests or reviews:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-reboot-reset-memo-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p10-comparative-decision-result-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-agent-a-reduced-rank-nystrom-ladder-plan-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-result-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p01-baseline-fixture-spec-2026-06-17.md`
- `docs/benchmarks/scalable_ot_candidate_result_schema.py`
- `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
- `tests/test_nystrom_transport_tf.py`

If Agent A's Phase 11 result exists, read it before executing review checks:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-reduced-rank-nystrom-ladder-result-2026-06-18.md`
- `docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.json`
- `docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.md`

Preserve unrelated dirty worktree changes.  Do not revert HMC/linear/test files
outside this scalable OT Nystrom verification scope.

## Owned Files

Agent B may create or edit:

- `tests/test_nystrom_transport_tf_independent.py`
- `docs/benchmarks/scalable_ot_p11_nystrom_independent_review.py`
- `docs/benchmarks/scalable-ot-p11-nystrom-independent-review-2026-06-18.json`
- `docs/benchmarks/scalable-ot-p11-nystrom-independent-review-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-nystrom-independent-review-result-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p00-intake-readiness-result-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p01-independent-unit-test-harness-result-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p02-artifact-review-script-result-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p03-independent-review-execution-result-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p04-closeout-decision-result-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-visible-execution-ledger-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-visible-stop-handoff-2026-06-18.md`

Agent B must not edit Agent A-owned implementation, diagnostic, JSON/Markdown,
or result-note files during the initial independent review pass.  Repairs to
Agent A-owned files require a separate follow-up handoff/amendment after the
independent verdict lands.

## Review Questions

Agent B must answer:

1. Does Agent A's diagnostic use the Phase 1 local dense TensorFlow baseline as
   comparator?
2. Are reduced-rank records genuinely reduced rank rather than full-rank replay
   wearing a reduced-rank label?
3. Do candidate records validate under the Phase 3 schema?
4. Are finite checks, row/column residuals, dense-reference errors, and shape
   checks present for every required fixture/rank record?
5. Are runtime and memory proxies classified as explanatory only unless
   validity gates pass?
6. Are source-route claims limited to cited source-faithful operations, with
   deterministic landmarks and local FilterFlow adapters classified as
   `fixed_hmc_adaptation` or `extension_or_invention`?
7. Does the result preserve all non-claims from Phase 10?
8. Is there at least one LEDH-specific deterministic fixture, and is it treated
   as a diagnostic rather than posterior correctness?
9. Does every direct top-level Agent A `candidate_records` entry use a
   `baseline_comparator` string beginning `phase1_dense_streaming`?
10. Does Agent A's Phase 11 JSON use the declared manifest shape with one
    direct Phase 3-valid `candidate_records` entry per fixture/rank pair,
    identified by `diagnostics.fixture` and `diagnostics.rank_label`?

## Independent Test Scope

Required independent tests:

1. Import and shape tests for `nystrom_transport_resample_tf`.
2. Explicit rank tests showing `rank < N` produces factor shapes with the
   declared rank.
3. Full-rank replay guard against the Phase 4 behavior.
4. Batch-shape test with `B > 1`.
5. Orientation test: materialized transport rows and columns match the declared
   `source_rows_target_columns` convention used by Phase 3 records.
6. Nonfinite guard: invalid inputs must not silently produce valid-looking
   candidate records.
7. Artifact schema test against Agent A's JSON, if present.
8. Non-claim text check against Agent A's result, if present.

Items 1-6 are Phase B1 implementation-invariant tests.  Items 7-8 are
artifact-review checks executed by the B2/B3 review script and preserved in the
B3/B4 review artifacts.

Tests should be small and CPU-only.  They must not fetch network sources,
install packages, use GPU evidence, execute POT/external code, or depend on
stochastic randomness.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do Agent A's reduced-rank Nystrom implementation and artifacts satisfy the declared Phase 11 evidence contract without unsupported claims or unfair comparisons? |
| Baseline/comparator | Agent A's artifacts must use the Phase 1 local dense/streaming TensorFlow comparator pair, and every candidate record must use a `baseline_comparator` string beginning `phase1_dense_streaming`.  Agent B compares artifacts against Agent A's plan and Phase 3 schema, not against external OT libraries. |
| Primary pass criterion | Independent tests pass; Agent A's JSON validates under Phase 3 schema; required fixtures/ranks are present; reduced-rank records are genuinely reduced; result text preserves non-claims and diagnostic roles. |
| Promotion veto | Missing schema validation; missing reduced-rank records; full-rank-only result promoted as reduced-rank; missing dense-reference errors; invalid residuals; runtime/memory proxy promoted before validity; unsupported source-faithfulness claim; default/speedup/ranking/posterior claim. |
| Continuation veto | Agent A result artifacts are absent; implementation cannot be imported in CPU-only mode; JSON is structurally unreadable; evidence contract cannot be checked because required fields are missing. |
| Repair trigger | Missing text field, artifact naming mismatch, rank-grid omission, diagnostic-role omission, source-route wording overclaim, narrow orientation or shape test failure. |
| Explanatory diagnostics | Test timings, artifact field inventory, per-fixture/rank coverage table, non-claim text matches, source-route classification table. |
| Not concluded | No speedup, no production/default readiness, no posterior correctness, no HMC readiness, no statistically supported ranking, and no broad scalable-OT decision. |
| Artifact preserving result | Independent test file, independent review script, JSON/Markdown review artifacts, review result note, ledger update, stop handoff update. |

## Diagnostic Role Ledger

| Diagnostic | Role |
| --- | --- |
| import and syntax checks | hard veto |
| independent unit tests | hard veto for review pass |
| Agent A JSON readability | hard veto |
| Phase 3 schema validation | hard veto |
| `baseline_comparator` prefix check | hard veto |
| required fixture/rank coverage | hard veto |
| genuine reduced-rank factor shapes | promotion veto if absent |
| non-claim preservation | promotion veto |
| source-route wording audit | promotion veto and repair trigger |
| runtime/memory field presence | explanatory unless Agent A used it as promotion |
| observed dense-reference errors | checked for presence and role, not reranked |

## Skeptical Plan Audit

- Wrong baseline risk: verify Agent A used Phase 1 local dense TensorFlow
  outputs, not an external library or Phase 4 full-rank result as the baseline.
- Proxy metric risk: search result text and JSON roles for runtime/memory
  promotion before validity.
- Missing stop conditions: block review pass if required JSON/result artifacts
  are absent or schema validation cannot run.
- Unfair comparison risk: block any ranking against positive-feature,
  low-rank-coupling, sparse/localized, sliced/subspace, exact online/GPU, or
  Mini-batch/BoMb.
- Hidden assumptions: verify rank grid, landmark rule, epsilon/scaling,
  orientation, dtype, and CPU-only policy are recorded.
- Stale context risk: reload the reboot memo and Agent A plan before judging
  artifacts.
- Artifact mismatch risk: confirm that the artifacts would actually answer the
  stated review questions.

This review plan passes its pre-execution audit only if Agent B checks the
artifact content and diagnostic roles before interpreting any metric.

## Required Commands

Minimum checks:

```bash
python -m py_compile tests/test_nystrom_transport_tf_independent.py docs/benchmarks/scalable_ot_p11_nystrom_independent_review.py
pytest -q tests/test_nystrom_transport_tf_independent.py
python docs/benchmarks/scalable_ot_p11_nystrom_independent_review.py --agent-a-json docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.json --agent-a-result docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-reduced-rank-nystrom-ladder-result-2026-06-18.md --output docs/benchmarks/scalable-ot-p11-nystrom-independent-review-2026-06-18.json --markdown-output docs/benchmarks/scalable-ot-p11-nystrom-independent-review-2026-06-18.md
```

Agent B may also run `pytest -q tests/test_nystrom_transport_tf.py` as
supplementary Agent A regression context, but that command is not part of the
core independent pass/fail gate.

If Agent A artifacts do not yet exist, Agent B may run only import/unit tests
and must record status
`PHASE_11_NYSTROM_INDEPENDENT_REVIEW_BLOCKED_WAITING_FOR_AGENT_A_ARTIFACTS`
rather than inventing substitute evidence.  Do not use shortened blocked-status
aliases.

## Review Result Requirements

Write
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-nystrom-independent-review-result-2026-06-18.md`
with:

- status;
- evidence contract result;
- run manifest with git commit, commands, environment, CPU/GPU status, wall
  time, and artifact paths;
- findings table ordered by severity;
- decision table;
- inference-status table;
- artifact coverage table;
- independent test summary;
- source-route and non-claim audit;
- post-review red-team note;
- exact handoff back to Agent A or to the next comparative-decision phase.

Allowed result statuses:

- `PHASE_11_NYSTROM_INDEPENDENT_REVIEW_AGREE`
- `PHASE_11_NYSTROM_INDEPENDENT_REVIEW_REVISE`
- `PHASE_11_NYSTROM_INDEPENDENT_REVIEW_BLOCKED_WAITING_FOR_AGENT_A_ARTIFACTS`

`AGREE` means the review found no material blocker under this plan.  It does
not mean Nystrom is production-ready, fastest, best, posterior-correct, or the
BayesFilter default.

## Finding Severity Guide

Use these severities:

| Severity | Meaning |
| --- | --- |
| `BLOCKER` | Invalidates the Phase 11 evidence contract or prevents artifact review. |
| `HIGH` | Allows execution but would make interpretation unsafe without repair. |
| `MEDIUM` | Narrow defect or missing diagnostic that should be repaired before comparative synthesis. |
| `LOW` | Wording, clarity, or minor artifact completeness issue. |

Every finding must include:

- file/path;
- line or JSON field when available;
- violated gate;
- minimal reproduction or check;
- recommended narrow repair;
- whether the issue blocks `AGREE`.

## Stop And Handoff Conditions

Stop and write a blocked review if:

- Agent A artifacts are not present;
- Agent A JSON cannot be read;
- TensorFlow import fails in CPU-only mode and prevents independent tests;
- schema validation cannot run;
- the implementation requires unapproved external package/network/GPU actions;
- Agent A's result makes a default/speedup/ranking/posterior claim that cannot
  be repaired by narrow wording changes.

On completion, hand off:

- independent review status;
- findings and severities;
- exact commands run;
- test and review artifact paths;
- whether Agent A may proceed to result closeout;
- whether a comparative-decision update is justified.
