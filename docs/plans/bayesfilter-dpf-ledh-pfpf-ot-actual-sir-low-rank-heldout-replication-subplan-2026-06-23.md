# Actual-SIR Low-Rank Heldout Replication Subplan

Date: 2026-06-23

Status: `DRAFT_READY_FOR_REVIEW_BEFORE_EXECUTION`

## Phase Objective

Validate the six repaired compiled-screen low-rank freeze-nominated candidates
on heldout seeds under the same GPU/XLA compiled-core provenance contract, to
determine whether any candidate remains viable beyond the single-seed bounded
screen.

## Entry Conditions Inherited From Previous Phase

- The repaired tensor-only low-rank route is accepted for compiled GPU/XLA route
  testing by
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-route-performance-repair-result-2026-06-22.md`.
- The bounded compiled rerun result is recorded in
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-compiled-rerun-result-2026-06-23.md`.
- The bounded compiled grid artifact
  `docs/benchmarks/actual-sir-low-rank-compiled-rerun-p02-grid-2026-06-23.json`
  has status `PASS`, with `6` freeze-nominated candidates and no row hard
  vetoes.
- The old contaminated P03 no-freeze-candidate verdict is superseded only for
  the bounded repaired-provenance screen; it must not be used as current
  performance evidence.

## Required Artifacts

- This subplan.
- A heldout/replication grid JSON and Markdown artifact under
  `docs/benchmarks`, with row JSON/Markdown/log artifacts.
- A phase result/close record under `docs/plans`.
- If any candidate remains viable, a next subplan for larger-shape or
  uncertainty-aware validation before any default/product/scientific claim.
- Runner patch required before execution: `run_actual_sir_low_rank_tuning_grid.py`
  must support `--candidate-ids` so the exact nominated set can be executed
  without extra rows.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before execution.
- Local syntax check for the validation harness and grid.
- Trusted GPU precheck before GPU execution.
- Execute only through
  `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py` with
  `streaming_timing_source=compiled_core`, `low_rank_timing_source=compiled_core`,
  `jit_compile=True`, GPU-visible scope, TF32 enabled, and expected GPU outputs.
- Verify aggregate JSON consistency after the run:
  candidate count, row status, row hard vetoes, provenance flags, labels, and
  artifact paths.
- Review the result for consistency, correctness, feasibility, artifact
  coverage, and boundary safety before drafting the next subplan.
- Claude may be used as a read-only reviewer only for material subplan or
  interpretation concerns. Claude is not an execution authority and cannot
  authorize crossing human, runtime, model-file, funding, product-capability,
  or scientific-claim boundaries.

## Evidence Contract

- Question: do any of the six bounded-screen freeze-nominated low-rank
  candidates remain viable on heldout seeds under the same compiled GPU/XLA
  actual-SIR screen?
- Baseline/comparator: paired streaming actual-SIR route rows from the same
  harness, shapes, dtype, TF32 mode, GPU visibility, and compiled-core timing
  contract.
- Candidate set:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
  - `r32_eps0p25_alpha1em08_it120`
  - `r64_eps0p25_alpha1em08_it120`
  - `r64_eps0p125_alpha1em08_it120`
  - `r128_eps0p25_alpha1em08_it120`
- Proposed heldout seeds: `81121,81122,81123`.
- Proposed shape: batch `3`, time steps `20`, particles `256`.
- Primary screen: a candidate remains viable only if it has no hard vetoes,
  complete GPU/XLA compiled-core provenance, paired comparability pass, and
  warm-time screen pass on the heldout batch.
- Promotion vetoes: any row hard veto, missing compiled/XLA provenance, missing
  GPU outputs, stale row mismatch, missing/corrupt artifacts, nonfinite outputs,
  ESS hard veto, log-weight normalization failure, factor residual threshold
  failure, or paired comparability failure.
- Explanatory diagnostics only: exact warm medians, warm ratios, row wall time,
  per-seed log-likelihood deltas, factor residual magnitudes below threshold,
  and GPU memory snapshots.
