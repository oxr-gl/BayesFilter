# Zhao-Cui Tensor-SSM P10 Audit Snapshot

metadata_date: 2026-05-30

This directory is a non-production audit artifact for the BayesFilter
high-dimensional nonlinear filtering monograph P10 pass.

It preserves a pinned copy of the Zhao-Cui companion code for:

- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Upstream repository:
  `https://github.com/DeepTransport/tensor-ssm-paper-demo`
- Upstream commit audited:
  `80034dccb99eb1d86284a1839b4a12067d13b9da`

## Contents

- `source/`: patched audit snapshot used for the Octave smoke.
- `octave_compatibility.patch`: the patch from upstream commit
  `80034dccb99eb1d86284a1839b4a12067d13b9da` to the local Octave-compatible
  audit snapshot.

## License Boundary

The upstream code carries LGPL-3.0-or-later and embedded deep-tensor license
files.  This directory is not BayesFilter production code and must not be
imported into the production `bayesfilter/` package without a separate license
and clean-room implementation decision.

## Reduced Octave Smoke

The audit patch adds a reduced Kalman smoke:

```bash
timeout 60s octave-cli --quiet --no-gui \
  third_party/audit/zhao_cui_tensor_ssm_p10/source/octave_compat/p10_octave_kalman_smoke.m
```

Expected success marker:

```text
P10_OCTAVE_SMOKE_DONE
```

This smoke uses `T=1`, `N=64`, `rank=4`, and one ALS pass.  It demonstrates
that the TT/SIRT solver path can execute under Octave after compatibility
patching.  It does not reproduce the paper figures and does not validate
posterior accuracy, HMC readiness, or production suitability.
