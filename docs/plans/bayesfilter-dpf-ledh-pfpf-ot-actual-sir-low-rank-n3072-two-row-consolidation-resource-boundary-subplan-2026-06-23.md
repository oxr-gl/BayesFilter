# Actual-SIR Low-Rank N3072 Two-Row Consolidation Resource-Boundary Subplan

Date: 2026-06-23

Status: `DRAFT_READY_FOR_LOCAL_REVIEW_NO_RUNTIME`

## Phase Objective

Consolidate the two completed `N=3072` rank-16 actual-SIR low-rank rows into a
local resource-boundary result and stop automatic runtime escalation unless a
fresh reviewed subplan and human/runtime approval authorize more GPU work.

This phase performs only local artifact validation, evidence classification,
and boundary cleanup. It must not run GPU benchmarks, N3072 seed replication,
N4096, larger shapes, API/default work, HMC work, or route repairs.

## Entry Conditions Inherited From Previous Phase

- N2048 minimal-rank validation passed for:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
- N2048 seed replication passed for the same two rank-16 candidates.
- N3072 representative resource smoke passed for:
  - candidate `r16_eps0p25_alpha1em08_it120`
  - seeds `81137,81138`
  - batch `2`, time steps `20`, particles `3072`
  - aggregate:
    `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.json`
  - result:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-representative-resource-smoke-result-2026-06-23.md`
- N3072 resource-boundary closeout required a fresh subplan, read-only review,
  explicit resource stop conditions, and human/runtime approval for more
  runtime.
- Human approval to continue was provided after that closeout by transcript
  message: `yesI approve`.
- N3072 second-candidate validation passed for:
  - candidate `r16_eps0p125_alpha1em08_it120`
  - seeds `81137,81138`
  - batch `2`, time steps `20`, particles `3072`
  - aggregate:
    `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.json`
  - result:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-second-candidate-validation-result-2026-06-23.md`
- Both N3072 row JSON basenames reached exactly `255` bytes, so future naming
  growth requires renewed dry-run path-length checks before runtime.
- Rank-32/64/128 candidates remain viable but deferred for resource-envelope
  reasons; they are not rejected.

## Required Artifacts

- This subplan.
- N3072 two-row consolidation/resource-boundary result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-two-row-consolidation-resource-boundary-result-2026-06-23.md`
- N3072 representative aggregate JSON and Markdown:
  - `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.json`
  - `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.md`
- N3072 second-candidate aggregate JSON and Markdown:
  - `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.json`
  - `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.md`
- Row JSON/Markdown/log artifacts referenced by both aggregates.
- Updated second-candidate review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-second-candidate-validation-review-ledger-2026-06-23.md`

The result must include a decision table, inference-status table, artifact
manifest, run manifest summary for both rows, post-run red-team note, exact
next handoff, and explicit nonclaims.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before local consolidation.
- Validate both aggregate JSON artifacts:
  - aggregate status `PASS`;
  - `summary.num_candidates = 1` for each aggregate;
  - `summary.num_freeze_nominated = 1` for each aggregate;
  - exact candidate ids:
    - `r16_eps0p25_alpha1em08_it120`;
    - `r16_eps0p125_alpha1em08_it120`;
  - exact assignment epsilons `0.25` and `0.125`;
  - exact seed batch `81137,81138`;
  - exact shape batch `2`, time steps `20`, particles `3072`;
  - row status `PASS`;
  - row hard vetoes `[]`;
  - actual-SIR semantics pass `true`;
  - GPU/XLA/TF32 compiled-core provenance present;
  - selected GPU is GPU 1 in both row manifests;
  - row JSON/Markdown/log artifacts exist;
  - filename components are no longer than `255` bytes.
- Classify diagnostics:
  - hard-veto evidence: row status, hard vetoes, artifact existence,
    provenance, timeout absence, nonfinite absence, actual-SIR semantics pass,
    and comparability thresholds;
  - descriptive-only evidence: warm ratios, warm medians, wall times,
    first-call times, log-likelihood deltas, residual magnitudes, ESS, and GPU
    memory snapshots;
  - statistical evidence: none.
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
- Review the drafted result for consistency, correctness, feasibility,
  artifact coverage, and boundary safety.
- Claude may be used as a read-only reviewer if a material boundary or artifact
  issue is found, but this local no-runtime consolidation does not require
  Claude unless the local review finds a fixable material issue.

## Evidence Contract

- Question: what can be concluded, and what must remain bounded, after one
  passing N3072 row for each rank-16 carry-forward candidate?
- Baseline/comparator: paired streaming actual-SIR route from each row's own
  harness execution under the same seeds, shape, dtype, TF32 mode, GPU
  visibility, and compiled-core timing contract.
- Candidate set:
  - `r16_eps0p25_alpha1em08_it120`;
  - `r16_eps0p125_alpha1em08_it120`.
- Seeds: `81137,81138`.
- Shape: batch `2`, time steps `20`, particles `3072`.
- Primary screen: consolidation passes only if both N3072 aggregate/row
  artifacts validate, no hard vetoes are present, provenance is complete,
  artifacts exist, and all result language preserves claim boundaries.
- Promotion vetoes: any missing/corrupt artifact, candidate/seed/shape
  mismatch, missing row artifact path, filename component over `255` bytes,
  row hard veto, row timeout, incomplete aggregate, missing GPU/XLA/TF32
  provenance, failed actual-SIR semantics, failed comparability threshold, or
  result language that ranks candidates or claims unsupported readiness.
