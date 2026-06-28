# Nystrom LEDH-PFPF-OT Algorithm-Complete Master Program

Date: 2026-06-21

Status: `DRAFT_FOR_REVIEW`

Supervisor/executor: Codex in this conversation.

Read-only reviewer: Claude Opus at high/max effort when material review is
needed. Claude is not an execution authority and cannot authorize human,
runtime, model-file, funding, product-capability, scientific-claim, production,
default, public-API, or HMC boundaries.

## Purpose

Implement and test the fixed-rank Nystrom kernel Sinkhorn candidate deeply
enough that it can later enter a common scalable-OT screening leaderboard as a
real algorithmic candidate rather than a half-implemented diagnostic artifact.

This program does not select a default algorithm. The current repository
default remains GPU-oriented streaming TF32 LEDH-PFPF-OT. This lane asks
whether Nystrom should become a leaderboard-ready candidate for later screening.

## Research Intent Ledger

| Field | Ledger |
| --- | --- |
| Main question | Can fixed-rank Nystrom kernel Sinkhorn be implemented as an end-to-end TensorFlow candidate for LEDH-PFPF-OT resampling with acceptable small-reference validity, downstream smoke behavior, and GPU large-N operational evidence? |
| Candidate/mechanism | Fixed-rank Nystrom approximation to the Gaussian Gibbs kernel, low-rank Sinkhorn scaling through `K ~= V A^{-1} V^T`, nonmaterialized factor application to particles, deterministic landmark rule for reproducibility, TensorFlow backend. |
| Expected failure mode | Rank too small for target geometry, factor residual failures, nonfinite factors/particles, landmark sensitivity, dense-reference drift at small N, GPU timeout/OOM, accidental dense matrix materialization, CPU fallback in GPU phase, or unsupported claims. |
| Promotion criterion | Candidate becomes `leaderboard_ready_diagnostic_candidate` only if implementation/static tests pass, small dense-reference gates pass for at least one predeclared rank per fixture, downstream LEDH smoke passes without hard vetoes, and GPU scale rows complete with finite outputs and no dense transport matrix. |
| Promotion veto | Nonfinite factors/particles, residual failures, missing artifacts, schema mismatch, dense matrix materialization, incorrect baseline/comparator, CPU fallback in GPU phase, overclaiming dense equivalence/speedup/default/posterior/HMC/API readiness, or Claude/local review finding unresolved boundary mismatch. |
| Continuation veto | Broken harness, source-route mismatch requiring redesign, unable to obtain trusted GPU state for GPU phase, repeated Claude review non-convergence after five rounds for the same material blocker, or any human-boundary decision not already approved. |
| Repair trigger | Missing metadata, incorrect plan claims, hard-veto failure caused by fixable harness bug, stale source anchors, unbounded stdout/logging, or a fixable artifact coverage gap. |
| Explanatory diagnostics | Runtime, memory metadata, memory-entry proxy, dense-reference particle error, residual magnitudes, rank/landmark metadata, GPU memory info, and same-harness streaming context. |
| Must not conclude | No default change, no final algorithm ranking, no posterior correctness, no HMC readiness, no public API readiness, no dense Sinkhorn equivalence beyond small checked fixtures, no statistical superiority, and no claim that Nystrom solves all large-N or high-D cases. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the Nystrom candidate be made algorithm-complete enough for later screening? |
| Baseline/comparator | Small-N dense TensorFlow annealed transport for reference validity; streaming TF32 default as operational context in GPU phase; prior Phase 11 diagnostic as provenance only. |
| Primary pass/fail criterion | All required phases complete with result artifacts, no hard vetoes in implementation/static, small-reference, downstream-smoke, and GPU-scale gates, and final closeout preserves claim boundaries. |
| Veto diagnostics | Nonfinite output, factor/scaling residual failures, dense matrix materialization, missing required artifact, missing source-route metadata, wrong comparator, CPU fallback in trusted GPU phase, stale default claim, or unsupported speedup/default/posterior/HMC/API claim. |
| Explanatory only | Runtime, memory, dense-reference errors for nonpromoted ranks, small one-seed fixture differences, and descriptive streaming context. |
| Not concluded | No production/default readiness, no public API readiness, no HMC readiness, no posterior correctness, no statistically supported ranking, no broad scalable-OT selection. |
| Artifacts | Phase subplans/results under `docs/plans`; harness/test and JSON/Markdown benchmark outputs under `docs/benchmarks`; logs under `docs/benchmarks/logs`; review/ledger/handoff files under `docs/plans`. |

