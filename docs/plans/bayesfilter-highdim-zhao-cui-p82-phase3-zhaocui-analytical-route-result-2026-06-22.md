# P82 Phase 3 Result: Zhao-Cui Analytical Comparator Route Audit

status: BLOCK_P82_P3_ANALYTICAL_COMPARATOR_ROUTE_NOT_READY
date: 2026-06-22
phase: P3

## Question

Is there an already-implemented Zhao-Cui analytical derivative route that is
source-backed and suitable as the governed comparator for SIR d=18 gradient
testing, with autodiff/JVP remaining diagnostic-only?

## Decision

P3 stops the P82 program before GPU comparison.  The current checkout contains
project derivations for a fixed-branch same-scalar analytical derivative, and it
contains source-route anchors for bounded fixed-TTSIRT SIR assembly.  It does
not contain an already-implemented, source-backed multistate SIR d=18
analytical comparator route for P82.

The runnable multistate score path still labels its target derivative backend as
`tensorflow_forward_accumulator_for_model_log_density`, and the multistate
target-derivative helpers call the ForwardAccumulator-backed scalar derivative.
Under the P3 subplan, that route cannot be promoted to the Zhao-Cui analytical
comparator.  Autodiff/JVP may remain diagnostic-only.

No comparator-route code edits were made in P3.  No GPU, LEDH, N=1000, or
N=10000 run was launched.  P4 is not handed off.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is there an already-implemented Zhao-Cui analytical derivative route that is source-backed and suitable as the governed comparator for SIR d=18 gradient testing? |
| Baseline/comparator | The current diagnostic/JVP/ForwardAccumulator route is the non-promotable audit baseline; candidate routes are compared against P11/P12/P15/P16 fixed-branch derivative artifacts and local author source anchors. |
| Primary criterion | A route may be called comparator-ready only if its derivative terms are paper/project/source-backed, classified per route/variant, and the promoted path does not use ForwardAccumulator/JVP/autodiff for the claimed analytical derivative. |
| Veto diagnostics | Any remaining ForwardAccumulator/JVP/autodiff on the promoted analytical path; missing paper/source/code anchor; multistate step justified only by analogy; broad route invention; GPU/research run launched; unsupported oracle/HMC/posterior/default/scientific claims. |
| Explanatory diagnostics | Search hits, code anchors, proof-ledger anchors, author-source anchors, focused no-edit inventory output. |
| Not concluded | No LEDH gradient validity, posterior correctness, exact likelihood correctness, HMC readiness, broad source-faithfulness, default-gradient readiness, or scientific superiority is concluded. |
| Artifact preserving result | This P3 result, P82 execution ledger, Claude review ledger if reviewed, and stop handoff. |

## Skeptical Plan Audit

Pass as a stop decision.  The no-edit inventory answered the P3 question.  The
candidate runnable path does not satisfy the primary criterion because it still
uses ForwardAccumulator/JVP for target log-density derivatives.  The derivation
ledgers are project evidence for what a same-scalar analytical route must do;
they are not evidence that the current multistate SIR d=18 route has already
implemented that route.  Treating numerical FD/JVP agreement as comparator
readiness would violate the P3 veto diagnostics.

## No-Edit Inventory Summary

### Current Runnable Score Path

| Evidence | Finding |
|---|---|
| `bayesfilter/highdim/filtering.py:1466` | Multistate score diagnostics emit `target_derivative_backend = "tensorflow_forward_accumulator_for_model_log_density"` for the multi-parameter path. |
| `bayesfilter/highdim/filtering.py:1507` | Initial multistate target derivative is routed through `multistate_nonlinear_initial_adjacent_target_derivative_batch`. |
| `bayesfilter/highdim/filtering.py:1524` | Transition multistate target derivative is routed through `multistate_nonlinear_transition_adjacent_target_derivative_batch`. |
| `bayesfilter/highdim/filtering.py:2550` to `bayesfilter/highdim/filtering.py:2555` | Initial target derivative calls `_scalar_target_log_derivative_by_forward_accumulator`. |
| `bayesfilter/highdim/filtering.py:2632` to `bayesfilter/highdim/filtering.py:2641` | Transition observation derivative calls `_scalar_target_log_derivative_by_forward_accumulator`. |
| `bayesfilter/highdim/filtering.py:2653` to `bayesfilter/highdim/filtering.py:2658` | Transition derivative diagnostics emit `derivative_backend = "tensorflow_forward_accumulator_for_model_log_density"`. |
| `bayesfilter/highdim/filtering.py:4316` to `bayesfilter/highdim/filtering.py:4325` | `_scalar_target_log_derivative_by_forward_accumulator` uses `tf.autodiff.ForwardAccumulator`. |

### Derivation And Source Anchors

