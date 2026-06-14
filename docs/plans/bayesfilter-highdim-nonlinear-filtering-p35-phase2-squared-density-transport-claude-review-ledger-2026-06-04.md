# P35 Phase 2 Zhao--Cui Highdim Squared Density And Transport Claude Review Ledger

metadata_date: 2026-06-04

phase: Phase 2 squared density and KR transport

review_scope:
- `bayesfilter/highdim/__init__.py`
- `bayesfilter/highdim/squared_tt.py`
- `bayesfilter/highdim/transport.py`
- `tests/highdim/test_squared_tt_density.py`
- `tests/highdim/test_transport.py`
- `tests/highdim/test_failure_exits.py`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-result-2026-06-04.md`

parent_plans:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-subplan-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md`

## Review Rules

Codex is supervisor and final authority.  Claude Code is a bounded hostile
reviewer.  For each finding, Codex classifies:

```text
ACCEPT
PARTIAL
DISPUTE
CLARIFY
```

Accepted or partially accepted findings require patches.  Disputed findings
require concise rebuttals.  If unresolved blockers remain after five
iterations, Phase 2 acceptance is blocked.

## Iteration 1

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-zhao-cui-phase2-impl-review-iter1 \
  --model sonnet \
  --effort high \
  "<prompt>"
```

Claude verdict: `FAIL`.

Codex classification summary:

```text
ACCEPT: 6
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| BLOCKER | `conditional_density()` computed a slice-normalized joint at suffix coordinates fixed to zero, not the required prefix conditional with suffix integration. | ACCEPT | Added deterministic tensor-product trapezoid suffix integration in `_prefix_axis_marginal_values()`; `conditional_density()` now normalizes the suffix-integrated prefix/axis marginal. |
| BLOCKER | `marginal_density()` returned a linearly contracted square-root TT while implying squared-density marginal semantics. | ACCEPT | Marked marginal diagnostics explicitly as `squared_density_marginal_metadata` and documented that the retained object is square-root metadata while squared marginal values are evaluated by grid integration in `conditional_density()`. |
| MAJOR | `KRTransport` accepted arbitrary coordinate order but only natural order was implemented. | ACCEPT | Constructor now rejects non-natural coordinate order with `NotImplementedError`. Added `test_transport_rejects_non_natural_coordinate_order`. |
| MAJOR | Required `NONFINITE_VALUE` vetoes were missing or misclassified. | ACCEPT | Added finite checks for density scalar configuration, input points, normalizers, conditionals, CDF totals/increments, and inverse targets. Added nonfinite failure tests. |
| MAJOR | Branch identity was type-checked but not validated against the actual density payload. | ACCEPT | Added `SquaredTTDensity.expected_manifest()` and `expected_branch_identity()`; constructor now rejects identities that do not match the density manifest. Added branch mismatch test. |
| MAJOR | Result ledger overclaimed failure-exit coverage. | ACCEPT | Updated result ledger and added tests for `CONDITIONAL_DENOMINATOR_FLOOR_EXCEEDED`, `NONFINITE_VALUE`, and `INVALID_BRANCH_MISMATCH`. |

Post-patch local validation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_failure_exits.py
```

Outcome: `16 passed, 2 warnings in 7.81s`.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_failure_exits.py
```

Outcome: `51 passed, 2 warnings in 5.08s`.

No disputed findings remain after iteration 1.

## Iteration 2

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-zhao-cui-phase2-impl-review-iter2 \
  --model sonnet \
  --effort high \
  "<prompt>"
```

Claude verdict: `TOOL_STALLED`.

Codex classification summary:

```text
ACCEPT: 0
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| TOOL | Broad iteration-2 review process remained live and silent past the practical review window. | N/A | Terminated only the stalled Claude process with `pkill -f highdim-zhao-cui-phase2-impl-review-iter2`; reran a narrower iteration-2b review focused on the accepted fixes. |

## Iteration 2b

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-zhao-cui-phase2-impl-review-iter2b \
  --model sonnet \
  --effort high \
  "<narrow prompt>"
```

Claude verdict: `FAIL`.

Codex classification summary:

```text
ACCEPT: 2
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| MAJOR | The result ledger overclaimed suffix-integration verification; the scoped test was one-dimensional and had no suffix coordinates. | ACCEPT | Added `test_conditional_density_integrates_suffix_coordinates`, a coupled two-dimensional TT fixture whose suffix-integrated conditional differs from zero-suffix slice normalization. |
| MAJOR | `NONFINITE_VALUE` coverage was incomplete for inverse input and CDF-path nonfinite handling. | ACCEPT | Added `test_transport_rejects_nonfinite_inputs` inverse branch and `test_transport_cdf_path_reports_nonfinite_status`; patched `_cdf_at()` to classify nonfinite queried `z_value` as `NONFINITE_VALUE`. |

Post-patch local validation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_failure_exits.py
```

Outcome: `18 passed, 2 warnings in 5.40s`.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py tests/highdim/test_failure_exits.py
```

Outcome: `53 passed, 2 warnings in 5.49s`.

No disputed findings remain after iteration 2b.

## Iteration 3

Claude command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-zhao-cui-phase2-impl-review-iter3 \
  --model sonnet \
  --effort high \
  "<prompt>"
```

Claude verdict: `PASS`.

Codex classification summary:

```text
ACCEPT: 0
PARTIAL: 0
DISPUTE: 0
CLARIFY: 0
```

| Severity | Claude finding | Codex classification | Patch or rebuttal |
|---|---|---|---|
| NONE | Claude found no remaining blocker or major issue in the requested Phase 2 closure scope. | N/A | No patch required. |

## Final Status

Final Claude status: `PASS`.

Open blockers: `NONE`.

Final Codex supervisor decision: `ACCEPT_PHASE2`.