## Baseline And Assumption Audit

| Choice | Provenance | Why reasonable | How it could mislead | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Use existing Nystrom prototype as source route | Phase 11 result and `nystrom_transport_tf.py` | It already implements `V A^{-1} V^T`, factor Sinkhorn scaling, and nonmaterialized apply. | Prototype was CPU/small-fixture only. | P01 static/unit tests and metadata checks. | Required |
| Use dense TensorFlow only for small reference validity | Existing `annealed_transport_tf.py` dense mode | Dense large-N is not operationally useful and may just OOM. | Dense small-N agreement could be overread as large-N correctness. | P02 declares small-reference only and separates promoted ranks from descriptive rows. | Required |
| Test downstream via LGSSM-shaped LEDH loop | Existing low-rank and streaming harness patterns | It exercises LEDH flow, weight correction, resampling, ESS, and final particles. | Synthetic fixture is not posterior validation. | P03 nonclaims and hard-veto smoke criteria. | Required |
| Prefer GPU1 unless busy, then GPU0 | User directive on 2026-06-21 | Keeps two-agent GPU use predictable. | Logical `/GPU:0` after remapping could hide physical GPU identity. | P04 trusted `nvidia-smi` preflight and artifact fields record physical GPU. | Required |
| Treat timing/memory as non-ranking evidence | Scientific coding policy | One-seed/single-shape runs are screening evidence only. | Could be turned into premature leaderboard. | Result inference-status tables. | Required |

## Skeptical Plan Audit

Audit decision: `PASS_FOR_REVIEW_BEFORE_EXECUTION`.

- Wrong baseline risk: controlled. Dense is used only for small reference
  validity; streaming default is operational context, not a ranking comparator.
- Proxy metric risk: controlled. Runtime and memory do not promote a rank or
  default; they only support later leaderboard readiness.
- Stop-condition risk: controlled. Each phase has explicit stop conditions.
- Unfair comparison risk: controlled. Nystrom is judged first against its own
  source-route and small-reference validity, not against mature production
  default behavior.
- Hidden assumptions: recorded for rank, landmarks, GPU selection, dtype, and
  nonmaterialized transport.
- Stale context: P00/P01 reread current files and record git status.
- Environment mismatch: GPU phase requires trusted `nvidia-smi` and device
  evidence.
- Artifact mismatch: each phase names required JSON/Markdown/result artifacts.

## Phase Index

| Phase | Name | Subplan | Result artifact |
| --- | --- | --- | --- |
| P00 | Governance and source lock | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p00-governance-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p00-governance-result-2026-06-21.md` |
| P01 | Implementation and harness | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p01-implementation-harness-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p01-implementation-harness-result-2026-06-21.md` |
| P02 | Small dense-reference validation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p02-small-reference-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p02-small-reference-result-2026-06-21.md` |
| P03 | Downstream LEDH smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p03-downstream-smoke-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p03-downstream-smoke-result-2026-06-21.md` |
| P04 | Trusted GPU scale envelope | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p04-gpu-scale-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p04-gpu-scale-result-2026-06-21.md` |
| P05 | Closeout and leaderboard readiness decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p05-closeout-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-result-2026-06-21.md` |

## Predeclared Ladders, Thresholds, And Schema

### P02 Small Dense-Reference Gate

Required fixtures and ranks:

| Fixture | Particle count | Ranks |
| --- | ---: | --- |
| `tiny_manual` | 4 | `2,3,4` |
| `small_parity` | 8 | `2,4,8` |
| `high_dim_low_rank` | 32 | `2,4,8,16,32` |
| `ledh_specific_smoke` | 32 | `4,8,16,32` |

Required promoted-rank thresholds:

