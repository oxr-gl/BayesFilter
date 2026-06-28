# P06 Subplan: SVD Fresh Validation

Date: 2026-06-24

Status: `READY_FOR_LOCAL_AND_CLAUDE_REVIEW`

## Phase Objective

Validate, on fresh disjoint seeds, whether the P05-nominated
`svd_truncated` Nystrom core solver supports the frozen `tau_component=0.03`
bounded value-route screen under the same deterministic-first and
Clopper-Pearson statistical rule used in P3.

This is validation of the SVD policy for the bounded value-route screen only.
It is not default promotion, posterior correctness, HMC readiness, or a
statistical ranking against cholesky.

## Entry Conditions Inherited From Previous Phase

- P3 final status:
  `P3_INCONCLUSIVE_STOP_THRESHOLD_UNSUPPORTED_BY_PANEL`.
- P4 selected policy robustness/tuning rather than post-hoc threshold revision.
- P5 status: `P05_NOMINATE_SVD_TO_P06`.
- P5 candidate policy:
  `rank=32,epsilon=0.5,kernel_mode=raw,scaling_normalization=none,core_solver=svd_truncated,core_rcond=1e-6`.
- P5 candidate SVD tuning rows were deterministic-valid on all six fresh tuning
  seeds and had `0/6` `tau_component=0.03` exceedances.
- P06 validation seeds must be disjoint from P1 calibration/extraction seeds,
  P3 cholesky validation/extension seeds, and P5 tuning seeds.
- Forbidden prior seed manifest:
  - P1 extraction/calibration seeds: `82920..82931`;
  - P3 initial validation seeds: `82932..82945`;
  - P3 extension seeds actually run: `82946..82950`;
  - P5 SVD tuning seeds: `82962..82967`.
- Frozen threshold remains `tau_component=0.03`, with `T=20`, `M=9`, and
  `tau_total=5.4`.

## Required Artifacts

Initial validation per seed:

- JSON:
  `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p06-svd-validation-seed<SEED>-r32-eps0p5-2026-06-24.json`
- Markdown:
  `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p06-svd-validation-seed<SEED>-r32-eps0p5-2026-06-24.md`
- Log:
  `docs/plans/logs/actual-sir-nystrom-threshold-calibration-p06-svd-validation-seed<SEED>-r32-eps0p5-2026-06-24.log`

Optional extension per seed, only if the initial panel is inconclusive:

- JSON:
  `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p06-svd-extension-seed<SEED>-r32-eps0p5-2026-06-24.json`
- Markdown:
  `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p06-svd-extension-seed<SEED>-r32-eps0p5-2026-06-24.md`
- Log:
  `docs/plans/logs/actual-sir-nystrom-threshold-calibration-p06-svd-extension-seed<SEED>-r32-eps0p5-2026-06-24.log`

Aggregate summary:

- `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p06-svd-validation-summary-2026-06-24.json`

P06 result:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p06-svd-fresh-validation-result-2026-06-24.md`

Next subplan:

- P07 closeout/evidence-package subplan if P06 passes the bounded validation
  gate;
- or P07 repair/closeout subplan if P06 fails validation or hits a blocker.

## Required Checks, Tests, And Reviews

Pre-run local checks:

- verify P05 summary exists and reports `P05_NOMINATE_SVD_TO_P06`;
- verify focused SVD metadata/tensor-route tests passed in P05 preflight;
- verify initial validation seeds `82968..82981` and reserved extension seeds
  `82982..82997` are disjoint from the forbidden prior seed manifest above;
- verify `tau_component=0.03`, `tau_total=5.4`, and CP pass gate `<=0.20` are
  not changed;
- verify output/log paths are unique and predeclared;
- trusted `nvidia-smi` preflight before GPU work;
- select physical GPU1 if available/suitable, otherwise GPU0, and freeze that
  selected physical GPU for the entire P06 panel including any extension rows.

Review:

- local review required before launch;
- Claude read-only review required before execution because P06 is a material
  validation phase that can support or reject the SVD bounded value-route screen.

Execution:

- initial validation seeds: `82968..82981` (`14` fresh disjoint seeds);
- reserved extension seeds: `82982..82997` (`16` additional fresh disjoint
  seeds);
- run one seed at a time;
- parse structured artifacts after every row;
- stop immediately on deterministic invalidity, malformed/missing artifact,
  GPU/TF32/shape/policy mismatch, missing SVD metadata, or seed overlap;
- if the initial 14 deterministic-valid seeds have `0` exceedances, P06 passes
  the CP validation gate because the one-sided 95% CP upper bound is below
  `0.20`;
- if the initial panel has `1` or `2` exceedances and no deterministic vetoes,
  continue to the reserved extension seeds until reaching 30 total
  deterministic-valid rows or a third exceedance;
- stop for futility if total exceedances reaches `3`, because `3/30` cannot
  pass the frozen `0.20` CP upper-bound gate;
- do not declare an early pass from interim extension looks.  Extension success
  may be assessed only after completing the planned 30 total deterministic-valid
  row panel; early stopping is allowed only for deterministic blockers or the
  third-exceedance futility condition.
- set `CUDA_VISIBLE_DEVICES=<GPU>` through the benchmark
  `--cuda-visible-devices <GPU>` option.  TensorFlow then sees the selected
  physical GPU as visible device `/GPU:0`; record the selected physical GPU and
  remapping note in row metadata.  The same selected physical GPU must be used
  for every included P06 row unless a GPU failure triggers `P06_BLOCKED` and a
  new reviewed repair subplan.

Per-row command template:

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds <SEED> --time-steps 20 --num-particles 8192 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices <GPU> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <GPU> --gpu-selection-note '<GPU note; CUDA_VISIBLE_DEVICES remaps selected physical GPU to TensorFlow /GPU:0>' --phase-id ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P06-SVD-<VALIDATION|EXTENSION>-SEED<SEED> --quiet --output <JSON> --markdown-output <MD> > <LOG> 2>&1
```

