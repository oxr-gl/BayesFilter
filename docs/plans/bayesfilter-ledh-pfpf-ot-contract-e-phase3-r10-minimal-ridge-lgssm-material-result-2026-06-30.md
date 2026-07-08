# Phase R10 Result: Minimal Stabilizing Ridge Material LGSSM Gate

Date: 2026-06-30

Status: `PARTIAL_SUCCESS_STAGE_B_RETAINS_BLOCKER`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Retain `PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION`, but narrow the diagnosis: the R9 fixed `lambda=0.75` covariance distortion is remedied by the minimal-ridge replay policy. |
| Primary criterion status | Stage A passed. Stage B failed only because the `D=2` `log_observation_variance` score mean was outside `2*MCSE` of exact Kalman. |
| Veto diagnostic status | No outer tape, CPU-hidden route, TF32 disabled, XLA disabled, no ridge failure, branch replay passed, same-scalar FD passed, and covariance residuals passed. Kalman score gate failed for one `D=2` score component. |
| Main uncertainty | Whether the remaining `D=2` score discrepancy is finite-seed Monte Carlo fluctuation, a small residual bias in the Contract E scalar, or a remaining manual-score implementation issue specific to the observation covariance contribution. |
| Next justified action | Run a discriminating R11 diagnostic that increases seed count or uses repeated independent seed blocks for the `D=2` score, with the same minimal-ridge replay policy and same-scalar FD guard. |
| Not concluded | No GPU/XLA/TF32 readiness, no SIR/SV/nonlinear correctness, no HMC readiness, no production readiness, and no claim that the branchy ridge selector itself is differentiable. |

## Implemented R10 Change

- Added material route policy `minimal_stabilizing_replayed_fixed_chart`.
- The center material pass selects the smallest per-batch Cholesky ridge on the configured ladder.
- The selected ridge vector is stored in the replay chart and reused for the manual VJP and same-scalar FD scalar.
- Branch diagnostics also report the ridge that would be reselected at FD perturbations; the FD gate requires this branch record to match.
- Legacy R9 fixed `lambda=0.75` commands still work for reproducibility.

## Stage A Manifest

Command:

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  --device-scope cpu \
  --num-particles 16 \
  --seed-count 3 \
  --time-steps 10 \
  --state-dims 1 \
  --settings 0.55:2 \
  --contract-e-reset-factorization cholesky-ridge \
  --chol-ridge-abs 1e-10 \
  --chol-ridge-rel 1e-8 \
  --chol-ridge-escalation 10 \
  --chol-ridge-max-attempts 12 \
  --gate-mode material \
  --fd-steps 1e-5,1e-5,1e-5 \
  --no-xla \
  --output /tmp/contract_e_phase3_r10_stage_a_material.json
```

Artifact: `/tmp/contract_e_phase3_r10_stage_a_material.json`

Result: `passed`.

Key diagnostics:

| Dim | Same-Scalar FD | Max Cov Residual | Realized Ridge Range | Max Attempts |
| ---: | --- | ---: | ---: | ---: |
| 1 | `pass` | `1.8020065274468433e-08` | `[4.4565216737463617e-10, 2.3184121415139693e-09]` | `1` |

Stage A value and score were also close to Kalman, but Stage A remains a route-scaling check, not the material promotion gate.

## Stage B Manifest

Command:

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  --device-scope cpu \
  --num-particles 64 \
  --seed-count 10 \
  --time-steps 10 \
  --state-dims 1 2 \
  --settings 0.55:2 \
  --contract-e-reset-factorization cholesky-ridge \
  --chol-ridge-abs 1e-10 \
  --chol-ridge-rel 1e-8 \
  --chol-ridge-escalation 10 \
  --chol-ridge-max-attempts 12 \
  --gate-mode material \
  --fd-steps 1e-5,1e-5,1e-5 \
  --no-xla \
  --output /tmp/contract_e_phase3_r10_stage_b_material.json
```

Artifact: `/tmp/contract_e_phase3_r10_stage_b_material.json`

Result: `failed`.

## Stage B Evidence

The ridge distortion from R9 is gone:

| Dim | Same-Scalar FD | Branch Replay | Max Cov Residual | Realized Ridge Range | Max Attempts |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | `pass` | `pass` | `5.163836266592292e-09` | `[9.745431432570664e-10, 2.19883743890681e-09]` | `1` |
| 2 | `pass` | `pass` | `6.992006362709771e-09` | `[1.156589299316169e-09, 2.2433125395906423e-09]` | `1` |

