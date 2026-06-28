# P02 Less-Intrusive Repair Selection Subplan

Date: 2026-06-23

## Phase Objective

Select exactly one less-intrusive Nystrom stabilization family for focused
implementation, based on prior artifacts and P01 diagnostic adequacy.

## Entry Conditions Inherited From Previous Phase

- P01 result exists.
- Required diagnostics are available in code and harness artifacts, or P01
  explicitly showed existing diagnostics are adequate.
- Focused tests passed if P01 edited code.
- P02 must not use dense `positive_projected` as a promotion repair.
- P01 added compiled-row serialization for `min_kernel_denominator` and
  `denominator_floor_hits`; these diagnostics are explanatory and repair
  selection inputs, not promotion criteria.

## Required Artifacts

- P02 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-repair-selection-result-2026-06-23.md`
- P03 refreshed subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-focused-implementation-subplan-2026-06-23.md`
- Claude review log:
  `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-claude-review-rN-2026-06-23.log`

## Required Checks, Tests, And Reviews

- Review prior evidence from the closed repair lane and current code.
- Use the P01 diagnostic surface now available in compiled rows:
  `min_kernel_denominator`, `denominator_floor_hits`, factor diagonal/range
  fields, core spectrum/range fields, kernel projection fields, scaling ranges,
  finite flags, residuals, and paired deltas.
- Enumerate plausible repair families and reject all but one with reasons.
- Required candidate classes to consider:
  - log-stable or normalized Sinkhorn scaling update;
  - factor normalization/rescaling that preserves the implied kernel operation;
  - spectral cutoff/tighter core solver variants;
  - dense positive projection as diagnostic-only;
  - fixed rank/epsilon policy restriction instead of repair.
- Claude read-only review of the selected repair contract, max five rounds for
  the same material blocker.
- Local structural check that P03 subplan names exactly one candidate and keeps
  paired thresholds unchanged.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which single less-intrusive repair is justified for focused implementation? |
| Baseline/comparator | P01 diagnostics, closed-lane P03/P06 artifacts, P09D SVD negative result, positive-projection paired failure. |
| Primary pass criterion | Exactly one repair family selected with implementation scope, validation gate, nonclaims, and stop conditions. |
| Veto diagnostics | Multiple simultaneous repairs, threshold drift, positive projection as promotion repair, unsupported default claim, missing P04 validation row, or Claude `VERDICT: REVISE` unresolved after five rounds. |
| Explanatory diagnostics | Diagnostic patterns motivating the selected repair and reasons rejected alternatives are less appropriate. |
| Not concluded | No repair effectiveness, no ranking, no default readiness. |
| Artifact preserving result | P02 result and Claude review log. |

## Forbidden Claims And Actions

- Do not implement code in P02.
- Do not select multiple repair families for simultaneous testing.
- Do not select `positive_projected` as a promotion repair.
- Do not treat SVD core solve as untried; it has negative prior evidence at
  `rcond=1e-6`.
- Do not change rank/epsilon defaults or paired thresholds.

## Exact Next-Phase Handoff Conditions

Advance to P03 only if:

- P02 result selects exactly one repair family;
- Claude review converges with `VERDICT: AGREE`;
- P03 subplan states exact code scope, tests, artifact fields, and P04 handoff.

## Stop Conditions

Stop and write a blocker result if:

- no less-intrusive repair can be justified from available diagnostics;
- the only viable path is policy restriction rather than repair and that
  requires human direction;
- Claude/Codex do not converge after five review rounds;
- selection would require changing the scientific threshold contract.

## Skeptical Plan Audit

Wrong baseline risk: selecting a repair only because it makes finite outputs
would repeat the positive-projection failure.  Mitigation: P04 paired thresholds
are hard vetoes.

Tuning risk: selecting rank/epsilon changes would turn repair into policy
restriction.  Mitigation: P02 separates repair from fixed-policy closeout.

Stale-context risk: SVD has already been tested.  Mitigation: P02 cites P09D and
does not relaunch a core-solver-only repair without new diagnostics.

Audit status: `READY_AFTER_P01_PASS`.
