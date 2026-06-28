# Final Result: Low-Rank LEDH-PFPF-OT TF32 Scale Smoke

Date: 2026-06-20
Owner: peer agent
Supervisor/executor: Codex

## Final Status

`AMENDED_TUNED_GPU_SCALE_PASSED_DIAGNOSTIC_ONLY`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Amend prior closeout and rerun with tuning | P00/P01 passed; old P02 amended; tuning found `rank=64`, `epsilon=0.015625`; tuned medium CPU and trusted GPU scale passed | No hard vetoes for tuned medium CPU or trusted GPU `N=50000,100000` | Whether this remains viable across real LEDH/PFPF filtering workloads and replications | Hand off tuned diagnostic evidence for coordinator synthesis or a separately planned integration benchmark | No speedup, ranking, TF32-help, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, full solver fidelity, or broad scalable-OT selection |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Tuned medium CPU and trusted GPU scale no-dense gates passed for `rank=64`, `assignment_epsilon=0.015625`. |
| Statistically supported ranking | None. No comparison or ranking was run. |
| Descriptive-only differences | Runtime, memory, TF32 metadata, projection iterations, and candidate-vs-naive moment deltas are explanatory only. |
| Default-readiness | Not supported. |
| Next evidence needed | Separate integration benchmark on the actual LEDH/PFPF filtering path if the coordinator wants evidence beyond component scale smoke. |

## Artifact Trail

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-master-program-2026-06-20.md`
- P00 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p00-governance-result-2026-06-20.md`
- P01 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p01-harness-invariants-result-2026-06-20.md`
- P02 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02-medium-cpu-result-2026-06-20.md`
- P02A tuning result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02a-tuning-result-2026-06-20.md`
- P02B focused tuning result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02b-focused-tuning-result-2026-06-20.md`
- P02C tuned medium CPU result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02c-medium-cpu-tuned-result-2026-06-20.md`
- P03 trusted GPU scale result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p03-trusted-gpu-scale-result-2026-06-20.md`
- Small diagnostic JSON/Markdown:
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-small-2026-06-20.json`
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-small-2026-06-20.md`
- Medium CPU diagnostic JSON/Markdown/log:
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.json`
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.md`
  `docs/benchmarks/logs/low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.log`
- Tuning diagnostic JSON/Markdown/log:
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-tuning-cpu-2026-06-20.json`
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-tuning-cpu-2026-06-20.md`
  `docs/benchmarks/logs/low-rank-tf32-scale-smoke-tuning-cpu-2026-06-20.log`
- Focused tuning diagnostic JSON/Markdown/log:
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-focused-tuning-cpu-2026-06-20.json`
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-focused-tuning-cpu-2026-06-20.md`
  `docs/benchmarks/logs/low-rank-tf32-scale-smoke-focused-tuning-cpu-2026-06-20.log`
- Tuned medium CPU diagnostic JSON/Markdown/log:
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-tuned-2026-06-20.json`
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-tuned-2026-06-20.md`
  `docs/benchmarks/logs/low-rank-tf32-scale-smoke-medium-cpu-tuned-2026-06-20.log`
- Tuned trusted GPU scale diagnostic JSON/Markdown/log:
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-gpu-scale-tuned-2026-06-20.json`
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-gpu-scale-tuned-2026-06-20.md`
  `docs/benchmarks/logs/low-rank-tf32-scale-smoke-gpu-scale-tuned-2026-06-20.log`

## Checks Actually Run

- `python -m py_compile docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py tests/test_low_rank_tf32_scale_smoke.py`
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_low_rank_tf32_scale_smoke.py`
- CPU-hidden P01 small diagnostic.
- JSON parse and manifest checks for P01/P02.
- CPU-hidden P02 medium diagnostic with `timeout 300`.
- CPU-hidden P02A coarse tuning diagnostic.
- CPU-hidden P02B focused tuning diagnostic.
- CPU-hidden P02C tuned medium CPU diagnostic.
- Trusted GPU P03 scale diagnostic at `N=50000` and conditional `N=100000`.
- Trusted GPU P03 metadata refresh rerun with explicit `--phase-id LR-TF32-3`
  and P03 phase-result path in the recorded command.
- JSON parse checks for tuned CPU/GPU diagnostics.
- Forbidden claim/boundary scans for lane artifacts.
- Claude amended-closeout read-only review returned `VERDICT: AGREE` with only
  nonblocking wording/provenance nits, both patched.

## Result Summary

P00 governance converged with Claude after two rounds.  P01 harness and tiny
invariants passed after a focused repair that kept small-mode moment errors
explanatory and reserved downstream moment hard vetoes for P02/P03.

Amendment: the previous P02 interpretation was wrong.  P02 ran one untuned
fixed CPU-hidden medium setting at `N=4096` and `N=8192` with `B=2`, `D=8`,
`rank=64`, `assignment_epsilon=0.5`, and `dtype=float32`.  The run wrote
complete JSON/Markdown/log artifacts and an embedded manifest.  The route did
not materialize a dense scale transport matrix and passed finite/sign/residual
and log-weight checks.  It failed weighted second-moment preservation:

- `N=4096`: `2.9352012276649475e-01` versus threshold `7.5e-02`;
- `N=8192`: `2.935119569301605e-01` versus threshold `7.5e-02`.

Those failures are now classified as tuning signals only.  They do not reject
the route or candidate family.  The planning error was applying the downstream
moment hard gate before a tuning phase.

Coarse tuning found no viable row but showed that decreasing
`assignment_epsilon` improved second-moment preservation.  Focused tuning found
the viable setting `rank=64`, `assignment_epsilon=0.015625`.  A renewed medium
CPU no-dense gate passed at `N=4096` and `N=8192` with weighted second-moment
errors approximately `6.984e-02`, below the `7.5e-02` threshold.

Trusted GPU scale then ran with the tuned setting on GPU 1 under trusted
execution.  Both `N=50000` and conditional `N=100000` passed without dense
scale materialization or hard vetoes.  Weighted second-moment errors were
approximately `6.983e-02`, below the `7.5e-02` threshold.

After Claude's amended-closeout review, the GPU diagnostic was rerun with
explicit phase metadata in the recorded command.  The rerun preserved status
`PASS`, phase `LR-TF32-3`, empty hard vetoes, no dense scale materialization,
and maximum weighted second-moment error `6.983824074268341e-02`.

## Post-Run Red Team

Strongest alternative explanation:

- The tuned route may be passing a deterministic component fixture while still
  failing to preserve the quantities that matter inside full LEDH/PFPF
  filtering workloads, or the selected `assignment_epsilon` may be
  fixture-specific.  This lane does not test posterior correctness or full
  filtering integration.

What would overturn this lane decision:

- A separately planned integration benchmark or replicated fixture ladder could
  show that the tuned setting fails hard validity checks, materializes dense
  scale transport, cannot complete at target scale, or does not preserve the
  needed downstream quantities.

Weakest part of the evidence:

- This is still a component scale smoke on deterministic synthetic
  LEDH/PFPF-shaped fixtures, not posterior correctness or full filtering
  evidence.

## Non-Claims

- No speedup claim.
- No ranking claim.
- No superiority claim.
- No posterior correctness claim.
- No HMC readiness claim.
- No public API readiness claim.
- No production/default readiness claim.
- No dense Sinkhorn equivalence claim.
- No full low-rank Sinkhorn solver-fidelity claim.
- No broad scalable-OT selection claim.
- No TF32-help claim.
