# P83 Phase 7 Reset Memo: Clean Reentry After Phase 6

Date: 2026-06-23

Status: `RESET_READY_FOR_NEW_SESSION`

## Why This Memo Exists

The prior P83 session accumulated enough context that a clean reentry artifact
is safer than continuing from memory.  This memo is the load target for a new
session before any P83 Phase 7 work.

Use this memo to continue from the stopped state after Phase 6.  Do not infer
authorization to run Phase 7 from this memo.

## Current Stop State

Current governing stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md`
- Status: `STOP_AFTER_PHASE6_PENDING_PHASE7_APPROVAL`

Execution is intentionally stopped after Phase 6.

P83-7 SIR d=18 source-route validation is drafted but blocked.  No fitting,
d=18 validation, LEDH comparison, GPU job, HMC, MCMC, long run, or production
claim is authorized until Phase 7 is refreshed with exact commands/artifacts
and the user explicitly approves execution.

## Phase Status Summary

| Phase | Status | Main artifact |
|---|---|---|
| P83-0 governance reset | PASS | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase0-governance-reset-result-2026-06-22.md` |
| P83-1 anchored inventory | PASS | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase1-source-route-inventory-result-2026-06-22.md` |
| P83-2 transport/marginalization design | PASS | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-result-2026-06-22.md` |
| P83-3 minimal transport slice | PASS | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase3-minimal-transport-slice-result-2026-06-22.md` |
| P83-4 analytical derivative audit | BLOCKED for derivative readiness | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase4-analytical-derivative-audit-result-2026-06-22.md` |
| P83-5 mechanics smoke | PASS mechanics-only | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase5-mechanics-smoke-result-2026-06-22.md` |
| P83-6 fitting budget design | PASS design-only | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-result-2026-06-22.md` |
| P83-7 d18 validation | DRAFT BLOCKED | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-subplan-2026-06-22.md` |

## Active Blockers And Boundaries

Active blocker:

- `BLOCK_P83_PHASE4_ANALYTICAL_DERIVATIVE_READINESS`
- Meaning: no local source-route same-branch analytical derivative wiring was
  found.  FD/JVP/ForwardAccumulator evidence remains diagnostic-only.

Active transport boundary:

- Current `FixedTTSIRTTransport` grid-CDF route is a diagnostic approximation.
- `production_kr_closure=False` must remain true in claims unless a later
  reviewed source-backed KR replacement passes.
- Proposal correction must remain through `eval_pdf` on local samples, not a
  base-density-only substitute.

Active source-route boundary:

- The governing lane is the fixed-TTSIRT retained-object Zhao-Cui source route.
- Local all-grid/operator route remains `extension_or_invention`.
- UKF is scout/calibration only and cannot close source-faithfulness or
  correctness gaps.
- Validation CE, replay diagnostics, finite values, ESS, and fit loss may
  explain or veto only under a declared evidence contract.  They do not by
  themselves prove correctness, convergence, derivative readiness, HMC
  readiness, or production readiness.

## Phase 6 Budget Contract To Preserve

Phase 6 result:

- `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-result-2026-06-22.md`
- Status: `PASS_P83_PHASE6_FITTING_BUDGET_DESIGN`

Parameter-count formula:

```text
P_theta = sum_axis ranks[axis] * b_axis * ranks[axis + 1]
```

For uniform interior rank `R`, uniform basis dimension `b`, and author SIR
target dimension `D=36`:

```text
P_theta = b * (2 * R + 34 * R^2)
```

Hard source-route fitting evidence minimum:

```text
minimum_training_samples = max(20 * P_theta, author_source_sample_floor)
author_source_sample_floor = 5000
```

Author SIR basis/domain anchor:

- Author script uses `Lagrangep(4,8)` on `AlgebraicMapping(1)`.
- Source cardinality implied by `Lagrangep(4,8)` is `33`.
- Current local fitter uses `LegendreBasis1D`, where `basis_dim=max_degree+1`.
- Therefore local Legendre rungs are diagnostic unless a reviewed fixed
  adaptation explicitly authorizes them for the Phase 7 target.

Phase 6 ladder values:

| Lane | Basis dimension | Rank pattern | `P_theta` | Minimum training samples | Role |
|---|---:|---|---:|---:|---|
| Local diagnostic rung A | `2` | `(1,2,...,2,1)` | `280` | `5600` | plumbing only |
| Local diagnostic rung B | `3` | `(1,4,...,4,1)` | `1656` | `33120` | first serious local budget diagnostic |
| Local stronger rung C | `4` | `(1,8,...,8,1)` | `8768` | `175360` | stronger local fixed-rank diagnostic |
| Local degree-richer rung D | `5` | `(1,8,...,8,1)` | `10960` | `219200` | degree sensitivity diagnostic |
| Local rank-richer rung E | `4` | `(1,12,...,12,1)` | `19680` | `393600` | rank sensitivity diagnostic |
| Author-basis rung F | `33` | `(1,4,...,4,1)` | `18216` | `364320` | author-basis feasibility rung |
| Author-basis rung G | `33` | `(1,8,...,8,1)` | `72336` | `1446720` | author-basis stronger rung |
| Author option envelope | `33` | effective rank `20` envelope | `450120` | `9002400` | separate long-run plan only |

## Phase 7 Draft State

Current Phase 7 draft:

- `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-subplan-2026-06-22.md`
- Status: `DRAFT_BLOCKED_PENDING_HUMAN_APPROVAL_AND_EXECUTION_REFRESH`

It is not executable.  It must be refreshed before launch.

Phase 7 may execute only after a reviewed refresh freezes:

- exact command(s);
- exact result artifact and JSON manifest paths;
- fit artifacts consumed;
- random seeds and evidence-cloud roles;
- runtime/GPU or CPU posture;
- comparator tier;
- pass/fail criteria;
- veto diagnostics;
- nonclaims;
- explicit user approval.

The expected result path in the draft is:

- `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-result-2026-06-22.md`

The expected JSON manifest path in the draft is:

- `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-2026-06-22.json`

A new session may update these to `2026-06-23` paths if it writes a refreshed
Phase 7 plan.

## Phase 7 Comparator Tiers

Phase 7 must choose exactly one tier before execution.

| Tier | Allowed interpretation | Extra requirements |
|---|---|---|
| `d18_execution_only` | finite source-route execution diagnostics only | no accuracy/correctness/rank-convergence claim |
| `d18_same_route_rank_convergence` | adjacent rank/degree stability diagnostic | budgeted stronger same-route comparator, same source invariants, disjoint clouds |
| `d18_correctness_candidate` | candidate evidence toward d=18 correctness | source-backed comparator/reference bridge and stricter audit contract |

Recommended reentry posture:

- Start with a refreshed `d18_execution_only` design if the goal is to make
  Phase 7 executable soon.
- Do not choose `d18_same_route_rank_convergence` unless the plan includes a
  budgeted stronger same-route comparator satisfying Phase 6 sample minima.
- Do not choose `d18_correctness_candidate` unless a source-backed comparator
  or reference bridge is explicitly available and reviewed.
- Do not include gradient/HMC/value-gradient claims while Phase 4 derivative
  readiness remains blocked.

## Local Code Surfaces To Inspect

Use these anchors before refreshing Phase 7.  Do not rely only on this memo.

Budget/fitting:

- `bayesfilter/highdim/fitting.py:39-107`: `FixedTTFitConfig`.
- `bayesfilter/highdim/fitting.py:111-152`: `FixedTTFitSampleBatch`.
- `bayesfilter/highdim/fitting.py:224-348`: `FixedTTFitter.fit`.
- `bayesfilter/highdim/fitting.py:544-598`: `_check_design_budget`.

Transport/readiness:

- `bayesfilter/highdim/transport.py:327-331`: P83 manifest fields including
  `proposition2_marginal_backend`, `production_kr_closure=False`, and
  `proposal_density_backend="eval_pdf_on_local_samples"`.
- `bayesfilter/highdim/source_route.py:70-97`: P58/P59 readiness constants,
  comparator tiers, target id `zhao_cui_sir_austria_d18`.
- `bayesfilter/highdim/source_route.py:1413-1487`:
  `p83_minimal_transport_slice_readiness`.
- `bayesfilter/highdim/source_route.py:1507-1560`:
  `p58_m9_source_route_pipeline_readiness`.

Existing bounded source-route helpers:

- `bayesfilter/highdim/source_route.py:2193-2405`:
  `p59_author_sir_36d_target_fit_prep`.
- `bayesfilter/highdim/source_route.py:2941-3282`:
  `p59_author_sir_step_spec_assembly`.
- `bayesfilter/highdim/source_route.py:5261-5337`:
  `p60_author_sir_same_route_rank_comparator`.
- `bayesfilter/highdim/source_route.py:5340-5390`:
  `p66_fixed_branch_sample_adequacy`.
- `bayesfilter/highdim/source_route.py:5452-5485` and following:
  `p66_author_sir_fixed_branch_validation_ladder`.
- `bayesfilter/highdim/source_route.py:6538-6665`:
  `p59_author_sir_runner_manifest_path`.
- `bayesfilter/highdim/source_route.py:6726-6860`:
  `p59_author_sir_validation_ladder`.

Important caveat:

- Several P59/P60/P66 helpers are bounded diagnostic surfaces with small
  defaults, for example `P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT=9`.
- Those defaults do not satisfy the Phase 6 `max(20 * P_theta, 5000)` evidence
  rule for Phase 7 source-route fitting claims.
- A Phase 7 refresh must either design a budget-compliant fitting/build phase
  or explicitly stay at a diagnostic/execution-only scope without fit-quality
  or correctness promotion.

Tests touched/available:

- `tests/highdim/test_p83_minimal_source_route_transport_slice.py`
- `tests/highdim/test_p58_m9_source_route_pipeline_readiness.py`
- Prior focused P83 Phase 3 bundle passed: `19 passed, 2 warnings`.
- Prior P83 Phase 5 mechanics smoke passed: `2 passed, 7 deselected, 2 warnings`.

## Author Source Anchors

Use these source anchors for any Phase 7 refresh:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-17`:
  author SIR uses `d=0`, `m=18`, `T=20`, hence target dimension
  `d + 2*m = 36`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:39-55`:
  author SIR declares `N=5e3`, `sqr=1`, `Lagrangep(4,8)`,
  `AlgebraicMapping(1)`, main/low `TTOption`, and calls `full_sol`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43`:
  source route push, reapproximation, `eval_irt`, `L`/`mu` mapping, and
  `eval_pdf` correction.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:64-98`:
  `computeL`, weighted resampling, `epd` scaling, and split local init/debug
  samples.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Options/TTOption.m:61-91`:
  author TT option fields and `fix_rank` behavior when `kick_rank=0`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/TTSIRT.m:185-188`:
  executable TTSIRT default defensive `tau=1E-8`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTFun/TTFun.m:176-204`:
  author TTFun sample-size heuristic and cross construction.

