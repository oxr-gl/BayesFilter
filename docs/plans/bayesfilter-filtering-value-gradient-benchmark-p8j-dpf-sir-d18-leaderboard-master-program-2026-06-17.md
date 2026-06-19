# P8j Master Program: DPF SIR d18 Leaderboard Completion

Date: 2026-06-17

Status: `DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

## Scope

P8j is the gated follow-on for the missing DPF leaderboard cells on the
Zhao-Cui spatial SIR d18 row:

`zhao_cui_spatial_sir_austria_j9_T20`

This lane closes the missing SIR d18 DPF route preserved by the P8d reset memo,
the current P8d runner, and the current route tests.  P8g/P8h/P8i are historical
provenance only for the repaired DPF/LEDH/OT mechanics and scalar-SV evidence;
they are not SIR d18 evidence owners.

P8j is not the Zhao-Cui fixed-branch/P71 lane and not the monograph rewrite
lane.  Zhao-Cui fixed TT/SIRT source-faithfulness, rank-selection, and adaptive
MATLAB parity remain out of scope.

## Target Boundary

The current source-paper SIR row is fixed-parameter:

- row ID: `zhao_cui_spatial_sir_austria_j9_T20`;
- horizon: `T=20`;
- state dimension: `18`, with `(S_j, I_j)` for `j=1..9`;
- observation dimension: `9`, infectious components only;
- rates are fixed in the benchmark row;
- no free theta exists in this row.

Therefore P8j may report value/log-likelihood, finite status, ESS, MC standard
error, runtime, DPF seed evidence, and blocker status.  Score, Hessian,
theta-gradient, HMC, NUTS, and posterior-sampling claims are forbidden unless a
new parameterized SIR row is separately proposed and explicitly approved by the
user.

## Inherited Route

The serious DPF route inherited from P8h is:

`Li-Coates Algorithm 1 UKF LEDH + PF-PF correction + Corenflos-style relaxed Sinkhorn OT resampling + same-transport barycentric covariance carry`

Exact inherited identifiers:

- algorithm ID: `ledh_pfpf_alg1_ukf_current`;
- resampling route: `ot_sinkhorn_barycentric_covariance_carry`;
- canonical transport convention: `target_by_source_row_stochastic`;
- bootstrap comparator algorithm ID: `bootstrap_dpf_current`;
- seed contract: five fixed seeds, default set `81120,81121,81122,81123,81124`;
- GPU evidence must use trusted/escalated context.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter complete the missing DPF leaderboard cells for Zhao-Cui spatial SIR d18 without overclaiming source-faithfulness, theta gradients, HMC readiness, or production readiness? |
| Baseline/comparator | P8d reset memo, current P8d runner callback contracts and route tests, P8 source-paper scope and adapter matrices, deterministic SIR value-only adapter, and existing DPF routes for LGSSM/SV/predator-prey/generalized-SV.  P8g/P8h/P8i provide historical non-SIR DPF/LEDH/OT provenance only. |
| Primary pass criterion | Every P8j phase either passes its declared gate with artifacts and review, or writes a blocker preserving exact SIR d18 and DPF claim boundaries.  Final leaderboard refresh may pass only if Phase 5 selects a reviewed SIR d18 particle count and Phase 6 executes SIR d18 DPF cells with that count and five fixed seeds; otherwise it must write a reviewed blocker. |
| Veto diagnostics | Treating P8h scalar-SV evidence as SIR evidence; fabricating SIR DPF callbacks without a reviewed contract; claiming Zhao-Cui TT/SIRT source-faithfulness; reporting score/Hessian/theta-gradient/HMC readiness for fixed-parameter SIR; using fewer than five seeds for DPF value evidence; GPU execution outside trusted context; changing model/data definitions after seeing results; Claude used as execution authority. |
| Explanatory diagnostics | ESS, MC SE, per-seed log likelihood, finite flags, runtime, covariance carry diagnostics, transport residuals, bootstrap comparator results, CPU/GPU smoke status, and blocker reason codes. |
| Not concluded | Zhao-Cui source-faithful TT/SIRT parity, exact nonlinear likelihood correctness, stochastic PF marginal-gradient correctness, theta-gradient correctness, posterior convergence, HMC/NUTS readiness, generic high-dimensional LEDH readiness, production readiness, or final default ranking. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and current evidence audit | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase0-governance-current-evidence-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase0-governance-current-evidence-result-2026-06-17.md` |
| 1 | SIR d18 DPF callback contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase1-sir-d18-dpf-callback-contract-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase1-sir-d18-dpf-callback-contract-result-2026-06-17.md` |
| 2 | Bootstrap DPF SIR smoke implementation | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-result-2026-06-17.md` |
| 3 | Algorithm 1 UKF LEDH SIR smoke | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-result-2026-06-17.md` |
| 4 | OT-resampled LEDH-PFPF-OT SIR smoke | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-result-2026-06-17.md` |
| 5 | SIR d18 particle-count tuning | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-result-2026-06-17.md` |
| 6 | SIR d18 leaderboard refresh | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase6-sir-leaderboard-refresh-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase6-sir-leaderboard-refresh-result-2026-06-17.md` |
| 7 | Closeout, artifact index, and repo boundary | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase7-closeout-boundary-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase7-closeout-boundary-result-2026-06-17.md` |

## Required Phase Protocol

For each phase:

1. create or refresh the dedicated subplan before execution;
2. run only the required local checks and reviewed commands;
3. write a phase result or blocker record;
4. draft or refresh the next phase subplan;
5. review the next subplan or material result with Claude when material.

Each subplan must state:

- phase objective;
- entry conditions inherited from the previous phase;
- required artifacts;
- required checks/tests/reviews;
- evidence contract;
- forbidden claims/actions;
- exact next-phase handoff conditions;
- stop conditions.

## Review And Repair Protocol

Claude Opus/max effort may be used only as a read-only reviewer for material
plans, subplans, implementation diffs, and results.  Claude is not an execution
authority and cannot authorize crossing human, runtime, model-file, funding,
product-capability, GPU, or scientific-claim boundaries.

If review finds a fixable issue, patch the same subplan or artifact visibly and
rerun focused checks.  Loop Claude review only for material issues, stopping
after five rounds for the same blocker.  Use path-bounded prompts and concise
excerpts rather than sending whole large artifacts.

If blocked, write a blocker result and explicitly ask for approval or
direction.  If a subplan converges, continue to the next phase.  If it does not
converge, write a blocker result and stop for clarification or human direction.

## Global Stop Conditions

- A phase would require package installation, network fetch, credential, or
  destructive filesystem/git action not already approved.
- A GPU/CUDA/TensorFlow GPU command would run without trusted/escalated context.
- Claude/Codex review fails to converge after five rounds for the same blocker.
- A result would need changed pass/fail criteria after seeing outcomes.
- A phase would mutate unrelated Zhao-Cui fixed-branch, monograph, or user work.
- A phase would claim score/Hessian/theta-gradient/HMC/NUTS evidence for the
  fixed-parameter SIR row.
- A phase would claim Zhao-Cui TT/SIRT source-faithfulness or MATLAB parity from
  DPF callback evidence.
- Runtime projection from a smaller gate shows that the next longer run would
  exceed the declared budget; write a blocker instead of forcing the run.
