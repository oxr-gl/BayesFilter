# Actual-SIR Low-Rank N1024 Seed-Replication Subplan

Date: 2026-06-23

Status: `DRAFT_READY_FOR_READ_ONLY_REVIEW_BEFORE_EXECUTION`

## Phase Objective

Run an independent `N=1024` seed-replication screen for the five low-rank
actual-SIR candidates that survived heldout, two `N=512` screens, and the first
`N=1024` paired-validation screen.

## Entry Conditions Inherited From Previous Phase

- The N1024 paired-validation result
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n1024-paired-validation-result-2026-06-23.md`
  left exactly five candidates viable.
- The previous phase used seeds `81129,81130`, batch `2`, time steps `20`,
  particles `1024`, `float32`, TF32 enabled, GPU visible,
  `CUDA_VISIBLE_DEVICES=1`, requested `/GPU:0`, and compiled-core timing for
  both streaming and low-rank routes.
- This phase must use independent seeds and preserve exact candidate filtering
  through `--candidate-ids`; it must not rerun extra grid rows and call them
  survivor validation.
- `r64_eps0p125_alpha1em08_it120` remains excluded because it failed heldout
  paired comparability. It must not be revived without a separate repair/tuning
  subplan.

## Required Artifacts

- This subplan.
- N1024 seed-replication aggregate JSON:
  `docs/benchmarks/actual-sir-low-rank-n1024-seed-replication-2026-06-23.json`
- N1024 seed-replication aggregate Markdown:
  `docs/benchmarks/actual-sir-low-rank-n1024-seed-replication-2026-06-23.md`
- Row JSON/Markdown/log artifacts produced by the grid runner under
  `docs/benchmarks` and `docs/benchmarks/logs`.
- A phase result/close record under `docs/plans`.
- The phase result/close record must include a decision table,
  inference-status table, post-run red-team note, and run manifest with git
  commit, command, environment, GPU/CPU status, seeds, wall time, output
  artifact paths, plan path, and result path.
- If one or more candidates remain viable, a next subplan before any further
  execution. Candidate consolidation is forbidden at this handoff unless a new
  reviewed consolidation subplan first declares an engineering criterion based
  on hard-veto survival and resource envelope only, not descriptive timing rank.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before execution.
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
- Exact candidate dry-run for the five survivor ids before GPU execution.
- Trusted GPU precheck before GPU execution.
- Execute only through
  `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py` with
  `streaming_timing_source=compiled_core`, `low_rank_timing_source=compiled_core`,
  `jit_compile=True`, GPU-visible scope, TF32 enabled, and expected GPU outputs.
- Verify aggregate JSON consistency after the run:
  candidate count, exact candidate ids, row status, row hard vetoes,
  provenance flags, labels, and row JSON/Markdown/log paths.
- Claude Opus/max may be used as a read-only reviewer for this material
  subplan. Claude is not an execution authority and cannot authorize crossing
  human, runtime, model-file, funding, product-capability, default-policy, or
  scientific-claim boundaries.

## Evidence Contract

- Question: do the five `N=1024` paired-validation survivors remain viable on
  an independent `N=1024` seed batch under the same compiled GPU/XLA actual-SIR
  paired screen?
- Baseline/comparator: paired streaming actual-SIR route rows from the same
  harness, seed batch, shape, dtype, TF32 mode, GPU visibility, and
  compiled-core timing contract.
- Candidate set:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
  - `r32_eps0p25_alpha1em08_it120`
  - `r64_eps0p25_alpha1em08_it120`
  - `r128_eps0p25_alpha1em08_it120`
- Excluded candidate:
  - `r64_eps0p125_alpha1em08_it120`, because it failed heldout paired
    comparability.
- Proposed seeds: `81131,81132`.
- Proposed shape: batch `2`, time steps `20`, particles `1024`.
- Primary screen: a candidate remains viable only if it has no hard vetoes,
  complete GPU/XLA compiled-core provenance, paired comparability pass,
  warm-time screen pass, and preserved row JSON/Markdown/log artifact paths.
- Warm-time screen pass is exactly the aggregate runner condition
  `_speed_screen_pass`: the row artifact's
  `paired_comparability.warm_median_streaming_over_low_rank` must be greater
  than or equal to
  `paired_comparability.thresholds.warm_median_streaming_over_low_rank`;
  the harness default threshold is `1.25`.
- Promotion vetoes: any row hard veto, missing compiled/XLA provenance, missing
  GPU outputs, stale row mismatch, missing/corrupt artifacts, nonfinite outputs,
  ESS hard veto, log-weight normalization failure, factor residual threshold
  failure, paired comparability failure, warm-time screen failure, missing
  per-row JSON/Markdown/log artifact paths, row timeout, or incomplete aggregate
  run.
- Explanatory diagnostics only: exact warm medians, warm ratios, row wall time,
  per-seed log-likelihood deltas, factor residual magnitudes below threshold,
  and GPU memory snapshots.
- What will not be concluded: statistical ranking, speedup, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API/default
  readiness, broad scalable-OT superiority, or production scientific validity.
- Artifact preserving result: the N1024 seed-replication grid JSON/Markdown,
  row artifacts/logs, and close record.

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Whether the five `N=1024` survivors remain viable on independent seeds |
| Candidate or mechanism under test | Repaired low-rank actual-SIR route under GPU/XLA compiled-core TensorFlow/TFP execution |
| Expected failure mode | Seed-specific paired-comparability failure, warm-screen failure, runtime timeout, numerical hard veto, or missing provenance/artifact |
| Promotion criterion | Exact candidate row has no hard vetoes, passes paired comparability and warm screen, has GPU/XLA/TF32 compiled-core provenance, and preserves row artifacts |
| Promotion veto | Any hard veto, missing provenance, failed comparability, failed warm screen, timeout, stale mismatch, or missing artifact |
| Continuation veto | Incomplete aggregate run, corrupt/missing artifacts that prevent interpretation, unavailable trusted GPU, or result requiring a forbidden claim |
| Repair trigger | Harness/provenance/artifact failure or a systematic hard veto pattern suggesting implementation rather than candidate-specific failure |
| Explanatory diagnostics | Warm ratios, row wall time, residual magnitudes below threshold, per-row deltas, GPU memory snapshots |
| Must not conclude | Ranking, speedup, correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, or scientific superiority |

## Skeptical Plan Audit

- Wrong baseline check: compare only against paired streaming rows from the
  same independent N1024 seed-replication run, not stale P03, N512, prior
  N1024, or low-rank-only rows.
- Proxy metric check: warm timing remains a viability screen, not proof of
  speedup, superiority, or production readiness.
- Stop condition check: provenance failures, hard vetoes, invalid artifacts,
  comparability failures, warm-screen failures, missing row artifact paths,
  stale-row mismatches, row timeouts, and incomplete aggregate runs block
  candidate advancement.
- Fairness check: all candidates share seeds, shape, dtype, TF32 mode, GPU
  visibility, timing source, and transport policy; only rank/epsilon vary.
- Hidden assumption check: independent `N=1024` seed replication is not a broad
  scaling law, high-N envelope, statistical ranking, or default-readiness
  claim.
- Environment mismatch check: GPU checks must be trusted; sandbox GPU failures
  do not establish machine/framework failure until rerun in trusted context.
- Artifact sufficiency check: aggregate JSON must preserve exact candidate ids,
  row labels, provenance flags, row artifacts, and summary counts.

Audit result: passes as a next-step replication screen because it tests the
same five candidates at the same particle count on independent seeds while
preserving scientific and product-claim boundaries.

## Candidate Dry-Run Command

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode dry-run \
  --route both \
  --batch-seeds 81131,81132 \
  --time-steps 20 \
  --num-particles 1024 \
  --low-rank-ranks 16,32,64,128 \
  --low-rank-assignment-epsilons 0.25,0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120,r32_eps0p25_alpha1em08_it120,r64_eps0p25_alpha1em08_it120,r128_eps0p25_alpha1em08_it120 \
  --warmups 1 \
  --repeats 2 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --jit-compile \
  --row-timeout-seconds 3600 \
  --output /tmp/actual-sir-low-rank-n1024-seed-replication-exact-candidate-dry-run.json \
  --markdown-output /tmp/actual-sir-low-rank-n1024-seed-replication-exact-candidate-dry-run.md \
  --quiet
```

