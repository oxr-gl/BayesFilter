# Phase R11 Diagnostic: N1000 GPU XLA TF32 Contract E Score Check

Date: 2026-06-30

Status: `ACTIVE`

## Question

For the Contract E Cholesky-ridge repaired LGSSM route, does increasing to
`N=1000` on the production-default GPU XLA TF32 batched branch remove the R10
`D=2` `log_observation_variance` score failure against exact Kalman under a
`2*MCSE` seed-mean gate?

## Evidence Contract

- Baseline: R10 Stage B found that `D=2,N=64,T=10,seed_count=10` failed only on
  `log_observation_variance`: delta `-0.026313285960432253`, MCSE
  `0.005241113478035648`, about `-5.0` MCSE.
- Comparator: exact FP64 Kalman value and score for the same LGSSM fixture and
  parameter convention.
- Candidate route: Contract E Cholesky-ridge reset on GPU-visible TensorFlow,
  `float32`, TF32 enabled, XLA `jit_compile=True`, batched `seed_count=10`, no
  CPU LEDH path.  The minimal stabilizing ridge is selected as a numerical
  chart and replayed through a stopped fixed-ridge Cholesky chart for the
  differentiated scalar.  The reset gradient uses the existing fixed-ridge
  manual VJP through a TensorFlow custom-gradient wrapper, rather than generic
  Cholesky autodiff.
- Primary criterion: for `D=2,N=1000,T=10`, the Contract E seed-mean value and
  all three score components are within `2*MCSE` of exact Kalman.
- Veto diagnostics: no visible logical GPU, XLA disabled, TF32 disabled,
  nonfinite values or scores, ridge failure, covariance residual above `5e-4`,
  condition proxy above `1e8`.
- Explanatory diagnostics: seed SDs, MCSEs, z-scores, realized ridge, Sinkhorn
  row/column residuals, covariance residual.
- Not concluded even if this passes: no same-scalar FD certificate, no SIR/SV
  correctness, no HMC readiness, no production readiness, and no proof that the
  branchy ridge selector is differentiable.
- Artifact: JSON and markdown under `docs/plans` with route/device manifest and
  gate table.

## Skeptical Plan Audit

- Wrong baseline risk: using CPU material replay would not answer the LEDH
  default-route question.  The CPU draft R11 plan is superseded and must not be
  executed as LEDH evidence.
- Proxy metric risk: the old pytest `2*seed_sd` gate is too loose for comparing
  the seed average to Kalman.  This plan uses `2*MCSE`.
- Hidden route mismatch risk: the runner must report visible logical GPU, XLA,
  TF32, `N=1000`, `T=10`, `seed_count=10`, and Contract E stopped fixed-chart
  Cholesky-ridge replay with reset custom VJP.
- Runtime risk: the 13-point FD ladder at `N=1000` would be much larger than
  necessary.  R11 runs only the base value/score gate; FD remains a separate
  follow-up if the GPU branch passes the finite-`N` diagnostic.

Audit status: `PASS_AFTER_REVISION`.

## Planned Command

All GPU commands require escalated sandbox permissions.

```bash
python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gpu_score.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --num-particles 1000 \
  --seed-count 10 \
  --time-steps 10 \
  --state-dims 2 \
  --settings 0.55:2 \
  --contract-e-reset-factorization cholesky-ridge \
  --chol-ridge-abs 1e-10 \
  --chol-ridge-rel 1e-8 \
  --chol-ridge-escalation 10 \
  --chol-ridge-max-attempts 12 \
  --tf32-mode enabled \
  --xla \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r11-n1000-gpu-xla-tf32-score-diagnostic-2026-06-30.json \
  --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r11-n1000-gpu-xla-tf32-score-diagnostic-result-2026-06-30.md
```

## Stop Conditions

- Stop and report if GPU is not visible under escalated execution.
- Stop and report if XLA compile fails or OOMs at `N=1000`.
- Stop and report if the runner emits a route manifest that is not GPU/XLA/TF32
  batched.
- If the score still fails `2*MCSE`, do not reinterpret it as success under
  `2*seed_sd`; treat it as a real remaining failure and debug the scalar or
  estimator next.
