# BayesFilter NeuTra c603 Integration Phase 3 Result

Date: 2026-07-06

## Status

`PASSED`

## Phase Objective

Run mechanics-only fixed-transport checks using the loaded c603 frozen dense-IAF
artifact and a reviewed value/score fixture or adapter boundary.

## Local Checks Run

- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_fixed_transport_hmc_binding_c603_fixture.py tests/test_fixed_transport_hmc_binding.py tests/test_neutra_c603_import_fixture.py -q -p no:cacheprovider`

Result:

- first run: `1 error` during collection because the new test imported
  `tests.test_neutra_c603_import_fixture` as a package module;
- repair: made `tests/test_fixed_transport_hmc_binding_c603_fixture.py`
  self-contained by inlining the local handoff-root and hash helpers instead of
  depending on `tests.*` package resolution;
- rerun: `8 passed in 5.16s`.

## Result

Phase 3 passed. BayesFilter now has a c603 mechanics-only fixed-transport
smoke test at `tests/test_fixed_transport_hmc_binding_c603_fixture.py`.

The mechanics smoke is deliberately narrow:

- it loads the reviewed c603 frozen dense-IAF artifact through the Phase 2
  fixture path;
- it binds that artifact to a synthetic quadratic base adapter;
- it checks finite value/score outputs and manifest identity fields;
- it compares the mechanics result against a direct reference computation for
  the frozen transport;
- it does not run HMC sampling, training, or GPU work.

## Nonclaims

- not a real Rotemberg target-adapter implementation;
- not HMC convergence evidence;
- not posterior correctness evidence;
- not production-readiness evidence;
- not a default-policy change.

## Next Action

Enter Phase 4 and write the generic nonlinear-SSM interface note from the now
validated import/mechanics boundaries, while keeping the separation between
target identity, filter program authority, frozen transport binding, and HMC
validation gates explicit.
