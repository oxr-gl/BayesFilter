# P57-M5 Result: Proposal Density And Retained Sampling

metadata_date: 2026-06-11
phase: P57-M5
status: PASS_CLAUDE_REVIEWED

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Verify retained sample generation uses source transport `eval_pdf` proposal semantics on local transported samples, not base uniform/reference density alone. |
| Primary criterion status | PASS: `source_route_generate_retained_samples` obtains `local_r = transport.inverse_transport(z)`, maps physical samples by `x = L local_r + mu`, computes proposal density from `transport.proposal_log_density(local_r,z)`, and sets correction weights `log_target(local_r) - log_proposal(local_r)`. |
| Veto diagnostic status | PASS: focused tests reject base-density-only semantics for the new `FixedTTSIRTTransport`, verify the author `exp(-fun_post(r))/eval_pdf(sirt,r)` identity, verify affine determinant placement inside `fun_post`, and check retained manifests/ESS. |
| Main uncertainty | M5 validates one-step retained sample generation and correction semantics. It does not connect retained objects across time; that is P57-M6. |
| Next justified action | Advance to P57-M6 sequential fixed-HMC source loop. |
| What is not concluded | No full sequential filtering loop, no rank selection, no HMC readiness, and no spatial SIR d=18/d=50/d=100 success. |

Required token:

`PASS_P57_M5_PROPOSAL_DENSITY_RETAINED_SAMPLING`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can retained sample generation and proposal correction match the author Algorithm 3 density semantics? |
| Baseline/comparator | Paper equations (21)--(23), Algorithm 3, author `full_sol.m:33-38`, `eval_irt`, and `eval_pdf`. |
| Primary pass criterion | Proposal correction divides by the same density represented by author `eval_pdf(sirt,r)` on local transported samples after `eval_irt`, with affine determinant handled in the target coordinate convention. |
| Veto diagnostics | Source transport uses `log_reference_density(reference)` as denominator; proposal sign untested; determinant placement ambiguous; retained samples lack route manifest. |
| Artifact | Focused tests, this result file, and Claude review. |

## Source Anchors

| Author operation | Anchor | BayesFilter implication |
| --- | --- | --- |
| Draw uniforms and invert SIRT | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:33-35` draws `z = rand(...)` and calls `[r, ~] = eval_irt(sol.SIRTs{t}, z)`. | `source_route_generate_retained_samples` receives fixed reference samples and calls `transport.inverse_transport(reference)` to get local `r`. |
| Affine local-to-physical samples | `full_sol.m:36` sets `samples = L(:,:,t) * r + mu(:,t)`. | `SourceRouteTarget.physical_points_from_reference(local_r)` applies `matrix @ local_r + mu`. |
| Proposal correction denominator | `full_sol.m:37` sets `w = exp(-fun_post(r))./eval_pdf(sol.SIRTs{t}, r)`. | Correction is `target_log_density(local_r) - proposal_log_density(local_r)`, with `proposal_log_density = log(eval_pdf(sirt, local_r))` for source transports. |
| Affine determinant in local target | `full_sol.m:91-93` defines `logfun_post(x) = fun_into_sirt(..., L_temp*x + mu_temp, const) - log(abs(det(L_temp)))`. | `SourceRouteTarget.negative_log_density(local_r)` computes physical negative log density minus `log|det L|` and then subtracts the shift constant. |
| Log normalizer increment | `full_sol.m:124` adds `log(sirt.z) - const`. | `SourceRouteNormalizerContribution.log_increment()` returns `log_transport_normalizer - shift_constant`. |

## Implementation And Tests

- M2 already patched `source_route_generate_retained_samples()` to call
  `transport.proposal_log_density(...)` instead of base
  `log_reference_density(reference)`.
- M4 added `FixedTTSIRTTransport.proposal_log_density(...)`, which returns
  `log(eval_pdf(local_r))`.
- M5 adds `tests/highdim/test_p57_m5_proposal_density_retained_sampling.py`.
- The main M5 test verifies:
  - `local_r = inverse_transport(reference)`;
  - `physical = L local_r + mu`;
  - `author_fun_post = negative_log_physical(physical) - log|det L| - const`;
  - `proposal_log_density = log(eval_pdf(local_r))`;
  - `correction = -author_fun_post - proposal_log_density`;
  - retained log weights are normalized correction weights.
- A separate M5 test verifies the proposal denominator for
  `FixedTTSIRTTransport` is not the base uniform density.
- A retained manifest test verifies source route labels, sample origin, sample
  count, and finite positive ESS.

## Checks

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m5_proposal_density_retained_sampling.py tests/highdim/test_p57_m4_source_kr_cdf_maps.py tests/highdim/test_p57_m2_fixed_ttsirt_transport_contract.py tests/highdim/test_p55_source_route_one_step.py tests/highdim/test_p49_source_route_sample_proposal.py
23 passed, 2 warnings
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p57_m5_proposal_density_retained_sampling.py bayesfilter/highdim/source_route.py bayesfilter/highdim/transport.py
```

Passed:

```text
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/transport.py tests/highdim/test_p57_m5_proposal_density_retained_sampling.py
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
| Random seeds | Fixed deterministic tensor samples in tests. |
| Wall time | Focused pytest ~12 seconds. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m5-proposal-density-retained-sampling-subplan-2026-06-11.md`. |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m5-proposal-density-retained-sampling-result-2026-06-11.md`. |

## Post-Run Red-Team Note

Strongest alternative explanation: a one-step retained-sampling test could pass
even if the sequential loop still uses the wrong previous retained object or
normalizer. M5 only closes the proposal-denominator/sign/determinant gate for
sample generation. M6 must connect retained objects across time and preserve
the same semantics in the full fixed-HMC sequential loop.