## Candidate Execution Command

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --route both \
  --batch-seeds 81131,81132 \
  --time-steps 20 \
  --num-particles 1024 \
  --low-rank-ranks 16,32,64,128 \
  --low-rank-assignment-epsilons 0.25,0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120,r32_eps0p25_alpha1em08_it120,r64_eps0p25_alpha1em08_it120,r128_eps0p25_alpha1em08_it120 \
  --warmups 1 \
  --repeats 2 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --jit-compile \
  --row-timeout-seconds 3600 \
  --output docs/benchmarks/actual-sir-low-rank-n1024-seed-replication-2026-06-23.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-n1024-seed-replication-2026-06-23.md
```

The row timeout remains `3600` seconds because the first `N=1024` run completed
each row below this limit but independent seeds may still vary. If a row times
out, record it as a blocker/result under the evidence contract rather than
inferring candidate or route invalidity.

## Forbidden Claims And Actions

- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not use old contaminated P03 rows as current performance evidence.
- Do not rank candidates statistically from descriptive warm timing alone.
- Do not claim speedup, posterior correctness, HMC readiness, dense Sinkhorn
  equivalence, public API/default readiness, scientific superiority, or
  production readiness.
- Do not continue from hard vetoes or failed comparability as if timing
  evidence were valid.
- Do not reintroduce `r64_eps0p125_alpha1em08_it120` into the survivor
  validation set without a new repair/tuning subplan.
- Do not consolidate candidates at this handoff unless a separate reviewed
  consolidation subplan defines an engineering-only criterion based on
  hard-veto survival and resource envelope.

## Exact Next-Phase Handoff Conditions

- If one or more candidates remain viable, draft either a reviewed
  consolidation/resource-envelope subplan or a larger-`N` validation subplan
  for the viable set. Consolidation must not rely on descriptive timing rank.
- If no candidate remains viable due to comparability, warm-screen, timeout, or
  hard-veto failures, write a negative result separating candidate rejection
  from route-repair rejection, then stop for repair selection or human
  direction.
- If execution fails due to harness/runner artifact issues, write a blocker
  result and create a focused harness repair subplan before rerunning.
- If trusted GPU availability prevents a complete result, write a
  blocker/result preserving partial artifacts and stop for scheduling or budget
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
  result.
- Any row times out or the aggregate run is incomplete; write a blocker/result
  preserving partial artifacts rather than interpreting the incomplete run as a
  pass.
- The result cannot be interpreted without crossing a forbidden claim boundary.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the N1024 seed-replication phase result or blocker result.
3. Draft or refresh the next subplan.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Subplan Self-Review

- Consistency: aligns with the N1024 paired-validation result and carries
  forward only the five exact survivor candidates.
- Correctness: preserves timing/provenance, exact candidate filtering, row
  artifact path integrity, and comparability gates before timing discussion.
- Feasibility: repeats the same `N=1024`, batch `2`, and row timeout on
  independent seeds rather than jumping to a broader high-N envelope.
- Artifact coverage: specifies aggregate, row, log, and close-record artifacts.
- Boundary safety: preserves no-NumPy implementation policy and avoids ranking,
  default-readiness, speedup, posterior-correctness, and scientific-validity
  claims.
