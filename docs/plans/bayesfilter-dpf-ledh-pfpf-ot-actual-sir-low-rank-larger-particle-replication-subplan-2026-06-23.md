# Actual-SIR Low-Rank Larger-Particle Replication Subplan

Date: 2026-06-23

Status: `DRAFT_READY_FOR_READ_ONLY_REVIEW_BEFORE_EXECUTION`

## Phase Objective

Run the smallest larger-particle paired GPU/XLA actual-SIR screen that tests
whether the five heldout-surviving low-rank candidates remain viable when the
particle count increases from `N=256` to `N=512`.

## Entry Conditions Inherited From Previous Phase

- The repaired tensor-only low-rank route is accepted for compiled GPU/XLA route
  testing by
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-route-performance-repair-result-2026-06-22.md`.
- The bounded compiled rerun result is recorded in
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-compiled-rerun-result-2026-06-23.md`.
- The heldout result
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-heldout-replication-result-2026-06-23.md`
  leaves exactly five candidates viable and rejects
  `r64_eps0p125_alpha1em08_it120` at the heldout comparability gate.
- The next phase must preserve exact candidate filtering through
  `--candidate-ids`; it must not rerun extra grid rows and call them survivor
  validation.

## Required Artifacts

- This subplan.
- Larger-particle aggregate JSON:
  `docs/benchmarks/actual-sir-low-rank-larger-particle-replication-2026-06-23.json`
- Larger-particle aggregate Markdown:
  `docs/benchmarks/actual-sir-low-rank-larger-particle-replication-2026-06-23.md`
- Row JSON/Markdown/log artifacts produced by the grid runner under
  `docs/benchmarks` and `docs/benchmarks/logs`.
- A phase result/close record under `docs/plans`.
- If one or more candidates remain viable, a next subplan for either
  uncertainty-aware replication or a carefully staged larger-N envelope.

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
  provenance flags, labels, and artifact paths.
- Claude Opus/max may be used as a read-only reviewer for this material
  subplan. Claude is not an execution authority and cannot authorize crossing
  human, runtime, model-file, funding, product-capability, default-policy, or
  scientific-claim boundaries.

## Evidence Contract

- Question: do the five heldout-surviving candidates remain viable when the
  particle count increases from `N=256` to `N=512` under the same compiled
  GPU/XLA actual-SIR screen?
- Baseline/comparator: paired streaming actual-SIR route rows from the same
  harness, seeds, shape, dtype, TF32 mode, GPU visibility, and compiled-core
  timing contract.
- Candidate set:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
  - `r32_eps0p25_alpha1em08_it120`
  - `r64_eps0p25_alpha1em08_it120`
  - `r128_eps0p25_alpha1em08_it120`
- Excluded candidate:
  - `r64_eps0p125_alpha1em08_it120`, because it failed heldout paired
    comparability.
- Proposed seeds: `81124,81125`.
- Proposed shape: batch `2`, time steps `20`, particles `512`.
- Primary screen: a candidate remains viable only if it has no hard vetoes,
  complete GPU/XLA compiled-core provenance, paired comparability pass, and
  warm-time screen pass on the larger-particle batch.
- Promotion vetoes: any row hard veto, missing compiled/XLA provenance, missing
  GPU outputs, stale row mismatch, missing/corrupt artifacts, nonfinite outputs,
  ESS hard veto, log-weight normalization failure, factor residual threshold
  failure, paired comparability failure, or missing per-row JSON/Markdown/log
  artifact paths needed to audit the aggregate result.
- Explanatory diagnostics only: exact warm medians, warm ratios, row wall time,
  per-seed log-likelihood deltas, factor residual magnitudes below threshold,
  and GPU memory snapshots.
- What will not be concluded: statistical ranking, speedup, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API/default
  readiness, broad scalable-OT superiority, or production scientific validity.
- Artifact preserving result: the larger-particle grid JSON/Markdown, row
  artifacts/logs, and close record.

## Skeptical Plan Audit

- Wrong baseline check: compare only against paired streaming rows from the
  same larger-particle run, not stale P03, compiled-screen, or heldout rows.
- Proxy metric check: warm timing remains a viability screen, not proof of
  speedup, superiority, or production readiness.
- Stop condition check: provenance failures, hard vetoes, invalid artifacts,
  and comparability failures block candidate advancement before timing is
  interpreted.
- Fairness check: all candidates share seeds, shape, dtype, TF32 mode, GPU
  visibility, timing source, and transport policy; only rank/epsilon vary.
- Hidden assumption check: `N=512` is a larger-shape screen, not a broad scaling
  law or high-N envelope claim.
- Artifact sufficiency check: aggregate JSON must preserve exact candidate ids,
  row labels, provenance flags, row artifacts, and summary counts.

Audit result: passes as a next-step validation screen because it directly tests
the heldout survivors at the next particle count while preserving the
scientific and product-claim boundaries.

## Candidate Command

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --route both \
  --batch-seeds 81124,81125 \
  --time-steps 20 \
  --num-particles 512 \
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
  --row-timeout-seconds 1800 \
  --output docs/benchmarks/actual-sir-low-rank-larger-particle-replication-2026-06-23.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-larger-particle-replication-2026-06-23.md
```

