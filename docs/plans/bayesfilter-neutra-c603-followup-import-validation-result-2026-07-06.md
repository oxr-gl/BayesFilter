# BayesFilter NeuTra c603 Follow-up Import Validation Result

Date: 2026-07-06

## Scope

This note records the BayesFilter-side import validation after the `dsge_hmc`
follow-up payload commit for NeuTra candidate `c603`.

This is an import/loader validation only. It is not a posterior convergence
claim, HMC-readiness claim, production-readiness claim, sampler ranking, or
scientific promotion of the Rotemberg second-order SVD target.

## Source

- Repository: `git@github.com:chakkeiwong/dsge_hmc.git`
- Branch: `bayesfilter-neutra-handoff-2026-07-05`
- Checked commit: `eb6f142e16e27b98dadaf9587eb5150187b9a44e`
- BayesFilter target signature:
  `8f5caae87797898bd8d4f0c795246f5103e3535e247a49e5ebf01217ece20d07`

## Hash Verification

The three c603 files committed by the follow-up were present and matched the
declared SHA-256 digests:

```text
935b46289332f545c29338ac2009982724e61935798e2314dd1571060ddee360  paper_dense_iaf_seed20260622.training_state.json
5f3c8e859ea859dbc3cd7cdc60bd0156f52da24b0bf1e3083ebb5a7ad580bf40  paper_dense_iaf_seed20260622_replay_state.json
5f61806c64f7abbf89271fbc41d545a98a8b99abe3f9ae82a97eea69da6bc2e8  0603_fixed_hmc_grid_candidate_index-603_leapfrog-2_step_size-0.729166666666_config.json
```

## Import Validation

The legacy `transport_state` was adapted to
`bayesfilter.neutra.dense_iaf_frozen_transport.v1` and passed:

- `finalize_dense_iaf_neutra_artifact_payload`;
- `load_frozen_neutra_artifact(..., expected_target_signature=...)`;
- finite forward/logdet smoke check on five 15-dimensional points;
- legacy NumPy forward/logdet comparison.

Component order:

```text
c603_00_dense_autoregressive_iaf
c603_01_mixing_linear
c603_02_dense_autoregressive_iaf
c603_03_mixing_linear
c603_04_dense_autoregressive_iaf
c603_05_affine
```

Adapter detail: dsge_hmc `MixingLinearTransport.forward_batch` computes
`z @ W.T`, while BayesFilter `mixing_linear` computes `values @ matrix`.
Therefore the import adapter used `matrix = W.T` for mixing layers. The final
dense affine `L_np` was kept as `L_np` because BayesFilter affine handling uses
`tf.matmul(values, matrix, transpose_b=True)`, matching dsge_hmc batch
semantics.

## Result

```text
status: loaded_and_legacy_forward_matched
transport_id: c603_rotemberg_second_order_svd_paper_dense_iaf_transport_sha256_06cbde30
dimension: 15
topology_hash: b898b910eb3367145f5260d124a3b5a8d48a1d6c2f9b050c2939990d5083e11f
tensor_hash: add7f57aa0f2d4ba61456b2a259632ca35969edbe278ed1b8af563be29f88cfd
transport_hash: 5d4b43cf2e0da2c35d5a0000a390110364f2d7d7fd205e8b0cabb72d0cf87dcc
artifact_signature: 4df1eeb2f9e6a094fbf2dfe07fd899de7a1e6576fc8a8a2268b8020228f283be
forward_shape: [5, 15]
logdet_shape: [5]
max_forward_abs_diff_vs_legacy_numpy: 4.440892098500626e-16
max_logdet_abs_diff_vs_legacy_numpy: 1.7763568394002505e-15
forward_all_finite: true
logdet_all_finite: true
```

The TensorFlow check was deliberately CPU-only with `CUDA_VISIBLE_DEVICES=-1`.
TensorFlow emitted sandbox-context CUDA initialization warnings, but the
CPU-only import validation completed successfully.

## Next Action

The payload is now bridgeable into BayesFilter's frozen dense-IAF loader. The
next engineering step is to preserve the legacy-to-BayesFilter conversion as a
small reviewed adapter or fixture, then run fixed-transport mechanics smoke
tests. Those tests remain mechanics-only unless a separate HMC evidence plan
promotes them.
