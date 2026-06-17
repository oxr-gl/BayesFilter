# Phase 2 Gate Packet: Candidate Audit Notes

Date: 2026-06-17

## Purpose

This compact packet repairs Claude review round 01 by enumerating the Phase 2
gate evidence directly.  It summarizes the seven candidate audit notes without
asking the reviewer to infer per-lane coverage from prose.

## Gate Contract

| Required item | Gate evidence |
| --- | --- |
| Mandatory matrix columns | Every note contains `Original paper`, `Local note`, `Downloaded code`, `Execution-value test`, and `Required resolution`. |
| Mandatory comparison rows | Every note contains `Problem solved`, `Transport object`, `Marginals/orientation`, `Cost/kernel/epsilon`, `Approximation knob`, `Backend and gradients`, and `Execution value`. |
| Source/semantic classification | Every note states `source_locked`, `source_reference_only`, or `source_partial_user_needed`, plus exact semantics / approximate kernel / semantic replacement / reference-only / blocked vocabulary. |
| Paper/survey and source anchors | Every non-blocked lane has at least one survey/paper anchor and at least one local downloaded-code anchor. Mini-batch is blocked but still lists visible partial source anchors. |
| Baseline comparator | Every execution-value contract names Phase 1 dense/streaming TensorFlow diagnostics as the comparator or, for semantic-replacement lanes, as the descriptive semantic-delta comparator. |
| Forbidden claims | Every note states no ranking/no speedup/no execution-value claim from static source inspection, or records the lane as blocked. |
| Backend boundary | Every note preserves TensorFlow/TFP as the BayesFilter-owned implementation default and treats non-TF source as reference unless later approved. |
| Mini-batch blocker | Mini-batch remains `source_partial_user_needed` and blocked for decision-grade use. |

Local structured check status: `PASS`.

## Candidate Evidence Table

| Candidate | Audit note | Source status | Semantic class | Baseline/comparator statement | Paper/survey anchor | Local downloaded-code anchor | Required resolution |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Exact online/GPU Sinkhorn | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-exact-online-gpu-audit-2026-06-17.md` | `source_reference_only` | exact semantics / reference-only | First execution-value contract names Phase 1 dense and TensorFlow streaming diagnostics; requires dense parity before runtime/memory interpretation. | Survey lines 390-435; equations for squared Euclidean online reduction, log-domain update, FlashSinkhorn barycentric application. | FlashSinkhorn `API.md` lines 397-438; GeomLoss `_ot_result.py` lines 7-49 and 331-357; OTT-JAX `sinkhorn.py` lines 442-469. | Treat as exact-semantics reference; do not make a BayesFilter default unless a TensorFlow/TFP operator path is implemented and reviewed. |
| Nystrom kernel Sinkhorn | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-nystrom-audit-2026-06-17.md` | `source_locked` | approximate kernel | First execution-value contract names Phase 1 dense TensorFlow transport and streaming parity fixtures. | Altschuler source TeX lines 17-27 and 121-172; survey lines 437-545. | POT `ot/lowrank.py` lines 530-730; POT `_empirical.py` lines 766-865; LinearSinkhorn `FastSinkhorn.py` lines 197-260. | Implement only as approximate-kernel lane; fixed landmarks/rank/epsilon map required before parity claims. |
| Positive-feature Sinkhorn | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-audit-2026-06-17.md` | `source_locked` | approximate kernel / semantic kernel replacement | First execution-value contract names Phase 1 dense/streaming baseline and Nystrom candidate diagnostics where available. | Positive-feature text `.localsource/scalable_ot_survey/2006.07057.txt`; survey lines 546-624. | LinearSinkhorn `FastSinkhorn.py` lines 77-161; `EXP_GAN/torch_lin_sinkhorn.py` as scalar-cost caution. | Declare whether features approximate the dense Gibbs kernel or replace it; scalar loss is not transport. |
| Direct low-rank coupling OT | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-coupling-audit-2026-06-17.md` | `source_locked` | semantic replacement | First execution-value contract names Phase 1 dense/streaming baseline for descriptive semantic delta, not exact parity. | Low-rank coupling paper text `.localsource/scalable_ot_survey/2103.04737.txt`; survey lines 628-760. | POT `ot/lowrank.py` lines 322-527; POT `ot/factored.py` lines 17-170; OTT-JAX `sinkhorn_lr.py` lines 153-180, 228-250, and 716-735. | Test as semantic replacement over low-rank couplings; factor marginals are hard vetoes, dense error is explanatory. |
| Sparse/localized OT | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-sparse-localized-audit-2026-06-17.md` | `source_reference_only` | exact semantics when certified sparse support holds; approximate support restriction/reference-only otherwise | First execution-value contract names Phase 1 dense baseline plus later LEDH fixtures for locality/support diagnostics. | Schmitzer/Screenkhorn paper text files; survey lines 762-826. | POT `_screenkhorn.py` lines 20-120 and 405-426; Schmitzer `TSinkhornSolver.cpp` lines 321-352; MultiScaleOT sparse coupling handlers. | Run locality diagnostic before implementation; block sparse prototype if support is diffuse or residuals fail. |
| Sliced/subspace OT | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-sliced-subspace-audit-2026-06-17.md` | `source_locked` | semantic replacement / exploratory surrogate | First execution-value contract names Phase 1 dense/streaming baseline for descriptive semantic delta and downstream diagnostics. | Paty-Cuturi, Kolouri, Deshpande paper text files; survey lines 892-973. | POT `ot/sliced/_sliced_plans.py` lines 21-184 and 187-260. | Do not claim dense OT equivalence; require projected/full-state output semantics before resampling claims. |
| Mini-batch / BoMb OT | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-minibatch-bomb-audit-2026-06-17.md` | `source_partial_user_needed` | blocked / semantic replacement | First execution-value contract is conditional if unblocked; Phase 1 dense/streaming baseline would be descriptive comparator. | BoMb and partial mini-batch paper text files; survey lines 847-890. | Manifest records partial checkout; `ABC/utils.py` lines 11-65; `ColorTransfer/utils.py` lines 8-120 and 160-196. | Blocked until clean source/archive; scalar/hierarchical costs must not be treated as BayesFilter transport. |

## Boundary Ledger

| Boundary | Status |
| --- | --- |
| No execution-value claim from source inspection | `PASS`: all notes state execution value is pending or blocked. |
| No ranking from static audit | `PASS`: all notes include no-ranking/no-speedup boundaries. |
| No non-TF default promotion | `PASS`: all non-TF sources are reference/comparator unless later approved. |
| Scalar cost not transport | `PASS`: positive-feature and Mini-batch notes explicitly block scalar-loss-only use. |
| Mini-batch blocker preserved | `PASS`: `source_partial_user_needed` and blocked. |
| Claude round 01 limitation recorded | `PASS`: round 01 artifact records summary review as limited and non-converged. |
| Source-locked pending-lane guard | `PASS`: `source_locked` plus `execution_value_pending` is source-readiness evidence only, not transport correctness, dense equivalence, default-readiness, or ranking evidence. |

## Repair Result

Round 01 requested direct enumeration of all seven candidates with baseline,
anchors, classifications, and required resolution.  This packet provides that
enumeration.  It is the intended object for Claude review round 02.
