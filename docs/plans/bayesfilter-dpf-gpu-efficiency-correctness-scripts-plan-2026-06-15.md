# BayesFilter DPF GPU Efficiency And Correctness Script Plan

Date: 2026-06-15

## Question

Can we add opt-in scripts that separate correctness gates from GPU/CPU timing
diagnostics for the experimental batched LEDH-PFPF-OT DPF path?

## Mechanism Being Tested

The scripts exercise the existing fixed-branch experimental implementation in
`experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`.
They do not promote that implementation to production default and do not change
the implementation route.

## Evidence Contract

- Engineering question: can deterministic tiny-fixture checks fail closed before
  running any timing matrix?
- Baseline/comparator: current fixed-branch batched value path compared against a
  scalar-row stack over the same deterministic inputs.
- Primary pass/fail criterion: finite outputs plus batched/scalar value parity
  within the existing tiny-fixture tolerances.
- Veto diagnostics: non-finite likelihood, failed row permutation, failed
  identical-row locality, failed JIT smoke, failed no-resampling finite
  difference score check, or wrong device placement when a device expectation is
  explicitly requested.
- Explanatory-only diagnostics: source-loop audit, compile-plus-first-call time,
  warm-call time, GPU memory readings, and active-transport score behavior.
- What will not be concluded: no production/default readiness, no GPU
  superiority, no posterior validity, no active-transport score correctness, and
  no HMC/NeuTra readiness.
- Artifact: JSON outputs from the correctness gate and benchmark matrix scripts.

## Skeptical Plan Audit

- Wrong baseline risk: avoid comparing only against a timing run; correctness
  uses scalar-row fixed-input parity first.
- Proxy metric risk: timing and memory are reported as descriptive diagnostics,
  never promotion criteria.
- Missing stop condition risk: timing matrix script runs the correctness
  preflight by default and fails if any child artifact fails.
- Unfair comparison risk: child benchmark commands record shape, mode, device,
  transport policy, JIT status, and output artifact path.
- Hidden assumptions: the fixed-branch path still has a Python time loop and
  dense `[B,N,N]` transport; source diagnostics report this instead of treating
  it as solved.
- Environment mismatch: scripts record TensorFlow, visible devices, requested
  device scope, and CUDA visibility.
- Artifact relevance: each child command writes JSON; the matrix script stores
  both child paths and a compact summary.

The plan passes for scoped script creation. Long `T=200,N=1000` GPU runs remain
future opt-in commands, not part of this edit.

## Commands

Tiny correctness smoke:

```bash
python docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_correctness.py \
  --device-scope cpu \
  --device /CPU:0 \
  --expect-device-kind cpu \
  --batch-size 2 \
  --time-steps 3 \
  --num-particles 4 \
  --sinkhorn-iterations 4 \
  --output /tmp/experimental-ledh-pfpf-ot-correctness-smoke.json
```

Tiny matrix smoke:

```bash
python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_efficiency_matrix.py \
  --device-scope cpu \
  --device /CPU:0 \
  --expect-device-kind cpu \
  --shape B=2,T=3,N=4 \
  --transport-policy no-resampling \
  --mode compiled-value \
  --sinkhorn-iterations 4 \
  --warmups 0 \
  --repeats 1 \
  --output /tmp/experimental-ledh-pfpf-ot-efficiency-matrix-smoke.json
```

## Interpretation Rule

- If the correctness gate fails, timing results are not usable for research or
  engineering decisions.
- If the correctness gate passes but timing is slow or memory-heavy, that is
  evidence about implementation shape only, not a rejection of the DPF method.
- If tiny CPU correctness passes, larger trusted GPU runs may be launched as
  opt-in benchmark diagnostics with the same nonclaims.
