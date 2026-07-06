# Actual-SIR Nystrom Fixed-Policy Validation Plan

Date: 2026-06-23

Status: `READY_TO_LAUNCH_P01_FIXED_POLICY_CONFIRMATION`

## Research Intent Ledger

| Field | Plan |
| --- | --- |
| Main question | Does the restricted fixed Nystrom policy `rank=32,epsilon=0.5`, raw kernel, default scaling normalization `none`, remain viable on the serious actual-SIR row after the balanced-scaling repair lane closed? |
| Candidate/mechanism | Fixed policy only: `--nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-kernel-mode raw --nystrom-scaling-normalization none`. |
| Expected failure mode | Nonfinite factors/particles/log likelihood, residual hard veto, paired likelihood drift, missing GPU/TF32 evidence, or selected-policy metadata missing. |
| Promotion criterion | This lane has no default-promotion criterion. Passing P01 only makes the fixed policy viable for a later restricted-policy stress program. |
| Promotion veto | Any claim of default readiness, broad rank/epsilon robustness, superiority, posterior correctness, or HMC readiness. |
| Continuation veto | Invalid/missing artifact, trusted GPU unavailable, missing selected-policy metadata, threshold drift, or P01 hard-veto failure. |
| Repair trigger | If fixed `rank=32,epsilon=0.5` fails under this confirmation, stop and classify the fixed policy as not currently viable. |
| Explanatory diagnostics | Runtime, residuals, paired deltas, denominator/factor/scaling diagnostics. |
| What must not be concluded | No default readiness, no broad robust policy, no statistical ranking, no posterior correctness, no HMC readiness. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Is the restricted fixed policy still viable on the serious actual-SIR comparator row with current code? |
| Exact baseline/comparator | Compiled streaming TF32 actual-SIR route in the same artifact. |
| Primary pass/fail criterion | Aggregate artifact `status == PASS`: finite GPU outputs, no Nystrom residual veto, paired max delta <= `10.0`, paired mean delta <= `5.0`, trusted GPU/TF32 evidence present, fixed-policy metadata present. |
| Veto diagnostics | Any aggregate hard veto, missing GPU/TF32 evidence, missing fixed-policy metadata, threshold drift, nonfinite outputs, row/column residual threshold failure, paired threshold failure, missing artifact. |
| Explanatory only | Runtime, warm timing ratio, factor/scaling ranges, denominator floor hits, spectrum diagnostics. |
| Not concluded if pass | No default readiness, no superiority/ranking, no broad rank/epsilon robustness, no posterior correctness, no HMC readiness. |
| Artifact preserving result | P01 JSON/Markdown/log plus result note. |

## Skeptical Plan Audit

Wrong-baseline risk: comparing fixed Nystrom to prior artifacts only would miss
current-code drift.  Mitigation: rerun streaming and fixed Nystrom in one
compiled paired artifact.

Proxy-promotion risk: one serious row passing could be mistaken for default
readiness.  Mitigation: primary criterion is fixed-policy viability only; stress
and uncertainty are separate future gates.

Hidden tuning risk: the fixed policy was chosen after observing failures.
Mitigation: this plan labels it as restricted fixed-policy validation, not broad
policy optimization or default promotion.

Environment risk: GPU failures can be sandbox artifacts.  Mitigation: trusted
GPU preflight and GPU/TF32 manifest are mandatory.

Audit status: `PASS_READY_TO_RUN_P01`.

## P01 Fixed-Policy Confirmation Command

Use physical GPU1 if available, otherwise GPU0.  In the command, replace
`<GPU_ID>` and `<GPU_NOTE>` from trusted preflight.

```bash
python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py \
  --route both \
  --batch-seeds 81920,81921,81922,81923,81924 \
  --time-steps 20 \
  --num-particles 1024 \
  --transport-policy active-all \
  --sinkhorn-iterations 10 \
  --sinkhorn-epsilon 1.0 \
  --annealed-scaling 0.9 \
  --annealed-convergence-threshold 0.001 \
  --row-chunk-size 1024 \
  --col-chunk-size 1024 \
  --particle-chunk-size 1024 \
  --nystrom-diagnostics \
  --nystrom-rank 32 \
  --nystrom-epsilon 0.5 \
  --nystrom-max-iterations 160 \
  --nystrom-convergence-threshold 0.0001 \
  --nystrom-kernel-mode raw \
  --nystrom-scaling-normalization none \
  --history-mode value-only \
  --warmups 0 \
  --repeats 1 \
  --dtype float32 \
  --tf32-mode enabled \
  --jit-compile \
  --device-scope visible \
  --cuda-visible-devices <GPU_ID> \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --selected-physical-gpu <GPU_ID> \
  --gpu-selection-note "<GPU_NOTE>" \
  --phase-id ACTUAL-SIR-NYSTROM-FIXED-POLICY-P01-R32-EPS0P5 \
  --quiet \
  --output docs/benchmarks/actual-sir-nystrom-fixed-policy-p01-r32-eps0p5-2026-06-23.json \
  --markdown-output docs/benchmarks/actual-sir-nystrom-fixed-policy-p01-r32-eps0p5-2026-06-23.md
```

## Stop Conditions

Stop after P01 if:

- trusted GPU is unavailable;
- artifact is missing/invalid;
- aggregate hard veto fires;
- selected-policy metadata is missing;
- continuing would require changing thresholds or broadening the policy.

If P01 passes, write a result recommending a separate fixed-policy stress
runbook rather than launching unplanned stress gates inside this plan.
