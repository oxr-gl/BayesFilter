# Actual-SIR Low-Rank Validation Visible Execution Ledger

Date: 2026-06-21

Status: `IN_PROGRESS`

## Ledger

### 2026-06-21T14:50:00+08:00 - Phase 0 - PRECHECK

Evidence contract:

- Question: can the planned program answer whether low-rank helps actual-SIR
  d18 LEDH/PFPF-OT large-N efficiency?
- Baseline/comparator: existing streaming actual-SIR TF32/GPU route.
- Primary criterion: source anchors, bounded ownership, skeptical audit, and
  read-only review converge before implementation.
- Veto diagnostics: wrong baseline, proxy metric promotion, missing stop
  condition, unsupported claim, shared contract change.
- Non-claims: no implementation, speed, posterior, HMC, default, or public API
  claim in P00.

Actions:

- Created draft master program, phase subplans, visible runbook, review ledger,
  and stop handoff.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-master-program-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-visible-gated-execution-runbook-2026-06-21.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Run P00 local path checks and Claude read-only review.

### 2026-06-21T15:16:10+08:00 - Phase 0 - CLOSE

Evidence contract:

- Question: can the planned program answer whether low-rank helps actual-SIR
  d18 LEDH/PFPF-OT large-N efficiency?
- Baseline/comparator: existing streaming actual-SIR TF32/GPU route.
- Primary criterion: source anchors, bounded ownership, skeptical audit, and
  read-only review converge before implementation.

Actions:

- Ran local source path checks for the actual-SIR benchmark, high-N actual-SIR
  anchor, prior synthetic low-rank result, and low-rank solver.
- Patched timeout-boundary and same-physical-GPU fairness rules after Claude R3.
- Claude R4 returned `VERDICT: AGREE`.
- Wrote P00 result.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p00-governance-result-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-claude-review-ledger-2026-06-21.md`

Gate status:

- `PASS`

Next action:

- Enter P01 harness integration.

### 2026-06-21T15:30:46+08:00 - Phase 1 - CLOSE

Evidence contract:

- Question: does the harness correctly route actual-SIR LEDH/PFPF-OT through
  streaming or low-rank while preserving route-fired evidence and diagnostics?
- Baseline/comparator: existing actual-SIR streaming route semantics from P8j.
- Primary criterion: harness compiles, focused tests pass, both route choices
  are encoded, actual-SIR semantics are preserved, and low-rank diagnostics are
  recorded.

Actions:

- Added owned harness
  `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`.
- Added focused tests
  `tests/test_actual_sir_low_rank_route_validation.py`.
- Ran required compile and pytest checks.
- Wrote a CPU-hidden tiny P01 JSON/Markdown artifact with both routes.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p01-harness-result-2026-06-21.md`
- `docs/benchmarks/actual-sir-low-rank-route-validation-p01-harness-smoke-2026-06-21.json`
- `docs/benchmarks/actual-sir-low-rank-route-validation-p01-harness-smoke-2026-06-21.md`

Gate status:

- `PASS`

Next action:

- Enter P02 tiny actual-SIR route smoke.

### 2026-06-21T15:33:20+08:00 - Phase 2 - CLOSE

Evidence contract:

- Question: do both route implementations execute on tiny actual-SIR rows and
  emit required validity/diagnostic artifacts?
- Baseline/comparator: streaming route on the same actual-SIR rows.
- Primary criterion: both routes pass tiny rows with finite outputs,
  route-fired evidence, and no hard vetoes.

Actions:

- Ran CPU-hidden `B=1,T=3,N=128` both-route smoke.
- Ran CPU-hidden `B=1,T=20,N=256` both-route smoke.
- Wrote smoke aggregate JSON/Markdown.
- Wrote P02 result.

Artifacts:

- `docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21.json`
- `docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p02-smoke-result-2026-06-21.md`

Gate status:

- `PASS`

Next action:

- Enter P03 paired actual-SIR GPU ladder after GPU status check.

### 2026-06-21T15:42:16+08:00 - Phase 3 - PRECHECK

Evidence contract:

- Question: on feasible paired actual-SIR d18 rows, does the low-rank route
  preserve hard validity and predeclared engineering comparability while
  showing bounded practical warm-time evidence versus the existing compiled
  streaming route?
- Baseline/comparator: existing compiled streaming actual-SIR TF32/GPU route
  from `docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py`, timed via
  `--streaming-timing-source compiled_core`.
- Primary criterion: at least two adjacent paired rows with no hard vetoes,
  no paired comparability vetoes, same physical GPU UUID, exact
  `warmups=1`, `repeats=3`, and warm-median `streaming / low_rank >= 1.25`.
