# Actual-SIR Low-Rank N3072 Replicated-Evidence Resource-Boundary Subplan

Date: 2026-06-23

Status: `EXECUTED_PASS_RESULT_WRITTEN_STOP_AUTOMATIC_RUNTIME_ESCALATION`

## Phase Objective

Run a no-runtime local closeout over the completed N3072 actual-SIR low-rank
rank-16 evidence. This phase validates artifact integrity and evidence
boundaries across the two N3072 seed batches:

- seed batch `81137,81138`, one row per candidate from the representative and
  second-candidate N3072 phases;
- seed batch `81139,81140`, two rows from the seed-replication phase.

The phase asks whether the current N3072 evidence supports the bounded statement
that both rank-16 candidates remain viable under two N3072 seed batches, while
stopping automatic runtime escalation. It must not run GPU benchmarks, N4096
jobs, larger shapes, route repairs, HMC work, API/default work, or scientific
claim work.

## Entry Conditions Inherited From Previous Phase

- N3072 representative resource smoke passed for
  `r16_eps0p25_alpha1em08_it120` on seeds `81137,81138`.
- N3072 second-candidate validation passed for
  `r16_eps0p125_alpha1em08_it120` on seeds `81137,81138`.
- N3072 seed replication passed for both rank-16 candidates on fresh seeds
  `81139,81140`.
- The seed-replication subplan passed skeptical audit, local checks, exact
  dry-run path-length validation, Claude Opus/max read-only review, and trusted
  GPU precheck before execution.
- The current phase is a local consolidation only; it inherits no authorization
  for further runtime.

## Required Artifacts

- This subplan.
- N3072 two-row consolidation/resource-boundary result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-two-row-consolidation-resource-boundary-result-2026-06-23.md`
- N3072 seed-replication result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-seed-replication-result-2026-06-23.md`
- Source aggregate JSON artifacts:
  - `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.json`
  - `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.json`
  - `docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.json`
