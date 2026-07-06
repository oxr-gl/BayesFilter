# Claude Review Ledger: Low-Rank LEDH/PFPF-OT Efficiency Validation

Date: 2026-06-21

Status: `ROUND_2_REVIEW_AGREE`

Claude is read-only reviewer only.  Codex remains supervisor and executor.

## Review Rounds

### 2026-06-21T03:38:46+08:00 - Round 1 Attempt

Review scope:

- Single absolute master-program path:
  `/home/ubuntu/python/BayesFilter/docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-master-program-2026-06-21.md`
- Claude would be instructed to inspect only same-prefix `docs/plans` paths
  named inside that master program.

Outcome:

- The local approval reviewer rejected the Claude worker command because the
  prior informed approval was specific to a different plan path/review.
- No Claude review result was obtained.
- Codex did not attempt a workaround or indirect execution.

Required human action:

- Explicitly approve this concrete action: Claude Code may read
  `/home/ubuntu/python/BayesFilter/docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-master-program-2026-06-21.md`
  and the same-prefix `docs/plans` paths named inside it, and may transmit
  their contents to the external Claude service for read-only review.

### 2026-06-21T03:38:46+08:00 - Approval Received

Outcome:

- User approved the concrete path-only Claude review transfer.
- Codex reran the same path-only read-only review.

### 2026-06-21T03:38:46+08:00 - Round 1 Review

Log:

- `docs/benchmarks/logs/low-rank-ledh-pfpf-efficiency-plan-review-r1.log`

Outcome:

- `VERDICT: REVISE`

Material findings:

- The paired screen was too small to answer the large-particle efficiency
  question.
- Resource proxies lacked a bounded output-comparability gate.
- Streaming/OOM/timeout policy lacked numeric row timeouts.
- Large-N wording drifted from streaming comparator to dense infeasibility.
- TF32 state was explanatory rather than a hard gate.
- Same-GPU rules for a paired claim were incomplete.
- Operative GPU and Claude path-only rules relied on `memory.md` rather than
  being self-contained in the reviewed plan set.

Repair:

- Master program and P00-P04/runbook were patched visibly.
- Paired ladder now extends through `[1024, 2048, 4096, 8192, 16384, 32768,
  50000, 100000]` until streaming reaches a fixed timeout/OOM/failure.
- P02 timeout is fixed at `900s` per route per row; P03 low-rank timeout is
  fixed at `1200s` per row.
- TF32 parity, same physical GPU, and bounded output-comparability are hard
  gates for efficiency claims.
- Low-rank-only 50k/100k rows are explicitly unpaired executable-envelope
  evidence, not streaming superiority evidence.
- GPU selection and Claude path-only review rules are inlined in the master
  program and runbook.

Next:

- Run focused local checks, then request round 2 path-only Claude review.

### 2026-06-21T04:01:33+08:00 - Round 2 Review

Log:

- `docs/benchmarks/logs/low-rank-ledh-pfpf-efficiency-plan-review-r2.log`

Outcome:

- `VERDICT: AGREE`

Summary:

- Claude agreed that the repaired plan now bounds the large-N efficiency
  question correctly, extends the paired ladder upward, adds numeric timeouts,
  makes TF32 and same-GPU rules hard gates, adds bounded
  output-comparability gates, prevents dense-baseline drift, and inlines the
  operative review/GPU rules.

Decision:

- P00 review gate converged.
- Proceed to P01 lane-owned harness implementation and small sanity checks.

### 2026-06-21T05:07:21+08:00 - P02 Result Review Round 1

Log:

- in-session Claude worker output; focused review of the master program,
  P02 result, and named P02 benchmark artifacts.

Outcome:

- `VERDICT: REVISE`

Material finding:

- The `N=32768` executable-envelope claim relied on a reconstructed missing
  streaming timeout row rather than direct route-fired evidence.  Claude
  correctly identified that this conflicted with the master-program promotion
  veto for missing route-fired evidence or invalid comparator artifacts.

Repair:

- Patched `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py` so
  the parent subprocess timeout handler writes a timeout JSON/Markdown sidecar
  at the expected row artifact path.
- Added a regression test in
  `tests/test_low_rank_ledh_pfpf_efficiency.py`.
- Reran focused checks:
  `python -m py_compile docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py`
  and
  `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_low_rank_ledh_pfpf_efficiency.py -q`.
- Reran only the missing `streaming,N=32768` row on trusted GPU1 with the fixed
  `900s` child timeout under a `1200s` outer guard.  The row wrote
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21-row-streaming-n32768.json`
  with `artifact_role: parent_enforced_row_timeout_sidecar`,
  `status: TIMEOUT`, and `timeout_status: timeout_enforced`.
- Refreshed the full P02 aggregate from row artifacts in trusted GPU context,
  preserving the paired rows and restoring a valid GPU/TF32 manifest.

Next:

- Request P02 result review round 2.

### 2026-06-21T05:34:08+08:00 - P02 Result Review Round 2

Outcome:

- `VERDICT: AGREE`

Summary:

- Claude agreed that the reconstructed-timeout blocker was repaired by a direct
  parent-enforced timeout sidecar for `streaming,N=32768`.
- Claude agreed that P02 now preserves same-GPU/TF32 gates, feasible-row
  comparability, speed-only bounded paired support, no memory-improvement
  claim, no unpaired `N=50000/100000` streaming superiority claim, and all
  required non-claims.

Decision:

- P02 review gate converged.
- Proceed to P03 and P04.

### 2026-06-21T05:44:02+08:00 - P04 Final Closeout Review

Outcome:

- `VERDICT: AGREE`

Summary:

- Claude agreed that the final claim class
  `LOW_RANK_LEDH_EFFICIENCY_SUPPORTED_BOUNDED` is within the master contract.
- Claude agreed that the final result limits paired efficiency support to the
  feasible paired speed-screen rows, keeps `N=32768` as direct
  executable-envelope support, keeps `N=50000/100000` as low-rank-only
  executable-envelope evidence, avoids a memory-improvement claim, avoids
  unpaired streaming superiority claims, and preserves posterior/default/HMC/API
  and other non-claims.

Decision:

- P04 review gate converged.
- Lane closeout is complete.
