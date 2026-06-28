# Actual-SIR Low-Rank N2048 Consolidation Resource-Decision Subplan

Date: 2026-06-23

Status: `DRAFT_READY_FOR_READ_ONLY_REVIEW_BEFORE_EXECUTION`

## Phase Objective

Consolidate the two completed N2048 rank-16 validation aggregates and decide
the next bounded phase: either a resource-feasibility subplan for larger `N`, a
single representative-arm resource smoke, or a stop/handoff if the evidence
does not justify more runtime.

This phase is local artifact analysis only. It must not run GPU benchmarks or
modify algorithmic code.

## Entry Conditions Inherited From Previous Phase

- N2048 minimal-rank validation passed for:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
- N2048 seed replication passed for the same two candidates.
- Required aggregates:
  - `docs/benchmarks/actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23.json`
  - `docs/benchmarks/actual-sir-low-rank-n2048-seed-replication-2026-06-23.json`
- Both phases used GPU-visible TensorFlow/TFP, `float32`, TF32 enabled,
  compiled-core timing sources, and `jit_compile=True`.
- Row artifact naming repair has passed focused checks and both N2048
  aggregates preserve distinct row JSON/Markdown/log paths.
- Rank-32/64/128 candidates remain viable but deferred; this phase must not
  claim they are inferior, invalid, or scientifically rejected.

## Required Artifacts

- This subplan.
- The two N2048 aggregate JSON files listed above.
- Consolidation result/close record:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n2048-consolidation-resource-decision-result-2026-06-23.md`
- A next subplan before any further execution.

The phase result must include a decision table, inference-status table,
artifact manifest, post-run red-team note, and exact handoff.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before execution.
- Local artifact consistency check parsing both N2048 aggregate JSON files and
  verifying:
  - exact candidate ids;
  - exact seed batches `81133,81134` and `81135,81136`;
  - aggregate status `PASS`;
  - every row status `PASS`;
  - row labels `freeze-nominated`;
  - no hard vetoes;
  - paired comparability pass;
  - warm-screen pass;
  - GPU/TF32 and low-rank provenance complete;
  - warm threshold exactly `1.25`;
  - row JSON/Markdown/log artifacts exist and are distinct within each
    aggregate;
  - filename components are no longer than `255` characters.
- Local syntax and focused grid tests remain useful guardrails:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  and
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`.
- Review this consolidation subplan for consistency, correctness, feasibility,
  artifact coverage, and boundary safety. Claude may be used read-only.

## Evidence Contract

- Question: after two independent N2048 seed batches, what is the next
  evidence-safe phase for the rank-16 survivor tier?
- Baseline/comparator: the two completed N2048 aggregates, each paired against
  streaming actual-SIR rows from the same harness, shape, dtype, TF32 mode, GPU
  visibility, and compiled-core timing contract.
- Candidate set:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
- Primary pass criterion for consolidation: both N2048 aggregates pass the
  artifact consistency check above and support "both candidates remain viable
  under the two checked N2048 seed batches".
- Decision options:
  - `larger_N_resource_feasibility_subplan`: choose this only if artifacts are
    valid and the close record explicitly treats N2048 memory use as a resource
    risk, not as a scientific veto.
  - `single_representative_arm_smoke_subplan`: choose this only if the result
    explicitly states the representative arm is a runtime/resource diagnostic
    and not a statistical winner.
  - `stop_or_handoff`: choose this if artifacts are invalid, if resource risk
    is too high for an unattended run, or if the next phase would require a
    forbidden claim.
- Promotion vetoes: missing/corrupt aggregate, candidate mismatch, row hard
  veto, failed provenance, failed comparability, failed warm screen, missing row
  artifacts, artifact path collision, filename length over `255`, or stale seed
  mismatch.
- Continuation vetoes: either N2048 aggregate is invalid, the next action would
  require ranking candidates statistically, or the next action would cross
  posterior-correctness, HMC-readiness, API/default-readiness, dense Sinkhorn
  equivalence, or scientific-validity boundaries.
- Explanatory diagnostics only: warm ratios, row wall times, log-likelihood
  deltas, factor residuals, and selected-GPU memory snapshots.
- What will not be concluded: statistical ranking, speedup, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API/default
  readiness, broad scalable-OT superiority, production scientific validity, or
  invalidity of deferred rank-32/64/128 candidates.
