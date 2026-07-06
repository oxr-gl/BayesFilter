# P03 Subplan: Frozen-Threshold Statistical Validation

Date: 2026-06-24

Status: `REPAIRED_LEGACY_EXIT_STATUS_READY_TO_CONTINUE`

## Phase Objective

Run disjoint-seed actual-SIR Nystrom validation under the frozen
`tau_component=0.03` bounded value-route threshold and exact one-sided 95%
Clopper-Pearson exceedance rule.

## Entry Conditions Inherited From Previous Phase

- P2 closed as `P2_FREEZE_PASS_TO_P3`.
- Frozen threshold:
  `tau_component=0.03`, `tau_total=5.4` for `T=20,M=9`.
- P1 calibration/extraction seeds were `82920..82931`.
- P3 validation seeds must be disjoint from P1 seeds.
- Legacy `5.0` is not the P3 decision threshold.
- GPU policy: trusted context, physical GPU1 if available/suitable, otherwise
  GPU0 with fallback note.

## Required Artifacts

Per validation seed:

- JSON:
  `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-validation-seed<SEED>-r32-eps0p5-2026-06-24.json`
- Markdown:
  `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-validation-seed<SEED>-r32-eps0p5-2026-06-24.md`
- Log:
  `docs/plans/logs/actual-sir-nystrom-threshold-calibration-p03-validation-seed<SEED>-r32-eps0p5-2026-06-24.log`

Aggregate summary:

- `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-validation-summary-2026-06-24.json`

P3 result:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p03-statistical-validation-result-2026-06-24.md`

P4 subplan or blocker:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p04-evidence-package-subplan-2026-06-24.md`

## Required Checks, Tests, And Reviews

Pre-run local checks:

- verify P2 result exists and freezes `tau_component=0.03`;
- verify validation seeds are disjoint from `82920..82931`;
- trusted `nvidia-smi` preflight;
- select physical GPU1 if suitable, otherwise GPU0;
- verify benchmark harness exists;
- verify output/log paths are unique and predeclared.

Validation seed panel:

- planned seeds: `82932..82945` (`14` disjoint seeds);
- rationale: with 0 exceedances, `14` valid seeds can make the exact one-sided
  95% Clopper-Pearson upper bound fall below `0.20`;
- if deterministic-valid exceedances occur, P3 may extend by reviewed repair of
  this subplan up to `22` or `30` total validation seeds only if runtime and
  user/runtime boundaries allow.

