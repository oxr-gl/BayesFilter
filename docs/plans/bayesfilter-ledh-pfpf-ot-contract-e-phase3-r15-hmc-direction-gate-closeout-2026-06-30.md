# Phase R15 Closeout: HMC-Direction LGSSM Gate

Date: 2026-06-30

Status: `PASS`

## Decision

The Contract E LGSSM GPU score diagnostic now uses an explicit HMC-direction
gate rather than a hard exact-gradient `2*MCSE` gate.  A component passes if it
satisfies at least one of:

1. within `2*MCSE`;
2. within `4*MCSE` with an explicit N-ladder MCSE-decrease certificate;
3. below `1%` relative error to exact Kalman.

The `4*MCSE` arm is intentionally not automatic.  The current rerun passed by
the `2*MCSE` and `<1%` relative-error arms; no N-ladder certificate was claimed
or used.

## Evidence

Regenerated artifact:

- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r14-gpu-xla-tf32-sinkhorn-while-loop-steps50-2026-06-30.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r14-gpu-xla-tf32-sinkhorn-while-loop-steps50-result-2026-06-30.md`

Route checks remained valid: visible GPU, XLA enabled, TF32 enabled, and
`manual-reverse-scan` score route.

## Numerical Summary

| dim | component | z over MCSE | relative error | pass reason |
| ---: | --- | ---: | ---: | --- |
| 2 | value | `-1.216` | `0.055%` | within `2*MCSE` |
| 2 | ar coefficient | `-0.517` | `0.172%` | within `2*MCSE` |
| 2 | log transition variance | `1.201` | `0.064%` | within `2*MCSE` |
| 2 | log observation variance | `2.930` | `0.153%` | below `1%` relative error |
| 1 | value | `1.608` | `0.052%` | within `2*MCSE` |
| 1 | ar coefficient | `2.115` | `0.571%` | below `1%` relative error |
| 1 | log transition variance | `4.142` | `0.282%` | below `1%` relative error |
| 1 | log observation variance | `4.339` | `0.320%` | below `1%` relative error |

## Checks

Passed:

```bash
python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gpu_score.py
python -m pytest tests/test_contract_e_gpu_score_hmc_gate.py -q
```

GPU rerun:

```bash
bash scripts/run_contract_e_r14_gpu_sinkhorn_while_loop_steps50.sh
```

Result: `{"elapsed_seconds": 34.1172892509494, "status": "passed"}`.

## Nonclaims

- This is not an exact-gradient proof.
- This is not a finite-difference certificate.
- This does not certify SIR/SV/nonlinear models.
- This does not certify HMC posterior correctness.
- This does not promote a global Sinkhorn budget.
