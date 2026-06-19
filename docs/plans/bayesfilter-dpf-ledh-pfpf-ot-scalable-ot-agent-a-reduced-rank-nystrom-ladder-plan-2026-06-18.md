# Agent A Plan: Reduced-Rank Nystrom Ladder Implementation

Date: 2026-06-18

## Agent Role

Agent A owns the reduced-rank Nystrom implementation and primary ladder
diagnostic artifacts for the next scalable OT round.

Agent A must not change BayesFilter defaults, public APIs, unrelated HMC/linear
files, or semantic-replacement lanes.  Agent A may edit only the Nystrom
implementation, focused Nystrom tests, Nystrom ladder diagnostics, and result
artifacts named in this plan unless a reviewed amendment expands scope.

## Objective

Test whether the Phase 4 full-rank TensorFlow Nystrom factor route remains
valid and useful at reduced ranks on deterministic Phase 1 fixtures plus at
least one LEDH-specific fixture.

This is a diagnostic implementation ladder.  It is not a production/default
selection, speedup claim, posterior-correctness claim, HMC-readiness claim, or
statistically supported ranking.

## Required Context To Load First

Read these files before editing code:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-reboot-reset-memo-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-reset-memo-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p10-comparative-decision-result-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-result-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p01-baseline-fixture-spec-2026-06-17.md`
- `docs/benchmarks/scalable_ot_candidate_result_schema.py`
- `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
- `tests/test_nystrom_transport_tf.py`

Preserve unrelated dirty worktree changes.  The reboot memo records unrelated
dirty files in BayesFilter HMC/linear/test areas; do not revert or reformat
them.

## Source Anchors Required Before Coding

Re-read and cite these when claiming source-faithful operations:

