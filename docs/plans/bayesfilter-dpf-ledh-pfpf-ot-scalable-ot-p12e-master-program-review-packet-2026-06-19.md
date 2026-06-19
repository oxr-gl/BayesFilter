# P12E Master Program Review Packet

Date: 2026-06-19
Purpose: concise Claude read-only review packet for the P12E master program and
phase subplans.

## Review Scope

Review paths:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-master-program-2026-06-19.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p0-first-checks-subplan-2026-06-19.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p1-diagnostic-implementation-subplan-2026-06-19.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p2-smoke-diagnostic-subplan-2026-06-19.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p3-official-diagnostic-subplan-2026-06-19.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p4-closeout-handoff-subplan-2026-06-19.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-visible-gated-overnight-execution-plan-2026-06-19.md`

Do not edit files.  Do not execute commands.  Do not launch agents.

## Key Contract

Codex is supervisor and executor.  Claude is read-only reviewer only.
These are execution/review roles, not additional active Wave 1 agents.  The
only active Wave 1 agents remain `peer agent` and `current agent`.

The lane asks:

Do deterministic LEDH-like post-flow particles exhibit enough local support
concentration that sparse/localized OT work should be reopened after Phase 8
blocked sparse implementation on Phase 1 dense fixtures?

## Required Review Checks

Check:

- exactly two active agents only: `peer agent` and `current agent`;
- no dependency on peer-agent artifacts during active execution;
- every phase has a dedicated subplan;
- each subplan states objective, entry conditions, required artifacts,
  checks/tests/reviews, evidence contract, forbidden claims/actions,
  next-phase handoff, and stop conditions;
- end-of-phase obligations are present;
- repair loop is explicit and does not stop for non-valid reasons;
- Claude is read-only reviewer, not execution authority;
- no execution is launched before human approvals;
- no whole-file Claude prompt is required;
- no sparse solver implementation is authorized;
- CPU-only TensorFlow import ordering is preserved;
- package install, network fetch, GPU evidence, external sparse solvers,
  shared-file edits, threshold changes after results, and unsupported claims
  are stop conditions;
- final statuses are limited to the approved status family.

## Known Risks For Review

- P12E-1 must preserve Phase 8 orientation/truncation semantics when adapting
  to LEDH post-flow particles.
- Fixture provenance must be fully frozen in code/JSON before official
  diagnostic interpretation.
- Claude prompts must be short and path-based to avoid approval blocks.

## Expected Review Output

Findings first, with file/line references when possible.

End with exactly one of:

- `VERDICT: AGREE`
- `VERDICT: REVISE`
