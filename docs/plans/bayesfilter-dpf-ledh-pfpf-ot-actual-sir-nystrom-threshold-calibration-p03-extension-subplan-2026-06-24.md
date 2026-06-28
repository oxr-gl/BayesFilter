# P03 Extension Subplan: Frozen-Threshold Statistical Validation To 30 Seeds

Date: 2026-06-24

Status: `READY_FOR_LOCAL_AND_CLAUDE_REVIEW`

## Phase Objective

Extend P3 frozen-threshold statistical validation from 14 to at most 30 total
disjoint deterministic-valid validation seeds, without changing
`tau_component=0.03`, the fixed Nystrom policy, the comparator, or the
Clopper-Pearson pass rule.

## Entry Conditions Inherited From Previous Phase

- P2 froze `tau_component=0.03` and `tau_total=5.4` for `T=20,M=9`.
- P3 initial panel seeds `82932..82945` are disjoint from P1 calibration seeds
  `82920..82931`.
- P3 initial panel deterministic validity passed for all 14 planned seeds.
- P3 initial panel had `n_valid=14`, `n_exceed=2`, and one-sided 95%
  Clopper-Pearson upper bound `0.38538968236388194`, above the `0.20` pass gate.
- Claude reviewed the legacy-exit repair and returned `VERDICT: AGREE`.
- Legacy paired total thresholds `5.0` and `10.0` remain deprecated and are not
  P3 decision thresholds.
- GPU policy remains trusted physical GPU1 if available/suitable, otherwise
  GPU0 with provenance note.

## Required Artifacts

Per extension seed:

- JSON:
  `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-extension-seed<SEED>-r32-eps0p5-2026-06-24.json`
- Markdown:
  `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-extension-seed<SEED>-r32-eps0p5-2026-06-24.md`
- Log:
  `docs/plans/logs/actual-sir-nystrom-threshold-calibration-p03-extension-seed<SEED>-r32-eps0p5-2026-06-24.log`

Aggregate summary:

- `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-extension-summary-2026-06-24.json`

Updated P3 result:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p03-statistical-validation-result-2026-06-24.md`

P4 subplan or stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p04-evidence-package-subplan-2026-06-24.md`
- or updated `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-visible-stop-handoff-2026-06-24.md`

## Required Checks, Tests, And Reviews

Pre-run local checks:

- verify the initial P3 summary exists and reports `n_valid=14`, `n_exceed=2`;
- verify extension seeds `82946..82961` are disjoint from P1 and initial P3
  seeds;
- verify `tau_component=0.03` and `tau_total=5.4` remain unchanged;
- trusted `nvidia-smi` preflight;
- select physical GPU1 if suitable, otherwise GPU0;
- verify benchmark harness exists;
- verify output/log paths are unique and predeclared;
- verify this extension subplan passes local section/evidence checks.

Review:

- local review required before launch;
- Claude read-only review required because this is a material extension after
  an inconclusive statistical panel.

Execution:

- planned extension seeds: `82946..82961` (`16` additional seeds);
- run one seed at a time;
- after each seed, parse the JSON/Markdown artifact before counting the row;
- stop immediately on deterministic invalidity;
- stop early if total exceedances across initial plus extension rows reaches
  `3`, because `3/30` cannot pass the frozen `0.20` CP upper-bound gate.
- do not declare an early pass from interim looks; success may be assessed only
  after completing the planned 30 total deterministic-valid row panel, while
  early stopping is allowed only for the predeclared blocker or futility
  conditions.

