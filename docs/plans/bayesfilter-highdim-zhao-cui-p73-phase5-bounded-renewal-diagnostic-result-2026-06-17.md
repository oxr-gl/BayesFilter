# P73 Phase 5 Result: Bounded Renewal Diagnostic

metadata_date: 2026-06-17
status: PHASE5_BLOCKED_CLAUDE_REVIEW_PENDING
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-subplan-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-result-2026-06-17.md
diagnostic_json: docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json
next_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase6-result-decision-subplan-2026-06-17.md

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | Does one-renewal P73-A reduce or clear the P72 lower-gate blockers under fresh guard/audit certification without training on same-round audit data? |
| Exact baseline/comparator | P72 Phase 5 blocked diagnostic row `rank_candidate_1_2_fit36`; P73-A uses the same rank/degree row with one renewal. |
| Primary pass/fail criterion | Failed.  The P73-A row blocked on step 1. |
| Veto diagnostics | `line_block`, `residual_rms_veto`, and `residual_max_veto` fired. |
| Explanatory only | Fit-cloud residual, cross-entropy value, runtime, support warnings, and condition spectra. |
| What is not concluded | No d18 validation, no HMC readiness, no scaling, no rank or degree promotion, no adaptive Zhao--Cui source-faithful parity, and no rejection of the adaptive Zhao--Cui method. |
| Artifact preserving result | This result and the JSON artifact named above. |

## Skeptical Plan Audit

The Phase 5 plan passed its skeptical audit before the diagnostic.  It fixed
the comparator, row label, runnable arm, blocked P73-B arm, CPU-only
environment, primary gates, veto diagnostics, explanatory metrics, and
nonclaims before execution.

During implementation of the Phase 5 runner, one additional plan-safety issue
was corrected before interpreting results: the round-0 enrichment set is now
selected from actual guard residual failures and guard-line failures, rather
than blindly adding every guard point.  This preserves the Phase 2 rule that
enrichment is failure-derived and not an unrestricted guard-training shortcut.

## Run Manifest

| Field | Value |
| --- | --- |
| Command | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p73_density_aware_renewal_diagnostic.py --output docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json` |
| CPU/GPU status | CPU-only intent via `CUDA_VISIBLE_DEVICES=-1`; TensorFlow still printed CUDA initialization warnings, treated as non-evidence because the run intentionally hid GPU devices. |
| Git head | `d52727c555d81783ce5a46b448d299429cb350f1` |
| Dirty worktree | Yes; status count recorded as 469 in the JSON run manifest. |
| Wall time | 13.283 seconds in the JSON run manifest. |
| Row spec | `rank_candidate_1_2_fit36`, degree 1, rank 2, fit count 36. |
| Random seeds | Recorded under `run_manifest.random_seeds` in the JSON. |

## Local Checks

Before and after the bounded diagnostic, the focused local checks passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p73_density_aware_renewal_diagnostic.py
```

