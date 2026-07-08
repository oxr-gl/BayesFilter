# Review Bundle: Minimal SSL-LSTM Zhao-Cui HMC Next Phase 5 Result

Date: 2026-07-06

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

## Review Scope

Review the compact Phase 5 result summary below for consistency, correctness,
artifact coverage, and boundary safety.

Primary artifacts:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase5-longer-diagnostics-execution-result-2026-07-06.md`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase6-closeout-subplan-2026-07-06.md`

Context:

- Phase 5 plan review initially returned `VERDICT: REVISE` for missing fixed
  guards on prior scale and initial offset scale.
- The repair added guards/tests and focused re-review returned
  `VERDICT: AGREE`.
- The exact reviewed trusted GPU/XLA command was approved and run.

## Evidence Contract To Audit

| Field | Contract |
| --- | --- |
| Question | Does the longer predeclared ladder avoid hard sampler/runtime vetoes and what, if anything, remains viable for future validation? |
| Baseline/comparator | Phase 3 trusted GPU/XLA smoke, Phase 2 CPU regression only as non-GPU debug context, and the Phase 4 reviewed design. |
| Primary pass criterion | The predeclared three-seed ladder completes, required artifacts are valid, all rows record `use_xla=True`/`jit_compile=True` with GPU provenance, and no hard vetoes are observed. |
| Veto diagnostics | Runtime exception, hidden/missing GPU, missing approval, nonfinite target/sample, invalid artifact, missing required diagnostic/provenance, positive native divergence if exposed, post-hoc criterion change, unsupported ranking/convergence/default claim, or review nonconvergence. |
| Explanatory diagnostics | Acceptance, runtime, sample shape, finite counts, sample summaries, per-seed rows, TensorFlow logs, and native divergence availability status when not positive. ESS/R-hat are not computed. |
| Not concluded | HMC convergence, posterior correctness, ranking/superiority, default readiness, production readiness, public API/package readiness, source-faithful parity, LEDH result, or broad scientific validity. |

## Result Summary

| Field | Value |
| --- | --- |
| Artifact status | `passed` |
| Hard vetoes | `[]` |
| All predeclared seeds passed | `true` |
| Seeds | `[20260706, 5101]`, `[20260706, 5102]`, `[20260706, 5103]` |
| Sample shape | `[8, 24]` for all three seeds |
| Samples finite | `true` for all three seeds |
| GPU provenance | `CUDA_VISIBLE_DEVICES=0`, GPU `/physical_device:GPU:0` |
| XLA/JIT | `use_xla=True`, `jit_compile=True` |
| TF32 | `true` |
| Acceptance rates | `1.0`, `1.0`, `1.0`; explanatory only |
| Native divergence status | `not_exposed_by_kernel`; explicitly not zero divergences |
| ESS/R-hat | Not computed |

## Checks Already Run

- Runtime command exited with status 0.
- JSON artifact validated with `python -m json.tool`.
- `git diff --check` passed after runtime and result writing.
- Claim-boundary scan hit only explicit nonclaims / forbidden-claim text.

## Specific Review Questions

1. Does the Phase 5 result match the artifact status and hard-veto fields?
2. Does it avoid promoting acceptance, runtime, sample summaries, or the
   three-seed hard-veto pass into convergence, posterior correctness, ranking,
   default readiness, or production readiness?
3. Is `not_exposed_by_kernel` native divergence status treated conservatively?
4. Are run manifest and artifact paths sufficient for recovery?
5. Is the Phase 6 handoff appropriate, or is a result repair needed first?

Findings first. End with exactly:

VERDICT: AGREE

or

VERDICT: REVISE