- What will not be concluded: statistical ranking, posterior correctness, HMC
  readiness, dense Sinkhorn equivalence, public API/default readiness, broad
  scalable-OT superiority, or production scientific validity.
- Artifact preserving result: the heldout grid JSON/Markdown, row artifacts,
  and close record.

## Skeptical Plan Audit

- Wrong baseline check: compare only against paired streaming rows from the
  same heldout run, not stale P03 artifacts.
- Proxy metric check: warm timing remains a viability screen, not proof of
  speedup or superiority.
- Stop condition check: provenance failures, hard vetoes, and invalid artifacts
  block interpretation rather than becoming timing evidence.
- Fairness check: all candidates share heldout seeds, shape, dtype, TF32 mode,
  GPU visibility, timing source, and transport policy; only rank/epsilon vary.
- Hidden assumption check: three heldout seeds are still limited evidence and
  cannot establish a statistical ranking without an explicit uncertainty model.
- Artifact sufficiency check: aggregate JSON must preserve row labels,
  provenance flags, row artifacts, and summary counts.

Audit result: passes as a next-step validation screen because it directly tests
whether bounded-screen nominations survive heldout seeds without crossing
scientific or product-readiness boundaries.

## Candidate Command

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --route both \
  --batch-seeds 81121,81122,81123 \
  --time-steps 20 \
  --num-particles 256 \
  --low-rank-ranks 16,32,64,128 \
  --low-rank-assignment-epsilons 0.25,0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120,r32_eps0p25_alpha1em08_it120,r64_eps0p25_alpha1em08_it120,r64_eps0p125_alpha1em08_it120,r128_eps0p25_alpha1em08_it120 \
  --warmups 1 \
  --repeats 2 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --jit-compile \
  --row-timeout-seconds 1200 \
  --output docs/benchmarks/actual-sir-low-rank-heldout-replication-2026-06-23.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-heldout-replication-2026-06-23.md
```

This command uses `--candidate-ids` to execute exactly the six nominated
candidate arms. If the runner does not support this flag or the requested ids
cannot be matched exactly, stop before GPU execution.

## Forbidden Claims And Actions

- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not use old contaminated P03 rows as current performance evidence.
- Do not rank candidates statistically from descriptive warm timing alone.
- Do not claim posterior correctness, HMC readiness, dense Sinkhorn
  equivalence, public API/default readiness, scientific superiority, or
  production readiness.
- Do not continue from hard vetoes as if timing evidence were valid.
- Do not execute extra grid rows and then describe them as nominated candidate
  validation.

## Exact Next-Phase Handoff Conditions

- If one or more candidates remain viable, draft a larger-shape or
  uncertainty-aware replication subplan using only those heldout-viable
  candidates.
- If no candidate remains viable due to comparability or hard-veto failures,
  write a negative result separating candidate rejection from route-repair
  rejection, then stop for repair selection or human direction.
- If execution fails due to harness/runner artifact issues, write a blocker
  result and create a focused harness repair subplan before rerunning.

## Stop Conditions

- Trusted GPU precheck cannot see a usable GPU for the requested device.
- The exact nominated candidate set cannot be executed by `--candidate-ids`.
- Any row lacks `compiled_core`, `jit_compile=True`, or expected GPU output
  provenance.
- Any row emits a hard veto or invalid artifact.
- The result cannot be interpreted without crossing a forbidden claim boundary.

## Subplan Review

- Consistency: aligns with the compiled rerun result and preserves the six
  nominated candidates as the validation target.
- Correctness: keeps timing/provenance and comparability gates explicit.
- Feasibility: requires the reviewed `--candidate-ids` runner patch so the
  exact six-candidate set is executed without extra rows.
- Artifact coverage: specifies aggregate, row, and close-record artifacts.
- Boundary safety: preserves nonclaims and blocks stale P03 evidence, NumPy
  algorithmic implementation, and descriptive-only statistical ranking.
