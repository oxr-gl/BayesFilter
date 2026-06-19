# P73 Phase 6 Result: Decision And Root-Cause Handoff

metadata_date: 2026-06-17
status: PHASE6_PASSED_CLAUDE_AGREE_P73_COMPLETE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase6-result-decision-subplan-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-result-2026-06-17.md
diagnostic_json: docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json
next_root_cause_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p74-fresh-audit-holdout-root-cause-subplan-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | What does the Phase 5 P73-A blocked result justify doing next? |
| Comparator | Phase 5 JSON/result, Phase 2 design, and P72 blocked diagnostic context. |
| Primary criterion | Satisfied as a decision artifact.  Phase 6 classifies the block and selects the smallest next root-cause artifact. |
| Veto diagnostics | No validation, HMC, scaling, GPU, rank promotion, threshold change, or new numerical diagnostic was launched. |
| Explanatory only | Fit residuals, cross-entropy, support warnings, condition spectra, runtime. |
| What is not concluded | No repaired lower gate, no validation readiness, no HMC readiness, no scaling, no rank-policy change, no source-faithful adaptive Zhao--Cui parity, and no adaptive Zhao--Cui failure claim. |
| Artifact preserving result | This result, the P74 root-cause subplan, the stop handoff, and updated ledgers. |

## Skeptical Plan Audit

Phase 6 passed the skeptical audit before execution because it was
interpretive only.  It consumed an already-run Phase 5 artifact, used the
actual P72/P73 blocked comparison, preserved the frozen gates, and did not
run new experiments or promote explanatory metrics to success evidence.

## Decision

The P73-A renewal-only repair remains blocked.

The most precise classification is:

```text
UNRESOLVED_LOWER_GATE_FAILURE_WITH_LEADING_FRESH_AUDIT_HOLDOUT_GENERALIZATION_SIGNAL
```

This is not presently classified as a confirmed implementation bug because:

- Claude reviewed the default Phase 5 route and agreed that the default
  command runs the real Phase 5 payload, not schema or smoke output;
- Claude reviewed \(E_0\), \(F_1\), and audit-exclusion construction and
  agreed that \(E_0\) comes only from guard/guard-line sources, \(F_1 =
  F_0 \cup E_0 \cup N_1\), and same-round audit/audit-line records are
  excluded from coefficient selection;
- Claude reviewed the post-fit gate logic and agreed that fresh
  guard/audit and guard-line/audit-line gates are evaluated after fitting;
- `NO_AUDIT_COEFFICIENT_SELECTION`, enrichment boundary, normalizer, and
  condition/effective-rank gates passed in the artifact.

It is also not classified as a pure capacity failure or a pure missing
P73-B objective failure.  Those remain viable explanations, but Phase 5 did
not isolate them.  The strongest current signal is the separation between
good fit on \(F_1\), acceptable fresh-guard behavior, and catastrophic fresh
audit holdout/audit-line behavior.

## Root-Cause Evidence From Phase 5

| Quantity | Phase 5 value |
| --- | --- |
| Failed row | `rank_candidate_1_2_fit36` |
| Step-1 blockers | `line_block`, `residual_rms_veto`, `residual_max_veto` |
| \(F_0,E_0,N_1,F_1\) counts | 36, 62, 36, 134 |
| Fit residual RMS / max relative on \(F_1\) | 0.0873 / 0.4432 |
| Fresh guard residual RMS / max relative | 1.5525 / 8.2733 |
| Fresh audit holdout residual RMS / max relative | 1239.4124 / 7436.1313 |
| Fresh audit replay residual RMS / max relative | 5.6041 / 28.7473 |
| Audit-line gate | block: `line_rms_residual_veto` |
| Normalizer gate | pass |
| Condition/effective-rank gate | pass |
| `NO_AUDIT_COEFFICIENT_SELECTION` | pass |
| P73-B | not executed; `P73_B_OPTIMIZER_BLOCKED_NONLINEAR_OBJECTIVE_NOT_IMPLEMENTED` |

The support diagnostics are warning-only and cannot veto by themselves, but
they point to the next root-cause question.  The fresh audit holdout cloud has
large nearest-fit distances and positive clipping/saturation warnings in the
artifact, while the renewed fit cloud is fit accurately.  This makes the next
smallest useful artifact a constructor/provenance and target-scale audit of
the fresh-audit holdout channel, not a validation ladder.

## Next Root-Cause Handoff

The next root-cause subplan is:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p74-fresh-audit-holdout-root-cause-subplan-2026-06-17.md
```

The exact blocker it targets is:

```text
rank_candidate_1_2_fit36, step 1:
line_block + residual_rms_veto + residual_max_veto,
driven by fresh audit holdout residuals and audit-line residuals.
```

The smallest next artifact should discriminate:

- runner or constructor mismatch in the fresh-audit holdout channel;
- target-frame, shift, or scaling mismatch;
- finite-cloud geometry and clipping/saturation failure;
- rank/degree capacity limitation;
- missing nonlinear density-aware optimization.

The first P74 action should be an artifact-and-code provenance audit before
any new fit or validation run.  If that audit finds a constructor mismatch,
the next action is repair.  If it finds no mismatch, the next action is a
separate, reviewed, bounded diagnostic plan for support geometry, target
scale, and capacity/objective ablations.

## Phase 6 Decision Table

| Decision field | Status |
| --- | --- |
| Primary criterion | met for decision/handoff |
| Phase 5 lower-gate status | blocked |
| Runner-bug classification | not proven; still a risk to audit in P74 |
| Cloud-geometry classification | leading current signal, not proven |
| Target-scale/shift classification | plausible unresolved explanation |
| Capacity classification | plausible unresolved explanation |
| Missing P73-B optimizer classification | plausible unresolved explanation; not tested because P73-B remained blocked |
| Next justified action | P74 fresh-audit holdout root-cause subplan |
| Downstream validation/HMC/scaling/rank promotion | still blocked |

## Nonclaims

- This does not reject the adaptive Zhao--Cui method.
- This does not reject all fixed-variant renewal strategies.
- This does not prove that the missing P73-B optimizer would fix the issue.
- This does not prove rank/degree capacity is sufficient or insufficient.
- This does not authorize validation, HMC, scaling, or rank promotion.

## Claude Closeout Review

Claude returned:

```text
VERDICT: AGREE
```

Claude agreed that Phase 6 correctly interprets Phase 5 as blocked, classifies
the remaining issue conservatively, avoids lower-gate repair/adaptive
Zhao--Cui failure/downstream readiness claims, and hands off to a bounded P74
constructor/provenance root-cause audit without launching new diagnostics or
downstream work.
