# Phase 1 Result: Full-Row LGSSM GPU/XLA Score Gate

Date: 2026-07-04

Status: `BLOCKED_GPU_MEMORY_OOM`

## Decision

Phase 1 executed and is blocked.

The phase plan and launcher were reviewed and patched, and Claude
`VERDICT: AGREE` was obtained on the bounded Phase 1 packet. The trusted GPU
launch did start, XLA compiled the cluster, and the run then aborted with a
real GPU out-of-memory failure inside `SelfAdjointEigV2`.

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Blocked by GPU memory exhaustion in the full-row manual-reverse route. |
| Primary criterion status | Not reached: the full-row run aborted before a result artifact was written. |
| Veto diagnostic status | Triggered: `RESOURCE_EXHAUSTED` OOM when allocating a tensor in `SelfAdjointEigV2` on GPU. |
| Main uncertainty | Whether the full-row manual-reverse score gate can be made memory-safe without changing the target or route contract. |
| Next justified action | Reduce the memory footprint with a reviewed route change or smaller diagnostic, then rerun Phase 1 only if the full-row contract is preserved. |
| Not concluded | No full-row score admission, no score correctness claim, no usable phase result artifact from the benchmark, and no leaderboard promotion. |

## Evidence Contract Result

| Field | Status |
| --- | --- |
| Question | Can the full `T=50` LGSSM LEDH row be admitted from the same-target manual-reverse value/score route? |
| Primary criterion | Not satisfied because the benchmark aborted before emitting the phase result artifact. |
| Veto diagnostics | GPU OOM in `SelfAdjointEigV2` while the trusted GPU run was active. |
| Explanatory diagnostics | The subplan and launcher passed local syntax and diff checks, Claude re-review returned `VERDICT: AGREE`, XLA compiled the cluster, and the GPU remained active until OOM. |
| Not concluded | No score admission, no value admission beyond the existing diagnostic artifact, and no row correctness claim. |

## Checks Run

- `bash -n scripts/run_phase1_lgssm_full_row_manual_reverse_gpu.sh`
- `git diff --check -- docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase1-lgssm-full-row-subplan-2026-07-04.md scripts/run_phase1_lgssm_full_row_manual_reverse_gpu.sh`
- Claude read-only bounded review of the Phase 1 packet: `VERDICT: REVISE`
- Claude read-only bounded re-review of the patched Phase 1 packet: `VERDICT: AGREE`
- Trusted GPU launcher command ran and aborted with GPU OOM in `SelfAdjointEigV2`

## Nonclaims

- This does not prove the score route is wrong.
- This does not admit the LGSSM row.
- This does not certify GPU readiness.
- This does not certify HMC readiness.

## Handoff

Phase 1 is blocked by GPU memory exhaustion. The trusted GPU launch was
granted but failed on memory.

The next attempt must be a reviewed memory-safe route change or a smaller
diagnostic that still preserves the full-row contract before promotion.

`bash scripts/run_phase1_lgssm_full_row_manual_reverse_gpu.sh`
