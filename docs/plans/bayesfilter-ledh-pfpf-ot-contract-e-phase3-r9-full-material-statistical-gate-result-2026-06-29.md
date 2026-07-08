# Phase R9 Result: Full Phase 3 Material Statistical Gate

Date: 2026-06-29

Status: `BLOCKED_STAGE_B_FAILED_FIXED_RIDGE_STATISTICAL_GATE`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Retain `PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION`; R9 cannot unblock the full Phase 3 material gate. |
| Primary criterion status | Failed at Stage B. The no-autodiff manual route and same-scalar FD parity passed, but the reviewed material statistical criteria failed for covariance restoration and exact Kalman agreement. |
| Veto diagnostic status | No outer tape, no logical GPU, TF32 disabled, XLA disabled, no ridge failure, and same-scalar FD passed. Vetoes were covariance residual and exact Kalman value/score disagreement. |
| Main uncertainty | Whether a smaller or principled fixed ridge `lambda`, or a different smooth chart policy, can preserve same-scalar differentiability while restoring covariance and Kalman agreement. |
| Next justified action | Start R10: a reviewed fixed-ridge `lambda` calibration and smooth-chart policy diagnostic. |
| Not concluded | No SIR/SV correctness, no HMC readiness, no GPU/XLA/TF32 readiness, no production readiness, and no full Phase 3 blocker removal. |

## Stage A Manifest

- Git commit: `9bc5a65` with dirty/untracked workspace artifacts.
- Command:

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  --device-scope cpu \
  --num-particles 16 \
  --seed-count 3 \
  --time-steps 10 \
  --state-dims 1 \
  --settings 0.55:2 \
  --contract-e-reset-factorization cholesky-ridge \
  --chol-ridge-abs 0.75 \
  --chol-ridge-rel 0 \
  --chol-ridge-max-attempts 1 \
  --gate-mode material \
  --fd-steps 1e-5,1e-5,1e-5 \
  --no-xla \
  --output /tmp/contract_e_phase3_r9_stage_a_material.json
```

- Artifact: `/tmp/contract_e_phase3_r9_stage_a_material.json`
- Environment: CPU-hidden TensorFlow run with `CUDA_VISIBLE_DEVICES=-1`.
- TensorFlow device manifest: `physical_gpus=[]`, `logical_gpus=[]`, `tf32_execution_enabled=false`, `xla=false`.
- Route: `manual_likelihood_reverse_scan_no_autodiff`.
- Route label: `contract_e_cholesky_fixed_ridge_manual_lgssm_t10`.
- Ridge policy: fixed `lambda=0.75`, `chol_ridge_rel=0`, `chol_ridge_max_attempts=1`.
- Seed schedule: initial/transition seeds `9100..9102`; residual seeds `[seed,43+t]` for `t=0..9`.

## Stage A Evidence

Stage A status was `passed`.

Same-scalar FD parity passed for all parameters:

| Parameter | Max Abs Error | Max Rel Error |
| --- | ---: | ---: |
| `ar_coefficient` | `3.219202682203104e-10` | `5.6129226156479905e-11` |
| `log_transition_variance` | `7.882716701601566e-11` | `6.132604737864704e-11` |
| `log_observation_variance` | `1.6306556105405434e-10` | `7.546650546412255e-11` |

Warnings from explanatory diagnostics:

- Value mean was `-8.02057674028184`; exact Kalman value was `-6.9145050235173295`; delta was `-1.10607171676451`; MCSE was `0.11693907989922726`.
- Score mean was `[-5.1089073113762415, -1.383973086877507, -2.1626917151101774]`.
- Exact Kalman score was `[-2.480624571002596, -1.952888328246029, -2.741816788342589]`.
- Score MCSE was `[0.33829018097643027, 0.05541071303432697, 0.018289186199146802]`.
- Maximum covariance relative residual was `7.446501238045564`; maximum mean residual was `9.71445146547012e-17`.

These warnings mean Stage A should not be read as evidence that Contract E is statistically correct.  It only confirms that the material manual score route scales from the R8 tiny fixture to `D=1,T=10,N=16,seed_count=3` and matches same-scalar FD on that route.

## Checks Run

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest \
  tests/test_contract_e_phase3_material_manual_route.py \
  tests/test_contract_e_phase3_r7_lgssm_manual_route.py \
  tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py \
  tests/test_contract_e_phase3_r5_manual_reverse_integration.py \
  tests/test_contract_e_cholesky_ridge_reset.py \
  tests/test_contract_e_phase3_gradient_route_audit.py -q
```

Result: `18 passed in 21.69s`.

```bash
python -m py_compile \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  docs/benchmarks/contract_e_reset_tf.py \
  tests/test_contract_e_phase3_material_manual_route.py
```

Result: passed.

```bash
git diff --check -- \
  docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r9-full-material-statistical-gate-execution-subplan-2026-06-29.md \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  tests/test_contract_e_phase3_material_manual_route.py \
  tests/test_contract_e_phase3_gradient_route_audit.py
```

Result: passed.

## Handoff To Stage B

