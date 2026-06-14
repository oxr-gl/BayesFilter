# BayesFilter Fixed-Trajectory HMC Tuning Master Plan

Date: 2026-06-12

## Status

`PRE_REVIEW_PLAN`

This file is a plan only. It authorizes no implementation until Claude review
returns `PROCEED` or the plan is revised after `NEEDS_REVISION`.

## Runtime Classification

- Core runtime class: `accepted TF/TFP runtime`.
- Tuning architecture: fixed-trajectory Hamiltonian Monte Carlo with explicit
  step size, leapfrog count, trajectory length, and mass/preconditioner policy.
- Forbidden substitute: TFP NUTS is demoted to reference/diagnostic only. NUTS
  must not be used as the default sampler, production remedy, tuning fallback,
  or evidence that fixed-trajectory HMC is tuned.
- Existing BayesFilter labels to preserve:
  `fixed_kernel_screen`, `dual_averaging_step_size`,
  `fixed_mass_dual_averaging`, `windowed_mass_adaptation_future`, and
  `manual_ladder_diagnostic`.
- Existing fail-closed behavior to preserve: raw or unsupported adaptation
  labels fail closed; future/windowed mass adaptation remains non-executable
  unless a later reviewed plan implements it; invalid target evaluations are
  not tuning successes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter add a complete fixed-trajectory HMC tuning procedure that chooses step size, leapfrog count or trajectory length, and mass/preconditioner policy while preserving fail-closed policy labels and demoting NUTS to diagnostic-only reference status? |
| Baseline/comparator | Current BayesFilter fixed-kernel HMC policy layer and diagnostics, especially `fixed_kernel_screen`, reviewed fixed-mass dual averaging metadata, precomputed mass artifacts, target failure policy labels, and full-chain HMC fail-closed authority checks. |
| Primary pass criterion | A reviewed design and first implementation slice expose a deterministic fixed-trajectory tuning ladder with structured artifacts for step-size bracket/search, leapfrog-count or trajectory-length selection, and mass/preconditioner policy selection, without making NUTS default, adaptive, or production. |
| Acceptance promotion band | Where HMC tuning uses acceptance as a promotion screen, the promotion band is 0.65 to 0.75. Values outside the band can reject a candidate tuning point but do not by themselves reject the target or scientific direction. |
| Veto diagnostics | Non-finite value/gradient, target failure branch treated as success, divergences if available, invalid mass/preconditioner artifact, covariance not positive definite, unstable energy error, unsupported policy label accepted, NUTS selected as default or remedy, missing artifact manifest, or any convergence/superiority/default-readiness claim from short tuning runs. |
| Explanatory diagnostics | Acceptance rate, log accept ratio summaries, energy error summaries, final step size, leapfrog count, trajectory length, runtime, gradient evaluations, finite sample count, branch labels, mass eigen summaries, and per-stage candidate tables. |
| Nonclaims | Passing this plan does not prove posterior convergence, sampler superiority, production readiness, GPU/XLA readiness, MacroFinance default readiness, large-scale CIP readiness, or correctness of any target model. |
| Artifact | This plan, Claude review note, implementation result note, JSON tuning artifacts under a later reviewed path, and focused tests named by the implementation slice. |

## Skeptical Audit Before Execution

- Wrong baseline risk: The baseline is current fixed-trajectory BayesFilter HMC
  and policy metadata, not TFP NUTS, old NUTS Gaussian benchmarks, or an
  external adaptive sampler.
- Proxy metric risk: Acceptance in 0.65 to 0.75 is a tuning screen, not a
  convergence proof. ESS, R-hat, validation loss, and runtime from short runs
  are explanatory unless a later plan promotes them with uncertainty evidence.
- Missing stop condition risk: Stop the implementation if unsupported labels
  execute, NUTS becomes default, invalid target branches are counted as
  successful tuning points, or artifacts omit policy/nonclaim metadata.
- Unfair comparison risk: NUTS may appear in documentation only as a
  reference/diagnostic comparator. It cannot be compared as a production
  alternative unless a separate method-comparison plan defines uncertainty
  evidence and default-readiness gates.
