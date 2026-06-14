# DPF V2 Algorithm Full BF/FilterFlow Comparison P0 Visible Governance Result

metadata_date: 2026-06-08
phase: P0
execution_route: `VISIBLE_IN_DIALOGUE`
status: `PASS_P0_READY_FOR_P1`

## Question

Are the governance, artifact, non-oracle, and stop-condition rules strong
enough to launch a full BF/FilterFlow comparison for bootstrap-OT and
LEDH-PFPF-OT across all V2 rows under the visible gated execution runbook?

## Evidence Contract

Primary criterion:

- Confirm this program is additive and does not reinterpret closed V2 evidence.
- Confirm every phase must preserve the six-row V2 model set.
- Confirm `.localsource/filterflow` mutation is forbidden.
- Confirm student code is out of scope.
- Confirm full-comparison success cannot be declared with an unexecuted
  required row or unexecuted required gradient knob.
- Confirm P1 advancement is blocked until Claude read-only review returns
  `VERDICT: AGREE`.

Veto diagnostics:

- any phase path missing;
- row-order mismatch with `EXPECTED_V2_MODEL_IDS`;
- old V2 deterministic closeout or detached P0 artifacts substituted for this
  algorithm comparison;
- FilterFlow, BayesFilter, TT, dense quadrature, paper tables, students, or
  simulated truth treated as an oracle;
- finite differences used as a gradient promotion gate;
- tolerance, scalar, branch, fixture, OT setting, or gradient knob changes
  after seeing results without reviewed amendment;
- `.localsource/filterflow` mutation;
- student command or student metric;
- full success allowed with an unexecuted row or required gradient knob.

Explanatory-only diagnostics:

- dirty worktree status;
- historical detached P0 artifacts;
- current `.localsource/filterflow` commit/status.

Non-claims:

- P0 does not establish any value or gradient match.

## Local Skeptical Phase Audit

Audit status: `PASS_LOCAL_PHASE_AUDIT`.

Wrong-baseline risk:

- Controlled. The visible P0 assessment does not use old deterministic V2
  evidence, BayesFilter, FilterFlow, TT, dense quadrature, paper tables,
  students, simulated truth, or the incidental detached P0 artifact as an
  oracle.

Proxy-metric risk:

- Controlled. P0 has no numerical promotion metric. ESS, RMSE, runtime, finite
  differences, seed robustness, and smoke summaries remain explanatory-only for
  later phases.

Missing stop-condition risk:

- Controlled. P0 blocks P1 until the visible ledger and Claude read-only review
  agree. Missing phase files, row loss, contract weakening,
  `.localsource/filterflow` mutation need, student execution, or unreviewed
  result-dependent changes remain stop conditions.

Artifact mismatch risk:

- Repaired after Claude P0 review round 1. The detached-route P0 result is now
  marked historical, and this visible-specific result records the current gate
  state as `LOCAL_PASS_REVIEW_PENDING` until review agreement.
- Repaired after Claude P0 review round 2. The visible runbook and P0 subplan
  now route P0 to the visible-specific result and JSON artifacts.

Audit decision:

- No material flaw remains in P0 after Claude round 3 returned
  `VERDICT: AGREE`.

## Visible Checks Performed

| Check | Visible result |
| --- | --- |
| all P0--P8 subplans exist | PASS |
| master phase table paths exist | PASS |
| six V2 rows preserved in master program | PASS |
| row order matches `EXPECTED_V2_MODEL_IDS` | PASS |
| `.localsource/filterflow` mutation forbidden by master/subplans | PASS |
| `.localsource/filterflow` checkout clean | PASS |
| student code out of scope | PASS |
| finite differences not a gradient promotion gate | PASS |
| full success blocked with any unexecuted row or required gradient knob | PASS |
| CPU-only TensorFlow command policy recorded | PASS |
| P1 blocked pending Claude review | PASS |

Required V2 rows, in order:

