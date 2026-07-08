# Review Bundle: Minimal SSL-LSTM Zhao-Cui HMC Next Phase 4/5

Date: 2026-07-06

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex is supervisor and executor. Claude review was blocked earlier by the
private-context approval boundary, so this is a fresh visible Codex substitute
review.

## Review Scope

Review the compact Phase 4/5 plan and harness summary below for consistency,
correctness, feasibility, artifact coverage, and boundary safety.

Primary artifacts:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase4-longer-diagnostics-design-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase4-longer-diagnostics-design-result-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase5-longer-diagnostics-execution-subplan-2026-07-06.md`
- `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py`
- `tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py`

Context:

- Phase 1 extracted the internal minimal scalar target adapter with no behavior
  drift versus the predecessor benchmark artifact.
- Phase 2 CPU-hidden regression passed.
- Phase 3 trusted GPU/XLA smoke passed with `use_xla=True`, `jit_compile=True`,
  visible GPU provenance, finite samples, and no hard vetoes.
- Phase 3 native divergence status was `not_exposed_by_kernel`; this must not
  be interpreted as zero divergences.

## Evidence Contract To Audit

| Field | Contract |
| --- | --- |
| Question | Does the minimally longer trusted GPU/XLA ladder avoid hard runtime/sampler vetoes under fixed settings? |
| Baseline/comparator | Phase 3 trusted GPU/XLA smoke as runtime baseline; Phase 2 CPU regression only as non-GPU debug context. |
| Primary pass criterion | All three predeclared seeds complete with valid artifacts, GPU provenance, `use_xla=True`, `jit_compile=True`, finite samples, and no hard vetoes. |
| Veto diagnostics | Runtime exception, hidden/missing GPU, missing approval, nonfinite target/sample, invalid artifact, missing diagnostic/provenance, positive native divergence if exposed, post-hoc criterion change, unsupported ranking/convergence/default claim, or review nonconvergence. |
| Explanatory diagnostics | Acceptance, runtime, sample shape, finite counts, sample mean/std/min/max, per-seed rows, TensorFlow logs, TF32/XLA metadata, and native divergence availability status when not positive. ESS/R-hat are not computed. |
| Not concluded | HMC convergence, posterior correctness, ranking/superiority, default readiness, production readiness, public API/package readiness, source-faithful parity, LEDH result, or broad scientific validity. |

## Fixed Phase 5 Runtime Settings

| Setting | Value |
| --- | --- |
| Harness mode | `phase5-longer-gpu-xla-ladder` |
| Device boundary | `CUDA_VISIBLE_DEVICES=0` |
| HMC seeds | `(20260706, 5101)`, `(20260706, 5102)`, `(20260706, 5103)` |
| `num_results` | `8` |
| `num_burnin_steps` | `4` |
| `step_size` | `1e-5` |
| `num_leapfrog_steps` | `1` |
| Prior scale | `5.0` |
| Initial offset scale | `1e-3` |
| `use_xla` / `jit_compile` | `True` / `True` |
| Chain execution mode | `tf_function` |
| Trace policy | `standard` |
| Adaptation policy | `fixed_kernel_no_adaptation` |

Reviewed runtime command pending explicit approval:

```bash
CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py --mode phase5-longer-gpu-xla-ladder --trusted-gpu-xla-approval --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.md --num-results 8 --num-burnin-steps 4 --step-size 1e-5 --num-leapfrog-steps 1 > docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_next_2026-07-06/phase5_longer_gpu_xla_ladder_2026-07-06.log 2>&1
```

## Harness/Test Summary

The Phase 5 harness mode:

- requires `--trusted-gpu-xla-approval`;
- rejects `--seed` and `--ladder-seeds`;
- rejects drift in `num_results`, burnin, step size, and leapfrog count;
- records per-seed rows and top-level hard-veto summary;
- classifies native divergence count as hard veto only when available and
  positive;
- records `not_exposed_by_kernel` as telemetry unavailability, not zero
  divergences;
- marks acceptance/runtime/sample summaries as explanatory only;
- records ESS/R-hat as not computed;
- preserves nonclaims against convergence, posterior correctness, ranking,
  default readiness, production readiness, source-faithful parity, public API
  readiness, and LEDH.

Checks already run before review:

- Compile check passed.
- CPU-hidden focused pytest returned `18 passed`.
- `git diff --check` passed.
- Forbidden implementation scan found no `GradientTape`, `tf.py_function`,
  `import numpy`, or `np.` in the target module/harness.
- Claim-boundary scan found only explicit nonclaims / forbidden-claim text.

## Round 1 Substitute Review Result And Repair

Fresh visible Codex substitute review returned `VERDICT: REVISE`.

Blocking finding:

- The Phase 5 plan fixed `prior_scale=5.0` and
  `initial_offset_scale=1e-3`, but the harness/CLI did not reject overrides for
  those two settings.

Minor finding:

- The Phase 4 design subplan had stale comparator wording that did not put
  Phase 3 trusted GPU/XLA smoke first as the immediate runtime baseline.

Repair applied:

- The harness now defines Phase 5 constants for prior scale and initial offset
  scale and rejects drift in both the builder and CLI.
- Tests now cover builder-level and CLI-level rejection of those overrides.
- The Phase 4 design subplan comparator wording now matches the Phase 4 result,
  Phase 5 subplan, and this review bundle.

Focused re-review should verify that these two findings are resolved and that
no new boundary drift was introduced.

## Specific Review Questions

1. Is Phase 3, not Phase 2, correctly used as the immediate GPU/XLA baseline?
2. Does the plan avoid treating acceptance/runtime/sample summaries as
   convergence, posterior, ranking, default-readiness, or production-readiness
   evidence?
3. Is native divergence unavailability handled conservatively?
4. Are the fixed seeds/settings and CLI rejection rules sufficient to prevent
   post-hoc drift?
5. Are artifact paths and result/closeout handoff conditions recoverable after
   interruption?
6. Does the plan avoid public API/default-policy/model-file/source-faithfulness
   boundaries?
7. Is there any material blocker before requesting explicit GPU/XLA runtime
   approval?

Findings first. End with exactly:

VERDICT: AGREE

or

VERDICT: REVISE
