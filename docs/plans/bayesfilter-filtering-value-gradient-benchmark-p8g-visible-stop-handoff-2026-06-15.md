# P8g Visible Stop Handoff

Date: 2026-06-15

Status: `BLOCK_DPF_PARTICLE_TUNING_RELATIVE_ESS_REVIEWED_READY_FOR_G4B_EXECUTION_GATE`

## Stop Point

Date: 2026-06-15

Stopped after trusted G4 GPU Stage 0 particle-tuning execution, G4 result
review, and reviewed G4b repair-subplan drafting. No G4b execution has
launched.

Prior reviewed blocker:

- `BLOCK_P8G_VECTORIZE_ALG1_SPEED_FEASIBILITY_REVIEWED`

Prior blocker artifact:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-result-2026-06-15.md`

Reviewed repair artifact:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-repair-result-2026-06-15.md`

Reviewed G3 artifact:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-result-2026-06-15.md`

## Reason

G2 added an opt-in `tf.vectorized_map` particle route that preserves parity and
uses GPU tensors, but it did not meet the G1/G2 speed feasibility gate.

G2 evidence:

- GPU vectorized route matches looped GPU value on the smoke profile.
- GPU tensor placement is real; no silent CPU fallback was observed.
- GPU vectorized speedup over looped GPU is only about `1.79x`.
- Required handoff gate is at least `5x` speedup or a reviewed feasible
  exception, tied to the G1 `30` minute projected full-horizon budget.

G2b reviewed repair evidence:

- Added distinct scalar-SV graph route `p8g_sv_scalar_graph`.
- CPU/reference parity and GPU placement passed.
- Tiny T10/1seed cold-compile speedup is only about `2.89x`, an explanatory
  caveat.
- T50/5seed feasibility-scale GPU diagnostic is about `10.62x` faster than the
  G1 looped GPU profile and linearly projects to about `10.63` minutes for a
  T1000/5seed N=32 run.
- Claude result review returned `VERDICT: AGREE` with no material blocker.

G3 reviewed evidence:

- Fixed-randomness/no-resampling gradients for actual scalar SV are finite and
  repeatable in `canonical_unconstrained` coordinate.
- CPU/GPU values and gradients match to floating precision for the small G3
  diagnostic scope.
- This is not stochastic PF marginal-gradient, HMC-readiness, tuned-particle,
  generalized-SV, or high-dimensional evidence.

G4 subplan review and execution evidence:

- User authorized five extra focused G4 review rounds.
- Extra review round 2 returned `VERDICT: AGREE`.
- G4 tuning CLI/test surfaces were implemented and focused local checks passed.
- Trusted GPU Stage 0 ran on actual-SV LEDH scalar graph with horizons
  `50,200`, particles `16,32`, and five fixed seeds.
- Stage 0 was finite and within runtime budget, but every probed rung failed
  the relative-ESS gate. The best min relative ESS was about `0.0735`, below
  the `0.25` gate.
- Current result artifact:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-result-2026-06-15.md`.
- Claude result review returned `VERDICT: AGREE`.
- Draft next repair subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4b-ess-repair-subplan-2026-06-15.md`.
- Claude G4b subplan review returned `VERDICT: AGREE`.

## Boundary

Do not run:

- G4 particle-count tuning;
- G6 HMC diagnostics;
- any full-horizon serious GPU/tuning run based on the current G2/G2b route
  before the G4 result is reviewed and a repair subplan is drafted/reviewed.

## Safe Next Action

Execute G4b only through the reviewed subplan. Start with local checks and the
smallest discriminating repair diagnostic: scalar-SV state/covariance
resampling route if implementable without crossing gradient boundaries, or the
bounded larger no-resampling ladder if resampling is blocked/deferred.

## Current State

G0, G1, G2, G2b, G3, and G4 have produced reviewed artifacts. G4 Stage 0 GPU
particle tuning has run and produced a reviewed relative-ESS blocker. G4b is a
reviewed subplan only; no G4b code/GPU run has launched.

## P8h Supersession Note

P8h supersedes P8g as the active serious DPF/LEDH value, gradient, GPU, and
HMC-diagnostic lane. P8g no-resampling/fixed-randomness artifacts remain
historical graph, kernel, shape, runtime, and gradient-plumbing diagnostics.
They must not be used as evidence that the serious DPF route is filter-ready,
gradient-correct for stochastic PF, or HMC-ready. The active serious candidate
is Li--Coates Algorithm 1 UKF LEDH with PF-PF correction and declared
Corenflos-style OT/Sinkhorn or annealed-transport resampling, subject to the P8h
phase gates.

## Launch Boundary

Before any further G4 repair/tuning/HMC launch, G4b required local checks must
pass and any GPU diagnostic must follow the reviewed G4b command/artifact
contract.

## Known Required Approvals Before Execution

- Any further trusted GPU repair ladder only after a reviewed repair subplan.

## Unresolved Blockers

- `BLOCK_DPF_PARTICLE_TUNING_RELATIVE_ESS_REVIEWED`

## What Is Not Concluded

- No selected/tuned G4 particle count.
- No HMC diagnostic compatibility.
