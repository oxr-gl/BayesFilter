# P06 Candidate-Failure Classification Result

Date: 2026-06-23

Status: `REPAIR_FAILED_OR_RESTRICT_POLICY`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Classify the lane as a valid repair-candidate failure and close rather than launch another automatic repair loop | `PASS`: P04 artifact is valid, boundary-safe classification is made, and no default-readiness claim is made | `PASS`: no artifact invalidity, threshold drift, unsupported promotion claim, or missing selected-repair metadata | A different future repair family might exist, but it would be a new reviewed lane rather than a bounded continuation of this one | Proceed to P07 closeout; recommend human choice between fixed-policy validation around `rank=32,epsilon=0.5` or a new numerical-method repair program | No default readiness, no superiority, no posterior correctness, no HMC readiness, no proof that Nystrom is broadly unusable |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Does this lane justify a separate promotion/stress program, and what must that next program test? |
| Baseline/comparator | P04 repair gate artifact, prior closed-lane SVD/positive-projection evidence, and repo evidence policy. |
| Primary pass criterion | `PASS`: P06 result makes a boundary-safe decision and does not claim default readiness. |
| Veto diagnostics | `PASS`: no unsupported default claim, missing uncertainty caveat, threshold drift, invalid prior artifact, or unreviewed promotion recommendation. |
| Explanatory diagnostics | P04 valid hard-veto failure, prior SVD negative result, prior positive-projection paired failure, and prior fixed-policy viability context. |
| Not concluded | No default readiness, no superiority, no posterior correctness, no HMC readiness. |
| Artifact preserving result | P06 result and P07 refreshed closeout subplan. |

## Classification

P04 did not invalidate the harness, target row, trusted GPU context, comparator,
or artifact:

- the JSON and Markdown artifacts exist;
- trusted GPU/TF32 evidence is present;
- physical GPU1 was selected by preflight and exposed as `/GPU:0`;
- the compiled streaming comparator passed;
- selected candidate metadata was present:
  `nystrom_kernel_mode="raw"` and
  `nystrom_scaling_normalization="balanced"`;
- the failure was localized to the Nystrom candidate:
  `nonfinite_log_likelihood`, `nonfinite_nystrom_factors`, and
  `nonfinite_nystrom_particles`.

Therefore P04 is a valid repair-candidate failure.  It rejects the current
balanced-scaling candidate for the original brittle row.

## Why No Automatic Return-To-P02 Loop

The current master program already tested the bounded less-intrusive repair
selected by P02.  The remaining obvious alternatives are not appropriate for an
automatic return-to-P02 loop inside this lane:

- `positive_projected` already made the first failing row finite/residual-valid
  but failed paired max delta, and it changes kernel entries directly;
- `svd_truncated,rcond=1e-6` already failed both known brittle rows;
- broad rank/epsilon search is policy tuning after observing failures, not an
  implementation repair;
- positive-feature or low-rank-coupling replacement changes the transport
  object class and should be a new method lane;
- a fixed `rank=32,epsilon=0.5` policy path remains viable context, but it is a
  restricted-policy validation program, not proof that this less-intrusive
  repair worked.

Because this result recommends closeout/restriction rather than promotion or a
new return-to-P02 repair loop, no additional Claude review is required by the
P06 subplan.

## Recommended Next Human Decision

Choose one of two separate next programs:

1. Fixed-policy validation: explicitly restrict actual-SIR Nystrom to the
   known viable `rank=32,epsilon=0.5` neighborhood and test robustness/stress
   under that restricted policy.
2. New numerical-method repair lane: design a fresh, reviewed method program
   for a more substantive raw low-rank-kernel stabilization or replacement.

This lane should not silently launch either program.

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | P04 failed hard-veto screen for the balanced candidate. |
| Statistically supported ranking | `NO`. |
| Descriptive-only differences | Runtime and finite per-seed deltas are descriptive only after hard veto failure. |
| Default-readiness | `NO`. |
| Next evidence needed | P07 closeout and human/reviewed selection of a separate next program. |

## Post-Run Red Team

Strongest alternative explanation: balanced scaling may have been the wrong
mechanistic repair; this does not prove that all raw Nystrom stabilization
strategies are impossible.

What would overturn this P06 decision: a bounded, pre-reviewed repair family
that has not already been rejected and does not require changing thresholds,
target rows, or transport object class.  No such repair family is currently
defined in this master program.

Weakest part of evidence: the conclusion is about this lane and this candidate,
not about all possible Nystrom variants.

## P07 Refresh

P07 should close with final status
`CLOSED_REPAIR_FAILED_OR_RESTRICT_POLICY`, preserve artifacts, and state that
P05 was skipped because P04 hard-vetoed.
