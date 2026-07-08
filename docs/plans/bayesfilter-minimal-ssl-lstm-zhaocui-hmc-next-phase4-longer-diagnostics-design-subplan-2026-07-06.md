# Phase 4 Subplan: Longer Sampler-Diagnostics Ladder Design

Date: 2026-07-06

Status: `READY_FOR_DESIGN_EXECUTION`

## Phase Objective

Design a longer sampler-diagnostics ladder using the extracted internal target,
with predeclared diagnostic roles, uncertainty limits, and stop conditions
before any longer run is launched.

## Entry Conditions Inherited From Previous Phase

- Phase 3 passed or was explicitly deferred with a human-accepted boundary
  decision.
- The reusable internal target and CPU regression remain valid.
- Phase 3 runtime artifact is available at
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase3_gpu_xla_smoke_2026-07-06.json`
  and records `use_xla=True`, `jit_compile=True`, visible GPU provenance, and
  no hard vetoes.

## Required Artifacts

- Phase 4 result/design record.
- Draft Phase 5 execution subplan with exact commands, seeds, budgets,
  artifacts, and evidence roles.
- Review bundle for Phase 5.
- Focused harness/test edits, if needed, to make the Phase 5 command an exact
  fail-closed reviewed mode rather than an ad hoc CLI invocation.

## Required Checks, Tests, Reviews

- Skeptical plan audit.
- Evidence contract and research intent ledger.
- Material review of Phase 5 before execution.
- Local compile/test checks for any Phase 5 harness/test edits.
- Artifact-path existence checks for Phase 3 predecessor evidence.

## Skeptical Plan Audit

This Phase 4 design survives the skeptical audit only if the Phase 5 plan:

- uses the Phase 3 trusted GPU/XLA smoke as the immediate runtime baseline, not
  the older CPU-hidden debug ladder as GPU evidence;
- treats acceptance, runtime, sample means/spreads, and per-seed differences as
  explanatory only;
- records native divergence as a hard veto only when a native divergence count
  is exposed and positive;
- says explicitly that `not_exposed_by_kernel` is not zero divergences;
- avoids R-hat/ESS language unless those diagnostics are actually computed and
  predeclared;
- uses fixed seeds, fixed budgets, fixed step size, and fixed leapfrog count;
- writes JSON, Markdown, and quiet log artifacts under the reviewed paths;
- asks for trusted GPU/XLA runtime approval before launch.

Audit result: `PASS_FOR_DESIGN`. The plan is design-only and does not run the
longer sampler.

## Research Intent Ledger

| Field | Ledger |
| --- | --- |
| Main question | Can a minimally longer trusted GPU/XLA HMC diagnostic ladder over the scalar `zhaocui_fixed` target avoid hard runtime/sampler vetoes under fixed settings? |
| Candidate/mechanism under test | Existing internal `MinimalZhaoCuiHMCTargetAdapter` through `run_full_chain_tfp_hmc` with fixed-kernel, no-adaptation HMC and XLA enabled. |
| Expected failure mode | CUDA/XLA runtime failure, nonfinite target or samples, hidden GPU context, invalid artifact, or positive native divergence if exposed. |
| Promotion criterion | Phase 5 artifact completes all predeclared seeds with no hard vetoes and preserves evidence limits. |
| Promotion veto | Any hard veto in the Phase 5 artifact; promotion means only "viable for future validation", not convergence or readiness. |
| Continuation veto | Invalid artifact, missing required diagnostics/provenance, unapproved runtime boundary, or unsupported claim pressure. |
| Repair trigger | Runtime exception, nonfinite samples, missing provenance, or fail-closed harness rejection triggers a smaller diagnostic or plan repair rather than a scientific rejection. |
| Explanatory diagnostics | Acceptance rate, runtime, sample shape, finite counts, initial target value/score, device list, TF32/XLA metadata, and TensorFlow logs. |
| Must not conclude | HMC convergence, posterior correctness, ranking/superiority, default readiness, production readiness, source-faithful Zhao-Cui parity, public API/package readiness, or LEDH result. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the smallest longer diagnostic ladder that can answer a sampler-mechanics question without promoting descriptive metrics into convergence or ranking evidence? |
| Baseline/comparator | Phase 3 trusted GPU/XLA smoke as immediate runtime baseline, Phase 2 CPU regression only as non-GPU debug context, and predecessor short ladder as mechanics context. |
| Primary pass criterion | Phase 5 subplan predeclares exact settings, artifacts, hard vetoes, explanatory diagnostics, nonclaims, and stop conditions. |
| Veto diagnostics | Missing exact commands/artifacts, post-hoc thresholds, descriptive metrics used for ranking, missing inference-status table, or unapproved long-run boundary. |
| Explanatory diagnostics | Proposed chain lengths, seeds, runtime budget, ESS/R-hat roles if computed, acceptance roles, and wall-time estimate. |
| Not concluded | Any sampler result; this is design only. |

## Phase 5 Design Fixed By This Phase

Phase 5 must use a dedicated harness mode named
`phase5-longer-gpu-xla-ladder` with these fixed settings:

| Setting | Value |
| --- | --- |
| Device boundary | `CUDA_VISIBLE_DEVICES=0` with explicit trusted GPU/XLA approval |
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

The exact Phase 5 runtime command, after review and approval, is:

```bash
CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py --mode phase5-longer-gpu-xla-ladder --trusted-gpu-xla-approval --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.md --num-results 8 --num-burnin-steps 4 --step-size 1e-5 --num-leapfrog-steps 1 > docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_next_2026-07-06/phase5_longer_gpu_xla_ladder_2026-07-06.log 2>&1
```

The command intentionally omits `--seed` and `--ladder-seeds`; the harness mode
must use only the predeclared Phase 5 seed tuple and reject drift.

## Forbidden Claims And Actions

Do not run the longer sampler in Phase 4. Do not claim convergence,
posterior correctness, ranking, default readiness, or production readiness.
Do not reinterpret Phase 2 CPU-hidden results as GPU evidence. Do not treat
native divergence unavailability as zero divergences.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 5 only if the execution subplan converges under review and
the user approves any required long-run/runtime boundary.

## Stop Conditions

Stop if a defensible evidence contract cannot be written, review does not
converge after five rounds, or the long-run boundary is not approved.
