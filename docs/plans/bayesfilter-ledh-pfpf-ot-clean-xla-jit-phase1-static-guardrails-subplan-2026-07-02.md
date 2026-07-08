# Phase 1 Subplan: Static Guardrails

Date: 2026-07-02

Status: `DRAFT_FOR_CLAUDE_REVIEW`

## Phase Objective

Add a static audit and focused tests that mechanically detect unclean
compiled-path patterns before later phases claim the LEDH-PFPF-OT corrected
full route is clean for GPU/XLA.

The audit is allowed, and expected, to report the current route as unclean.
Phase 1 passes when the audit can reliably detect and report the known Phase 0
surfaces with line-anchored findings and when tests prove the guardrail itself
works.

## Entry Conditions Inherited From Previous Phase

- Phase 0 inventory result exists and names concrete file/line surfaces.
- Clean-XLA target is frozen: TensorFlow loop state, not Python-unrolled
  compiled-path scans, is required for score-bearing dynamic recursions.
- Existing local static checks passed under CPU-hidden source-check mode:
  `3 passed in 4.15s`.
- No implementation route is fixed yet.

## Required Artifacts

- Static audit script:
  `scripts/audit_ledh_clean_xla.py`
- Static audit tests:
  `tests/test_audit_ledh_clean_xla.py`
- Phase 1 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-guardrails-result-2026-07-02.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-visible-execution-ledger-2026-07-02.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-claude-review-ledger-2026-07-02.md`
- Draft Phase 2 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase2-fixed-randomness-tensorization-subplan-2026-07-02.md`

## Required Checks, Tests, Reviews

Before implementation:

- Codex skeptical audit of this subplan.
- Claude read-only review of this subplan using a bounded prompt. If fixed-path
  file reading hangs while a small health probe works, switch to an embedded
  mini-packet or exact line-range packet and record that prompt repair.

After implementation:

