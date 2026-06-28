# Actual-SIR Low-Rank N2048 Seed-Replication Subplan

Date: 2026-06-23

Status: `DRAFT_READY_FOR_READ_ONLY_REVIEW_BEFORE_EXECUTION`

## Phase Objective

Run an independent N2048 GPU/XLA actual-SIR seed-replication screen for the two
rank-16 candidates that passed the N2048 minimal-rank validation phase.

## Entry Conditions Inherited From Previous Phase

- N2048 minimal-rank validation passed for exactly:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
- The N2048 validation aggregate is:
  `docs/benchmarks/actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23.json`
- The row artifact naming repair converged and passed focused checks.
- Rank-32/64/128 candidates remain viable but deferred; this phase must not
  claim they are inferior, invalid, or scientifically rejected.
- `r64_eps0p125_alpha1em08_it120` remains excluded from this lane because it
  failed heldout paired comparability and must not be revived without a separate
  repair/tuning subplan.

## Required Artifacts

- This subplan.
- N2048 seed-replication aggregate JSON:
  `docs/benchmarks/actual-sir-low-rank-n2048-seed-replication-2026-06-23.json`
- N2048 seed-replication aggregate Markdown:
  `docs/benchmarks/actual-sir-low-rank-n2048-seed-replication-2026-06-23.md`
- Row JSON/Markdown/log artifacts produced by the grid runner under
  `docs/benchmarks` and `docs/benchmarks/logs`.
- A phase result/close or blocker record under `docs/plans`.
- A next subplan before any further execution.

The phase result/close record must include a decision table,
inference-status table, post-run red-team note, and run manifest with git
commit, command, environment, GPU/CPU status, seeds, wall time, artifact paths,
plan path, and result path.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before execution.
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
- Exact candidate dry-run for the two rank-16 survivor ids before GPU
  execution.
- Dry-run artifact-path check verifying row JSON/Markdown/log paths are
  distinct and every filename component is no longer than `255` characters.
- Trusted GPU precheck before GPU execution.
- Execute only through
  `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py` with
  `streaming_timing_source=compiled_core`, `low_rank_timing_source=compiled_core`,
  `jit_compile=True`, GPU-visible scope, TF32 enabled, and expected GPU outputs.
- Verify aggregate JSON consistency after the run:
  candidate count, exact candidate ids, row status, row hard vetoes,
  provenance flags, labels, warm threshold `1.25`, and row JSON/Markdown/log
  paths.
- Claude may be used as a read-only reviewer for this material subplan. Claude
  is not an execution authority and cannot authorize crossing human, runtime,
  model-file, funding, product-capability, default-policy, or scientific-claim
  boundaries.

## Evidence Contract

- Question: do the two rank-16 N2048 survivor candidates remain viable under an
  independent seed batch at the same `N=2048` shape?
- Baseline/comparator: paired streaming actual-SIR route rows from the same
  harness, seed batch, shape, dtype, TF32 mode, GPU visibility, and
  compiled-core timing contract.
- Candidate set:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
- Proposed seeds: `81135,81136`.
- Proposed shape: batch `2`, time steps `20`, particles `2048`.
- Primary screen: a candidate remains viable only if it has no hard vetoes,
  complete GPU/XLA compiled-core provenance, paired comparability pass,
  warm-time screen pass, and preserved row JSON/Markdown/log artifact paths.
- Warm-time screen pass is exactly the aggregate runner condition
  `_speed_screen_pass`: the row artifact's
  `paired_comparability.warm_median_streaming_over_low_rank` must be greater
  than or equal to
  `paired_comparability.thresholds.warm_median_streaming_over_low_rank`;
  for this phase the threshold is pinned as
  `warm_median_streaming_over_low_rank >= 1.25`.
- Promotion vetoes: any row hard veto, missing compiled/XLA provenance, missing
  GPU outputs, stale row mismatch, missing/corrupt artifacts, nonfinite outputs,
  ESS hard veto, log-weight normalization failure, factor residual threshold
  failure, paired comparability failure, warm-time screen failure, missing
  per-row JSON/Markdown/log artifact paths, artifact path collision, row
  timeout, or incomplete aggregate run.
