# P75 Master Program: Stochastic Density Training Pilot For The Fixed Variant

metadata_date: 2026-06-17
status: PHASE10_CLAUDE_AGREE_READY_FOR_PHASE11
executor: Codex in the current conversation
reviewer: Claude Opus max effort, read-only and bounded
predecessor_handoff: docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-stop-handoff-2026-06-17.md
predecessor_result: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase6-result-decision-result-2026-06-17.md

## Objective

Design, implement, and run a small but genuine stochastic differentiable
density-training pilot for the fixed Zhao--Cui variant.  The pilot is meant to
test whether moving from undersampled least-squares ALS to fresh-batch
KL/cross-entropy-style optimization can improve fresh audit generalization.

P75 is an `extension_or_invention` lane.  It is not a source-faithful
adaptive Zhao--Cui reproduction.  It may borrow the fixed Zhao--Cui target,
coordinate frame, and audit gates as comparators, but stochastic neural-style
training, KL terms, trainable TT variables, optimizers, schedules, penalties,
and sample-renewal policies are new fixed-variant machinery unless later
paper/source anchors are supplied.

## Starting Evidence

P73 completed as a blocked diagnostic/root-cause handoff:

- P73-A renewal-only remained blocked.
- The failing row was `rank_candidate_1_2_fit36`.
- The fresh audit holdout residual RMS/max relative was
  1239.4124 / 7436.1313.
- The audit-line gate blocked with `line_rms_residual_veto`.
- Normalizer, condition/effective-rank, audit exclusion, and enrichment
  boundary gates passed.
- P73-B did not execute because the nonlinear density-aware optimizer was not
  implemented.

The user diagnosis is that the prior sample/capacity regime is not meaningful:
134 fit samples for 280 raw TT coefficients is far below a minimum
data-to-parameter ratio, and least-squares ALS does not optimize a density
KL/cross-entropy objective.

## Global Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can a small stochastic differentiable density-training pilot be made to run correctly enough to test the fixed-variant objective direction? |
| Exact baseline/comparator | P73 Phase 5 blocked diagnostic and P73 Phase 6 handoff; optional comparisons to the current ALS row are explanatory unless the phase predeclares them primary. |
| Primary program pass criterion | The program passes if it produces a reviewed design, an opt-in implementation, and a bounded pilot artifact showing that the stochastic objective runs with finite losses/gradients and independently evaluates fresh audit gates. |
| Veto diagnostics | Source-faithfulness overclaim; treating pilot loss as validation; using audit holdout for training; changing P73/P75 thresholds after outputs; launching validation/HMC/scaling/rank promotion; GPU claims without trusted GPU evidence; default-policy changes. |
| Explanatory diagnostics | Training loss curves, cross-entropy estimates, log-normalizer estimates, gradient norms, parameter norms, fresh audit residuals, line gates, runtime, memory, seed sensitivity. |
| Not concluded | No repaired lower gate unless frozen fresh-audit gates pass; no adaptive Zhao--Cui parity; no validation readiness; no HMC readiness; no scaling claim; no final rank/degree/sample policy. |
| Artifacts | Master program, runbook, execution ledger, review ledger, phase subplans/results, implementation diffs if launched, pilot JSONs, stop handoff. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Planning and objective-boundary review | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase0-objective-boundary-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase0-objective-boundary-result-2026-06-17.md` |
| 1 | Mathematical pilot design contract | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-result-2026-06-17.md` |
| 2 | Implementation surface and test plan | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-result-2026-06-17.md` |
| 3 | Opt-in implementation and unit tests | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-result-2026-06-17.md` |
| 4 | Bounded pilot run | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase4-bounded-pilot-run-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase4-bounded-pilot-run-result-2026-06-17.md` |
| 5 | Result decision and next handoff | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase5-result-decision-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase5-result-decision-result-2026-06-17.md` |
| 6 | Guided warm-start mechanism smoke | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase6-guided-warm-start-smoke-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase6-guided-warm-start-smoke-result-2026-06-18.md` |
| 7 | UKF/source-guided initializer design | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase7-ukf-source-guided-initializer-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase7-ukf-source-guided-initializer-design-result-2026-06-18.md` |
| 8 | Source-guided square-root prefit implementation and tiny test | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase8-source-guided-prefit-implementation-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase8-source-guided-prefit-implementation-result-2026-06-18.md` |
| 9 | Guided prefit decision and larger-pilot handoff | to be drafted at Phase 8 close | to be drafted at Phase 8 close |
| 10 | Bounded capacity/sample/prefit ladder | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase10-capacity-sample-ladder-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase10-capacity-sample-ladder-result-2026-06-18.md` |

Only Phase 0 is drafted at master-program creation.  Each later subplan must
be drafted or refreshed at the end of the immediately previous phase.

## Dependency Matrix

