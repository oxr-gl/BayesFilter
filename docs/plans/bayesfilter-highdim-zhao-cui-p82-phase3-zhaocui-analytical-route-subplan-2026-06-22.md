# P82 Phase 3 Subplan: Zhao-Cui Analytical Comparator Route Audit / Repair

status: DRAFT_PENDING_REVIEW
date: 2026-06-22
phase: P3

## Phase Objective

Audit the current checkout for the correct Zhao-Cui analytical derivative
route for the SIR d=18 comparator and either:

- identify the already-implemented analytical route with exact code, paper, and
  author-source anchors; or
- patch the narrow route needed to use that analytical derivative as the
  comparator while keeping autodiff/JVP diagnostic-only; or
- write a blocker result if no source-grounded analytical route can be safely
  identified or repaired.

P3 is a comparator-route gate.  It is not an LEDH run and not a GPU phase.
P3 begins with a no-edit discovery phase.  Comparator-route edits are forbidden
until that inventory is recorded in the P3 result or an interim P3 inventory
note.

## Entry Conditions Inherited From Previous Phase

- P2 harness protocol repair passed focused CPU-only checks.
- Regression FD remains diagnostic-only and not an oracle.
- Current multistate SIR score surface exists, but P1 found it still records
  `target_derivative_backend = tensorflow_forward_accumulator_for_model_log_density`.
- P81/P82 corrections remain binding: Zhao-Cui is approximate, not an oracle;
  the analytical derivative route is intended comparator; autodiff/JVP is
  diagnostic-only.
- Zhao-Cui source-anchor gate is binding: paper/math and local author-source
  anchors are required before any source-faithfulness or comparator-route
  approval.

## Required Artifacts

- P3 result markdown:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase3-zhaocui-analytical-route-result-2026-06-22.md`
- Decision table and run manifest inside the P3 result.  If route
  classification changes materially, also write a reset memo or explicit
  reset-memo section in the P3 result.
- Focused code diff only if audit shows a narrow repair is possible.
- Focused tests under `tests/highdim/` if code is patched.
- Updated P82 execution ledger.
- Draft P4 GPU/tiny LEDH smoke subplan only if P3 passes.
- Claude read-only review note for route classification and any patch.

## Required Read-Only Inventory Checks

Run before any code edits:

```bash
rg -n "ForwardAccumulator|target_derivative_backend|multistate_nonlinear_fixed_design_tt_score_path|scalar_nonlinear_initial_adjacent_target_derivative_batch|multistate_nonlinear_initial_adjacent_target_derivative_batch|multistate_nonlinear_transition_adjacent_target_derivative_batch" bayesfilter/highdim/filtering.py tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_p81_analytical_sir_score.py
rg -n "fixed-branch|Analytical gradient differentiates|Proposition 2|same-scalar|adaptive TT-cross|rank-changing|log-normalizer derivative" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-* docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-* docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-* docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-*
rg -n "P58_M9_AUTHOR_SIR_TARGET_ID|_P59_9B_AUTHOR_SIR_SOURCE_ANCHORS|_P59_9C_AUTHOR_SIR_SOURCE_ANCHORS|fixed_ttsirt_source_route|transition_log_density|observation_log_density|source_anchors" bayesfilter/highdim/source_route.py tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py
sed -n '1,80p' third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m
file third_party/audit/tensor-ssm-paper-demo/models/sir_austria/like.mlx third_party/audit/tensor-ssm-paper-demo/models/sir_austria/transition.mlx third_party/audit/tensor-ssm-paper-demo/models/sir_austria/sir_step.mlx
```

If code edits are made, run focused CPU-only checks:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest <focused P3 tests> -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/highdim/filtering.py bayesfilter/highdim/models.py <focused P3 tests>
git diff --check -- bayesfilter/highdim/filtering.py bayesfilter/highdim/models.py <focused P3 tests> docs/plans/bayesfilter-highdim-zhao-cui-p82-*
```

If P3 edits or approves any comparator route, it must also run and record a
targeted backend-label verification.  The exact check may be a focused pytest
or a small CPU-only diagnostic, but it must assert that:

- the promoted comparator route emits an analytical, source-backed backend
  label only when justified by the P3 route classification;
- the promoted analytical comparator path does not traverse
  `ForwardAccumulator`, JVP, or autodiff for the claimed analytical derivative;
- diagnostic JVP/autodiff paths remain explicitly labeled diagnostic.

This backend-label verification is a required check, not merely a next-phase
handoff preference.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is there an already-implemented Zhao-Cui analytical derivative route that is source-backed and suitable as the governed comparator for SIR d=18 gradient testing? |
| Baseline/comparator | The current diagnostic/JVP/ForwardAccumulator route is the non-promotable baseline for audit, not a comparator oracle; candidate routes are compared against P11/P12/P15/P16 fixed-branch derivative artifacts and local author source under `third_party/audit/zhao_cui_tensor_ssm_p10`. |
| Primary criterion | A route may be called comparator-ready only if its derivative terms are paper/project/source-backed, classified per route/variant, and the promoted path does not use ForwardAccumulator/JVP/autodiff for the claimed analytical derivative. Otherwise P3 writes a blocker. |
| Veto diagnostics | Any remaining ForwardAccumulator/JVP/autodiff on the promoted analytical path; missing paper/source/code anchor; multistate step justified only by analogy; source-faithful label on all-grid/local-operator inventions; hidden theta/data/scalar mismatch; broad route refactor; GPU/research run launched; unsupported HMC/posterior/default/scientific claims. |
| Explanatory diagnostics | FD agreement, autodiff/JVP agreement, search hits, code anchors, proof ledger anchors, author-source anchors, focused test output, finite-value smoke output if any. |
| Not concluded | Numerical FD/JVP agreement does not establish source-faithfulness; no LEDH gradient validity, posterior correctness, exact likelihood correctness, HMC readiness, adaptive Zhao-Cui differentiability, broad source-faithfulness, or scientific superiority is concluded. |
| Artifact preserving result | P3 result markdown with decision table, run manifest, route classification table, and tests/diff if patched. |

