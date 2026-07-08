# Phase 3 Subplan: Longer HMC Diagnostics

Date: 2026-07-06

Status: `READY_FOR_REVIEW_APPROVED_RUNTIME_AFTER_REVIEW`

## Phase Objective

Run one exact, reviewed, trusted GPU/XLA longer HMC diagnostic on the minimal
scalar-dimension `zhaocui_fixed` target, adding R-hat/ESS and sampled-state
target/reference checks that the earlier hard-veto ladder did not compute.

This phase may reject the current fixed-kernel sampler settings without
rejecting the research direction. R-hat/ESS or sampled-state reference failures
are promotion vetoes unless they also invalidate the artifact, target, runtime,
or required diagnostics.

## Entry Conditions Inherited From Previous Phase

- Phase 2 result exists and passed:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase2-oracle-implementation-result-2026-07-06.md`.
- Phase 2 JSON artifact status is `passed`:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase2_oracle_cpu_hidden_2026-07-06.json`.
- Phase 2 establishes only selected conditional-slice and sampled-value
  reference machinery; it does not establish full posterior correctness.
- The latest completed mechanics baseline remains:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.json`.
- The user approved crossing the longer-HMC runtime boundary on 2026-07-06,
  but runtime still waits for this exact subplan to pass review.

## Required Artifacts

- Harness:
  `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_validity_phase3_2026_07_06.py`
- Tests:
  `tests/test_minimal_ssl_lstm_zhaocui_hmc_validity_phase3.py`
- JSON runtime artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.json`
- Markdown runtime artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.md`
- Quiet log:
  `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase3_longer_gpu_xla_2026-07-06.log`
- Review bundle/result record under `docs/reviews`.
- Phase 3 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-longer-hmc-diagnostics-result-2026-07-06.md`
- Refreshed Phase 4 divergence-telemetry subplan.

## Exact Runtime Command

Run only after local checks and review converge:

```bash
CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_validity_phase3_2026_07_06.py --trusted-gpu-xla-approval --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.md
```

Stdout/stderr must be captured in the quiet log path listed above.

## Predeclared Runtime Settings

| Setting | Value |
| --- | --- |
| Device target | Trusted GPU/XLA, `CUDA_VISIBLE_DEVICES=0` |
| `use_xla` / `jit_compile` | `True` / `True` |
| Target adapter | `MinimalZhaoCuiHMCTargetAdapter` |
| Filter name | `zhaocui_fixed` |
| Prior scale | `5.0` |
| Initial center | `initial_minimal_ssl_lstm_hmc_state(1.0e-3)` |
| Chain count | `4` |
| Chain start spread | `0.03` deterministic alternating-sign offsets |
| Retained draws per chain | `64` |
| Burn-in draws per chain | `32` |
| HMC step size | `1.0e-5` |
| Leapfrog steps | `1` |
| HMC seed | `[20260706, 6301]` |
| Trace policy | `standard` |
| Adaptation policy | `fixed_kernel_no_adaptation` |
| R-hat diagnostic | split R-hat, threshold `max_finite_split_rhat <= 1.2` |
| ESS diagnostic | cross-chain ESS, threshold `min_finite_ess >= 16.0` |
| Sampled-state reference check | first, middle, and final draw for every chain |
| Target/reference tolerance | absolute `<= 1.0e-9` or relative `<= 1.0e-12` |

These settings are deliberately modest and diagnostic. They are not a default
policy, not a tuned sampler, and not a production route.

## Required Checks, Tests, Reviews

Before runtime:

- Skeptical plan audit: confirm this exact command answers the Phase 3
  question and does not smuggle a posterior, ranking, default, or source-faithful
  claim.
- Confirm Phase 2 JSON status is `passed`.
- Compile:
  `python -m py_compile docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_validity_phase3_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_hmc_validity_phase3.py`
- Focused tests:
  `CUDA_VISIBLE_DEVICES=-1 python -m pytest -q tests/test_minimal_ssl_lstm_zhaocui_hmc_validity_phase3.py`
