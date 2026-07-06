# Actual-SIR Low-Rank N3072 Second-Candidate Validation Subplan

Date: 2026-06-23

Status: `DRAFT_READY_FOR_READ_ONLY_REVIEW_BEFORE_EXECUTION`

## Phase Objective

Run one bounded paired GPU/XLA actual-SIR row at `N=3072` for the second
rank-16 carry-forward candidate, `r16_eps0p125_alpha1em08_it120`, using the
same seed batch and shape as the completed N3072 representative resource smoke.

This phase asks only whether the second rank-16 candidate can complete this
specific N3072 paired row with valid artifacts and provenance. It is not a
ranking, speedup, default-readiness, HMC-readiness, posterior-correctness,
dense-equivalence, or scientific-validity gate.

## Entry Conditions Inherited From Previous Phase

- N2048 minimal-rank validation passed for:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
- N2048 seed replication passed for the same two rank-16 candidates.
- N3072 representative resource smoke passed for
  `r16_eps0p25_alpha1em08_it120` on seeds `81137,81138`.
- N3072 resource-boundary closeout documented that future runtime requires a
  fresh subplan, read-only review, explicit resource stop conditions, and
  human/runtime approval.
- Human approval to continue was provided after the closeout.
- `r16_eps0p125_alpha1em08_it120` remains viable but untested at N3072.
- Rank-32/64/128 candidates remain viable but deferred for resource-envelope
  reasons; they are not rejected.

## Required Artifacts

- This subplan.
- N3072 second-candidate validation aggregate JSON:
  `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.json`
- N3072 second-candidate validation aggregate Markdown:
  `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.md`
- Row JSON/Markdown/log artifacts produced by the grid runner under
  `docs/benchmarks` and `docs/benchmarks/logs`.
