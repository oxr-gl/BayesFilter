# Actual-SIR Low-Rank N3072 Representative Resource-Smoke Subplan

Date: 2026-06-23

Status: `DRAFT_READY_FOR_READ_ONLY_REVIEW_BEFORE_EXECUTION`

## Phase Objective

Run one larger-`N` paired GPU/XLA actual-SIR resource smoke at `N=3072` for a
single representative rank-16 candidate, only to test whether the harness can
complete the larger row with valid artifacts and provenance.

This phase is not a candidate ranking, not a speedup claim, not a larger-`N`
validation ladder, and not a promotion/default-readiness gate.

## Entry Conditions Inherited From Previous Phase

- The N2048 validation aggregate passed.
- The N2048 seed-replication aggregate passed.
- The N2048 consolidation/resource-decision phase validated both aggregates.
- Both rank-16 candidates remain viable and unranked:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
- The representative resource-smoke arm is
  `r16_eps0p25_alpha1em08_it120` because it is the first candidate in the
  established carry-forward order. This is not a statistical ranking or winner
  selection.
- `r16_eps0p125_alpha1em08_it120` remains viable and is not rejected or
  demoted by this single-row resource smoke.

## Required Artifacts

- This subplan.
- N3072 representative resource-smoke aggregate JSON:
  `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.json`
- N3072 representative resource-smoke aggregate Markdown:
  `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.md`
- Row JSON/Markdown/log artifacts produced by the grid runner under
  `docs/benchmarks` and `docs/benchmarks/logs`.
- A phase result/close or blocker record under `docs/plans`.
- A next subplan before any further execution.

The phase result must include a decision table, inference-status table,
post-run red-team note, and run manifest with git commit, command, environment,
GPU/CPU status, seeds, wall time, artifact paths, plan path, and result path.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before execution.
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
- Exact candidate dry-run for the single representative id before GPU
  execution.
- Dry-run artifact-path check verifying one row, exact candidate id, row
  JSON/Markdown/log paths, and filename components no longer than `255`
  characters.
- Trusted GPU precheck before GPU execution.
- Execute only through
  `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py` with
  `streaming_timing_source=compiled_core`, `low_rank_timing_source=compiled_core`,
  `jit_compile=True`, GPU-visible scope, TF32 enabled, and expected GPU outputs.
- Verify aggregate JSON consistency after the run:
  candidate count `1`, exact candidate id, row status, row hard vetoes,
  provenance flags, label, warm threshold `1.25`, and row JSON/Markdown/log
  paths.
- Claude may be used as a read-only reviewer for this material subplan. Claude
  is not an execution authority and cannot authorize crossing human, runtime,
  model-file, funding, product-capability, default-policy, or scientific-claim
  boundaries.

## Evidence Contract

- Question: can one representative rank-16 low-rank actual-SIR row complete at
  `N=3072` under the compiled GPU/XLA paired harness with valid artifacts and
  provenance?
- Baseline/comparator: paired streaming actual-SIR route from the same harness,
  seed batch, shape, dtype, TF32 mode, GPU visibility, and compiled-core timing
  contract.
- Candidate set: exactly `r16_eps0p25_alpha1em08_it120`.
- Proposed seeds: `81137,81138`.
- Proposed shape: batch `2`, time steps `20`, particles `3072`.
- Primary screen: resource-smoke pass only if the row completes, has no hard
  vetoes, has complete GPU/XLA compiled-core provenance, passes paired
  comparability and warm screen, and preserves row JSON/Markdown/log artifacts.
- Warm-time screen pass is exactly the aggregate runner condition
  `_speed_screen_pass`, with threshold pinned as
  `warm_median_streaming_over_low_rank >= 1.25`.
