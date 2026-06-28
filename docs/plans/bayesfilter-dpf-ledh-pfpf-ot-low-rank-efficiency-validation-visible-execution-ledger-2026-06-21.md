# Visible Execution Ledger: Low-Rank LEDH/PFPF-OT Efficiency Validation

Date: 2026-06-21

Status: `COMPLETE`

## Entries

### Phase P00 - Governance, Review, And GPU Preflight

Status: `P00_PASSED`

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-master-program-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p00-governance-result-2026-06-21.md`
- `docs/benchmarks/logs/low-rank-ledh-pfpf-efficiency-plan-review-r1.log`
- `docs/benchmarks/logs/low-rank-ledh-pfpf-efficiency-plan-review-r2.log`

Outcome:

- User approved path-only Claude review for the efficiency master program.
- Claude review round 1 returned `VERDICT: REVISE`.
- Codex patched the master program to add large-N paired ladder, fixed numeric
  timeouts, TF32/same-GPU hard gates, output-comparability gates, and explicit
  unpaired large-N non-claims.
- Claude review round 2 returned `VERDICT: AGREE`.
- GPU1 selected via `CUDA_VISIBLE_DEVICES=1`.

### Phase P01 - Harness And Small Sanity

Status: `P01_PASSED`

Artifacts:

- `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py`
- `tests/test_low_rank_ledh_pfpf_efficiency.py`
- `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-small-2026-06-21.json`
- `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-small-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p01-harness-result-2026-06-21.md`

Checks:

- `python -m py_compile docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_low_rank_ledh_pfpf_efficiency.py -q`
- CPU small harness run.

Outcome:

- Both streaming and low-rank routes ran on the common small fixture.
- Sentinel transport shapes, finite outputs, low-rank diagnostics, and
  bounded comparability fields were emitted.

### Phase P02 - Paired GPU Efficiency Screen

Status: `P02_PASSED_BOUNDED_RESOURCE_PROXY_AND_ENVELOPE_AFTER_TIMEOUT_REPAIR`

Artifacts:

- `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.json`
- `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.md`
- `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21-row-streaming-n32768.json`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p02-paired-gpu-result-2026-06-21.md`

Checks:

- Focused compile/test checks passed after timeout-sidecar repair.
- JSON consistency check passed for aggregate status, TF32, GPU manifest, direct
  timeout sidecar, adjacent speed-screen support, and non-claim boundaries.
- Claude P02 review round 1 returned `VERDICT: REVISE`.
- Repair loop wrote direct timeout sidecar and reran focused checks.
- Claude P02 review round 2 returned `VERDICT: AGREE`.

Outcome:

- Paired rows through `N=16384` passed output comparability.
- Speed screen passed on adjacent feasible rows `N=2048`, `4096`, `8192`, and
  `16384`.
- Memory screen did not pass.
- Streaming timed out at `N=32768` under the fixed `900s` row timeout with a
  route-fired parent-enforced timeout sidecar; low-rank passed `N=32768`.

### Phase P03 - Large-N Low-Rank Executable Envelope

Status: `P03_PASSED_LOW_RANK_LARGE_N_ENVELOPE_ONLY`

Artifacts:

- `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.json`
- `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.md`
- `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21-row-low_rank-n50000.json`
- `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21-row-low_rank-n100000.json`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p03-large-n-result-2026-06-21.md`

Command:

`timeout 3000 python docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py --mode large-n --cuda-visible-devices 1 --output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.json --markdown-output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.md --quiet`

Outcome:

- Low-rank `N=50000` and `N=100000` rows passed under the fixed `1200s` row
  timeout on GPU1 with TF32 recorded enabled.
- Rows had finite outputs, no materialized dense transport matrix, and factor
  residuals below threshold.
- Evidence is low-rank-only executable-envelope evidence, not unpaired speed or
  superiority evidence.

### Phase P04 - Final Closeout

Status: `LOW_RANK_LEDH_EFFICIENCY_SUPPORTED_BOUNDED`

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-result-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-visible-stop-handoff-2026-06-21.md`

Outcome:

- Final result classifies evidence as bounded resource-proxy efficiency support
  plus executable-envelope support.
- Non-claims are preserved: no posterior correctness, HMC readiness, public
  API readiness, production/default readiness, dense Sinkhorn equivalence,
  broad scalable-OT selection, memory improvement, statistically supported
  ranking, or unpaired 50k/100k streaming superiority.
