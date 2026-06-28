# Nystrom LEDH/PFPF-OT Effectiveness Leaderboard Plan

Date: 2026-06-22

Status: `PILOT_PLAN_READY`

## Purpose

Test whether the fixed-rank Nystrom LEDH/PFPF-OT diagnostic candidate is useful
as an effectiveness leaderboard candidate against the current streaming TF32
LEDH/PFPF-OT route.  This is a separate lane from the algorithm-complete
diagnostic lane: the completed Nystrom artifacts show that the candidate fires,
has bounded dense-reference drift on tiny fixtures, and scales on GPU; they do
not establish paired effectiveness, speedup, posterior correctness, or default
readiness.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Does the Nystrom route remain valid and descriptively resource-competitive against the streaming TF32 route on the same downstream LEDH/PFPF-OT fixture and GPU? |
| Candidate | Fixed-rank Nystrom kernel transport inside the LEDH/PFPF-OT filter loop. |
| Comparator | Current streaming TF32 LEDH/PFPF-OT route on the same fixture, same seed, same visible physical GPU, same TF32 state, and same row timeout. |
| Primary pilot criterion | For all required pilot rows, both routes complete without hard vetoes, output-comparability passes, TF32 is recorded enabled, output tensors are on GPU, and rows run on one selected physical GPU. |
| Promotion criterion for a later bounded leaderboard claim | At least two adjacent paired sizes in a predeclared ladder pass validity and output-comparability gates, then a predeclared uncertainty analysis supports a resource ranking or the result remains descriptive only. |
| Promotion veto | Route crash, nonfinite output, failed log-weight normalization, ESS fraction below threshold, Nystrom residual failure, dense transport materialization in scalable candidate rows, output-comparability failure for a claimed row, CPU fallback in GPU mode, TF32 mismatch, mixed physical GPU within the phase, or unsupported posterior/default/API/HMC claim. |
| Continuation veto | Neither GPU1 nor GPU0 is usable in trusted context; the common fixture cannot run both routes at a tiny CPU sanity size; the harness requires network/package installation; or a required implementation change would alter public/default BayesFilter behavior. |
| Repair trigger | Harness schema or route invocation mismatch; missing output metrics; Nystrom validity failure at tiny sanity size; GPU1 busy or unavailable before phase start, which triggers GPU0 fallback with manifest note; GPU change mid-phase, which invalidates paired rows and requires restart. |
| Explanatory diagnostics | Wall time, warm-call median, peak/current GPU allocator deltas, memory maxrss, residual magnitudes, ESS fraction, state-mean L2, and log-likelihood L2. |
| What must not be concluded | No superiority, no speedup claim, no statistical ranking, no posterior correctness, no dense Sinkhorn equivalence beyond prior tiny checks, no HMC readiness, no public API readiness, and no production/default route change. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Is Nystrom useful enough to enter a proper paired leaderboard screen against streaming TF32? |
| Exact baseline/comparator | Streaming TF32 LEDH/PFPF-OT route from `experimental_batched_ledh_pfpf_ot_streaming_tf` and `batched_annealed_transport_core_tf`, same fixture and GPU. |
| Primary pass/fail criterion | Pilot passes only if required paired rows complete for both routes with no hard vetoes and paired output-comparability passes. |
| Veto diagnostics | Nonfinite output; output log-weight normalization `> 1.0e-6`; ESS fraction `< 0.01`; Nystrom row/column residual `> 5.0e-2`; materialized scalable candidate transport matrix; output device not GPU in GPU mode; TF32 not recorded enabled in TF32 GPU mode; shape mismatch; state mean absolute L2 `> 1.0` and relative L2 `> 0.5`; log-likelihood absolute L2 `> 1.0`; selected GPU missing. |
| Explanatory-only diagnostics | Wall time, warm-call median, peak allocator delta, current allocator delta, maxrss, residual values below threshold, ESS values above threshold, and preview values. |
| Not concluded on pass | A pass only says Nystrom is a viable paired leaderboard candidate under this pilot. It does not establish ranking, superiority, posterior correctness, HMC readiness, or default readiness. |
| Artifact preserving result | JSON and Markdown under `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-effectiveness-leaderboard-*`; plan/result notes under this `docs/plans` prefix. |

## Fixed Pilot Criteria

| Diagnostic | Threshold | Role |
| --- | ---: | --- |
| Route invocations | `> 0` and equal to active mask count | hard veto |
| Output finite | `true` | hard veto |
| Output log-weight normalization | `<= 1.0e-6` | hard veto |
| ESS fraction | `>= 0.01` | hard veto |
| Nystrom row/column residual | `<= 5.0e-2` | hard veto |
| Nystrom transport matrix shape | sentinel `[B, 0, 0]` | hard veto if materialized |
| Streaming transport matrix shape | sentinel `[B, 0, 0]` | hard veto if materialized |
| Output-comparability state mean | relative L2 `<= 0.5` or absolute L2 `<= 1.0` | hard veto for paired-usefulness claim |
| Output-comparability log likelihood | absolute L2 `<= 1.0` | hard veto for paired-usefulness claim |
| TF32 state in GPU mode | recorded enabled | hard veto |
| Device in GPU mode | output tensors contain `GPU` | hard veto |
| Pilot particle counts | `[1024, 4096]` | pilot scope; not a ranking ladder |
| Warm timings | `repeats=1` after first materialization | explanatory only |

## GPU Selection Rule

Use trusted/elevated GPU context.  Prefer physical GPU1 by setting
`CUDA_VISIBLE_DEVICES=1`; use physical GPU0 only if GPU1 is busy, unavailable,
or unsuitable.  Record the selected GPU and fallback reason in the result
manifest.  All paired rows in one result artifact must run under one
`CUDA_VISIBLE_DEVICES` value.

## Skeptical Plan Audit

Pre-execution audit status: `PASSED_FOR_PILOT`.

The pilot does not use dense transport as a large-N comparator, does not treat
runtime or memory proxies as promotion criteria without paired validity, uses
fixed stop conditions and row timeouts, compares routes on one common fixture,
records GPU/TF32 state, and writes JSON/Markdown artifacts that answer only the
pilot usefulness question.  If the pilot passes, the next step is a replicated
leaderboard plan with uncertainty analysis before ranking language is allowed.

## Phase Sketch

| Phase | Artifact | Purpose |
| --- | --- | --- |
| P01 | `docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_effectiveness_leaderboard.py` and focused tests | Implement common paired harness and tiny CPU sanity. |
| P02 | `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-effectiveness-leaderboard-p02-pilot-2026-06-22.*` | Run GPU1-preferred paired pilot at `N=1024,4096`. |
| P03 | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-effectiveness-leaderboard-result-2026-06-22.md` | Interpret hard vetoes, viable candidates, statistical status, and next evidence. |

