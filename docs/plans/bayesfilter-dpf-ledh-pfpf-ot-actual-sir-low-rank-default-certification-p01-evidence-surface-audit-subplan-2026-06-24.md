# P01 Evidence Inventory And Default-Surface Audit Subplan

Date: 2026-06-24

Status: `COMPLETE_P01_PASSED`

## Phase Objective

Run a local-check-only audit that inventories existing low-rank actual-SIR d18
evidence, verifies the locked default candidate, maps the code/config/API
surface that would need to change for a default route, and determines the exact
P02/P03 evidence gaps before any GPU benchmark runtime or code change.

This phase is an audit only. It may run local syntax, focused pytest, text
search, and artifact-validation commands. It does not change defaults, run GPU
benchmarks, or certify low-rank as default.

## Entry Conditions Inherited From Previous Phase

- P00 governance result exists and passes.
- Master program, runbook, review ledger, execution ledger, stop handoff, and
  P01 subplan exist.
- Claude Opus/max read-only review of P00/P01 converged or found no material
  issue.
- No approval is inherited for GPU benchmark runtime, default-code changes,
  public API changes, package installs, network fetches, destructive git
  operations, HMC readiness claims, or scientific claims.

## Required Artifacts

- This subplan.
- P01 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p01-evidence-surface-audit-result-2026-06-24.md`
- Updated execution ledger.
- Updated review ledger if Claude is used.
- Existing evidence anchor:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-replicated-evidence-resource-boundary-result-2026-06-23.md`
- Code-surface inventory over:
  - `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`
  - `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py`
  - `tests/test_actual_sir_low_rank_route_validation.py`
  - `tests/test_actual_sir_low_rank_tuning_grid.py`
  - relevant BayesFilter public/default modules discovered by `rg`

## Required Checks, Tests, And Reviews

- Skeptical plan audit before execution.
- No-runtime artifact validator over the N3072 evidence anchor and its source
  aggregate JSONs.
- `rg` code-surface audit for default, route, low-rank, NumPy, public API, and
  LEDH/PFPF-OT configuration surfaces.
- Candidate-lock check confirming `r16_eps0p25_alpha1em08_it120` is present in
  completed evidence and remains bounded engineering candidate only.
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
- Boundary scan over P01 result and P02 draft.
- Claude review if the audit identifies a material ambiguity about default
  surface, evidence sufficiency, or boundary safety.

## Evidence Contract

- Question: what exact evidence and implementation-surface gaps remain before
  low-rank can be considered for bounded LEDH engineering default?
- Baseline/comparator: current streaming route, current low-rank validation
  harness, and completed N3072 evidence.
- Primary pass criterion: P01 produces a complete inventory of current evidence,
  default-surface files, missing gates, and next P02/P03 requirements without
  unsupported claims.
- Veto diagnostics: missing or corrupt evidence anchor, inability to identify
  default/API surface, failed local checks, unsupported claim, or discovery that
  immediate progress requires unapproved GPU benchmark/default/API changes.
- Explanatory diagnostics: discovered files, tests, current nonclaims,
  candidate metrics, and dirty worktree context.
- What will not be concluded: default readiness, speedup, statistical ranking,
  posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API
  readiness, N4096 feasibility, formal memory scaling, production readiness, or
  scientific validity.
- Artifact preserving result: P01 result and updated ledgers.

## Forbidden Claims And Actions

- Do not run GPU benchmarks.
- Do not change defaults, public exports, API, package metadata, or algorithmic
  code.
- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not claim low-rank default readiness or speedup from warm ratios alone.
- Do not reject viable/deferred candidates from this audit.
- Do not treat Claude as execution authority.

## Exact Next-Phase Handoff Conditions

- If P01 passes and finds no implementation-surface blocker, draft or refresh
  P02 implementation/no-NumPy audit subplan and review it.
- If P01 finds that a default switch target is ambiguous, write a blocker
  result and ask for human direction.
- If P01 finds unapproved API/default changes are required immediately, stop
  before code changes and ask for approval.
- If P01 local checks fail, write a blocker result and stop for focused repair.

## Stop Conditions

- Missing/corrupt evidence anchor.
- Candidate lock cannot be verified.
- Default/API surface cannot be identified enough to plan P02/P05.
- Required local checks fail.
- Boundary scan finds unsupported claims.
- Any action would require GPU benchmark runtime, default-code change, public
  API change, package/network access, destructive git operation, or
  scientific/HMC claim.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the P01 result or blocker result.
3. Draft or refresh the P02 subplan.
4. Review P02 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.

## Subplan Self-Review

- Consistency: follows P00 and remains local-check-only.
- Correctness: validates current evidence and maps default surface before
  further claims or code changes.
- Feasibility: local file/artifact audit only; no GPU benchmark or code change.
- Artifact coverage: result, ledgers, evidence anchor, and discovered surfaces.
- Boundary safety: forbids GPU benchmark runtime, default/API changes, and
  unsupported scientific/HMC claims.
