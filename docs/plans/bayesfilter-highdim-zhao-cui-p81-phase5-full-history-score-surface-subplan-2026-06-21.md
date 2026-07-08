# P81 Phase 5 Subplan: Full-History Score Surface Audit

status: DRAFT_REVIEW_PENDING
date: 2026-06-21

## Phase Objective

Turn the Phase 4 backend-feasibility smoke into an honest next-step plan for
full-history SIR d=18 value/gradient validation.  Phase 5 must decide whether
the Zhao-Cui fixed-branch/JVP-backed candidate can be extended from one-row
horizon-0 score wiring to multistep score propagation before any LEDH-PFPF-OT
value/gradient comparison is run.

## Entry Conditions Inherited From Phase 4

- Phase 3 established only one-row horizon-0 observation-term engineering
  wiring under same-branch finite-difference stability.
- Phase 4 established only trusted GPU-visible backend feasibility for that
  one-row horizon-0 smoke.
- Claude agreed on Phase 4 with the guardrail that Phase 5 is justified only
  as drafting/reviewing a new subplan.
- The current candidate score API
  `multistate_nonlinear_fixed_design_tt_score_path(...)` rejects histories with
  more than one observation row.
- The existing multistate value path can process multiple rows, but
  derivative/score propagation through multistate retained filters has not
  been implemented or tested.
- The scalar fixed-branch score path has a two-step transition derivative
  template, but it is scalar-specific and cannot be cited as multistate
  correctness.

## Required Artifacts