| Anchor | Required use |
| --- | --- |
| `.localsource/1812.05189-src/sections/nystrom.tex` lines 10-27 | Nystrom Gaussian factors, `V A^{-1} V^T`, Cholesky/triangular-solve matvec route. |
| `.localsource/1812.05189-src/sections/nystrom.tex` lines 121-172 | Adaptive Nystrom context only; do not claim the deterministic reduced-rank ladder is adaptive source-faithful. |
| `.localsource/1812.05189-src/sections/sinkhorn.tex` lines 8-24 and 41-50 | Approximate-kernel Sinkhorn scaling, marginal residual target, matvec-based route. |
| `.localsource/scalable_ot_code_audit/POT/ot/lowrank.py` lines 530-730 | Reference Nystrom factors, low-rank Sinkhorn scaling, lazy plan conventions. |
| `.localsource/scalable_ot_code_audit/POT/ot/bregman/_empirical.py` lines 766-865 | Empirical Nystrom wrapper and `reg`/`sigma` mapping context. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex` lines 437-545 | Local notation for factors, matvecs, approximate plan, residuals, transported-particle error. |

## Entry Conditions

- Phase 10 status is
  `PHASE_10_COMPARATIVE_DECISION_COMPLETED_NO_DEFAULT_ALGORITHM_YET`.
- Phase 4 Nystrom full-rank factor route passed, but reduced-rank behavior is
  untested.
- Phase 1 dense/streaming TensorFlow baseline remains the comparator.
- Phase 3 candidate schema remains the result-record schema.
- Agent B may independently create tests/review artifacts, but Agent B is not
  allowed to silently change Agent A's implementation files.

## Owned Files

Agent A may create or edit:

- `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
- `tests/test_nystrom_transport_tf.py`
- `docs/benchmarks/scalable_ot_p11_reduced_rank_nystrom_ladder_diagnostics.py`
- `docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.json`
- `docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.md`
- `docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.log` if needed
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-reduced-rank-nystrom-ladder-result-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-visible-execution-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-visible-stop-handoff-2026-06-17.md`

Agent A must not edit Agent B's independent test/review artifacts except to
address a finding in Agent A-owned implementation or diagnostics.

## Implementation Scope

Required implementation work:

1. Preserve the existing full-rank Nystrom behavior.
2. Add reduced-rank ladder support if the current API cannot already express
   all required ranks robustly.
3. Keep TensorFlow/TensorFlow Probability as the implementation backend.
4. Keep deterministic rank/landmark choices for reproducibility.
5. Record source-route classification for every nontrivial operation:
   `source_faithful`, `fixed_hmc_adaptation`, or `extension_or_invention`.
6. Emit a Phase 3-valid candidate result for every diagnostic record.
7. Include memory/runtime proxy fields, but classify them as explanatory until
   validity gates pass.
8. Write the Phase 11 JSON as a manifest containing one Phase 3-valid
   `candidate_record` per fixture/rank record plus a summary section.  Every
   nested `candidate_record.baseline_comparator` must begin with
   `phase1_dense_streaming` to satisfy the local schema convention.

Forbidden implementation work:

- Do not change BayesFilter production defaults.
- Do not expose a public API.
- Do not use NumPy as an algorithmic backend in BayesFilter-owned code.
- Do not fetch network sources, install packages, execute POT/external code, or
  use GPU evidence.
- Do not claim speedup, scalability, ranking, posterior correctness,
  HMC-readiness, or production readiness.
- Do not unblock Mini-batch/BoMb.
- Do not implement sparse/localized, exact online/GPU, positive-feature,
  sliced/subspace, or low-rank solver routes in this plan.

## Fixture Ladder

Run at minimum:

| Fixture | Source | Required ranks |
| --- | --- | --- |
| `tiny_manual` | Phase 1 | `1, 2, 3, full` |
| `small_parity` | Phase 1 | `2, 4, 8, full` |
| `high_dim_low_rank` | Phase 1 | `2, 4, 8, 16, full` |
| `high_dim_locality` | Phase 1 | `2, 4, 8, 16, full` |
| `ledh_specific_smoke` | new deterministic LEDH-like fixture | `2, 4, 8, 16, full` or all ranks not exceeding particle count |

The LEDH-specific fixture must be deterministic, CPU-only, and recorded in the
diagnostic script.  It should mimic post-flow particle geometry enough to catch
rank sensitivity, but it must not be interpreted as posterior correctness.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the reduced-rank Nystrom factor route preserve finite, schema-valid transport and dense-reference agreement well enough on Phase 1 and LEDH-specific fixtures to justify deeper LEDH-PFPF-OT testing? |
| Baseline/comparator | Phase 1 local dense/streaming TensorFlow comparator pair.  Every Phase 3 candidate record must use a `baseline_comparator` string beginning `phase1_dense_streaming`; dense-reference errors are diagnostics against the dense materialized member of that comparator pair, not a schema rename. |
| Primary promotion criterion | At least one genuinely reduced rank per required fixture passes finite checks, row/column residual thresholds, dense-reference max/RMS thresholds, and schema validation while recording memory/runtime proxy fields. |
| Promotion veto | Nonfinite output; invalid shapes; missing `kernel_factors`; invalid row/column residuals; missing dense-reference error; source-route overclaim; reduced-rank result only works at full rank; non-TensorFlow default route; memory/runtime proxy promoted before validity. |
| Continuation veto | Missing or inconsistent Phase 1 baseline; schema validation cannot be repaired narrowly; source anchors contradict the planned route; implementation requires unapproved package/network/GPU/external execution; reduced-rank route cannot be represented as a valid transport object. |
| Repair trigger | Failure localized to rank grid, landmark rule, transpose/orientation, normalization, epsilon map, Cholesky jitter, dtype, or batch shape. |
| Explanatory diagnostics | Rank, landmark indices/rule, factor shapes, condition/jitter, row/column residuals, dense-reference max/RMS errors, runtime, memory proxy, iteration count, LEDH-specific fixture geometry summary. |
| Not concluded | No speedup, no production/default readiness, no posterior correctness, no HMC readiness, no public API readiness, and no statistically supported ranking. |
| Artifact preserving result | Implementation diff, focused tests, diagnostic script, JSON/Markdown/log artifacts, Phase 11 result, ledger update, stop handoff update. |

## Diagnostic Role Ledger

| Diagnostic | Role |
| --- | --- |
| finite transported particles | hard veto |
| finite factors/scalings | hard veto |
| output shape | hard veto |
| Phase 3 schema validation | hard veto |
| row marginal residual | hard veto |
| column marginal residual | hard veto |
| dense-reference max/RMS transported-particle error | promotion criterion for reduced-rank viability |
| at least one passing reduced rank per fixture | promotion criterion |
| full-rank replay | repair trigger and regression guard |
| rank, landmark rule, condition/jitter | explanatory and repair trigger |
| runtime and memory proxy | explanatory only until validity gates pass |
| downstream filtering metrics | out of scope for Agent A unless a reviewed amendment adds them |

## Predeclared Thresholds

Hard validity thresholds for every rank/fixture record:

- finite outputs, factors, scalings, residuals, and dense-reference errors;
- transported particle shape matches the baseline fixture output shape;
- row marginal residual `<= 5e-2`;
- column marginal residual `<= 5e-2`;
- candidate result validates under `scalable_ot_candidate_result_schema.py`;
- every fixture/rank record, including `high_dim_locality`, emits
  dense-reference max and RMS transported-particle error fields.  These fields
  may be explanatory for selected fixtures, but they must not be omitted.

Reduced-rank promotion thresholds:

- For `tiny_manual`, `small_parity`, and `high_dim_low_rank`, at least one
  non-full rank must have max dense-reference particle error `<= 7.5e-2` and
  RMS dense-reference particle error `<= 3e-2`.
- For `ledh_specific_smoke`, at least one non-full rank must satisfy the same
  thresholds unless the result explicitly records a repair-trigger rationale.
- For `high_dim_locality`, dense-reference error is explanatory because Phase 8
  already found locality issues on Phase 1 fixtures.
- The `ledh_specific_smoke` fixture construction must be pinned in the
  diagnostic script and summarized in the result artifact so reruns compare the
  same deterministic geometry.

These are viability gates for continuing Nystrom work only.  Passing them does
not establish scalability or production readiness.

## Required Commands

Use the project Python environment already used by prior artifacts when
available.  CPU-only runs must hide GPU devices before TensorFlow import.

Minimum checks:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py docs/benchmarks/scalable_ot_p11_reduced_rank_nystrom_ladder_diagnostics.py tests/test_nystrom_transport_tf.py
pytest -q tests/test_nystrom_transport_tf.py
python docs/benchmarks/scalable_ot_p11_reduced_rank_nystrom_ladder_diagnostics.py --device-scope cpu --output docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.json --markdown-output docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.md
```