- Row JSON/Markdown/log artifacts referenced by those aggregates.
- N3072 replicated-evidence/resource-boundary result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-replicated-evidence-resource-boundary-result-2026-06-23.md`

## Required Checks, Tests, And Reviews

- Skeptical plan audit before local validation.
- No-runtime JSON/artifact validator confirming:
  - exactly four total validated rows;
  - exact candidates `r16_eps0p25_alpha1em08_it120` and
    `r16_eps0p125_alpha1em08_it120`;
  - exact N3072 seed batches `81137,81138` and `81139,81140`;
  - row status `PASS` for all rows;
  - row hard vetoes `[]`;
  - paired comparability `true`;
  - actual-SIR semantics `true`;
  - low-rank and GPU/TF32 provenance complete;
  - row JSON/Markdown/log artifacts exist;
  - row filename components are no longer than `255` bytes.
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
- Boundary scan of this subplan and result for unsupported ranking, speedup,
  posterior-correctness, HMC-readiness, dense-equivalence, public API/default,
  N4096-feasibility, formal memory-scaling, production-readiness, or scientific
  validity claims.
- Claude may be used as read-only reviewer if a material consistency,
  feasibility, artifact-coverage, or boundary-safety issue is found. Claude is
  not an execution authority and cannot authorize crossing human, runtime,
  model-file, funding, product-capability, default-policy, public API, or
  scientific-claim boundaries.

## Evidence Contract

- Question: after local validation of the completed N3072 artifacts, do both
  rank-16 candidates remain viable under two N3072 seed batches with no hard
  vetoes and complete artifact/provenance records?
- Baseline/comparator: each row's paired streaming actual-SIR route from the
  same harness run, same seed batch, same shape, same dtype/TF32 policy, same
  GPU visibility, and same compiled-core timing contract.
- Candidate set:
  - `r16_eps0p25_alpha1em08_it120`;
  - `r16_eps0p125_alpha1em08_it120`.
- Seed batches: `81137,81138` and `81139,81140`.
- Shape: batch `2`, time steps `20`, particles `3072`.
- Primary screen: closeout passes only if all four row artifacts validate with
  status `PASS`, no hard vetoes, complete provenance, paired comparability,
  actual-SIR semantics, and present row JSON/Markdown/log artifacts.
- Promotion vetoes: missing/corrupt aggregate, source candidate mismatch, seed
  or shape mismatch, row hard veto, missing actual-SIR semantics, missing
  compiled/GPU/TF32 provenance, missing row artifact, filename component over
  `255` bytes, failed local syntax/test check, or boundary scan finding a
  forbidden claim.
- Continuation vetoes: any artifact validation failure, any unsupported claim
  required to interpret the result, or any need for new runtime.
- Explanatory diagnostics only: warm ratios, wall times, log-likelihood deltas,
  ESS, residual magnitudes, GPU memory snapshots, and filename lengths below
  the ceiling.
- What will not be concluded: statistical ranking, speedup, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API/default
  readiness, N4096 feasibility, formal memory scaling, broad scalable-OT
  superiority, production scientific validity, or invalidity of deferred
  rank-32/64/128 candidates.
- Artifact preserving result: the replicated-evidence/resource-boundary result
  file named above.

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Whether completed artifacts support a bounded N3072 viability closeout for both rank-16 candidates |
| Candidate or mechanism under test | `r16_eps0p25_alpha1em08_it120` and `r16_eps0p125_alpha1em08_it120` under GPU/XLA compiled-core TensorFlow/TFP execution |
| Expected failure mode | Artifact mismatch, missing provenance, path-length issue, unsupported claim, or stale-row mismatch |
| Promotion criterion | All four N3072 rows validate locally with no hard vetoes and complete artifacts/provenance |
| Promotion veto | Any missing/corrupt artifact, mismatch, hard veto, failed semantics/comparability/provenance, overlong filename, failed local check, or boundary violation |
| Continuation veto | Any need for new runtime or any result interpretation requiring a forbidden claim |
| Repair trigger | Artifact/provenance/path validation failure, result-note claim mismatch, or stale evidence |
| Explanatory diagnostics | Warm ratios, wall times, log-likelihood deltas, ESS, residuals, GPU memory snapshots, filename lengths |
| Must not conclude | Ranking, speedup, correctness, HMC readiness, dense equivalence, API/default readiness, N4096 feasibility, formal memory scaling, scientific validity, or invalidity of deferred candidates |

## Skeptical Plan Audit

- Wrong baseline check: this phase reuses each row's paired streaming comparator
  from the same completed harness run; it does not compare against stale or
  unrelated baselines.
- Proxy metric check: warm ratios and timings remain descriptive and cannot
  become speedup, ranking, default-readiness, or production-readiness evidence.
- Stop condition check: any artifact mismatch, missing provenance, failed local
  check, or forbidden claim blocks a pass.
- Fairness check: both rank-16 candidates are represented at both N3072 seed
  batches; deferred rank-32/64/128 candidates are not evaluated or rejected.
- Hidden assumption check: two N3072 seed batches do not imply N4096 feasibility,
  statistical ranking, posterior correctness, HMC readiness, formal memory
  scaling, API/default readiness, or scientific validity.
- Environment mismatch check: no new GPU runtime is authorized; prior GPU
  snapshots remain descriptive context only.
- Artifact sufficiency check: the validator must inspect aggregate fields, row
  JSON fields, row artifact paths, and filename lengths.

Audit result: passes as a no-runtime local closeout plan because it validates
completed artifacts only, preserves explicit claim boundaries, and stops
automatic runtime escalation.

## Forbidden Claims And Actions

- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not run GPU benchmarks, N4096, larger shapes, HMC work, route repairs,
  API/default changes, or scientific-claim experiments from this subplan.
- Do not use old contaminated P03 rows as current evidence.
- Do not rank candidates statistically from descriptive metrics.
- Do not claim speedup, posterior correctness, HMC readiness, dense Sinkhorn
  equivalence, public API/default readiness, scientific superiority,
  production readiness, N4096 feasibility, formal memory scaling, or invalidity
  of either rank-16 candidate or deferred rank-32/64/128 candidates.
- Do not continue from validation failures as if timing evidence were valid.

## Exact Next-Phase Handoff Conditions

- If local validation and checks pass, write the closeout result and stop
  automatic runtime escalation. Any future runtime requires a fresh dedicated
  subplan, review as needed, resource stop conditions, and explicit user/runtime
  approval.
- If validation fails due to artifact or provenance mismatch, write a blocker
  result and stop for repair or human direction.
- If local tests fail, write a blocker result and stop for focused repair.
- If the result cannot be interpreted without a forbidden claim, write a
  blocker result and stop for clarification.

## Stop Conditions

- Any source aggregate is missing or corrupt.
- The validator cannot match exact candidate ids, seed batches, shape, dtype,
  timing source, TF32 mode, or device policy.
- Any row lacks actual-SIR semantics, paired comparability, GPU/XLA/TF32
  provenance, or row JSON/Markdown/log artifacts.
- Any row has a hard veto or failed status.
- Any filename component exceeds `255` bytes.
- Required local checks fail.
- The phase would require new runtime or crossing a forbidden claim boundary.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the replicated-evidence/resource-boundary result or blocker result.
3. State the next handoff conditions clearly.
4. Stop automatic runtime escalation unless the user requests a fresh reviewed
   runtime subplan.

## Subplan Self-Review

- Consistency: follows the reviewed N3072 seed-replication result and prior
  two-row consolidation.
- Correctness: validates exact candidates, seed batches, status, hard vetoes,
  provenance, semantics, artifact paths, and filename lengths.
- Feasibility: local JSON/artifact validation only; no GPU runtime.
- Artifact coverage: includes aggregate JSONs, row artifacts, prior results,
  this subplan, and closeout result.
- Boundary safety: preserves no-NumPy implementation policy and forbids ranking,
  speedup, posterior-correctness, HMC-readiness, dense-equivalence,
  public API/default, N4096-feasibility, formal memory-scaling, production, and
  scientific-validity claims.
