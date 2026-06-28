# Nystrom Algorithm-Complete Reset Memo

Date: 2026-06-21T19:27:26+08:00

Status: `RESET_FOR_NEW_SESSION`

## Purpose

This memo restarts the fixed-rank Nystrom kernel Sinkhorn lane cleanly after
repeated stream disconnects during P01 setup.  It is a handoff artifact for a
fresh Codex session.  No P01 implementation files were successfully created in
this session.

## Current Lane

Algorithm under test: fixed-rank Nystrom kernel Sinkhorn for
LEDH-PFPF-OT resampling.

Lane objective: implement and test Nystrom thoroughly enough that it can later
enter a common scalable-OT screening leaderboard as a real diagnostic candidate.

Current repository default: streaming GPU TF32 LEDH-PFPF-OT remains the
production/default target.  This Nystrom lane is diagnostic only and must not
change defaults.

## Completed State

P00 is complete and closed with status:

- `P00_GOVERNANCE_SOURCE_LOCK_PASSED`

Claude review state:

- Round 1 returned `VERDICT: REVISE`.
- The master program/subplans were patched for exact thresholds, commands, GPU
  rules, and schema fields.
- Round 2 returned `VERDICT: AGREE`.

Main planning artifacts already written:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-master-program-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-visible-gated-execution-runbook-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-claude-review-ledger-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-visible-execution-ledger-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-visible-stop-handoff-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p00-governance-result-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p01-implementation-harness-subplan-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p02-small-reference-subplan-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p03-downstream-smoke-subplan-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p04-gpu-scale-subplan-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p05-closeout-subplan-2026-06-21.md`

## Not Completed

P01 has not been implemented.

These required P01 artifacts do not yet exist and should be created next:

- `docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py`
- `tests/test_nystrom_ledh_pfpf_algorithm_complete.py`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p01-implementation-harness-result-2026-06-21.md`

No P01 checks have been run.

## Existing Source Route

Candidate implementation:

- `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`

Existing focused tests:

- `tests/test_nystrom_transport_tf.py`
- `tests/test_nystrom_transport_tf_independent.py`

Useful prior diagnostics:

- `docs/benchmarks/scalable_ot_p11_reduced_rank_nystrom_ladder_diagnostics.py`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-reduced-rank-nystrom-ladder-result-2026-06-18.md`

Useful harness patterns:

- `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py`
- `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_integration_smoke.py`
- `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py`

## Next Phase To Execute

Start at P01:

- Read
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p01-implementation-harness-subplan-2026-06-21.md`.
- Restate the P01 evidence contract before editing.
- Implement the harness and tests.
- Run the exact P01 checks.
- Write the P01 result.
- Refresh/review P02 before running P02.