Post-run checks:

- each JSON parses;
- deterministic validity is assessed from parsed artifacts and declared checks,
  not process exit alone;
- legacy-threshold-only process exits remain stochastic exceedances, not
  deterministic invalidity, if parsed artifact checks pass;
- each included row has route `both`, `T=20`, `N=8192`, `state_dim=18`,
  `obs_dim=9`, `float32`, TF32 enabled, expected GPU output, fixed SVD policy
  metadata, finite route outputs, finite Nystrom factors/particles, no residual
  hard veto, SVD metadata, and paired delta present;
- compute `abs(delta)/(20*9)` for each deterministic-valid row;
- count exceedance if normalized error `>0.03`;
- compute exact one-sided 95% Clopper-Pearson upper bound using all
  deterministic-valid P06 validation rows;
- write aggregate summary and P06 result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do fresh disjoint validation seeds support SVD policy `tau_component=0.03` under the exact one-sided 95% CP exceedance rule? |
| Fixed harness/execution configuration | Same-artifact compiled streaming TF32 actual-SIR route is the within-artifact value-route reference used to compute paired deltas; P06 is not a cholesky-vs-SVD method comparison and has no method-comparison baseline. |
| Candidate | `rank=32`, `epsilon=0.5`, `kernel_mode=raw`, `scaling_normalization=none`, `core_solver=svd_truncated`, `core_rcond=1e-6`. |
| Primary pass criterion | Deterministic validity passes and P06 one-sided 95% CP upper bound for `Pr(abs(delta)/(T*M)>0.03)` is `<=0.20`. |
| Continuation veto | Deterministic invalidity, malformed/missing artifact, GPU/TF32/shape/policy mismatch, missing SVD metadata, seed overlap, or total exceedances reaching `3` before/at 30 seeds. |
| Explanatory diagnostics | Runtime, residual magnitudes below deterministic thresholds, SVD factor/core diagnostics, observed normalized deltas. |
| Not concluded | No default readiness, no posterior correctness, no HMC readiness, no statistical superiority, no broad Nystrom rejection, no validation beyond this bounded value-route screen. |
| Artifact | Per-seed JSON/Markdown/logs, aggregate summary, P06 result, and P07 subplan. |

## Forbidden Claims And Actions

- Do not change `tau_component=0.03`.
- Do not change the CP pass gate `<=0.20`.
- Do not reuse P1, P3, or P5 seeds for validation claims.
- Do not use seeds in the forbidden prior seed manifest:
  `82920..82950` or `82962..82967`.
- Do not count deterministic-invalid rows as stochastic non-exceedances.
- Do not use legacy total thresholds `5.0` or `10.0` as decision thresholds.
- Do not rank SVD as statistically superior to cholesky from P06.
- Do not claim default readiness, HMC readiness, posterior correctness,
  statistical superiority, or broad Nystrom rejection.
- Do not tune threshold, rank, epsilon, kernel mode, scaling normalization,
  dtype, TF32 mode, shape, transport policy, or SVD `rcond` in this phase.

## Exact Next-Phase Handoff Conditions

- `P06_PASS_TO_P07_EVIDENCE_PACKAGE`: deterministic validity passes for all
  included rows and the P06 CP upper bound is `<=0.20`.
- `P06_FAIL_TO_P07_REPAIR_OR_CLOSEOUT`: deterministic validity passes but the
  P06 CP upper bound is `>0.20`, or total exceedances reaches `3`.
- `P06_DETERMINISTIC_BLOCKER`: any deterministic validity, artifact, GPU/TF32,
  shape, policy, metadata, timeout-without-artifact, or seed-overlap veto
  occurs.
- `P06_BLOCKED`: execution requires unapproved Claude export, GPU runtime,
  environment setup, package install, destructive action, or human
  product/scientific decision.

## Stop Conditions

- Claude/local review does not converge.
- Trusted GPU unavailable.
- Any P06 seed overlaps P1, P3, or P5 seed panels.
- A launched row times out and writes no parseable artifact.
- Deterministic validity fails.
- Total exceedance count reaches `3`.
- Continuing would require changing threshold, default policy, HMC/posterior
  scope, package/environment setup, or destructive action.

## Skeptical Plan Audit

| Risk | P06 Audit |
| --- | --- |
| Wrong baseline | Same-artifact streaming comparator is explicit; it is not a truth oracle. |
| Method-comparison confusion | P06 is single-arm SVD validation against the fixed paired-delta harness, not a cholesky-vs-SVD ranking phase. |
| Proxy metric | P06 validates only the frozen bounded value-route exceedance screen, not default readiness or posterior correctness. |
| Missing stop conditions | GPU, artifact, deterministic validity, seed overlap, timeout, metadata, third exceedance, and threshold-change stops are explicit. |
| Unfair comparison | Same model, fresh disjoint seeds, dtype, TF32, transport policy, SVD policy, shape, and one frozen selected physical GPU for the whole P06 panel. |
| Hidden assumption | SVD may pass tuning and fail validation; that would reject the current SVD bounded screen, not Nystrom broadly. |
| Stale context | P3 cholesky failure cannot be reused as SVD validation evidence; P5 tuning cannot be reused as validation evidence. |
| Environment mismatch | Trusted GPU preflight required; GPU1 preferred otherwise GPU0. |
| Artifact mismatch | Structured JSON/Markdown/logs are required for every included seed. |

Audit status: `READY_FOR_LOCAL_AND_CLAUDE_REVIEW`.
