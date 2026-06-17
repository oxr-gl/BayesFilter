# Phase 2 Atomized Claude Review Protocol

Date: 2026-06-17

## Purpose

Repair the Phase 2 Claude review gate by replacing broad review prompts with
bounded, atomized read-only checks.  The previous review attempts showed that
Claude probes and a tiny file-aware prompt can respond, while broad review
prompts stall.  This protocol narrows each review to one lane or one boundary.

## Review Unit Contract

Each Claude review unit must be:

- read-only;
- no edits, experiments, agents, or state changes;
- one audit note or one boundary question only;
- bounded by `timeout 180`;
- saved as a review artifact under `docs/plans`;
- ended by Claude with `VERDICT: AGREE` or `VERDICT: REVISE`.

If a unit times out or returns no verdict, retry once with an even smaller
prompt for the same unit.  If it still times out, mark only that unit blocked.

## Lane Review Units

| Unit | Artifact under review | Required check |
| --- | --- | --- |
| `lane-exact-online-gpu` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-exact-online-gpu-audit-2026-06-17.md` | exact semantics/reference-only, Phase 1 comparator, no non-TF default, no execution-value claim |
| `lane-nystrom` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-nystrom-audit-2026-06-17.md` | `source_locked`, approximate kernel, anchors, fixed-rank/epsilon requirements, no execution-value claim |
| `lane-positive-feature` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-audit-2026-06-17.md` | feature-kernel semantic warning, scalar loss not transport, TensorFlow boundary |
| `lane-low-rank-coupling` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-coupling-audit-2026-06-17.md` | semantic replacement, factor marginals, dense error explanatory not exact parity |
| `lane-sparse-localized` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-sparse-localized-audit-2026-06-17.md` | diagnostic-first locality gate, source_reference_only, no sparse implementation before locality |
| `lane-sliced-subspace` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-sliced-subspace-audit-2026-06-17.md` | semantic replacement, projected/full-state distinction, no dense equivalence |
| `lane-minibatch-bomb` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-minibatch-bomb-audit-2026-06-17.md` | `source_partial_user_needed`, blocked, scalar/hierarchical costs not transport |

## Cross-Boundary Review Units

| Unit | Artifact under review | Required check |
| --- | --- | --- |
| `boundary-matrix-and-baseline` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p02-gate-packet-2026-06-17.md` | all seven candidates have matrix coverage and Phase 1 baseline/descriptive comparator |
| `boundary-claims-and-backend` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p02-gate-packet-2026-06-17.md` | no execution-value/ranking/static-source overclaim; non-TF source not default |
| `boundary-blockers-and-handoff` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p02-gate-packet-2026-06-17.md` plus blocker result | Mini-batch blocker preserved; Phase 3 must not begin without aggregate review convergence or explicit user override |

## Aggregate Convergence Rule

Phase 2 Claude review converges if:

- every lane review unit returns `VERDICT: AGREE`;
- every cross-boundary review unit returns `VERDICT: AGREE`;
- any `VERDICT: REVISE` finding is patched visibly and rerun for the focused
  unit;
- no focused unit exceeds the retry limit.

Claude remains a read-only reviewer.  Aggregate agreement is review-convergence
evidence only; Codex must still verify local checks and boundaries before
advancing.
