# Reset Memo: DPF V2 Full Algorithm BF/FilterFlow Comparison

## Date

2026-06-07

## Active Scope

This memo records the current state of the new DPF V2 full algorithm
BayesFilter/FilterFlow comparison lane.

Active master program:
`docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-master-program-2026-06-07.md`.

Claude review ledger:
`docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-claude-review-ledger-2026-06-07.md`.

Status:
`REVIEWED_READY_FOR_VISIBLE_P0_PRECHECK`.

No intended visible comparison phase has been executed for this new lane yet.
The intended route is now the visible in-dialogue runbook:
`docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-visible-gated-execution-runbook-2026-06-08.md`.

An earlier live/detached launch attempt misunderstood the user's intent and
created incidental P0 artifacts before stopping. Those artifacts are historical
context only. They do not count as visible phase completion unless revalidated
through the visible state machine in the current dialogue.

The prior live/detached execution plan is superseded as the active route:
`docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-live-gated-execution-plan-2026-06-07.md`.

## Program Purpose

The program is designed to compare BayesFilter and executable local
FilterFlow-side adapters under the same frozen contracts for:

1. bootstrap particle filter with FilterFlow-style OT transport resampling;
2. LEDH-PFPF-OT, meaning LEDH proposal flow, PF-PF proposal correction, and
   FilterFlow-style OT transport resampling.

The comparison is for both value and fixed-branch AD-gradient agreement across
all six V2 common-model rows.

## Required V2 Rows

Every phase must carry these six rows, in order:

1. `lgssm_2d_h25_rich`
2. `sv_1d_h18_rich`
3. `range_bearing_4d_h20_rich`
4. `structural_ar1_quadratic_h16`
5. `spatial_sir_j3_rk4`
6. `predator_prey_rk4`

Rows cannot silently disappear. Full comparison success requires every required
row and every required physical-gradient knob to execute and match. A reviewed
blocker can close only as `BLOCKED_WITH_REVIEWED_CLASSIFICATION`, not as a full
comparison pass.

## Phase Order

- P0: governance and artifact contract.
- P1: BF/FF adapter architecture.
- P2: bootstrap-OT frozen contracts.
- P3: bootstrap-OT values.
- P4: bootstrap-OT fixed-branch AD gradients.
- P5: LEDH-PFPF-OT frozen contracts.
- P6: LEDH-PFPF-OT values.
- P7: LEDH-PFPF-OT fixed-branch AD gradients.
- P8: closeout or reviewed blocker classification.

Bootstrap-OT and LEDH-PFPF-OT are deliberately split. A LEDH adapter blocker
must not contaminate the simpler bootstrap-OT evidence.

## Claude Review Status

Claude reviewed the master program and P0--P8 subplans in one round.

Verdict:
`PASS`.

Material blockers:
none.

Claude confirmed that the program:

- covers both bootstrap-OT and LEDH-PFPF-OT;
- requires all six V2 rows;
- separates value and gradient gates;
- treats FilterFlow-hosted LEDH as adapter work, not native FilterFlow support;
- forbids `.localsource/filterflow` mutation;
- keeps finite differences diagnostic-only;
- excludes stochastic-resampling distribution correctness and
  random/discrete-branch gradient claims;
- includes phase questions, evidence contracts, veto diagnostics,
  explanatory-only diagnostics, artifacts, exit criteria, and stop conditions.

## Hard Gates

- Do not mutate `.localsource/filterflow`.
- Do not run student implementation commands or derive student metrics in this
  lane.
- Do not treat BayesFilter, FilterFlow, students, TT, dense quadrature, paper
  tables, or simulated truth as an oracle.
- Do not relax tolerances, change fixtures, change branch masks, change scalar
  definitions, change OT settings, or change gradient knobs after seeing
  results without a reviewed amendment.
- Do not use finite differences as a gradient promotion gate.
- Do not claim stochastic resampling distribution correctness.
- Do not claim gradients through random seeds, random sampling,
  random/discrete ancestor selection, or Boolean resampling-trigger decisions.
- Use `CUDA_VISIBLE_DEVICES=-1` before TensorFlow imports for CPU-only runs
  unless a separate GPU plan is explicitly approved.
- Preserve command manifests, JSON artifacts, markdown reports, docs/plans
  result ledgers, checksums, and non-claims.

## FilterFlow Architecture Caveat

Local FilterFlow has generic SMC/proposal/resampling architecture and
`RegularisedTransform`, but it does not appear to contain a native LEDH proposal
implementation. The LEDH-PFPF-OT comparison therefore requires a BayesFilter-owned
FilterFlow-side adapter implementing FilterFlow interfaces without modifying
`.localsource/filterflow`.

This is why P1 and P5 are hard architecture/contract gates before any
LEDH-PFPF-OT value or gradient evidence.

## Current Artifacts Created

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-master-program-2026-06-07.md`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-subplan-2026-06-07.md`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p1-architecture-subplan-2026-06-07.md`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p2-bootstrap-ot-contracts-subplan-2026-06-07.md`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p3-bootstrap-ot-values-subplan-2026-06-07.md`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p4-bootstrap-ot-gradients-subplan-2026-06-07.md`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-subplan-2026-06-07.md`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p6-ledh-pfpf-ot-values-subplan-2026-06-07.md`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p7-ledh-pfpf-ot-gradients-subplan-2026-06-07.md`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p8-closeout-subplan-2026-06-07.md`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-claude-review-ledger-2026-06-07.md`
- this reset memo.

## Local Git/Workspace Caveat

The main workspace is dirty and contains many unrelated untracked artifacts from
prior DPF and high-dimensional filtering work. Do not stage broad paths. Use
path-scoped staging if committing this lane.

The last pushed remote closeout commit was integrated as:
`c63ed9d Document BF FilterFlow DPF tieout closeout`.

The local `main` worktree may still be at the pre-integration local commit and
not fast-forwarded to `origin/main`. Do not run destructive Git operations or
reset the worktree without explicit user approval.

## Next Justified Action

Execute P0 only:

`docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-subplan-2026-06-07.md`.

P0 should verify the program files, row set, artifact contract, no-oracle
policy, `.localsource/filterflow` no-mutation policy, and CPU-only TensorFlow
policy. Continue to P1 only after P0 writes a PASS result ledger and receives
Claude result/governance review.

## Non-Claims To Preserve

- no BayesFilter correctness claim;
- no FilterFlow correctness claim;
- no LEDH-PFPF-OT scientific correctness claim;
- no bootstrap-OT scientific correctness claim;
- no stochastic resampling distribution correctness claim;
- no gradient-through-random/discrete-branch claim;
- no student implementation claim;
- no TT/SIRT, paper-table, HMC, DSGE, GPU, scalability, deployment, or
  production-readiness claim.
