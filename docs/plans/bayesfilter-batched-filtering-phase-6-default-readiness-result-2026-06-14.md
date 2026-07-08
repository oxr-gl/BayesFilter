# Phase 6 Result: Default-Readiness Decision

Date: 2026-06-14

## Status

`FILTERING_PRODUCTION_CANDIDATE_READY_FOR_FILTER_LANE_REVIEW`

## Objective

Produce the final filtering-lane readiness decision for the experimental
batched filtering value+score work, separating engineering correctness,
filtering performance evidence, filtering API scope, remaining gaps, and
nonclaims.

## Decision

Correction: the earlier Phase 6 draft over-scoped filtering readiness by
treating an HMC/static-unroll downstream consumer test as a filtering gate.
That was the wrong lane.  Filtering should be verified independently using
filtering correctness, analytic score parity, JIT compatibility, CPU/GPU
behavior, numerical robustness, and filtering API policy.  HMC/NeuTra are
consumers and are not prerequisites for filtering production status.

Under that corrected filter-lane scope, the batched-over-parameters value+score
work is historically significant but is no longer the promoted UKF default
story.  The strict-SPD principal-square-root UKF route now occupies the promoted
scalar/public UKF role, while the old eigenderivative SVD-UKF lane remains a
historical filtering production-candidate result for the specific tested 2026-06
batched fixtures and a diagnostic/regression comparator.  It is not an
unconditional default across all filtering workloads.

Kalman has scalar parity, analytic score parity, interface tests, compiled
CPU/GPU benchmark evidence, and large-batch artifacts.  The historical batched
SVD-UKF lane has scalar parity on the realistic affine fixture, small
nonlinear/fail-closed branch coverage, interface tests, and compiled GPU
benchmark evidence, but its current role after the principal-square-root
promotion is diagnostic comparison rather than the HMC-facing promoted route.

No unconditional default, public export change, HMC/NeuTra readiness,
posterior-validity, broad model-coverage, statistically supported speed-ranking,
or CUT4 readiness claim is made.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Decision question | Answered: the current filtering evidence supports a production-candidate filtering path for tested Kalman and SVD-UKF scopes, not an unconditional default. |
| Baseline/comparator | Scalar filtering value+score authority paths, scalar-row parity tests, filtering interface tests, filtering export scan, and JIT-only benchmark artifacts. |
| Primary criterion | Passed for filtering production-candidate status: the decision table and inference-status table separate Kalman evidence, SVD-UKF evidence, trusted/JIT performance provenance, filtering default-policy blockers, human approvals, and nonclaims. |
| Promotion veto diagnostics | Unconditional filtering default promotion is vetoed by missing human API/default approval, limited model coverage, working-tree/release reproducibility gaps, scalar SVD compiled-loop comparator infeasibility, and missing production docs/CI policy. |
| Explanatory diagnostics | Phase 4 benchmark timings, capacity timeouts, scalar comparator infeasibility, and TensorFlow warnings are explanatory only. |
| Not concluded | No unconditional filtering default, no HMC/NeuTra readiness, no posterior quality, no CUT4 readiness, no broad model coverage, no statistically supported speed ranking. |

## Pre-Decision Checks

| Check | Result |
| --- | --- |
| Phase 0-4 filtering result files exist | Passed. Phase 5 HMC/static-unroll consumer evidence is historical only and is not used as a filtering production gate. |
| Phase 1-4 filtering checks recorded as passing | Passed in result files: Phase 1 `19 passed`; Phase 2 `19 passed` plus scalar nonlinear subset `6 passed, 12 deselected`; Phase 3 `35 passed`; Phase 4 `45 passed`. |
| Experimental public export/default guard | Passed: `rg -n "experimental_batched_value_score|experimental_batched_kalman|experimental_batched_svd" bayesfilter/__init__.py bayesfilter/linear/__init__.py bayesfilter/nonlinear/__init__.py` returned empty output. |
| GPU JSON JIT/device/finite-output guard | Passed for six batched GPU artifacts: Kalman and SVD-UKF at `B=20`, `B=256`, and `B=4096` all record `jit_compile: true`, finite outputs, and value/score device placement on `GPU:0`. |
| Trusted GPU provenance | Passed: Phase 4 records that GPU timing rows were JIT/XLA compiled and run in trusted context with `CUDA_VISIBLE_DEVICES=1`, TensorFlow logical `/GPU:0`, NVIDIA RTX 4080 SUPER. |
| HMC/downstream exclusion | Passed: HMC/static-unroll consumer evidence is excluded from filtering production criteria. |
| Snapshot scope | Current HEAD is `207419e49d2dbbc5c6aa3bca2f2ce450b6e2ffde`. Phases 3-5 have explicit manifests at this HEAD. Phases 0-2 do not have explicit commit manifests and are treated as result-file-scoped historical evidence. The current work is still in an uncommitted working tree, so release reproducibility remains a promotion gap. |

