# Phase 0 Subplan: Governance, Source Lock, And Runbook Gate

Date: 2026-06-17

## Phase Objective

Review and harden the scalable-OT master program before execution advances.
This phase locks the source-audit result, creates the visible gated execution
runbook, creates the execution ledger and stop handoff, drafts the Phase 1
baseline-fixture subplan, and obtains read-only Claude review convergence.

This phase does not edit algorithm code, run benchmarks, install packages, or
make empirical performance claims.

## Entry Conditions Inherited From Previous Phase

- No earlier execution phase is required for this visible run.
- The self-contained survey paper exists as `.tex` and compiled `.pdf`.
- The source-code audit manifest exists under `.localsource`.
- The static Phase 0 source-lock result exists:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-source-lock-result-2026-06-17.md`.
- The worktree may contain unrelated dirty changes; preserve them.
- Claude may be used only as read-only reviewer.

## Required Artifacts

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-code-master-program-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-source-lock-result-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-visible-gated-execution-runbook-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-visible-execution-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-visible-stop-handoff-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p00-governance-source-lock-result-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p01-baseline-fixture-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p00-claude-review-round-01-2026-06-17.md`

## Required Checks, Tests, And Reviews

Local checks:

1. Verify every required artifact path exists.
2. Verify no unresolved template placeholders remain in the master program,
   runbook, Phase 0 subplan, ledger, stop handoff, or Phase 1 subplan.
3. Verify the master program and runbook identify Codex as supervisor/executor
   and Claude as read-only reviewer only.
4. Verify the master program and Phase 1 subplan preserve the TensorFlow/TFP
   implementation default and non-TensorFlow reference boundary.
5. Verify the master program, source lock, and Phase 1 subplan keep
   Mini-batch/BoMb blocked for decision-grade use until clean source is
   available.
6. Verify the runbook forbids detached execution, nested supervisors,
   destructive actions, and whole-file Claude prompts.

Review:

1. Run Claude Opus at max effort as a read-only reviewer on concise named paths.
2. Save the review output as the required Claude review artifact.
3. Treat `VERDICT: AGREE` as review-convergence evidence only.  Codex may
   advance only if local checks, subplan gates, human-required boundaries, and
   review-convergence evidence all pass.
4. If review says `VERDICT: REVISE`, patch the same artifacts visibly, rerun
   focused local checks, and retry review.
5. Stop after five Claude review rounds for the same blocker.
6. If a broad prompt stalls, run a tiny read-only Claude probe.  If the probe
   responds, redesign the prompt to be narrower and retry.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the governance artifacts complete and safe enough to start Phase 1 baseline-fixture execution for scalable OT candidates? |
| Baseline/comparator | Master program, visible runbook template, source-lock result, survey paper, code audit manifest, and project AGENTS policy. |
| Primary pass criterion | Required artifacts exist, local checks pass, Claude read-only review converges with `VERDICT: AGREE`, Codex confirms no human-required stop is active, and the Phase 0 result records exact Phase 1 handoff conditions. |
| Veto diagnostics | Missing artifact; unresolved template placeholder; Claude used as executor; detached execution allowed; non-TensorFlow default implementation claim; Mini-batch source blocker ignored; missing stop condition; missing Phase 1 handoff. |
| Explanatory diagnostics | Artifact naming clarity, review-loop clarity, and output/log discipline. |
| Not concluded | No algorithm correctness, no speedup, no posterior validity, no production readiness, no public API readiness, no statistically supported ranking. |
| Artifact preserving result | Phase 0 result file, Claude review artifact, and execution ledger entry. |

## Skeptical Plan Audit

- Wrong baseline: Phase 0 uses the source-lock result and current
  TensorFlow dense/streaming transport as baseline context, not a literature
  popularity ranking.
- Proxy metric risk: no source availability or GitHub validity is promoted to
  execution value.
- Missing stop conditions: Claude nonconvergence, missing source, package
  installs, detached execution, and default-policy changes are explicit stops.
- Unfair comparisons: no candidate comparison is run in this phase.
- Hidden assumptions: TensorFlow default and non-TensorFlow reference-only
  boundaries are checked locally.
- Stale context: all artifacts are dated 2026-06-17 and named explicitly.
- Environment mismatch: no GPU, package, or benchmark result is interpreted.
- Artifact adequacy: existence, placeholder, boundary, and review checks answer
  the governance question.

Skeptical audit status: `PASSED_FOR_PHASE_0_GOVERNANCE`.

## Forbidden Claims And Actions

- Do not edit algorithm, benchmark, or test code in this phase.
- Do not run execution benchmarks, GPU checks, package installs, or network
  fetches.
- Do not launch detached execution, nested Codex, or background supervisors.
- Do not paste whole long files into Claude prompts.
- Do not let Claude edit files, run commands, or authorize phase crossing.
- Do not claim any candidate has execution value from source inspection alone.
- Do not unblock Mini-batch/BoMb without clean source or explicit user-supplied
  archive/source.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only after:

- Phase 0 result exists and records `PHASE_0_GOVERNANCE_PASSED`;
- the visible runbook, execution ledger, stop handoff, and Phase 1 subplan
  exist;
- local checks pass;
- Claude review artifact exists and ends with `VERDICT: AGREE` as
  review-convergence evidence, not phase-advancement authorization;
- no human-required stop condition is active.

## Stop Conditions

Stop and write/update the stop handoff if:

- required artifacts cannot be written;
- local checks reveal a material governance inconsistency that cannot be fixed
  locally;
- Claude review does not converge after five rounds for the same blocker;
- continuing requires package installation, network fetch, credentials,
  destructive git/filesystem action, default-policy change, or unrelated dirty
  worktree modification;
- the user redirects or pauses the execution.

## End-Of-Phase Checklist

1. Run the required local checks.
2. Write the Phase 0 result/close record.
3. Draft or refresh the Phase 1 baseline-fixture subplan.
4. Review the Phase 1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
