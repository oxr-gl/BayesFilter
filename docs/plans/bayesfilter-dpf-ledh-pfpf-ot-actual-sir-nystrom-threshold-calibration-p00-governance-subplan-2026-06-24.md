# P00 Subplan: Threshold Calibration Governance And Runbook Lock

Date: 2026-06-24

Status: `READY_FOR_LOCAL_AND_CLAUDE_REVIEW`

## Phase Objective

Lock the threshold-calibration master program, visible gated runbook, execution
ledger, stop handoff, and P1 artifact-scale subplan before any threshold
freezing or GPU validation work begins.

## Entry Conditions Inherited From Previous Phase

- Statistical testing amendment exists and supersedes the zero-failure
  stochastic rejection rule.
- Threshold calibration plan exists and states that legacy `5.0` is not
  principled.
- User requested a master program with phase subplans, read-only Claude review
  until convergence or five rounds, and visible gated execution.
- No new threshold has been frozen.
- No new validation seeds may be interpreted before threshold freeze.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-master-program-2026-06-24.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-visible-gated-execution-runbook-2026-06-24.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-visible-execution-ledger-2026-06-24.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-visible-stop-handoff-2026-06-24.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-claude-review-ledger-2026-06-24.md`
- P1 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p01-artifact-scale-subplan-2026-06-24.md`
- P0 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p00-governance-result-2026-06-24.md`

## Required Checks, Tests, And Reviews

Local checks:

- required files exist;
- master program references all phase artifacts;
- P0 and P1 subplans contain required sections;
- runbook includes quiet visible execution, repair loop, Claude read-only role,
  and human-required stop conditions;
- no plan claims default readiness, posterior correctness, HMC readiness,
  statistical superiority, or principled status for legacy `5.0`;
- skeptical audit records wrong-baseline, proxy-threshold, stop-condition,
  unfair-comparison, hidden-assumption, stale-context, environment, and artifact
  risks.

Review:

- Claude Opus/max-effort read-only review of bounded excerpts from the master
  program, runbook, P0 subplan, and P1 subplan.
- If Claude does not respond, run a small read-only probe.  If the probe works,
  redesign the prompt and retry.
- Loop review at most five rounds for the same material blocker.

Blocker identity rule: the same material flaw remains the same blocker when it
concerns the same phase, evidence-contract field, artifact set, or boundary
condition, even if phrased differently in later reviews.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the threshold-calibration program complete, bounded, reviewable, and safe to launch into artifact-only P1? |
| Baseline/comparator | Statistical amendment, threshold calibration plan, visible runbook template, and local benchmark harness. |
| Primary pass criterion | Local checks pass and Claude read-only review returns `VERDICT: AGREE`, or only nonmaterial wording issues remain with local justification. |
| Veto diagnostics | Missing required sections, missing artifacts, unsupported claims, threshold freeze before calibration, GPU validation before threshold freeze, Claude execution authority, or absent stop conditions. |
| Explanatory diagnostics | Reviewer suggestions, wording improvements, artifact path inventory. |
| Not concluded | No calibrated threshold, no validation result, no default readiness, no statistical rejection, no HMC/posterior readiness. |
| Artifact | P0 result and Claude review ledger. |

## Forbidden Claims And Actions

- Do not freeze `tau_component` in P0.
- Do not launch GPU benchmarks in P0.
- Do not claim `5.0` is principled, MCSE-derived, or accepted.
- Do not let Claude authorize execution or edit files.
- Do not use detached agents or overnight supervisors.

## Exact Next-Phase Handoff Conditions

- `P0_PASS_TO_P1`: required artifacts exist, local checks pass, Claude review
  converges or has only documented nonmaterial issues, and P1 subplan is ready.
- `P0_REPAIR_LOOP`: local or Claude review finds fixable material flaws.
- `P0_BLOCKED`: review fails to converge after five rounds, required artifact
  cannot be created, or a human/product/scientific boundary must be crossed.

## Stop Conditions

- Missing required artifact after repair attempt.
- Claude review cannot be obtained and a probe shows Claude itself is
  unavailable.
- Claude/Codex do not converge after five rounds for the same blocker.
- Continuing would require threshold choice, GPU validation, default-policy
  change, package installation, network fetch, or destructive filesystem/git
  action.

## Skeptical Plan Audit

| Risk | P0 Audit |
| --- | --- |
| Wrong baseline | P0 checks only governance artifacts; it does not compare algorithms. |
| Proxy metrics | Legacy `5.0` is explicitly non-authoritative. |
| Missing stop conditions | Stop conditions are present in P0 and required for later phases. |
| Unfair comparison | P0 forbids new validation runs. |
| Hidden assumptions | Intended scope is value-route diagnostics, not HMC/posterior. |
| Stale context | Superseded G5 zero-failure interpretation is not used. |
| Environment mismatch | P0 is artifact-only; GPU checks start only when needed. |
| Artifact mismatch | Required file checks are part of P0. |

Audit status: `PASS_FOR_P0_LOCAL_CHECKS`.
