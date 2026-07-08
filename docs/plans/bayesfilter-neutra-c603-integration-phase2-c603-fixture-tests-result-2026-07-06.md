# BayesFilter NeuTra c603 Integration Phase 2 Result

Date: 2026-07-06

## Status

`PASSED`

## Phase Objective

Add a repeatable c603 fixture test path that uses the Phase 1 adapter to
reproduce the validated import, loader acceptance, payload/hash identity, and
legacy forward/logdet tie-out from a documented local dsge_hmc handoff
checkout.

## Local Checks Run

- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_neutra_c603_import_fixture.py tests/test_legacy_neutra_import.py tests/test_dense_iaf_neutra_artifact_loader.py -q -p no:cacheprovider`

Result:

- first run: `1 failed, 11 passed` because the new c603 fixture test sourced
  `theta_reference` from the export proposal instead of the reviewed preflight
  JSON;
- repair: patched `tests/test_neutra_c603_import_fixture.py` to read
  `theta_reference` from
  `phase1/preflight/rotemberg_second_order_svd_target_preflight.json`;
- rerun: `12 passed in 4.36s`.

## Result

Phase 2 passed. BayesFilter now has a repeatable c603 local-fixture test at
`tests/test_neutra_c603_import_fixture.py`.

The fixture test is explicit about its boundary:

- it uses a documented local handoff checkout rooted at
  `BAYESFILTER_DSGE_HMC_HANDOFF_ROOT` or the reviewed default
  `/tmp/dsge_hmc-neutra-handoff-20260705`;
- it skips loudly if that local checkout is absent;
- it does not fetch from network and does not import live `dsge_hmc` Python
  modules;
- it verifies the three reviewed c603 file SHA-256 digests before importing;
- it rebuilds the payload through the Phase 1 adapter, not through a one-off
  manual script.

The c603 fixture test reproduced the validated import identity:

```text
target_signature: 8f5caae87797898bd8d4f0c795246f5103e3535e247a49e5ebf01217ece20d07
topology_hash:   b898b910eb3367145f5260d124a3b5a8d48a1d6c2f9b050c2939990d5083e11f
tensor_hash:     add7f57aa0f2d4ba61456b2a259632ca35969edbe278ed1b8af563be29f88cfd
transport_hash:  5d4b43cf2e0da2c35d5a0000a390110364f2d7d7fd205e8b0cabb72d0cf87dcc
artifact_signature:
                 4df1eeb2f9e6a094fbf2dfe07fd899de7a1e6576fc8a8a2268b8020228f283be
```

It also reproduced the reviewed component order:

```text
c603_00_dense_autoregressive_iaf
c603_01_mixing_linear
c603_02_dense_autoregressive_iaf
c603_03_mixing_linear
c603_04_dense_autoregressive_iaf
c603_05_affine
```

Finally, the test matched the loaded BayesFilter transport against a direct
legacy forward/logdet replay on five 15-dimensional points under CPU-only
execution.

## Nonclaims

- not a generic target-contract reconstruction proof;
- not a real HMC or sampler-quality check;
- not a posterior correctness claim;
- not a production-readiness claim;
- not evidence that local external handoff artifacts should become tracked
  BayesFilter repo artifacts.

## Next Action

Enter Phase 3 and use the loaded c603 local fixture artifact in a
mechanics-only fixed-transport test, still without running HMC sampling,
training, or GPU work.
