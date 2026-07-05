# Phase R11 Closeout: N1000 GPU XLA TF32 Contract E Score Diagnostic

Date: 2026-06-30

Status: `FAILED_SCORE_ROUTE_BLOCKED_BY_GPU_OUTER_TAPE_NAN`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Do not use the CPU-hidden material route as LEDH evidence.  The correct R11 route is GPU-visible, XLA-compiled, TF32-enabled, batched over 10 seeds. |
| Primary criterion status | Failed.  The `D=2,N=1000,T=10,R=10` value mean was finite but just outside `2*MCSE`; the score was not interpretable because all score components were `NaN`. |
| Veto diagnostic status | GPU visible, XLA compiled on CUDA, TF32 enabled, no ridge failure, covariance residual passed.  Score finite-base veto failed. |
| Main uncertainty | The remaining score failure is not yet evidence against the Contract E mathematical repair, because the GPU nonmaterial score runner uses an outer-tape path that produces `NaN` upstream of the Contract E reset. |
| Next justified action | Implement or port the Contract E batched manual-reverse score route under `tf.while_loop`/XLA, matching the existing successful batched manual-score pattern, then rerun `N=1000`. |
| Not concluded | No CPU LEDH evidence, no SIR/SV correctness, no HMC readiness, no production readiness, and no same-scalar FD certificate at `N=1000`. |

## Run Manifest

Main command:

```bash
bash scripts/run_contract_e_r11_gpu_score.sh
```

Localization command:

```bash
bash scripts/run_contract_e_r11_gpu_score_skip_reset_probe.sh
```

Both commands were run with trusted GPU/CUDA sandbox escalation.

Environment:

- TensorFlow: `2.19.1`
- GPU: NVIDIA GeForce RTX 4080 SUPER
- Logical GPU visible: true
- XLA: true; log contained `Compiled cluster using XLA!`
- TF32 execution: true
- `N=1000`, `T=10`, `seed_count=10`, `state_dim=2`
- reset: Contract E Cholesky-ridge, minimal ridge with stopped fixed-chart replay and reset custom VJP in the main diagnostic.

Artifacts:

- Main JSON: `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r11-n1000-gpu-xla-tf32-score-diagnostic-2026-06-30.json`
- Main markdown: `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r11-n1000-gpu-xla-tf32-score-diagnostic-result-2026-06-30.md`
- Skip-reset JSON: `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r11-n1000-gpu-xla-tf32-skip-reset-probe-2026-06-30.json`
- Skip-reset markdown: `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r11-n1000-gpu-xla-tf32-skip-reset-probe-result-2026-06-30.md`

## Main Result

The main GPU/XLA/TF32 run used the correct LEDH execution route and completed
without OOM.  Its route/device manifest passed: GPU visible, XLA true, TF32
true.

Value result:

| Dim | Mean | Kalman | Delta | SD | MCSE | z |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | `-13.797056` | `-13.784139` | `-0.012917` | `0.019898` | `0.006292` | `-2.053` |

Score result:

| Parameter | Status |
| --- | --- |
| `ar_coefficient` | `NaN` |
| `log_transition_variance` | `NaN` |
| `log_observation_variance` | `NaN` |

Reset diagnostics:

- max covariance relative residual: `2.350563903519287e-07`
- max mean residual: `1.4901161193847656e-08`
- max realized ridge: `2.060866144404372e-09`
- max ridge attempts: `1`
- ridge failure: false

## Localization Result

The skip-reset GPU/XLA/TF32 probe bypassed Contract E reset computation and
used the barycentric next particles.  It still produced `NaN` scores for all
three parameters.

Therefore, the `NaN` score is upstream of the Contract E reset custom VJP.  It
is in the nonmaterial GPU outer-tape score route around the LEDH flow,
logweight correction, or dense transport matrix AD path.  The correct next move
is not CPU replay and not more ridge tuning; it is to wire a fully batched
manual-reverse Contract E score route under XLA.

## Checks

```bash
python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gpu_score.py docs/benchmarks/contract_e_reset_tf.py
```

Result: passed.

```bash
python -m pytest tests/test_contract_e_cholesky_ridge_reset.py -q
```

Result: `7 passed`.

```bash
git diff --check -- docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gpu_score.py docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r11-n1000-gpu-xla-tf32-score-diagnostic-2026-06-30.md
```

Result: passed.