If diagnostics are long, first run a `/tmp` smoke with the smallest rank/fixture
subset and record it in the result.

## Result Note Requirements

Write
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-reduced-rank-nystrom-ladder-result-2026-06-18.md`
with:

- status;
- evidence contract result;
- run manifest with git commit, command, environment, CPU/GPU status, seeds or
  deterministic fixture note, wall time, and artifact paths;
- decision table;
- inference-status table;
- fixture/rank result table;
- hard vetoes;
- viable reduced ranks;
- descriptive-only runtime/memory notes;
- source-route classification;
- post-run red-team note;
- exact handoff for Agent B review.

Allowed result statuses:

- `PHASE_11_REDUCED_RANK_NYSTROM_LADDER_PASSED_DIAGNOSTIC_ONLY`
- `PHASE_11_REDUCED_RANK_NYSTROM_LADDER_COMPLETED_CANDIDATE_NOT_PROMOTED`
- `PHASE_11_REDUCED_RANK_NYSTROM_LADDER_BLOCKED`

Do not use a status that says default-ready, production-ready, speedup-proven,
or best algorithm.

## Skeptical Plan Audit

- Wrong baseline risk: use Phase 1 local TensorFlow dense outputs, not a generic
  external Sinkhorn solver.
- Proxy metric risk: runtime and memory are explanatory until validity gates
  pass; they cannot promote a candidate by themselves.
- Missing stop conditions: stop for missing baseline, schema failure,
  source-anchor contradiction, unapproved package/network/GPU need, or invalid
  transport object.
- Unfair comparison risk: compare Nystrom ranks to the Phase 1 baseline only;
  do not rank against semantic-replacement lanes.
- Hidden assumptions: record epsilon, scaling, row/column orientation, target
  weights, rank grid, landmark rule, dtype, and jitter.
- Stale context risk: reload the reboot memo and Phase 10 result before coding.
- Artifact adequacy: a runtime-only benchmark or smoke-only artifact does not
  answer the stated question.

This plan passes the pre-execution audit only if all above risks are handled in
the result artifact before interpreting diagnostics.

## Stop And Handoff Conditions

Stop and write a blocker if:

- Phase 1 artifacts are missing or inconsistent;
- TensorFlow import or CPU-only execution fails in a way that prevents even
  `/tmp` smoke diagnostics;
- schema validation cannot represent the candidate record;
- the reduced-rank route requires unapproved external code;
- source anchors contradict the operation being implemented;
- Agent B reports a material independent-test finding that invalidates the
  harness and cannot be narrowly repaired.

On completion, hand off to Agent B with:

- implementation diff summary;
- exact commands run;
- JSON/Markdown diagnostic paths;
- result path;
- hard veto list;
- viable rank list;
- unresolved uncertainties and non-claims.
