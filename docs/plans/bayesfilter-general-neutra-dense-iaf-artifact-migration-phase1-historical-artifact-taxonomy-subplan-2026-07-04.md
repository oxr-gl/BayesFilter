# Phase 1 Subplan: Historical Artifact Taxonomy

Date: 2026-07-04

Status: `PHASE1_DRAFT_FOR_REVIEW`

## Phase Objective

Build a read-only taxonomy of historical dense-IAF NeuTra source code, result
notes, replay states, training states, and named evidence cells in
`/home/chakwong/python`. In this phase, "candidate cells" means named
experiment/evidence rows in result notes and JSON summaries, not notebook cells.
Notebook artifacts are outside Phase 1 unless a discovered source/result file
explicitly references one as required evidence. The taxonomy must classify every
discovered candidate in the declared discovery scope, fail-closed, and record
which artifacts may be eligible for a future BayesFilter dense-IAF migration
schema and which are blocked by missing payload, missing target signature,
unsupported schema, unsafe identity fields, or unresolved ambiguity.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result exists and records `PHASE0_GATE_PASSED`.
- The master program and visible runbook exist.
- Claude read-only review of this subplan returned `VERDICT: AGREE`, or all
  fixable review findings were patched and rereviewed.
- Phase 1 remains read-only with respect to `/home/chakwong/python`.
- No network fetch, GPU command, large copy, NeuTra training, or serious HMC is
  authorized by Phase 1.
- Baseline artifact:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-inventory-2026-07-03.json`.
- Handoff artifact:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-visible-stop-handoff-2026-07-03.md`.

## Required Artifacts

- Phase 1 inventory JSON:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-2026-07-04.json`
- Phase 1 result:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-result-2026-07-04.md`
- Phase 2 subplan draft or refresh:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-subplan-2026-07-04.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-visible-execution-ledger-2026-07-04.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-claude-review-ledger-2026-07-04.md`

## Required Checks, Tests, And Reviews

Read-only local checks:

```text
rg -n "paper_dense_iaf|plain_dense_iaf|dense_autoregressive_iaf|DenseAutoregressiveIAFTransport|training_state|replay_state" /home/chakwong/python -g '*.py' -g '*.md' -g '*.json'
find /home/chakwong/python/docs/plans/artifacts -maxdepth 6 -iname '*training_state*.json' -o -iname '*replay_state*.json' -o -iname '*dense*iaf*.json'
stat -c '%s %n' <every discovered candidate payload/note path admitted to inventory>
sha256sum <every discovered candidate payload/note path admitted to inventory when file size permits bounded hashing>
python -m json.tool <every discovered JSON payload admitted for schema inspection when file size permits bounded parsing>
git diff --check -- <Phase 1 result/inventory/subplan docs>
```

Discovery and classification rule:

- The inventory must record the exact discovery commands or scripts and their
  include/exclude rules.
- Every discovered candidate in the declared scope must receive a status. It is
  not sufficient to classify only a selected subset.
- If a discovered artifact is too large for bounded JSON inspection, the
  inventory must still record path, size, hash if feasible, status, and the
  reason payload-level inspection was deferred.
- Uninspected discovered candidates are forbidden unless they are assigned a
  fail-closed status with an explicit reason.

Reviews:

- Codex reviews the inventory for fail-closed classifications before any next
  phase is drafted.
- Claude reviews the Phase 2 schema subplan as a read-only exact-path review.
- If Claude review cannot be obtained after the probe/narrowing protocol, write
  a blocker result instead of advancing.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which historical dense-IAF artifacts and source surfaces are candidates for a BayesFilter dense-IAF migration bridge, and what blocks each candidate? |
| Baseline/comparator | Exact prior inventory `docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-inventory-2026-07-03.json`, exact prior stop handoff `docs/plans/bayesfilter-general-neutra-ssm-interface-visible-stop-handoff-2026-07-03.md`, and legacy dense-IAF source surfaces such as `/home/chakwong/python/src/dsge_hmc/estimation/_transports.py` and replay helpers in legacy scripts. |
| Primary pass criterion | Every discovered candidate in the declared Phase 1 scope is classified fail-closed with path, size, SHA-256 when feasible, payload status, target-signature status, schema status, and next required action. |
| Veto diagnostics | Missing payload, missing generic target signature, unsupported or unknown transport kind, process-local identity, nonfinite JSON payload, unreadable source, or classification ambiguity that would make a future loader unsafe. |
| Explanatory diagnostics | Candidate ID, arm, seed, topology, tensor counts, source result status, step size, leapfrog count, R-hat when available, and whether a training or replay state exists. |
| Not concluded | Loader compatibility, migrated payload success, HMC convergence, posterior correctness, sampler ranking, and default readiness. |
| Result artifact | Phase 1 inventory JSON and Phase 1 result Markdown. |

## Forbidden Claims And Actions

- Do not load historical artifacts through BayesFilter yet.
- Do not copy large payloads into the repo.
- Do not modify `/home/chakwong/python`.
- Do not train, retune, or run HMC.
- Do not run GPU/CUDA commands.
- Do not infer generic target-signature compatibility from legacy target names
  alone.
- Do not classify an artifact as reusable unless schema, payload, logdet
  semantics, and target-signature requirements are explicit and satisfied.
- Do not leave a discovered in-scope candidate without a fail-closed status.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if:

- Phase 1 inventory JSON exists and records classification counts;
- every discovered candidate in the declared scope has one of these statuses:
  `schema_candidate`, `missing_payload`, `missing_target_signature`,
  `unsupported_transport_kind`, `unsafe_identity`, `ambiguous_needs_manual_review`,
  `too_large_for_bounded_payload_inspection`, `not_readable`, or
  `not_migration_candidate`;
- Phase 1 result states what is `correct`, `unsupported`, and `not checked`;
- Phase 1 result records actual commands run, environment, CPU/GPU status, and
  reasons when SHA-256 or JSON parsing was not feasible;
- Phase 2 schema subplan exists and is reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety;
- no Phase 1 stop condition fired.

## Stop Conditions

Stop and write a blocker result if:

- `/home/chakwong/python` is inaccessible;
- legacy dense-IAF source surfaces cannot be located;
- all candidate JSON payloads needed for taxonomy are unreadable;
- any discovered in-scope artifact remains ambiguous without either
  `ambiguous_needs_manual_review` status or a blocker result;
- the inventory cannot account for every discovered in-scope candidate;
- inventory classification would require loading model code, running training,
  running HMC, network fetch, GPU execution, or modifying external files;
- Claude review for the Phase 2 subplan cannot be obtained after the
  probe/narrowing protocol;
- Claude and Codex do not converge after five review rounds for the Phase 2
  subplan.

## Skeptical Plan Audit

Phase 1 is a taxonomy, not evidence of migration success. Historical HMC metrics
are explanatory only. The phase does not treat small JSON parse success, file
existence, or R-hat values as posterior validity. The phase output answers the
artifact-readiness question by preserving blockers instead of bypassing them.

`PHASE1_DRAFT_FOR_REVIEW`
