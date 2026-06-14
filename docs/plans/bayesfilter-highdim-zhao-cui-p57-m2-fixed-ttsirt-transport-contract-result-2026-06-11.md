# P57-M2 Result: FixedTTSIRT Transport Contract

metadata_date: 2026-06-11
phase: P57-M2
status: PASS_CLAUDE_REVIEWED

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Strengthen the source-route transport contract so later fixed-HMC TTSIRT work cannot use base/reference-density-only semantics or grid-KR substitutes as Zhao-Cui source faithfulness. |
| Primary criterion status | PASS after repair: `SourceRouteTransportProtocol` now requires inverse KR, forward KR, conditional inverse KR, `eval_pdf`, potential, proposal log density, marginalization, log normalizer, and explicit source-contract metadata. Production `fixed_ttsirt` transports must declare TT-core and defensive-density metadata; analytic doubles must be labeled `contract_test_double`. |
| Veto diagnostic status | PASS after repair: base-density-only transports are rejected; retained sampling uses transport proposal/eval-pdf semantics rather than `log_reference_density(reference)` as the real source-route denominator; result wording no longer claims that M2 implemented production TT cores or defensive density. |
| Main uncertainty | The production fixed TTSIRT transport is not implemented yet; M2 locks the required surface and tests analytic doubles. |
| Next justified action | Claude read-only source-anchor review; if agreed, advance to P57-M3 Proposition-2 marginalization. |
| What is not concluded | No production TTSIRT fit, no Proposition-2 implementation, no rank readiness, no filtering correctness, no HMC readiness, and no spatial SIR success. |

Required token:

`PASS_P57_M2_FIXED_TTSIRT_TRANSPORT_CONTRACT`

## Source Anchors

| Author operation | Anchor | Contract implication |
| --- | --- | --- |
| Inverse KR map and density | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m:152-188` implements `eval_irt(obj,z)` returning target samples and density. | Contract requires `inverse_transport(reference_points)` and `eval_pdf(local_points)`. |
| Forward KR map | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m:192-213` implements `eval_rt(obj,x)`. | Contract requires `forward_transport(local_points)`. |
| Conditional inverse KR map | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m:217-270` implements `eval_cirt(obj,x,z)`. | Contract requires `conditional_inverse_transport(conditioning_points, reference_points)`. |
| Normalized potential/pdf | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m:299-354` implements `eval_pdf`, `eval_potential`, and `random`; `@TTSIRT/eval_potential_reference.m:1-36` defines normalized potential using `obj.z`, `fx+tau`, and measure potential. | Contract requires `eval_pdf`, `potential`, `proposal_log_density`, and positive finite density checks. |
| Defensive density and CDF construction | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/SIRT.m:50-86` converts potential to square-root density, constructs CDFs, sets `tau`, and calls `marginalise`. | Contract records source-route methods and rejects grid/base-only substitutes. |
| TT/SIRT marginalization | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:1-87` performs mass-matrix/QR recursions and sets `obj.z = obj.fun_z + obj.tau`. | Contract requires `marginalize(keep_axes)` for later retained-object phases. |
| Proposal correction denominator | P56 checked author `full_sol.m:33-38` and `AbstractIRT.m` density semantics: samples from `eval_irt` are corrected using `eval_pdf(sirt,r)`. | `source_route_generate_retained_samples` now calls `transport.proposal_log_density(local_points=..., reference_points=...)`, whose source-faithful implementation must be `eval_pdf`-equivalent on local transported samples. |

## Implementation Changes

- `SourceRouteTransportProtocol` now requires:
  - `inverse_transport`;
  - `forward_transport`;
  - `conditional_inverse_transport`;
  - `eval_pdf`;
  - `potential`;
  - `proposal_log_density`;
  - `marginalize`;
  - `log_normalizer`.
- `SourceRouteTransportProtocol` now also requires `manifest_payload()` to
  declare `source_contract_level`:
  - `contract_test_double` for analytic tests that expose the required source
    surface but do not claim production TT/SIRT semantics;
  - `fixed_ttsirt` for production transports, which must also declare
    `tt_cores_declared=True` and `defensive_density_declared=True`.
- `manifest_payload()` records `required_source_methods` and
  `proposal_density_semantics`.
- `source_route_generate_retained_samples()` now obtains proposal density from
  `transport.proposal_log_density(local_points=..., reference_points=...)`
  rather than `log_reference_density(reference)`.
- P55 analytic test doubles were updated to expose the full source-route
  surface; their base-density methods remain diagnostic-only.
- Added `tests/highdim/test_p57_m2_fixed_ttsirt_transport_contract.py`.
- Claude iteration 1 found that the first result overstated the evidence: M2
  had implemented the API surface but not fixed TT-core or defensive-density
  invariants. Accepted and repaired by adding metadata gates and revising this
  result's wording.
- Claude repair review returned `VERDICT: AGREE`.

## Checks

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m2_fixed_ttsirt_transport_contract.py tests/highdim/test_p55_source_route_target_transport.py tests/highdim/test_p55_source_route_one_step.py
12 passed, 2 warnings
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py tests/highdim/test_p57_m2_fixed_ttsirt_transport_contract.py tests/highdim/test_p55_source_route_target_transport.py tests/highdim/test_p55_source_route_one_step.py
```

Passed:

```text
git diff --check -- bayesfilter/highdim/source_route.py tests/highdim/test_p57_m2_fixed_ttsirt_transport_contract.py tests/highdim/test_p55_source_route_target_transport.py tests/highdim/test_p55_source_route_one_step.py
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Not recorded; dirty worktree contains prior unrelated changes. |
| Environment | Codex visible supervisor/executor in `/home/chakwong/BayesFilter`; TensorFlow/TFP CPU-only validation. |
| CPU/GPU status | CPU-only by `CUDA_VISIBLE_DEVICES=-1`; GPU not used. |
| Data version | Local author source under `third_party/audit/zhao_cui_tensor_ssm_p10/source`. |
| Random seeds | N/A. |
| Wall time | Focused pytest ~5 seconds. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m2-fixed-ttsirt-transport-contract-subplan-2026-06-11.md`. |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m2-fixed-ttsirt-transport-contract-result-2026-06-11.md`. |

## Post-Run Red-Team Note

Strongest alternative explanation: a stricter contract plus metadata can still
be satisfied by a fake transport unless later phases prove the fixed TT/SIRT
implementation has Proposition-2 marginalization and KR semantics.  M2 only
makes the required surface and production metadata impossible to ignore and
prevents base-density-only proposal correction from being mistaken for author
`eval_pdf` semantics.
