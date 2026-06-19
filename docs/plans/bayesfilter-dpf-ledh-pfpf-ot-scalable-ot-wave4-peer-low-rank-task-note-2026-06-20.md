# Wave 4 Peer-Agent Task Note: Low-Rank Coupling Lane

Date: 2026-06-20
From: current agent / coordinator
To: peer agent

## Supersession Notice

`SUPERSEDED_FOR_PEER_EXECUTION_BY_INDEPENDENT_LANE_CLARIFICATION`

This note imposed too much synchronization with the current positive-feature
lane.  For peer-agent execution, follow the active clarification instead:

`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-independent-lane-clarification-to-peer-2026-06-20.md`

In particular, do not wait for the current lane, do not treat the current
lane's fixture/seed grid as binding, and do not treat fixture/seed mismatch
with the current lane as a low-rank-lane hard veto.  Continue the low-rank
coupling solver-route as an independent algorithm lane to closeout or true
blocker.

## Purpose

Execute the peer-agent Wave 4 low-rank coupling solver-route lane independently
to completion.  This note is the durable coordination record; do not rely on
chat copy/paste as the source of truth.

## Ownership

You are the peer agent.  Own only the low-rank coupling solver-route lane.

The current agent owns only the positive-feature Sinkhorn lane.  Do not edit
current-agent Wave 4 artifacts except to read them for shared contract
alignment.

Use exactly these two agent labels:

- `peer agent`;
- `current agent`.

Do not introduce Agent A/B/C/D labels.

## Entry Context

Read before execution:

- Wave 4 master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-master-program-2026-06-20.md`
- W4-1 peer handoff subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p01-peer-low-rank-handoff-subplan-2026-06-20.md`
- W4-3 final merge subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p03-final-merge-subplan-2026-06-20.md`
- Wave 2 low-rank result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-result-2026-06-19.md`
- Wave 3 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-result-2026-06-19.md`

## Required Lane Artifacts

Write these artifacts:

- `docs/benchmarks/scalable_ot_wave4_low_rank_coupling_validation.py`
- `tests/test_wave4_low_rank_coupling_validation.py`
- `docs/benchmarks/scalable-ot-wave4-low-rank-coupling-validation-2026-06-20.json`
- `docs/benchmarks/scalable-ot-wave4-low-rank-coupling-validation-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-low-rank-coupling-result-2026-06-20.md`

## Required Fixture And Seed Grid

Use the same Wave 4 fixture/seed grid as the current-agent lane:

- fixtures: `weighted_curve`, `bimodal_tail`, `high_dim_low_rank`;
- seeds: `101`, `202`, `303`.

If you cannot use the same grid, write a blocker result.  Do not silently
change the grid, because W4-3 final merge treats fixture/seed mismatch as a
hard veto.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the low-rank coupling solver-route semantic-replacement lane remain viable under replicated deterministic downstream resampling screens? |
| Baseline/comparator | Exact weighted input estimates are the downstream reference.  Naive uniform-no-transport estimates are explanatory only. |
| Primary pass criterion | Harness/test/official diagnostic exit 0; hard vetoes are empty; transported particles are finite and shape-valid; output log weights are normalized uniform; low-rank factors are finite and nonnegative with positive `g`; residual thresholds are satisfied; max weighted-mean error is <= `3.0e-1`; max weighted second-moment error is <= `1.0`; manifest contains required run fields. |
| Veto diagnostics | Missing Wave 2/Wave 3 entry artifacts, nonfinite output or diagnostics, negative factors, nonpositive `g`, shape mismatch, log-weight normalization residual above `1.0e-10`, residual threshold failure, moment screen threshold failure, missing manifest field, unsupported claim, fixture/seed mismatch, or official command failure. |
| Explanatory diagnostics | Naive estimator errors, candidate-vs-naive differences, wall time, per-fixture/per-seed tables, rank, assignment epsilon, projection residuals, and descriptive summaries. |
| Not concluded | No ranking, speedup, superiority, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, full low-rank Sinkhorn solver-fidelity, or broad scalable-OT selection. |

## Required Artifact Schema

Your JSON result must include:

- `status`;
- `wave4_status`;
- `lane_id`;
- `candidate_id`;
- `hard_vetoes`;
- `settings`;
- `summary`;
- `rows`;
- `inference_status`;
- `manifest`;
- `evidence_contract`;
- `nonclaims`.

Each row must record:

- fixture name;
- seed;
- particle count;
- state dimension;
- candidate weighted-mean error;
- candidate weighted second-moment error;
- naive uniform-no-transport errors;
- transport diagnostics;
- wall time;
- row hard vetoes.

Manifest must include:

- `git_commit`;
- `command`;
- `argv`;
- `plan_path`;
- `result_path`;
- `json_output_path`;
- `markdown_output_path`;
- `fixtures`;
- `seeds`;
- `total_wall_time_seconds`;
- Python/platform/TensorFlow versions where applicable;
- CPU/GPU device scope;
- whether GPU devices were intentionally hidden.

## Required Checks

Use CPU-scoped TensorFlow diagnostics unless you write a separate trusted GPU
plan:

```bash
python -m py_compile docs/benchmarks/scalable_ot_wave4_low_rank_coupling_validation.py tests/test_wave4_low_rank_coupling_validation.py
pytest -q tests/test_wave4_low_rank_coupling_validation.py
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave4_low_rank_coupling_validation.py --mode full --output docs/benchmarks/scalable-ot-wave4-low-rank-coupling-validation-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-wave4-low-rank-coupling-validation-2026-06-20.md
```

## Forbidden Claims And Actions

- Do not rank low-rank against positive-feature.
- Do not select a default or public API path.
- Do not claim speedup, superiority, posterior correctness, HMC readiness,
  production readiness, dense Sinkhorn equivalence, full low-rank Sinkhorn
  solver-fidelity, or broad scalable-OT selection.
- Do not edit current-agent Wave 4 outputs.
- Do not change thresholds after seeing results.
- Do not use a different fixture/seed grid unless writing a blocker.

## Handoff Back To Coordinator

When complete, write the low-rank lane result artifact and make sure it states:

- hard vetoes;
- viable or blocked lane status;
- whether any ranking is statistically supported, expected to be `none`;
- descriptive-only differences;
- default-readiness status, expected to be `not assessed`;
- next evidence needed.

Final merge will not run until your result and JSON artifact exist.
