# Positive-Feature Independent Validation

- Status: `PASS`
- Program status: `POSITIVE_FEATURE_INDEPENDENT_VALIDATION_PASSED_HARD_SCREEN_NO_RANKING`
- Wave 4 status: `WAVE4_POSITIVE_FEATURE_VALIDATION_PASSED_HARD_SCREEN_NO_RANKING`
- Lane: `current_agent_positive_feature`
- Candidate: `positive_feature_sinkhorn`
- Hard vetoes: `[]`

## Evidence Contract

| Field | Value |
| --- | --- |
| question | Does the positive-feature lane remain viable under replicated downstream resampling screens? |
| baseline_comparator | exact weighted input estimates; naive uniform-no-transport is explanatory only |
| primary_pass_criterion | empty hard vetoes across entry audit, transport validity, residual, and moment screens |
| ranking_rule | no ranking in current lane |

## Summary

| Metric | Value | Role |
| --- | ---: | --- |
| rows | `9` | hard-veto context |
| hard vetoes | `0` | hard veto |
| max candidate weighted mean error | `2.220446e-16` | hard veto |
| max candidate weighted second moment error | `5.218177e-01` | hard veto |
| max transport residual | `3.079331e-05` | hard veto |
| max wall time seconds | `3.731838e-02` | explanatory |
| ranking statistically supported | `False` | inference status |

## Rows

| Fixture | Seed | Valid | Hard vetoes | Mean error | Second moment error | Naive mean error | Naive second error | Max residual |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |
| weighted_curve | `101` | `True` | `[]` | `8.326673e-17` | `5.107561e-01` | `2.054221e-01` | `2.415164e-02` | `3.079331e-05` |
| weighted_curve | `202` | `True` | `[]` | `4.163336e-17` | `5.172404e-01` | `2.072316e-01` | `3.304763e-02` | `2.542596e-05` |
| weighted_curve | `303` | `True` | `[]` | `5.551115e-17` | `5.218177e-01` | `2.093703e-01` | `4.116786e-02` | `1.743759e-05` |
| bimodal_tail | `101` | `True` | `[]` | `1.110223e-16` | `5.050291e-01` | `8.881956e-01` | `6.415759e-02` | `2.427318e-06` |
| bimodal_tail | `202` | `True` | `[]` | `2.220446e-16` | `4.859472e-01` | `8.745193e-01` | `1.721250e-02` | `2.895192e-06` |
| bimodal_tail | `303` | `True` | `[]` | `1.110223e-16` | `4.638568e-01` | `8.545213e-01` | `4.821121e-02` | `3.661968e-06` |
| high_dim_low_rank | `101` | `True` | `[]` | `6.245005e-17` | `3.233517e-01` | `4.915116e-02` | `3.154544e-02` | `3.385579e-06` |
| high_dim_low_rank | `202` | `True` | `[]` | `5.377643e-17` | `3.025178e-01` | `5.275910e-02` | `3.008801e-02` | `1.072220e-05` |
| high_dim_low_rank | `303` | `True` | `[]` | `6.245005e-17` | `1.671129e-01` | `4.271216e-02` | `2.076726e-02` | `2.986357e-05` |

## Inference Status

| Evidence class | Status |
| --- | --- |
| hard_veto_screen | `passed` |
| statistically_supported_ranking | `none` |
| descriptive_only_differences | `['naive uniform estimator errors', 'candidate minus naive deltas', 'wall time', 'per-seed tables']` |
| default_readiness | `not assessed` |
| next_evidence_needed | `future coordinator comparison or larger filtering/posterior/HMC validation only after independent lane closeouts` |

## Non-Claims

- positive-feature lane hard screen only
- no ranking claim
- no speedup claim
- no production default change
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no dense Sinkhorn equivalence claim
- no broad scalable-OT selection claim
