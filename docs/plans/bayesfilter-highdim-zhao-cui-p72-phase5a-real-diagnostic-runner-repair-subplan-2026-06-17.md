# P72 Phase 5a Subplan: Real Diagnostic Runner Repair

metadata_date: 2026-06-17
status: READY_FOR_PHASE5A_IMPLEMENTATION_AFTER_CLAUDE_R2_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-skeptical-audit-blocker-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Repair the P72 diagnostic script so it can execute real bounded P72 diagnostic
rows and produce a non-schema JSON artifact for Phase 5.  Phase 5a is still an
implementation repair phase; it must not interpret the diagnostic result as
passed or failed.

## Entry Conditions

- Phase 4 passed Claude review.
- Phase 5 skeptical audit blocked execution because the script is schema-only.
- The blocker result exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-skeptical-audit-blocker-result-2026-06-17.md`.

## Authorized Edit Surfaces

Phase 5a may edit:

- `scripts/p72_support_certified_lower_gate_diagnostic.py`;
- `tests/highdim/test_p72_support_certified_lower_gate.py`;
- `bayesfilter/highdim/source_route.py` only for missing helper fields needed
  by the real runner;
- `bayesfilter/highdim/__init__.py` only if a helper export is needed by tests
  or the script;
- required `docs/plans` artifacts and ledgers.

Phase 5a must not edit `bayesfilter/highdim/fitting.py` unless a new,
reviewed, diagnostic-only need is recorded first.

## Required Artifacts

Phase 5a must produce:

- Phase 5a repair result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5a-real-diagnostic-runner-repair-result-2026-06-17.md`;
- a bounded non-Phase-5 smoke JSON artifact proving the default script path is
  no longer schema-only:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5a-runner-smoke-2026-06-17.json`;
- refreshed Phase 5 subplan if the command, options, output path, or evidence
  contract changes;
- updated execution ledger;
- updated review ledger.

## Required Implementation Contents

The repaired script must:

- reuse P69/P70 bounded row mechanics where possible;
- construct real `Z_fit`, `Z_guard`, and `Z_audit` roles for the bounded rows;
- fit only on `Z_fit` plus `Z_guard`;
- prove `Z_audit` and audit-line points are excluded from coefficient
  selection;
- evaluate direct targets for all guard, audit, and line points;
- apply the Phase 4 support/clipping, full normalizer, line, provenance,
  condition/effective-rank, and rank-activity gates;
- emit non-schema JSON with run manifest, row diagnostics, gate summary, and
  nonclaims;
- still support an explicit schema-only mode only if named as such and not used
  by the Phase 5 default command.

## Required Checks

After repair:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p72_support_certified_lower_gate_diagnostic.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p72_support_certified_lower_gate.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p72_support_certified_lower_gate_diagnostic.py --output docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5a-runner-smoke-2026-06-17.json --smoke-only
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5a-runner-smoke-2026-06-17.json >/tmp/p72_phase5a_smoke_json_check.json
rg -n "PHASE4_SCHEMA_READY_PHASE5_NOT_EXECUTED" docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5a-runner-smoke-2026-06-17.json
git diff --check -- scripts/p72_support_certified_lower_gate_diagnostic.py tests/highdim/test_p72_support_certified_lower_gate.py bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5a-real-diagnostic-runner-repair-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md
```

The `rg -n` command above is expected to produce no matches after the repair
because the smoke JSON must not contain the schema-only sentinel.  Record its
exit code/output explicitly as pass evidence for "sentinel absent"; do not use
shell chaining that would hide the result.

The `--smoke-only` invocation must use the same default script execution path
and gate code as Phase 5, but with tiny bounded rows and an explicit
`smoke_only_not_phase5_evidence` manifest field.  It is implementation evidence
only and must not be interpreted as Phase 5 diagnostic evidence.

Do not run the full Phase 5 diagnostic until Claude agrees the repair is ready.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the P72 script now capable of producing a real bounded diagnostic JSON rather than schema-only output? |
| Baseline/comparator | The Phase 4 schema-only script and Phase 5 blocker result. |
| Primary criterion | Focused tests plus the mandatory `--smoke-only` default-path invocation prove the script is non-schema diagnostic-capable, audit exclusion is manifest-tested, required gate fields are present, the schema sentinel is absent from smoke JSON, and local checks pass. |
| Veto diagnostics | Default command still schema-only, audit data enters training, missing direct targets, missing normalizer/provenance/line/condition/rank gates, threshold drift, source-faithfulness overclaim, or Phase 5 full diagnostic run before review. |
| Explanatory only | Stub row magnitudes and schema field order. |
| Not concluded | No repaired lower-gate pass/fail, no d18 validation, no HMC readiness. |

## Forbidden Claims And Actions

- Do not run the full Phase 5 diagnostic in Phase 5a.
- Do not change P72 thresholds or seeds.
- Do not use audit data for coefficient selection.
- Do not add shape/stable-LS/Christoffel/leverage/oversampling logic.
- Do not claim source-faithfulness for P72 guard/audit/line gates.
- Do not treat synthetic tests as evidence that the numerical blocker is fixed.

## Exact Next-Phase Handoff Conditions

Phase 5 diagnostic execution may resume only if:

- Phase 5a result exists and records passing local checks;
- the default script path is non-schema diagnostic-capable as shown by the
  required `--smoke-only` JSON artifact;
- Phase 5 subplan is refreshed if command/options changed;
- Claude returns `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- a real runner requires changing Phase 2 thresholds;
- audit exclusion cannot be proven;
- real bounded-row construction requires unreviewed source-route changes;
- local tests fail in a way requiring Phase 2/4 redesign;
- Claude and Codex do not converge after five rounds for the same blocker.