- Hidden assumption risk: Step-size adaptation tunes only step size. It does
  not imply mass adaptation. Fixed mass, diagonal mass, dense precomputed mass,
  and future windowed mass policies must be labeled separately.
- Stale context risk: BayesFilter has dirty worktree changes. This plan must
  not overwrite or normalize unrelated files.
- Environment mismatch risk: CPU-only checks should hide GPUs before TF import;
  GPU/XLA claims require a separate trusted GPU context and exact-path evidence.
- Artifact relevance risk: The first slice must produce a small artifact that
  answers fixed-trajectory tuning plumbing, not a long posterior-quality claim.

Audit result: the plan is executable only after Claude review because it
separates fixed-trajectory HMC tuning from NUTS, keeps promotion and veto
diagnostics distinct, names stop conditions, and requires artifacts that answer
the stated engineering question.

Isolation repair note, 2026-06-12: the first implementation slice initially
touched the shared `bayesfilter.inference.hmc_tuning` export surface. That was a
material integration flaw because another agent may depend on the legacy API.
The repaired first slice must keep the new tuner in an explicit v2 module and
must not re-export it from `bayesfilter.inference` or top-level `bayesfilter`.

## Research Intent Ledger

| Item | Ledger |
| --- | --- |
| Main question | Build BayesFilter-owned fixed-trajectory HMC tuning, not NUTS, with fail-closed policy labels and auditable tuning artifacts. |
| Candidate/mechanism | Multistage fixed-trajectory tuning over step size, leapfrog count or trajectory length, and mass/preconditioner policy. |
| Expected failure mode | Acceptance outside 0.65 to 0.75, non-finite target/gradient, invalid mass artifact, energy instability, or too-short trajectory geometry for the target. |
| Promotion criterion | Candidate fixed-trajectory configuration passes target finite checks, mass/preconditioner validation, acceptance screen 0.65 to 0.75 where used, and artifact completeness checks. |
| Promotion veto | Any hard veto diagnostic above, missing artifact provenance, or policy/nonclaim drift. |
| Continuation veto | Broken target contract, corrupted artifact, missing required diagnostics, implementation path requiring NUTS as remedy, or unsupported policy executing silently. |
| Repair trigger | Acceptance too low or high, energy error unstable, mass artifact invalid, branch failures, step-size bracket failure, or trajectory selection indeterminate. |
| Explanatory diagnostics | Candidate tables, energy/log-accept summaries, acceptance, runtime, gradient evaluations, branch labels, and mass eigen summaries. |
| Must not conclude | Do not conclude convergence, posterior accuracy, sampler superiority, production readiness, or MacroFinance default readiness. |

## Fixed-Trajectory HMC Architecture

1. Policy layer:
   Keep `HMCTuningPolicy` as the authority boundary. Add no raw-string adaptive
   escape hatch. `fixed_kernel_screen` remains the default. Reviewed tuning
   policies must serialize label, source, enabled/implemented status,
   diagnostic role, nonclaims, and pass/fail status.

2. Tuning plan object:
   Add a future `FixedTrajectoryHMCTuningPlan` or equivalent structured object
   carrying target identity, seed policy, initial position policy, candidate
   step sizes, candidate leapfrog counts or trajectory lengths, mass policy,
   pass/fail thresholds, artifact path, and nonclaims.

3. Mass/preconditioner policy:
   Support explicit policies, initially `identity`, `diagonal_from_scale`,
   and `precomputed_dense_mass_artifact` if the existing artifact validates.
   Future `windowed_mass_adaptation_future` remains named but non-executable.
   Mass policy must report eigen summaries, provenance, position role, adapter
   signature, and whether the artifact is fixed or estimated.

4. Step-size search:
   Use a bounded bracket and refinement ladder for fixed trajectory HMC.
   Optional reviewed `dual_averaging_step_size` or
   `fixed_mass_dual_averaging` may nominate a step size only for fixed mass;
   it does not choose mass and does not authorize NUTS.

