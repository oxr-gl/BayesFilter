# P04 Subplan: Trusted GPU Scale Envelope

Date: 2026-06-21

Status: `DRAFT_DEPENDS_ON_P03`

## Phase Objective

Run a bounded trusted-GPU Nystrom scale envelope with GPU1 preferred unless
busy/unsuitable, recording finite output, nonmaterialized transport, device,
TF32, runtime, and memory metadata.

## Entry Conditions Inherited From Previous Phase

- P03 downstream smoke passed.
- Nystrom remains diagnostic/non-default.
- GPU usage follows the user directive: use GPU1 unless busy, then GPU0.

## Required Artifacts

- JSON:
  `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.json`
- Markdown:
  `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.md`
- Log:
  `docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.log`
- P04 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p04-gpu-scale-result-2026-06-21.md`
- Refreshed P05 subplan.

## Required Checks, Tests, Reviews

- Trusted `nvidia-smi` preflight.
- Select GPU1 unless absent/busy/unsuitable; otherwise select GPU0 if usable.
- Exact command, after replacing `<physical_gpu>` with the selected physical
  GPU index:

```bash
CUDA_VISIBLE_DEVICES=<physical_gpu> timeout 7200 python docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py --mode gpu-scale --device-scope visible --cuda-visible-devices <physical_gpu> --output docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.json --markdown-output docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.md > docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.log 2>&1
```

- Exact JSON parse command:

```bash
python -m json.tool docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.json
```

- Local result review for device and nonclaim boundaries.

## Predeclared GPU Rows, Budgets, And Thresholds

Required rows:

| N | Rank | Time steps | State dim | Obs dim |
| ---: | ---: | ---: | ---: | ---: |
| 1024 | 16 | 2 | 8 | 6 |
| 4096 | 32 | 2 | 8 | 6 |
| 8192 | 32 | 2 | 8 | 6 |

Optional row: `N=16384`, rank `64`, time steps `2`, state dim `8`, obs dim
`6`; attempt only if all required rows pass and elapsed P04 wall time is at
most 45 minutes.

Budgets:

- phase wall-clock budget: `7200` seconds;
- per-row timeout inside harness: `1200` seconds.

GPU busy/unsuitable rule:

- Prefer physical GPU1 unless absent, total memory used is at least `2048 MiB`,
  utilization is at least `20%`, or any non-display compute process uses at
  least `2048 MiB`.
- Use physical GPU0 only if GPU1 is busy/unsuitable by the same rule and GPU0
  is usable.
- Stop and write a blocker if neither GPU is usable.

Thresholds:

- output log-weight normalization residual: at most `1.0e-6`;
- ESS fraction minimum: at least `1.0e-2`;
- max Nystrom row residual: at most `5.0e-2`;
- max Nystrom column residual: at most `5.0e-2`;
- finite outputs, factors, and scalings: required;
- TF32 execution recorded enabled for float32 rows: required;
- GPU output device evidence: required;
- no candidate dense transport matrix: required.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Nystrom run on GPU at bounded medium/large particle counts without hard operational failures? |
| Baseline/comparator | Same candidate route across predeclared GPU particle ladder; streaming default context is explanatory only. |
| Primary criterion | All required GPU rows pass exact thresholds with finite outputs, GPU device evidence, TF32 enabled for float32, no dense transport matrix, complete artifacts, and no hard vetoes. |
| Veto diagnostics | GPU unavailable by predeclared rule, CPU fallback, OOM/timeout on required row, nonfinite output, residual/ESS/log-weight threshold failure, dense transport materialization, wrong GPU selection record, unrelated GPU contamination, or missing artifact. |
| Explanatory diagnostics | Runtime, memory info, compile/eager overhead, optional larger rows, streaming context if recorded. |
| Not concluded | No statistical speedup, no default change, no posterior correctness, no HMC readiness, no public API readiness, no broad large-N guarantee. |
| Artifact | P04 JSON/Markdown and result. |

## Forbidden Claims And Actions

- Do not claim production/default readiness.
- Do not infer statistical ranking from one GPU ladder.
- Do not continue if selected GPU is contaminated by unrelated compute.

## Exact Next-Phase Handoff Conditions

P05 may begin only after:

- P04 JSON/Markdown exist and parse, or a blocker result explains why GPU phase
  could not run;
- P04 result records GPU selection and hard-veto status;
- P05 subplan is refreshed and reviewed.

## Stop Conditions

- No usable trusted GPU is available.
- Required row times out/OOMs for candidate-route reasons.
- Device evidence shows CPU fallback.
