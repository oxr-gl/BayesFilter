# Phase 2 result: actual-SV SGQF strict analytical score

Date: 2026-06-30

Status: `PASSED`

Subplan: `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-subplan-2026-06-30.md`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Admit the direct exact-transformed actual-SV fixed-SGQF row as `executed_value_score`. |
| Primary criterion status | Passed: score is emitted by a manual forward-sensitivity recurrence with derivation/provenance mapping. |
| Veto diagnostic status | Passed: no `GradientTape`/`.gradient`/`tape.watch` in the admitted score body; finite value and score; same target and coordinate recorded. |
| Main uncertainty | The score differentiates the fixed-SGQF approximate value recursion, not an exact nonlinear likelihood oracle. |
| Next justified action | Advance to Phase 3 after Claude review convergence. |
| Not concluded | No HMC posterior correctness, no exact likelihood proof, no GPU/XLA performance, no Zhao-Cui TT source-faithfulness claim. |

## What Changed

- Replaced the direct actual-SV fixed-SGQF score wrapper in `bayesfilter/highdim/sv_mixture_cut4.py` with a manual forward-sensitivity recurrence.
- Updated the focused P43 test to require `manual_forward_sensitivity_direct_likelihood_reweighting` provenance and to keep centered finite-difference consistency.
- Updated `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py` so the actual-SV fixed-SGQF row emits value+score only through the manual recurrence.
- Regenerated:
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`
- Wrote derivation/provenance artifact:
  - `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-derivation-2026-06-30.md`

## Numerical Result

For row `zhao_cui_sv_actual_nongaussian_T1000`, algorithm `fixed_sgqf`:

| Metric | Value |
| --- | ---: |
| status | `executed_value_score` |
| log likelihood | -2300.9108495009923 |
| average log likelihood | -2.3009108495009922 |
| score | `[25.92680758701344, 29.605825646547327]` |
| score L2 norm | 39.35358006417938 |
| score coordinate system | `theta=[probit_gamma, log_beta] per coordinate` |
| score provenance | `fixed_sgqf_exact_transformed_sv_manual_forward_sensitivity_analytical_recurrence` |

## Local Checks

All checks below were run CPU-only with `CUDA_VISIBLE_DEVICES=-1` where TensorFlow was imported. TensorFlow emitted CUDA factory/cuInit startup warnings during leaderboard regeneration despite CPU masking; these are recorded as non-authoritative framework/sandbox noise for this CPU-only artifact.

| Check | Result |
| --- | --- |
| `CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/highdim/sv_mixture_cut4.py docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py` | Passed |
| `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py -k lane_a_fixed_sgqf_wrapper_score_matches_centered_finite_difference -q` | Passed: 3 passed, 36 deselected |
| route body scan for `GradientTape`, `.gradient(`, `tape.watch` | Passed |
| JSON assertion for actual-SV fixed-SGQF `executed_value_score` row and finite 2-vector score | Passed |
| `git diff --check -- bayesfilter/highdim/sv_mixture_cut4.py tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md` | Passed |

## Evidence Contract Close

The Phase 2 evidence contract asked whether the direct exact-transformed actual-SV SGQF row can emit a strict analytical score.

Result: yes, for the fixed-SGQF approximate value target, by manual forward sensitivity. FD is treated as a necessary diagnostic only; the non-proxy anchor is the derivation/provenance mapping in `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-derivation-2026-06-30.md` plus the no-tape route scan.

## Claude Review

Claude read-only bounded review of this result returned `VERDICT: AGREE`.

Review caveat: Claude reviewed exactly this result path and did not inspect the cited subplan or derivation artifact.

## Next-Phase Handoff

Phase 3 may start. Phase 3 target remains:

- `docs/plans/bayesfilter-leaderboard-repair-phase3-zhaocui-lgssm-adapter-subplan-2026-06-30.md`
- objective: repair or precisely close the Zhao-Cui LGSSM m3 evaluator adapter blocker.