| Phase | Must consume | Must produce for next phase |
| --- | --- | --- |
| 0 | P73 closeout, P73 Phase 6 handoff, current code surface | Objective-boundary ledger and reviewed Phase 1 design subplan |
| 1 | Phase 0 boundary ledger | Frozen pilot objective, train/eval split, batch schedule, sample budgets, gates, and reviewed Phase 2 subplan |
| 2 | Phase 1 design | Exact implementation surface map, focused tests, risks, and reviewed Phase 3 subplan |
| 3 | Phase 2 surface map | Opt-in code/tests only; no default behavior change; reviewed Phase 4 subplan |
| 4 | Phase 3 implementation | Bounded pilot JSON/result with finite-loss/gradient evidence and fresh audit evaluation |
| 5 | Phase 4 result and review | Collapse diagnosis, selected next mechanism test, and reviewed Phase 6 subplan |
| 6 | Phase 5 diagnosis and Phase 6 subplan | Same-draw random/guided warm-start smoke result and reviewed Phase 7 design subplan |
| 7 | Phase 6 result and Phase 7 subplan | Bounded UKF/source-guided initializer design and reviewed Phase 8 implementation subplan |
| 8 | Phase 7 design and Phase 8 subplan | Opt-in prefit implementation, unit checks, tiny same-draw test, and Phase 9 decision subplan |
| 9 | Phase 8 result and review | Phase 9 decision result and reviewed Phase 10 bounded ladder subplan |
| 10 | Phase 9 result and Phase 10 subplan | Bounded ladder JSON/result and Phase 11 decision subplan or stop handoff |
| 11 | Phase 10 negative ladder result | Decision artifact: stop, redesign handoff, or separately reviewed larger-pilot plan |

A phase may repair the blocker handed to it.  It must not require the repair
to have already succeeded before it begins.

## Phase Boundaries

### Phase 0: Planning and objective-boundary review

Classify P75 as an extension, not source-faithful Zhao--Cui.  Check that the
program targets the objective problem rather than only the sample-count
problem.  Confirm the initial pilot should be CPU-only unless a later phase
explicitly asks for trusted GPU evidence and receives user approval.

### Phase 1: Mathematical pilot design contract

Define the stochastic objective before implementation.  The contract must
state whether the pilot optimizes an unnormalized density objective, an
empirical forward-KL/cross-entropy surrogate, a normalizer-penalized objective,
or a safer first proxy.  It must specify which samples are training samples,
which are fresh audit/line samples, and which quantities are pass criteria
versus explanatory.

### Phase 2: Implementation surface and test plan

Map trainable TT variables, differentiable log-density/normalizer terms,
fresh-batch generation, optimizer loops, manifests, and gates to concrete
files/tests.  No implementation edits except planning/result artifacts.

### Phase 3: Opt-in implementation and unit tests

Implement only reviewed opt-in surfaces.  BayesFilter-owned differentiable
code must use TensorFlow/TensorFlow Probability.  NumPy is allowed only for
fixtures, closed-form checks, reporting, and serialization.

### Phase 4: Bounded pilot run

Run the smallest pilot that answers whether the stochastic objective can
execute sanely.  The intended final target may be degree 2, rank 4, batch size
1024, many fresh batches, but the first visible pilot may use a smaller
schedule if needed for runtime.  Any escalation to GPU or long training is a
human-required boundary unless already reviewed and approved.

### Phase 5: Result decision and next handoff

Interpret the pilot result.  A successful pilot can justify a larger training
plan; it does not by itself prove validation readiness or source-faithful
Zhao--Cui parity.

### Phase 6: Guided warm-start mechanism smoke

Test whether guide information can fix the immediate defensive-floor collapse
without claiming fit quality.  The comparison must use identical target-smoke
and audit draws for random and guided arms.  Audit residuals remain veto
diagnostics for lower-gate claims.

### Phase 7: UKF/source-guided initializer design

Design the next initializer before code changes.  The design may use UKF
summaries as support and scale scouts and source-route training clouds as
target-evaluation data, but it must not use audit data or claim UKF truth.

### Phase 8: Source-guided square-root prefit implementation and tiny test

Implement only the reviewed opt-in prefit surface.  The intended first target
is a small source-guided square-root prefit, followed by the existing P75
cross-entropy objective, on a tiny CPU-only same-draw diagnostic.  It must not
launch the degree 2/rank 4/batch 1024/500-batch run.

### Phase 9: Guided prefit decision and larger-pilot handoff

Interpret Phase 8.  Passing a tiny guided prefit diagnostic may justify a
separate larger-pilot plan; it does not by itself prove lower-gate repair,
validation readiness, HMC readiness, scaling, or source-faithful Zhao--Cui
parity.

### Phase 10: Bounded capacity/sample/prefit ladder

Run a small CPU-only diagnostic ladder if and only if Phase 9 review agrees.
This ladder may test degree, rank, batch size, density-objective batches, and
prefit steps under frozen same-draw rules.  It must not run or authorize the
degree-2/rank-4/batch-1024/500-batch pilot.

### Phase 11: Negative ladder decision and redesign handoff

Interpret the Phase 10 ladder.  If the current source-guided prefit produces
no mechanism wins, do not launch the large pilot by inertia.  Decide whether
to stop P75, hand off to a new redesign program, or draft a separately reviewed
larger-pilot plan with a stronger mathematical rationale.

## Global Forbidden Actions

- Do not launch a detached process, nested agent, background runner, or copied
  workspace execution.
- Do not run validation, HMC, scaling, GPU, or rank promotion during P75
  unless a later reviewed phase explicitly reaches that human-required
  boundary and the user approves it.
- Do not change pass/fail criteria or thresholds after seeing outputs.
- Do not train on fresh audit holdout or audit-line samples that are declared
  certification samples.
- Do not call stochastic training source-faithful Zhao--Cui without paper and
  author-source anchors.
- Do not treat training loss, KL proxy, or short pilot success as lower-gate
  repair unless the frozen fresh-audit gates also pass.

## Skeptical Plan Audit

This master program passes the initial skeptical audit because it uses P73 as
the actual blocked baseline, names the objective mismatch as the target,
classifies stochastic training as an extension, separates training and fresh
audit evidence, and gates implementation/pilot runs behind reviewed design
and focused checks.  Routine reviewed phase transitions continue under the
visible runbook unless a human-required boundary appears.
