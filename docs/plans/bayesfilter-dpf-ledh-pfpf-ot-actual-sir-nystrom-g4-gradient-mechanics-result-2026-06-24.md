# G4 Result: Nystrom-Specific Gradient Mechanics Gate

Date: 2026-06-24

Status: `G4_GRADIENT_MECHANICS_PASS`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Close G4 as passed for the tiny actual-SIR Nystrom gradient mechanics smoke. |
| Primary criterion status | `PASS`: command exited 0, JSON/Markdown artifacts exist, artifact reports finite scalar, non-`None` finite gradient, finite gradient norm, positive Nystrom route invocations, fixed-policy metadata, and CPU-hidden metadata. |
| Veto diagnostic status | `PASS`: no hard vetoes. |
| Main uncertainty | This is a tiny mechanics smoke only; it does not establish HMC readiness, sampler behavior, posterior correctness, or target-shape viability. |
| Next justified action | Draft G5 evidence-package/default-readiness review plan.  Any default decision still needs human review and must preserve the seed `82921` hard-case caveat. |
| What is not being concluded | No HMC readiness, no posterior convergence, no posterior correctness, no target-shape HMC viability, no default readiness, no statistical ranking, no acceptance of seed `82921`. |

## Evidence Summary

| Diagnostic | Value |
| --- | --- |
| Status | `PASS` |
| Hard vetoes | `[]` |
| Route under test | `actual_sir_nystrom` |
| Shape | `B=1,T=2,N=32,D=18,M=9` |
| Dtype / device | `float64`, CPU-hidden, `CUDA_VISIBLE_DEVICES=-1` |
| Scalar value | `-69.70620229788184` |
| Scalar finite | `True` |
| Gradient is `None` | `False` |
| Gradient finite | `True` |
| Gradient norm | `0.2716932645717483` |
| Gradient shape | `[1,32,18]` |
| Nystrom route invocations | `2` |
| Nystrom row residual | `2.6793091285615134e-05` |
| Nystrom column residual | `1.1102230246251565e-16` |

## Artifacts

- Script:
  `docs/benchmarks/run_actual_sir_nystrom_gradient_mechanics_smoke.py`
- JSON:
  `docs/benchmarks/actual-sir-nystrom-g4-gradient-mechanics-cpu-2026-06-24.json`
- Markdown:
  `docs/benchmarks/actual-sir-nystrom-g4-gradient-mechanics-cpu-2026-06-24.md`
- Log:
  `docs/plans/logs/actual-sir-nystrom-g4-gradient-mechanics-cpu-2026-06-24.log`

## Local Checks

- Syntax check for the new script: `PASS`.
- Focused CPU-hidden tests:
  `tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py`:
  `13 passed`.
- G4 JSON artifact audit: `PASS`.

The log contains an expected CUDA no-device line because the command
intentionally used `CUDA_VISIBLE_DEVICES=-1`; the artifact records CPU-hidden
execution with no logical or physical GPUs visible.

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | `PASS` for tiny Nystrom scalar/gradient mechanics. |
| Statistically supported ranking | None. |
| Descriptive-only differences | Scalar value, gradient norm, tiny shape, runtime. |
| HMC readiness | No. |
| Default-readiness | No. |
| Next evidence needed | G5 evidence package and human/default-scope review, with seed `82921` unresolved. |

## Post-Run Red-Team Note

Strongest alternative explanation: finite gradient mechanics at `T=2,N=32`
could still fail at target shape, inside real HMC trajectories, or under
parameter gradients instead of initial-particle gradients.

What would overturn this result: a rerun showing nonfinite scalar/gradient,
zero route invocations, missing CPU-hidden metadata, or unsupported claims in
the artifact.

Weakest part of evidence: it is intentionally a tiny mechanics screen, not HMC
sampling evidence.