Result: passed.

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p73_density_aware_renewal.py
```

Result: 15 passed, 2 TensorFlow Probability deprecation warnings.

```text
rg -n "p73_phase5_payload|P73_PHASE5_DENSITY_AWARE_RENEWAL_BLOCKED|phase5_diagnostic_executed.*True|schema_only_sentinel_present.*False|P73_B_OPTIMIZER_BLOCKED" scripts/p73_density_aware_renewal_diagnostic.py tests/highdim/test_p73_density_aware_renewal.py docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json
```

Result: required Phase 5 tokens found.

```text
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py scripts/p73_density_aware_renewal_diagnostic.py tests/highdim/test_p73_density_aware_renewal.py docs/plans/bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-claude-review-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-phase6-result-decision-subplan-2026-06-17.md
```

Result: passed.

## Diagnostic Result

The bounded diagnostic blocked:

```text
P73_PHASE5_DENSITY_AWARE_RENEWAL_BLOCKED
```

The failed row was:

```text
rank_candidate_1_2_fit36
```

Only P73-A ran.  P73-B remained:

```text
P73_B_OPTIMIZER_BLOCKED_NONLINEAR_OBJECTIVE_NOT_IMPLEMENTED
```

## Step-1 Gate Table

| Gate | Result |
| --- | --- |
| Overall step status | `BLOCK_P73_DENSITY_AWARE_RENEWED_SUPPORT_LOWER_GATE` |
| Gate reasons | `line_block`, `residual_rms_veto`, `residual_max_veto` |
| \(F_0,E_0,N_1,F_1\) counts | 36, 62, 36, 134 |
| Fit residual RMS / max relative on \(F_1\) | 0.0873 / 0.4432 |
| Fresh guard residual RMS / max relative | 1.5525 / 8.2733 |
| Fresh audit holdout residual RMS / max relative | 1239.4124 / 7436.1313 |
| Fresh audit replay residual RMS / max relative | 5.6041 / 28.7473 |
| Guard-line gate | pass |
| Audit-line gate | block: `line_rms_residual_veto` |
| Normalizer gate | pass; fit mass fraction 1.0; log normalizer 48.2145 |
| Condition/effective-rank gate | pass; condition max 1761.7169; effective rank min 4.0 |
| `NO_AUDIT_COEFFICIENT_SELECTION` | pass |
| Enrichment boundary | pass |
| Density-aware evaluator | pass; cross entropy 36.9265, weighted contribution 3.6926 |

Step 2 was skipped because step 1 blocked before a retained object could be
certified.

## Interpretation

This is a real negative result for the current P73-A renewal-only repair.  It
is not a provenance failure, normalizer failure, or condition-number failure.
It is also not a P73-B result, because the density-aware optimizer remains
blocked.

The important pattern is:

- the renewed fit cloud \(F_1\) is fit well;
- fresh guard diagnostics are acceptable under the frozen residual gates;
- fresh audit replay is acceptable under the RMS gate but not especially
  tight;
- fresh audit holdout is catastrophically off-support in residual terms;
- the audit-line gate blocks.

So one renewal with failure-derived guard/line enrichment and fresh support is
not enough to make the fixed rank-2 square-root regression generalize to the
fresh audit holdout cloud.  The next root-cause question is why the fresh
audit holdout cloud differs so sharply from \(F_1\) and from the replay/guard
channels despite passing the finite support warning-only checks.

## Decision Table

| Decision field | Status |
| --- | --- |
| Primary criterion | failed |
| Veto diagnostics | residual and audit-line vetoes fired |
| Engineering correctness ledger | P73-A runner produced a real bounded artifact; audit exclusion and enrichment provenance passed |
| Numerical validity ledger | normalizer and condition/effective-rank gates passed; residual and line gates failed |
| Scientific interpretation ledger | P73-A renewal-only is not sufficient evidence for repair |
| Main uncertainty | whether the remaining failure is caused by cloud geometry, clipping/saturation, target scaling, rank/degree capacity, or the missing nonlinear density-aware optimizer |
| Next justified action | Phase 6 result decision and root-cause handoff; do not run validation/HMC/scaling/rank promotion yet |
| Not concluded | no adaptive Zhao--Cui failure claim; no downstream readiness; no rank policy change |

## Post-Run Red-Team Note

The strongest alternative explanation is implementation-route mismatch in the
new P73 runner, especially the finite-cloud renewal construction and the
fresh audit channel definitions.  The result weakens the renewal-only repair
as implemented here, not the broader idea that a better renewal strategy or a
true density-aware optimizer could help.

A result that would overturn this conclusion would show the same row passing
fresh audit and audit-line gates under the frozen criteria, with
`NO_AUDIT_COEFFICIENT_SELECTION` still passing and without changing thresholds
after seeing outputs.

The weakest part of the evidence is that Phase 5 used a newly patched P73
diagnostic runner.  The focused tests and Claude review should therefore
inspect whether the runner faithfully implements the Phase 5 subplan before
using this negative result to choose the next root-cause lane.