- Continuation vetoes: trusted GPU unavailable, both rows timeout, aggregate
  corrupt/missing, source candidate mismatch, or any result interpretation that
  requires crossing a forbidden claim boundary.
- Repair trigger: row timeout, memory/resource failure, harness/provenance
  artifact failure, artifact path collision, or systematic hard veto pattern
  that could indicate route implementation rather than candidate-specific
  failure.
- Timeout classification: every row timeout must be classified in the row
  record or close record as `low-rank-arm`, `streaming-arm`, or
  `shared-harness/resource`. Only a `low-rank-arm` timeout may be treated as
  candidate rejection; `streaming-arm` and `shared-harness/resource` timeouts
  are blocker or route-repair outcomes.
- Explanatory diagnostics only: exact warm medians, warm ratios, row wall time,
  per-seed log-likelihood deltas, factor residual magnitudes below threshold,
  and GPU memory snapshots.
- What will not be concluded: statistical ranking, speedup, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API/default
  readiness, broad scalable-OT superiority, production scientific validity, or
  invalidity of deferred rank-32/64/128 candidates.
- Artifact preserving result: the N2048 seed-replication grid JSON/Markdown,
  row artifacts/logs, and close or blocker record.

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Whether the two rank-16 N2048 survivors remain viable under fresh seeds |
| Candidate or mechanism under test | Repaired low-rank actual-SIR route under GPU/XLA compiled-core TensorFlow/TFP execution |
| Expected failure mode | Seed-specific comparability failure, warm-screen failure, resource pressure, row timeout, numerical hard veto, or missing provenance/artifact |
| Promotion criterion | Exact candidate row has no hard vetoes, passes paired comparability and warm screen, has GPU/XLA/TF32 compiled-core provenance, and preserves distinct row artifacts |
| Promotion veto | Any hard veto, missing provenance, failed comparability, failed warm screen, artifact path collision, timeout, stale mismatch, or missing artifact |
| Continuation veto | Trusted GPU unavailable, both rows timeout, incomplete/corrupt aggregate, or result requiring a forbidden claim |
| Repair trigger | Harness/provenance/artifact failure, resource timeout, memory failure, or systematic hard veto pattern |
| Explanatory diagnostics | Warm ratios, row wall time, residual magnitudes below threshold, per-row deltas, GPU memory snapshots |
| Must not conclude | Ranking, speedup, correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, or invalidity of deferred viable candidates |

## Skeptical Plan Audit

- Wrong baseline check: compare only against paired streaming rows from the
  same independent N2048 seed-replication run.
- Proxy metric check: warm timing remains a viability screen, not proof of
  speedup, superiority, or production readiness.
- Stop condition check: provenance failures, hard vetoes, invalid artifacts,
  comparability failures, warm-screen failures, missing row artifact paths,
  artifact path collisions, stale-row mismatches, row timeouts, and incomplete
  aggregate runs block candidate advancement.
- Fairness check: both candidates share seeds, shape, dtype, TF32 mode, GPU
  visibility, timing source, transport policy, rank, alpha, and projection
  iteration count; only assignment epsilon varies.
- Hidden assumption check: this is seed replication at one particle count, not
  a broad scaling law, statistical ranking, posterior-correctness, or
  default-readiness claim.
- Environment mismatch check: GPU checks must be trusted; sandbox GPU failures
  do not establish machine/framework failure until rerun in trusted context.
- Artifact sufficiency check: aggregate JSON must preserve exact candidate ids,
  row labels, provenance flags, row artifacts, and summary counts.

Audit result: passes as the next discriminating replication screen because it
holds `N=2048` fixed and changes only the seed batch.