- Promotion vetoes: any row hard veto, missing compiled/XLA provenance, missing
  GPU outputs, stale row mismatch, missing/corrupt artifacts, nonfinite outputs,
  ESS hard veto, log-weight normalization failure, factor residual threshold
  failure, paired comparability failure, warm-time screen failure, missing row
  JSON/Markdown/log artifact paths, row timeout, or incomplete aggregate run.
- Continuation vetoes: trusted GPU unavailable, row timeout, aggregate
  corrupt/missing, source candidate mismatch, or any result interpretation that
  requires crossing a forbidden claim boundary.
- Timeout classification: any row timeout must be classified in the close
  record as `low-rank-arm`, `streaming-arm`, or `shared-harness/resource`. Only
  a `low-rank-arm` timeout may be treated as representative-arm resource
  failure; `streaming-arm` and `shared-harness/resource` timeouts are blocker or
  route-repair outcomes.
- Explanatory diagnostics only: warm medians, warm ratio, row wall time,
  log-likelihood deltas, factor residual magnitudes below threshold, and GPU
  memory snapshots.
- What will not be concluded: statistical ranking, speedup, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API/default
  readiness, broad scalable-OT superiority, production scientific validity,
  invalidity of `r16_eps0p125_alpha1em08_it120`, or invalidity of deferred
  rank-32/64/128 candidates.
- Artifact preserving result: the N3072 resource-smoke grid JSON/Markdown, row
  artifacts/logs, and close or blocker record.

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Whether one representative rank-16 row can complete at N3072 under the GPU/XLA paired harness |
| Candidate or mechanism under test | Repaired low-rank actual-SIR route under GPU/XLA compiled-core TensorFlow/TFP execution |
| Expected failure mode | Resource pressure, row timeout, memory failure, comparability failure, warm-screen failure, numerical hard veto, or missing provenance/artifact |
| Promotion criterion | One representative row completes with no hard vetoes, passes comparability and warm screen, has GPU/XLA/TF32 compiled-core provenance, and preserves row artifacts |
| Promotion veto | Any hard veto, missing provenance, failed comparability, failed warm screen, timeout, stale mismatch, or missing artifact |
| Continuation veto | Trusted GPU unavailable, row timeout, incomplete/corrupt aggregate, or result requiring a forbidden claim |
| Repair trigger | Harness/provenance/artifact failure, resource timeout, memory failure, or systematic hard veto pattern |
| Explanatory diagnostics | Warm ratio, row wall time, residual magnitudes, log-likelihood deltas, GPU memory snapshots |
| Must not conclude | Ranking, speedup, correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, or invalidity of other viable candidates |

## Skeptical Plan Audit

- Wrong baseline check: compare only against the paired streaming row from the
  same N3072 run.
- Proxy metric check: warm timing remains a viability/resource-smoke screen,
  not proof of speedup, superiority, or production readiness.
- Stop condition check: provenance failures, hard vetoes, invalid artifacts,
  comparability failures, warm-screen failure, missing row artifact paths, row
  timeout, and incomplete aggregate run block any advancement.
- Fairness check: the smoke uses one candidate only to reduce resource risk; it
  must not be used to rank or reject the other viable rank-16 candidate.
- Hidden assumption check: one N3072 row does not imply N3072 two-candidate
  validation, N4096 feasibility, posterior correctness, or default-readiness.
- Environment mismatch check: GPU checks must be trusted; sandbox GPU failures
  do not establish machine/framework failure until rerun in trusted context.
- Artifact sufficiency check: aggregate JSON must preserve exact candidate id,
  row label, provenance flags, row artifacts, and summary counts.

Audit result: passes as a bounded resource smoke because it runs one larger row
only after two N2048 seed batches passed, and it preserves all claim
boundaries.

