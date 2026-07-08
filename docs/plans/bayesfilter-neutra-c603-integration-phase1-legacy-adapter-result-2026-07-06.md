# BayesFilter NeuTra c603 Integration Phase 1 Result

Date: 2026-07-06

## Status

`PASSED`

## Phase Objective

Implement a small BayesFilter-owned legacy dsge_hmc dense-IAF transport-state
adapter that converts reviewed legacy `transport_state` dictionaries into
`bayesfilter.neutra.dense_iaf_frozen_transport.v1` payloads with fail-closed
semantics.

## Local Checks Run

- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_legacy_neutra_import.py tests/test_dense_iaf_neutra_artifact_loader.py -q -p no:cacheprovider`

Result:

- `11 passed in 3.87s`

## Result

Phase 1 passed. BayesFilter now has an internal legacy NeuTra import helper at
`bayesfilter/inference/legacy_neutra_import.py` plus focused tests at
`tests/test_legacy_neutra_import.py`.

The adapter remains intentionally narrow and fail-closed:

- supported legacy component kinds are only
  `dense_autoregressive_iaf`, `mixing_linear`, and `affine`;
- legacy dense IAF import rejects `s_max != 1.0`;
- nonfinite tensors are rejected;
- mixing orientation is converted from legacy `z @ W.T` to BayesFilter
  `values @ matrix` by importing `matrix = W.T`;
- loader acceptance still requires
  `finalize_dense_iaf_neutra_artifact_payload` and
  `load_frozen_neutra_artifact`;
- no public `bayesfilter.inference` API expansion was required.

The focused tests proved that the adapter can build a schema-valid dense-IAF
payload from reviewed legacy state, that the loaded transport matches a direct
legacy-style forward/logdet computation on a synthetic fixture, and that the
rejection rules fire for unsupported component kinds, nonfinite tensors,
dimension mismatches, and `s_max != 1.0`.

## Nonclaims

- not a c603 real-artifact replay yet;
- not a generic loader for arbitrary dsge_hmc transports;
- not a posterior correctness claim;
- not an HMC readiness claim;
- not a production-readiness claim;
- not a default-policy change.

## Next Action

Enter Phase 2 and add a repeatable c603 fixture test that uses the reviewed
adapter plus the local dsge_hmc handoff checkout to reproduce the validated
import, payload hashes, loader acceptance, and legacy forward/logdet tie-out
without a one-off manual script.