## Claude Review Trail

Review ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md`

Key review trail:

- `p83-p0-governance-review-r1`: `VERDICT: AGREE`
- `p83-p1-inventory-p2-handoff-review-r1`: stalled, probe succeeded
- `p83-p1-inventory-p2-handoff-review-r2`: `VERDICT: AGREE`
- `p83-p2-design-p3-handoff-review-r1`: `VERDICT: AGREE`
- `p83-p3-minimal-slice-p4-handoff-review-r1`: `VERDICT: AGREE`
- `p83-p4-derivative-blocker-p5-handoff-review-r1`: stalled
- `p83-p4-claude-probe`: `PROBE_OK`
- `p83-p4-derivative-blocker-p5-handoff-review-r2`: stalled
- `p83-p4-derivative-blocker-p5-handoff-review-r3`: `VERDICT: AGREE`
- `p83-p6-budget-p7-handoff-review-r1`: stalled
- `p83-p6-claude-probe`: `PROBE_OK`
- `p83-p6-budget-p7-handoff-review-r2`: `VERDICT: AGREE`

Pattern:

- Do not send whole files or large packets to Claude.
- If Claude stalls, interrupt, run the tiny probe
  `READ-ONLY PROBE. Reply exactly PROBE_OK.`
- If the probe succeeds, redesign the prompt to a minimal verdict-only boundary
  question.

Claude remains read-only reviewer only.  Claude cannot authorize crossing
human, runtime, GPU, model-file, funding, product-capability, default-policy,
or scientific-claim boundaries.

## Required Reentry Steps For A New Session

1. Load this memo.
2. Read the stop handoff:
   `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md`.
3. Read Phase 6 result and Phase 7 draft:
   `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-result-2026-06-22.md`
   and
   `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-subplan-2026-06-22.md`.
4. Run a skeptical audit before any Phase 7 refresh.
5. Refresh Phase 7 as a new dated subplan/result pair or patch the existing
   Phase 7 draft visibly.
6. State whether Phase 7 is:
   - fitting/build only;
   - `d18_execution_only`;
   - `d18_same_route_rank_convergence`;
   - `d18_correctness_candidate`;
   - or blocked.
7. Freeze exact commands, artifacts, seeds, runtime/GPU posture, pass/fail
   criteria, vetoes, and nonclaims.
8. Run local doc/code checks.
9. Use tiny Claude read-only review for material Phase 7 boundary decisions.
10. Ask the user for explicit approval before any d=18, fitting, GPU, LEDH,
    HMC, MCMC, or long command.

## Approval Boundary

The user has not approved Phase 7 execution yet.

Before execution, ask for approval with the exact command(s) and state:

- whether GPU is used;
- expected runtime;
- output artifacts;
- whether the run is fitting/build, execution-only, rank-convergence, or
  correctness-candidate;
- why the command answers the stated evidence contract;
- what will not be concluded even if it passes.

Per local AGENTS policy:

- GPU/CUDA/NVIDIA detection or use requires escalated permissions.
- Claude Code calls require escalated/trusted permissions.
- CPU-only runs must set `CUDA_VISIBLE_DEVICES=-1` before framework import and
  record that choice in the artifact.

## What Not To Reopen

Do not reopen these unless the user explicitly redirects:

- whether the local all-grid/operator route is source-faithful; it is not, it
  remains `extension_or_invention`;
- whether UKF can close source-faithfulness or correctness; it cannot;
- whether FD/JVP/ForwardAccumulator is the analytical source-route derivative;
  it remains diagnostic-only under the Phase 4 blocker;
- whether Phase 6 authorized Phase 7 execution; it did not;
- whether current grid-CDF mechanics are production KR closure; they are not.

## Immediate Next Safe Action

The next safe action is to refresh Phase 7 into an executable-or-blocked
subplan, with exact commands/artifacts and a clear approval request.

If no budget-compliant fit artifacts or exact executable path can be frozen,
write a Phase 7 blocker result instead of launching a run.
