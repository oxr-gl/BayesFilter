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
- For scholarly readiness, every ranking entry must cite the supporting
  chapter evidence, source-support class, BayesFilter evidence or blocker,
  downstream validation burden, and the reason the ranking is not a performance
  or posterior-accuracy leaderboard.

Veto diagnostics:

- Candidate ranking hides evidence burden.
- A fast but invalid method is ranked above a slower but diagnosable method
  without stating that the ranking is research-directional.
- Synthesis claims production readiness.
- Ranking relies on intuition without linking to P1-P6 evidence, source gaps,
  or BayesFilter diagnostics.
- The ranking omits what would overturn it.

Explanatory diagnostics:

- Hybrid designs such as block IEKF plus transport proposals plus NeuTra/HNN
  HMC.

Non-implications:

- Passing P7 does not select a default backend.

Artifact:

- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`

## Exit Label

`P7_SYNTHESIS_ACCEPTED` if the ranking is explicit and conservative.

`P7_SCHOLARLY_SYNTHESIS_ACCEPTED` only if the ranking reads as a defended
research-prior with evidence burden, not as an unsupported opinion table.
