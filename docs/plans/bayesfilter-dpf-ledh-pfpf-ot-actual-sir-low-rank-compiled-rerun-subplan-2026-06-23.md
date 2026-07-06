# Actual-SIR Low-Rank Compiled Rerun Subplan

Date: 2026-06-23

Status: `READY_FOR_LOCAL_EXECUTION`

## Phase Objective

Rerun the actual-SIR low-rank tuning/performance screen after the TensorFlow
tensor-only XLA repair, using only GPU-targeted compiled-core route timing, to
answer whether the earlier stale `NO_FREEZE_CANDIDATE_REPAIR_REQUIRED` verdict
changes under repaired provenance.

## Entry Conditions Inherited From Previous Phase

- The low-rank route repair result is recorded in
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-route-performance-repair-result-2026-06-22.md`.
- The validation harness and tuning grid require `compiled_core` timing and
  `jit_compile=True`; there is no promotional non-XLA timing escape.
- The previous P03 tuning result is stale as performance evidence because it
  included eager/diagnostic route timing contamination.
- BayesFilter-owned algorithmic paths must remain TensorFlow/TensorFlow
  Probability, GPU-oriented, and XLA compiled for this route.

## Required Artifacts

- Subplan: this file.
- Tiny trusted GPU compiled smoke:
  `docs/benchmarks/actual-sir-low-rank-compiled-rerun-p01-smoke-2026-06-23.json`
  and matching Markdown.
- Bounded trusted GPU compiled grid, if the smoke passes:
  `docs/benchmarks/actual-sir-low-rank-compiled-rerun-p02-grid-2026-06-23.json`
  and matching Markdown, plus row JSON/Markdown/log artifacts.
- Close record:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-compiled-rerun-result-2026-06-23.md`.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before GPU execution.
- Local syntax check for the harness, grid, and focused tests.
- Focused unit tests for the low-rank solver, validation harness, and tuning
  grid after any code edits. If no code edits are made after this subplan, the
  previous focused pass may be cited and the rerun must still preserve the
  current file provenance.
- Trusted GPU precheck with `nvidia-smi`.
- Tiny compiled GPU smoke with `--route both`, `--jit-compile`,
  `--device-scope visible`, `--expect-device-kind gpu`, and
  `CUDA_VISIBLE_DEVICES=1`.
- Bounded compiled GPU grid only if the smoke status is `PASS` and has no hard
  vetoes.
- Result review by Codex for consistency, artifact coverage, boundary safety,
  and stale-row rejection. Claude is not an execution authority; no Claude
  agreement is required to interpret the local artifacts for this bounded rerun.

## Evidence Contract

- Question: after removing eager/NumPy-style timing barriers from the low-rank
  route, does the repaired GPU/XLA compiled-core route nominate any low-rank
  freeze candidate on the bounded actual-SIR screen?
- Baseline/comparator: streaming actual-SIR route rows from the same harness,
  seed, shape, dtype, TF32 mode, GPU visibility, and compiled-core timing
  contract.
- Primary screen: a row is only freeze-nominated if the grid classifies it as
  `freeze-nominated`, which requires no hard vetoes, paired comparability pass,
  complete low-rank compiled/XLA provenance, complete GPU/TF32 provenance, and
  the predeclared warm-time screen.
- Veto diagnostics: nonzero subprocess exit, stale row request mismatch,
  missing JSON/Markdown artifacts, missing GPU outputs, missing XLA provenance,
  nonfinite route outputs, ESS hard veto, log-weight normalization failure,
  factor marginal residual threshold failure, negative/nonfinite low-rank
  factors, or route invocation mismatch.
- Explanatory diagnostics only: medians, means, individual warm timings,
  GPU memory snapshots, per-candidate descriptive ratios, and row ordering.
- Not concluded even if rows pass: posterior correctness, HMC readiness, dense
  Sinkhorn equivalence, public API/default readiness, broad scalable-OT
  superiority, statistical ranking, or production scientific validity.
- Artifact preserving result: the close record and the smoke/grid JSON/Markdown
  artifacts listed above.

## Skeptical Plan Audit

- Wrong baseline check: the comparator is the paired streaming route from the
  same compiled harness, not old P03 contaminated timing rows.
- Proxy metric check: warm median ratio is a screen for candidate nomination,
  not proof of speedup or superiority.
