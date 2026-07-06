# Actual-SIR Nystrom Compiled-Redo P09B Rescue Tuning Plan

Date: 2026-06-23

Status: `READY_TO_LAUNCH_SEQUENTIAL_DIAGNOSTIC`

## Purpose

P09 exposed two sensitivity failures:

- `rank=16,epsilon=1.0` failed paired thresholds.
- `rank=32,epsilon=0.25` produced nonfinite Nystrom outputs.

This diagnostic tests whether the `rank=32,epsilon=0.25` failure is a
tuning/stabilization problem.  It is not promotion evidence and does not change
default policy by itself.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can the failing `rank=32,epsilon=0.25` setting be rescued by rank, epsilon floor, jitter, denominator floor, or smaller-N behavior while holding the model and seeds fixed? |
| Candidate/mechanism under test | Nystrom numerical/tuning policy: rank, kernel epsilon, Cholesky jitter, denominator floor. |
| Baseline/comparator | Compiled streaming TF32 route for paired rows. |
| Base failing row | `B=5,T=20,N=1024,D=18,M=9`, seeds `81920..81924`, `rank=32,epsilon=0.25`. |
| Expected failure mode | Reproduce nonfinite Nystrom factors/particles/log-likelihood at the base failing setting. |
| Primary diagnostic criterion | A rescue setting is viable if it reports `status=PASS`, `hard_vetoes=[]`, finite factors/particles, and paired max/mean log-likelihood deltas within thresholds. |
| Promotion criterion | None. P09B can only classify a repair path. |
| Promotion veto | Any attempt to use P09B as default-readiness or superiority evidence. |
| Continuation veto | Artifact write failure, GPU unavailable, harness/schema failure, or inability to reproduce/diagnose due to environment failure. Expected candidate failures are repair evidence, not continuation vetoes. |
| Repair trigger | Any rescue setting that passes suggests a narrowed policy or numerical-stability repair; all rescue settings failing suggests deeper instability. |
| Explanatory diagnostics | Per-seed deltas, residuals, finite-factor flags, runtime, memory, rescue setting. |
| What must not be concluded | No default readiness, no statistical ranking, no posterior correctness, no HMC readiness, no proof that one setting is superior. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the P09 failure a tunable/stabilizable numerical issue? |
| Exact baseline | Compiled streaming TF32 route with same model, seeds, GPU, dtype, and transport policy. |
| Pass/fail criterion | Each row is classified as `PASS_RESCUE`, `FAIL_REPRODUCED`, `FAIL_QUALITY`, `FAIL_NUMERIC`, or `ENV_BLOCKER` from artifact fields. |
| Veto diagnostics | Nonfinite factors/particles/log-likelihood, paired threshold failures, missing GPU/TF32/JIT evidence, artifact mismatch. |
| Explanatory-only diagnostics | Runtime, warm ratio, memory, residual magnitudes below threshold. |
| Not concluded | No default promotion, no candidate ranking, no broad robustness claim. |
| Artifacts | `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09b-*.json/md` and this result prefix. |

## Skeptical Pre-Launch Audit

Status: `PASS_FOR_P09B_RESCUE_DIAGNOSTIC`

The plan holds model, seeds, comparator, and thresholds fixed where possible.
It does not lower the paired thresholds after seeing the failure.  It separates
expected candidate failures from continuation vetoes.  It does not use
quarantined Python-loop timing artifacts.  Runtime remains descriptive.

## Diagnostic Rows

Rows use `B=5,T=20,N=1024`, seeds `81920..81924`, route `both`, active-all,
float32, TF32 enabled, JIT enabled, unless noted.

| Row | Purpose | N | Rank | Epsilon | Jitter | Denominator floor |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| reproduce | Reproduce failing base row | `1024` | `32` | `0.25` | `1e-8` | `1e-30` |
| rank64 | Rank rescue | `1024` | `64` | `0.25` | `1e-8` | `1e-30` |
| rank128 | Rank rescue | `1024` | `128` | `0.25` | `1e-8` | `1e-30` |
| eps0p3 | Epsilon boundary | `1024` | `32` | `0.3` | `1e-8` | `1e-30` |
| eps0p375 | Epsilon boundary | `1024` | `32` | `0.375` | `1e-8` | `1e-30` |
| jitter1e-7 | Stabilization | `1024` | `32` | `0.25` | `1e-7` | `1e-30` |
| jitter1e-6 | Stabilization | `1024` | `32` | `0.25` | `1e-6` | `1e-30` |
| jitter1e-5 | Stabilization | `1024` | `32` | `0.25` | `1e-5` | `1e-30` |
| floor1e-24 | Stabilization | `1024` | `32` | `0.25` | `1e-8` | `1e-24` |
| floor1e-18 | Stabilization | `1024` | `32` | `0.25` | `1e-8` | `1e-18` |
| floor1e-12 | Stabilization | `1024` | `32` | `0.25` | `1e-8` | `1e-12` |
| smallN256 | Smaller-N pathology check | `256` | `32` | `0.25` | `1e-8` | `1e-30` |
| smallN512 | Smaller-N pathology check | `512` | `32` | `0.25` | `1e-8` | `1e-30` |

## Automatic Execution Rule

Run every diagnostic row unless a continuation veto fires.  Candidate failures
are expected evidence and should not stop the diagnostic.  Stop only for
environment/artifact/harness failure.