- This subplan.
- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase5-full-history-score-surface-result-2026-06-21.md`.
- Optional implementation subplan for Phase 6 if Phase 5 finds a bounded,
  testable multistate score propagation surface.
- Updated P81 master, runbook, execution ledger, Claude review ledger, and stop
  handoff.

The Phase 5 result must include the repository-required serious-run governance
sections even though Phase 5 is an audit-only phase: a skeptical-audit
pass/fail note before execution, a decision table, and a run manifest covering
the local audit commands actually run, git/worktree status, CPU/GPU status
(`N/A` for no framework execution), random seeds (`N/A` for read-only audit),
artifact paths, and reviewer status.

## Required Checks, Tests, And Reviews

No heavy diagnostics and no LEDH-PFPF-OT comparison may run in Phase 5.

Local audit checks:

```bash
rg -n "def scalar_nonlinear_fixed_design_tt_score_path|def scalar_nonlinear_transition_adjacent_target_derivative_batch|def _scalar_tt_predictive_log_density_and_derivative_from_retained|def multistate_nonlinear_fixed_design_tt_score_path|def multistate_nonlinear_transition_adjacent_target_batch|def _multistate_pairwise_transition_between_grids_log_density|multistate score path currently supports horizon-0" bayesfilter/highdim/filtering.py
rg -n "benchmark_p8p_parameterized_sir_gradient|batch-seeds|num-particles|transport-ad-mode|per_seed_gradient|monte_carlo_gradient_noise|expect-device-kind" docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
rg -n "status: PHASE4_CLAUDE_AGREE_READY_TO_DRAFT_PHASE5|PHASE4_TRUSTED_GPU_VISIBLE_BACKEND_FEASIBILITY_SMOKE_PASSED_CLAUDE_AGREE|Phase 5" docs/plans/bayesfilter-highdim-zhao-cui-p81-*2026-06-21.md
```

Review this Phase 5 subplan with Claude read-only before execution.  After the
Phase 5 audit result is written, review the result and the next subplan with
Claude read-only.  Loop until convergence or five rounds for the same blocker.

Concrete Phase 6 test anchors, if Phase 5 finds the implementation bounded:

- Add or extend `tests/highdim/test_fixed_branch_derivatives.py` with a tiny
  d=2 or d=3 two-observation multistate fixture whose transition density is
  parameter-sensitive and whose finite-difference rows require same-branch
  hashes across base/plus/minus.
- Add or extend `tests/highdim/test_p81_analytical_sir_score.py` only after the
  tiny multistate transition regression passes, with an explicitly bounded
  SIR d=18 two-row/full-history score smoke.
- Require focused pre-implementation checks that locate the scalar score
  template, current multistate horizon-0 guard, multistate transition value
  target, branch-hash helper, and the two target test files.
- Do not add LEDH/P8p comparator tests in Phase 6; those belong to Phase 7 only
  after candidate full-history score evidence exists.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What exact implementation surface is missing before the Zhao-Cui fixed-branch/JVP-backed candidate can be compared fairly against LEDH-PFPF-OT on SIR d=18 value and gradient? |
| Exact baseline/comparator | Current code surface: scalar two-step score path as design template, multistate horizon-0 score path as current candidate capability, P8p LEDH harness as later comparator only. |
| Primary criterion | Phase 5 passes if it produces a concrete implementation-surface map and Phase 6 subplan for multistate full-history score propagation, or a precise blocker explaining why such a bounded implementation is not currently feasible. |
| Veto diagnostics | Treating horizon-0 candidate evidence as full-history gradient correctness; running LEDH comparison before candidate full-history score exists; comparing full-history LEDH against horizon-0 candidate; missing branch-stability/finite-difference contract; unreviewed GPU/large-run command; source-faithfulness overclaim. |
| Explanatory diagnostics | Located scalar template functions, located missing multistate functions, P8p comparator command shape, expected runtime/memory risks, and proposed tiny d=2 transition regression. |
| Not concluded | No implementation correctness, no SIR d=18 full likelihood correctness, no LEDH agreement, no HMC readiness, no posterior/scientific validity, no performance scaling, no default readiness. |
| Artifact preserving result | Phase 5 result markdown and updated P81 ledgers. |

## Required Phase 5 Analysis

Phase 5 must produce a table with at least these rows:

| Surface | Current status to verify | Required next evidence |
|---|---|---|
| Multistate initial target derivative | Exists from Phase 3 | Keep covered by horizon-0 d=18 smoke and tiny d=2 FD regression. |
| Multistate transition target derivative | Missing or not public | Needs implementation mirroring scalar transition derivative with multistate retained TT grid. |
| Multistate retained log-density derivative | Missing or scalar-only | Needs derivative values on retained multistate grid and shape/storage gates. |
| Multistep branch compatibility hash | Missing beyond horizon-0 | Needs fixed-design same-branch hash excluding theta but including samples/basis/ranks/seeds/horizon. |
| Tiny multistate transition regression | Missing | Needs d=2 or d=3, two-observation test with finite score and same-branch FD agreement. |
| Actual SIR d=18 full-history score smoke | Not authorized yet | Only after tiny multistate transition regression passes. |
| LEDH-PFPF-OT comparator | Available as P8p harness | Comparator only after candidate full-history score exists and Phase 6/7 contracts define budgets and tolerances. |

## Forbidden Claims And Actions

- Do not run P8p LEDH-PFPF-OT diagnostics in Phase 5.
- Do not run SIR d=18 full-history candidate diagnostics in Phase 5.
- Do not claim Phase 4 made the candidate GPU-validated beyond backend
  feasibility.
- Do not compare LEDH full-history value/gradient to a horizon-0 candidate.
- Do not implement production/default behavior changes in Phase 5.
- Do not use NumPy as a BayesFilter algorithmic implementation backend.
- Do not claim source-faithfulness for the fixed-branch candidate without
  Zhao-Cui paper/source anchors.

## Exact Next-Phase Handoff Conditions

Phase 6 may implement only if Phase 5 identifies a bounded multistate
full-history score propagation surface and a reviewed Phase 6 subplan states:

- exact functions/classes to edit;
- exact target tests/files to add before any SIR d=18 full-history diagnostic,
  including the tiny multistate transition finite-difference regression in
  `tests/highdim/test_fixed_branch_derivatives.py`;
- shape/storage/complexity gates;
- same-branch finite-difference compatibility hash contract;
- CPU-hidden and GPU-visible check boundaries;
- no LEDH comparison until candidate full-history score smoke passes.

If Phase 5 cannot identify a bounded implementation surface, it must write a
blocker result and stop.

## Stop Conditions

Stop with a blocker if the audit cannot distinguish candidate capability from
LEDH comparator capability, if the only available comparison would be
horizon-0-vs-full-history, if the implementation would require broad refactors
or default changes, or if Claude review does not converge after five rounds.
