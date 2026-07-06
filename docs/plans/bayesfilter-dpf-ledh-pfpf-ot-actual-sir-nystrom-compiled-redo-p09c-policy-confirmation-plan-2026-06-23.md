# Actual-SIR Nystrom Compiled-Redo P09C Policy Confirmation Plan

Date: 2026-06-23

Status: `READY_TO_LAUNCH_SEQUENTIAL_GRID`

## Purpose

P09B identified `epsilon=0.25` as an unsafe epsilon floor and showed rescue at
`epsilon=0.3` and `0.375`.  P09C confirms a narrowed policy neighborhood before
continuing to P10 stress.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Does the policy neighborhood with `epsilon=0.25` excluded remain paired-comparable for the intended Nystrom route? |
| Candidate family | `rank in {32,64}`, `epsilon in {0.3,0.5}`. |
| Baseline/comparator | Compiled streaming TF32 route in the same process and selected physical GPU. |
| Shape | `B=5,T=20,N=1024,D=18,M=9`, seeds `81920..81924`. |
| Primary pass criterion | Every row writes JSON/Markdown with `status=PASS`, `hard_vetoes=[]`, finite Nystrom outputs, residuals pass, GPU/TF32/JIT evidence, and paired thresholds pass. |
| Promotion veto | Any row failure blocks P10 until repaired or policy is narrowed further with a reviewed rationale. |
| Continuation veto | Artifact/GPU/harness failure. |
| Repair trigger | Any failure in the narrowed policy neighborhood. |
| Explanatory diagnostics | Runtime, warm ratio, residuals below threshold, per-seed deltas. |
| What must not be concluded | No default readiness, no statistical ranking, no superiority, no posterior correctness, no HMC readiness. |

## Evidence Contract

Passing P09C supports continuing to P10 with a proposed admissible epsilon floor
of `>=0.3` and the existing intended default `rank=32,epsilon=0.5`.  It does
not finalize default policy.

## Skeptical Pre-Launch Audit

Status: `PASS_FOR_P09C_POLICY_CONFIRMATION`

This plan does not hide the `epsilon=0.25` failure; it explicitly excludes that
unsafe setting based on P09B evidence and tests the narrowed neighborhood with
the same seeds, comparator, model, dtype, thresholds, and artifact contract.

## Rows

| Row | Rank | Epsilon | Artifact suffix |
| --- | ---: | ---: | --- |
| 1 | `32` | `0.3` | `r32-eps0p3` |
| 2 | `32` | `0.5` | `r32-eps0p5` |
| 3 | `64` | `0.3` | `r64-eps0p3` |
| 4 | `64` | `0.5` | `r64-eps0p5` |

Output pattern:

- JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09c-policy-<suffix>-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09c-policy-<suffix>-2026-06-23.md`
