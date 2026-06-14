# DPF V2 Algorithm Full Comparison P0 Governance Report

run_id: `dpf-v2-algorithm-full-comparison-live-20260608-012812`
metadata_date: 2026-06-07
phase: P0
status: `PASS_P0_READY_FOR_P1`

## Question

Are the governance, artifact, non-oracle, and stop-condition rules strong
enough to launch the full BF/FilterFlow algorithm comparison for bootstrap-OT
and LEDH-PFPF-OT across all V2 rows?

## Local Skeptical Phase Audit

Status: `PASS_LOCAL_PHASE_AUDIT`

The P0 plan does not promote numerical evidence. It only checks that the live
lane is additive, has all phase files, carries the six-row V2 model set in
order, forbids `.localsource/filterflow` mutation, excludes student execution,
keeps finite differences diagnostic-only, and blocks full-comparison success
unless all required rows and gradient knobs execute in later phases.

Material flaws found: none.

## Primary Results

| Gate | Status |
|---|---|
| Additive program, no closed V2 reinterpretation | PASS |
| P0--P8 subplans exist | PASS |
| Master phase table paths match files on disk | PASS |
| Six V2 rows preserved in order | PASS |
| Rows match `EXPECTED_V2_MODEL_IDS` | PASS |
| `.localsource/filterflow` mutation forbidden and checkout clean | PASS |
| Student implementation commands out of scope | PASS |
| Full success requires every row and required gradient knob | PASS |
| CPU-only TensorFlow policy recorded | PASS |
| JSON, markdown/report, result ledger, command log, manifest paths recorded | PASS |

Required V2 rows, in order:

1. `lgssm_2d_h25_rich`
2. `sv_1d_h18_rich`
3. `range_bearing_4d_h20_rich`
4. `structural_ar1_quadratic_h16`
5. `spatial_sir_j3_rk4`
6. `predator_prey_rk4`

## Veto Diagnostics

| Veto | Status |
|---|---|
| Missing phase path | PASS |
| Old deterministic V2 evidence used as substitute | PASS |
| BayesFilter, FilterFlow, TT, dense quadrature, paper tables, students, or simulated truth treated as oracle | PASS |
| FD allowed as gradient promotion gate | PASS |
| Tolerance, scalar, branch, fixture, OT setting, or gradient knob change after results without reviewed amendment | PASS |
| `.localsource/filterflow` mutation | PASS |
| Student command or student metric | PASS |
| Full-comparison success with unexecuted row or gradient knob | PASS |

## Explanatory Diagnostics

| Field | Value |
|---|---|
| root head | `137f6ba5a03ebab199c8ab4699354d50bd560123` |
| FilterFlow head | `1e5fbc288c1c11fc18ba01bb4842832e2088b800` |
| FilterFlow dirty status lines | `0` |
| root `git status --short` lines | `1178` |
| untracked docs/experiments/scripts lines | `1249` |
| TensorFlow commands run | `false` |
| student implementation commands run | `false` |
| values or gradients computed | `false` |

P0 did not import TensorFlow. The CPU-only policy is recorded for later phases:
set `CUDA_VISIBLE_DEVICES=-1` before any TensorFlow import unless a separate
GPU plan is approved.

## Artifacts

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_p0_governance_2026-06-07.json`
- Result ledger:
  `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-result-2026-06-07.md`
- Command log:
  `docs/plans/logs/dpf-v2-algorithm-full-comparison-live-20260608-012812/P0-governance-check.log`
- Command manifest:
  `docs/plans/logs/dpf-v2-algorithm-full-comparison-live-20260608-012812/P0-command-manifest.json`
- Local skeptical audit:
  `docs/plans/logs/dpf-v2-algorithm-full-comparison-live-20260608-012812/P0-local-skeptical-phase-audit.md`

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| `PASS_P0_READY_FOR_P1` | governance and artifact contract checked for all six rows | all P0 veto diagnostics pass | later phases may still expose architecture, contract, value, or gradient blockers | supervisor read-only review, then P1 | no value match, gradient match, filtering correctness, implementation correctness, student, TT/SIRT, paper-table, GPU, HMC, DSGE, scalability, deployment, or production-readiness claim |

## Post-Run Red Team

Strongest alternative explanation:

- P0 can pass while later implementation phases still fail because governance
  only verifies the launch contract.

Result that would overturn this decision:

- A reviewer finds a missing phase gate, row-order mismatch, oracle allowance,
  unreviewed contract-weakening path, student execution path, or need to mutate
  `.localsource/filterflow`.

Weakest evidence link:

- The live workspace is dirty. P0 controls this by preserving protected dirty
  tracked files and writing run-scoped artifacts, not by claiming a clean
  repository state.

## Non-Claims

- No BayesFilter correctness proof.
- No FilterFlow correctness proof.
- No bootstrap-OT or LEDH-PFPF-OT scientific correctness claim.
- No value or gradient match.
- No student implementation claim.
- No TT/SIRT, dense quadrature, paper-table, simulated-truth, GPU, HMC, DSGE,
  scalability, deployment, or production-readiness claim.
