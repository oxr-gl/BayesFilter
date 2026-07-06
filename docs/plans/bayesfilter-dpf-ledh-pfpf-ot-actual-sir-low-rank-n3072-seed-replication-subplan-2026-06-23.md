# Actual-SIR Low-Rank N3072 Seed-Replication Subplan

Date: 2026-06-23

Status: `DRAFT_READY_FOR_LOCAL_CHECKS_AND_READ_ONLY_REVIEW`

## Phase Objective

Run one fresh `N=3072` paired GPU/XLA actual-SIR seed-replication screen for
the two rank-16 carry-forward candidates:

- `r16_eps0p25_alpha1em08_it120`
- `r16_eps0p125_alpha1em08_it120`

The fresh seed batch is `81139,81140`. The shape is batch `2`, time steps `20`,
particles `3072`. This phase asks whether both rank-16 candidates remain viable
under one additional N3072 seed batch with valid artifacts, no hard vetoes, and
complete GPU/XLA/TF32 provenance.

This phase is not a ranking, speedup, default-readiness, HMC-readiness,
posterior-correctness, dense-equivalence, N4096-feasibility, formal
memory-scaling, or scientific-validity gate.

## Entry Conditions Inherited From Previous Phase

- N2048 minimal-rank validation passed for both rank-16 candidates.
- N2048 seed replication passed for both rank-16 candidates.
- N3072 representative resource smoke passed for
  `r16_eps0p25_alpha1em08_it120` on seeds `81137,81138`.
- N3072 second-candidate validation passed for
  `r16_eps0p125_alpha1em08_it120` on seeds `81137,81138`.
- N3072 two-row consolidation/resource-boundary closeout passed and explicitly
  stopped automatic runtime escalation:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-two-row-consolidation-resource-boundary-result-2026-06-23.md`
- The user authorized the next recommended phase with the transcript message
  `do as you suggested`.
- Both previous N3072 row JSON basenames reached exactly `255` bytes, so this
  phase must use a shortened benchmark prefix and must pass a fresh dry-run
  filename-length check before GPU execution.
- Rank-32/64/128 candidates remain viable but deferred for resource-envelope
  reasons; they are not rejected by this phase.

## Required Artifacts

- This subplan.
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-seed-replication-review-ledger-2026-06-23.md`
- N3072 seed-replication aggregate JSON:
  `docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.json`
- N3072 seed-replication aggregate Markdown:
  `docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.md`
- Row JSON/Markdown/log artifacts produced by the grid runner under
  `docs/benchmarks` and `docs/benchmarks/logs`.
