# P04B Subplan: Nonlinear Threshold Governance Repair

Date: 2026-06-25

Status: `P04B_DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

## Phase Objective

Repair the P04/P04A threshold-governance regression before any further
promotion-ladder execution. P04 and P04A used an uncalibrated
`abs(log_likelihood_delta)/(T*M) <= 0.05` nonlinear range-bearing screen. This
phase reclassifies those artifacts as descriptive nonlinear scale evidence and
drafts the next calibration subplan without freezing a new threshold, running
P05, or making a method-failure/promotion claim.

## Entry Conditions Inherited From Previous Phase

- P04A previously emitted
  `P04A_LOCKED_FAILURE_CONFIRMED_REPAIR_REQUIRED_REVIEW_AGREE`.
- The user challenged the source of the `0.05` threshold and identified the
  repeated random-threshold problem.
- The actual-SIR threshold-calibration lane already established the governing
  pattern: descriptive scale extraction, reviewed threshold freeze, disjoint
  validation seeds, and one-sided 95% Clopper-Pearson exceedance rule.
- P04/P04A range-bearing rows were deterministic-valid but failed the
  hardcoded `0.05` paired threshold.
- P05 remains ineligible until the nonlinear threshold screen is calibrated or
  the owner explicitly changes the program boundary.

## Required Artifacts

- P04B subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04b-threshold-governance-repair-subplan-2026-06-25.md`
- P04B result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04b-threshold-governance-repair-result-2026-06-25.md`
- Corrected P04 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04-nonlinear-gaussian-result-2026-06-25.md`
- Corrected P04A result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04a-range-bearing-failure-diagnostic-result-2026-06-25.md`
- Corrected master program, visible runbook, execution ledger, Claude review
  ledger, and stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-master-program-2026-06-25.md`
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-gated-execution-runbook-2026-06-25.md`
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-execution-ledger-2026-06-25.md`
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-claude-review-ledger-2026-06-25.md`
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-stop-handoff-2026-06-25.md`
- Next subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c-nonlinear-threshold-scale-subplan-2026-06-25.md`
- Existing P04/P04A benchmark summaries:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-summary-2026-06-25.json`
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-diagnostic-summary-2026-06-25.json`

## Required Checks, Tests, And Reviews

- Local artifact checks:
  - Parse the P04 and P04A summary JSON artifacts.
  - Confirm P04/P04A deterministic validity passed for the executed rows.
  - Confirm the paired threshold in those artifacts was `0.05`.
  - Confirm P04/P04A are now described as uncalibrated threshold-governance
    evidence, not promotion-grade method-rejection evidence.
- Local document checks:
  - Confirm the active master/runbook/handoff status no longer presents
    `P04A_LOCKED_FAILURE_CONFIRMED_REPAIR_REQUIRED_REVIEW_AGREE` as the final
    scientific or promotion-ladder conclusion.
  - Confirm the active master/runbook/handoff status positively replaces the
    old conclusion with
    `P04_BLOCKED_UNCALIBRATED_NONLINEAR_THRESHOLD_PENDING_P04B_REVIEW` or the
    later P04B pass/blocker token once P04B closes.
  - Confirm P05 remains blocked.
  - Confirm P04C exists and has these required subplan sections by exact name:
    Phase Objective; Entry Conditions Inherited From Previous Phase; Required
    Artifacts; Required Checks, Tests, And Reviews; Calibration Panel; Per-Row
    Artifact Manifest; Evidence Contract; Forbidden Claims And Actions; Exact
    Next-Phase Handoff Conditions; Stop Conditions; End-Of-Phase Requirements;
    Local Self-Review Of This Subplan.
  - Confirm P04C preserves the same no-claims boundary: no calibrated
    threshold, no P04 pass/fail, no P05 execution, no default promotion, no
    posterior correctness, no HMC readiness, no statistical superiority, and no
    broad nonlinear validity.
- Claude read-only review:
  - Review P04B and P04C exact paths plus same-prefix corrected same-lane
    artifacts only.
  - Claude may not read source code, run commands, edit files, authorize a
    threshold, authorize P05, or authorize promotion/default/scientific/HMC
    boundaries.
  - Review convergence requires an explicit `VERDICT: AGREE` from Claude after
    exact-path review of the repaired P04B/P04C plan set.
  - If Claude returns `VERDICT: REVISE`, patch the same subplan/result visibly
    and rerun focused local checks and review, up to five rounds for the same
    blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the lane safely repair the P04/P04A uncalibrated-threshold conclusion and hand off to a principled nonlinear threshold-calibration phase? |
| Baseline/comparator | Existing P04/P04A artifacts compared against the actual-SIR threshold-calibration discipline: descriptive scale extraction, reviewed freeze, disjoint validation, CP exceedance rule. |
| Primary criterion | Corrected artifacts reclassify P04/P04A as `P04_BLOCKED_UNCALIBRATED_NONLINEAR_THRESHOLD`; P05 remains blocked; P04C is drafted with no threshold freeze and with disjoint future validation. |
| Veto diagnostics | Any continued active claim that `0.05` is calibrated, any claim that P04/P04A statistically reject the method, missing correction artifacts, malformed P04/P04A summaries, missing P04C sections, or Claude review nonconvergence. |
| Explanatory diagnostics | Observed P04/P04A normalized deltas around `0.095` to `0.102`, residuals, ESS, runtime, and rank/epsilon controls. |
| Not concluded | No calibrated nonlinear threshold, no P04 pass/fail under a valid calibrated threshold, no default promotion, no posterior correctness, no HMC readiness, no statistical superiority, and no broad nonlinear validity. |
| Artifact | P04B result plus corrected ledgers/handoff and P04C subplan. |

## Forbidden Claims And Actions

- Do not freeze a new nonlinear `tau_component` in P04B.
- Do not describe `0.05` as calibrated or principled for the range-bearing
  nonlinear fixture.
- Do not treat P04/P04A as statistically significant method failure evidence.
- Do not launch P05.
- Do not run new GPU validation seeds in P04B.
- Do not use seed `84000` as future validation evidence.
- Do not send source code, tests, credentials, model files, or unrelated paths
  to Claude.
- Do not make default, product, HMC-readiness, posterior-correctness,
  statistical-superiority, or broad scientific-validity claims.

## Exact Next-Phase Handoff Conditions

- `P04B_PASS_TO_P04C_NONLINEAR_THRESHOLD_SCALE_EXTRACTION`: all required local
  checks pass and are recorded in the P04B result, Claude returns explicit
  `VERDICT: AGREE` after exact-path review of the repaired P04B/P04C plan set,
  P04C exists with the exact required sections and inherited no-claims boundary,
  and P05 remains blocked.
- `P04B_REPAIR_LOOP_CONTINUES`: Claude or local checks find a fixable
  consistency problem and fewer than five review rounds have been used for the
  same blocker.
- `P04B_BLOCKED_THRESHOLD_GOVERNANCE_NONCONVERGENCE`: local checks fail or
  Claude review does not converge after five rounds for the same blocker.

## Stop Conditions

- A required P04/P04A summary artifact is missing or malformed.
- The correction would require changing historical benchmark outputs instead
  of adding governance interpretation.
- A new threshold freeze is needed before P04C scale extraction.
- P04C cannot be written with disjoint calibration/validation handling and a
  no-claims boundary.
- Claude review blocks on access and cannot be narrowed with exact-path prompts
  within the approved same-prefix file scope.
- Continuing would require source-code disclosure to Claude, P05 execution,
  product/default/scientific/HMC authorization, package installation, network
  fetches, commits, pushes, or destructive actions.

## End-Of-Phase Requirements

At P04B close, Codex must:

1. run the required local checks;
2. write the P04B result/close record;
3. draft or refresh P04C;
4. review P04C locally and with Claude for consistency, correctness,
   feasibility, artifact coverage, and boundary safety;
5. update the execution ledger, Claude review ledger, master/runbook status,
   and stop handoff.

## Skeptical Plan Audit

| Risk | Audit |
| --- | --- |
| Wrong baseline | Guarded: P04B compares the lane against the prior threshold-calibration discipline, not against an invented threshold. |
| Proxy metric promoted | Guarded: P04/P04A deltas are descriptive scale evidence only. |
| Missing stop conditions | Guarded: missing artifacts, threshold freeze pressure, P05 launch pressure, and review nonconvergence are explicit stops. |
| Unfair comparison | Guarded: no ranking or candidate comparison is made in P04B. |
| Hidden assumption | Guarded: range-bearing threshold calibration remains undone; P04B only repairs governance. |
| Stale context | Guarded: local checks parse current P04/P04A summaries and current corrected docs. |
| Environment mismatch | Guarded: P04B is documentation/artifact governance only and runs no GPU benchmark. |
| Artifact mismatch | Guarded: exact same-prefix artifacts are named before review. |

Audit status: `PASS_FOR_LOCAL_CHECKS_AND_CLAUDE_REVIEW_AFTER_PATCH`.
