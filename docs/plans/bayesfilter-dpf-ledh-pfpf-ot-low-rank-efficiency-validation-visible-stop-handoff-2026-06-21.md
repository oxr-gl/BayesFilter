# Visible Stop Handoff: Low-Rank LEDH/PFPF-OT Efficiency Validation

Date: 2026-06-21

Status: `COMPLETE`

## Final Claim Class

`LOW_RANK_LEDH_EFFICIENCY_SUPPORTED_BOUNDED`

## What Was Established

Under the governed synthetic LEDH/PFPF-OT TF32 benchmark:

- low-rank passed the paired speed-screen on adjacent feasible rows
  `N=2048`, `4096`, `8192`, and `16384` after validity, TF32, same-GPU, and
  bounded output-comparability gates;
- streaming timed out at `N=32768` under the fixed `900s` row timeout with a
  route-fired parent-enforced timeout sidecar, while low-rank passed the same
  `N=32768` row;
- low-rank completed low-rank-only large-N rows at `N=50000` and `N=100000`
  under P03 with finite outputs, no materialized dense transport matrix, and
  factor residuals below threshold.

## Key Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-master-program-2026-06-21.md`
- Final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-result-2026-06-21.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-visible-execution-ledger-2026-06-21.md`
- P02 paired artifact:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.json`
- P02 streaming timeout sidecar:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21-row-streaming-n32768.json`
- P03 large-N artifact:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.json`

## Review State

- Master plan Claude review converged at `VERDICT: AGREE`.
- P02 result Claude review initially returned `VERDICT: REVISE` because the
  `N=32768` streaming timeout was reconstructed rather than route-fired.
- Codex repaired the harness to write a direct parent-enforced timeout sidecar,
  reran the targeted row on GPU1, refreshed the P02 aggregate in trusted GPU
  context, reran focused checks, and Claude returned `VERDICT: AGREE`.

## Boundaries

Do not treat this result as evidence of:

- posterior correctness;
- HMC readiness;
- public API readiness;
- production/default readiness;
- dense Sinkhorn equivalence;
- broad scalable-OT selection;
- memory improvement;
- statistically supported ranking;
- streaming superiority at unpaired `N=50000` or `N=100000`.

## Suggested Next Program

If this lane feeds an integration decision, the next program should test real
target workloads and posterior-quality/default-readiness gates separately.  The
current lane supports an optional efficiency route investigation, not a public
default change.
