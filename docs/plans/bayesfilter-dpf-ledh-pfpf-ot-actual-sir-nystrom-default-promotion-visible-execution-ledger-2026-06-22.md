# Actual-SIR Nystrom Default-Promotion Visible Execution Ledger

Date: 2026-06-22

Status: `COMPILED_REDO_P04_SERIOUS_B5_GATE_PASSED`

## Ledger

| Time | Phase | Entry |
| --- | --- | --- |
| 2026-06-22 | P01 | Harness compile and tiny CPU tests passed: `pytest -q tests/test_actual_sir_nystrom_default_promotion.py` reported `3 passed`. |
| 2026-06-22 | P02 | Small actual-SIR GPU pilot passed at `B=1,T=3,N=128,rank=32`; artifact `docs/benchmarks/actual-sir-nystrom-default-promotion-p02-gpu-pilot-2026-06-22.json` reports `status=PASS`, `hard_vetoes=[]`. |
| 2026-06-22 | P00 | Governance precheck passed; P02 rechecked as `PASS` with `hard_vetoes=[]`. |
| 2026-06-22 | P01 | Relaunch precheck passed: compile succeeded and focused pytest reported `3 passed`. |
| 2026-06-22 | P03 | Serious actual-SIR row completed on fallback physical GPU0 because GPU1 was memory-busy. Artifact `docs/benchmarks/actual-sir-nystrom-default-promotion-p03-serious-b5-t20-n1024-2026-06-22.json` reports `status=PASS`, `hard_vetoes=[]`, and paired comparability passed. |
| 2026-06-22 | P05A | Seed-replication actual-SIR row completed on physical GPU1. Artifact `docs/benchmarks/actual-sir-nystrom-default-promotion-p05a-seed-repl-b5-t20-n1024-2026-06-22.json` reports `status=PASS`, `hard_vetoes=[]`, and paired comparability passed. |
| 2026-06-22 | P05B | `N=2048` actual-SIR ladder row completed on physical GPU1. Artifact `docs/benchmarks/actual-sir-nystrom-default-promotion-p05b-ladder-b5-t20-n2048-2026-06-22.json` reports `status=PASS`, `hard_vetoes=[]`, and paired comparability passed. |
| 2026-06-22 | P05C | One-seed paired `N=4096` launch was stopped before artifact creation after runtime protocol concerns. |
| 2026-06-22 | Runtime diagnostic | Same-GPU compiled streaming sanity row at `B=5,T=20,N=2048` passed on physical GPU1 with `20.397380776004866s` compile plus first call and `0.29988364898599684s` warm call. This shows P05B streaming runtime was a harness/runtime-path artifact, not GPU/TF32 slowness. Result: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-runtime-protocol-diagnostic-result-2026-06-22.md`. |
| 2026-06-22 | Compiled redo | Added graph-compatible tensor Nystrom core and compiled redo harness. Focused tests passed, and GPU P02 smoke at `B=1,T=3,N=128` passed on physical GPU1 with `hard_vetoes=[]`. Result: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-result-2026-06-22.md`. |
| 2026-06-22 | Compiled redo P03 | Moderate compiled paired row `B=1,T=20,N=1024`, seed `81120`, passed on physical GPU1 with `hard_vetoes=[]` and paired log-likelihood max abs delta `0.1632080078125`. Nystrom compile plus first call took `804.5176504359115s`; warm call took `0.09494141908362508s`. Result: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p03-moderate-gate-result-2026-06-22.md`. |
| 2026-06-23 | Compile repair P03B | Replaced Nystrom Sinkhorn and actual-SIR time Python loops with `tf.while_loop`. Focused tests passed. Same moderate row passed on physical GPU1 with `hard_vetoes=[]`; Nystrom compile plus first call dropped from `804.5176504359115s` to `12.189794685924426s`. Result: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p03b-while-loop-compile-repair-result-2026-06-23.md`. |
| 2026-06-23 | Compiled redo P04 | Serious repaired compiled row `B=5,T=20,N=1024`, seeds `81120..81124`, passed on physical GPU1 with `hard_vetoes=[]`; paired log-likelihood max abs delta `3.85498046875`; Nystrom compile plus first call `14.019542706897482s`, warm call `0.05731428205035627s`. Result: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p04-serious-b5-gate-result-2026-06-23.md`. |

## Next Phase

P05 replicated actual-SIR ladder:

- Candidate row basis: P03 `B=5,T=20,N=1024,D=18,M=9` passed.
- Seed replication basis: P05A `B=5,T=20,N=1024,D=18,M=9` with seeds `81220..81224` passed.
- Completed larger-N row: P05B `B=5,T=20,N=2048,D=18,M=9` passed.
- Next row: launch a repaired compiled disjoint seed-batch replication at `B=5,T=20,N=1024`, suggested seeds `81220..81224`, before any larger-N ladder.
- Candidate: Nystrom `rank=32`
- Comparator: compiled streaming TF32 actual-SIR under the new redo harness
- GPU: physical GPU1 if usable, otherwise GPU0