- N3072 second-candidate validation result or blocker:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-second-candidate-validation-result-2026-06-23.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-second-candidate-validation-review-ledger-2026-06-23.md`

The result must include a decision table, inference-status table, run manifest,
artifact manifest, post-run red-team note, exact next handoff, and explicit
nonclaims.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before execution.
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
- Exact candidate dry-run before GPU execution.
- Dry-run artifact-path check verifying:
  - exactly one row;
  - exact candidate id `r16_eps0p125_alpha1em08_it120`;
  - exact assignment epsilon `0.125`;
  - exact seeds `81137,81138`;
  - exact shape batch `2`, time steps `20`, particles `3072`;
  - row JSON/Markdown/log paths are present;
  - filename components are no longer than `255` bytes.
- Trusted GPU precheck before GPU execution.
- Execute only through
  `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py` with
  `streaming_timing_source=compiled_core`, `low_rank_timing_source=compiled_core`,
  `jit_compile=True`, GPU-visible scope, TF32 enabled, and expected GPU outputs.
- Verify aggregate JSON consistency after the run:
  - aggregate status;
  - candidate count `1`;
  - exact candidate id;
  - exact seed batch and shape;
  - row status;
  - row hard vetoes;
  - provenance flags;
  - label, with timing label interpreted as descriptive/resource-triage
    evidence only;
  - warm threshold `1.25` if present;
  - row JSON/Markdown/log paths exist;
  - filename components are no longer than `255` bytes.
- Claude read-only review of this subplan until `VERDICT: AGREE` or max five
  rounds for the same blocker. Claude is not an execution authority and cannot
  authorize crossing human, runtime, model-file, funding, product-capability,
  default-policy, public API, or scientific-claim boundaries.

## Evidence Contract

- Question: can `r16_eps0p125_alpha1em08_it120` complete the paired N3072
  actual-SIR row with valid artifacts, no hard vetoes, paired comparability,
  and complete GPU/XLA/TF32 provenance?
- Baseline/comparator: paired streaming actual-SIR route from the same harness,
  seed batch, shape, dtype, TF32 mode, GPU visibility, and compiled-core timing
  contract.
- Candidate set: exactly `r16_eps0p125_alpha1em08_it120`.
- Seeds: `81137,81138`.
- Shape: batch `2`, time steps `20`, particles `3072`.
- Primary screen: second-candidate validation pass only if the row completes,
  has no hard vetoes, has complete GPU/XLA compiled-core provenance, passes
  paired comparability, and preserves row JSON/Markdown/log artifacts.
- Warm-time screen is not a phase-defining promotion/pass criterion here. The
  aggregate runner will still emit the label produced by `_speed_screen_pass`
  with threshold `warm_median_streaming_over_low_rank >= 1.25`; this phase
  records that timing label as descriptive/resource-triage evidence only.
- Promotion vetoes: any row hard veto, missing compiled/XLA provenance, missing
  GPU outputs, stale row mismatch, missing/corrupt artifacts, nonfinite outputs,
  ESS hard veto, log-weight normalization failure, factor residual threshold
  failure, paired comparability failure, missing row JSON/Markdown/log artifact
  paths, filename component over `255` bytes, row timeout, or incomplete
  aggregate run. Warm-time screen failure is a resource-triage diagnostic in
  this phase, not a promotion veto.
- Continuation vetoes: trusted GPU unavailable, row timeout, aggregate
  corrupt/missing, source candidate mismatch, or any result interpretation that
  requires crossing a forbidden claim boundary.
- Timeout classification: any row timeout must be classified in the result as
  `low-rank-arm`, `streaming-arm`, or `shared-harness/resource`. Only a
  `low-rank-arm` timeout may be treated as second-candidate resource failure;
  `streaming-arm` and `shared-harness/resource` timeouts are blocker or
  route-repair outcomes.
- Explanatory diagnostics only: warm medians, warm ratio, row wall time,
  first-call times, log-likelihood deltas, factor residual magnitudes below
  threshold, ESS values, and GPU memory snapshots.
- What will not be concluded: statistical ranking, speedup, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API/default
  readiness, broad scalable-OT superiority, production scientific validity,
  invalidity of `r16_eps0p25_alpha1em08_it120`, or invalidity of deferred
  rank-32/64/128 candidates.
- Artifact preserving result: the N3072 second-candidate grid JSON/Markdown,
  row artifacts/logs, review ledger, and result or blocker record.

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Whether the second rank-16 candidate can complete the same N3072 paired actual-SIR row |
| Candidate or mechanism under test | `r16_eps0p125_alpha1em08_it120` under GPU/XLA compiled-core TensorFlow/TFP execution |
| Expected failure mode | Resource pressure, row timeout, memory failure, comparability failure, warm-screen descriptive label failure, numerical hard veto, or missing provenance/artifact |
| Promotion criterion | One row completes with no hard vetoes, passes comparability, has GPU/XLA/TF32 compiled-core provenance, and preserves row artifacts |
| Promotion veto | Any hard veto, missing provenance, failed comparability, timeout, stale mismatch, or missing artifact |
| Continuation veto | Trusted GPU unavailable, row timeout, incomplete/corrupt aggregate, or result requiring a forbidden claim |
| Repair trigger | Harness/provenance/artifact failure, resource timeout, memory failure, or systematic hard veto pattern |
| Explanatory diagnostics | Warm ratio, row wall time, first-call times, residual magnitudes, log-likelihood deltas, GPU memory snapshots |
| Must not conclude | Ranking, speedup, correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, scientific validity, or invalidity of other viable candidates |

## Skeptical Plan Audit

- Wrong baseline check: compare only against the paired streaming row from the
  same N3072 run.
- Proxy metric check: warm timing remains resource-triage evidence, not
  proof of speedup, superiority, or production readiness.
- Stop condition check: provenance failures, hard vetoes, invalid artifacts,
  comparability failures, missing row artifact paths, row timeout, and
  incomplete aggregate run block advancement. Warm-screen failure is recorded
  only as descriptive/resource-triage evidence in this phase.
- Fairness check: the phase tests the second rank-16 candidate only because the
  first rank-16 candidate already has one N3072 row; it must not rank the two
  candidates or reject deferred candidates.
- Hidden assumption check: two N3072 one-candidate rows, even if both pass,
  still do not imply N4096 feasibility, statistical ranking, posterior
  correctness, HMC readiness, default readiness, or scientific validity.
- Environment mismatch check: GPU checks must be trusted; memory snapshots are
  explanatory and not formal memory-scaling evidence.
- Artifact sufficiency check: aggregate JSON must preserve exact candidate id,
  row label, provenance flags, row artifacts, and summary counts.

Audit result: passes as a bounded second-candidate validation because it runs
one reviewed row after the prior N3072 resource-smoke closeout and preserves
all claim boundaries.

## Candidate Dry-Run Command

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode dry-run \
  --route both \
  --batch-seeds 81137,81138 \
  --time-steps 20 \
  --num-particles 3072 \
  --low-rank-ranks 16 \
  --low-rank-assignment-epsilons 0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --candidate-ids r16_eps0p125_alpha1em08_it120 \
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
  --output /tmp/actual-sir-low-rank-n3072-second-candidate-validation-dry-run.json \
  --markdown-output /tmp/actual-sir-low-rank-n3072-second-candidate-validation-dry-run.md \
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
  --low-rank-assignment-epsilons 0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --candidate-ids r16_eps0p125_alpha1em08_it120 \
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
  --output docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.md \
  --quiet
```

