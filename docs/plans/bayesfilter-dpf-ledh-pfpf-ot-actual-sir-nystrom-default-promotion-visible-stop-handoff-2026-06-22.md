# Actual-SIR Nystrom Default-Promotion Visible Stop Handoff

Date: 2026-06-22

Status: `PAUSED_COMPILED_REDO_P04_SERIOUS_B5_GATE_PASSED`

## Current State

The actual-SIR Nystrom lane has completed P01, P02, P03, P05A, and P05B.
P03/P05A passed replicated `N=1024` evidence, and P05B passed the `N=2048`
actual-SIR validity/comparability row.  The P05B speed interpretation has been
withdrawn: a same-GPU compiled streaming sanity row at `B=5,T=20,N=2048`
completed in `20.397380776004866s` compile plus first call and
`0.29988364898599684s` warm call, while P05B's paired harness reported
`1160.5996048829984s` streaming warm time because it used a Python-level route
loop with small chunks.  A one-seed paired `N=4096` launch was stopped before
artifact creation.  The lane has since been restarted as a compiled redo:
`nystrom_transport_resample_tensors_tf` was added, focused tests passed, the
compiled GPU P02 smoke at `B=1,T=3,N=128` passed on physical GPU1, and the P03
moderate gate at `B=1,T=20,N=1024` passed with `hard_vetoes=[]`.  The P03 row
exposed a serious compile-latency issue: Nystrom compile plus first call took
`804.5176504359115s`, while the warm call took `0.09494141908362508s`.  P03B
replaced the Nystrom Sinkhorn and actual-SIR time Python loops with
`tf.while_loop`, and the same row passed with Nystrom compile plus first call
reduced to `12.189794685924426s`.  P04 then passed a serious repaired compiled
row at `B=5,T=20,N=1024`, seeds `81120..81124`, with `hard_vetoes=[]`.

## Key Artifacts

- Runbook: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-visible-gated-execution-runbook-2026-06-22.md`
- Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-plan-2026-06-22.md`
- Current result: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-result-2026-06-22.md`
- P03 result: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-p03-serious-row-result-2026-06-22.md`
- P05A result: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-p05a-seed-replication-result-2026-06-22.md`
- P05B result: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-p05b-ladder-result-2026-06-22.md`
- P05 interim result: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-p05-replicated-ladder-result-2026-06-22.md`
- Runtime diagnostic result: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-runtime-protocol-diagnostic-result-2026-06-22.md`
- Compiled redo result: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-result-2026-06-22.md`
- Compiled redo P03 result: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p03-moderate-gate-result-2026-06-22.md`
- Compiled redo P03B result: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p03b-while-loop-compile-repair-result-2026-06-23.md`
- Compiled redo P04 result: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p04-serious-b5-gate-result-2026-06-23.md`
- Compiled redo harness: `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`
- Harness: `docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py`
- Tests: `tests/test_actual_sir_nystrom_default_promotion.py`
- Compiled redo tests: `tests/test_actual_sir_nystrom_compiled_redo.py`
- P02 JSON: `docs/benchmarks/actual-sir-nystrom-default-promotion-p02-gpu-pilot-2026-06-22.json`
- P03 JSON: `docs/benchmarks/actual-sir-nystrom-default-promotion-p03-serious-b5-t20-n1024-2026-06-22.json`
- P05A JSON: `docs/benchmarks/actual-sir-nystrom-default-promotion-p05a-seed-repl-b5-t20-n1024-2026-06-22.json`
- P05B JSON: `docs/benchmarks/actual-sir-nystrom-default-promotion-p05b-ladder-b5-t20-n2048-2026-06-22.json`
- Compiled streaming sanity JSON: `docs/benchmarks/actual-sir-streaming-compiled-sanity-b5-t20-n2048-gpu1-2026-06-22.json`
- Compiled redo P02 JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p02-gpu-smoke-2026-06-22.json`
- Compiled redo P03 JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p03-moderate-b1-t20-n1024-2026-06-22.json`
- Compiled redo P03B JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p03b-while-loop-repair-b1-t20-n1024-2026-06-23.json`
- Compiled redo P04 JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p04-serious-b5-t20-n1024-2026-06-23.json`

## Nonclaims

- No default readiness claim.
- No posterior correctness claim.
- No HMC readiness claim.
- No public API readiness claim.
- No statistical ranking claim.
- No dense Sinkhorn equivalence claim.

## Resume Instruction

Do not use prior Python-loop timing artifacts for speed, ranking, or promotion.
The Nystrom XLA compile-latency issue is repaired for the moderate gate.
P04 serious `B=5,T=20,N=1024` passed.  Resume with a repaired compiled disjoint
seed-batch replication at the same shape, suggested seeds `81220..81224`, before
any larger-N ladder.  Track paired log-likelihood deltas and keep runtime ratios
descriptive unless/until uncertainty analysis is added.  Use trusted/elevated
GPU preflight and prefer physical GPU1 if usable.
