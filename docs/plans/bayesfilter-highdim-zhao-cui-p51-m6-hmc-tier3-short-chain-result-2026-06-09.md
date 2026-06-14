# P51-M6 Result: HMC Tier 3 Short-Chain Diagnostics

metadata_date: 2026-06-09
phase: P51-M6
status: BLOCK_P51_M6_HMC_TIER3_SHORT_CHAIN
supervisor: Codex
reviewer: Claude Code read-only

## Decision

P51-M6 blocks the Tier 3 short-chain diagnostic for the same exact transformed
SV dim-1 dense reference target that passed P51-M5 Tier 2.  The attempted
posterior target added an explicit independent normal prior over
`theta=(Phi^{-1}(gamma), log(beta))`, and the posterior/reference check used a
deterministic two-dimensional quadrature over the same unnormalized target.

The phase blocks because the predeclared posterior/reference veto diagnostics
failed.  The short chain did not meet the posterior mean tolerance, and the
bounded quadrature reference itself failed its boundary diagnostic.

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Short-chain HMC diagnostic against a declared posterior/reference for the same target that passed Tier 2. |
| Baseline/comparator | P51-M5 exact transformed SV dim-1 dense reference target plus deterministic two-dimensional posterior quadrature. |
| Primary criterion | Blocked: the attempted same-target short chain failed the predeclared posterior/reference criteria. |
| Veto diagnostics | Failed: posterior mean error was above tolerance and the bounded-grid reference tail diagnostic showed inadequate grid support. |
| Not concluded | No production HMC readiness, GPU readiness, broad sampler convergence, or model production readiness. |

## Limiting Metrics

| Diagnostic | Observed | Criterion | Status |
| --- | ---: | ---: | --- |
| nonfinite sample count | `0` | `0` | pass |
| acceptance rate | `1.0` | `[0.5, 1.0]` | pass |
| posterior mean infinity error | `0.19210895764534353` | `< 0.15` | fail |
| posterior covariance infinity error | `0.04810846122539929` | `< 0.08` | pass |
| reference tail-boundary log ratio | `0.0` | `< -3.0` | fail |

The predeclared divergence and reproducibility criteria are not used as a
salvage path.  They are recorded as not assessed after the posterior/reference
veto fired; M6 is not promotion-eligible regardless of any later sampler
plumbing diagnostic.

## Validation

Focused validation was run CPU-only with `CUDA_VISIBLE_DEVICES=-1`.

The initial pass-form test failed as intended under the repair loop:

```text
tests/highdim/test_p51_hmc_tier3_short_chain.py::test_p51_m6_recomputed_short_chain_metrics_match_manifest_and_pass
assert 0.19210895764534353 < 0.15
```

The full metric extraction recorded the boundary diagnostic failure as well:

```text
reference_tail_boundary_log_ratio = 0.0
```

After converting M6 to a reviewed blocker, use:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p51_hmc_tier3_short_chain.py tests/highdim/test_p51_hmc_tier2_leapfrog.py tests/highdim/test_p50_hmc_readiness_tiers.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p51_hmc_tier3_short_chain.py
git diff --check -- tests/highdim/test_p51_hmc_tier3_short_chain.py docs/plans/bayesfilter-highdim-zhao-cui-p51-m6-hmc-tier3-short-chain-manifest-2026-06-09.json docs/plans/bayesfilter-highdim-zhao-cui-p51-m6-hmc-tier3-short-chain-result-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p51-visible-execution-ledger-2026-06-09.md
```

Blocker-form validation outcomes:

- pytest passed: 12 tests passed, with 2 TensorFlow Probability deprecation
  warnings;
- compileall passed;
- git diff whitespace check passed.

## Nonclaims

- No production HMC readiness.
- No GPU readiness.
- No broad sampler convergence.
- No model production readiness.
- No source-faithful adaptive TT/SIRT filtering.
- No S&P 500 reproduction.