Per-row benchmark command template:

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds <SEED> --time-steps 20 --num-particles 8192 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices <GPU> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <GPU> --gpu-selection-note '<GPU note>' --phase-id ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P03-EXT-SEED<SEED> --quiet --output <JSON> --markdown-output <MD>
```

Post-run checks:

- each JSON parses;
- deterministic validity is assessed from parsed artifacts and declared checks,
  not process exit alone;
- each included row has route `both`, `T=20`, `N=8192`, `state_dim=18`,
  `obs_dim=9`, `float32`, TF32 enabled, expected GPU output, fixed Nystrom
  policy metadata, finite route outputs, finite Nystrom factors/particles, no
  residual hard veto, and paired delta present;
- if the benchmark process exits nonzero solely because the structured JSON
  reports deprecated legacy paired threshold labels, and all deterministic
  validity checks pass, classify that row as deterministic-valid and score it
  through the frozen stochastic rule;
- compute `abs(delta)/(20*9)`;
- count exceedance if normalized error `>0.03`;
- compute exact one-sided 95% Clopper-Pearson upper bound using all
  deterministic-valid P3 rows;
- preserve audit rows for any legacy-threshold-only process exits;
- write aggregate summary and updated P3 result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does extending to at most 30 total disjoint validation seeds support frozen `tau_component=0.03` under the exact one-sided 95% CP exceedance rule? |
| Baseline/comparator | Same-artifact compiled streaming TF32 actual-SIR route. |
| Primary pass criterion | Deterministic validity passes and total P3 one-sided 95% CP upper bound for `Pr(abs(delta)/(T*M)>0.03)` is `<=0.20`. |
| Continuation veto | Deterministic invalidity, malformed/missing artifact, GPU/TF32/shape/policy mismatch, seed overlap, or total exceedances reaching `3` before/at 30 seeds. |
| Explanatory diagnostics | Runtime, residual magnitudes below deterministic thresholds, factor/scaling diagnostics, observed normalized deltas. |
| Not concluded | No default readiness, no posterior correctness, no HMC readiness, no statistical superiority, no broad Nystrom rejection, no uniqueness claim for `tau_component=0.03`. |
| Artifact | Per-seed JSON/Markdown/logs, extension summary, updated P3 result. |

## Forbidden Claims And Actions

- Do not change `tau_component`.
- Do not change the CP pass gate `<=0.20`.
- Do not use legacy `5.0` as a decision threshold.
- Do not use P1 seeds or initial P3 seeds as new extension seeds.
- Do not count deterministic-invalid rows as stochastic non-exceedances.
- Do not claim default readiness, HMC readiness, posterior correctness,
  statistical superiority, or broad Nystrom rejection.
- Do not extend beyond 30 total P3 validation seeds without a new reviewed
  subplan and human-visible rationale.
- Do not retune rank, epsilon, solver, kernel mode, scaling normalization,
  dtype, TF32 mode, shape, or transport policy during this extension.

## Exact Next-Phase Handoff Conditions

- `P3_PASS_TO_P4`: deterministic validity passes for all included rows and total
  P3 CP upper bound is `<=0.20`.  With current `n_exceed=2`, this requires no
  additional exceedances through 30 total valid seeds.
- `P3_INCONCLUSIVE_STOP_THRESHOLD_UNSUPPORTED_BY_PANEL`: deterministic validity
  passes but total exceedances reach `3`, making the planned 30-seed extension
  unable to pass the `0.20` gate.  This is not a deterministic failure and not a
  broad Nystrom rejection.
- `P3_DETERMINISTIC_BLOCKER`: any deterministic validity veto, timeout without
  artifact, GPU mismatch, malformed artifact, or seed overlap occurs.

## Stop Conditions

- Trusted GPU unavailable.
- Any extension seed overlaps P1 or initial P3 seed panels.
- A launched row times out and writes no parseable artifact.
- Deterministic validity fails.
- Total exceedance count reaches `3`.
- Continuing would require changing threshold, default policy, HMC/posterior
  scope, package/environment setup, or destructive action.

## Skeptical Plan Audit

| Risk | P3 Extension Audit |
| --- | --- |
| Wrong baseline | Same-artifact streaming comparator, not truth. |
| Proxy metric | Frozen `tau_component` remains only a bounded value-route criterion. |
| Missing stop conditions | GPU, artifact, deterministic validity, seed overlap, timeout, third exceedance, and threshold-change stops are explicit. |
| Unfair comparison | Same model, seeds disjoint, dtype, TF32, transport policy, fixed Nystrom policy, and selected GPU per row. |
| Hidden assumption | A pass would validate only this bounded threshold screen, not posterior/HMC/default readiness. |
| Stale context | Legacy `5.0` remains deprecated and cannot re-enter through exit status. |
| Environment mismatch | Trusted GPU preflight required; GPU1 preferred otherwise GPU0. |
| Artifact mismatch | Structured JSON/Markdown/logs are required for every included seed. |

Audit status: `READY_FOR_LOCAL_AND_CLAUDE_REVIEW`.

Claude read-only review round P3-extension-R1 returned `VERDICT: AGREE` under a
bounded no-file-inspection prompt.  Claude requested no required fixes and
suggested clarifying that interim looks cannot declare early pass; that
clarification is incorporated above.
