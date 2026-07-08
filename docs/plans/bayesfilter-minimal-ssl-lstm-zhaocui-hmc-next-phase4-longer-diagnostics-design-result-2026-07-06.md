# Phase 4 Result: Longer Sampler-Diagnostics Ladder Design

Date: 2026-07-06

Status: `COMPLETE_AWAITING_PHASE5_REVIEW_APPROVAL`

## Phase Objective

Design a longer sampler-diagnostics ladder using the extracted internal target,
with predeclared diagnostic roles, uncertainty limits, exact commands, and stop
conditions before any longer run is launched.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the smallest longer diagnostic ladder that can answer a sampler-mechanics hard-veto question without promoting descriptive metrics into convergence or ranking evidence? |
| Baseline/comparator | Phase 3 trusted GPU/XLA smoke as immediate runtime baseline, Phase 2 CPU regression only as non-GPU debug context, predecessor short ladder as mechanics context. |
| Primary pass criterion | Phase 5 subplan predeclares exact settings, artifacts, hard vetoes, explanatory diagnostics, nonclaims, stop conditions, and approval boundary. |
| Veto diagnostics | Missing exact command/artifacts, post-hoc thresholds, descriptive metrics used for ranking, missing inference-status table, unapproved GPU/XLA runtime boundary, or native divergence unavailability treated as zero divergences. |
| Explanatory diagnostics | Chain length, seeds, runtime budget, acceptance roles, sample summaries, wall-time estimate, TF32/XLA provenance, and native divergence availability status. |
| Not concluded | Any sampler result; Phase 4 is design only. |

## Design Fixed For Phase 5

Phase 5 must use dedicated harness mode `phase5-longer-gpu-xla-ladder`.

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

Reviewed runtime command, pending approval:

```bash
CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py --mode phase5-longer-gpu-xla-ladder --trusted-gpu-xla-approval --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.md --num-results 8 --num-burnin-steps 4 --step-size 1e-5 --num-leapfrog-steps 1 > docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_next_2026-07-06/phase5_longer_gpu_xla_ladder_2026-07-06.log 2>&1
```

## Harness/Test Preparation

Updated:

- `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py`
- `tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py`

The harness now has a fail-closed Phase 5 mode that:

- fixes Phase 5 seeds and rejects `--seed` / `--ladder-seeds`;
- rejects changed `num_results`, burnin, step size, or leapfrog count;
- requires `--trusted-gpu-xla-approval`;
- records GPU/XLA provenance, `use_xla=True`, `jit_compile=True`, TF32 status,
  device summary, exact seeds, and quiet log path;
- treats native divergence as a hard veto only when exposed and positive;
- records native divergence unavailability as uncertainty, not zero
  divergences;
- classifies acceptance, runtime, sample summaries, and seed differences as
  explanatory only;
- records that ESS/R-hat are not computed in this modest ladder.

## Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Compile | `PASSED` | `python -m compileall -q bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py tests/test_ssl_lstm_zhaocui_hmc_minimal.py tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py` |
| Focused pytest | `PASSED` | `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 pytest -q tests/test_ssl_lstm_zhaocui_hmc_minimal.py tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py` returned `18 passed`. |
| `git diff --check` | `PASSED` | No whitespace errors. |
| Forbidden implementation scan | `PASSED` | No `GradientTape`, `tf.py_function`, `import numpy`, or `np.` in the target module/harness scan. |
| Claim-boundary scan | `PASSED` | Hits were explicit nonclaims / forbidden-claim text only. |
| Phase 3 artifact existence | `PASSED` | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase3_gpu_xla_smoke_2026-07-06.json` exists. |

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | `NOT_RUN_IN_PHASE4` |
| Statistically supported ranking | `NOT_CLAIMED` |
| Descriptive-only differences | Phase 5 will treat acceptance, runtime, and sample summaries as explanatory only. |
| Default-readiness | `NOT_CHECKED` |
| Next evidence needed | Phase 5 reviewed runtime execution, then result review and closeout. |

## Decision Table

| Field | Decision |
| --- | --- |
| Phase decision | `PASS_PHASE4_DESIGN_ADVANCE_TO_PHASE5_REVIEW_APPROVAL` |
| Primary criterion status | `PASSED_DESIGN_ONLY` |
| Veto diagnostic status | `NO_PHASE4_DESIGN_HARD_VETO_OBSERVED` |
| Main uncertainty | Phase 5 has not run; the design can only control evidence roles and runtime boundaries. |
| Next justified action | Run material review of Phase 5 subplan and harness mode, then request trusted GPU/XLA runtime approval. |
| What is not being concluded | No HMC convergence, posterior correctness, ranking, default readiness, production readiness, source-faithful parity, public API/package readiness, or LEDH result. |

## Review Status

External Claude review remains unavailable due to the private-context transfer
approval denial recorded in Phase 0. The Phase 5 review will use a fresh visible
Codex read-only substitute reviewer and must converge before runtime launch.

### Substitute Review Round 1

Fresh visible Codex substitute review returned `VERDICT: REVISE`.

Findings:

- Phase 5 fixed-setting drift protection was incomplete because the plan fixed
  `prior_scale=5.0` and `initial_offset_scale=1e-3`, while the harness and CLI
  did not reject those overrides.
- Phase 4 design subplan had stale comparator wording that listed Phase 2
  before Phase 3 rather than Phase 3 as the immediate GPU/XLA baseline.

Repair:

- Added Phase 5 constants and builder/CLI guards for `prior_scale` and
  `initial_offset_scale`.
- Added tests for builder-level and CLI-level rejection of those overrides.
- Updated the Phase 4 comparator wording.

Focused checks and re-review are required before Phase 5 runtime approval.

### Focused Re-Review

Focused visible Codex substitute re-review returned `VERDICT: AGREE`.

Residual note:

- The compact review bundle settings table did not list prior scale and initial
  offset scale even though the repair section, Phase 4/5 plans, harness, and
  tests did. This was patched as a consistency update.