The row timeout is intentionally larger than the heldout `N=256` timeout
because paired streaming rows are expected to be more expensive at `N=512`.
If a row times out, record it as a blocker/result under the evidence contract
rather than inferring candidate or route invalidity.

## Forbidden Claims And Actions

- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not use old contaminated P03 rows as current performance evidence.
- Do not rank candidates statistically from descriptive warm timing alone.
- Do not claim speedup, posterior correctness, HMC readiness, dense Sinkhorn
  equivalence, public API/default readiness, scientific superiority, or
  production readiness.
- Do not continue from hard vetoes or failed comparability as if timing evidence
  were valid.
- Do not reintroduce `r64_eps0p125_alpha1em08_it120` into the survivor
  validation set without a new repair/tuning subplan.

## Exact Next-Phase Handoff Conditions

- If one or more candidates remain viable, draft an uncertainty-aware
  replication subplan or a staged larger-N envelope subplan using only those
  larger-particle viable candidates.
- If no candidate remains viable due to comparability or hard-veto failures,
  write a negative result separating candidate rejection from route-repair
  rejection, then stop for repair selection or human direction.
- If execution fails due to harness/runner artifact issues, write a blocker
  result and create a focused harness repair subplan before rerunning.
- If trusted GPU availability or row timeouts prevent a complete result, write
  a blocker/result preserving partial artifacts and stop for scheduling or
  budget direction.

## Stop Conditions

- Trusted GPU precheck cannot see a usable GPU for the requested device.
- The exact survivor candidate set cannot be executed by `--candidate-ids`.
- Any row lacks `compiled_core`, `jit_compile=True`, or expected GPU output
  provenance.
- Any row emits a hard veto or invalid artifact.
- Any row is missing its JSON, Markdown, or log artifact path in the aggregate
  result.
- The result cannot be interpreted without crossing a forbidden claim boundary.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the larger-particle phase result or blocker result.
3. Draft or refresh the next subplan.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Subplan Review

- Consistency: aligns with the heldout result and carries forward only the five
  candidates that passed heldout paired comparability.
- Correctness: preserves timing/provenance, exact candidate filtering, and
  comparability gates before timing interpretation.
- Feasibility: uses the next particle count (`N=512`) rather than jumping to a
  high-N envelope, with a larger row timeout to account for paired streaming
  cost.
- Artifact coverage: specifies aggregate, row, log, and close-record artifacts.
- Boundary safety: preserves nonclaims and blocks stale evidence, NumPy
  algorithmic implementation, and descriptive-only statistical ranking.
