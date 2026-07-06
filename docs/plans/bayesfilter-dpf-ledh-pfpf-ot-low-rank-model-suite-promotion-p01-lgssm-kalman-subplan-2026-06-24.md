# P01 LGSSM Exact-Kalman Gate Subplan

Date: 2026-06-24

Status: `FAIL_STOP_P01_HARD_ROUTE_DIAGNOSTIC_VETO`

## Phase Objective

Implement and validate the missing LGSSM exact-Kalman low-rank LEDH-PFPF-OT
gate before any trusted P01 runtime is launched. P01 must first create a
concrete TensorFlow/TFP-oriented harness and focused tests for the pinned LGSSM
cases. Only after that implementation subgate passes review may the same phase
advance to trusted GPU runtime under a separate explicit approval.

The eventual runtime question remains: test the locked low-rank LEDH-PFPF-OT
route on LGSSM cases where exact Kalman filtering supplies a reference for
filtered means, variances, and log likelihood. P01 is the first quality gate
that can distinguish "fast route" from "acceptable filtering component" under
an exact oracle.

P01 does not by itself promote the algorithm beyond LGSSM. Passing P01 is a
required but insufficient condition for model-suite promotion.

## Pinned LGSSM Case And Tolerance Contract

These cases, seeds, and tolerances are fixed before P01 runtime. They may be
changed only by a visible pre-runtime subplan repair that resets P01 status and
reruns local/Claude review.

| Case id | Role | State dim | Obs dim | Time steps | Particles | Seeds | Mean RMSE max | Variance RMSE max | Loglik abs delta max |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| `lgssm_small_exact_ref` | smoke/exact-reference sanity | 4 | 3 | 12 | 1024 | `91001,91002,91003` | `0.25` | `0.35` | `12.0` |
| `lgssm_medium_exact_ref` | promotion quality screen | 16 | 8 | 20 | 2048 | `91011,91012,91013` | `0.35` | `0.50` | `25.0` |
| `lgssm_informative_obs_stress` | high-information stress | 16 | 12 | 20 | 2048 | `91021,91022,91023` | `0.45` | `0.65` | `35.0` |

The tolerances are gross engineering screens, not posterior-equivalence or
statistical-superiority claims. They are deliberately loose enough to detect
obvious filtering-quality breakage while allowing finite-particle Monte Carlo
variation. Passing them keeps the candidate viable; it does not prove
superiority.

Required hard screens for every row:

- exact Kalman reference finite;
- streaming and low-rank outputs finite;
- filtered mean, filtered variance, and log-likelihood metrics present;
- low-rank route fired at every active transport step;
- no dense transport materialized by the low-rank route;
- GPU/TF32/XLA provenance present for GPU claims;
- candidate settings match the locked candidate.

## Entry Conditions Inherited From Previous Phase

- P00 governance result exists and passes as
  `PASS_P00_READY_FOR_P01_IMPLEMENTATION_REFRESH`.
- Master program, runbook, ledgers, stop handoff, and P01 subplan review have
  converged.
- Candidate remains locked to `r16_eps0p25_alpha1em08_it120`.
- Current comparator remains streaming GPU/TF32 LEDH-PFPF-OT.
- Exact reference for this phase is LGSSM Kalman filtering only.
- P00 executable-surface audit found no concrete checked-in harness/test for
  the preferred P01 exact-Kalman gate paths.
- No approval is inherited for HMC readiness, public API changes, package
  default changes, package installs, network fetches, destructive git
  operations, or scientific claims.
- Trusted GPU runtime requires explicit approval before P01 execution.

## Required Artifacts