5. Trajectory selection:
   Choose leapfrog count or trajectory length from a finite candidate set.
   Selection should balance acceptance screen, energy stability, finite target
   behavior, and movement diagnostics. It must not rely on NUTS tree depth or
   No-U-Turn termination.

6. Result classifier:
   Emit structured candidate outcomes: `passed_screen`, `rejected_accept_low`,
   `rejected_accept_high`, `rejected_nonfinite_target`,
   `rejected_invalid_mass`, `rejected_energy_instability`,
   `blocked_missing_diagnostics`, or `blocked_policy_violation`.

7. Artifacts:
   Write JSON or JSONL artifacts with command, git commit, environment,
   CPU/GPU policy, seed, target metadata, policy labels, candidate grid,
   diagnostics, selected candidate, vetoes, nonclaims, and elapsed time.

## Multistage Tuning Procedure

### Stage 0: Preflight

- Validate target value/score contract and target failure policy.
- Validate seed policy, initial position policy, shape/dtype stability, and
  finite value/gradient at the starting point.
- Validate mass/preconditioner candidates before any HMC transition.
- Fail closed if the target is invalid, the mass artifact is invalid, a policy
  label is unsupported, or the requested policy is NUTS.

### Stage 1: Step-Size Bracket

- Run short fixed-trajectory probes with fixed leapfrog count, fixed mass, and
  candidate step sizes.
- Use acceptance as a screen only; the promotion band is 0.65 to 0.75 where
  used for HMC tuning.
- Reject step sizes with non-finite values, invalid branch labels, severe
  energy instability, or acceptance outside the configured screen.
- If no candidate passes, record a repair trigger rather than falling back to
  NUTS.

### Stage 2: Leapfrog Count or Trajectory Length

- For viable step sizes, evaluate a finite set of leapfrog counts or total
  trajectory lengths.
- Prefer stable fixed trajectories that remain in the 0.65 to 0.75 acceptance
  band where used, maintain finite diagnostics, and provide non-degenerate
  movement.
- Reject candidates with finite-target vetoes or energy/log-accept pathologies.
- Do not use NUTS tree depth, U-turn detection, or dynamic path length.

### Stage 3: Mass/Preconditioner Policy

- Compare identity, diagonal, and reviewed precomputed dense mass policies only
  when each artifact is valid and provenance is complete.
- Treat mass comparisons as screen outcomes unless a later plan defines
  replicated uncertainty evidence.
- A precomputed mass artifact may be selected only if adapter signature,
  position role, covariance source, positive definiteness, factor orientation,
  and nonclaims validate.

### Stage 4: Confirmation Screen

- Rerun the selected fixed-trajectory configuration with a held-out seed or
  repeated short diagnostic.
- Require artifact reproducibility, finite target/gradient diagnostics, no
  policy drift, and acceptance in 0.65 to 0.75 where the screen is active.
- A pass means "fixed-trajectory HMC tuning candidate selected"; it does not
  mean posterior convergence or production readiness.

## Pass/Fail Criteria

Pass:

- NUTS remains reference/diagnostic only and is absent from default or remedy
  paths.
- Fixed-trajectory HMC tuning selects explicit step size, leapfrog count or
  trajectory length, and mass/preconditioner policy.
- Acceptance-based promotion, where used, requires 0.65 to 0.75.
- All hard vetoes are evaluated before descriptive metrics.
- Artifacts include policy labels, fail-closed outcomes, nonclaims, and command
  provenance.
- Tests verify unsupported labels, NUTS requests, invalid mass artifacts, and
  invalid target branches fail closed.

Fail:

- NUTS is used as default, production remedy, or implicit tuning fallback.
- Any unsupported adaptive policy executes.
- Target fallback/non-finite branches are counted as tuning success.
- Acceptance outside 0.65 to 0.75 is promoted where the acceptance screen is
  active.
- Result text claims convergence, sampler superiority, or default readiness.
- Artifact metadata is missing enough provenance that the selected candidate
  cannot be audited.

