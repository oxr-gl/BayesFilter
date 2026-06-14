# P57-M3 Result: Proposition-2 Marginalization

metadata_date: 2026-06-11
phase: P57-M3
status: PASS_CLAUDE_REVIEWED

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Implement a source-style paired-core mass-contraction evaluator for normalized squared-TT retained marginals, and stop treating grid integration or metadata-only marginals as the promoted source route. |
| Primary criterion status | PASS for value-level retained marginal pdf evaluation on prefix/suffix retained axes used by the fixed route. `SquaredTTDensity.marginal_density(...).normalized_retained_density_values(...)` now contracts paired TT cores with basis mass matrices for integrated axes and pointwise paired basis/core factors for retained axes. |
| Veto diagnostic status | PASS: tensor-product grid integration is used only as an independent low-dimensional comparator in tests; non-prefix/suffix retained axes are rejected rather than promoted; the result does not claim full KR/CDF map state. |
| Main uncertainty | The author `@TTSIRT/marginalise.m` stores QR recursion state (`ys`, `ms`) used by later KR/CDF construction. M3 implements marginal value contraction and normalizer semantics, but the stored QR map state remains a P57-M4 dependency. |
| Next justified action | Advance to P57-M4 Source KR/CDF Maps. |
| What is not concluded | No full transport map, no conditional KR/CDF implementation, no proposal density correction, no sequential filtering loop, no rank readiness, no HMC readiness, and no spatial SIR success. |

Required token:

`PASS_P57_M3_PROPOSITION2_MARGINALIZATION`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter implement the source squared-TT marginalization needed for retained objects and later KR conditionals? |
| Baseline/comparator | Zhao-Cui Proposition 2 and author `@TTSIRT/marginalise.m`. |
| Primary pass criterion | Source-style mass-matrix contractions produce normalized marginal pdf values and normalizer semantics for retained prefix/suffix cases used by the route, with tests. |
| Veto diagnostics | Grid integration claimed as implementation; metadata-only marginal objects; normalizer mismatch; claim of full QR/KR map state before M4. |
| Artifact | This result file, implementation diff in `bayesfilter/highdim/squared_tt.py`, focused tests, and Claude read-only review. |

## Source Anchors

| Author operation | Anchor | BayesFilter implication |
| --- | --- | --- |
| Directional marginalization order | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:19-23` sets `obj.order` from the integration direction. | M3 supports prefix/suffix retained axes, matching the two directional marginalization cases; non-prefix/suffix retained sets raise `NotImplementedError`. |
| Backward mass recursion | `@TTSIRT/marginalise.m:25-51` pushes right-side dimensions into the current core using mass contractions and QR, then sets `fun_z`. | M3 contracts paired TT cores with one-dimensional mass matrices for integrated axes and returns normalized retained marginal values. |
| Forward mass recursion | `@TTSIRT/marginalise.m:53-82` performs the analogous left-to-right recursion. | M3 handles suffix retained axes by the same paired-core contraction order. |
| Defensive normalizer | `@TTSIRT/marginalise.m:85` sets `obj.z = obj.fun_z + obj.tau`. | `SquaredTTDensity.normalizer()` keeps `sqrt_square_normalizer + tau * defensive_normalizer`; marginal values add the retained defensive density before division by the same normalizer. |

## Implementation Changes

- `SquaredTTMarginal` now carries the source density when available and exposes
  `normalized_retained_density_values(points)`.
- `SquaredTTDensity.marginal_density(keep_axes)` now:
  - validates retained axes are prefix or suffix;
  - records `semantics: source_style_squared_tt_marginal`;
  - records the author marginalization anchor;
  - returns a marginal object that can evaluate retained pdf values.
- `SquaredTTDensity.normalized_marginal_density_values(...)` now evaluates the
  unnormalized marginal by:
  - multiplying paired basis evaluations and paired core coefficients for
    retained axes;
  - multiplying paired core coefficients with the declared basis mass matrix
    for integrated axes;
  - adding the retained defensive density term;
  - dividing by the global squared-TT normalizer.
- `TensorProductReferenceDensity` defensive marginals are handled in retained
  dimensions. Non-tensor-product defensive marginals remain unimplemented and
  fail explicitly.
- Non-prefix/suffix retained axes are not promoted as source-faithful.

## Checks

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m3_proposition2_marginalization.py tests/highdim/test_squared_tt_density.py tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py
14 passed, 2 warnings
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/squared_tt.py tests/highdim/test_p57_m3_proposition2_marginalization.py tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py
```

Passed:

```text
git diff --check -- bayesfilter/highdim/squared_tt.py tests/highdim/test_p57_m3_proposition2_marginalization.py tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py
```

Claude read-only review:

```text
VERDICT: AGREE
```

## Test Notes

- `tests/highdim/test_p57_m3_proposition2_marginalization.py` verifies prefix
  and suffix retained marginals against dense grid integration as an
  independent comparator.
- The dense comparator integrates normalized density under the reference
  measure, so a one-dimensional Lebesgue trapezoid integral is multiplied by
  `0.5` on `[-1, 1]`.
- The tests reject a non-prefix/suffix retained set (`[0, 2]`) so M3 does not
  overclaim arbitrary-axis marginalization.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Not recorded; dirty worktree contains prior unrelated changes. |
| Environment | Codex visible supervisor/executor in `/home/chakwong/BayesFilter`; TensorFlow/TFP CPU-only validation. |
| CPU/GPU status | CPU-only by `CUDA_VISIBLE_DEVICES=-1`; GPU not used. |
| Data version | Local author source under `third_party/audit/zhao_cui_tensor_ssm_p10/source`. |
| Random seeds | N/A. |
| Wall time | Focused pytest ~5 seconds. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m3-proposition2-marginalization-subplan-2026-06-11.md`. |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m3-proposition2-marginalization-result-2026-06-11.md`. |

## Post-Run Red-Team Note

Strongest alternative explanation: this could be mistaken for the full author
`marginalise` object because it uses the same mass-matrix squared-TT algebra.
That would overclaim. The implemented gate proves normalized retained marginal
value semantics and rejects grid-as-implementation; it does not yet build the
stored QR `ys/ms` recursion needed by source-style conditional KR/CDF maps.
That remaining map-state requirement belongs to P57-M4.
