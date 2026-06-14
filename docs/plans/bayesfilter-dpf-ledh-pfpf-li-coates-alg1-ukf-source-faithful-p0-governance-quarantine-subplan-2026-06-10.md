# P0 Subplan: Governance And Evidence Quarantine

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we make the old LEDH-PFPF-OT evidence impossible to accidentally cite as source-faithful method evidence before rebuilding Algorithm 1? |
| Baseline/comparator | Existing LEDH-PFPF-OT plans, reports, JSON files, runner code, and P8/P44 amendments. |
| Primary pass criterion | A quarantine manifest and supersession note identify old LEDH-PFPF-OT artifacts and state that none may support source-faithful LEDH-PFPF claims. |
| Veto diagnostics | Deleting historical files, overwriting old result files, leaving the 2026-06-10 auxiliary-flow-only repair labelled as final source-faithful evidence, or omitting known LEDH-PFPF-OT artifacts from the manifest without explanation. |
| Explanatory diagnostics | Artifact counts, route identifiers, old method labels, old result-table row counts. |
| Not concluded | P0 does not decide the new implementation design and does not run numerical tests. |
| Required artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p0-governance-quarantine-result-2026-06-10.md` |

## Required Actions

1. Search `docs/plans`, `experiments/dpf_implementation`, `tests`, and
   `scripts` for `LEDH-PFPF`, `ledh_pfpf`, `dpf_ledh_pfpf_ot`, and related
   route identifiers.
2. Create a quarantine manifest listing each known artifact, its role, and
   whether it is superseded, historical-only, or reusable as non-evidence
   scaffolding.
3. Explicitly quarantine at least:
   - `docs/plans/bayesfilter-dpf-ledh-pfpf-source-faithful-repair-plan-2026-06-10.md`;
   - `docs/plans/bayesfilter-dpf-ledh-pfpf-source-faithful-repair-result-2026-06-10.md`;
   - `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p8-m3-ledh-pfpf-source-faithful-amendment-2026-06-10.md`;
   - `experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_source_faithful_repair_tf.py`;
   - reports and JSON outputs from the same repair lineage.
4. Write a short supersession rule:
   - old LEDH-PFPF-OT rows are discarded for method claims;
   - old rows may be used only as regression symptoms or historical lineage;
   - new tables must use a source-route identifier that includes Algorithm 1
     UKF covariance lifecycle evidence.
5. Run Claude read-only review until `VERDICT: AGREE` or five loops.

## Skeptical Audit

| Risk | Control |
| --- | --- |
| Treating quarantine as deletion | Historical artifacts remain in place. |
| Missing old artifacts | Use `rg --files`/`rg` inventory before writing the result. |
| Quarantining too broadly | Non-LEDH-PFPF-OT artifacts remain usable if their own evidence contracts pass. |
| Letting old scaffolding leak into new results | New implementation must carry a new source-route identifier and generation tag. |

## Gate

P0 passes only when the result artifact includes the manifest, supersession
language, command log, and Claude review verdict.