1. `lgssm_2d_h25_rich`
2. `sv_1d_h18_rich`
3. `range_bearing_4d_h20_rich`
4. `structural_ar1_quadratic_h16`
5. `spatial_sir_j3_rk4`
6. `predator_prey_rk4`

## Visible Command Summary

Codex ran visible shell checks in the current dialogue:

- `rg --files docs/plans | rg '^docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p[0-8]-.*-subplan-2026-06-07\\.md$'`
- `rg -n` checks over the master program and P0--P8 subplans for required row
  ids, pass tokens, no-FilterFlow-mutation language, no-student/no-oracle
  language, and FD diagnostic-only constraints.
- `sed -n '820,838p' experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py`
- `git -C .localsource/filterflow rev-parse HEAD`
- `git -C .localsource/filterflow status --short`

Observed `.localsource/filterflow` HEAD:

- `1e5fbc288c1c11fc18ba01bb4842832e2088b800`

Observed `.localsource/filterflow` status:

- clean.

No TensorFlow command, GPU command, student command, value computation, or
gradient computation was run during visible P0.

## Current Gate State

Local decision:

- `PASS_P0_READY_FOR_P1` is locally supported.

Review gate:

- Claude read-only review round 3 returned `VERDICT: AGREE`.

Current status:

- `PASS_P0_READY_FOR_P1`.

## Claude Read-Only Review Trail

| Round | Verdict | Outcome |
| --- | --- | --- |
| 1 | `VERDICT: REVISE` | Repaired stale detached-route top-level P0 pass metadata by marking it historical and creating visible-specific P0 artifacts. |
| 2 | `VERDICT: REVISE` | Repaired the visible runbook and P0 subplan artifact map so P0 routes to visible-specific artifacts. |
| 3 | `VERDICT: AGREE` | Claude agreed the active visible route points P0 to visible artifacts, detached P0 is historical only, and P1 was blocked until review agreement. |

## Historical Context

The prior detached/live P0 artifacts are historical context only:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-result-2026-06-07.md`
- `experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_p0_governance_2026-06-07.json`
- `experiments/dpf_implementation/reports/dpf-v2-algorithm-full-comparison-p0-governance-2026-06-07.md`
- `docs/plans/logs/dpf-v2-algorithm-full-comparison-live-20260608-012812/`

They do not by themselves satisfy the visible route's P0 gate.

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `PASS_P0_READY_FOR_P1` | governance, artifact contract, row order, no-mutation, no-oracle, no-student, full-success gate, and visible-review gate checked | all P0 veto diagnostics pass after reviewed repairs | later phases may still expose architecture, contract, value, or gradient blockers | begin P1 `PRECHECK` visibly | no value match, gradient match, filtering correctness, implementation correctness, scientific correctness, student, TT/SIRT, dense quadrature, paper-table, simulated-truth, GPU, HMC, DSGE, scalability, deployment, or production-readiness claim |

## Post-Run Red Team

Strongest alternative explanation:

- P0 can pass while later executable phases still fail; P0 is only the
  governance and artifact contract.

Result that would overturn the local decision:

- A reviewer finds a missing phase path, row-order mismatch, oracle allowance,
  unreviewed contract-weakening path, student execution path, FD promotion
  gate, need to mutate `.localsource/filterflow`, or visible/detached artifact
  mismatch.

Weakest evidence link:

- The workspace is dirty. P0 controls this by making no broad staging or
  cleanup action and by restricting its local evidence to read-only governance
  checks.

## Non-Claims

- No BayesFilter correctness proof.
- No FilterFlow correctness proof.
- No proof that bootstrap-OT or LEDH-PFPF-OT is scientifically correct.
- No stochastic resampling distribution correctness claim.
- No value or gradient match.
- No gradient-through-random/discrete-branch claim.
- No student implementation claim.
- No TT/SIRT, dense quadrature, paper-table, simulated-truth, GPU, HMC, DSGE,
  scalability, deployment, or production-readiness claim.