- `git diff --check`.
- Claim-boundary scan over the Phase 3 harness, test, subplan, result, and
  artifacts.
- Read-only review of this subplan and review bundle. Claude may be used only
  through the compact read-only review gate; if external review is blocked or
  unavailable, use a fresh visible Codex substitute review and record that the
  substitute is weaker than full Claude review.

After runtime:

- Validate JSON with `python -m json.tool`.
- Confirm the artifact records GPU provenance, XLA/JIT, TF32 flag, command,
  seed, chain count, draw count, Phase 2 artifact path, and nonclaims.
- Write the Phase 3 result with decision and inference-status tables.
- Refresh Phase 4 divergence-telemetry subplan based on observed telemetry
  status.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does a modest longer trusted GPU/XLA fixed-kernel HMC run on the minimal target produce valid artifacts, finite samples, sampled-state target/reference agreement, and minimal R-hat/ESS convergence-screen evidence? |
| Baseline/comparator | Phase 2 conditional-slice/sampled-value oracle machinery plus the completed `hmc-next` Phase 5 GPU/XLA hard-veto mechanics artifact. |
| Primary artifact criterion | The exact command runs or cleanly records a preflight blocker, writes valid JSON/Markdown/log artifacts, and preserves all diagnostic roles and nonclaims. |
| Promotion criterion | No hard runtime vetoes, sampled-state target/reference checks pass, split R-hat is finite for all 24 coordinates with max `<= 1.2`, cross-chain ESS is finite for all 24 coordinates with min `>= 16.0`, and required provenance is present. |
| Promotion vetoes | Failed R-hat threshold, failed ESS threshold, sampled-state target/reference mismatch, missing native divergence telemetry, or descriptive sample behavior that argues against treating this fixed-kernel setting as a viable sampler setting under a written diagnostic. Acceptance rate is explanatory only unless a required finite log-accept or target-log-prob diagnostic is missing/nonfinite. |
| Continuation vetoes | Runtime exception that prevents artifact creation, nonfinite samples or target values, invalid JSON/artifact schema, missing required diagnostics, corrupted Phase 2 comparator, GPU/XLA provenance failure for the trusted run, or unsupported claim. |
| Explanatory diagnostics | Runtime, acceptance, sample summaries, per-coordinate means/stds, R-hat/ESS summaries, native divergence availability, trace key availability, and sampled-state target/reference errors. |
| Not concluded | Full posterior correctness, broad HMC convergence, dimensional generality, source-faithful Zhao-Cui parity, ranking/superiority, default readiness, production readiness, public API/package readiness, or LEDH evidence. |

## Forbidden Claims And Actions

- Do not claim full posterior correctness from conditional-slice or sampled-state
  value agreement.
- Do not claim broad HMC convergence; a passing screen would mean only that the
  minimal target passed this modest predeclared diagnostic.
- Do not treat `not_exposed_by_kernel` native divergence status as zero
  divergences.
- Do not rank, tune, change defaults, change public API, edit model files,
  install packages, fetch network resources, or perform destructive git actions.
- Do not use source-faithful Zhao-Cui language; this target remains the internal
  frozen `zhaocui_fixed` fixture unless a later source-anchor phase earns more.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 4 after Phase 3 writes a result record and one of these is
true:

- the promotion screen passes and Phase 4 investigates native divergence
  telemetry with the passing artifact as context;
- the promotion screen fails without a continuation veto and Phase 4/5 are
  updated to localize telemetry or tuning/mass causes;
- runtime is blocked and the result records the approval, environment, or
  artifact blocker.

Do not stop merely because R-hat/ESS fail. That is a sampler-setting promotion
veto and a repair trigger unless it also invalidates the artifact or required
diagnostics.

## Stop Conditions

Stop if review does not converge after five rounds for the same blocker, if the
exact runtime command is no longer approved, if required diagnostics cannot be
recorded, if Phase 2 comparator status is not `passed`, if GPU/XLA provenance is
missing for the trusted run, if artifact schema is invalid, or if continuing
would cross an unreviewed scientific/runtime/product/source-faithful boundary.
