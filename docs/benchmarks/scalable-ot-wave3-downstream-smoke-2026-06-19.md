# Wave 3 Downstream Smoke Diagnostics

- Mode: `smoke`
- Status: `PASS`
- Wave 3 status: `WAVE3_DOWNSTREAM_SMOKE_PASSED_NO_RANKING`
- Hard vetoes: `[]`

## Artifact Audit

- Artifact audit pass: `True`
- Artifact hard vetoes: `[]`

## Summary

| Metric | Value | Role |
| --- | ---: | --- |
| num rows | `4` | hard-veto context |
| num hard vetoes | `0` | hard veto |
| max mean delta from input | `1.239000e-01` | explanatory |
| max variance delta from input | `1.659154e-01` | explanatory |
| max wall time seconds | `8.784064e-02` | explanatory |

## Rows

| Fixture | Candidate | Valid | Hard vetoes | Transport kind | Mean delta, explanatory | Variance delta, explanatory |
| --- | --- | --- | --- | --- | ---: | ---: |
| tiny_manual_common | low_rank_coupling | `True` | `[]` | `low_rank_coupling_factors` | `1.074999e-01` | `1.130119e-01` |
| tiny_manual_common | positive_feature | `True` | `[]` | `kernel_factors` | `1.075000e-01` | `1.214562e-01` |
| wider_state_common | low_rank_coupling | `True` | `[]` | `low_rank_coupling_factors` | `1.238999e-01` | `1.575842e-01` |
| wider_state_common | positive_feature | `True` | `[]` | `kernel_factors` | `1.239000e-01` | `1.659154e-01` |

## Non-Claims

- Wave 3 downstream smoke diagnostics only
- no ranking claim
- no speedup claim
- no production default change
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no dense Sinkhorn equivalence claim
- no broad scalable-OT selection claim
