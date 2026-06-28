# Actual-SIR Low-Rank N512 Seed-Replication Subplan

Date: 2026-06-23

Status: `DRAFT_READY_FOR_READ_ONLY_REVIEW_BEFORE_EXECUTION`

## Phase Objective

Run an independent same-particle `N=512` seed-batch replication over the five
larger-particle viable low-rank candidates, to test whether the larger-particle
viability screen survives another seed batch without using descriptive timing as
ranking evidence.

## Entry Conditions Inherited From Previous Phase

- The heldout result
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-heldout-replication-result-2026-06-23.md`
  left five candidates viable and rejected
  `r64_eps0p125_alpha1em08_it120` at the heldout comparability gate.
- The larger-particle result
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-larger-particle-replication-result-2026-06-23.md`
  left exactly the same five candidates viable at `N=512`.
- The next phase must preserve exact candidate filtering through
  `--candidate-ids`; it must not rerun extra grid rows and call them survivor
  validation.

## Required Artifacts

- This subplan.
- N512 seed-replication aggregate JSON:
  `docs/benchmarks/actual-sir-low-rank-n512-seed-replication-2026-06-23.json`
- N512 seed-replication aggregate Markdown:
  `docs/benchmarks/actual-sir-low-rank-n512-seed-replication-2026-06-23.md`
- Row JSON/Markdown/log artifacts produced by the grid runner under
  `docs/benchmarks` and `docs/benchmarks/logs`.
- A phase result/close record under `docs/plans`.
- If one or more candidates remain viable, a next subplan for either staged
  `N=1024` paired validation or candidate consolidation under a reviewed
  engineering criterion.

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

- Question: do the five `N=512` larger-particle survivors remain viable on an
  independent `N=512` seed batch under the same compiled GPU/XLA actual-SIR
  screen?
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
- Proposed independent seeds: `81126,81127,81128`.
- Proposed shape: batch `3`, time steps `20`, particles `512`.
- Primary screen: a candidate remains viable only if it has no hard vetoes,
  complete GPU/XLA compiled-core provenance, paired comparability pass,
  warm-time screen pass, and preserved row JSON/Markdown/log artifact paths.
- Promotion vetoes: any row hard veto, missing compiled/XLA provenance, missing
  GPU outputs, stale row mismatch, missing/corrupt artifacts, nonfinite outputs,
  ESS hard veto, log-weight normalization failure, factor residual threshold
  failure, paired comparability failure, warm-time screen failure, or missing
  per-row JSON/Markdown/log artifact paths needed to audit the aggregate
  result.
- Explanatory diagnostics only: exact warm medians, warm ratios, row wall time,
  per-seed log-likelihood deltas, factor residual magnitudes below threshold,
  and GPU memory snapshots.
- What will not be concluded: statistical ranking, speedup, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API/default
  readiness, broad scalable-OT superiority, or production scientific validity.
- Artifact preserving result: the seed-replication grid JSON/Markdown, row
  artifacts/logs, and close record.

## Skeptical Plan Audit

- Wrong baseline check: compare only against paired streaming rows from the
  same seed-replication run, not stale P03, compiled-screen, heldout, or first
  `N=512` rows.
- Proxy metric check: warm timing remains a viability screen, not proof of
  speedup, superiority, or production readiness.
- Stop condition check: provenance failures, hard vetoes, invalid artifacts,
  comparability failures, missing row artifact paths, and warm-screen failures
  block candidate advancement before descriptive timing is discussed; stale-row
  mismatches, row timeouts, and incomplete aggregate runs become blocker
  results rather than pass evidence.
- Fairness check: all candidates share seeds, shape, dtype, TF32 mode, GPU
  visibility, timing source, and transport policy; only rank/epsilon vary.
- Hidden assumption check: another `N=512` seed batch increases replication
  support but still does not establish statistical ranking without a declared
  uncertainty model.
- Artifact sufficiency check: aggregate JSON must preserve exact candidate ids,
  row labels, provenance flags, row artifacts, and summary counts.

Audit result: passes as a next-step replication screen because it tests the
same five candidates on independent seeds while preserving scientific and
product-claim boundaries.

## Candidate Command

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --route both \
  --batch-seeds 81126,81127,81128 \
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
  --row-timeout-seconds 2400 \
  --output docs/benchmarks/actual-sir-low-rank-n512-seed-replication-2026-06-23.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-n512-seed-replication-2026-06-23.md
```

The row timeout is raised relative to the first `N=512` screen because this
replication uses batch size `3` instead of `2`. If a row times out, record it as
a blocker/result under the evidence contract rather than inferring candidate or
route invalidity.

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

- If one or more candidates remain viable, draft either a staged `N=1024`
  paired validation subplan or a candidate-consolidation subplan with a
  reviewed engineering criterion that does not pretend to be a statistical
  ranking.
- If no candidate remains viable due to comparability, warm-screen, or
  hard-veto failures, write a negative result separating candidate rejection
  from route-repair rejection, then stop for repair selection or human
  direction.
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
- Any row has a stale row mismatch with the requested seed batch, shape,
  candidate id, dtype, timing source, TF32 mode, or device policy.
- Any row emits a hard veto, paired comparability failure, warm-screen failure,
  or invalid artifact.
- Any row is missing its JSON, Markdown, or log artifact path in the aggregate
  result.
- Any row times out or the aggregate run is incomplete; write a blocker/result
  preserving partial artifacts rather than interpreting the incomplete run as a
  pass.
- The result cannot be interpreted without crossing a forbidden claim boundary.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the N512 seed-replication phase result or blocker result.
3. Draft or refresh the next subplan.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Subplan Review

- Consistency: aligns with the larger-particle result and carries forward only
  the five candidates that passed heldout and first `N=512` paired screens.
- Correctness: preserves timing/provenance, exact candidate filtering, row
  artifact path integrity, and comparability gates before timing discussion.
- Feasibility: repeats the `N=512` screen on a new seed batch with a row timeout
  scaled for batch size `3`.
- Artifact coverage: specifies aggregate, row, log, and close-record artifacts.
- Boundary safety: preserves nonclaims and blocks stale evidence, NumPy
  algorithmic implementation, descriptive-only statistical ranking, and
  overinterpretation of timing.