## End-Of-Phase Local Checks

| Check | Command summary | Result |
| --- | --- | --- |
| Filtering implementation/interface gate | `CUDA_VISIBLE_DEVICES=-1 ... pytest -q tests/test_experimental_batched_value_score_interface.py tests/test_experimental_batched_benchmark_harness.py tests/test_experimental_batched_linear_kalman_tf.py tests/test_experimental_batched_svd_sigma_point_tf.py tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py` | Passed: `40 passed`; TensorFlow/GAST warnings only. |
| Public package/HMC import checks | Not used as filtering gate. The earlier HMC/static-unroll downstream test was removed from the filtering test set. |
| Experimental export scan | `rg -n "experimental_batched_value_score|experimental_batched_kalman|experimental_batched_svd" bayesfilter/__init__.py bayesfilter/linear/__init__.py bayesfilter/nonlinear/__init__.py` | Empty output; no experimental batched export/default drift found. |

## Repair Loop Assessment

The material correction was scope-related, not a filtering implementation
failure.  The HMC/static-unroll downstream test was a consumer-boundary test,
not a filtering test, so it was removed from this filtering gate.  The
filtering lane is assessed from scalar parity, analytic score parity,
branch/fail-closed coverage, filtering interface tests, and compiled
CPU/GPU artifacts.

## Scope Decision Table

| Scope | Current status | Evidence supporting production-candidate use | Remaining default-readiness blockers | Human approval required | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Kalman batched value+score | Filtering production candidate for tested dense fixtures | Scalar value+score parity tests; interface wrapper; JIT CPU/GPU benchmark artifacts; large-batch parity artifacts | No public export/default approval; limited model/shape coverage; uncommitted artifact state; production docs/maintenance path missing | Required before public export or default selection | Broad model correctness, unconditional default |
| SVD-UKF batched value+score | Filtering production candidate for tested SVD-UKF fixtures | Affine realistic scalar value+score parity; small nonlinear scalar parity; fail-closed branch tests; interface wrapper; JIT GPU benchmark artifacts at `B=20/256/4096` | Scalar SVD compiled-loop comparator is currently XLA TraceType-infeasible; broader nonlinear and robustness coverage missing; no public export/default approval | Required before public export/default selection | Broad nonlinear accuracy, unconditional default |
| CUT4 | Outside this default-promotion program | None in this phase | Point count and scope excluded by reviewed plan | Required for any future CUT4-specific program | CUT4 readiness |
| CPU/GPU performance | Engineering diagnostic only | Phase 4 JIT-only GPU artifacts show finite compiled execution and descriptive warm timings; CPU capacity/infeasibility records are preserved | Single-shape/single-machine evidence; reduced repeats for large `B`; no statistical uncertainty; scalar SVD comparator infeasible | Required before marketing, default policy, or broad performance claims | Statistically supported speed ranking |
| HMC/NeuTra/posterior workflows | Out of filtering-lane scope | N/A | Must be tested by consumer-specific plans if those consumers adopt the filter | Required only for HMC/NeuTra claims | Filtering correctness does not imply sampler validity |
| Filtering default/public API | Production-candidate, not default | No experimental batched export/default drift; explicit module import path available | Human approval missing; release reproducibility and CI/maintenance gaps remain; default policy evidence incomplete | Required explicitly | Any default change |

## Benchmark Evidence Summary

All GPU timing rows below are descriptive engineering diagnostics from Phase 4.
They are JIT/XLA compiled and trusted-context device-placed, but they are not
statistical rankings or production benchmarks.

| Kernel | B | GPU warm median seconds | Per-filter GPU warm median seconds | Compile/first-call seconds | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| Kalman | 20 | 0.04977 | 0.002489 | 2.398 | finite |
| Kalman | 256 | 0.1388 | 0.000542 | 2.417 | finite |
| Kalman | 4096 | 1.6320 | 0.000398 | 4.386 | finite |
| SVD-UKF | 20 | 0.3735 | 0.01868 | 5.581 | finite |
| SVD-UKF | 256 | 0.7836 | 0.003061 | 6.021 | finite |
| SVD-UKF | 4096 | 7.7604 | 0.001895 | 13.960 | finite, one repeat |