- max row residual: at most `5.0e-2`;
- max column residual: at most `5.0e-2`;
- max dense-reference transported-particle error: at most `7.5e-2`;
- RMS dense-reference transported-particle error: at most `3.0e-2`;
- finite factors and finite transported particles: required;
- candidate transport matrix shape must end in `[0, 0]`.

At least one rank per required fixture must pass all promoted-rank thresholds.
Rows that fail thresholds remain explanatory and must not be used as ranking
evidence.

### P03 Downstream Smoke Gate

Required CPU smoke rows:

| Fixture id | N | Rank | Time steps | State dim | Obs dim | Required |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `nystrom_ledh_smoke_n64_rank8` | 64 | 8 | 2 | 6 | 4 | yes |
| `nystrom_ledh_smoke_n128_rank16` | 128 | 16 | 2 | 6 | 4 | yes |

Required thresholds:

- output log-weight normalization residual: at most `1.0e-6`;
- ESS fraction minimum: at least `1.0e-2`;
- max Nystrom row residual: at most `5.0e-2`;
- max Nystrom column residual: at most `5.0e-2`;
- finite log likelihood, summaries, final particles, final log weights, factors,
  and scalings: required;
- no candidate dense transport matrix: required.

### P04 Trusted GPU Scale Gate

Required GPU rows:

| N | Rank | Time steps | State dim | Obs dim | Required |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1024 | 16 | 2 | 8 | 6 | yes |
| 4096 | 32 | 2 | 8 | 6 | yes |
| 8192 | 32 | 2 | 8 | 6 | yes |

Optional GPU row:

| N | Rank | Time steps | State dim | Obs dim | Attempt condition |
| ---: | ---: | ---: | ---: | ---: | --- |
| 16384 | 64 | 2 | 8 | 6 | all required rows pass and elapsed P04 wall time is at most 45 minutes |

GPU phase budgets and selection:

- P04 wall-clock budget: `7200` seconds.
- Per-row timeout: `1200` seconds.
- Prefer physical GPU1 unless absent, total memory used is at least `2048 MiB`,
  utilization is at least `20%`, or any non-display compute process uses at
  least `2048 MiB`.
- Use physical GPU0 only if GPU1 is busy/unsuitable by the above rule and GPU0
  is usable by the same rule.
- Stop and write a blocker if neither GPU is usable.
- Record physical GPU, `CUDA_VISIBLE_DEVICES`, logical TensorFlow device list,
  and `nvidia-smi` summary in the artifact.

Required P04 thresholds:

- finite outputs and factors: required;
- output log-weight normalization residual: at most `1.0e-6`;
- ESS fraction minimum: at least `1.0e-2`;
- max Nystrom row residual: at most `5.0e-2`;
- max Nystrom column residual: at most `5.0e-2`;
- TF32 execution recorded enabled for float32 rows: required;
- GPU output device evidence: required;
- no candidate dense transport matrix: required.

### Required Candidate Schema Fields

Every P02-P04 JSON artifact must include:

- `algorithm_family`;
- `mode`;
- `status`;
- `hard_vetoes`;
- `run_manifest`;
- `source_route`;
- `source_route_components`;
- `semantic_class`;
- `baseline_comparator`;
- `transport_object_kind`;
- `transport_matrix_materialized`;
- `nonclaims`;
- per-row `rank`, `landmark_indices`, residuals, finite checks, output shape,
  transport-matrix shape, and timing fields.

## Planned Implementation Artifacts

- Harness:
  `docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py`
- Tests:
  `tests/test_nystrom_ledh_pfpf_algorithm_complete.py`
- Existing candidate implementation:
  `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`

## Planned Benchmark Artifacts

- P02 JSON/Markdown:
  `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.{json,md}`
- P03 JSON/Markdown:
  `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.{json,md}`
- P04 JSON/Markdown:
  `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.{json,md}`

## Review And Repair Loop

For material issues:

1. Record the issue in the visible execution ledger.
2. Patch the same subplan, harness, or result visibly.
3. Rerun focused local checks.
4. Use Claude only as a read-only reviewer for material plan or claim-boundary
   changes.
5. Stop after five Claude review rounds for the same blocker and write a
   blocker result.

Claude review prompts must be compact and path-based. Do not paste whole files.
