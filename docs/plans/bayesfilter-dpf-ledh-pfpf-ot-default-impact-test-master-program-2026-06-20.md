# BayesFilter DPF LEDH-PFPF-OT Default Impact Test Master Program - 2026-06-20

## Status

`COMPLETED_P06_OPERATIONAL_VIABILITY_SUPPORTED_WITH_NONCLAIMS`

## Objective

Test whether the promoted GPU-oriented LEDH-PFPF-OT TF32 default helps the LEDH
filter in the narrow engineering sense: finite execution, preserved fixed-branch
accounting, tolerable precision drift screens, trusted GPU placement, bounded
memory/runtime evidence, and tiny CPU-hidden HMC-facing mechanics hard-veto
screening.

This program does not prove posterior correctness, HMC readiness, statistical
superiority, dense Sinkhorn equivalence, or public API readiness.

## Research Intent Ledger

| Field | Ledger |
| --- | --- |
| Main question | Does the promoted GPU TF32 LEDH-PFPF-OT default remain viable when tested through a staged LEDH filter ladder? |
| Candidate/mechanism | Streaming/chunked GPU LEDH-PFPF-OT route with `float32` tensors and TensorFlow TF32 execution enabled. |
| Expected failure mode | TF32/default route may be finite and GPU placed but show unacceptable drift, CPU fallback, memory failure at target shapes, or nonfinite HMC mechanics. |
| Promotion criterion | The route passes each hard screen through the final completed phase without reinterpreting descriptive timing or short-chain diagnostics as scientific proof. |
| Promotion veto | Nonfinite outputs, device mismatch in trusted GPU phases, missing required artifacts, stale/default metadata mismatch, or failed phase-specific hard screens. |
| Continuation veto | Broken harness, corrupted artifacts, criteria changed after seeing results, untrusted GPU evidence used as GPU evidence, or Claude/Codex non-convergence after five rounds on the same blocker. |
| Repair trigger | Fixable artifact/schema/metadata mismatch, command typo, stale title/nonclaim, or too-broad Claude prompt. |
| Explanatory diagnostics | Runtime, memory, drift magnitudes, acceptance rate, log-accept values, and compile times unless a phase explicitly assigns them hard-screen roles. |
| Must not conclude | Posterior correctness, HMC readiness, sampler convergence, statistical superiority, dense Sinkhorn equivalence, public API readiness, or low-rank lane rejection. |

## Phase Index

| Phase | Name | Subplan | Result |
| --- | --- | --- | --- |
| P00 | Governance, runbook, and review lock | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p00-governance-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p00-governance-result-2026-06-20.md` |
| P01 | Small deterministic correctness gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p01-correctness-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p01-correctness-result-2026-06-20.md` |
| P02 | Trusted GPU precision drift screen | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p02-precision-gpu-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p02-precision-gpu-result-2026-06-20.md` |
| P03 | Target-shape trusted GPU smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p03-target-gpu-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p03-target-gpu-result-2026-06-20.md` |
| P04 | Performance and memory interpretation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p04-performance-memory-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p04-performance-memory-result-2026-06-20.md` |
| P05 | Tiny HMC mechanics smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p05-hmc-mechanics-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p05-hmc-mechanics-result-2026-06-20.md` |
| P06 | Final synthesis and handoff | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p06-closeout-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-result-2026-06-20.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the promoted default help the LEDH filter enough to remain the engineering default for follow-on validation? |
| Baseline/comparator | Existing FP64/reference arms, FP32-no-TF32 arms, pre-promotion metadata/result artifacts, and phase-local previous rung. |
| Primary pass criterion | Each executed phase passes its hard screens and preserves artifacts, boundaries, and next subplan review. |
| Veto diagnostics | Nonfinite outputs, GPU placement mismatch in trusted GPU phases, metadata contradicting `production_ledh_pfpf_ot_gpu_tf32`, missing artifacts, failed correctness gate, or unsupported scientific/default-policy overclaim. |
| Explanatory diagnostics | Runtime, memory, drift magnitudes, compile time, warm-call timing, HMC acceptance/log-accept values, and historical artifact comparisons. |
| Not concluded | No posterior correctness, HMC readiness, statistical ranking, broad speedup claim, dense Sinkhorn equivalence, public API readiness, or low-rank lane rejection. |
| Artifacts | This master program, visible runbook, execution ledger, Claude review ledger, phase subplans/results, benchmark JSON/MD artifacts, and logs where commands are quieted. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| GPU TF32 default route | `AGENTS.md`, `CLAUDE.md`, `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-gpu-tf32-production-default-result-2026-06-20.md` | Owner directive made this the DPF transport default. | Treating directive as proof of correctness. | P00 review and nonclaim checks. | reviewed target |
| Existing benchmark harnesses | `docs/benchmarks/*ledh_pfpf_ot*` | Avoids inventing new harnesses before proving a gap. | Harness may not answer target question. | P00/P01 skeptical audit. | baseline |
| Trusted GPU phases use `/GPU:0` | Existing fresh default smoke artifact | Prior trusted smoke placed outputs on GPU:0. | GPU unavailable/busy or sandbox failure. | Trusted-context command with explicit device checks. | hypothesis |
| Target shape starts bounded before larger evidence | Prior capacity artifacts and current uncertainty | Prevents an immediate long run from masking harness defects. | Bounded smoke passes but realistic shape fails. | P03/P04 runged target-shape artifacts. | planned |
| HMC mechanics is tiny hard-veto only | Existing HMC mechanics harness and policy | Short HMC can catch nonfinite mechanics but not convergence. | Acceptance metrics are overinterpreted. | P05 evidence contract. | planned |

## Skeptical Plan Audit

- Wrong baseline: avoided by keeping FP64/reference and FP32-no-TF32 arms as
  comparators, not production defaults.
- Proxy metrics: timing, memory, drift, and HMC acceptance are descriptive
  unless a phase explicitly uses finiteness/device/artifact presence as a hard
  veto.
- Missing stop conditions: each phase subplan must include artifact, hard veto,
  review, and handoff stops.
- Unfair comparison: no speed ranking is inferred from single runs.
- Hidden assumptions: GPU evidence must be trusted; CPU-only checks cannot
  certify GPU placement.
- Stale context: dirty HMC and low-rank peer files are not part of this lane and
  must not be reverted or claimed.
- Artifact mismatch: every result must cite its actual command and generated
  artifacts.

Audit status: P00 passed after Claude read-only review; later phases must run
their own phase-local skeptical audit before execution.

## Repair Loop

For material Claude findings, Codex patches the same artifact visibly, reruns
focused checks, and repeats read-only Claude review up to five rounds for the
same blocker. Claude is not an execution authority and cannot authorize crossing
human, runtime, model-file, funding, product-capability, default-policy, or
scientific-claim boundaries.