## Candidate Dry-Run Command

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode dry-run \
  --route both \
  --batch-seeds 81137,81138 \
  --time-steps 20 \
  --num-particles 3072 \
  --low-rank-ranks 16 \
  --low-rank-assignment-epsilons 0.25,0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --candidate-ids r16_eps0p25_alpha1em08_it120 \
  --warmups 1 \
  --repeats 2 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --jit-compile \
  --row-timeout-seconds 7200 \
  --output /tmp/actual-sir-low-rank-n3072-representative-resource-smoke-dry-run.json \
  --markdown-output /tmp/actual-sir-low-rank-n3072-representative-resource-smoke-dry-run.md \
  --quiet
```

## Candidate Execution Command

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --route both \
  --batch-seeds 81137,81138 \
  --time-steps 20 \
  --num-particles 3072 \
  --low-rank-ranks 16 \
  --low-rank-assignment-epsilons 0.25,0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --candidate-ids r16_eps0p25_alpha1em08_it120 \
  --warmups 1 \
  --repeats 2 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --jit-compile \
  --row-timeout-seconds 7200 \
  --output docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.md
```

## Forbidden Claims And Actions

- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not use old contaminated P03 rows as current performance evidence.
- Do not rank candidates statistically from this single representative row.
- Do not claim speedup, posterior correctness, HMC readiness, dense Sinkhorn
  equivalence, public API/default readiness, scientific superiority, production
  readiness, or invalidity of the other viable rank-16 candidate or deferred
  rank-32/64/128 candidates.
- Do not continue from hard vetoes or failed comparability as if timing
  evidence were valid.
- Do not reintroduce any excluded or deferred candidate without a separate
  reviewed subplan.

## Exact Next-Phase Handoff Conditions

- If the representative row passes, write the resource-smoke result and draft a
  reviewed next subplan for either N3072 two-candidate validation, a second
  representative-arm seed smoke, or a resource-envelope stop/handoff.
- If the row fails due to resource timeout or memory, write a blocker/result
  separating resource failure from scientific rejection and draft a smaller
  repair or handoff subplan.
- If the row fails due to comparability or numerical hard veto, write a
  negative representative-row result and stop for repair selection or human
  direction.
- If execution fails due to harness/runner artifact issues, write a blocker
  result and create a focused harness repair subplan before rerunning.
- If trusted GPU availability prevents a complete result, write a blocker
  result preserving partial artifacts and stop for scheduling or budget
  direction.

## Stop Conditions

- Trusted GPU precheck cannot see a usable GPU for the requested device.
- The exact representative candidate cannot be executed by `--candidate-ids`.
- The dry-run row artifact filename component exceeds `255` characters.
- Any row lacks `compiled_core`, `jit_compile=True`, or expected GPU output
  provenance.
- Any row has a stale row mismatch with the requested seed batch, shape,
  candidate id, dtype, timing source, TF32 mode, or device policy.
- Any row emits a hard veto, nonfinite output, ESS hard veto, log-weight
  normalization failure, factor residual threshold failure, paired
  comparability failure, warm-screen failure, or invalid artifact.
- Any row is missing its JSON, Markdown, or log artifact path in the aggregate
  result.
- Any row times out or the aggregate run is incomplete; write a blocker/result
  preserving partial artifacts and timeout classification rather than
  interpreting the incomplete run as a pass.
- The result cannot be interpreted without crossing a forbidden claim boundary.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the N3072 resource-smoke phase result or blocker result.
3. Draft or refresh the next subplan.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Subplan Self-Review

- Consistency: follows the N2048 consolidation result and uses a single
  representative row only as a resource smoke.
- Correctness: preserves timing/provenance, exact candidate filtering, bounded
  row artifact path integrity, and comparability gates before timing discussion.
- Feasibility: stages `N=3072` before any N4096 or two-candidate larger-`N`
  run.
- Artifact coverage: specifies aggregate, row, log, close-record, and
  next-subplan artifacts.
- Boundary safety: preserves no-NumPy implementation policy and avoids ranking,
  default-readiness, speedup, posterior-correctness, HMC-readiness,
  other-candidate invalidity, deferred-candidate invalidity, and
  scientific-validity claims.
