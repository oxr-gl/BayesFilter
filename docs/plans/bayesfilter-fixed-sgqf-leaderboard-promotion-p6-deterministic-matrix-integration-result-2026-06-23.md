# Phase Result: Fixed-SGQF Leaderboard Promotion P6 Deterministic Matrix Integration

metadata_date: 2026-06-23
plan_reference: `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p6-deterministic-matrix-integration-subplan-2026-06-23.md`
master_program: `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md`
status: PASS_P6_FIXED_SGQF_MATRIX_INTEGRATION_COMPLETE

## Phase Objective

Propagate the refreshed SGQF family ledger into the machine-readable
deterministic benchmark-governance artifacts so that admitted, blocked,
diagnostic-only, and scope-qualified SGQF cells are represented with no silent
holes.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | answered for the current machine-readable deterministic stack: the SGQF deterministic coverage and preflight cells now reflect the refreshed family ledger with no silent SGQF hole, and the KSC tiny-scope analytical-score qualifier is preserved |
| Primary criterion status | satisfied after roster-level amendment and rerun |
| Veto diagnostic status | no widened KSC scope was introduced; blocked families remain explicit; the previous silent SGQF hole in preflight was resolved by adding `fixed_sgqf` to the frozen roster and defining its cells consistently |
| Main uncertainty | later runner/numeric artifacts still need to absorb the same SGQF row semantics, especially the tiny-scope KSC score qualifier |
| Next justified action | execute P7 preflight-and-smoke refresh and then continue downstream with the same SGQF scope boundaries |
| What is not concluded | no numeric benchmark run yet, no broader family-score expansion beyond KSC, no actual transformed non-Gaussian SV claim |

## Focused Work Completed

### Deterministic coverage artifact
Updated:
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json`

The `fixed_sgqf` KSC surrogate cell now carries:
- `cell_status: READY_SURROGATE_VALUE_GRADIENT`
- `value_status_when_run: VALID`
- `gradient_status_when_run: VALID`
- `reason_codes: ["NONE"]`
- evidence tests referencing the SGQF wrapper-score FD test and the updated
  same-target surrogate evidence test.

Also updated:
- `adapter_paths` for `fixed_sgqf` now include
  `bayesfilter.highdim.sv_mixture_cut4.independent_panel_sv_mixture_fixed_sgqf_score`
- `nonclaims` now say analytical-score admission is only for the declared tiny
  same-target surrogate fixture.
- stale evidence-test nodeids using old value-only SGQF naming were refreshed.

### Deterministic smoke payload artifact
Updated:
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-smoke-payloads-2026-06-10.json`

The fixed-SGQF KSC smoke payload now carries:
- `gradient_status: VALID`
- representative diagnostic gradient coordinates
- `reason_codes: ["NONE"]`
- `diagnostics.wrapper_score_contract = "analytic_component_score_logsumexp_aggregation"`
- nonclaims updated so the row is no longer described as lacking analytical
  outer score certification.

### Preflight matrix artifact
Updated:
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-preflight-matrix-2026-06-10.json`

Resolved blocker:
- added `fixed_sgqf` to `frozen_roster.algorithm_ids`
- increased `expected_cell_count` accordingly
- added `fixed_sgqf` preflight cells for every required row
- added `fixed_sgqf` value-status and gradient-status matrix entries
- ensured the KSC surrogate row uses:
  - `source_status: READY_SURROGATE_VALUE_GRADIENT`
  - `raw_gradient_status: VALID`
  - `normalized_gradient_status: valid_analytic_gradient`
  - `p8_gradient_error_policy: numeric_error_against_declared_surrogate_reference`
  - `scope_qualifier: tiny_same_target_surrogate_fixture_only`
  - `cell_kind: smoke_fixture_available`
  - a smoke-payload stub that preserves the same tiny-scope qualifier
- left non-KSC SGQF rows blocked/adapter-required exactly as in the deterministic
  coverage ledger

## Focused Checks Run

### Deterministic coverage + semantics checks
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py
```
Observed after deterministic coverage refresh:
- `10 passed`

