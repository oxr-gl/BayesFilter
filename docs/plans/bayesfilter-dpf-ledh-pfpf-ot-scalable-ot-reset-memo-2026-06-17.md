# Reset Memo: Scalable OT For LEDH-PFPF-OT

Date: 2026-06-17
Timestamp: 2026-06-18T04:18:30+08:00

## Current Status

`PHASE_10_COMPARATIVE_DECISION_COMPLETED_NO_DEFAULT_ALGORITHM_YET`

The scalable OT master program has completed the source-lock, survey,
candidate audit, interface, prototype/diagnostic, and comparative-decision
passes.  No BayesFilter default algorithm has been changed.

## Main Decision

Do not pick a production/default scalable OT algorithm yet.

The next justified technical target is a reviewed reduced-rank Nystrom ladder,
because Phase 4 validated the TensorFlow factor route at full rank with the
lowest semantic mismatch.  This is not a claim that Nystrom is fastest or best;
rank reduction, memory/runtime behavior, and downstream LEDH filtering behavior
remain untested.

## Lane Status

| Lane | Status | Carry-forward rule |
| --- | --- | --- |
| Dense/streaming baseline | Phase 1 comparator passed | Keep as local reference. |
| Nystrom | Full-rank factor route passed | Next reduced-rank ladder candidate; no scalability claim yet. |
| Positive-feature | Semantic-replacement validity passed | Optional downstream surrogate, not dense equivalence. |
| Low-rank coupling | `Q,R,g` transport-object fixture passed | Needs true solver-route plan before solver-fidelity claims. |
| Exact online/GPU | Reference-only close | Revisit only with TensorFlow parity or approved external/GPU plan. |
| Sparse/localized | Phase 8 locality screen blocks implementation for now | Reopen only with LEDH-specific locality evidence or revised reviewed criteria. |
| Sliced/subspace | Semantic-replacement projection diagnostic passed | Optional downstream surrogate, not dense equivalence. |
| Mini-batch/BoMb | Source-blocked | Needs clean source/archive and transport-object audit. |

## Non-Claims To Preserve

- No speedup claim.
- No production/default readiness.
- No posterior correctness.
- No HMC-readiness.
- No public API readiness.
- No statistically supported ranking.
- No sparse solver validity.
- No dense entropic equivalence for semantic-replacement lanes.
- No Mini-batch/BoMb viability until clean source is provided.

## Key Artifacts

| Purpose | Artifact |
| --- | --- |
| Master program | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-code-master-program-2026-06-17.md` |
| Survey paper | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex` |
| Source lock | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-source-lock-result-2026-06-17.md` |
| Execution runbook | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-visible-gated-execution-runbook-2026-06-17.md` |
| Ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-visible-execution-ledger-2026-06-17.md` |
| Stop handoff | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-visible-stop-handoff-2026-06-17.md` |
| Phase 10 decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p10-comparative-decision-result-2026-06-17.md` |

## Recommended Next Plan

Write a new reviewed subplan for a reduced-rank Nystrom ladder.

Minimum contract:

- Phase 1 dense/streaming baseline remains comparator.
- Include Phase 1 fixtures plus at least one LEDH-specific fixture before any
  LEDH algorithm selection claim.
- Predeclare rank grid, dense-reference thresholds, marginal residual
  thresholds, finite checks, and memory/runtime proxy role.
- Treat runtime/memory as explanatory until validity passes.
- Keep GPU/external/POT/network/package actions blocked unless separately
  approved.
- Do not rank against semantic-replacement lanes without downstream
  uncertainty-aware evidence.

## Dirty Worktree Note

The repository contains unrelated dirty worktree changes outside this scalable
OT runbook, including BayesFilter HMC/linear/test files.  Preserve them.  Do
not revert unrelated user work.

## Review Note

Claude was used only as read-only reviewer.  Broad file reviews sometimes
stalled or produced tool-shape issues, so bounded micro-reviews were used when
appropriate under the user's approval.