## Diagnostics Classification

| Diagnostic | Role |
| --- | --- |
| Non-finite value/gradient | Promotion veto and continuation veto if target contract is broken |
| Target branch label | Promotion veto when fallback/invalid branch is used |
| Unsupported policy label | Continuation veto |
| NUTS request | Continuation veto for this tuning path |
| Acceptance rate | Promotion screen only, with 0.65 to 0.75 where used |
| Energy error/log accept summaries | Promotion veto if unstable; otherwise explanatory |
| Step size | Selected parameter and explanatory diagnostic |
| Leapfrog count/trajectory length | Selected parameter and explanatory diagnostic |
| Mass eigen summary | Promotion veto for invalid mass; otherwise explanatory |
| Runtime and gradient evaluations | Explanatory diagnostic |
| ESS/R-hat from short tuning probes | Explanatory only unless a later plan promotes them |

## Implementation Blocks

1. Review and plan gate:
   Submit this file to Claude read-only review. Do not edit code until review
   returns `PROCEED`.

2. Policy and schema block:
   Add fixed-trajectory tuning plan/result dataclasses, strict labels, NUTS
   rejection, artifact schema, and result classifier. Preserve current
   `HMCTuningPolicy` labels and fail-closed raw-string behavior.

3. Target/mass validation block:
   Reuse target failure policy and precomputed mass artifact validation.
   Add explicit mass/preconditioner validation result payloads.

4. Step-size block:
   Implement bounded fixed-trajectory step-size bracket and refinement for a
   tiny Gaussian or existing deterministic fixture.

5. Trajectory block:
   Implement finite candidate selection for leapfrog count or trajectory
   length. No NUTS tree logic.

6. Mass policy block:
   Implement identity and diagonal policies first. Add precomputed dense mass
   only when existing artifact validation can be reused without broad refactor.

7. Artifact and tests block:
   Write focused tests for fail-closed labels, NUTS demotion, invalid target,
   invalid mass, acceptance band enforcement, and artifact completeness.

8. Result note block:
   Record command, environment, elapsed time, artifact paths, pass/fail table,
   inference-status table, hard vetoes, viable candidates, statistical ranking
   status, descriptive-only differences, and next evidence needed.

## Minimal First Implementation Slice After Claude Review

The smallest executable slice should avoid model-specific complexity and prove
only the fixed-trajectory tuning plumbing:

1. Add a tiny Gaussian fixed-trajectory tuning fixture using existing TFP HMC,
   not NUTS.
2. Add a plan/result schema with fields for policy label, step size,
   leapfrog count, trajectory length, mass policy, acceptance band 0.65 to
   0.75, diagnostics, vetoes, and nonclaims.
3. Implement identity-mass step-size and leapfrog-count grid evaluation on the
   fixture.
4. Reject any request for NUTS with a fail-closed error that says NUTS is
   reference/diagnostic only.
5. Emit one small JSON artifact under a reviewed artifact path.
6. Add focused tests:
   NUTS request fails closed; unsupported policy fails closed; invalid target
   branch fails closed; selected candidate records step size, leapfrog count,
   mass policy, and acceptance band; no payload claims convergence,
   superiority, default readiness, production readiness, or NUTS promotion.

This first slice is enough for immediate execution after Claude review because
it exercises the policy boundary and fixed-trajectory selection mechanics
without touching MacroFinance defaults, large models, GPU/XLA, or mass
adaptation.

## Claude Review Request

Ask Claude for read-only review of this file only. Required review questions:

- Does the plan fully demote TFP NUTS to reference/diagnostic only?
- Is the architecture fixed-trajectory HMC rather than NUTS?
- Are step size, leapfrog count/trajectory length, and mass/preconditioner
  policy all selected by the procedure?
- Are acceptance promotion semantics fixed at 0.65 to 0.75 where used?
- Are current BayesFilter labels and fail-closed behavior preserved?
- Is the minimal first slice small enough to implement immediately after
  review without making posterior convergence, default-readiness, or production
  claims?
