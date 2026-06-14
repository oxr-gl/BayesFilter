# P47-M4 Result: Spatial SIR Filtering And Equality

metadata_date: 2026-06-08
phase: P47-M4
status: `PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | M4a passed local evidence and Claude read-only review as a lower-rung small-`J` additive-Gaussian spatial SIR closure gate with dense reference, CUT4 value diagnostic, and P46/P47 Zhao--Cui fixed-design route. |
| Primary criterion status | `PASS_LOCAL_M4A`: focused M4a tests pass for dense-reference, Zhao--Cui lower-rung value/state moments, CUT4 value diagnostic, and production-token non-emission. |
| Veto diagnostic status | The target manifest separates lower-rung reference/equality from production filtering and keeps native SIR/paper-scale claims as nonclaims. |
| Main uncertainty | M4a is a J=1 closure target, not native non-Gaussian SIR and not paper-scale J=9 filtering. |
| Next justified action | Run local M4a gates, then Claude read-only review for `PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY`. M4b production remains blocked until a separate production/near-paper-scale row is reviewed. |
| Not concluded | No native SIR correctness, no production spatial SIR filtering, no paper-scale J=9 validation, no HMC readiness, no production score API, no adaptive MATLAB TT-cross/SIRT reproduction, and no S&P 500 reproduction. |

## Evidence Contract Outcome

M4a freezes the promoted target as a small-`J` additive-Gaussian spatial SIR
closure.  The dense reference and Zhao--Cui fixed-design route use the same
state law, observation law, domain policy, and observations.  Observed
infectious and unobserved susceptible Zhao--Cui state errors are tested
separately against the dense reference.  CUT4 remains a same-closure value
diagnostic in M4a; its state moments are not promoted.

M4a does not emit `PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING`.

## Skeptical Phase Audit

Status: `PASS_TO_LOCAL_M4A_GATES`.

- Wrong baseline risk: CUT4 is not used as the sole truth; dense quadrature is
  the reference for Zhao--Cui lower-rung filtering, and CUT4 is kept as a
  value-only diagnostic on the same closure.
- Target-mismatch risk: native SIR and additive-Gaussian closure are explicitly
  separated.
- Proxy-metric risk: finite lower-rung output and J=1 agreement do not promote
  production filtering.
- Observed-only risk: observed infectious and unobserved susceptible mean
  errors are reported and tested separately.

## Artifacts

- Target manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-spatial-sir-filtering-target-manifest-2026-06-08.json`
- Focused test:
  `tests/highdim/test_p47_spatial_sir_filtering.py`

## Local Commands

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p47-spatial-sir-filtering-target-manifest-2026-06-08.json
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_spatial_sir_filtering.py
```

Result: 5 passed, 2 TensorFlow Probability deprecation warnings.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_spatial_sir_filtering.py
```

Result: passed.

```bash
git diff --check -- tests/highdim/test_p47_spatial_sir_filtering.py docs/plans/bayesfilter-highdim-zhao-cui-p47-spatial-sir-filtering-target-manifest-2026-06-08.json docs/plans/bayesfilter-highdim-zhao-cui-p47-phase4-spatial-sir-filtering-result-2026-06-08.md docs/plans/bayesfilter-highdim-zhao-cui-p47-phase4-spatial-sir-filtering-claude-review-ledger-2026-06-08.md
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_target_registry.py tests/highdim/test_p47_paper_scale_readiness.py tests/highdim/test_p47_spatial_sir_filtering.py tests/highdim/test_p46_multistate_zhaocui_adapter.py tests/highdim/test_p45_spatial_sir_comparison_blocker.py tests/highdim/test_p44_spatial_sir_diagnostic.py tests/highdim/test_p30_spatial_sir.py
```

Result: 37 passed, 2 TensorFlow Probability deprecation warnings.

## Claude Review

Iteration 1 returned:

```text
PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY
```

Claude accepted only the lower-rung reference/equality token.  The review
confirmed the shared closure target for dense and Zhao--Cui, separate observed
infectious and unobserved susceptible checks, CUT4 value-diagnostic
non-promotion, M1 route-label preservation, and non-emission of the production
token.

## M4b Production Gate Status

Status: `BLOCKED_NO_PRODUCTION_TOKEN`.

After M4a passed, Codex ran a non-promotional feasibility probe to check whether
a larger retained-grid spatial SIR row was plausible under CPU caps:

- J=2, horizon 2, order 3: completed, but this is still below the M2
  near-paper candidate.
- J=3, horizon 2, order 3: first attempt hit `COMPLEXITY_GATE`; one budget
  repair completed, reporting observed and unobserved RMSE, but J=3 is still a
  feasibility probe rather than the near-paper J=9 row named by M2.

Decision: do not emit
`PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING`.  A future M4b attempt needs a
separate reviewed production/near-paper-scale plan preserving the M4a target,
resource caps, observed/unobserved metrics, and stop conditions.
