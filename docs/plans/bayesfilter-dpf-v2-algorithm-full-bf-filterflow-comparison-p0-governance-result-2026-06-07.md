# DPF V2 Algorithm Full BF/FilterFlow Comparison P0 Governance Result

metadata_date: 2026-06-07
run_id: `dpf-v2-algorithm-full-comparison-live-20260608-012812`
phase: P0
status: `HISTORICAL_DETACHED_P0_CONTEXT_VISIBLE_REVALIDATION_PENDING`

## Historical Status Note

This artifact was originally created by the superseded live/detached route.
The visible execution route supersedes that mechanism:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-visible-gated-execution-runbook-2026-06-08.md`

The original detached-route `PASS_P0_READY_FOR_P1` decision below is retained
as historical context only. It is not a visible-route gate pass. Under the
visible route, P0 may advance to P1 only after the visible execution ledger and
Claude read-only review agree.

## Question

Are the governance, artifact, non-oracle, and stop-condition rules strong
enough to launch a full BF/FilterFlow comparison for bootstrap-OT and
LEDH-PFPF-OT across all V2 rows?

## Evidence Contract

Primary criterion:

- Confirm this program is additive and does not reinterpret closed V2 evidence.
- Confirm every phase must preserve the six-row V2 model set.
- Confirm `.localsource/filterflow` mutation is forbidden.
- Confirm student code is out of scope.
- Confirm full-comparison success cannot be declared with an unexecuted
  required row or unexecuted required gradient knob.

Veto diagnostics:

- any phase path missing;
- any phase allows old V2 deterministic closeout to substitute for algorithm
  comparison;
- any phase treats FilterFlow, BayesFilter, TT, dense quadrature, paper tables,
  students, or simulated truth as an oracle;
- any phase allows FD as a gradient promotion gate;
- any phase allows tolerance, scalar, branch, fixture, OT setting, or gradient
  knob changes after seeing results without reviewed amendment.

Explanatory-only diagnostics:

- current dirty git status;
- count of untracked DPF planning artifacts;
- prior closed V2 result summary.

Non-claims:

- P0 does not establish any value or gradient match.

## Local Skeptical Phase Audit

Audit status: `PASS_LOCAL_PHASE_AUDIT`

Wrong-baseline risk:

- Controlled. P0 does not use closed deterministic V2 evidence, BayesFilter,
  FilterFlow, TT, dense quadrature, paper tables, students, or simulated truth
  as an oracle.

Proxy-metric risk:

- Controlled. P0 has no numerical promotion metric. ESS, RMSE, runtime, FD
  ladders, seed robustness, and smoke summaries remain explanatory-only in
  later phases.

Missing stop-condition risk:

- Controlled. The master program and P0 subplan require stop/review on missing
  phase files, row loss, contract weakening, `.localsource/filterflow`
  mutation need, student execution, or unreviewed result-dependent changes.

Unfair comparison risk:

- Controlled for P0. Later P2/P5 phases must freeze common contracts before
  value or gradient phases.

Hidden assumption risk:

- Controlled. P0 records that no TensorFlow numerical command, student command,
  value computation, or gradient computation was run.

Stale context and environment risk:

- Controlled for P0. The live workspace is dirty, so protected dirty tracked
  files are recorded in the run directory. P0 writes only additive lane
  artifacts. TensorFlow was not imported; later TensorFlow commands must set
  `CUDA_VISIBLE_DEVICES=-1` before import.

Audit decision:

- No material flaw was found for P0 execution.

## Result

P0 governance passes locally.

Required V2 rows are preserved in this exact order:

1. `lgssm_2d_h25_rich`
2. `sv_1d_h18_rich`
3. `range_bearing_4d_h20_rich`
4. `structural_ar1_quadratic_h16`
5. `spatial_sir_j3_rk4`
6. `predator_prey_rk4`

The same row order appears in:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-master-program-2026-06-07.md`;
- `scripts/dpf_v2_algorithm_full_comparison_live_gate.py`;
- `experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py`
  as `EXPECTED_V2_MODEL_IDS`.

All P0--P8 phase subplans exist and match the master program phase table.

## Primary Criterion Fields

| Field | Status |
|---|---|
| additive program, no closed V2 reinterpretation | PASS |
| all phase subplans exist | PASS |
| master phase table paths exist | PASS |
| six V2 rows preserved in order | PASS |
| row names match `EXPECTED_V2_MODEL_IDS` | PASS |
| `.localsource/filterflow` mutation forbidden | PASS |
| `.localsource/filterflow` checkout currently clean | PASS |
| student code out of scope | PASS |
| full success blocked with any unexecuted row or required gradient knob | PASS |
| CPU-only TensorFlow command policy recorded | PASS |
| artifacts and command manifest written | PASS |

