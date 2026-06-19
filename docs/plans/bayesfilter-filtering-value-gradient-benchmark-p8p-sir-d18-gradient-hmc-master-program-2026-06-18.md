# P8p Master Program: Parameterized SIR d18 DPF Gradient And HMC-Mechanics Readiness

Date: 2026-06-18

Status: `BLOCKED_AT_PHASE3_AD_FD_RESIDUAL`

## Scope

P8p is the gated follow-on to the closed SIR d18 value-only DPF work.  It tests
whether the current batched TensorFlow/GPU LEDH-PFPF-OT route can support an
explicit parameterized SIR d18 diagnostic target with usable gradients for HMC
mechanics.

This lane is DPF/SIR d18 only.  It is not the Zhao-Cui fixed-branch/TT/SIRT
lane and not the monograph rewrite lane.

Inherited value-only entry condition:

- row ID: `zhao_cui_spatial_sir_austria_j9_T20`;
- route: batched TF32/GPU streaming LEDH-PFPF-OT with relaxed Sinkhorn OT;
- selected value-only particle count: `N=10000`;
- adjacent checked count: `N=50000`;
- value-only evidence artifact:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-sir-d18-dpf-particle-adequacy-leaderboard-result-2026-06-18.md`;
- P8o result status: `PASS_SELECT_N10000_FOR_VALUE_ONLY_SIR_D18_DPF_CELL`.

The original SIR d18 leaderboard row is fixed-parameter.  P8p therefore creates
and tests a separate diagnostic parameterized target.  P8p must not rewrite the
meaning of the fixed-parameter leaderboard cell.

## Diagnostic Target Boundary

Default P8p theta, subject to Phase 0/1 review:

```text
theta = [
  log_kappa_scale,
  log_nu_scale,
  log_obs_noise_scale
]
```

At theta zero, this target recovers the current fixed SIR d18 base settings:

- `kappa = base_kappa * exp(log_kappa_scale)`;
- `nu = base_nu * exp(log_nu_scale)`;
- `observation_covariance = base_observation_covariance * exp(2 * log_obs_noise_scale)`.

The target must use:

- fixed P8 SIR observations;
- fixed initial particles and fixed process-noise streams under common random
  numbers;
- differentiable relaxed Sinkhorn/Corenflos-style OT transport;
- no stochastic categorical resampling inside the theta target;
- TensorFlow/TensorFlow Probability implementation paths for differentiable
  BayesFilter-owned code;
- trusted/escalated GPU context for GPU/CUDA/TensorFlow GPU runs.

Gradient connectivity caveat:

- the existing streaming helper
  `streaming_batched_ledh_pfpf_ot_value_and_score_tf` uses zero fill for
  unconnected gradients, so P8p must not rely on that helper alone to certify
  connectivity;
- Phase 2 must add an explicit connectivity diagnostic that watches theta
  components separately or otherwise proves each declared theta component
  affects the objective before any "connected gradient" gate can pass;
- a zero component is a blocker unless Phase 2/3 provides a reviewed
  structural explanation and a finite-difference sensitivity diagnostic for
  that same component.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the current batched streaming LEDH-PFPF-OT SIR d18 route support finite, connected, repeatable gradients on an explicit fixed-randomness diagnostic theta target, and then pass a tiny HMC mechanics smoke without overstating posterior validity? |
| Baseline/comparator | P8o fixed-parameter value-only SIR d18 route for entry and shape/runtime provenance; same fixed-randomness target under central finite differences for local diagnostic comparison; small precision/chunk variants for stability. |
| Primary pass criterion | Each phase either passes its declared gate with artifacts and review, or writes a blocker.  Final P8p pass requires finite connected repeatable AD gradients, a reviewed finite-difference diagnostic on the same fixed-randomness target, a trusted GPU full-horizon gradient probe, stability checks that do not trigger vetoes, and a tiny HMC mechanics smoke that emits finite states/energies under the diagnostic target. |
| Veto diagnostics | Nonfinite value or gradient; disconnected or `None` gradient; zero-gradient result without a reviewed structural explanation; stochastic categorical resampling in the theta target; randomness changing between theta evaluations; GPU claims without trusted context; finite-difference residuals treated as proof of stochastic PF marginal-gradient correctness; changing pass/fail criteria after seeing results; posterior convergence, NUTS readiness, production/default, exact likelihood, or Zhao-Cui TT/SIRT claims. |
| Explanatory diagnostics | Gradient norms, finite-difference residuals, seed-to-seed variability, chunk/precision deltas, Sinkhorn residuals, ESS, runtime, GPU memory, HMC acceptance, and tiny-chain traces. |
| Not concluded | Stochastic PF marginal-gradient correctness, exact nonlinear likelihood correctness, posterior convergence, NUTS readiness, tuned HMC readiness, production/default readiness, Zhao-Cui TT/SIRT parity, MATLAB parity, filter ranking, or cross-model default policy. |
| Artifacts | P8p master program, phase subplans/results, visible runbook, execution ledger, Claude review ledger, JSON/CSV diagnostics, and final stop handoff/reset memo. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and target boundary | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase0-governance-target-boundary-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase0-governance-target-boundary-result-2026-06-18.md` |
| 1 | Parameterized SIR objective contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase1-parameterized-sir-objective-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase1-parameterized-sir-objective-result-2026-06-18.md` |
| 2 | Fixed-randomness gradient smoke implementation | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-result-2026-06-18.md` |
| 3 | Central finite-difference validation | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3-finite-difference-validation-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3-finite-difference-validation-result-2026-06-18.md` |
| 4 | Full-horizon SIR d18 gradient probe | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase4-full-horizon-gradient-probe-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase4-full-horizon-gradient-probe-result-2026-06-18.md` |
| 5 | Chunk and precision stability | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase5-chunk-precision-stability-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase5-chunk-precision-stability-result-2026-06-18.md` |
| 6 | Multi-seed gradient stability and particle ladder | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase6-multiseed-gradient-ladder-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase6-multiseed-gradient-ladder-result-2026-06-18.md` |
| 7 | Tiny HMC mechanics smoke | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase7-hmc-mechanics-smoke-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase7-hmc-mechanics-smoke-result-2026-06-18.md` |
| 8 | Closeout and reset memo | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase8-closeout-reset-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase8-closeout-reset-result-2026-06-18.md` |

