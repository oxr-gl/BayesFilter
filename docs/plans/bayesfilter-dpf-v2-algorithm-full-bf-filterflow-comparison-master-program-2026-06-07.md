# DPF V2 Algorithm Full BF/FilterFlow Comparison Master Program

metadata_date: 2026-06-07
status: REVIEWED_READY_FOR_P0_EXECUTION

## Purpose

Create a staged evidence program for full same-contract BayesFilter versus
FilterFlow comparison of two DPF algorithm stacks over the six V2 common-model
rows:

1. bootstrap particle filter with FilterFlow-style OT transport resampling;
2. LEDH-PFPF-OT, meaning LEDH proposal flow, PF-PF proposal correction, and
   FilterFlow-style OT transport resampling.

The program covers both value and fixed-branch AD-gradient comparison. It does
not claim filtering correctness, mathematical correctness of either
implementation, stochastic resampling distribution correctness, or correctness
of gradients through random/discrete branch selection.

## Inputs And Existing Evidence

- Closed V2 common-model suite:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-master-plan-2026-06-07.md`.
- Closed deterministic BF/FilterFlow tie-out:
  `docs/plans/bayesfilter-dpf-bf-filterflow-final-comparison-closeout-and-robustness-result-2026-06-07.md`.
- V2 model source:
  `experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py`.
- BayesFilter experimental bootstrap-OT and LEDH-PFPF-OT components:
  `experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py`,
  `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`,
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.
- Local executable FilterFlow checkout:
  `.localsource/filterflow`.

## V2 Model Rows

All phases must carry the complete V2 row set, in this exact order:

1. `lgssm_2d_h25_rich`
2. `sv_1d_h18_rich`
3. `range_bearing_4d_h20_rich`
4. `structural_ar1_quadratic_h16`
5. `spatial_sir_j3_rk4`
6. `predator_prey_rk4`

No row may silently disappear. A row that cannot be executed must be classified
before result inspection as `ARCHITECTURE_BLOCKED`, `CONTRACT_BLOCKED`,
`SCIENTIFIC_CONTRACT_BLOCKED`, or `INFRASTRUCTURE_BLOCKED`, with a repair plan
or a stop decision. A final `PASS_FULL_COMPARISON` requires every required row
and every required physical-gradient knob to execute and match. A classified
blocker can close only as `BLOCKED_WITH_REVIEWED_CLASSIFICATION`, not as full
comparison success.

## Algorithm Contracts

### Bootstrap-OT

Bootstrap-OT means:

- proposal equals the transition model;
- initial particles, transition innovations, observations, parameters, dtype,
  ESS trigger masks, OT settings, and scalar definition are frozen before
  results;
- OT is FilterFlow `RegularisedTransform` semantics, mirrored by
  BayesFilter's `annealed_transport_tf`;
- gradients include differentiable value-path operations and the deterministic
  OT transform under fixed trigger masks, but exclude gradients through random
  seeds, random initial sampling, random transition sampling, and Boolean
  resampling-trigger decisions.

### LEDH-PFPF-OT

LEDH-PFPF-OT means:

- proposal particles are obtained by applying a local EDH/LEDH affine flow to
  pre-flow transition proposals;
- PF-PF correction uses target transition density, observation density,
  pre-flow proposal density, and the forward log-determinant of the flow;
- FilterFlow side execution is hosted by an adapter in the BayesFilter
  workspace that implements FilterFlow interfaces such as `ProposalModelBase`,
  `TransitionModelBase`, `ObservationModelBase`, and `RegularisedTransform`;
- `.localsource/filterflow` must not be mutated;
- gradients include the fixed-branch LEDH flow, PF-PF correction, and
  deterministic OT transform under fixed trigger masks, but exclude gradients
  through random/discrete branch selection.

## Evidence Contract

Scientific/engineering question:

Can BayesFilter and executable local FilterFlow-side adapters produce matching
values and fixed-branch AD gradients for bootstrap-OT and LEDH-PFPF-OT on all
six V2 model rows under identical frozen contracts, without treating either
implementation as an oracle?

Comparator:

For each algorithm and V2 row, BayesFilter and FilterFlow execute the same
frozen JSON contract: model parameters, observations, initial particles,
transition/proposal innovations, fixed ESS trigger masks, OT settings, scalar,
gradient knobs, dtype, tolerances, and source checksums.

Primary pass criteria:

1. P0 and P1 establish executable, no-mutation architecture contracts.
2. Bootstrap-OT values match for all six rows within declared tolerance.
3. Bootstrap-OT fixed-branch AD gradients match for all required physical knobs
   within declared tolerance.
4. LEDH-PFPF-OT proposal, PF-PF correction, and OT contracts are frozen and
   audited before value or gradient execution.
5. LEDH-PFPF-OT values match for all six rows within declared tolerance.
6. LEDH-PFPF-OT fixed-branch AD gradients match for all required physical
   knobs within declared tolerance.
7. Every phase writes JSON, markdown, and docs/plans result ledgers with
   primary, veto, and explanatory fields separated.

Veto diagnostics:

- mutation of `.localsource/filterflow`;
- use of student repositories, student metrics, TT, dense quadrature, paper
  tables, or simulated truth as an oracle;
- changed fixtures, branch masks, scalar definitions, tolerances, gradient
  knobs, or OT settings after seeing results without a reviewed amendment;
- finite differences used as a gradient gate;
- nonfinite value, density, transport matrix, PF-PF correction, Jacobian/logdet,
  or AD gradient;
- FilterFlow adapter not mathematically matching the frozen V2 contract;
- BayesFilter adapter not mathematically matching the frozen V2 contract;
- hidden stochastic branch differences;
- full-comparison success declared with any unexecuted required V2 row.

Explanatory-only diagnostics:

- ESS, filtered means/variances, RMSE to simulated or reference paths, runtime,
  FD ladders, FD pass/fail booleans, seed robustness, transport residual sizes,
  and stochastic-run summaries.

Not concluded even if all phases pass:

- no proof that BayesFilter is correct;
- no proof that FilterFlow is correct;
- no proof that LEDH-PFPF-OT or bootstrap-OT is scientifically correct;
- no stochastic resampling distribution correctness claim;
- no gradient-through-random/discrete-branch claim;
- no student implementation claim;
- no TT/SIRT, paper-table, HMC, DSGE, GPU, scalability, deployment, or
  production-readiness claim.

## Skeptical Plan Audit

Wrong-baseline risk: the plan compares BF and FF under frozen contracts only.
It does not promote either side to oracle status.

Proxy-metric risk: ESS, RMSE, runtime, FD diagnostics, and transport residual
sizes cannot promote a row. They can explain or veto only as stated.

Hidden-architecture risk: FilterFlow has native SMC and RegularisedTransform
surfaces but no native LEDH proposal implementation. P5 must therefore certify
a no-mutation FilterFlow-side LEDH proposal adapter before LEDH execution.

Stochastic-branch risk: full stochastic distribution matching is not claimed.
Primary value and gradient evidence must use fixed particles, innovations,
trigger masks, and branches.

Artifact adequacy risk: console output is not evidence. Each phase must write
JSON and markdown artifacts with command manifests, contract checksums, git
status, CPU/GPU status, seeds, dtype, and non-claims.

Audit decision: PASS_TO_CLAUDE_REVIEW. The program is executable as a planning
artifact because it separates bootstrap-OT from LEDH-PFPF-OT, preserves
non-oracle framing, and blocks full-comparison success unless all V2 rows and
required gradients are executed or separately stopped.

## Phases

| Phase | Subplan | Gate |
|---|---|---|
| P0 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-subplan-2026-06-07.md` | governance and artifact contract reviewed |
| P1 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p1-architecture-subplan-2026-06-07.md` | BF/FF adapter architecture frozen |
| P2 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p2-bootstrap-ot-contracts-subplan-2026-06-07.md` | bootstrap-OT contracts frozen for six rows |
| P3 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p3-bootstrap-ot-values-subplan-2026-06-07.md` | bootstrap-OT values matched |
| P4 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p4-bootstrap-ot-gradients-subplan-2026-06-07.md` | bootstrap-OT AD gradients matched |
| P5 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-subplan-2026-06-07.md` | LEDH-PFPF-OT contracts frozen for six rows |
| P6 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p6-ledh-pfpf-ot-values-subplan-2026-06-07.md` | LEDH-PFPF-OT values matched |
| P7 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p7-ledh-pfpf-ot-gradients-subplan-2026-06-07.md` | LEDH-PFPF-OT AD gradients matched |
| P8 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p8-closeout-subplan-2026-06-07.md` | full comparison closeout or reviewed blocker |

Claude review ledger:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-claude-review-ledger-2026-06-07.md`

## Claude Review Rule

Review this master program and all P0--P8 subplans with Claude until PASS or
convergence, or until five total review rounds have run. Patch material blockers
before declaring the program reviewed. Non-blocking notes may be recorded
without patching only if local verification shows they do not change execution
soundness.

## Execution State Machine

Each phase uses:

1. load prior phase artifacts and frozen contracts;
2. run local skeptical phase audit;
3. run implementation/evidence command;
4. write JSON, markdown, and docs/plans result ledger;
5. run Claude result/governance review;
6. continue only on PASS.

On blocker:

1. classify blocker;
2. write repair amendment;
3. review amendment with Claude until PASS or max five rounds;
4. implement only reviewed repair;
5. rerun affected evidence;
6. stop only if the blocker requires human intervention, contract weakening, or
   mutation of `.localsource/filterflow`.