- N3072 seed-replication result or blocker:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-seed-replication-result-2026-06-23.md`

The result must include a decision table, inference-status table, run manifest,
artifact manifest, post-run red-team note, exact next handoff, and explicit
nonclaims.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before execution.
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
- Exact two-candidate dry-run before GPU execution.
- Dry-run artifact-path check verifying:
  - exactly two rows;
  - exact candidate ids `r16_eps0p25_alpha1em08_it120` and
    `r16_eps0p125_alpha1em08_it120`;
  - exact assignment epsilons `0.25` and `0.125`;
  - exact seeds `81139,81140`;
  - exact shape batch `2`, time steps `20`, particles `3072`;
  - row JSON/Markdown/log paths are present and distinct;
  - every filename component is no longer than `255` bytes.
- Claude Opus/max read-only review of this subplan and review ledger until
  `VERDICT: AGREE` or max five rounds for the same blocker. Claude is not an
  execution authority and cannot authorize crossing human, runtime, model-file,
  funding, product-capability, default-policy, public API, or scientific-claim
  boundaries.
- Trusted GPU precheck before GPU execution.
- Execute only through
  `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py` with
  `streaming_timing_source=compiled_core`, `low_rank_timing_source=compiled_core`,
  `jit_compile=True`, GPU-visible scope, TF32 enabled, and expected GPU outputs.
- Verify aggregate JSON consistency after the run:
  - aggregate status;
  - candidate count `2`;
  - exact candidate ids;
  - exact seed batch and shape;
  - row statuses;
  - row hard vetoes;
  - provenance flags;
  - labels, with timing labels interpreted as descriptive/resource-triage
    evidence only;
  - row JSON/Markdown/log paths exist and are distinct;
  - filename components are no longer than `255` bytes.

## Evidence Contract

- Question: do the two rank-16 carry-forward candidates remain viable under one
  additional N3072 paired actual-SIR seed batch with valid artifacts, no hard
  vetoes, paired comparability, and complete GPU/XLA/TF32 provenance?
- Baseline/comparator: paired streaming actual-SIR route from the same harness,
  seed batch, shape, dtype, TF32 mode, GPU visibility, and compiled-core timing
  contract for each row.
- Candidate set:
  - `r16_eps0p25_alpha1em08_it120`;
  - `r16_eps0p125_alpha1em08_it120`.
- Seeds: `81139,81140`.
- Shape: batch `2`, time steps `20`, particles `3072`.
- Primary screen: seed-replication passes only if both rows complete, have no
  hard vetoes, have complete GPU/XLA compiled-core provenance, pass paired
  comparability thresholds, and preserve row JSON/Markdown/log artifacts.
- Warm-time labels and ratios are not phase-defining promotion/pass criteria
  here. They are descriptive/resource-triage evidence only.
- Promotion vetoes: any row hard veto, missing compiled/XLA provenance, missing
  GPU outputs, stale row mismatch, missing/corrupt artifacts, nonfinite outputs,
  ESS hard veto, log-weight normalization failure, factor residual threshold
  failure, paired comparability failure, missing row JSON/Markdown/log artifact
  paths, filename component over `255` bytes, row timeout, or incomplete
  aggregate run.
- Continuation vetoes: trusted GPU unavailable, any row timeout, aggregate
  corrupt/missing, source candidate mismatch, path-length failure, or any result
  interpretation that requires crossing a forbidden claim boundary.
- Timeout classification: any row timeout must be classified in the result as
  `low-rank-arm`, `streaming-arm`, or `shared-harness/resource`. Only a
  `low-rank-arm` timeout may be treated as candidate resource failure;
  `streaming-arm` and `shared-harness/resource` timeouts are blocker or
  route-repair outcomes.
- Explanatory diagnostics only: warm medians, warm ratios, row wall times,
  first-call times, log-likelihood deltas, factor residual magnitudes below
  threshold, ESS values, and GPU memory snapshots.
- What will not be concluded: statistical ranking, speedup, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API/default
  readiness, N4096 feasibility, formal memory scaling, broad scalable-OT
  superiority, production scientific validity, invalidity of either rank-16
  candidate, or invalidity of deferred rank-32/64/128 candidates.
- Artifact preserving result: the N3072 seed-replication grid JSON/Markdown,
  row artifacts/logs, review ledger, and result or blocker record.

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Whether both rank-16 candidates survive one fresh N3072 seed-replication screen |
| Candidate or mechanism under test | `r16_eps0p25_alpha1em08_it120` and `r16_eps0p125_alpha1em08_it120` under GPU/XLA compiled-core TensorFlow/TFP execution |
| Expected failure mode | Resource pressure, row timeout, memory failure, comparability failure, numerical hard veto, missing provenance/artifact, or path-length failure |
| Promotion criterion | Both rows complete with no hard vetoes, pass comparability thresholds, have GPU/XLA/TF32 compiled-core provenance, and preserve row artifacts |
| Promotion veto | Any hard veto, missing provenance, failed comparability, timeout, stale mismatch, overlong filename, or missing artifact |
| Continuation veto | Trusted GPU unavailable, row timeout, incomplete/corrupt aggregate, path-length failure, or result requiring a forbidden claim |
| Repair trigger | Harness/provenance/artifact failure, path-length failure, resource timeout, memory failure, or systematic hard veto pattern |
| Explanatory diagnostics | Warm ratios, row wall times, first-call times, residual magnitudes, log-likelihood deltas, GPU memory snapshots |
| Must not conclude | Ranking, speedup, correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, N4096 feasibility, scientific validity, or invalidity of viable/deferred candidates |

## Skeptical Plan Audit

- Wrong baseline check: each candidate is compared only against its paired
  streaming route from the same fresh seed-replication run.
- Proxy metric check: warm timing remains resource-triage evidence, not proof
  of speedup, superiority, or production readiness.
- Stop condition check: provenance failures, hard vetoes, invalid artifacts,
  comparability failures, overlong filenames, missing row artifact paths, row
  timeout, and incomplete aggregate run block advancement.
- Fairness check: this phase tests both rank-16 candidates on the same fresh
  seed batch; it must not rank the two candidates or reject deferred
  rank-32/64/128 candidates.
- Hidden assumption check: two seed batches at N3072, even if all rows pass,
  still do not imply N4096 feasibility, statistical ranking, posterior
  correctness, HMC readiness, default readiness, or scientific validity.
- Environment mismatch check: GPU checks must be trusted; memory snapshots are
  explanatory and not formal memory-scaling evidence.
- Artifact sufficiency check: aggregate JSON must preserve exact candidate ids,
  row labels, provenance flags, row artifacts, and summary counts.

Audit result: passes as a bounded N3072 seed-replication plan because it uses a
fresh seed batch, shortened artifact prefix, explicit path-length gate,
review-before-runtime, and preserved claim boundaries.

## Candidate Dry-Run Command

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode dry-run \
  --route both \
  --batch-seeds 81139,81140 \
  --time-steps 20 \
  --num-particles 3072 \
  --low-rank-ranks 16 \
  --low-rank-assignment-epsilons 0.25,0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120 \
  --phase-id-prefix ASLR-N3072-SR \
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
  --output /tmp/actual-sir-lr-n3072-seedrep-20260623-dry-run.json \
  --markdown-output /tmp/actual-sir-lr-n3072-seedrep-20260623-dry-run.md \
  --quiet
```