## Required Phase Protocol

For each phase:

1. create or refresh the dedicated subplan before execution;
2. run the required local checks;
3. write a phase result or blocker record;
4. draft or refresh the next phase subplan;
5. review the next subplan, material implementation diff, and material result
   for consistency, correctness, feasibility, artifact coverage, and boundary
   safety.

Each subplan must state:

- phase objective;
- entry conditions inherited from the previous phase;
- required artifacts;
- required checks/tests/reviews;
- evidence contract;
- forbidden claims/actions;
- exact next-phase handoff conditions;
- stop conditions.

Claude Opus/max effort may be used only as a read-only reviewer.  Claude is not
an execution authority and cannot authorize crossing human, runtime,
model-file, funding, product-capability, GPU, or scientific-claim boundaries.

If review finds a fixable issue, patch the same subplan or artifact visibly and
rerun focused checks.  Loop Claude review only for material issues, stopping
after five rounds for the same blocker.  Use path-bounded prompts and concise
excerpts rather than sending whole large artifacts.

## Global Stop Conditions

- A phase would require package installation, network fetch, credential, or
  destructive filesystem/git action not already approved.
- A GPU/CUDA/TensorFlow GPU command would run without trusted/escalated context.
- Claude/Codex review fails to converge after five rounds for the same blocker.
- A result would need changed pass/fail criteria after seeing outcomes.
- A phase would mutate unrelated Zhao-Cui fixed-branch, monograph, or user work.
- A phase would claim stochastic PF marginal-gradient correctness, exact
  likelihood correctness, posterior convergence, NUTS readiness, tuned HMC,
  production/default readiness, or filter ranking.
- A phase would treat the current zero-filled score helper as sufficient
  connectivity evidence without an explicit per-theta connectivity diagnostic.
- Runtime projection from a smaller gate shows that the next longer run would
  exceed the declared budget; write a blocker instead of forcing the run.

## Anticipated Approvals

The program anticipates these approvals for smooth execution:

- trusted/escalated TensorFlow GPU commands for phases 2, 4, 5, 6, and 7;
- trusted/escalated Claude Code worker calls for read-only review;
- writing P8p plan/result/JSON/CSV artifacts under `docs/plans`;
- scoped code changes only after Phase 1/2 identifies exact implementation
  files and local checks.

No network fetch, package installation, destructive git action, copied
workspace, or detached supervisor is included in this master program.
