# Experiment plan: LEDH-PFPF-OT scalable OT literature survey

## Question
Can arXiv:1812.05189, or closely related scalable optimal-transport methods,
reduce the dense OT bottleneck in LEDH-PFPF-OT for large state dimension and
large particle count without changing the filtering question being solved?

## Mechanism being tested
Literature-only design screen for replacing or approximating the dense
particle-to-particle OT solve.  Candidate mechanisms include low-rank/Nyström
Sinkhorn, screened or multiscale Sinkhorn, stochastic/minibatch OT, sliced or
projection OT, and filtering-specific ensemble transform variants.

## Scope
- Variant: no code change; source and literature audit only.
- Objective: identify whether each method plausibly preserves the LEDH-PFPF-OT
  role of moving weighted particles to an approximately equally weighted
  particle cloud.
- Seed(s): N/A.
- Training steps: N/A.
- HMC/MCMC settings: N/A.
- XLA/JIT mode: N/A.
- Expected runtime: under one hour, dominated by reading and citation checks.

## Success criteria
- The target paper is downloaded into `.localsource`.
- The conclusion distinguishes direct drop-in candidates from research
  prototypes and from methods useful only as baselines or diagnostics.
- Any recommendation states scaling benefit, filtering risk, implementation
  fit with TensorFlow/TensorFlow Probability, and evidence gaps.

## Diagnostics
Primary:
- Does the method reduce dense `N x N` memory or cubic/superlinear solve cost?
- Does it handle weighted empirical measures with squared-Euclidean-like costs?
- Does it produce a usable barycentric map or coupling for particle transport?
- Is the method compatible with high-dimensional filtering geometry?

Secondary:
- Availability of algorithmic detail sufficient for TensorFlow implementation.
- Numerical stability and bias controls such as entropic regularization,
  truncation error, or approximation rank.

Sanity checks:
- Do not treat demo-scale benchmarks as proof of filtering validity.
- Do not infer posterior correctness from transport approximation alone.

## Expected failure modes
- A method approximates only the scalar Sinkhorn divergence, not the coupling or
  barycentric transport needed by LEDH-PFPF-OT.
- Low-rank assumptions fail in high dimension unless the post-flow particle
  clouds lie near low-dimensional structure.
- Entropic bias, minibatch bias, or sliced-projection bias changes the particle
  filter behavior enough that downstream validation is required.
- GPU-friendly speedups still require dense `N x N` costs and therefore do not
  solve memory scaling.

## What would change our mind
- A source provides a coupling/barycentric map with provable or empirically
  stable filtering performance at large `d,N`.
- A small TensorFlow prototype shows close agreement with dense OT on existing
  LEDH-PFPF-OT fixtures while reducing peak memory.
- Filtering diagnostics show downstream posterior/reference agreement, not only
  lower OT runtime.

## Command
```bash
mkdir -p .localsource
wget -c -P .localsource https://arxiv.org/pdf/1812.05189
```

## Interpretation rule
- If a method only approximates an OT value/divergence, classify it as useful
  for diagnostics or training losses, not as a direct LEDH-PFPF-OT transport
  replacement.
- If a method yields an approximate coupling/barycentric map but changes the
  filter distribution, classify it as an optional experimental lane requiring a
  dense-OT parity ladder and posterior validation.
- If a method lowers memory below dense `N x N` while preserving a transport map,
  classify it as the highest-priority prototype candidate.

## Skeptical plan audit
Passed on 2026-06-16.  The baseline is the dense particle OT solve used by
LEDH-PFPF-OT, not a generic OT benchmark.  Promotion is not based on paper speed
claims alone: a candidate must plausibly return the transport object needed by
the filter, and later implementation would still need dense-OT parity and
downstream filtering validation.  Stale context is mitigated by checking current
source pages and primary papers before concluding.
