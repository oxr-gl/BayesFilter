# P72 Phase 5 Subplan: Repaired Lower-Gate Diagnostic

metadata_date: 2026-06-17
status: EXECUTED_BLOCKED_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Current Status Note

The pre-execution skeptical audit initially blocked this phase because the
diagnostic script was schema-only.  Phase 5a repaired the runner, the default
command now emits real bounded Phase 5 rows, and the Phase 5 diagnostic has
executed.  The current result is blocked on residual, line, condition, and
normalizer veto diagnostics, pending Claude read-only review.

## Phase Objective

Run the bounded P72 repaired lower-gate diagnostic using the Phase 4 gate
surfaces and determine whether the former P70 Phase 6h blocker is reduced,
unchanged, or replaced by a new blocker.

## Entry Conditions Inherited From Phase 4

Phase 5 may begin only if:

- Phase 4 result exists and records all checks/tests;
- the P72 diagnostic script exists and is importable;
- `tests/highdim/test_p72_support_certified_lower_gate.py` passes;
- local `git diff --check` passes for the authorized Phase 4 surfaces and
  artifacts;
- this Phase 5 subplan exists with a serious-run evidence contract and
  manifest requirements;
- Claude returns `VERDICT: AGREE` for Phase 4 implementation/result and this
  subplan.

## Required Artifacts

Phase 5 must produce:

- diagnostic JSON under `docs/plans`, using a P72 filename;
- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-result-2026-06-17.md`;
- updated execution and review ledgers;
- Phase 6 root-cause subplan or stop-handoff, depending on diagnostic status.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does the support-certified fixed-fit gate reduce the P70 Phase 6h off-cloud/conditioning blocker on the bounded diagnostic rows without violating the P72 design contract? |
| Exact baseline/comparator | P70 Phase 6h root-cause probes: line growth up to `2.053e10` and `8.987e7`, huge holdout/replay residuals, row-B scaled condition `1.305e14 > 1e14`, and unresolved support mismatch. |
| Primary pass/fail criterion | Every executed P72 bounded row returns the P72 pass status: fit/guard/audit residual gates pass, line absolute/growth gates pass, full normalizer gates pass, support/clipping gates do not block, provenance is complete, P72 condition/effective-rank admission passes, rank activity passes, and audit data is proven excluded from coefficient selection. |
| Veto diagnostics | Any nonfinite target/prediction, missing direct line target, audit cloud entering training, missing provenance hash, normalizer block, line growth block, support block, `kappa > 1e10`, `r_eff < 1`, low-level solver veto at `1e14`, source-faithfulness overclaim, or script/schema mismatch. |
| Explanatory only | Raw fit residuals, raw condition warnings below veto, support warning distances, positive clipping warnings below block threshold, runtime, row labels, and synthetic Phase 4 test magnitudes. |
| What will not be concluded | A pass will not establish d18 validation, rank/degree promotion, HMC readiness, scaling, source-faithful Zhao-Cui parity, or correctness of the adaptive author algorithm. |
| Artifact preserving result | P72 diagnostic JSON, Phase 5 result note, execution ledger, review ledger, and any Phase 6 subplan or stop-handoff. |

## Required Run Manifest

The JSON and result note must record:

- git commit and dirty status;
- exact command;
- conda/Python environment when available;
- CPU/GPU status, with `CUDA_VISIBLE_DEVICES=-1` for this CPU-only run;
- random seeds for fit, guard, audit, and line construction;
- row labels and rank/degree/sample settings;
- wall time;
- output artifact paths;
- Phase 5 subplan path;
- nonclaims.

## Required Checks

Before running:

```bash
git status --short
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p72_support_certified_lower_gate_diagnostic.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p72_support_certified_lower_gate.py
```

Run command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p72_support_certified_lower_gate_diagnostic.py
```

After running:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json >/tmp/p72_phase5_json_check.json
git diff --check -- scripts/p72_support_certified_lower_gate_diagnostic.py docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md
```

If the script still emits only `PHASE4_SCHEMA_READY_PHASE5_NOT_EXECUTED`, stop:
Phase 5 implementation is incomplete and must not be interpreted as a repaired
diagnostic run.

## Forbidden Claims And Actions

- Do not run GPU diagnostics.
- Do not run downstream validation, d18 validation, HMC, rank/degree promotion,
  or scaling benchmarks.
- Do not change thresholds after seeing results.
- Do not use audit clouds or audit-line probes for coefficient selection.
- Do not call the P72 guard/audit/line/admission gates source-faithful.
- Do not compare against a weak baseline in place of the P70 Phase 6h artifact.
- Do not proceed to Phase 6 if the JSON is schema-only or missing required
  manifest fields.

## Exact Next-Phase Handoff Conditions

Phase 6 may begin only if:

- Phase 5 diagnostic JSON exists and is not schema-only;
- Phase 5 result interprets all primary and veto diagnostics;
- the result includes a decision table and nonclaims;
- local checks pass;
- Claude returns `VERDICT: AGREE`;
- if the diagnostic fails, the Phase 6 subplan is a root-cause plan, not a
  validation or promotion plan.

## Stop Conditions

Stop and write a blocker if:

- the script remains schema-only;
- the diagnostic cannot run CPU-only;
- audit exclusion cannot be proven;
- any gate result is missing or nonfinite;
- the diagnostic fails in a way requiring Phase 2/4 redesign;
- Claude and Codex do not converge after five rounds for the same blocker;
- the user redirects the lane.

## Skeptical Plan Audit

Completed before Phase 5 execution.  The initial audit blocked the schema-only
script and created Phase 5a.  After the Phase 5a repair, the default command
was rechecked as a real bounded diagnostic path before execution.  The audit
still forbids treating fit residual improvement, smoke output, or schema output
as promotion evidence.