- `CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_clean_xla.py --format json`
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py`
- Re-run the existing nearby checks:
  `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py::test_streaming_module_source_is_gpu_oriented tests/test_contract_e_phase3_gradient_route_audit.py::test_phase3_r12_gpu_manual_score_route_is_explicit_reverse_scan tests/test_contract_e_phase3_gradient_route_audit.py::test_phase3_r14_manual_dense_sinkhorn_recursions_use_tf_while_loop`
- Claude read-only review of the Phase 1 execution result before Phase 2
  execution.

These are CPU-hidden source/static checks. They are not GPU/XLA runtime
evidence.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we add a guardrail that detects the known unclean compiled-path patterns before refactoring begins? |
| Baseline/comparator | Phase 0 inventory and current source tree. |
| Primary pass criterion | Audit reports the current route as `FAIL_CURRENT_ROUTE` or equivalent with line-anchored findings covering every required current-veto Phase 0 pattern class; warning-only rows are reported separately; tests pass and include synthetic positive/negative cases. |
| Veto diagnostics | Audit misses a required current-veto Phase 0 pattern class; audit treats stopped partial derivatives as scores; tests make current unclean code look clean; audit relies only on broad file-level grep without symbol/range awareness; unrelated implementation edits are made; or Claude review returns unresolved `VERDICT: REVISE`. |
| Explanatory diagnostics | Counts by pattern class, line anchors, symbol names, and whether each finding is a current veto, warning, or future clean-route requirement. |
| Not concluded | No code is fixed; no compile-time improvement is claimed; no HLO evidence; no numerical correctness; no HMC readiness. |
| Artifact | Phase 1 result markdown plus audit JSON emitted by the command. |

## Implementation Details

Implement `scripts/audit_ledh_clean_xla.py` as a small, repository-local static
audit. Prefer Python `ast` symbol spans plus targeted substring checks over a
global grep. The script should:

- locate top-level function spans in:
  - `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`;
  - `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`;
- scan `_sir_transition_mean_with_aux_tf` for Python `for` over `range`, Python
  list initialization, and `.append`;
- scan `_sir_transition_mean_vjp_tf` for `reversed(aux)`;
- scan `_manual_value_and_score_from_components` for:
  - `int(observations.shape[0])`;
  - `records = []`;
  - `for time_index in range(time_steps)`;
  - `noise_rows = []`;
  - seed loop over `args.batch_seeds`;
  - `noise_rows.append`;
  - `records.append`;
  - `reversed(records)`;
- scan streaming finite Sinkhorn helper symbols for:
  - `tf.stop_gradient(x)` in stopped-key score-bearing helpers;
  - `for _ in range(steps)`;
  - `states = []` and `states.append`;
  - local `tf.GradientTape` and `tape.gradient` in total custom-gradient helpers.

### Closed Required Pattern Checklist

The audit must use this closed checklist for Phase 1. Adding broader checks is
allowed only as warnings; Phase 1 pass/fail coverage is judged against this
table.

| ID | File | Symbol | Required pattern or AST shape | Severity | Absence after implementation means |
| --- | --- | --- | --- | --- | --- |
| `SIR-RK4-FWD-LIST` | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py` | `_sir_transition_mean_with_aux_tf` | `aux = []` and `aux.append(...)` | current veto | clean or renamed; if renamed, update checklist before claiming coverage |
| `SIR-RK4-FWD-RANGE` | same | `_sir_transition_mean_with_aux_tf` | Python `for` whose iterator is `range(int(substeps))` or equivalent source text `for _ in range(int(substeps))` | current veto | clean or renamed |
| `SIR-RK4-REV-REVERSED` | same | `_sir_transition_mean_vjp_tf` | `reversed(aux)` | current veto | clean or renamed |
| `SIR-MANUAL-TIME-STATIC` | same | `_manual_value_and_score_from_components` | `int(observations.shape[0])` | current veto | clean or renamed |
| `SIR-MANUAL-RECORD-LIST` | same | `_manual_value_and_score_from_components` | `records = []` and `records.append(...)` | current veto | clean or renamed |
| `SIR-MANUAL-FWD-RANGE` | same | `_manual_value_and_score_from_components` | Python `for` over `range(time_steps)` | current veto | clean or renamed |
| `SIR-MANUAL-SEED-LOOP` | same | `_manual_value_and_score_from_components` | `noise_rows = []`, loop over `args.batch_seeds`, and `noise_rows.append(...)` | current veto | clean or renamed |
| `SIR-MANUAL-REV-REVERSED` | same | `_manual_value_and_score_from_components` | `reversed(records)` | current veto | clean or renamed |
| `SINK-STOPPED-VALUE-KEY` | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py` | `_filterflow_streaming_finite_sinkhorn_potentials_stopped_scale_keys` | `tf.stop_gradient(x)` | current veto for score-bearing route | clean, not score-bearing, or explicitly excluded with reason |
| `SINK-STOPPED-VALUE-RANGE` | same | `_filterflow_streaming_finite_sinkhorn_potentials_stopped_scale_keys` | Python `for` over `range(steps)` | current veto | clean or explicitly excluded with reason |
| `SINK-TOTAL-VALUE-RANGE` | same | `_filterflow_streaming_finite_sinkhorn_potentials_total_vjp` | Python `for` over `range(steps)` | current veto | clean or explicitly excluded with reason |
| `SINK-STOPPED-VJP-KEY` | same | `_filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys` | `tf.stop_gradient(x)` | current veto for score-bearing route | clean, not score-bearing, or explicitly excluded with reason |
| `SINK-STOPPED-VJP-STATES` | same | `_filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys` | `states = []`, `states.append(...)`, and Python `for` over `range(steps)` | current veto | clean or explicitly excluded with reason |
| `SINK-TOTAL-CUSTOM-TAPE` | same | `_filterflow_manual_streaming_finite_transport_total_vjp` | local `tf.GradientTape` and `tape.gradient(...)` inside the helper | current warning | if absent, classify as clean or moved; not a Phase 1 veto by itself |

For rows marked `current veto`, the exact symbol name must be resolved by AST.
If a current-veto symbol is missing, the audit must fail with `MISSING_SYMBOL`
rather than silently scanning the whole file. For warning-only rows such as
`SINK-TOTAL-CUSTOM-TAPE`, a missing symbol should be reported as
`MISSING_WARNING_SYMBOL` and should not by itself fail Phase 1; if later phases
promote that helper to a hard clean-XLA gate, they must first update this
checklist.

### Line Anchoring

The audit must derive line numbers from `ast` node locations when possible:

- top-level `FunctionDef` spans come from `node.lineno` and `node.end_lineno`;
- assignment, loop, call, and decorator findings use the matched AST node's
  `lineno`;
- substring fallback is allowed only inside a resolved function span and must
  report the actual file line number by adding the span start offset to the
  local line offset;
- no Phase 1 required finding may be reported as file-level-only.

The audit should emit JSON with:

- `decision`;
- `required_pattern_results`;
- `findings`;
- `missing_required_patterns`;
- `warning_findings`;
- `summary_by_file`;
- `nonclaims`.

Expected current decision after Phase 1 implementation:

`FAIL_CURRENT_ROUTE`

That expected decision is not a failing test. The tests should assert the audit
finds the current unclean surfaces and reports them plainly.

## Forbidden Claims And Actions

- Do not claim clean XLA after Phase 1.
- Do not edit the implementation route except to add the audit script and
  tests.
- Do not run GPU jobs in Phase 1.
- Do not hide stopped partial derivative findings behind soft wording.
- Do not make `GradientTape` findings disappear by whitelisting the whole file.
- Do not change numerical pass criteria, score definitions, or project default
  GPU policy.

## Exact Next-Phase Handoff Conditions

Phase 1 may hand off to Phase 2 only if:

- the audit command runs and emits line-anchored JSON;
- tests pass;
- the result file records that current source is still unclean and names the
  required Phase 2 repair scope;
- Phase 2 subplan exists and covers fixed randomness tensorization only;
- Claude read-only review of the Phase 1 result and Phase 2 subplan returns
  `VERDICT: AGREE`, or fixable findings are patched and rereviewed.

## Stop Conditions

Stop and write a blocker result if:

- the audit cannot inspect the required files or symbols;
- the required pattern classes cannot be represented without brittle whole-file
  grep;
- tests require package installation or network access;
- the implementation would need broad unrelated refactors;
- Claude and Codex do not converge after five rounds on this subplan or the
  Phase 1 result.

## Skeptical Pre-Execution Audit

Result: `PASS_PENDING_CLAUDE_REVIEW`

- Wrong baseline: avoided by making the current unclean route the expected
  audited object.
- Proxy promotion: avoided because Phase 1 can only prove guardrail coverage,
  not compiler cleanliness.
- Missing stop conditions: explicit above.
- Unfair comparison: no runtime comparison is made.
- Hidden assumption: the plan explicitly treats `FAIL_CURRENT_ROUTE` as the
  expected current audit decision.
- Environment mismatch: CPU-hidden static checks only; GPU evidence is deferred.
- Artifact mismatch: audit JSON and result markdown must preserve all findings
  and nonclaims.