## Forbidden Claims And Actions

- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not use old contaminated P03 rows as current performance evidence.
- Do not rank candidates statistically from this row or from descriptive
  timing.
- Do not claim speedup, posterior correctness, HMC readiness, dense Sinkhorn
  equivalence, public API/default readiness, scientific superiority,
  production readiness, or invalidity of the other viable rank-16 candidate or
  deferred rank-32/64/128 candidates.
- Do not continue from hard vetoes or failed comparability as if timing
  evidence were valid.
- Do not run N4096, larger shapes, API/default work, HMC work, or route repairs
  from this subplan.

## Exact Next-Phase Handoff Conditions

- If the second candidate passes, write the result and stop for a local
  two-row N3072 evidence consolidation/resource-boundary subplan before any
  further runtime.
- If the row fails due to resource timeout or memory, write a blocker/result
  separating resource failure from scientific rejection and stop for repair or
  human direction.
- If the row fails due to comparability or numerical hard veto, write a
  negative second-candidate result and stop for repair selection or human
  direction.
- If execution fails due to harness/runner artifact issues, write a blocker
  result and create a focused harness repair subplan before rerunning.
- If trusted GPU availability prevents a complete result, write a blocker
  result preserving partial artifacts and stop for scheduling or budget
  direction.

## Stop Conditions

- Trusted GPU precheck cannot see a usable GPU for the requested device.
- The exact second candidate cannot be executed by `--candidate-ids`.
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
2. Write the N3072 second-candidate validation result or blocker result.
3. Draft or refresh the next subplan, which should be local N3072 two-row
   consolidation/resource-boundary analysis if this row passes.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Subplan Self-Review

- Consistency: follows the N3072 resource-boundary closeout and uses explicit
  human approval for the next bounded runtime.
- Correctness: preserves timing/provenance, exact candidate filtering, bounded
  row artifact path integrity, and comparability gates before timing
  discussion.
- Feasibility: one row at a previously completed shape; no N4096 or broader
  ladder.
- Artifact coverage: specifies aggregate, row, log, result, review ledger, and
  next handoff artifacts.
- Boundary safety: preserves no-NumPy implementation policy and avoids ranking,
  default-readiness, speedup, posterior-correctness, HMC-readiness,
  other-candidate invalidity, deferred-candidate invalidity, and
  scientific-validity claims.