- Veto diagnostics: nonfinite outputs, missing actual-SIR semantics, missing
  GPU/TF32 provenance, route-fired mismatch, dense low-rank materialization,
  invalid factors, factor residual above threshold, paired comparability
  failure, or cross-physical-GPU route evidence.
- Explanatory-only diagnostics: compile/first-call time, memory, ESS above the
  hard floor, diagnostic-loop streaming time, and low-rank projection
  iterations.
- Nonclaims: no posterior correctness, HMC readiness, public API readiness,
  default/production readiness, dense Sinkhorn equivalence, broad scalable-OT
  selection, or statistical ranking.

Skeptical audit:

- Wrong baseline: guarded by using the existing compiled actual-SIR streaming
  route, not a synthetic comparator or the owned eager diagnostic loop.
- Proxy metrics: guarded by treating runtime as promotion evidence only after
  hard validity and paired comparability gates pass.
- Missing stop conditions: guarded by P03 `TUNING_REQUIRED` and
  `REJECT_CURRENT_ROUTE` stop labels.
- Unfair comparison: guarded by same seeds, same tensors, same dtype/TF32
  mode, same command row shape, and same physical GPU UUID.
- Hidden assumptions: guarded by preserving low-rank as a diagnostic route
  replacement, not dense Sinkhorn equivalence or posterior correctness.
- Stale context: P00-P02 result artifacts exist and P03 subplan has the
  reviewed timeout/physical-GPU amendments.
- Environment mismatch: trusted `nvidia-smi` selected GPU1
  `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`; the harness must record the
  same physical UUID for support rows.
- Artifact mismatch: each row command writes JSON/Markdown row artifacts with
  route, semantics, diagnostics, timing, and run manifest fields.

Gate status:

- `IN_PROGRESS`

Next action:

- Run the first P03 paired GPU row at `B=5,T=20,N=1024` on GPU1.

### 2026-06-21T15:57:46+08:00 - Phase 3 - CLOSE

Evidence contract:

- Question: on feasible paired actual-SIR d18 rows, does the low-rank route
  preserve hard validity and predeclared engineering comparability while
  showing bounded practical warm-time evidence versus the existing compiled
  streaming route?
- Baseline/comparator: existing compiled streaming actual-SIR TF32/GPU route.
- Primary criterion: at least two adjacent paired rows with no hard vetoes,
  no paired comparability vetoes, same physical GPU UUID, exact
  `warmups=1`, `repeats=3`, and warm median `streaming / low_rank >= 1.25`.

Actions:

- Ran trusted GPU status check; GPU1 was available and selected.
- Ran the first required P03 paired row
  `B=5,T=20,N=1024` on GPU1 with five seeds, TF32 enabled,
  compiled streaming timing, and exact `warmups=1`, `repeats=3`.
- The row completed before the `3600s` outer timeout and wrote JSON/Markdown.
- Wrote the P03 aggregate and P03 result.
- Refreshed P04 as blocked and wrote a P04 blocked result.

Artifacts:

- `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.json`
- `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.md`
- `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21.json`
- `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p03-paired-ladder-result-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p04-large-n-envelope-result-2026-06-21.md`

Gate status:

- Hard validity: `PASS` for the attempted row.
- Paired log-likelihood comparability: `FAIL`; max absolute delta
  `58.0933837890625`, mean absolute delta `42.93328857421875`.
- Warm-time support: `FAIL`; ratio `0.016606596042173186`, below required
  `1.25`.
- P03 final status: `TUNING_REQUIRED`.

Next action:

- Stop the master program before P04 large-N execution and write final
  stop handoff/result artifacts.

### 2026-06-21T16:17:09+08:00 - Phase 5 - CLOSE

Evidence contract:

- Question: what bounded decision is supported by the actual-SIR validation
  artifacts?
- Baseline/comparator: existing compiled streaming actual-SIR route and P03
  paired artifact.
- Primary criterion: final label must be supported by phase artifacts without
  unsupported speedup, large-N, default, posterior, API, HMC, dense-equivalence,
  broad-selection, or statistical-ranking claims.

Actions:

- Wrote final result and stop handoff.
- Ran local JSON/path/text consistency checks.
- Ran Claude final closeout review rounds P05-R1 through P05-R4 using
  path-only read-only prompts.
- Patched R1 broad wording/P04 allowance/stale master issues.
- Patched R2 master/result stop-handoff wording.
- Patched R3 self-referential review-ledger wording.
- Claude R4 returned `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-result-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-visible-stop-handoff-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-claude-review-ledger-2026-06-21.md`

Gate status:

- `STOPPED_TUNING_REQUIRED`

Next action:

- Human decision: open a new predeclared tuning/repair program or defer this
  low-rank route for actual-SIR large-particle efficiency.