- Artifact preserving result: the consolidation result/close record and the
  next reviewed subplan.

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Which evidence-safe phase should follow two passing N2048 seed batches? |
| Candidate or mechanism under test | Rank-16 low-rank actual-SIR survivor tier under GPU/XLA compiled-core TensorFlow/TFP execution |
| Expected failure mode | Artifact inconsistency, over-interpretation, resource-envelope ambiguity, or unsupported ranking |
| Promotion criterion | Both N2048 aggregates validate and the next phase preserves claim boundaries |
| Promotion veto | Any invalid aggregate/artifact, hard veto, stale mismatch, or unsupported statistical/product/scientific claim |
| Continuation veto | Invalid aggregate or next phase requiring forbidden claim boundaries |
| Repair trigger | Artifact inconsistency, missing provenance, path collision, or resource risk needing a smaller diagnostic |
| Explanatory diagnostics | Warm ratios, wall times, residuals, log-likelihood deltas, memory snapshots |
| Must not conclude | Ranking, speedup, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, or invalidity of deferred viable candidates |

## Skeptical Plan Audit

- Wrong baseline check: use only the two valid N2048 paired aggregates, not old
  P03 rows, N512/N1024 results, or unpaired timing.
- Proxy metric check: warm ratio and wall time may motivate resource planning
  but cannot prove speedup or superiority.
- Stop condition check: invalid artifacts or any forbidden claim boundary stop
  the phase before a next runtime plan.
- Fairness check: both N2048 aggregates used the same candidate ids, shape,
  dtype, TF32 mode, timing sources, GPU visibility, rank, alpha, and projection
  iteration count; only assignment epsilon and seed batch varied as planned.
- Hidden assumption check: N2048 viability does not imply N4096 feasibility,
  posterior correctness, or default-readiness.
- Environment mismatch check: GPU memory observations are explanatory and must
  not be treated as a formal larger-`N` benchmark.
- Artifact sufficiency check: result must cite aggregate and row artifacts and
  preserve the next subplan.

Audit result: passes as a local consolidation phase because it runs no new
scientific experiment and only decides the next bounded plan from existing
artifacts.

## Forbidden Claims And Actions

- Do not run GPU benchmarks in this phase.
- Do not modify filtering, transport, TensorFlow, TensorFlow Probability, or
  numerical algorithm implementation paths.
- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not rank candidates statistically from descriptive warm timing or two
  N2048 seed batches.
- Do not claim speedup, posterior correctness, HMC readiness, dense Sinkhorn
  equivalence, public API/default readiness, scientific superiority, production
  readiness, or invalidity of deferred rank-32/64/128 candidates.
- Do not reintroduce any excluded or deferred candidate without a separate
  reviewed subplan.

## Exact Next-Phase Handoff Conditions

- If both aggregates validate and resource risk is acceptable only for a small
  diagnostic, draft a reviewed larger-`N` resource-feasibility subplan with
  explicit stop conditions and no performance/scientific claims.
- If both aggregates validate but larger-`N` risk is too high for unattended
  execution, draft a reviewed resource-envelope repair or human-direction
  handoff.
- If artifact validation fails, write a blocker result and stop for repair
  selection.
- If the next decision depends on ranking candidates, stop and require a
  separate statistical evidence plan.

## Stop Conditions

- Either N2048 aggregate is missing, corrupt, stale, or not `PASS`.
- Candidate ids or seed batches do not match the expected values.
- Any row has hard vetoes, failed comparability, failed warm screen, failed
  provenance, missing artifacts, or artifact path collision.
- Any row JSON emits a warm threshold other than `1.25`.
- The result cannot be written without crossing a forbidden claim boundary.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the consolidation result/close or blocker result.
3. Draft or refresh the next subplan.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Subplan Self-Review

- Consistency: uses only the two completed N2048 aggregates and carries forward
  both rank-16 candidates as viable.
- Correctness: validates status, provenance, thresholds, row artifacts, and
  exact candidate/seed identity before deciding a next phase.
- Feasibility: local artifact analysis only; no GPU runtime.
- Artifact coverage: specifies inputs, close record, and next subplan.
- Boundary safety: avoids ranking, speedup, posterior-correctness,
  default-readiness, HMC-readiness, and scientific-validity claims.