- Always required before any P01 runtime:
  - P01A implementation result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p01-lgssm-kalman-implementation-result-2026-06-24.md`
  - New exact-Kalman harness:
  `docs/benchmarks/benchmark_low_rank_ledh_lgssm_kalman_gate.py`
  - New focused test:
  `tests/test_low_rank_ledh_lgssm_kalman_gate.py`
- Required if P01A fails or P01B runtime is unavailable, unapproved, or
  blocked:
  - P01 blocker result:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p01-lgssm-kalman-blocker-2026-06-24.md`
  - Optional P02 planning draft, labeled `P02_DRAFT_NO_EXECUTION_AUTHORIZED`:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p02-actual-sir-stress-subplan-2026-06-24.md`
- Required only if P01B trusted GPU runtime is explicitly approved and run:
  - P01 runtime result:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p01-lgssm-kalman-result-2026-06-24.md`
  - P02 executable refreshed subplan:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p02-actual-sir-stress-subplan-2026-06-24.md`
  - Structured LGSSM benchmark JSON:
    `docs/benchmarks/low-rank-ledh-model-suite-p01-lgssm-kalman-2026-06-24.json`
  - LGSSM benchmark Markdown:
    `docs/benchmarks/low-rank-ledh-model-suite-p01-lgssm-kalman-2026-06-24.md`
  - Command log:
    `docs/logs/low-rank-ledh-model-suite-promotion-2026-06-24/p01-lgssm-kalman.log`
- Existing implementation surfaces to reuse where feasible:
  - `experiments/dpf_implementation/tf_tfp/fixtures/lgssm_tf.py`
  - `experiments/dpf_implementation/tf_tfp/references/kalman_lgssm_tf.py`
  - `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
  - `experiments/dpf_implementation/tf_tfp/resampling/streaming.py`
  - `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py`

## Required Checks, Tests, And Reviews

- P01A implementation-before-runtime checks:
  - implement only the new harness/test plus plan/result/ledger artifacts;
  - preserve TensorFlow/TFP as the implementation backend;
  - keep the candidate route as TensorFlow tensors through the filtering and
    low-rank transport path;
  - allow Python/reporting conversions only outside compiled or
    differentiable algorithmic paths, and label them as reporting;
  - compile-check the new harness and test;
  - run focused pytest for the new test;
  - run a no-active-path-NumPy audit on the new harness/test and the touched
    low-rank path;
  - run a command-shape/debug smoke only if it is short and explicitly labeled
    non-GPU-evidence.
- P01A implementation review:
  - local skeptical audit before code changes;
  - Claude Opus/max read-only review of the refreshed P01 subplan before code
    implementation;
  - after implementation, local review of harness contract, artifact coverage,
    and boundary safety;
  - Claude read-only review of material implementation result if local checks
    expose a material ambiguity.
- P01B runtime checks, only after P01A passes and trusted GPU approval is
  explicitly recorded:
  - trusted GPU precheck using `nvidia-smi`;
  - trusted GPU LGSSM exact-reference benchmark with paired streaming and
    low-rank rows, fixed seeds, fixed shapes, TF32 enabled, XLA provenance, and
    exact Kalman reference recorded;
  - post-run structured artifact validator checking finite references/outputs,
    low-rank and streaming route-fired evidence, exact-reference metrics,
    predeclared tolerance status, nonmaterialization evidence, and GPU/TF32/XLA
    provenance;
  - Claude Opus/max read-only review of P01 result and refreshed P02 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the locked low-rank route preserve LGSSM filtering quality against exact Kalman references while retaining route/provenance validity? |
| Baseline/comparator | Exact Kalman for correctness; streaming GPU/TF32 LEDH-PFPF-OT for route comparison. |
| Primary pass criterion | P01A: concrete harness/test exists and passes focused local checks without active-path NumPy or boundary drift. P01B: low-rank passes hard finite/provenance/nonmaterialization screens and the pinned Kalman-error screens across all P01 cases and seeds. |
| Veto diagnostics | Nonfinite reference/output, missing Kalman metrics, low-rank quality above tolerance, route mismatch, active-path NumPy, dense materialization, missing GPU/TF32/XLA provenance, or missing artifacts. |
| Explanatory diagnostics | Timings, memory, ESS, seed variation, and streaming-vs-low-rank descriptive differences. |
| Not concluded | No broad model-suite promotion, statistical superiority, nonlinear posterior correctness, dense equivalence, HMC readiness, public API readiness, or package default readiness. |
| Artifact | P01A implementation result and harness/test always; P01 blocker result if runtime cannot proceed; P01 runtime result plus JSON/Markdown/log only if trusted GPU runtime is explicitly approved and run; review ledger; execution ledger. |

