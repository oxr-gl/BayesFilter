# Actual-SIR Low-Rank N3072 Resource-Boundary Closeout Subplan

Date: 2026-06-23

Status: `DRAFT_READY_FOR_READ_ONLY_REVIEW_BEFORE_EXECUTION`

## Phase Objective

Consolidate the passed N2048 rank-16 evidence and the passed single-row N3072
representative resource smoke, then write a boundary-safe closeout decision for
the current low-rank actual-SIR tuning/validation run.

This phase is local artifact analysis and documentation only. It must not run
GPU benchmarks, change algorithmic code, change defaults, or authorize larger
runtime by implication.

## Entry Conditions Inherited From Previous Phase

- N2048 minimal-rank validation passed for:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
- N2048 seed replication passed for the same two rank-16 candidates.
- N2048 consolidation carried forward both rank-16 candidates as viable and
  unranked.
- N3072 representative resource smoke passed for exactly:
  - `r16_eps0p25_alpha1em08_it120`
  - seeds `81137,81138`
  - batch `2`, time steps `20`, particles `3072`
- `r16_eps0p125_alpha1em08_it120` remains viable but was not tested at N3072.
- Rank-32/64/128 candidates remain viable but deferred for resource-envelope
  reasons; they are not rejected.
- The N3072 representative row selected GPU 1, NVIDIA GeForce RTX 4080 SUPER,
  UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`.
- The aggregate records `selected_physical_gpu.memory_used_mib = 30693` from
  `nvidia-smi` at provenance capture. A trusted post-review `nvidia-smi` check
  reported `32760` MiB total memory for the named device class on this host, so
  the field is locally plausible but remains explanatory only and is not a
  formal memory scaling benchmark.

## Required Artifacts

- This subplan.
- N3072 resource-smoke result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-representative-resource-smoke-result-2026-06-23.md`
- N3072 aggregate JSON:
  `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.json`
- N3072 aggregate Markdown:
  `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.md`
- N3072 row JSON/Markdown/log artifacts referenced by the aggregate.
- Resource-boundary closeout result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-resource-boundary-closeout-result-2026-06-23.md`
- Optional read-only review ledger if Claude review is run:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-resource-boundary-review-ledger-2026-06-23.md`

The closeout result must include a decision table, inference-status table,
artifact manifest, post-run red-team note, exact future-runtime requirements,
and explicit nonclaims.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before execution.
- Local artifact consistency check parsing the N3072 aggregate JSON and
  verifying:
  - aggregate status `PASS`;
  - `summary.num_candidates = 1`;
  - `summary.num_freeze_nominated = 1`;
  - exact candidate id `r16_eps0p25_alpha1em08_it120`;
  - exact seeds `81137,81138`;
  - exact shape batch `2`, time steps `20`, particles `3072`;
  - row status `PASS`;
  - row label `freeze-nominated`;
  - row hard vetoes `[]`;
  - paired comparability pass;
  - warm-screen pass;
  - GPU/TF32 and low-rank provenance complete;
  - warm threshold exactly `1.25`;
  - row JSON/Markdown/log artifacts exist;
  - filename components are no longer than `255` bytes.
- Provenance hierarchy check:
  - aggregate `plan_path` is the broader tuning master program;
  - the dedicated N3072 representative resource-smoke subplan is preserved as
    the governing phase subplan in the result/closeout artifacts because the
    grid runner does not accept a per-phase subplan-path argument.
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
- Review this subplan for consistency, correctness, feasibility, artifact
  coverage, and boundary safety. Claude may be used read-only.

## Evidence Contract

- Question: after two passing N2048 seed batches and one passing N3072
  representative resource smoke, what is the boundary-safe status of the
  current low-rank actual-SIR tuning/validation run?
- Baseline/comparator: prior paired streaming actual-SIR rows from the same
  harness, shape, dtype, TF32 mode, GPU visibility, and compiled-core timing
  contract, plus the N3072 paired streaming row from the representative smoke.
- Candidate set in evidence:
  - N2048 evidence: `r16_eps0p25_alpha1em08_it120` and
    `r16_eps0p125_alpha1em08_it120`
  - N3072 evidence: `r16_eps0p25_alpha1em08_it120` only
- Primary pass criterion: the N3072 aggregate and row artifacts validate
  exactly, the closeout preserves all claim boundaries, and the result does
  not authorize more GPU runtime without a separate reviewed subplan.
- Promotion vetoes: missing/corrupt aggregate, candidate mismatch, stale seed
  or shape mismatch, row hard veto, failed provenance, failed comparability,
  failed warm screen, missing row artifacts, artifact path collision, filename
  component over `255` bytes, or unsupported claim language.
- Continuation vetoes: a future action would require statistical ranking,
  product/default/API claims, scientific validity claims, or large-resource
  execution without fresh human/runtime approval and a reviewed subplan.
- Explanatory diagnostics only: warm ratios, first-call and row wall times,
  selected-physical-GPU memory snapshots, log-likelihood deltas, ESS values,
  and factor residual magnitudes below threshold. Memory snapshots are not
  formal capacity/scaling evidence.
- What will not be concluded: statistical ranking, speedup, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API/default
  readiness, broad scalable-OT superiority, production scientific validity,
  invalidity of `r16_eps0p125_alpha1em08_it120`, or invalidity of deferred
  rank-32/64/128 candidates.
