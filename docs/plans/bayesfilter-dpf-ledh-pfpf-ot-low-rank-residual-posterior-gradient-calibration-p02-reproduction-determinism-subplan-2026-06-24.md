# P02 Three-Seed Reproduction And Jitter Subplan

Date: 2026-06-24

Status: `READY_FOR_VISIBLE_GPU_EXECUTION`

## Phase Objective

Rerun the completed `lgssm_small_exact_ref` seeds `91001,91002,91003` with the
P01 value/gradient harness and repeat the same rows under the same trusted
GPU/XLA settings to distinguish stable residual behavior from run-to-run
numerical jitter.

P02 answers whether seed `91003` has value/gradient/peak harm commensurate with
its residual exceedance.

## Entry Conditions Inherited From Previous Phase

- P01 result exists and passes instrumentation checks.
- Harness and tests exist at the P01 required paths.
- P02 subplan is refreshed with actual command shapes and reviewed.
- Owner directive on 2026-06-25 designates visible non-elevated GPU runs in
  the managed BayesFilter Codex session as trusted BayesFilter GPU evidence
  when provenance is recorded and the artifact states the trust basis.
- Candidate remains locked to `r16_eps0p25_alpha1em08_it120`.
- No approval is inherited for HMC runtime, package/API/default changes,
  package installs, network fetches, model-file edits, or scientific claims.

## Required Artifacts

- P02 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p02-reproduction-determinism-result-2026-06-24.md`
- Structured aggregate JSON:
  `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02-reproduction-2026-06-24.json`
- Aggregate Markdown:
  `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02-reproduction-2026-06-24.md`
- Logs under:
  `docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/`
- Refreshed P03 subplan.

## Required Checks, Tests, And Reviews

- Visible GPU precheck with `nvidia-smi`; elevated execution is not required
  under the 2026-06-25 owner directive for this managed session.
- Quiet visible execution with full stdout/stderr redirected to logs.
- Run fixed seeds `91001,91002,91003`, fixed case `lgssm_small_exact_ref`,
  routes `streaming` and `low_rank`, and three same-config repeats for
  residual/value/gradient diagnostics.
- Validate JSON has finite values/gradients, residuals, projection iterations,
  candidate settings, GPU/TF32/XLA provenance, nonmaterialization, and nonclaims.
- Compare observed value/gradient/peak harm against predeclared engineering
  screens:
  - exact-reference log-value absolute error is recorded and finite;
  - gradient relative norm error is recorded and finite;
  - gradient cosine similarity is recorded and finite;
  - max coordinate gradient error is recorded and finite;
  - peak-neighborhood winner or local-probe displacement is recorded.
- Claude read-only review of P02 result and P03 subplan.

## Command Shape

Visible GPU precheck:

```bash
nvidia-smi
```

P02 reproduction command:

```bash
python docs/benchmarks/benchmark_low_rank_ledh_posterior_gradient_calibration.py \
  --case-ids lgssm_small_exact_ref \
  --seeds 91001,91002,91003 \
  --route both \
  --num-particles 1024 \
  --time-steps 12 \
  --low-rank-rank 16 \
  --low-rank-assignment-epsilon 0.25 \
  --low-rank-alpha 1.0e-8 \
  --low-rank-max-projection-iterations 120 \
  --particle-chunk-size 64 \
  --warmups 0 \
  --repeats 3 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02-reproduction-2026-06-24.json \
  --markdown-output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02-reproduction-2026-06-24.md \
  --quiet
```

Full stdout/stderr must be captured under
`docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/`.
The structured artifact must record
`owner_designated_managed_session_visible_gpu_trusted` as the GPU trust basis.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the seed `91003` residual exceedance correspond to posterior value, gradient, or peak-neighborhood harm, and is the residual stable across repeats? |
| Baseline/comparator | Exact Kalman value/gradient oracle and streaming finite-particle route for the same seeds/probes. |
| Primary pass criterion | All required P02 rows produce finite visible GPU/XLA artifacts with value/gradient/peak diagnostics, recorded owner-designated managed-session trust basis, and no hard validity vetoes. |
| Veto diagnostics | Nonfinite values/gradients, missing exact reference, active-path NumPy, invalid low-rank factors, dense materialization, missing GPU/XLA provenance, corrupt artifact, or unsupported claim. |
| Explanatory diagnostics | Residual exceedance, repeat jitter, projection iterations, timing, memory, ESS, and descriptive value/gradient differences. |
| Not concluded | No calibrated threshold, no statistical ranking, no posterior correctness beyond this exact-reference diagnostic, no HMC readiness, and no default readiness. |
| Artifact | P02 result, aggregate JSON/Markdown, row logs, review ledger, and refreshed P03 subplan. |

## Forbidden Claims And Actions

- Do not change the candidate settings or threshold based on the P02 outputs.
- Do not treat P02 alone as threshold calibration or holdout validation.
- Do not rank routes statistically from three seeds or repeats without
  uncertainty support.
- Do not run HMC.
- Do not change public API, package metadata, default policy, model files, or
  dependencies.

## Exact Next-Phase Handoff Conditions

P02 hands off to P03 only if:

- P02 result and structured artifacts exist;
- local artifact validator passes;
- validity vetoes are absent, or the result explicitly classifies a blocker;
- Claude review returns `VERDICT: AGREE`;
- P03 subplan is refreshed with actual P02 findings while preserving the
  rule that P03 is calibration, not holdout.

If P02 shows the harness is invalid or gradients are nonfinite, stop for repair
instead of running P03.

## Stop Conditions

- Visible GPU runtime is unavailable or cannot record provenance/trust basis.
- Required artifacts are missing or corrupt.
- Exact reference or gradient metrics are missing.
- Low-rank route invalidity prevents measuring the target quantities.
- Claude/Codex review does not converge within five rounds for the same
  blocker.

## End-Of-Subplan Procedure

1. Run required local checks and runtime validators.
2. Write P02 result or blocker result.
3. Draft or refresh P03 subplan.
4. Review P03 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
5. Send material result/subplan to Claude read-only review and record verdict.