## Skeptical Pre-Execution Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: P01 uses exact Kalman for LGSSM quality and streaming only as route comparator. |
| Proxy metric promoted | Guarded: timing, ESS, and memory are explanatory unless a hard route/provenance screen fails. |
| Missing stop conditions | Guarded: missing harness blocks runtime; failed focused checks stop before GPU runtime. |
| Unfair comparison | Guarded: runtime rows must share seeds, shapes, dtype, TF32 mode, GPU, and candidate settings. |
| Hidden assumptions | Guarded: P01A must implement pinned fixture definitions before P01B runtime. |
| Stale context | Guarded: P00 found the harness missing; this refresh repairs that exact gap. |
| Environment mismatch | Guarded: P01A local checks make no GPU claim; P01B requires trusted GPU approval/provenance. |
| Artifact mismatch | Guarded: harness, test, JSON, Markdown, log, result, and next subplan paths are named. |

Audit conclusion: P01 may proceed only as an implementation-before-runtime
phase until local checks and review converge. P01 trusted GPU runtime remains
blocked pending explicit approval after P01A.

## Forbidden Claims And Actions

- Do not claim full promotion from LGSSM alone.
- Do not claim statistical superiority from few seeds or descriptive timing.
- Do not treat synthetic LGSSM-shaped efficiency evidence as exact-Kalman
  quality evidence unless exact Kalman metrics are present.
- Do not change P01 case set, seeds, or tolerances after seeing runtime
  results.
- Do not change candidate settings after seeing results.
- Do not run P01 trusted GPU runtime before the harness/test exists, focused
  checks pass, implementation result is written, and explicit trusted-GPU
  approval is recorded.
- Do not use NumPy in BayesFilter-owned algorithmic implementation paths.
- Do not add PyTorch or JAX.
- Do not run HMC/autodiff runtime.
- Do not change public API, package metadata, model files, dependencies, or
  default policy.

## Exact Next-Phase Handoff Conditions

P01 hands off to P02 only if:

- P01A implementation result exists, focused local checks passed, and the
  harness/test pair exists at the named paths;
- P01 trusted GPU runtime was explicitly approved after P01A and completed;
- P01 result is written with a decision table and inference-status table;
- local validators pass;
- Claude review of P01/P02 returns `VERDICT: AGREE`;
- P02 subplan is refreshed to use P01's actual result and preserve actual-SIR
  stress boundaries.

If P01 trusted GPU runtime is unavailable, unapproved, or blocked, P01 must
write a reviewed blocker result and stop execution at P01. It may draft or
refresh P02 only as a non-executable planning artifact labeled
`P02_DRAFT_NO_EXECUTION_AUTHORIZED`; that draft does not authorize P02 runtime
or continuation of the model-suite gate.

If P01 fails the exact-Kalman quality screen, P02 may proceed only if the P01
result classifies the failure as harness invalidity or repairable diagnostic
gap. A true candidate quality failure is a promotion veto and should hand off
to P08 or a repair plan, not silent continuation.

## Stop Conditions

- No exact Kalman reference can be produced or validated.
- P01 exact-Kalman harness/validator is missing and cannot be created within an
  approved P01 implementation write set.
- Focused local checks fail in a way that invalidates the harness.
- Trusted GPU runtime is unavailable or unapproved.
- Low-rank route does not fire or materializes dense transport in the default
  path.
- Active-path NumPy or `.numpy()` barrier appears in candidate implementation.
- Candidate fails LGSSM quality tolerance under a valid harness.
- Claude/Codex review does not converge within five rounds for the same
  blocker.

## End-Of-Subplan Procedure

1. Run required local checks.
2. Write P01A implementation result before runtime.
3. If P01A passes and runtime is approved, run P01B runtime checks and write
   P01 result or blocker result.
4. Draft or refresh P02 subplan.
5. Review P02 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
6. If P01B runtime is blocked, label any P02 refresh
   `P02_DRAFT_NO_EXECUTION_AUTHORIZED` and stop at P01.
