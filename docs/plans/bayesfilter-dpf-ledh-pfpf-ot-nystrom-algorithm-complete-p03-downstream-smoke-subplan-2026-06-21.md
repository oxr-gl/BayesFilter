# P03 Subplan: Downstream LEDH Smoke

Date: 2026-06-21

Status: `DRAFT_DEPENDS_ON_P02`

## Phase Objective

Run a CPU-scoped downstream LEDH/PFPF-OT smoke using Nystrom resampling inside
the filtering loop, with finite output, ESS, log-weight normalization, and
nonmaterialized transport gates.

## Entry Conditions Inherited From Previous Phase

- P02 passed small dense-reference validation.
- P02 selected or recorded viable ranks for the smoke configuration.
- The route remains diagnostic and non-default.

## Required Artifacts

- JSON:
  `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.json`
- Markdown:
  `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.md`
- Log:
  `docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.log`
- P03 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p03-downstream-smoke-result-2026-06-21.md`
- Refreshed P04 subplan.

## Required Checks, Tests, Reviews

- Exact command:

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py --mode downstream-smoke --device-scope cpu --output docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.json --markdown-output docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.md > docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.log 2>&1
```

- Exact JSON parse command:

```bash
python -m json.tool docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.json
```

- Local review of hard-veto and nonclaim fields.
- Claude review if the phase result would promote beyond diagnostic
  leaderboard-readiness.

## Predeclared Smoke Rows And Thresholds

Required CPU rows:

| Fixture id | N | Rank | Time steps | State dim | Obs dim |
| --- | ---: | ---: | ---: | ---: | ---: |
| `nystrom_ledh_smoke_n64_rank8` | 64 | 8 | 2 | 6 | 4 |
| `nystrom_ledh_smoke_n128_rank16` | 128 | 16 | 2 | 6 | 4 |

Thresholds:

- output log-weight normalization residual: at most `1.0e-6`;
- ESS fraction minimum: at least `1.0e-2`;
- max Nystrom row residual: at most `5.0e-2`;
- max Nystrom column residual: at most `5.0e-2`;
- finite log likelihood, summaries, final particles, final log weights,
  factors, and scalings: required;
- no candidate dense transport matrix: required.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Nystrom resampling run through an LEDH/PFPF-OT filtering loop without hard smoke failures? |
| Baseline/comparator | Same-harness streaming context is explanatory; this phase primarily checks Nystrom route self-consistency. |
| Primary criterion | Both predeclared Nystrom rows produce finite log likelihood, filtered summaries, ESS, final particles/log weights, normalized output weights, finite factors/scalings, residuals below exact thresholds, and no dense transport matrix. |
| Veto diagnostics | Nonfinite output, zero transport invocations, log-weight normalization above `1.0e-6`, ESS fraction below `1.0e-2`, row/column residual above `5.0e-2`, dense transport materialization, missing rank/landmark metadata. |
| Explanatory diagnostics | State-mean context versus streaming, wall time, memory metadata, step diagnostics. |
| Not concluded | No posterior correctness, no speedup, no ranking, no default readiness, no HMC readiness. |
| Artifact | P03 JSON/Markdown and result. |

## Forbidden Claims And Actions

- Do not call the smoke a posterior validation.
- Do not rank Nystrom against streaming from one smoke.
- Do not change default route.

## Exact Next-Phase Handoff Conditions

P04 may begin only after:

- P03 hard vetoes are empty;
- P03 result records route and downstream diagnostics;
- trusted GPU phase remains justified and P04 subplan is refreshed.

## Stop Conditions

- Nystrom cannot run in the filtering loop.
- Hard vetoes fire for non-harness reasons.
- GPU phase would answer a different question than the P03 result supports.