Capacity and feasibility records remain part of the evidence:

- CPU `B=4096` timed out for batched Kalman and batched SVD-UKF within the
  Phase 4 visible timeout cap.
- Kalman scalar-loop GPU was only timed at `B=20`; larger scalar-loop GPU rows
  were recorded as capacity-not-run after the `B=20` cost.
- SVD-UKF scalar-loop compiled comparator was not timed because TensorFlow could
  not generate a `TraceType` for the scalar `TFStructuralStateSpace` object at
  the compiled wrapper boundary.

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for filtering production-candidate status; unconditional default promotion still has policy and coverage gaps. |
| Statistically supported ranking | Not established. Timings are descriptive single-shape diagnostics without uncertainty analysis. |
| Descriptive-only differences | Batched GPU execution is descriptively favorable in the tested compiled fixtures, especially at larger `B`, but this is not a statistical speed ranking. |
| Filtering production-candidate readiness | Established for the tested Kalman and SVD-UKF scopes. |
| Unconditional default-readiness | Not established. |
| Next evidence needed | Broader real-model filtering fixtures, CI/release reproducibility, documentation/API design, and explicit default-policy approval before any unconditional default proposal. |

## Remaining Production Gaps

1. Decide the filtering API/export shape with human approval.
2. Commit or otherwise freeze a reproducible release snapshot; the current
   evidence includes uncommitted working-tree files and generated artifacts.
3. Expand model coverage beyond the current deterministic fixtures, including
   time-varying, masked/missing-observation, and larger nonlinear cases where
   applicable.
4. Resolve or deliberately document the scalar SVD compiled comparator XLA
   boundary.
5. Add production-grade error handling, documentation, and CI-sized benchmarks.
6. Establish performance evidence with replication or an explicit production
   performance criterion before making broad speed claims.
7. Keep HMC/NeuTra/surrogate validation in separate consumer-lane plans.

## Claude Review Trail

Phase 6 subplan review:

- `docs/plans/bayesfilter-batched-filtering-phase-6-claude-review-round-01-2026-06-14.md`: `VERDICT: REVISE`
- `docs/plans/bayesfilter-batched-filtering-phase-6-claude-review-round-02-2026-06-14.md`: `VERDICT: AGREE`

The earlier Phase 6 result reviews are superseded by this filtering-lane
correction because they reviewed the over-scoped downstream/HMC framing.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Promote to filtering production-candidate status | Passed for tested Kalman and SVD-UKF filtering scopes | No scalar parity, nonfinite output, JIT/GPU provenance, or experimental export/default drift veto observed | Evidence is fixture-limited and working-tree-scoped | Decide public API/export/default policy | Unconditional default readiness |
| Do not make unconditional default yet | Default-readiness criterion not fully satisfied | Remaining vetoes: human approval, broader model coverage, release reproducibility, production docs/CI, scalar SVD comparator boundary | Which filtering API shape should be chosen is a human/product decision | Start a filtering productionization/API plan | Broad model coverage, statistical speed ranking |
| Exclude HMC/NeuTra from filtering gate | Passed | Consumer tests are not filtering correctness evidence | Consumer integration can still matter for those products | Keep consumer validation separate | Sampler convergence, posterior quality |
| Keep CUT4 out of scope | Passed | No CUT4 artifact used for promotion | Tiny CUT4 may still be useful in a separate niche plan | Require separate CUT4 plan if revived | CUT4 readiness |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `207419e49d2dbbc5c6aa3bca2f2ce450b6e2ffde` |
| Worktree status | Dirty/uncommitted; filtering result is scoped to current working tree plus recorded artifacts |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` for local checks |
| TensorFlow | `2.20.0` in prior phase manifests/checks |
| CPU/GPU status | Phase 6 local checks are CPU-only unless otherwise noted; Phase 4 GPU evidence used trusted `CUDA_VISIBLE_DEVICES=1` artifacts |
| Data version | Synthetic deterministic fixtures |
| Random seeds | N/A |
| Plan file | `docs/plans/bayesfilter-batched-filtering-phase-6-default-readiness-subplan-2026-06-14.md` |
| Result file | `docs/plans/bayesfilter-batched-filtering-phase-6-default-readiness-result-2026-06-14.md` |

## Handoff

The next human decision is whether to authorize a filtering productionization
program: public API/export shape, default policy, CI coverage, docs, and broader
filtering fixtures.  HMC/NeuTra validation belongs to separate consumer plans.