## Skeptical Plan Audit Checklist

Before implementation, P3 must record whether:

- the candidate route differentiates the same scalar that the comparator value
  path computes;
- the route is the user-intended analytical derivative path, not a JVP/autodiff
  substitute;
- numerical agreement with FD or JVP is treated as explanatory only and never
  as source-faithfulness evidence;
- every source-faithfulness statement has both project proof/paper anchors and
  local author-source anchors;
- the no-edit discovery inventory has enumerated candidate derivative
  implementations, backend-label emission sites, all ForwardAccumulator/JVP
  uses touching the comparator path, and all local source anchors relied upon;
- any fixed-HMC adaptation only freezes branch/randomness/schedules and does
  not invent a different transition/filtering route;
- the d=18 SIR theta convention remains `log_kappa_scale`, `log_nu_scale`,
  `log_obs_noise_scale`;
- no CPU smoke is interpreted as GPU viability or research validation;
- no comparator route is called an oracle.

If any item fails and cannot be repaired narrowly, write a blocker result.

## Route Classification Rules

Every proposed implementation choice must be classified before code is written,
and classification is per derivative route and per state variant.  A
single-state or scalar formula cannot promote the multistate SIR route by
analogy unless the multistate derivation/source support is documented.

| Class | Meaning |
|---|---|
| `source_faithful` | Matches cited author paper/source operation, with source file and line anchors. |
| `fixed_hmc_adaptation` | Preserves author algorithmic route but freezes randomness, ranks, bases, schedules, or samples for differentiability/HMC; still cites the source route being adapted. |
| `extension_or_invention` | Not present in author paper/source; may be useful, but cannot close a source-faithfulness or analytical-comparator gap unless explicitly approved. |

The current all-grid multistate score path and the ForwardAccumulator/JVP target
derivative must start as `extension_or_invention` or diagnostic-only until P3
proves otherwise.

If no already-implemented source-backed analytical multistate comparator exists,
do not invent one under comparator labeling.  Record the missing route as
`extension_or_invention` and stop with
`BLOCK_P82_P3_ANALYTICAL_COMPARATOR_ROUTE_NOT_READY`.

## Proposed P3 Work Sequence

1. Run the read-only inventory checks and write a route classification table.
   This no-edit discovery must enumerate candidate analytical derivative
   implementations, backend-label emission sites, ForwardAccumulator/JVP uses,
   and relied-upon source anchors.
2. Identify whether the analytical derivative is already implemented in code.
3. Only after the no-edit discovery is recorded, if a source-backed analytical
   route is present, wire the comparator to that implementation with focused
   tests.
4. If an analytical helper is missing inside an already-implemented,
   source-backed, already-classified multistate comparator route, patch only
   that helper and focused tests.  This exception cannot create a comparator
   route where the source-backed multistate route itself is absent.
5. If the only available route is ForwardAccumulator/JVP or a broad all-grid
   invention, write `BLOCK_P82_P3_ANALYTICAL_COMPARATOR_ROUTE_NOT_READY`.
6. Review P3 result and any P4 subplan with Claude using compact fact packets.

## Forbidden Claims / Actions

- Do not call Zhao-Cui an oracle.
- Do not claim broad source-faithfulness without paper/source line anchors.
- Do not claim source-faithfulness from numerical agreement with FD, JVP, or
  autodiff.
- Do not use ForwardAccumulator/JVP as the primary comparator.
- Do not run GPU/CUDA/NVIDIA commands in P3.
- Do not launch LEDH N=1000/N=10000 runs.
- Do not claim posterior correctness, HMC readiness, exact likelihood
  correctness, default-gradient readiness, or scientific superiority.
- Do not revert unrelated dirty worktree changes.

## Exact Next-Phase Handoff Conditions

P4 may begin only if:

- P3 result exists;
- the comparator route is either passed with exact paper/source/code anchors and
  focused tests, or a blocker is written and the master program is updated to
  stop before GPU comparison;
- no ForwardAccumulator/JVP-backed route is promoted;
- backend metadata for any promoted comparator route has an analytical,
  source-backed label only when justified, and diagnostic JVP/autodiff paths
  remain labeled diagnostic;
- P4 subplan exists and includes trusted/escalated GPU preflight requirements.

## Stop Conditions

Stop and write a blocker result if:

- no already-implemented analytical route can be found and a narrow repair is
  not source-grounded;
- source files needed for anchors are unreadable and no reviewed source ledger
  can substitute;
- the analytical route would require a broad rewrite of TT/SIRT filtering;
- code edits would collide with unrelated dirty worktree changes;
- passing P3 would depend on treating autodiff/JVP, regression FD, or LEDH as
  an oracle.

## End-of-Phase Duties

At the end of P3:

1. run the required local checks;
2. write the P3 result / close record;
3. draft or refresh the P4 subplan only if P3 passes;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. use Claude as read-only reviewer for any material route classification or
   patch, stopping after five rounds for the same blocker.
