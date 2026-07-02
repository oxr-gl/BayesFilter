# Phase 1 result: actual-SV SGQF same-target value row

Date: 2026-06-30

Status: `PASSED`

## Objective

Replace the stale actual-SV SGQF `blocked_not_same_target` leaderboard cell with a finite same-target direct exact-transformed SGQF value-only row.

## Skeptical Audit

Risks checked before execution:

- wrong baseline: this phase used the corrected exact-transformed actual-SV target note `docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md`, not the older augmented-noise Gaussian-closure lane;
- proxy metric: finite value was used only to admit a value-only row, not a gradient or production claim;
- stale context: old `blocked_not_same_target` labels were explicitly searched after regeneration;
- environment mismatch: TensorFlow runs were CPU-only with `CUDA_VISIBLE_DEVICES=-1` before import;
- unsupported claim: no SGQF actual-SV analytical score was emitted.

## Edits

Updated `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`:

- added `_actual_sv_direct_sgqf_value()`;
- used `highdim.exact_transformed_sv_independent_panel_fixed_sgqf_filter` for `zhao_cui_sv_actual_nongaussian_T1000/fixed_sgqf`;
- marked the cell `executed_value_only`;
- set `target_contract_status` to `target_compatible_direct_exact_transformed_sv_sgqf_value`;
- set score status to `blocked_strict_analytical_score_adapter`;
- added nonclaims:
  - not KSC Gaussian mixture approximation;
  - not augmented-noise Gaussian-closure route;
  - no analytical score claim;
  - not production GPU timing;
- fixed relative output path handling for Markdown generation.

## Checks Run

| Check | Result |
| --- | --- |
| `python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py` | `PASSED` |
| CPU-only direct value probe with `CUDA_VISIBLE_DEVICES=-1` | `PASSED` |
| CPU-only highdim leaderboard regeneration with `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp` | `PASSED` |
| JSON assertion for actual-SV SGQF value-only cell | `PASSED` |
| Stale `blocked_not_same_target` search in current emitter/artifacts | `PASSED` |
| Trailing whitespace check on edited/generated artifacts | `PASSED` |
| `git diff --check` on edited/generated tracked artifacts | `PASSED` |

TensorFlow emitted CUDA plugin registration and `cuInit` messages despite `CUDA_VISIBLE_DEVICES=-1`; per repo GPU policy, this CPU-only run intentionally hid GPUs and these messages are not trusted GPU diagnostics.

## Result Cell

| Field | Value |
| --- | --- |
| Row | `zhao_cui_sv_actual_nongaussian_T1000` |
| Algorithm | `fixed_sgqf` |
| Comparison status | `executed_value_only` |
| Numeric execution status | `executed_direct_exact_transformed_sv_sgqf_value` |
| Target contract status | `target_compatible_direct_exact_transformed_sv_sgqf_value` |
| Log likelihood | `-2300.9108495009923` |
| Avg log likelihood | `-2.3009108495009922` |
| Score status | `blocked_strict_analytical_score_adapter` |
| Score vector | `None` |
| Score provenance | `None` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Admit direct actual-SV SGQF as value-only | Passed | No stale target or score-claim veto active | Strict analytical score remains unwired | Phase 2 analytical-score implementation/defer decision | No SGQF actual-SV analytical gradient, no GPU timing, no production readiness |

## Artifacts

- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`

## Phase 2 Handoff

Phase 2 may proceed under `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-subplan-2026-06-30.md`.

Boundary to preserve:

- The direct actual-SV SGQF row remains value-only unless Phase 2 implements strict analytical derivatives.
- The current `exact_transformed_sv_independent_panel_fixed_sgqf_score` wrapper uses `GradientTape` and is not admissible as an analytical leaderboard score.