Per-row benchmark command template:

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds <SEED> --time-steps 20 --num-particles 8192 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices <GPU> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <GPU> --gpu-selection-note '<GPU note>' --phase-id ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P03-SEED<SEED> --quiet --output <JSON> --markdown-output <MD>
```

Post-run checks:

- each JSON parses;
- each included row has deterministic validity:
  route `both`, `T=20`, `N=8192`, `state_dim=18`, `obs_dim=9`, `float32`,
  TF32 enabled, expected GPU output, fixed Nystrom policy metadata, finite
  route outputs, finite Nystrom factors/particles, no residual hard veto, and
  paired delta present;
- if the benchmark process exits nonzero solely because the structured JSON
  reports `paired:paired_log_likelihood_mean_abs_delta` or
  `paired:paired_log_likelihood_max_abs_delta` from the deprecated legacy
  threshold, and all deterministic validity checks above pass, classify that
  row as deterministic-valid and score it only through the frozen P3 stochastic
  exceedance rule;
- compute `abs(delta)/(20*9)`;
- count exceedance if normalized error `>0.03`;
- compute exact one-sided 95% Clopper-Pearson upper bound using denominator
  `n_valid`, the number of deterministic-valid validation seeds;
- write aggregate summary and P3 result;
- preserve an audit trail in the aggregate summary and P3 result for any row
  whose process exit was nonzero only because of deprecated legacy paired
  threshold labels, including its normalized error and P3 exceedance status.

Review:

- local review required;
- Claude read-only review required for P3 result and P4 subplan if P3 claims a
  pass, inconclusive result, rejection, or extension decision.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do disjoint validation seeds support the frozen `tau_component=0.03` bounded value-route threshold? |
| Baseline/comparator | Same-artifact compiled streaming TF32 actual-SIR route. |
| Primary pass criterion | Deterministic validity passes and exact one-sided 95% Clopper-Pearson upper bound for `Pr(abs(delta)/(T*M)>0.03)` is `<=0.20`. |
| Veto diagnostics | Deterministic invalidity, malformed artifact, wrong policy/shape/GPU/TF32 metadata, validation seeds overlapping P1 seeds, timeout, missing paired delta, or post-hoc threshold change. |
| Explanatory diagnostics | Runtime, ESS, residual magnitudes below deterministic thresholds, factor/scaling diagnostics, observed normalized deltas. |
| Not concluded | No default readiness, no posterior correctness, no HMC readiness, no statistical superiority, no broad Nystrom rejection. |
| Artifact | Per-seed JSON/Markdown/logs, aggregate summary, P3 result. |

## Forbidden Claims And Actions

- Do not change `tau_component`.
- Do not use legacy `5.0` as the decision threshold.
- Do not let the benchmark harness exit status reintroduce legacy `5.0` as a
  deterministic P3 stop when the structured artifact is complete and
  deterministic-valid.
- Do not use P1 seeds as validation seeds.
- Do not count deterministic-invalid rows as stochastic non-exceedances.
- Do not claim default readiness, HMC readiness, posterior correctness, or
  statistical superiority.
- Do not extend beyond planned seeds without a reviewed subplan patch.

## Exact Next-Phase Handoff Conditions

- `P3_PASS_TO_P4`: deterministic validity passes for all included rows and
  Clopper-Pearson upper bound is `<=0.20`.
- `P3_INCONCLUSIVE_EXTENSION_REVIEW`: deterministic validity passes but upper
  bound is `>0.20`, and extending to more disjoint seeds is feasible and
  reviewed.
- `P3_INCONCLUSIVE_STOP`: deterministic validity passes but statistical evidence
  remains underpowered and extension is not authorized or feasible.
- `P3_DETERMINISTIC_BLOCKER`: any deterministic validity veto, timeout, GPU
  mismatch, malformed artifact, or seed overlap occurs.

## Stop Conditions

- Trusted GPU unavailable.
- Any validation seed overlaps P1 seed panel.
- A launched row times out or writes malformed/missing artifacts.
- Deterministic validity fails.
- Continuing would require changing threshold, default policy, HMC/posterior
  scope, package/environment setup, or destructive action.

Non-stop condition:

- Benchmark process exit code `1` caused only by deprecated legacy paired
  log-likelihood thresholds is not a P3 deterministic blocker when the JSON and
  Markdown artifacts exist, parse, and pass deterministic validity.  The row is
  counted as one stochastic exceedance if `abs(delta)/(20*9) > 0.03`.

## Focused Repair Audit: Legacy Harness Exit Status

During execution, seed `82943` wrote complete JSON/Markdown artifacts but the
benchmark process returned nonzero because the inherited harness still exits on
the deprecated total paired mean threshold `5.0`.  The structured artifact
showed both routes deterministic-valid and a normalized paired delta above the
frozen `tau_component=0.03`.

This repair does not change `tau_component`, the validation split, GPU policy,
shape, Nystrom policy, or the Clopper-Pearson rule.  It prevents the legacy
threshold from re-entering P3 as a deterministic stop through process exit
status.  Malformed artifacts, timeouts, GPU mismatch, wrong metadata, nonfinite
values, Nystrom residual failures, missing paired delta, and true deterministic
validity failures remain stop conditions.

Claude read-only review round P3-repair-R1b returned `VERDICT: AGREE` under a
bounded no-file-inspection prompt.  Required guardrails are incorporated here:
only exclusively legacy paired-threshold exits are downgraded; deterministic
validity is assessed from parsed artifacts and declared P3 checks; the aggregate
summary and P3 result must record any such downgraded legacy-exit row.

## Skeptical Plan Audit

| Risk | P3 Audit |
| --- | --- |
| Wrong baseline | Same-artifact streaming comparator, not truth. |
| Proxy metric | Frozen `tau_component` is only bounded value-route criterion. |
| Missing stop conditions | GPU, artifact, deterministic validity, seed overlap, timeout, and threshold-change stops are explicit. |
| Unfair comparison | Same model, seeds, dtype, TF32, transport policy, fixed Nystrom policy, and selected GPU per row. |
| Hidden assumption | `0.20` exceedance target is bounded value-route only. |
| Stale context | Legacy `5.0` is not used as decision threshold. |
| Environment mismatch | Trusted GPU preflight required; GPU1 preferred otherwise GPU0. |
| Artifact mismatch | Structured JSON/Markdown/logs are required for every seed. |

Audit status: `READY_FOR_LOCAL_PRECHECK`.
