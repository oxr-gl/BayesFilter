# P50-M5 SV And Generalized SV Ladder Result

metadata_date: 2026-06-09
phase: P50-M5
status: PASS_P50_M5_SV_GENERALIZED_SV_LADDER

## Decision Table

| Field | Decision |
| --- | --- |
| Gate decision | Pass M5 with scoped evidence: strict dim 1/2/3 same-target value-gradient passes are established for KSC CUT4/Kalman and exact transformed SV Zhao-Cui/dense rows; KSC Zhao-Cui/dense remains diagnostic because existing tests use looser fit-tolerance gates; native generalized SV same-target equality is blocked rather than overclaimed. |
| Primary criterion status | Passed in the subplan sense: SV dim 1/2/3 tests pass for the strict rows, diagnostic KSC Zhao-Cui/dense evidence is classified without promotion, and generalized SV has a documented model-specific native-reference blocker with diagnostic probes only. |
| Veto diagnostic status | Passed: KSC Gaussian mixture is not treated as exact native SV; CUT4 value agreement is not promoted without gradient tests; native generalized SV cross-term and residual transformation are not ignored or claimed exact. |
| Main uncertainty | The Zhao-Cui rows are factorized scalar fixed-design substitute rows on tiny fixtures, not coupled multivariate adaptive TT/SIRT or paper-scale evidence.  Native generalized SV still lacks an approved same-target value/gradient reference. |
| Next justified action | Advance to M6 spatial SIR and predator-prey ladder under the M4 calibration rules. |
| Not concluded | No HMC readiness, no production SV/generalized SV readiness, no smoothing support, no source-faithful adaptive TT/SIRT filtering, and no S&P 500 reproduction. |

## Artifacts

- `docs/plans/bayesfilter-highdim-zhao-cui-p50-m5-sv-generalized-sv-ladder-manifest-2026-06-09.json`
- `tests/highdim/test_p50_sv_generalized_sv_ladder.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/highdim/test_p47_generalized_sv_equality.py`
- `tests/highdim/test_p44_generalized_sv_target.py`
- `tests/highdim/test_p45_generalized_sv_comparison_blocker.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-m5-sv-generalized-sv-ladder-result-2026-06-09.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-visible-execution-ledger-2026-06-09.md`

## Supported Rows

| Row | Dimensions | Candidate | Reference | M4 class |
| --- | --- | --- | --- | --- |
| KSC SV CUT4 vs Kalman | 1, 2, 3 | CUT4 mixture filter | Kalman enumeration over KSC components | `PASS_SAME_TARGET_VALUE_AND_GRADIENT` |
| Exact transformed SV Zhao-Cui vs dense | 1, 2, 3 | factorized scalar fixed-design Zhao-Cui TT substitute | dense exact transformed SV reference | `PASS_SAME_TARGET_VALUE_AND_GRADIENT` |

## Diagnostic Rows

| Row | Dimensions | Candidate | Reference | M4 class |
| --- | --- | --- | --- | --- |
| KSC SV Zhao-Cui vs dense | 1, 2, 3 | factorized scalar fixed-design Zhao-Cui TT substitute | dense scalar mixture reference summed by coordinate | `PASS_GRADIENT_LOCAL_DIAGNOSTIC` |

The KSC Zhao-Cui/dense tests remain useful same-target local diagnostics, but
their existing gates are fit-tolerance-scale checks looser than the default
P50-M4 promoted same-target thresholds.  M5 therefore does not promote that row
to `PASS_SAME_TARGET_VALUE_AND_GRADIENT`.

## Scoped Blocker

Native generalized SV same-target value/gradient equality remains blocked:

- target: `y_t = beta s_t + exp(h_t/2) epsilon_t`, state `(s_t, h_t)`;
- blocker: no approved exact/dense or reviewed same-target reference for the
  native generalized SV value and gradient equality row;
- diagnostic-only paths: transformed-residual CUT4 probes and moment-matched
  Kalman approximations.

This blocker is not a phase stop because the M5 primary criterion allowed a
documented model-specific blocker.  It remains a claim boundary for any future
native generalized SV equality or HMC claim.

## Local Validation

Commands run CPU-only:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py tests/highdim/test_p47_generalized_sv_equality.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p50_sv_generalized_sv_ladder.py tests/highdim/test_p44_generalized_sv_target.py tests/highdim/test_p45_generalized_sv_comparison_blocker.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p50_sv_generalized_sv_ladder.py
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p50-m5-sv-generalized-sv-ladder-manifest-2026-06-09.json tests/highdim/test_p50_sv_generalized_sv_ladder.py docs/plans/bayesfilter-highdim-zhao-cui-p50-m5-sv-generalized-sv-ladder-result-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p50-visible-execution-ledger-2026-06-09.md
```

Observed results:

- SV value/gradient suite: `23 passed, 2 TensorFlow Probability deprecation
  warnings`;
- manifest and generalized-SV blocker suite: `11 passed, 2 TensorFlow
  Probability deprecation warnings`;
- post-repair combined M5 suite:
  `35 passed, 2 TensorFlow Probability deprecation warnings`;
- compileall passed with no output;
- `git diff --check` passed.

## Claude Review Repair

Claude returned `VERDICT: REVISE` on the first M5 review because the original
manifest overpromoted the KSC Zhao-Cui/dense row as a strict M4 promoted
same-target pass even though its existing tests use fit-tolerance-scale gates
looser than the P50-M4 default promoted thresholds.

Repairs:

- kept strict promoted rows for KSC CUT4/Kalman and exact transformed SV
  Zhao-Cui/dense;
- reclassified KSC Zhao-Cui/dense as `PASS_GRADIENT_LOCAL_DIAGNOSTIC`;
- added a manifest test that enforces the diagnostic boundary;
- reran the combined M5 suite.

Claude then returned `VERDICT: AGREE`.

## Non-Claims

M5 does not claim:

- exact native SV evidence for KSC Gaussian-mixture rows;
- strict M4 promotion for the KSC Zhao-Cui/dense row;
- native generalized SV same-target equality;
- coupled multivariate Zhao-Cui TT;
- adaptive MATLAB TT-cross/SIRT reproduction;
- HMC readiness;
- production SV or generalized SV readiness;
- smoothing support.