Stage B is justified as the smallest reviewed run that can decide whether the full material blocker can be removed for CPU-hidden FP64 evidence.  Because Stage A shows large covariance residual and Kalman disagreement, Stage B should be interpreted with veto diagnostics first.  If Stage B fails, R9 should write a blocker result and retain `PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION`.

## Stage B Manifest

- Command:

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  --device-scope cpu \
  --num-particles 64 \
  --seed-count 10 \
  --time-steps 10 \
  --state-dims 1 2 \
  --settings 0.55:2 \
  --contract-e-reset-factorization cholesky-ridge \
  --chol-ridge-abs 0.75 \
  --chol-ridge-rel 0 \
  --chol-ridge-max-attempts 1 \
  --gate-mode material \
  --fd-steps 1e-5,1e-5,1e-5 \
  --no-xla \
  --output /tmp/contract_e_phase3_r9_stage_b_material.json
```

- Artifact: `/tmp/contract_e_phase3_r9_stage_b_material.json`
- Environment: CPU-hidden TensorFlow run with `CUDA_VISIBLE_DEVICES=-1`.
- TensorFlow device manifest: `physical_gpus=[]`, `logical_gpus=[]`, `tf32_execution_enabled=false`, `xla=false`.
- Route: `manual_likelihood_reverse_scan_no_autodiff`.
- Route label: `contract_e_cholesky_fixed_ridge_manual_lgssm_t10`.
- Ridge policy: fixed `lambda=0.75`, `chol_ridge_rel=0`, `chol_ridge_max_attempts=1`.
- Exit status: failed as expected from the gate because Stage B criteria were not met.

## Stage B Evidence

Overall gate status: `failed`.

Both dimensions passed the route and same-scalar FD checks:

| Dim | Parameter | FD Pass | Max Abs Error | Max Rel Error |
| ---: | --- | --- | ---: | ---: |
| 1 | `ar_coefficient` | true | `4.232854067254266e-10` | `9.036854652792006e-11` |
| 1 | `log_transition_variance` | true | `1.6779799771882153e-10` | `1.1287594953946473e-10` |
| 1 | `log_observation_variance` | true | `2.013580413517957e-10` | `9.257543365059191e-11` |
| 2 | `ar_coefficient` | true | `6.430092014397815e-10` | `6.31085546844888e-11` |
| 2 | `log_transition_variance` | true | `2.302189550107414e-10` | `7.889260791392336e-11` |
| 2 | `log_observation_variance` | true | `3.5623148875174593e-10` | `8.270185087442504e-11` |

The material statistical checks failed:

| Dim | Value Mean | Kalman Value | Delta | MCSE | Max Cov Residual |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `-8.081136031457655` | `-6.9145050235173295` | `-1.1666310079403255` | `0.025297404801998914` | `3.1382688364049636` |
| 2 | `-16.168097413931537` | `-13.784138558146358` | `-2.3839588557851794` | `0.0428541736799126` | `2.5196124029294915` |

| Dim | Parameter | Score Mean | Kalman Score | Delta | MCSE | Within 2 MCSE |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `ar_coefficient` | `-4.969960033001023` | `-2.480624571002596` | `-2.4893354619984267` | `0.061025255907908464` | false |
| 1 | `log_transition_variance` | `-1.4414287697755115` | `-1.952888328246029` | `0.5114595584705175` | `0.009953195098769772` | false |
| 1 | `log_observation_variance` | `-2.1601340015524406` | `-2.741816788342589` | `0.5816827867901484` | `0.008265470838112687` | false |
| 2 | `ar_coefficient` | `-10.103121400080214` | `-4.97169664637836` | `-5.131424753701854` | `0.12907031235881558` | false |
| 2 | `log_transition_variance` | `-2.883021657709835` | `-3.9324314599263497` | `1.0494098022165148` | `0.018139171254883773` | false |
| 2 | `log_observation_variance` | `-4.360755584650311` | `-5.503182552777064` | `1.1424269681267525` | `0.013581368340004533` | false |

## Interpretation

R9 rules out the previous wiring/autodiff explanation for the full material failure: the material route is now a no-autodiff manual reverse scan and agrees with central same-scalar FD to around `1e-10` on Stage B.  The remaining failure is statistical/numerical: the fixed `lambda=0.75` Cholesky-ridge chart badly distorts covariance restoration and therefore value/score agreement with the exact LGSSM Kalman comparator.

The blocker is therefore retained with a narrower diagnosis:

`PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION`

means: the manual route is validated as a derivative of its own fixed-ridge scalar, but the current fixed-ridge scalar is not acceptable material LGSSM evidence because covariance restoration and exact Kalman checks fail.

## R10 Handoff

R10 should not revisit the reverse-scan wiring unless same-scalar FD fails again.  It should instead ask whether there exists a principled fixed-ridge or smooth-chart policy that:

- keeps the no-autodiff manual route and same-scalar FD parity;
- avoids branch replay instability;
- reduces covariance residual below `5e-4`; and
- restores exact Kalman value/score agreement within the reviewed uncertainty criterion.