- Stop condition check: smoke hard vetoes, GPU/XLA provenance failures, stale
  row mismatches, and invalid artifacts stop the grid or block interpretation.
- Fairness check: all grid rows use the same seed, shape, dtype, TF32 mode,
  GPU visibility, route timing source, and transport policy; only low-rank
  rank/epsilon vary.
- Hidden assumption check: one seed and one target shape are not enough for a
  statistical ranking; the result can only nominate or reject bounded-screen
  candidates.
- Environment mismatch check: GPU failures from untrusted context are not
  machine failures; trusted GPU execution is required for the smoke/grid.
- Artifact sufficiency check: the aggregate grid JSON must record
  `num_freeze_nominated`, labels, row artifact paths, and provenance checks.

Audit result: passes for a bounded rerun because the planned artifacts directly
answer the repaired-provenance tuning-screen question while preserving
nonclaims and continuation vetoes.

## Commands

Syntax check:

```bash
python -m py_compile \
  docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py \
  docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  tests/test_low_rank_coupling_solver_tf.py \
  tests/test_actual_sir_low_rank_route_validation.py \
  tests/test_actual_sir_low_rank_tuning_grid.py
```

Trusted GPU precheck:

```bash
nvidia-smi --query-gpu=index,name,uuid,memory.used,utilization.gpu --format=csv,noheader,nounits
```

Tiny compiled smoke:

```bash
python docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py \
  --route both \
  --batch-seeds 81120 \
  --time-steps 3 \
  --num-particles 128 \
  --low-rank-rank 32 \
  --low-rank-assignment-epsilon 0.25 \
  --low-rank-max-projection-iterations 120 \
  --warmups 0 \
  --repeats 1 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --jit-compile \
  --output docs/benchmarks/actual-sir-low-rank-compiled-rerun-p01-smoke-2026-06-23.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-compiled-rerun-p01-smoke-2026-06-23.md
```

Bounded compiled grid:

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --route both \
  --batch-seeds 81120 \
  --time-steps 20 \
  --num-particles 256 \
  --low-rank-ranks 16,32,64,128 \
  --low-rank-assignment-epsilons 0.25,0.125,0.0625 \
  --low-rank-max-projection-iterations-list 120 \
  --warmups 1 \
  --repeats 2 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --jit-compile \
  --row-timeout-seconds 900 \
  --output docs/benchmarks/actual-sir-low-rank-compiled-rerun-p02-grid-2026-06-23.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-compiled-rerun-p02-grid-2026-06-23.md
```

## Forbidden Claims And Actions

- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not use old P03 rows as current performance evidence.
- Do not rank stochastic candidates statistically from this one-seed bounded
  screen.
- Do not claim posterior correctness, HMC readiness, dense Sinkhorn
  equivalence, public API/default readiness, scientific superiority, or
  production readiness from this rerun.
- Do not continue from a smoke/grid hard veto as if timing evidence were valid.
- Do not let Claude authorize crossing human, runtime, model-file, funding,
  product-capability, or scientific-claim boundaries.

## Exact Next-Phase Handoff Conditions

- If `num_freeze_nominated > 0`, hand off to a heldout/replication subplan that
  treats candidates as nominated only, with multi-seed or uncertainty-aware
  evidence before any ranking or default claim.
- If `num_freeze_nominated == 0` and artifacts are valid, hand off to a
  closeout or repair-selection subplan stating that the repaired compiled
  bounded grid did not alter the practical no-freeze-candidate verdict for this
  shape.
- If the smoke or grid emits a hard veto, hand off to a focused repair subplan
  only if the veto identifies a fixable harness/implementation issue; otherwise
  write a blocker result and stop for direction.

## Stop Conditions

- Trusted GPU precheck cannot see a usable GPU for `CUDA_VISIBLE_DEVICES=1`.
- Smoke row status is not `PASS`, or any aggregate hard veto is present.
- Grid subprocess exits nonzero, times out, or emits missing/corrupt/stale row
  artifacts.
- Any row lacks `compiled_core`, `jit_compile=True`, or expected GPU output
  provenance.
- Any BayesFilter-owned algorithmic path reintroduces NumPy/eager barriers.
- The result cannot be interpreted without crossing a forbidden claim boundary.
