# P02 Subplan: Small Dense-Reference Validation

Date: 2026-06-21

Status: `DRAFT_DEPENDS_ON_P01`

## Phase Objective

Run small dense-reference validation for Nystrom ranks on deterministic
fixtures, preserving exact dense TensorFlow transport as the small-N comparator.

## Entry Conditions Inherited From Previous Phase

- P01 harness and tests passed.
- Harness can emit JSON/Markdown artifacts.
- Dense reference is allowed only for small-N validity.

## Required Artifacts

- JSON:
  `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.json`
- Markdown:
  `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.md`
- Log:
  `docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.log`
- P02 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p02-small-reference-result-2026-06-21.md`
- Refreshed P03 subplan.

## Required Checks, Tests, Reviews

- Exact command:

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py --mode small-reference --device-scope cpu --output docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.json --markdown-output docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.md > docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.log 2>&1
```

- Exact JSON parse command:

```bash
python -m json.tool docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.json
```

- Run focused test if the phase repairs code.
- Local review that hard-veto fields and nonclaims are present.

## Predeclared Fixtures, Ranks, And Thresholds

Required fixtures and ranks:

| Fixture | Particle count | Ranks |
| --- | ---: | --- |
| `tiny_manual` | 4 | `2,3,4` |
| `small_parity` | 8 | `2,4,8` |
| `high_dim_low_rank` | 32 | `2,4,8,16,32` |
| `ledh_specific_smoke` | 32 | `4,8,16,32` |

Promoted-rank thresholds:

- max row residual: at most `5.0e-2`;
- max column residual: at most `5.0e-2`;
- max dense-reference transported-particle error: at most `7.5e-2`;
- RMS dense-reference transported-particle error: at most `3.0e-2`;
- finite factors and finite transported particles: required;
- candidate transport matrix shape must end in `[0, 0]`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does Nystrom match small dense-reference behavior closely enough at at least one predeclared rank per fixture to continue? |
| Baseline/comparator | Dense TensorFlow `annealed_transport_resample_tf` on the same small fixtures. |
| Primary criterion | No hard vetoes; at least one predeclared rank per required fixture passes the exact residual and dense-reference particle thresholds listed above; output is finite and nonmaterialized. |
| Veto diagnostics | Nonfinite factors/particles, row/column residual threshold failure for promoted rank, missing dense-reference fields, dense matrix materialized by candidate, or no viable rank for a required fixture. |
| Explanatory diagnostics | Dense-reference errors for nonpromoted ranks, runtime, memory proxy, landmark indices. |
| Not concluded | No large-N scalability, GPU readiness, speedup, posterior correctness, default readiness, or ranking. |
| Artifact | P02 JSON/Markdown and result. |

## Forbidden Claims And Actions

- Do not use dense-reference error to rank all algorithms.
- Do not infer large-N performance from small fixtures.
- Do not claim exact dense Sinkhorn equivalence.

## Exact Next-Phase Handoff Conditions

P03 may begin only after:

- P02 JSON/Markdown exist and parse;
- hard vetoes are empty;
- P02 result records viable ranks and nonclaims;
- P03 subplan is refreshed and locally reviewed.

## Stop Conditions

- No required fixture has a viable rank.
- Candidate emits nonfinite values or materializes dense transport.
- Artifact schema is missing required gate fields.
