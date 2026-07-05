# Phase 1 Subplan: Full-Row LGSSM GPU/XLA Score Gate

Date: 2026-07-04

Status: `IN_PROGRESS`

## Phase Objective

Take the already repaired LGSSM same-target LEDH route and decide whether the
full `T=50` row can be admitted by the same-target manual-reverse score route
with trusted GPU/XLA evidence, or else keep the row blocked with a precise
reason.

## Entry Conditions Inherited From The Previous Phase

- Phase 0 freezes the July 3 combined leaderboard baseline and repair-priority
  coverage/order.
- The tiny-prefix LGSSM manual total score route is already known locally and
  is diagnostic only.
- GPU/XLA execution must be trusted if the phase claims full-row admission.
- The launcher may use `transport-ad-mode=full` only as an internal transport
  setting required by the manual-reverse route; that setting is not itself
  score provenance.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase1-lgssm-full-row-result-2026-07-04.md`
- Full-row JSON/Markdown artifact for `benchmark_lgssm_exact_oracle_m3_T50`
  emitted by the manual-reverse launcher.
- Visible execution ledger update.
- If the phase claims admission, a refreshed combined leaderboard artifact.

## Required Checks, Tests, And Reviews

- `python -m py_compile` for the LGSSM benchmark code if code is changed.
- Trusted GPU/XLA full-row run using the same value/score route.
- Same-target score verification on the full row, meaning the result fields
  must show manual-reverse provenance, the same-route value/score fields, and a
  passing same-scalar finite-difference check, or a precise blocker note if any
  of those fail.
- `git diff --check` on touched files.
- Claude read-only review of the phase result if admission is claimed or if
  the blocker wording changes materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the full `T=50` LGSSM LEDH row be admitted from the same-target manual-reverse value/score route? |
| Baseline/comparator | The July 3 combined leaderboard LGSSM row and the previously accepted tiny-prefix diagnostic only. |
| Primary criterion | Trusted GPU/XLA full-row evidence shows finite value, finite score, manual-reverse score provenance, same-target verification passing, and same-route metadata; or the result records a precise blocker. |
| Veto diagnostics | Prefix-only evidence, autodiff/tape score provenance, wrong target, CPU-only claim as GPU evidence, score/value route mismatch, or manual-reverse same-scalar finite-difference failure. |
| Explanatory diagnostics | Compile time, runtime, exact Kalman value comparison, same-scalar FD on the full row if run, and row residuals. |
| Not concluded | Any other row family, HMC readiness, posterior correctness, or runtime superiority. |

## Forbidden Claims/Actions

- Do not call the tiny-prefix result a full-row admission.
- Do not claim GPU readiness from CPU-hidden evidence.
- Do not treat `transport-ad-mode=full` as score provenance or as tape/autodiff
  evidence.
- Do not admit a score if the value and score routes do not share the same
  target or if same-scalar verification fails.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if Phase 1 writes either:

- admitted full-row LGSSM score with trusted GPU/XLA evidence and passing
  same-target verification; or
- a precise full-row blocker that does not change the target freeze.

## Stop Conditions

Stop and write a blocker result if:

- the GPU/XLA evidence is untrusted or missing;
- the score route is not the same target as the value route;
- the same-target verification fails on the full row even if the score is
  finite;
- the phase tries to use prefix-only evidence as row admission.

## Phase-End Duties

At the end of Phase 1:

1. run the required local checks;
2. write the Phase 1 result / close record;
3. draft or refresh the Phase 2 subplan;
4. review the Phase 2 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