The material value gate passed:

| Dim | Value Mean | Kalman | Delta | MCSE | Within 2 MCSE |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | `-6.902093357677832` | `-6.9145050235173295` | `0.012411665839497488` | `0.024466550594093472` | true |
| 2 | `-13.791735498018861` | `-13.784138558146358` | `-0.0075969398725028725` | `0.018742286360267053` | true |

The score gate passed except for `D=2` `log_observation_variance`:

| Dim | Parameter | Score Mean | Kalman | Delta | MCSE | Within 2 MCSE |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `ar_coefficient` | `-2.4310453125556966` | `-2.480624571002596` | `0.04957925844689948` | `0.07033434680268297` | true |
| 1 | `log_transition_variance` | `-1.9545121707111768` | `-1.952888328246029` | `-0.0016238424651477956` | `0.010321420497201325` | true |
| 1 | `log_observation_variance` | `-2.7402821602073835` | `-2.741816788342589` | `0.0015346281352055513` | `0.0053231961485146135` | true |
| 2 | `ar_coefficient` | `-5.050012787378971` | `-4.97169664637836` | `-0.07831614100061035` | `0.0664032700935952` | true |
| 2 | `log_transition_variance` | `-3.9273062315951712` | `-3.9324314599263497` | `0.005125228331178455` | `0.008802906967326737` | true |
| 2 | `log_observation_variance` | `-5.529495838737496` | `-5.503182552777064` | `-0.026313285960432253` | `0.005241113478035648` | false |

Same-scalar FD max errors remained small:

| Dim | Parameter | Max Abs Error | Max Rel Error |
| ---: | --- | ---: | ---: |
| 1 | `ar_coefficient` | `1.0609824130369816e-10` | `4.7137195464806274e-11` |
| 1 | `log_transition_variance` | `1.7064194501870134e-10` | `8.534926631786914e-11` |
| 1 | `log_observation_variance` | `2.0893597962867716e-10` | `7.594217697569579e-11` |
| 2 | `ar_coefficient` | `1.972022545260188e-10` | `3.6757560825987015e-11` |
| 2 | `log_transition_variance` | `3.635576284466424e-10` | `9.248070620536749e-11` |
| 2 | `log_observation_variance` | `5.254765511608639e-10` | `9.503692078184841e-11` |

## Checks Run

```bash
python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py docs/benchmarks/contract_e_reset_tf.py tests/test_contract_e_phase3_material_manual_route.py
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_contract_e_phase3_material_manual_route.py -q
```

Result: `5 passed`.

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest \
  tests/test_contract_e_phase3_material_manual_route.py \
  tests/test_contract_e_phase3_r7_lgssm_manual_route.py \
  tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py \
  tests/test_contract_e_phase3_r5_manual_reverse_integration.py \
  tests/test_contract_e_cholesky_ridge_reset.py \
  tests/test_contract_e_phase3_gradient_route_audit.py -q
```

Result before the final legacy diagnostic-field cleanup: `21 passed`.

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest \
  tests/test_contract_e_phase3_material_manual_route.py \
  tests/test_contract_e_cholesky_ridge_reset.py -q
```

Result after the final cleanup: `12 passed`.

```bash
git diff --check -- docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py docs/benchmarks/contract_e_reset_tf.py tests/test_contract_e_phase3_material_manual_route.py docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r10-minimal-ridge-lgssm-material-subplan-2026-06-30.md
```

Result: passed.

## Interpretation

R10 confirms the user's concern: fixed `lambda=0.75` was a planning/numerical policy error, not a principled Contract E setting.  A minimal stabilizing ridge near `1e-9` restores covariance to below `1e-8` while preserving the no-autodiff manual route and same-scalar FD parity.

However, the full material LGSSM gate is still not formally cleared because the `D=2` observation-variance score misses the exact Kalman comparator by about `5.0` MCSE under the current 10-seed Stage B protocol.  The remaining issue is now much narrower than R9: it is not ridge-induced covariance distortion, not outer autodiff leakage, and not same-scalar derivative mismatch.

## Handoff To R11

R11 should keep the R10 minimal-ridge replay policy fixed and run the smallest discriminating diagnostic for the remaining `D=2` `log_observation_variance` score discrepancy:

- increase independent seed blocks or seed count for `D=2,N=64,T=10`;
- preserve same-scalar FD and branch replay checks;
- report whether the `log_observation_variance` score discrepancy shrinks like Monte Carlo error or remains biased;
- do not lower the material gate without a reviewed evidence-contract change.
