# P00 Governance, Scope Lock, And Program Review Subplan

Date: 2026-06-24

Status: `COMPLETE_P00_PASSED`

## Phase Objective

Launch the visible default-certification program without crossing GPU benchmark,
default-policy, public API, code-changing, HMC, or scientific-claim boundaries.
P00 validates that the master program, runbook, review ledger, execution
ledger, current N3072 evidence anchor, and P01 subplan exist and preserve the
required evidence boundaries.

This phase may run local syntax, focused pytest, text search, and
artifact-validation commands. It does not run GPU benchmarks, change defaults,
touch public API, modify algorithmic code, make HMC claims, or make scientific
claims.

## Entry Conditions Inherited From Previous Phase

- The N3072 replicated-evidence closeout exists and has status
  `PASS_STOP_AUTOMATIC_RUNTIME_ESCALATION`.
- The user requested a master program, dedicated subplans, visible runbook, and
  Claude Opus/max read-only review with a repair loop.
- The user instructed Codex to be supervisor/executor and Claude to be
  read-only reviewer.
- BayesFilter policy requires TensorFlow/TFP GPU/XLA-oriented implementation
  and forbids NumPy as BayesFilter-owned algorithmic backend except for allowed
  reference/reporting uses.
- No approval is inherited for GPU benchmark runtime, default-code changes,
  public API changes, package installs, network fetches, destructive git
  operations, HMC readiness claims, or scientific claims.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-master-program-2026-06-24.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-visible-gated-execution-runbook-2026-06-24.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-claude-review-ledger-2026-06-24.md`
- Visible execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-visible-execution-ledger-2026-06-24.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-visible-stop-handoff-2026-06-24.md`
- P00 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p00-governance-result-2026-06-24.md`
- Draft P01 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p01-evidence-surface-audit-subplan-2026-06-24.md`

## Required Checks, Tests, And Reviews

- Skeptical plan audit before execution.
- File-existence check for the master program, runbook, ledgers, stop handoff,
  P00 subplan, P01 subplan, and N3072 evidence anchor.
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
- Boundary scan over the new program artifacts for unsupported default,
  speedup, ranking, posterior, HMC, dense-equivalence, API, N4096, formal
  memory, production, or scientific claims.
- Claude Opus/max read-only review of the master program, visible runbook, P00
  subplan, P01 subplan, and review ledger until `VERDICT: AGREE` or max five
  rounds for the same blocker.

## Evidence Contract

- Question: is the default-certification program well-scoped, reviewable,
  artifact-complete, and safe to launch through local-check-only P00?
- Baseline/comparator: the completed N3072 replicated-evidence closeout and
  existing actual-SIR low-rank validation harness/results.
- Primary pass criterion: required files exist, local checks pass, boundary
  scan passes, Claude review converges, and P00 result preserves all nonclaims.
- Veto diagnostics: missing required artifact, failed local check, unsupported
  claim, default/API/runtime boundary crossing, stale evidence anchor, missing
  repair loop, or Claude `VERDICT: REVISE` after five rounds for the same
  blocker.
- Explanatory diagnostics: file counts, local check output, review findings,
  and dirty worktree context.
- What will not be concluded: low-rank default readiness, speedup, statistical
  ranking, posterior correctness, HMC readiness, dense Sinkhorn equivalence,
  public API readiness, N4096 feasibility, formal memory scaling, production
  readiness, or scientific validity.
- Artifact preserving result: the P00 governance result and updated review and
  execution ledgers.

## Forbidden Claims And Actions

- Do not run GPU benchmarks.
- Do not change BayesFilter defaults, public exports, API, package metadata, or
  algorithmic code.
- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not claim speedup, statistical ranking, posterior correctness, HMC
  readiness, dense Sinkhorn equivalence, public API/default readiness, N4096
  feasibility, formal memory scaling, production readiness, or scientific
  validity.
- Do not treat Claude as an execution authority.
- Do not continue after a material review blocker without a visible patch and
  focused recheck.

## Exact Next-Phase Handoff Conditions

- If P00 passes, write the P00 result, update ledgers, and proceed to P01
  evidence inventory/default-surface audit.
- If P00 fails due to missing artifacts or local checks, write a blocker result
  and stop for repair.
- If Claude review does not converge after five rounds for the same blocker,
  write a blocker result and stop for human direction.
- If P00 discovers that default certification requires an unapproved GPU
  benchmark, code-changing, default-policy, public API, HMC, or scientific-claim
  boundary immediately, write a stop handoff and ask for approval.

## Stop Conditions

- Required artifact missing.
- Local syntax/test check fails.
- Boundary scan finds an unsupported claim.
- Claude review returns a material unpatched `VERDICT: REVISE`.
- Any action would require GPU benchmark runtime, default-code change, public
  API change, package/network access, destructive git operation, or
  scientific/HMC claim.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the P00 result or blocker result.
3. Draft or refresh the P01 subplan.
4. Review P01 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.

## Subplan Self-Review

- Consistency: P00 launches the requested visible program while allowing local
  checks and without crossing later GPU benchmark/default boundaries.
- Correctness: it checks required artifacts, evidence anchor, repair loop, and
  local tests.
- Feasibility: local-check-only; no GPU benchmark, no code-changing runtime.
- Artifact coverage: includes master, runbook, ledgers, stop handoff, P00
  result, and P01 subplan.
- Boundary safety: preserves no-NumPy policy and forbids GPU benchmark,
  default/API, HMC, and scientific claim boundaries.
