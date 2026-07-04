# Phase 6 Result: Existing NeuTra Artifact Reuse Bridge

Date: 2026-07-03

Status: `PHASE6_GATE_PASSED_WITH_REAL_ARTIFACT_REUSE_BLOCKED`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Which existing NeuTra artifacts are safely reusable as frozen transports for the generic BayesFilter target interface? |
| Baseline/comparator | Existing `~/python` closeout notes, candidate summaries, and artifact hashes. |
| Primary criterion | Passed fail-closed: all checked artifacts are explicitly classified; no missing, unsigned, or signature-absent artifact was used as reusable. |
| Veto diagnostics | No Phase 6 veto fired. No missing payload was loaded, no absent target signature was treated as compatible, no loader warning was treated as pass, and no serious HMC was launched. |
| Explanatory diagnostics | Candidate IDs, step sizes, leapfrog counts, R-hat values where available, file sizes, SHA-256 hashes, historical notes, and missing payload checks. |
| Not concluded | No new NeuTra training, no real-artifact loader reuse success, no HMC convergence, no posterior validity, no method ranking, and no default-readiness claim. |
| Artifacts | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-inventory-2026-07-03.json` and this result. |

## Decision

The user is right that there are successful NeuTra training/HMC artifacts in
`~/python`, and Phase 6 found the intended evidence cells. Those artifacts
should be reused as historical evidence, target-specific design input, and
future migration fixtures.

They are not yet reusable by the new generic BayesFilter loader. None of the
checked external artifacts exposes both:

- the Phase 4 loader schema `bayesfilter.neutra.frozen_affine_diag.v1`; and
- a stable generic `SSMTargetContract` `target_signature`.

Several result notes also reference training-state payloads that are absent in
the reconciled checkout. Because the Phase 6 contract is fail-closed, no
external artifact was loaded and no mechanics canary was run.

## Inventory Summary

| Cell | Candidate | Step | L | Max R-hat | Historical status | Generic loader classification |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| NK + linear solver + Kalman | 45 | 0.5 | 4 | 1.0007741578596723 | Manual closeout reconstructed after reducer metadata failure | `signature_not_available_nonreusable` |
| NK + linear solver + principal-sqrt UKF | 44 | 0.5 | 3 | n/a | Budgeted reducer completed; weaker evidence | `signature_not_available_nonreusable` |
| Rotemberg + linear solver + KF | 46 | 0.5 | 8 | 1.0018239461076908 | Mechanically completed, but tuning invalid high acceptance | `missing_payload` |
| Rotemberg + linear solver + pruned UKF | 92 | 1.03125 | 3 | 1.1364772795911446 | Completed serious baseline with diagnostics | `missing_payload` |
| Rotemberg + second solver + pruned UKF | 603 | 0.729166666666 | 2 | 1.0032378500239167 | Completed serious baseline | `missing_payload` |

Additional checked artifacts include the Rotemberg XLA HMC gate, the fixed
transport tuning repair result, the SGU serious launch JSON, the Phase 10f
relaunch dry-run, and the NK Phase 8 freeze manifest. They also lack the new
generic loader signature contract and are classified nonreusable in the
inventory JSON.

## Separate Ledgers

| Ledger | Status |
| --- | --- |
| Trained-transport availability | Historical trained-transport evidence exists. Referenced full training-state payloads for the Rotemberg/SGU serious runs were missing at their recorded paths in this checkout. |
| Loader success | No external artifact was passed to `load_frozen_neutra_artifact` because none satisfied the required schema/signature precondition. |
| Target-signature compatibility | Not established for external artifacts. Older artifacts carry target identity, adapter signatures, or transport manifest hashes, but not the new generic `SSMTargetContract` target signature. |
| HMC/mechanics canary | Not run on external artifacts. Running it would have violated the Phase 6 rule against using signature-absent or missing-payload artifacts as reusable. |

## Local Checks

Commands run for this phase were read-only inventory checks:

```text
find /home/chakwong/python/docs/plans/artifacts ...
rg -n "candidate_index|R-hat|step_size|target_signature|transport_manifest_hash" /home/chakwong/python/...
sha256sum <selected result notes and JSON summaries>
stat -c '%s %n' <selected result notes and JSON summaries>
test -e <referenced training-state payloads>
```

No GPU/CUDA probe, NeuTra training, serious HMC, or detached execution was
launched. No large payload was copied into the BayesFilter repo.

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for Phase 6 reuse safety: no missing/signature-absent artifact was used as reusable. |
| Statistically supported ranking | None. Existing candidate choices remain historical reducer/tuning outcomes, not statistical method rankings. |
| Descriptive-only differences | R-hat, ESS, acceptance, runtime, and candidate score values remain descriptive unless a source result note made them part of a predeclared hard screen. |
| Default-readiness | Not established. |
| Next evidence needed | A migration bridge that exports a small BayesFilter-owned frozen-transport manifest with target signature, transport hash, dimension, logdet semantics, and payload or a restoration plan for missing training states. |

## Decision Table

| Decision field | Status |
| --- | --- |
| Primary criterion | Passed fail-closed classification. |
| Veto diagnostic status | No active veto. |
| Main uncertainty | Whether the missing training-state payloads can be restored or whether dense IAF artifacts need a new supported loader schema rather than the Phase 4 affine-diagonal fixture schema. |
| Next justified action | Phase 7 should validate the implemented generic interface with synthetic fixtures and close out with real-artifact reuse blocked pending a signed migration bridge. |
| What is not concluded | No real-artifact loader reuse, no HMC convergence, no posterior correctness, no method superiority, and no production readiness. |

## Phase 7 Handoff

Phase 7 may begin with this narrowed scope:

- re-run the focused generic interface tests from Phases 1-5;
- build a validation ledger that distinguishes implemented generic surfaces
  from real-artifact migration blockers;
- avoid serious HMC and artifact reuse claims;
- recommend a later bridge for dense IAF or restored training-state artifacts.

`PHASE6_GATE_PASSED_WITH_REAL_ARTIFACT_REUSE_BLOCKED`
