# P00 Program Review And Launch Gate Subplan

Date: 2026-06-23

## Phase Objective

Verify that the new less-intrusive stability master program, visible runbook,
phase index, and initial subplans are internally consistent, boundary-safe, and
ready for visible gated execution.

## Entry Conditions Inherited From Previous Phase

- The previous positive-projection stability-repair master program is closed as
  `REPAIR_FAILED_OR_BLOCKED`.
- P09/P10 from that closed program must not be reopened.
- The user requested a new master program with phase subplans, visible gated
  runbook, Claude read-only review to convergence or max five rounds, and
  automatic gated continuation until a real blocker.
- Current repo policy requires skeptical plan audit and evidence contracts
  before research actions.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-master-program-2026-06-23.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-visible-gated-execution-runbook-2026-06-23.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-visible-execution-ledger-2026-06-23.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-claude-review-ledger-2026-06-23.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-visible-stop-handoff-2026-06-23.md`
- P00 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p00-program-review-result-2026-06-23.md`
- Claude log paths:
  `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p00-claude-review-rN-2026-06-23.log`

## Required Checks, Tests, And Reviews

- Local structural check verifies:
  - all phase subplans P00-P07 exist;
  - every subplan contains the required sections named by the user;
  - the runbook names Codex as supervisor/executor and Claude as read-only
    reviewer;
  - `positive_projected` is diagnostic-only and not a promotion repair;
  - paired thresholds `10.0` and `5.0` are preserved;
  - no detached execution authority is present.
- Claude read-only review of bounded paths and plan summary, max five rounds.
- If Claude finds a fixable material issue, patch the relevant subplan/runbook
  visibly, rerun focused local checks, and re-review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is this new less-intrusive repair program safe and complete enough to launch? |
| Baseline/comparator | Repo policy, visible runbook template, prior closeout result, user protocol. |
| Primary pass criterion | Local structural checks pass and Claude review ends with `VERDICT: AGREE` within five rounds. |
| Veto diagnostics | Missing required section, missing stop condition, detached execution, Claude as executor, changed thresholds, positive projection treated as promotion repair, unsupported default claim. |
| Explanatory diagnostics | Wording issues, artifact naming issues, phase boundary suggestions. |
| Not concluded | No repair effectiveness, no default readiness, no scientific validity, no performance claim. |
| Artifact preserving result | P00 result file, review ledger, Claude log. |

## Forbidden Claims And Actions

- Do not run code changes or GPU benchmarks in P00.
- Do not treat Claude as execution authority.
- Do not change scientific thresholds during P00.
- Do not claim the repair exists or works.
- Do not claim default readiness.
- Do not launch detached agents or background phase runners.

## Exact Next-Phase Handoff Conditions

Advance to P01 only if:

- local structural checks pass;
- Claude returns `VERDICT: AGREE` within five rounds;
- P00 result is written;
- P01 subplan is present and refreshed if P00 review required changes.

## Stop Conditions

Stop and write a blocker result if:

- local checks fail in a way that cannot be patched safely;
- Claude and Codex do not converge after five rounds for the same material
  blocker;
- continuing would require changing thresholds, default policy, package
  installation, credentials, network fetches, destructive git/filesystem
  action, or human project-direction approval.

## Skeptical Plan Audit

Wrong baseline risk: P00 could accidentally continue the closed repair program.
Mitigation: all paths use the new `less-intrusive-stability` lane and prior
program artifacts are evidence only.

Proxy promotion risk: plan review cannot prove repair effectiveness.  Mitigation:
P00 forbids repair/default/scientific claims.

Missing stop condition risk: automatic continuation could run through a true
boundary.  Mitigation: stop conditions are explicit in runbook and subplans.

Audit status: `PASS_FOR_LOCAL_STRUCTURAL_CHECK_AND_CLAUDE_REVIEW`.