- Continuation vetoes: any artifact inconsistency that cannot be resolved from
  local files, any stale-row mismatch, or any need to run GPU work from this
  phase.
- Explanatory diagnostics only: warm ratios, warm medians, row wall times,
  first-call times, log-likelihood deltas, residual magnitudes, ESS values, and
  GPU memory snapshots.
- What will not be concluded: statistical ranking, speedup, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API/default
  readiness, N4096 feasibility, formal memory scaling, broad scalable-OT
  superiority, production scientific validity, invalidity of either rank-16
  candidate, or invalidity of deferred rank-32/64/128 candidates.
- Artifact preserving result: the N3072 two-row consolidation/resource-boundary
  result plus the two aggregate/row/log artifact sets.

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | What boundary-safe evidence remains after two one-row N3072 rank-16 passes |
| Candidate or mechanism under test | Local evidence classification for `r16_eps0p25_alpha1em08_it120` and `r16_eps0p125_alpha1em08_it120` |
| Expected failure mode | Artifact mismatch, stale candidate/seed/shape, missing provenance, overlong path component, unsupported claim, or hidden runtime escalation |
| Promotion criterion | Both N3072 rows validate locally and the closeout preserves claim boundaries |
| Promotion veto | Artifact/provenance mismatch, hard veto, stale row, overlong filename, or unsupported ranking/readiness claim |
| Continuation veto | Any need for GPU runtime, unresolved artifact corruption, or result requiring a forbidden claim |
| Repair trigger | Fixable documentation mismatch, missing artifact pointer, or unclear evidence classification |
| Explanatory diagnostics | Warm ratios, wall times, first-call times, log-likelihood deltas, residuals, ESS, memory snapshots |
| Must not conclude | Ranking, speedup, correctness, HMC readiness, dense equivalence, default/API readiness, N4096 feasibility, scientific validity, or deferred-candidate invalidity |

## Skeptical Plan Audit

- Wrong baseline check: each row is compared only against its paired streaming
  route from the same harness execution.
- Proxy metric check: warm timing and wall time remain descriptive; they do not
  rank candidates or establish speedup.
- Stop condition check: this phase has a strict no-runtime boundary; any need
  for GPU execution stops the phase and requires a fresh subplan.
- Fairness check: one row per rank-16 candidate is not enough for statistical
  ranking, seed robustness, or default-readiness.
- Hidden assumption check: two N3072 passes do not imply N4096 feasibility,
  formal memory scaling, posterior correctness, or HMC readiness.
- Environment mismatch check: trusted GPU execution was used for the completed
  rows, but this phase performs local validation only.
- Artifact sufficiency check: row JSON/Markdown/log artifacts and aggregate
  JSON/Markdown must be present for both rows.

Audit result: passes as a local consolidation plan because it requires no new
runtime and converts the two N3072 row facts into a boundary-safe handoff.

## Forbidden Claims And Actions

- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not run GPU benchmarks, N3072 seed replication, N4096, larger shapes,
  API/default work, HMC work, or route repairs from this subplan.
- Do not rank the two rank-16 candidates statistically.
- Do not claim speedup, posterior correctness, HMC readiness, dense Sinkhorn
  equivalence, public API/default readiness, scientific superiority, production
  readiness, N4096 feasibility, formal memory scaling, or invalidity of the
  other viable/deferred candidates.
- Do not continue from any artifact or provenance mismatch by treating timing
  evidence as sufficient.

## Exact Next-Phase Handoff Conditions

- If both N3072 row artifact sets validate, write the consolidation result and
  stop automatic runtime escalation.
- If a documentation-only mismatch is found and fixable, patch the affected
  plan/result/ledger visibly, rerun focused local checks, and then write the
  consolidation result.
- If an aggregate or row artifact is missing/corrupt or stale in a way local
  files cannot resolve, write a blocker result and stop for human direction.
- If a future runtime is desired, it must begin from a fresh dedicated subplan,
  read-only review as needed, explicit resource stop conditions, and
  human/runtime approval.

## Stop Conditions

- Any need to execute GPU/runtime benchmark commands.
- Any aggregate/row artifact cannot be read or is corrupt.
- Any candidate id, seed batch, shape, dtype, timing-source, TF32, JIT, or
  device-policy mismatch is found.
- Any row artifact path is missing.
- Any filename component exceeds `255` bytes.
- Any hard veto or failed actual-SIR/comparability/provenance screen is found
  in either completed row.
- The result cannot be written without crossing a forbidden claim boundary.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the N3072 two-row consolidation/resource-boundary result or blocker
   result.
3. Draft or refresh the next handoff instructions. If consolidation passes,
   the default handoff is to stop automatic runtime escalation.
4. Review the handoff for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Subplan Self-Review

- Consistency: follows the second-candidate result and closes the two-row N3072
  evidence without adding runtime.
- Correctness: validates artifacts and provenance before any interpretation.
- Feasibility: local JSON/Markdown/log validation only.
- Artifact coverage: covers both aggregates, both row artifacts, logs, result,
  and ledger.
- Boundary safety: preserves no-NumPy implementation policy and avoids ranking,
  speedup, default/API readiness, posterior-correctness, HMC-readiness, dense
  equivalence, N4096 feasibility, formal memory-scaling, and scientific-validity
  claims.
