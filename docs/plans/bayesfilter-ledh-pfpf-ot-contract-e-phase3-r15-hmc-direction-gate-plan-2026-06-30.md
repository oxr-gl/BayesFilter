# Phase R15 Plan: HMC-Direction LGSSM Gate

Date: 2026-06-30

Status: `ACTIVE`

## Objective

Replace the brittle Contract E LGSSM GPU score diagnostic hard gate "every
component must be within `2*MCSE`" with an HMC-direction gate:

For each value/score component, pass if at least one of the following holds:

1. absolute error is within `2*MCSE`;
2. absolute error is within `4*MCSE` and a separate N-ladder certificate says
   MCSE decreases as N increases;
3. relative error to exact Kalman is below `1%`.

## Evidence Contract

- Comparator: exact FP64 Kalman value and score for the same LGSSM fixture.
- Primary criterion: all requested fixtures satisfy route checks and the new
  componentwise HMC-direction gate.
- Veto diagnostics: CPU route, XLA disabled, TF32 disabled, non-manual score
  route, nonfinite values/scores, covariance restoration failure, conditioning
  failure, or ridge failure.
- Required guard: the `4*MCSE` arm must not silently pass unless an explicit
  MCSE-decreases-with-N certificate flag and artifact are supplied.
- Not concluded: exact-gradient equality, finite-difference certification,
  SIR/SV correctness, HMC posterior correctness, or production budget
  promotion.

## Skeptical Audit

- Proxy-risk check: this is an HMC-direction diagnostic, not an exact-gradient
  proof.  The report must preserve exact deltas, MCSE z-scores, and relative
  errors.
- Hidden-assumption check: `4*MCSE` alone is not enough; it needs the explicit
  N-ladder MCSE certificate.
- Comparator check: exact Kalman remains the comparator.
- Route check: GPU/XLA/TF32/manual-score route checks remain vetoes.

Audit status: `PASS`.

## Planned Checks

```bash
python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gpu_score.py
python -m pytest tests/test_contract_e_gpu_score_hmc_gate.py -q
```

Then rerun the bounded `steps50` GPU diagnostic so the JSON/markdown artifact
uses the new gate.
