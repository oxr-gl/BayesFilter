# P57-M4 Result: Source KR/CDF Maps

metadata_date: 2026-06-11
phase: P57-M4
status: PASS_CLAUDE_REVIEWED

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Add a fixed source-style `FixedTTSIRTTransport` map surface rather than promoting the older grid-diagnostic `KRTransport` as Zhao-Cui source faithful. |
| Primary criterion status | PASS: `FixedTTSIRTTransport` exposes source-style inverse KR, forward KR, and prefix-conditional inverse KR maps for fixed natural-order `int_dir > 0`, with `eval_pdf` and forward-Jacobian tie-out. The broader P57-M2 protocol methods are present for compatibility but are not promoted as M5/M6 evidence. |
| Veto diagnostic status | PASS: the implementation does not use `KRTransport` as the promoted source route; tests cover monotone forward/inverse roundtrip, conditional inverse consistency, source contract metadata, and density/Jacobian tie-out on an analytic low-dimensional source-TT target. |
| Main uncertainty | The transport currently supports natural-order `int_dir > 0` reference-coordinate maps over already-built squared TT cores. It does not implement TT fitting, arbitrary order, `int_dir < 0`, adaptive TT-cross, or paper-scale spatial SIR. |
| Next justified action | Advance to P57-M5 proposal density and retained sampling. |
| What is not concluded | No proposal correction gate, no sequential filtering loop, no rank selection, no HMC readiness, and no spatial SIR d=18/d=50/d=100 success. |

Required token:

`PASS_P57_M4_SOURCE_KR_CDF_MAPS`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter provide source-style KR maps rather than grid diagnostic KR maps? |
| Baseline/comparator | Zhao-Cui source map methods in `AbstractIRT.m`, `SIRT.m`, and `@TTSIRT/eval_*_reference.m`. |
| Primary pass criterion | Fixed transport exposes forward KR, inverse KR, and conditional KR maps whose densities tie to Proposition-2 conditionals and `eval_pdf` semantics. |
| Veto diagnostics | `transport.py` grid CDFs promoted as source-faithful; no monotonicity/inversion tests; no density/Jacobian tie-out. |
| Artifact | `FixedTTSIRTTransport`, focused tests, this result file, and Claude review. |

## Source Anchors

| Author operation | Anchor | BayesFilter implication |
| --- | --- | --- |
| One-dimensional CDF constructors | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/SIRT.m:80-85` constructs `oned_cdfs` and calls `marginalise`. | `FixedTTSIRTTransport` is a separate source-style transport over a squared TT density and CDF config; the old grid diagnostic object is not promoted. |
| Inverse KR reference map | `@TTSIRT/eval_irt_reference.m:15-42` uses `pk + tau`, `invert_cdf`, and forward TT contractions. | `inverse_transport` sequentially inverts per-axis source conditional CDFs in natural order. |
| Forward KR reference map | `@TTSIRT/eval_rt_reference.m:13-33` uses `pk + tau`, `eval_cdf`, and updates the left contraction. | `forward_transport` evaluates per-axis source conditional CDFs using retained marginal ratios. |
| Conditional inverse KR reference map | `@TTSIRT/eval_cirt_reference.m:43-100` conditions on prefix coordinates and inverts suffix CDFs. | `conditional_inverse_transport` accepts prefix conditioning coordinates and suffix reference uniforms for `int_dir > 0`. |
| Normalized potential/pdf | `@TTSIRT/eval_potential_reference.m:10-22` uses `obj.ms`, `obj.z`, `tau`, and the reference measure potential. | `eval_pdf` combines normalized squared-TT density under the reference measure with the one-dimensional reference-measure density factor. |
| Density/Jacobian semantics | `@TTSIRT/eval_rt_jac_reference.m:1-190` differentiates the forward reference map and includes the same `pk + tau` CDF derivative semantics. | `forward_log_jacobian` sums log conditional CDF derivatives and is tested against `log(eval_pdf(...))`. |

## Implementation Changes

- Added `FixedTTSIRTTransport` in `bayesfilter/highdim/transport.py`.
- Exported `FixedTTSIRTTransport` from `bayesfilter/highdim/__init__.py`.
- `FixedTTSIRTTransport.manifest_payload()` declares:
  - `source_contract_level: fixed_ttsirt`;
  - `tt_cores_declared: True`;
  - `defensive_density_declared: True`;
  - source map anchors.
- `inverse_transport(reference_points)` implements natural-order inverse
  source KR maps on uniforms in `[0,1]`.
- `forward_transport(local_points)` implements natural-order forward source
  KR maps.
- `conditional_inverse_transport(conditioning_points, reference_points)`
  implements prefix-conditioned suffix inverse maps for `int_dir > 0`.
- `eval_pdf(local_points)` returns reference-coordinate density, including the
  Legendre reference-measure density factor, matching the author
  `eval_measure_potential_reference` convention.
- `forward_log_jacobian(local_points)` exposes the density/Jacobian tie-out.
- Existing `KRTransport` remains a lower-level diagnostic helper.

## Checks

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m4_source_kr_cdf_maps.py tests/highdim/test_p57_m2_fixed_ttsirt_transport_contract.py tests/highdim/test_transport.py tests/highdim/test_p57_m3_proposition2_marginalization.py
18 passed, 2 warnings
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/transport.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m4_source_kr_cdf_maps.py
```

Passed:

```text
git diff --check -- bayesfilter/highdim/transport.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m4_source_kr_cdf_maps.py
```

Claude read-only review:

```text
VERDICT: AGREE
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Not recorded; dirty worktree contains prior unrelated changes. |
| Environment | Codex visible supervisor/executor in `/home/chakwong/BayesFilter`; TensorFlow/TFP CPU-only validation. |
| CPU/GPU status | CPU-only by `CUDA_VISIBLE_DEVICES=-1`; GPU not used. |
| Data version | Local author source under `third_party/audit/zhao_cui_tensor_ssm_p10/source`. |
| Random seeds | N/A. |
| Wall time | Focused pytest ~7 seconds. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m4-source-kr-cdf-maps-subplan-2026-06-11.md`. |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m4-source-kr-cdf-maps-result-2026-06-11.md`. |

## Post-Run Red-Team Note

Strongest alternative explanation: the new class could be mistaken for the
complete paper-scale TTSIRT machinery. It is not. It supplies the source-style
fixed map surface over already-available squared TT cores and source marginal
value semantics. TT fitting, rank choice, proposal correction, sequential
filtering, and spatial SIR validation remain later P57 phases.