Exact P01 required checks:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py tests/test_nystrom_ledh_pfpf_algorithm_complete.py
```

```bash
pytest -q tests/test_nystrom_transport_tf.py tests/test_nystrom_ledh_pfpf_algorithm_complete.py
```

## P02 Thresholds To Preserve

Required small-reference fixtures and ranks:

| Fixture | Particle count | Ranks |
| --- | ---: | --- |
| `tiny_manual` | 4 | `2,3,4` |
| `small_parity` | 8 | `2,4,8` |
| `high_dim_low_rank` | 32 | `2,4,8,16,32` |
| `ledh_specific_smoke` | 32 | `4,8,16,32` |

Promoted-rank thresholds:

- max row residual <= `5.0e-2`;
- max column residual <= `5.0e-2`;
- max dense-reference transported-particle error <= `7.5e-2`;
- RMS dense-reference transported-particle error <= `3.0e-2`;
- finite factors and finite transported particles required;
- candidate transport matrix shape must end in `[0, 0]`;
- at least one rank per fixture must pass.

Important: do not silently inherit older Phase 1 fixture particle counts for
P02.  The reviewed P02 plan requires the smaller counts listed above.

## P03 Rows To Preserve

Required CPU downstream smoke rows:

- `nystrom_ledh_smoke_n64_rank8`: `N=64`, rank `8`, `T=2`, `D=6`, `M=4`
- `nystrom_ledh_smoke_n128_rank16`: `N=128`, rank `16`, `T=2`, `D=6`, `M=4`

Thresholds:

- output log-weight normalization residual <= `1.0e-6`;
- ESS fraction >= `1.0e-2`;
- max Nystrom row residual <= `5.0e-2`;
- max Nystrom column residual <= `5.0e-2`;
- finite log likelihood, summaries, final particles, final log weights,
  factors, and scalings;
- no dense transport matrix.

## P04 GPU Policy To Preserve

GPU preference from user:

- use physical GPU1 unless it is busy or unsuitable;
- if GPU1 is busy/unsuitable, use physical GPU0 if usable.

Busy/unsuitable rule:

- GPU absent;
- total memory used >= `2048 MiB`;
- utilization >= `20%`;
- any non-display compute process uses >= `2048 MiB`.

Required GPU rows:

- `N=1024`, rank `16`, `T=2`, `D=8`, `M=6`
- `N=4096`, rank `32`, `T=2`, `D=8`, `M=6`
- `N=8192`, rank `32`, `T=2`, `D=8`, `M=6`

Optional row:

- `N=16384`, rank `64`, `T=2`, `D=8`, `M=6`, only if required rows pass and
  elapsed P04 wall time is at most 45 minutes.

P04 budget:

- phase wall-clock budget: `7200` seconds;
- per-row timeout: `1200` seconds.

## Required JSON Schema Fields

P02-P04 JSON artifacts must include:

- `algorithm_family`
- `mode`
- `status`
- `hard_vetoes`
- `run_manifest`
- `source_route`
- `source_route_components`
- `semantic_class`
- `baseline_comparator`
- `transport_object_kind`
- `transport_matrix_materialized`
- `nonclaims`

Per-row fields must include rank, landmark indices, residuals, finite checks,
output shape, transport-matrix shape, and timing fields.

## Forbidden Claims And Actions

Do not claim:

- Nystrom helps LEDH yet;
- speedup;
- ranking;
- production/default readiness;
- posterior correctness;
- HMC readiness;
- public API readiness;
- dense Sinkhorn equivalence beyond the checked small fixtures.

Do not:

- change the default route;
- commit or push unless explicitly requested;
- start a screening leaderboard automatically;
- use NumPy as the BayesFilter algorithm backend except for fixtures,
  reporting, and independent reference inspection.

## Worktree Warning

The worktree is dirty with many unrelated artifacts from other lanes, including
HMC/default-quality/low-rank files.  Preserve unrelated changes.  Treat the
Nystrom algorithm-complete owned write set as:

- `docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py`
- `tests/test_nystrom_ledh_pfpf_algorithm_complete.py`
- Nystrom algorithm-complete plan/result/ledger files under `docs/plans`
- Nystrom algorithm-complete benchmark JSON/Markdown/log artifacts under
  `docs/benchmarks`

Do not revert or clean unrelated files.

## Suggested P01 Implementation Shape

Implement one dedicated harness with modes:

- `small-reference`;
- `downstream-smoke`;
- `gpu-scale`.

Recommended structure:

- deterministic small-reference fixture builder with the reviewed P02 counts;
- dense TensorFlow `annealed_transport_resample_tf` comparator only for
  `small-reference`;
- Nystrom route through `nystrom_transport_resample_tf`;
- deterministic LGSSM-shaped LEDH loop for downstream smoke and GPU scale,
  adapted from the low-rank integration/efficiency harnesses;
- top-level and row-level nonclaims and hard-veto fields;
- row-subprocess timeout support for P04;
- no default-route changes.

## Immediate Restart Checklist

1. Read this reset memo and the P01 subplan.
2. Confirm `docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py`
   and `tests/test_nystrom_ledh_pfpf_algorithm_complete.py` still do not
   exist.
3. Implement P01 only.
4. Run P01 exact checks.
5. Write P01 result and update the visible execution ledger.
6. Refresh/review P02 before running P02.

