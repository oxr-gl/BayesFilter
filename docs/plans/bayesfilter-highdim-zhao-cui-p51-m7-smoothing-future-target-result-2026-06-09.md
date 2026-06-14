# P51-M7 Result: Smoothing Future-Target Decision

metadata_date: 2026-06-09
phase: P51-M7
status: PASS_P51_M7_SMOOTHING_FUTURE_TARGET
supervisor: Codex
reviewer: Claude Code read-only

## Decision

P51-M7 keeps smoothing deferred as a future latent-path inference target.  P51
filtering, score API, model-ladder, and HMC Tier 2/Tier 3 tokens are not
smoothing evidence.

Any future smoother must be a separate reviewed program with backward
conditional maps, backward weights, smoothing marginal checks, and a dedicated
smoother pass token.

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Should P51 implement smoothing now or preserve it as a future target? |
| Baseline/comparator | P50-M8 smoothing boundary and P49 `SourceRouteSmoothingBoundary`. |
| Primary criterion | Passed: smoothing remains deferred with explicit future requirements and guard tests. |
| Veto diagnostics | Passed: no P51 filtering or HMC token is smoothing support; deferred smoothing carries no smoother token. |
| Not concluded | No smoothing support, latent-path posterior inference, smoothing marginal accuracy, or smoother production readiness. |

## Validation

Focused validation was run CPU-only with `CUDA_VISIBLE_DEVICES=-1`:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p51_smoothing_future_target.py tests/highdim/test_p50_smoothing_boundary.py tests/highdim/test_p49_source_route_smoothing_boundary.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p51_smoothing_future_target.py
git diff --check -- tests/highdim/test_p51_smoothing_future_target.py docs/plans/bayesfilter-highdim-zhao-cui-p51-m7-smoothing-future-target-manifest-2026-06-09.json docs/plans/bayesfilter-highdim-zhao-cui-p51-m7-smoothing-future-target-result-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p51-visible-execution-ledger-2026-06-09.md
```

Outcomes:

- initial pytest passed: 14 tests passed, with 2 TensorFlow Probability
  deprecation warnings;
- after Claude review repair, pytest passed: 15 tests passed, with 2
  TensorFlow Probability deprecation warnings;
- the shared `SourceRouteSmoothingBoundary` now enforces
  `smoothing_marginal_checks` as a required future-smoother field;
- compileall passed;
- git diff whitespace check passed.

## Nonclaims

- No smoothing support.
- No latent-path posterior inference.
- No backward conditional map implementation.
- No backward weight implementation.
- No smoothing marginal accuracy.
- No smoother production readiness.
- No production HMC readiness.
- No GPU readiness.
- No source-faithful adaptive TT/SIRT filtering.
- No S&P 500 reproduction.