- Artifact preserving result: the resource-boundary closeout result and, if
  Claude is used, the review ledger.

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | What boundary-safe status follows the passed N3072 representative resource smoke? |
| Candidate or mechanism under test | Rank-16 low-rank actual-SIR survivor tier under GPU/XLA compiled-core TensorFlow/TFP execution |
| Expected failure mode | Artifact inconsistency, over-interpretation, or unsupported runtime/scientific/product claim |
| Promotion criterion | Valid N3072 artifact plus closeout that preserves resource and claim boundaries |
| Promotion veto | Invalid artifact, stale mismatch, failed provenance/check, missing row artifact, or unsupported claim |
| Continuation veto | Further GPU runtime without a separate reviewed subplan and explicit resource stop conditions |
| Repair trigger | Artifact mismatch, missing provenance, unsupported claim, or need for a future runtime plan |
| Explanatory diagnostics | Warm ratio, wall time, first-call times, selected-physical-GPU memory snapshot, residuals, log-likelihood deltas |
| Must not conclude | Ranking, speedup, correctness, HMC readiness, dense Sinkhorn equivalence, API/default readiness, scientific validity, or rejection of untested/deferred candidates |

## Skeptical Plan Audit

- Wrong baseline check: use only paired actual-SIR artifacts from the current
  harness; do not use old contaminated P03 rows or proxy rows as current
  promotion evidence.
- Proxy metric check: warm ratio and wall time remain viability/resource-smoke
  diagnostics; they do not prove speedup or superiority.
- Stop condition check: any artifact mismatch, unsupported claim, or proposed
  further GPU runtime without a new reviewed subplan stops this phase.
- Fairness check: the N3072 row is representative by fixed carry-forward
  order only; it must not rank or reject the other viable rank-16 candidate.
- Hidden assumption check: one N3072 row does not imply N3072 two-candidate
  feasibility, N4096 feasibility, posterior correctness, HMC readiness,
  default readiness, or scientific validity.
- Environment mismatch check: selected-GPU memory snapshots are explanatory
  and not formal memory-scaling evidence; the closeout boundary must not depend
  solely on memory-used metadata.
- Artifact sufficiency check: the closeout must cite aggregate, row, log,
  result, and review artifacts.

Audit result: passes as a local closeout/resource-boundary phase because it
runs no new experiment and is designed to prevent over-interpretation of the
passed N3072 representative smoke.

## Forbidden Claims And Actions

- Do not run GPU benchmarks in this phase.
- Do not modify filtering, transport, TensorFlow, TensorFlow Probability, or
  numerical algorithm implementation paths.
- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not rank candidates statistically from descriptive warm timing or from a
  single N3072 representative row.
- Do not claim speedup, posterior correctness, HMC readiness, dense Sinkhorn
  equivalence, public API/default readiness, scientific superiority,
  production readiness, broad scalable-OT selection, or invalidity of
  `r16_eps0p125_alpha1em08_it120` or deferred rank-32/64/128 candidates.
- Do not authorize N3072 two-candidate validation, a second N3072 seed smoke,
  N4096, or any larger runtime without a separate reviewed subplan and explicit
  human/runtime approval.

## Exact Next-Phase Handoff Conditions

- If local artifact validation and checks pass, write the resource-boundary
  closeout result and stop automatic runtime escalation.
- If artifact validation fails, write a blocker result and stop for artifact
  repair selection.
- If the closeout cannot preserve claim boundaries, patch the closeout plan or
  stop for human direction.
- Future runtime may be proposed only through a new dedicated subplan with
  exact candidate ids, seed batch, shape, memory/resource stop conditions,
  artifact contract, and read-only review before execution.

## Stop Conditions

- The N3072 aggregate is missing, corrupt, stale, or not `PASS`.
- Candidate id, seeds, shape, dtype, timing source, TF32 mode, or device policy
  do not match the N3072 resource-smoke contract.
- The closeout treats aggregate `plan_path` as the dedicated phase subplan
  rather than documenting the master-program/phase-subplan hierarchy.
- The row has hard vetoes, failed comparability, failed warm screen, failed
  provenance, missing artifacts, or filename components over `255` bytes.
- Local syntax or focused grid tests fail.
- The result cannot be written without crossing a forbidden claim boundary.
- Continuing would require further GPU runtime, default/API/product-policy
  changes, package installs, network fetches, destructive git/filesystem
  actions, or unsupported scientific/product claims.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the N3072 resource-boundary closeout or blocker result.
3. If stopping automatic runtime escalation, write the exact future-runtime
   handoff conditions instead of drafting another execution subplan.
4. Review the closeout/result for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.

## Subplan Self-Review

- Consistency: follows the N2048 consolidation and N3072 representative-smoke
  result, carrying forward all viable candidates without ranking them.
- Correctness: validates status, candidate identity, seeds, shape, provenance,
  thresholds, row artifacts, and filename bounds.
- Feasibility: local artifact analysis only; no GPU runtime.
- Artifact coverage: specifies aggregate, row, log, result, closeout, and
  optional review-ledger artifacts.
- Boundary safety: avoids ranking, speedup, posterior-correctness,
  default-readiness, HMC-readiness, scientific-validity, and untested-candidate
  rejection claims.