## Candidate Dry-Run Command

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode dry-run \
  --route both \
  --batch-seeds 81135,81136 \
  --time-steps 20 \
  --num-particles 2048 \
  --low-rank-ranks 16 \
  --low-rank-assignment-epsilons 0.25,0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120 \
  --warmups 1 \
  --repeats 2 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --jit-compile \
  --row-timeout-seconds 5400 \
  --output /tmp/actual-sir-low-rank-n2048-seed-replication-exact-candidate-dry-run.json \
  --markdown-output /tmp/actual-sir-low-rank-n2048-seed-replication-exact-candidate-dry-run.md \
  --quiet
```

## Candidate Execution Command

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --route both \
  --batch-seeds 81135,81136 \
  --time-steps 20 \
  --num-particles 2048 \
  --low-rank-ranks 16 \
  --low-rank-assignment-epsilons 0.25,0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120 \
  --warmups 1 \
  --repeats 2 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --jit-compile \
  --row-timeout-seconds 5400 \
  --output docs/benchmarks/actual-sir-low-rank-n2048-seed-replication-2026-06-23.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-n2048-seed-replication-2026-06-23.md
```

## Forbidden Claims And Actions

- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not use old contaminated P03 rows as current performance evidence.
- Do not rank candidates statistically from descriptive warm timing alone.
- Do not claim speedup, posterior correctness, HMC readiness, dense Sinkhorn
  equivalence, public API/default readiness, scientific superiority, production
  readiness, or invalidity of deferred rank-32/64/128 candidates.
- Do not continue from hard vetoes or failed comparability as if timing
  evidence were valid.
- Do not reintroduce any excluded or deferred candidate without a separate
  reviewed subplan.

## Exact Next-Phase Handoff Conditions

- If both rank-16 candidates remain viable, write the seed-replication result
  and draft a reviewed next subplan for a staged larger-`N` validation or final
  N2048 evidence consolidation decision.
- If one row fails but the other passes, do not rank by timing; separate
  candidate viability from route validity and draft a reviewed next subplan.
- If no candidate remains viable due to comparability, warm-screen, timeout, or
  hard-veto failures, write a negative result separating candidate rejection,
  tuning/resource failure, and route-repair rejection, then stop for repair
  selection or human direction.
- If execution fails due to harness/runner artifact issues, write a blocker
  result and create a focused harness repair subplan before rerunning.
- If trusted GPU availability prevents a complete result, write a blocker
  result preserving partial artifacts and stop for scheduling or budget
  direction.

## Stop Conditions

- Trusted GPU precheck cannot see a usable GPU for the requested device.
- The exact survivor candidate set cannot be executed by `--candidate-ids`.
- Any row lacks `compiled_core`, `jit_compile=True`, or expected GPU output
  provenance.
- Any row has a stale row mismatch with the requested seed batch, shape,
  candidate id, dtype, timing source, TF32 mode, or device policy.
- Any row emits a hard veto, nonfinite output, ESS hard veto, log-weight
  normalization failure, factor residual threshold failure, paired
  comparability failure, warm-screen failure, or invalid artifact.
- Any row is missing its JSON, Markdown, or log artifact path in the aggregate
  result, or two rows share a JSON, Markdown, or log path.
- Any row times out or the aggregate run is incomplete; write a blocker/result
  preserving partial artifacts and the timeout classification rather than
  interpreting the incomplete run as a pass.
- The result cannot be interpreted without crossing a forbidden claim boundary.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the N2048 seed-replication phase result or blocker result.
3. Draft or refresh the next subplan.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Subplan Self-Review

- Consistency: follows the N2048 validation result and carries forward only the
  two rank-16 candidates.
- Correctness: preserves timing/provenance, exact candidate filtering, bounded
  row artifact path integrity, and comparability gates before timing discussion.
- Feasibility: repeats the same `N=2048` shape with fresh seeds and two rows.
- Artifact coverage: specifies aggregate, row, log, close-record, and
  next-subplan artifacts.
- Boundary safety: preserves no-NumPy implementation policy and avoids ranking,
  default-readiness, speedup, posterior-correctness, deferred-candidate
  invalidity, and scientific-validity claims.
