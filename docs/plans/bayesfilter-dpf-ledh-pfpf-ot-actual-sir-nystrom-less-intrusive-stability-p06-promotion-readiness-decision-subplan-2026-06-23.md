# P06 Promotion-Readiness Decision Gate Subplan

Date: 2026-06-23

## Phase Objective

Decide whether the less-intrusive repair evidence justifies drafting a separate
default-promotion or stress-validation master program, or whether the current
lane should close as repair-viability evidence only.

## Entry Conditions Inherited From Previous Phase

- One of the following is true:
  - P04 and P05 passed and this phase is deciding whether to recommend a
    separate promotion/stress program;
  - P04 produced a valid candidate-failure artifact and this phase is deciding
    whether to close out, restrict policy, or draft a bounded return-to-P02
    repair loop;
  - P05 produced a valid neighborhood/control-failure artifact and this phase is
    deciding whether to close out, restrict policy, or draft a bounded
    return-to-P02 repair loop.
- Current actual entry path: P04 produced a valid candidate-failure artifact
  and P05 is skipped by predeclared stop-on-hard-veto logic.
- Required completed gate artifacts exist and preserve trusted GPU/TF32 evidence
  when the completed gate was a GPU gate.
- Claude review of P05 interpretation is required only for a P05-pass path or a
  material next-loop recommendation.

## Required Artifacts

- P06 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p06-promotion-readiness-decision-result-2026-06-23.md`
- P07 refreshed closeout subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p07-closeout-subplan-2026-06-23.md`
- Optional Claude review log:
  `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p06-claude-review-rN-2026-06-23.log`

## Required Checks, Tests, And Reviews

- No new benchmark runs by default.
- Audit P04/P05 artifacts for threshold stability, trusted GPU evidence,
  selected-repair metadata, and nonclaims.
- For the current P04-failure path, audit specifically whether the result
  invalidates the harness, implementation, target, data, math, or artifact, or
  merely rejects the current balanced-scaling candidate.
- Draft decision:
  - `DRAFT_SEPARATE_PROMOTION_PROGRAM` if P04/P05 passed cleanly;
  - `REPAIR_VIABLE_BUT_NOT_PROMOTION_READY` if evidence is promising but
    insufficient for default;
  - `RETURN_TO_P02_REPAIR_LOOP` if a valid candidate failure is exactly the
    failure type this program is designed to repair and another bounded repair
    family remains;
  - `REPAIR_FAILED_OR_RESTRICT_POLICY` if prior gates failed and no bounded
    repair loop remains justified.
- Claude read-only review of the decision if it would recommend a future
  promotion program or a return-to-P02 repair loop.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does this lane justify a separate promotion/stress program, and what must that next program test? |
| Baseline/comparator | P04/P05 repair gate artifacts and repo evidence policy. |
| Primary pass criterion | P06 result makes a boundary-safe decision and does not claim default readiness. |
| Veto diagnostics | Unsupported default claim, missing uncertainty caveat, missing next evidence list, threshold drift, invalid prior artifact, or Claude review unresolved for promotion or repair-loop recommendation. |
| Explanatory diagnostics | Which gates passed, residual/paired margins, runtime and diagnostics as descriptive only. |
| Not concluded | No default readiness, no superiority, no posterior correctness, no HMC readiness. |
| Artifact preserving result | P06 result and optional review log. |

## Forbidden Claims And Actions

- Do not change default policy.
- Do not launch high-N, HMC, or stress tests in P06 unless a separate reviewed
  plan is created.
- Do not claim statistical ranking from P04/P05.
- Do not call descriptive runtime a promotion criterion.
- Do not route a valid candidate failure straight to final closeout without
  answering whether it invalidated the harness, implementation, target, data,
  math, or artifact, or merely rejected the current candidate.

## Exact Next-Phase Handoff Conditions

Advance to P07 only if:

- P06 result is written;
- P07 closeout subplan is refreshed with final status and artifacts;
- any material promotion-program or return-to-P02 repair-loop recommendation has
  Claude `VERDICT: AGREE`.

## Stop Conditions

Stop and write blocker if:

- required P04/P05 artifacts are inconsistent or missing;
- the only safe next step requires human project-direction approval before
  closeout wording can be chosen;
- Claude/Codex do not converge after five rounds on a promotion recommendation.

## Skeptical Plan Audit

Promotion-overreach risk: passing repair gates is still not default readiness.
Mitigation: P06 can only recommend a separate promotion/stress program.

Artifact risk: P06 might miss a veto in P04/P05.  Mitigation: threshold and
manifest audit is required.

Audit status: `READY_AFTER_P04_VALID_CANDIDATE_FAILURE`.
