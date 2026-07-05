# Phase 0 Subplan: Scope And Route Freeze

Date: 2026-07-01

Status: `DRAFT_FOR_CLAUDE_REVIEW`

## Phase Objective

Freeze the current evidence, code paths, baseline artifacts, and exact
questions before implementing regional or sensitivity diagnostics.

## Entry Conditions Inherited From Previous Phase

- User requested a systematic ladder covering regional expansion, regional
  orthogonal coordinates, RK4 sensitivity, and non-centered innovation ideas.
- Existing raw/physics/whitened budget-10 SIR diagnostics are available.
- Claude read-only review is approved by user policy for this repo.

## Required Artifacts

- This subplan.
- Master program:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-master-program-2026-07-01.md`
- Visible runbook:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-visible-gated-execution-runbook-2026-07-01.md`
- Phase 0 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase0-scope-route-result-2026-07-01.md`
- Claude review ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-claude-review-ledger-2026-07-01.md`
- Visible execution ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-visible-execution-ledger-2026-07-01.md`

## Required Checks, Tests, Reviews

- Local artifact presence and heading check with `rg`.
- Read-only code inventory of:
  - `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
  - `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
  - relevant SIR manual-score tests.
- Claude read-only review of the master program, runbook, and Phase 0/1
  subplans.

Exact local commands:

```bash
rg -n "^#|Phase Objective|Entry Conditions|Required Artifacts|Required Checks|Evidence Contract|Forbidden Claims|Exact Next-Phase|Stop Conditions|End-Of-Subplan" docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-*.md
rg -n "log_kappa_scale|log_nu_scale|PARAMETER_NAMES|_manual_value_and_score|_sir_transition_mean_vjp_tf|_sir_rhs_vjp_tf" docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/test_ledh_pfpf_ot_p7_manual_score.py
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
```

Exact Claude review command template:

```bash
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name sir-reparam-rootcause-plan-review-iter3 --model opus --effort max "READ-ONLY REVIEW ONLY. Do not edit files, run experiments, launch agents, or change state. Review exact paths named in the prompt. Findings first. End with exactly VERDICT: AGREE or VERDICT: REVISE."
```

The Claude command is a foreground read-only reviewer call, not detached phase
execution.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the ladder, baseline, phase gates, and first implementation target correctly scoped before code changes? |
| Baseline/comparator | Existing raw/physics/whitened SIR budget-10 artifacts and current `benchmark_p8p_*` code paths. |
| Primary pass criterion | Phase 0 result lists exact code anchors, baseline artifacts, and Phase 1 handoff conditions; Claude returns `VERDICT: AGREE` or all material findings are patched. |
| Veto diagnostics | Missing exact paths, stale baseline, unsupported claim, material plan review finding, or subplan lacking required fields. |
| Explanatory diagnostics | Code-path inventory and current artifact summary. |
| Not concluded | No implementation correctness, no SIR gradient correctness, no HMC readiness. |

## Forbidden Claims And Actions

- Do not edit algorithmic code in Phase 0.
- Do not run material GPU diagnostics in Phase 0.
- Do not claim any root cause is found.
- Do not change thresholds or default policy.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- Phase 0 result exists.
- Master/runbook/Phase 1 subplan pass local artifact checks.
- Claude read-only review converges for launch plan material issues.
- Phase 1 has exact implementation targets and stop conditions.

## Stop Conditions

- Claude review does not converge after five rounds for the same blocker.
- Code inventory shows regional expansion would require broad production
  changes rather than diagnostic-only code.
- Required artifacts cannot be written under `docs/plans`.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write Phase 0 result / close record.
3. Draft or refresh Phase 1 subplan.
4. Review Phase 1 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