### Preflight + deterministic + semantics checks after roster amendment
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_filtering_value_gradient_benchmark_preflight_matrix.py tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py
```
Observed after preflight roster integration:
- `15 passed`

## Run Manifest

| Field | Value |
| --- | --- |
| git commit | `N/A` |
| command actually run | `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_filtering_value_gradient_benchmark_preflight_matrix.py tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py` |
| environment / conda env | `tf-gpu` |
| CPU/GPU status | `CPU-only; no GPU work performed` |
| seed(s) | `N/A` |
| wall time | `N/A` |
| output artifact paths | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p6-deterministic-matrix-integration-result-2026-06-23.md` |
| plan file | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p6-deterministic-matrix-integration-subplan-2026-06-23.md` |
| result file | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p6-deterministic-matrix-integration-result-2026-06-23.md` |

## Machine-Readable Delta Summary

### What changed successfully
1. `fixed_sgqf` is now part of the deterministic coverage stack and the preflight
   frozen roster, rather than disappearing between P6 layers.
2. The KSC surrogate row now reflects the P5 family ledger in both deterministic
   coverage and preflight semantics.
3. The KSC score scope remains tiny-fixture/surrogate-only rather than being
   widened silently.

### What remained unchanged intentionally
1. non-KSC fixed-SGQF rows remain adapter-required or blocked.
2. no broader literature-backed SGQF family besides KSC gained score admission.
3. no numeric runner / P8 benchmark artifact was updated in P6.

## Engineering Observations

- The earlier blocker was real, but user direction to amend the frozen roster was
  sufficient to resolve it inside P6.
- The benchmark-governance stack is highly layered; deterministic coverage alone
  is not enough unless preflight carries the same algorithm roster and row
  semantics.
- The `fixed_sgqf` KSC row now aligns across:
  - family ledger,
  - deterministic coverage,
  - smoke payload,
  - preflight cell,
  - value matrix,
  - gradient matrix.

## Nonclaims

- P6 does not update numeric runner / P8 benchmark execution artifacts.
- P6 does not widen the KSC analytical-score admission beyond the declared tiny
  same-target surrogate fixture.
- P6 does not admit broader family-score expansion beyond KSC.

## Post-Run Red-Team Note

- Strongest alternative explanation:
  - The machine-readable stack may now be internally consistent while still
    needing a later careful pass on numeric-runner artifacts to ensure the same
    SGQF scope qualifier survives through emitted benchmark tables.
- What result would overturn the current P6 conclusion:
  - A later governance test showing the updated fixed-SGQF preflight cells are
    inconsistent with the gradient-semantics artifact or with downstream runner
    matrices.
- Weakest part of the evidence:
  - P6 resolves consistency of structure and semantics, not benchmark numeric
    evidence itself.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| pass P6 and complete deterministic machine-readable SGQF integration | satisfied | no silent SGQF hole remains in deterministic coverage/preflight; no widened KSC scope | whether later preflight/smoke and runner artifacts preserve the same scope qualifier without erosion | execute P7 preflight-and-smoke refresh, then continue to later runner-matrix phases | no numeric benchmark execution or broad family score expansion |

## Exact Next-Phase Handoff

P7 may begin only after:
- the P7 preflight-and-smoke subplan exists and preserves the P6 KSC tiny-scope
  qualifier;
- the visible execution ledger and stop handoff are updated for the P6 pass;
- the bounded P6 review packet is issued on the exact files named in the review
  ledger;
- any review findings are patched visibly and the focused P6 checks rerun;
- no numeric-runner widening is inferred from P6 alone.

## Stop-Condition Outcome

The earlier P6 blocker was resolved under explicit user direction to amend the
frozen roster. No remaining P6 stop condition triggered after the roster-level
integration and test reruns.