## Candidate Execution Command

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --route both \
  --batch-seeds 81139,81140 \
  --time-steps 20 \
  --num-particles 3072 \
  --low-rank-ranks 16 \
  --low-rank-assignment-epsilons 0.25,0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120 \
  --phase-id-prefix ASLR-N3072-SR \
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
  --output docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.json \
  --markdown-output docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.md \
  --quiet
```

## Forbidden Claims And Actions

- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not use old contaminated P03 rows as current performance evidence.
- Do not rank candidates statistically from this run or from descriptive
  timing.
- Do not claim speedup, posterior correctness, HMC readiness, dense Sinkhorn
  equivalence, public API/default readiness, scientific superiority,
  production readiness, N4096 feasibility, formal memory scaling, or invalidity
  of either rank-16 candidate or deferred rank-32/64/128 candidates.
- Do not continue from hard vetoes or failed comparability as if timing
  evidence were valid.
- Do not run N4096, larger shapes, API/default work, HMC work, or route repairs
  from this subplan.

## Exact Next-Phase Handoff Conditions

- If both seed-replication rows pass, write the result and stop for a local
  N3072 replicated-evidence/resource-boundary closeout before any further
  runtime.
- If one row fails due to resource timeout or memory, write a result separating
  candidate/resource failure from scientific rejection and stop for repair or
  human direction.
- If any row fails due to comparability or numerical hard veto, write a
  negative seed-replication result and stop for repair selection or human
  direction.
- If execution fails due to harness/runner artifact issues or path-length
  problems, write a blocker result and create a focused harness/path repair
  subplan before rerunning.
- If trusted GPU availability prevents a complete result, write a blocker
  result preserving partial artifacts and stop for scheduling or budget
  direction.

## Stop Conditions

- Trusted GPU precheck cannot see a usable GPU for the requested device.
- The exact two candidates cannot be executed by `--candidate-ids`.
- The dry-run row artifact filename component exceeds `255` bytes.
- Any row lacks `compiled_core`, `jit_compile=True`, or expected GPU output
  provenance.
- Any row has a stale row mismatch with the requested seed batch, shape,
  candidate id, dtype, timing source, TF32 mode, or device policy.
- Any row emits a hard veto, nonfinite output, ESS hard veto, log-weight
  normalization failure, factor residual threshold failure, paired
  comparability failure, or invalid artifact.
- Any row is missing its JSON, Markdown, or log artifact path in the aggregate
  result.
- Any row times out or the aggregate run is incomplete; write a blocker/result
  preserving partial artifacts and timeout classification rather than
  interpreting the incomplete run as a pass.
- The result cannot be interpreted without crossing a forbidden claim boundary.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the N3072 seed-replication result or blocker result.
3. Draft or refresh the next subplan, which should be local replicated-evidence
   consolidation/resource-boundary analysis if both rows pass.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Subplan Self-Review

- Consistency: follows the N3072 two-row closeout and uses explicit user
  approval for the next bounded runtime.
- Correctness: preserves timing/provenance, exact candidate filtering, bounded
  row artifact path integrity, and comparability gates before timing
  discussion.
- Feasibility: two rows at a previously completed shape; no N4096 or broader
  ladder.
- Artifact coverage: specifies aggregate, row, log, result, review ledger, and
  next handoff artifacts.
- Boundary safety: preserves no-NumPy implementation policy and avoids ranking,
  default-readiness, speedup, posterior-correctness, HMC-readiness,
  dense-equivalence, N4096-feasibility, formal memory-scaling,
  other-candidate invalidity, deferred-candidate invalidity, and
  scientific-validity claims.