| Evidence | Finding |
|---|---|
| `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-proposition-proof-ledger-2026-05-31.md:40` to `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-proposition-proof-ledger-2026-05-31.md:64` | Proposition 2 is a human-reviewed project derivation for the declared fixed-branch approximate likelihood, not a broad adaptive-code derivative. |
| `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-gradient-derivation-ledger-2026-05-31.md:18` to `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-gradient-derivation-ledger-2026-05-31.md:39` | P15 identifies the fixed-branch scalar and obligations, with a scalar reference-example parity check. |
| `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-claim-support-ledger-2026-06-01.md:26` to `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-claim-support-ledger-2026-06-01.md:31` | P16 supports fixed-branch recursion and derivative as project derivations and states the runnable-program gap. |
| `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.tex:776` to `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.tex:799` | The implementation checklist requires derivative objects including core sensitivities, previous-filter sensitivities, normalizer derivatives, and same-scalar diagnostics. |
| `bayesfilter/highdim/source_route.py:2199` to `bayesfilter/highdim/source_route.py:2209` | Source-route artifacts preserve author SIR fixed-TTSIRT anchors for bounded preparation evidence. |
| `bayesfilter/highdim/source_route.py:3042` to `bayesfilter/highdim/source_route.py:3111` | Source-route step-spec assembly records `fixed_ttsirt_source_route`, source anchors, retained carry, and previous marginal evidence. |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14` to `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:56` | Author SIR example declares `m = 18`, `T = 20`, FTT options, and SIRT solve/smoothing calls. |
| `third_party/audit/tensor-ssm-paper-demo/models/sir_austria/like.mlx`, `transition.mlx`, `sir_step.mlx` | Local author model files are Microsoft OOXML `.mlx` files, so the P3 audit records their availability but does not claim fresh line-level analytical-derivative extraction from them. |

## Route Classification

| Candidate route | Classification | Reason |
|---|---|---|
| Current `multistate_nonlinear_fixed_design_tt_score_path` target-derivative path | diagnostic-only / `extension_or_invention` for comparator purposes | Runnable, but backend metadata and helper internals use TensorFlow ForwardAccumulator for target log-density derivatives. |
| P12/P15/P16 fixed-branch same-scalar analytical derivative contract | `fixed_hmc_adaptation` as a derivation/specification, not a ready implementation | It gives the fixed-branch analytical obligations but does not by itself provide the implemented multistate SIR d=18 comparator route. |
| Source-route bounded fixed-TTSIRT SIR assembly in `source_route.py` | `source_faithful` for bounded source-route assembly only | It preserves author SIR/source-route anchors, but P3 did not find a wired analytical derivative comparator on this route. |
| A new analytical multistate comparator patched from the derivation during P3 | `extension_or_invention` if created here | The P3 subplan forbids inventing a missing comparator route under comparator labeling. |

## Required Inventory Commands

Run in `/home/chakwong/BayesFilter`:

```bash
rg -n "ForwardAccumulator|target_derivative_backend|multistate_nonlinear_fixed_design_tt_score_path|scalar_nonlinear_initial_adjacent_target_derivative_batch|multistate_nonlinear_initial_adjacent_target_derivative_batch|multistate_nonlinear_transition_adjacent_target_derivative_batch" bayesfilter/highdim/filtering.py tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_p81_analytical_sir_score.py
rg -n "fixed-branch|Analytical gradient differentiates|Proposition 2|same-scalar|adaptive TT-cross|rank-changing|log-normalizer derivative" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-* docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-* docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-* docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-*
rg -n "P58_M9_AUTHOR_SIR_TARGET_ID|_P59_9B_AUTHOR_SIR_SOURCE_ANCHORS|_P59_9C_AUTHOR_SIR_SOURCE_ANCHORS|fixed_ttsirt_source_route|transition_log_density|observation_log_density|source_anchors" bayesfilter/highdim/source_route.py tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py
sed -n '1,80p' third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m
file third_party/audit/tensor-ssm-paper-demo/models/sir_austria/like.mlx third_party/audit/tensor-ssm-paper-demo/models/sir_austria/transition.mlx third_party/audit/tensor-ssm-paper-demo/models/sir_austria/sir_step.mlx
```

Observed status: completed as no-edit inventory.  These commands support the
blocker decision above.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Stop P82 at P3 | Failed: no ready source-backed analytical multistate comparator found | Veto triggered by ForwardAccumulator/JVP on the candidate promoted path | A future narrow implementation may be possible, but it is not already present | Write a dedicated comparator-route implementation subplan or ask for human direction | No LEDH validation or gradient claim |
| Preserve JVP/autodiff only as diagnostic | Passed | No JVP path promoted | JVP may remain useful for focused debugging | Keep diagnostic labeling explicit | No comparator certification |
| Do not draft P4 GPU subplan | Passed | GPU/LEDH work would lack the governed comparator | None for P82 as currently scoped | Stop and hand off blocker | No GPU evidence |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `5ea363e` |
| Working directory | `/home/chakwong/BayesFilter` |
| Date/time | `2026-06-22T05:10:58+08:00` |
| Phase | P3 |
| CPU/GPU status | No GPU commands run; no TensorFlow GPU initialization. |
| Commands | Read-only `rg`, `sed`, `nl`, `file`, `git rev-parse`, `pwd`, and `date` inventory commands. |
| Code edits | None in comparator route. |
| New artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase3-zhaocui-analytical-route-result-2026-06-22.md` |
| Random seeds | N/A |
| Runtime budget | Short no-edit inventory only |

## Stop Handoff

P82 stops here with
`BLOCK_P82_P3_ANALYTICAL_COMPARATOR_ROUTE_NOT_READY`.

Exact blocker:

- The intended comparator is the Zhao-Cui analytical derivative route.
- The current runnable multistate SIR d=18 score path still depends on
  ForwardAccumulator/JVP for target derivatives.
- The source-route and derivation artifacts are not yet a wired analytical
  comparator implementation for this target.

Next safe human decision:

- authorize a new dedicated phase/program to implement the source-backed
  fixed-branch analytical multistate SIR comparator route; or
- explicitly approve a different comparator boundary, with JVP/autodiff clearly
  labeled diagnostic/non-oracle if used.

## Nonclaims

This result does not conclude posterior correctness, exact likelihood
correctness, HMC readiness, default-gradient readiness, LEDH gradient validity,
manual-adjoint correctness, streaming memory improvement, scientific
superiority, or production readiness.
