# Phase 5 Subplan: Longer Sampler-Diagnostics Execution

Date: 2026-07-06

Status: `DRAFT_AWAITING_PHASE4_RESULT_REVIEW_AND_RUNTIME_APPROVAL`

## Phase Objective

Execute the reviewed longer sampler-diagnostics ladder exactly as approved in
Phase 4, preserving diagnostic roles and evidence limits.

## Entry Conditions Inherited From Previous Phase

- Phase 4 design result passed review.
- Exact commands, seeds, budgets, artifacts, diagnostic roles, and stop
  conditions are predeclared.
- Required long-run/runtime approval is granted.
- Phase 5 harness mode exists and rejects setting/seed drift before runtime.
- Phase 3 GPU/XLA smoke artifact remains the immediate runtime baseline.

## Required Artifacts

- Runtime JSON/Markdown artifacts.
- Quiet logs.
- Phase 5 result with decision table, inference-status table, run manifest, and
  post-run red-team note.
- Refreshed Phase 6 closeout subplan.

Exact Phase 5 runtime artifacts:

- JSON:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.json`
- Markdown:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.md`
- Quiet log:
  `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_next_2026-07-06/phase5_longer_gpu_xla_ladder_2026-07-06.log`
- Result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase5-longer-diagnostics-execution-result-2026-07-06.md`

## Required Checks, Tests, Reviews

- Pre-run compile/import checks.
- The exact reviewed longer sampler command.
- Artifact validation.
- Material result review.
- `git diff --check`.
- Claim-boundary scan for unsupported convergence, ranking, default-readiness,
  source-faithfulness, and production-readiness claims.

## Skeptical Plan Audit

The plan is allowed to execute only if:

- Phase 3, not Phase 2, is the immediate GPU/XLA runtime baseline;
- the runtime command uses `CUDA_VISIBLE_DEVICES=0`, `use_xla=True`, and
  `jit_compile=True`;
- every numerical diagnostic is preclassified before execution;
- acceptance, runtime, sample summaries, and seed-to-seed variation are
  explanatory only;
- native divergence is a hard veto only when native telemetry is available and
  positive;
- native divergence status `not_exposed_by_kernel` is recorded as uncertainty,
  not as zero divergences;
- the command cannot silently change seeds, chain length, burnin, step size, or
  leapfrog count;
- approval is requested for the trusted GPU/XLA runtime boundary before launch.

Audit status before execution: `PENDING_PHASE4_REVIEW_AND_APPROVAL`.

## Research Intent Ledger

| Field | Ledger |
| --- | --- |
| Main question | Does the minimally longer trusted GPU/XLA ladder avoid hard runtime/sampler vetoes under fixed settings? |
| Candidate/mechanism under test | Internal minimal scalar `zhaocui_fixed` HMC target with fixed-kernel TFP HMC, no adaptation, XLA enabled. |
| Expected failure mode | CUDA/XLA runtime exception, hidden GPU, nonfinite target/sample, invalid artifact, missing telemetry/provenance, or positive native divergence if exposed. |
| Promotion criterion | All three predeclared seeds complete with no hard vetoes and valid artifacts. |
| Promotion veto | Any hard veto in any seed row. |
| Continuation veto | Invalid artifact, missing provenance, unapproved runtime boundary, post-hoc criterion edits, or unsupported claim pressure. |
| Repair trigger | Runtime exception, nonfinite samples, missing telemetry, or fail-closed validation triggers a smaller diagnostic/plan repair. |
| Explanatory diagnostics | Acceptance rate, runtime, sample shape, sample finite counts, sample mean/std/min/max, initial log prob/score norm, device provenance, TF32, XLA/JIT metadata, TensorFlow log. |
| Must not conclude | HMC convergence, posterior correctness, ranking/superiority, default readiness, production readiness, source-faithful parity, public API/package readiness, or LEDH result. |

## Fixed Runtime Settings

| Setting | Value |
| --- | --- |
| Harness mode | `phase5-longer-gpu-xla-ladder` |
| Device boundary | `CUDA_VISIBLE_DEVICES=0` |
| HMC seeds | `(20260706, 5101)`, `(20260706, 5102)`, `(20260706, 5103)` |
| `num_results` | `8` |
| `num_burnin_steps` | `4` |
| `step_size` | `1e-5` |
| `num_leapfrog_steps` | `1` |
| `use_xla` / `jit_compile` | `True` / `True` |
| Chain execution mode | `tf_function` |
| Trace policy | `standard` |
| Adaptation policy | `fixed_kernel_no_adaptation` |
| Prior scale | `5.0` |
| Initial offset scale | `1e-3` |

The harness must reject changes to these fixed settings for this mode.

## Exact Commands

Pre-run local checks:

```bash
python -m compileall -q bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py tests/test_ssl_lstm_zhaocui_hmc_minimal.py tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 pytest -q tests/test_ssl_lstm_zhaocui_hmc_minimal.py tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py
```

Reviewed runtime command, after explicit approval:

```bash
CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py --mode phase5-longer-gpu-xla-ladder --trusted-gpu-xla-approval --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.md --num-results 8 --num-burnin-steps 4 --step-size 1e-5 --num-leapfrog-steps 1 > docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_next_2026-07-06/phase5_longer_gpu_xla_ladder_2026-07-06.log 2>&1
```

Post-run validation:

```bash
python -m json.tool docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.json >/tmp/minimal_ssl_lstm_phase5_json_validation_2026-07-06.out
```

```bash
git diff --check
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the longer predeclared ladder avoid hard sampler/runtime vetoes and what, if anything, remains viable for future validation? |
| Baseline/comparator | Phase 3 trusted GPU/XLA smoke, Phase 2 CPU regression only as non-GPU debug context, and the Phase 4 reviewed design. |
| Primary pass criterion | The predeclared three-seed ladder completes, required artifacts are valid, all rows record `use_xla=True`/`jit_compile=True` with GPU provenance, and no hard vetoes are observed. |
| Veto diagnostics | Runtime exception, hidden/missing GPU, missing approval, nonfinite target/sample, invalid artifact, missing required diagnostic/provenance, positive native divergence if exposed, post-hoc criterion change, unsupported ranking/convergence/default claim, or review nonconvergence. |
| Explanatory diagnostics | Acceptance, runtime, sample shape, finite counts, sample mean/std/min/max, per-seed rows, TensorFlow logs, and native divergence availability status when not positive. ESS/R-hat are not computed in this modest ladder. |
| Not concluded | HMC convergence, posterior correctness, ranking/superiority, default readiness, production readiness, public API/package readiness, source-faithful parity, LEDH result, or broad scientific validity. |

## Forbidden Claims And Actions

Do not rank viable stochastic candidates using descriptive diagnostics alone.
Do not claim convergence or posterior correctness unless Phase 4 explicitly
predeclared a sufficient evidence criterion and the result satisfies it.
Do not treat acceptance rate or sample summaries as promotion evidence beyond
the hard-veto screen. Do not treat `not_exposed_by_kernel` divergence status as
zero divergences. Do not run a CPU-hidden substitute for this phase.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 6 after result artifact and review converge, regardless of
pass/fail, unless a human-required blocker appears.

## Stop Conditions

Stop on invalid artifact, corrupted run, missing required diagnostic, post-hoc
criterion pressure, unapproved runtime boundary, or review nonconvergence.
Stop rather than repair in place if the exact command cannot launch after
approval; a smaller diagnostic requires a revised subplan.