## Veto Diagnostics Result

| Veto | Status |
|---|---|
| missing phase path | PASS |
| old V2 deterministic closeout substitution | PASS |
| oracle misuse allowed | PASS |
| FD gradient promotion allowed | PASS |
| post-result tolerance/scalar/branch/fixture/OT/knob weakening allowed | PASS |
| `.localsource/filterflow` mutation | PASS |
| student command or metric | PASS |
| full success with missing row or gradient knob | PASS |

## Explanatory Only Fields

- root head: `137f6ba5a03ebab199c8ab4699354d50bd560123`
- FilterFlow head: `1e5fbc288c1c11fc18ba01bb4842832e2088b800`
- FilterFlow status lines: `0`
- root `git status --short` lines: `1178`
- untracked docs/experiments/scripts lines: `1249`
- TensorFlow commands run: `false`
- student implementation commands run: `false`
- values or gradients computed: `false`

Protected prelaunch dirty tracked files were read from:

- `docs/plans/logs/dpf-v2-algorithm-full-comparison-live-20260608-012812/prelaunch-dirty-tracked.txt`

No protected tracked dirty file was edited by P0.

## Historical Detached Command Manifest

| Field | Value |
|---|---|
| command manifest | `docs/plans/logs/dpf-v2-algorithm-full-comparison-live-20260608-012812/P0-command-manifest.json` |
| local skeptical audit | `docs/plans/logs/dpf-v2-algorithm-full-comparison-live-20260608-012812/P0-local-skeptical-phase-audit.md` |
| governance command log | `docs/plans/logs/dpf-v2-algorithm-full-comparison-live-20260608-012812/P0-governance-check.log` |
| JSON artifact | `experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_p0_governance_2026-06-07.json` |
| markdown report | `experiments/dpf_implementation/reports/dpf-v2-algorithm-full-comparison-p0-governance-2026-06-07.md` |

These paths are artifacts from the superseded live/detached route. They may be
read as historical context, but they are not current visible-route execution
evidence.

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next action | Not concluded |
|---|---|---|---|---|---|
| `PASS_P0_READY_FOR_P1` | governance, artifact contract, row order, no-mutation, no-oracle, no-student, and full-success gates checked | all P0 veto diagnostics pass | later phases may still expose architecture, contract, value, or gradient blockers | supervisor read-only review, then P1 if reviewed PASS | no value match, gradient match, filtering correctness, implementation correctness, student, TT/SIRT, dense quadrature, paper-table, simulated-truth, GPU, HMC, DSGE, scalability, deployment, or production-readiness claim |

## Post-Run Red Team

Strongest alternative explanation:

- P0 can pass while later executable phases still fail; P0 is only the
  governance and artifact contract.

Result that would overturn the decision:

- A reviewer finds a missing phase path, row-order mismatch, oracle allowance,
  unreviewed contract-weakening path, student execution path, FD promotion
  gate, or need to mutate `.localsource/filterflow`.

Weakest evidence link:

- The live workspace is dirty. This is controlled by run-scoped protected file
  manifests and additive artifact writes, not by claiming a clean repository.

## Repair History

No P0 repair amendment was required.

## Visible Execution Revalidation

visible_runbook:
`docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-visible-gated-execution-runbook-2026-06-08.md`

visible_ledger:
`docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-visible-execution-ledger-2026-06-08.md`

timestamp: `2026-06-08T01:58:36+08:00`

Status: `LOCAL_PASS_REVIEW_PENDING`.

The original P0 result above was produced during an incidental live/detached
attempt after the intended execution mode was misunderstood. Under the visible
runbook, Codex revalidated P0 in the current dialogue before asking Claude for
read-only review.

Visible P0 checks performed:

- read the P0 subplan and visible runbook;
- verified all P0--P8 subplan paths exist;
- checked master/subplan hard-gate language for row preservation, no-oracle
  framing, no-student scope, `.localsource/filterflow` no-mutation policy, and
  FD diagnostic-only treatment;
- checked `EXPECTED_V2_MODEL_IDS` in
  `experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py`;
- recorded `.localsource/filterflow` HEAD
  `1e5fbc288c1c11fc18ba01bb4842832e2088b800`;
- recorded `.localsource/filterflow` status as clean.

Visible P0 did not run TensorFlow, GPU probes, student commands, value
computations, or gradient computations.

Visible P0 local decision:

- `PASS_P0_READY_FOR_P1` is locally supported, pending Claude read-only review.
  Until that review returns `VERDICT: AGREE`, the visible-route status remains
  `LOCAL_PASS_REVIEW_PENDING`.

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
