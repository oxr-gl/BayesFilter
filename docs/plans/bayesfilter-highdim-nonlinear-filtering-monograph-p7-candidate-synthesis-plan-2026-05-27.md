# P7 Candidate Ranking and Industrial Synthesis Plan

## Question

How should BayesFilter rank and synthesize candidate methods for industrial
high-dimensional nonlinear SSMs with NAWM-style degeneracy?

## Evidence Contract

Baseline:

- P1-P6 literature and derivation outputs.
- BayesFilter V1 nonlinear evidence.

Primary criterion:

- A candidate table ranks at least eight method families by scaling, required
  structure, failure modes, degeneracy behavior, XLA/GPU readiness, BayesFilter
  implementation burden, evidence needed, and NAWM suitability.

Veto diagnostics:

- Candidate ranking hides evidence burden.
- A fast but invalid method is ranked above a slower but diagnosable method
  without stating that the ranking is research-directional.
- Synthesis claims production readiness.

Explanatory diagnostics:

- Hybrid designs such as block IEKF plus transport proposals plus NeuTra/HNN
  HMC.

Non-implications:

- Passing P7 does not select a default backend.

Artifact:

- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`

## Exit Label

`P7_SYNTHESIS_ACCEPTED` if the ranking is explicit and conservative.
