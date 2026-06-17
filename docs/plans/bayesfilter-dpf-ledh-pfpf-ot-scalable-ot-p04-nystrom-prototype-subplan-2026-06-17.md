# Phase 4 Subplan: Nystrom Prototype

Date: 2026-06-17

## Phase Objective

Implement the first TensorFlow fixed-rank Nystrom approximate-kernel transport
prototype for LEDH-PFPF-OT and compare it against the Phase 1 dense/streaming
FilterFlow-style annealed transport fixtures.

The phase objective is narrow: build a deterministic fixed-rank prototype that
can return transported particles plus a `kernel_factors` transport object under
the Phase 3 schema.  This phase does not choose a production default, does not
rank all scalable OT candidates, and does not claim general high-dimensional
scalability.

Phase 4 has two possible non-blocked outcomes:

- `PHASE_4_NYSTROM_PROTOTYPE_PASSED`: hard transport-validity vetoes pass and
  the declared dense-reference viability thresholds below pass.
- `PHASE_4_NYSTROM_PROTOTYPE_COMPLETED_CANDIDATE_NOT_PROMOTED`: hard
  transport-validity vetoes pass, but dense-reference viability thresholds fail
  or indicate the tested rank/landmark settings are not worth deeper Nystrom
  work.  This is a candidate-specific negative result, not a failure of the
  whole scalable-OT program.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result records `PHASE_1_BASELINE_FIXTURE_PASSED`.
- Phase 2 result records
  `PHASE_2_CANDIDATE_AUDITS_PASSED_WITH_USER_APPROVED_MICRO_REVIEW_RESOLUTION`.
- Phase 3 result records `PHASE_3_COMMON_INTERFACE_HARNESS_PASSED`.
- Phase 3 schema helper and smoke artifacts exist.
- Nystrom lane audit records `source_locked`, semantic class
  `approximate_kernel`, and execution value `execution_value_pending`.
- The comparator remains the local TensorFlow dense/streaming
  `annealed_transport_tf.py` fixture, not an external balanced OT library
  result.
- Mini-batch/BoMb remains blocked and is unrelated to this phase.
- No candidate correctness, speedup, ranking, or default change has been
  claimed.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-result-2026-06-17.md`
- TensorFlow experimental implementation artifact, expected location:
  `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
- Candidate diagnostic script:
  `docs/benchmarks/scalable_ot_p04_nystrom_prototype_diagnostics.py`
- JSON result:
  `docs/benchmarks/scalable-ot-p04-nystrom-prototype-diagnostics-2026-06-17.json`
- Markdown result:
  `docs/benchmarks/scalable-ot-p04-nystrom-prototype-diagnostics-2026-06-17.md`
- Optional log if diagnostics are verbose:
  `docs/benchmarks/scalable-ot-p04-nystrom-prototype-diagnostics-2026-06-17.log`
- Targeted tests, either new focused tests under `tests/` or a focused
  diagnostic command recorded in the result.
- Updated execution ledger and stop handoff.
- Phase 5 positive-feature prototype subplan draft:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p05-positive-feature-prototype-subplan-2026-06-17.md`

## Source Anchors Required Before Coding

The implementation must cite these anchors in comments or result notes when
claiming source-faithful operations:

| Anchor | Required use |
| --- | --- |
| `.localsource/1812.05189-src/sections/nystrom.tex` lines 10-27 | Gaussian kernel, `V A^{-1} V^T` factorization, Cholesky triangular-solve matvec, and `O(nr)` matvec route. |
| `.localsource/1812.05189-src/sections/nystrom.tex` lines 121-172 | Adaptive Nystrom diagonal error and rank-doubling route.  Phase 4 may record this as source context but must not implement adaptive/random rank unless explicitly added to this subplan. |
| `.localsource/1812.05189-src/sections/sinkhorn.tex` lines 8-24 and 41-50 | Approximate kernel Sinkhorn scaling, marginal residual target, runtime in terms of matvecs, and log-kernel perturbation stability. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex` lines 437-545 | Local equations for `K`, `V`, `A`, matvec, approximate plan, transported-particle application, marginal residual, and transported-particle error. |
| `.localsource/scalable_ot_code_audit/POT/ot/lowrank.py` lines 530-730 | Reference code for Nystrom kernel factors, low-rank Sinkhorn scaling, scaling-vector updates, and lazy plan return. |
| `.localsource/scalable_ot_code_audit/POT/ot/bregman/_empirical.py` lines 766-865 | Reference empirical Nystrom wrapper and `reg` to `sigma=(reg/2)**0.5` map. |
| `.localsource/scalable_ot_code_audit/LinearSinkhorn/FastSinkhorn.py` lines 197-260 | Research-script reference for `A,V` scaling updates; reference only, not BayesFilter default implementation. |

## Required Checks, Tests, And Reviews

Local checks before implementation:

1. Re-read the Nystrom audit note, Phase 3 schema helper, Phase 1 fixture
   result, and the current `annealed_transport_tf.py` cost/potential/transport
   orientation.
2. Confirm the implementation route is `source_faithful` only for operations
   directly anchored in the Nystrom paper/source or downloaded code:
   Gaussian/Nystrom factors, `V A^{-1} V^T`, triangular-solve matvecs, and
   low-rank Sinkhorn scaling.  Classify the local FilterFlow cost scaling,
   epsilon/reg/sigma/eta adapter, deterministic landmark rule, Cholesky jitter,
   and any frozen schedule as `fixed_hmc_adaptation` when they preserve the
   source route for reproducibility, or `extension_or_invention` when they
   change the route.
3. Confirm no non-TensorFlow implementation path is introduced as BayesFilter
   default.

Implementation checks:

1. Python syntax/import checks for new Python files.
2. Tiny fixture check with `B=1`, `N<=8`, `D<=3`, and rank values that include
   full or near-full rank where feasible.
3. Phase 1 fixture diagnostic check on `tiny_manual`, `small_parity`,
   `high_dim_low_rank`, and `high_dim_locality`.
4. Candidate result must validate with
   `docs.benchmarks.scalable_ot_candidate_result_schema.validate_candidate_result`.
5. Hard-veto diagnostics must include finite transported particles, finite
   factors/scalings, valid shapes, row residual, column residual, and no
   missing transport object.
6. Promotion/viability diagnostics for this phase must include
   dense-reference transported-particle error for approximate-kernel lanes.
7. Explanatory diagnostics must include rank, landmark indices or deterministic
   landmark rule, epsilon/reg/sigma/eta map, iteration count, factor shapes, and
   runtime/memory proxy if measured.

Review:

- Because Phase 4 is implementation-bearing, run local checks first, then send
  the subplan and material diffs/results to Claude as read-only review using a
  bounded path-based prompt.
- Claude is not an execution authority.  Phase advancement requires Codex to
  confirm local checks, evidence contract, human boundaries, and review
  convergence.
- If Claude stalls, run the tiny read-only probe.  If the probe responds,
  redesign the prompt into smaller source-anchor, backend-boundary, or
  diagnostic-role micro reviews.
- Stop after five review rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a TensorFlow fixed-rank Nystrom approximate-kernel transport return finite transported particles and valid factor diagnostics on Phase 1 fixtures, with dense-reference error recorded against the local FilterFlow-style baseline? |
| Baseline/comparator | Phase 1 dense/streaming TensorFlow `annealed_transport_tf.py` fixture outputs, especially `docs/benchmarks/scalable-ot-p01-baseline-fixture-diagnostics-2026-06-17.json`. |
| Primary pass criterion | The candidate returns a Phase 3-valid `kernel_factors` result with finite transported particles, finite factors/scalings, row/column residuals below the Phase 4 validity tolerances, and dense-reference transported-particle error below the Phase 4 viability thresholds for the declared fixture/rank scope. |
| Promotion veto | Nonfinite output; missing transported particles; no usable `kernel_factors` object; invalid row/column residuals; epsilon/reg/sigma/eta mismatch not declared; shape/orientation mismatch; dense-reference error missing; non-TensorFlow backend promoted as default; source route claimed without paper/source anchors. |
| Continuation veto | Phase 1 baseline artifact missing or inconsistent; schema validation fails and cannot be repaired narrowly; implementation requires package installation or network fetch; candidate cannot be compared under the declared transport object; source anchors contradict the planned operation. |
| Repair trigger | Failure localized to transpose/orientation, normalization, epsilon map, landmark selection, Cholesky jitter, dtype, or batch shape.  Run the smallest focused fixture after repair. |
| Explanatory diagnostics | Rank, landmark rule, diagonal kernel approximation error when available, factor condition/jitter, marginal residuals, dense-reference particle error, runtime, memory proxy, and iteration count. |
| Not concluded | No general scalability, no high-dimensional success, no speedup claim, no ranking against positive-feature/low-rank/sparse/sliced methods, no posterior correctness, no HMC readiness, no production default change. |
| Artifact preserving result | Implementation file, diagnostic script, JSON/Markdown diagnostics, logs if any, Phase 4 result, ledger, stop handoff, and Phase 5 subplan draft. |

## Phase 4 Validity And Viability Thresholds

These thresholds are predeclared for Phase 4 only.  They are viability gates for
continuing Nystrom prototype work, not claims of general correctness,
scalability, or ranking.

| Diagnostic | Threshold | Role |
| --- | --- | --- |
| finite transported particles, factors, scalings, residuals, and dense-reference errors | all must be finite | hard veto |
| output shape | transported particles must match the dense baseline particle shape for the same fixture | hard veto |
| row marginal residual | maximum absolute row residual `<= 5e-2` for every fixture/rank record | hard veto |
| column marginal residual | maximum absolute column residual `<= 5e-2` for every fixture/rank record | hard veto |
| dense-reference max absolute transported-particle error | at least one tested rank for each of `tiny_manual`, `small_parity`, and `high_dim_low_rank` must have max error `<= 5e-2` | promotion criterion for Nystrom continuation |
| dense-reference RMS transported-particle error | at least one tested rank for each of `tiny_manual`, `small_parity`, and `high_dim_low_rank` must have RMS error `<= 2e-2` | promotion criterion for Nystrom continuation |
| `high_dim_locality` dense-reference error | record max/RMS error but do not require promotion threshold in Phase 4 | explanatory and repair trigger |
| runtime and memory proxy | record when available | explanatory only |

If hard transport-validity vetoes pass but one or more dense-reference
viability thresholds fail, the correct result status is
`PHASE_4_NYSTROM_PROTOTYPE_COMPLETED_CANDIDATE_NOT_PROMOTED`, with a repair or
Phase 5 handoff decision.  It must not be recorded as
`PHASE_4_NYSTROM_PROTOTYPE_PASSED`.

## Source-Route Classification For Phase 4

| Operation | Required classification |
| --- | --- |
| Nystrom Gaussian factors `V`, `A`, and `V A^{-1} V^T` | `source_faithful` when implemented as in the paper/source anchors. |
| Cholesky/triangular-solve or equivalent stable solve for factor matvec/application | `source_faithful` when it preserves the anchored `A^{-1}` matvec route; jitter must be separately recorded. |
| Low-rank Sinkhorn scaling through factors | `source_faithful` when anchored to paper/source scaling and POT/LinearSinkhorn reference behavior. |
| Local FilterFlow scaling, annealing schedule, and cost normalization adapter | `fixed_hmc_adaptation` if it preserves the Nystrom factor/scaling route while matching the BayesFilter baseline; otherwise `extension_or_invention`. |
| Deterministic landmark rule used instead of random/adaptive sampling | `fixed_hmc_adaptation` for reproducibility; it is not a paper-faithful adaptive-rank claim. |
| Cholesky jitter or clipping/stabilization not in the source paper | `fixed_hmc_adaptation` if only numerical stabilization; `extension_or_invention` if it changes the solved object. |

The phase result must not call the entire prototype `source_faithful` unless it
also states which adapter pieces are not paper-source-faithful.

## Diagnostic Role Ledger

| Diagnostic | Role |
| --- | --- |
| finite transported particles | hard veto |
| finite factors/scalings | hard veto |
| output shape and schema validation | hard veto |
| row/column marginal residual | hard veto |
| epsilon/reg/sigma/eta map recorded | hard veto for parity claims |
| dense-reference transported-particle error | promotion criterion for approximate-kernel viability in this phase under the declared Phase 4 thresholds |
| rank and landmark rule | explanatory and repair trigger |
| diagonal Nystrom error if computed | explanatory and repair trigger |
| runtime and memory proxy | explanatory only until correctness gates pass |
| downstream LEDH/LGSSM value | not in Phase 4 unless the subplan is explicitly revised before running it |

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Does the fixed-rank Nystrom approximation preserve enough of the local dense transport on deterministic fixtures to justify deeper scalable-OT testing? |
| Candidate/mechanism | Approximate the Gaussian/FilterFlow Gibbs kernel by factors and run Sinkhorn-like scaling/application through the factors. |
| Expected failure mode | Kernel effective rank is too high, epsilon mapping differs from the baseline, factors become ill-conditioned, or the transport object has valid shapes but wrong orientation. |
| Promotion criterion | Phase 3-valid result plus finite residuals and dense-reference particle error below the declared Phase 4 viability thresholds. |
| Promotion veto | Any hard veto in the diagnostic role ledger. |
| Continuation veto | Any continuation veto in the evidence contract. |
| Repair trigger | Localized normalization, transpose, epsilon map, jitter, landmark, dtype, or batch-shape failure. |
| Explanatory diagnostics | Rank, landmarks, diagonal error, condition/jitter, runtime, memory proxy, and iteration count. |
| Must not conclude | A Phase 4 pass does not prove large-state scaling or make Nystrom the best candidate. |

## Skeptical Plan Audit

- Wrong baseline: Phase 4 compares to the Phase 1 local FilterFlow-style
  dense/streaming baseline, not a generic external Sinkhorn solve.
- Proxy metric risk: runtime and memory are explanatory until hard transport
  validity checks pass.
- Missing stop conditions: stop for missing baseline, schema failure,
  source-anchor contradiction, package/network need, or unrepairable transport
  object mismatch.
- Unfair comparisons: Nystrom is an approximate-kernel lane; dense-reference
  error is a Phase 4 viability criterion, not a ranking against other methods.
- Hidden assumptions: the plan must record cost scaling, epsilon/reg/sigma/eta
  map, row/column orientation, target weights, rank, and landmark rule.
- Source-route overclaim risk: paper-anchored factor/matvec/scaling operations
  must be separated from BayesFilter-specific adapters such as FilterFlow
  scaling, deterministic landmarks, jitter, and schedule freezing.
- Stale context: use the Phase 2 Nystrom audit and Phase 3 schema fields before
  coding.
- Environment mismatch: no package installation, no network fetch, no GPU
  evidence, no non-TensorFlow default implementation.
- Artifact adequacy: JSON/Markdown diagnostics must include transported
  particles status, transport object, source route, diagnostics roles,
  baseline comparator, and non-claims; runtime-only artifacts are inadequate.

Skeptical audit status: `PASSED_FOR_PHASE_4_NYSTROM_PROTOTYPE_PLAN`.

## Forbidden Claims And Actions

- Do not claim Nystrom correctness, speedup, ranking, posterior validity,
  production readiness, public API readiness, or default readiness from Phase 4.
- Do not treat POT, LinearSinkhorn, NumPy, PyTorch, or JAX code as the
  BayesFilter-owned implementation backend.
- Do not install packages, fetch network sources, or use GPU evidence.
- Do not silently switch to a different OT problem or semantic replacement.
- Do not implement adaptive/random landmark selection as a decision-grade
  feature unless this subplan is visibly revised and reviewed first.
- Do not unblock Mini-batch/BoMb.
- Do not modify unrelated dirty user work.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only after:

- Phase 4 result records `PHASE_4_NYSTROM_PROTOTYPE_PASSED`,
  `PHASE_4_NYSTROM_PROTOTYPE_COMPLETED_CANDIDATE_NOT_PROMOTED`, or a precise
  blocker/failure result;
- implementation and diagnostic artifacts exist, or the result explains why
  implementation was stopped;
- syntax/import and candidate diagnostic checks pass, unless the phase result
  is a blocker/failure;
- the candidate JSON validates against the Phase 3 schema, unless schema repair
  is the recorded blocker;
- source-route classification is recorded with paper/source anchors;
- dense-reference transported-particle error and marginal residual diagnostics
  are recorded for the declared fixture/rank scope, and the result states
  whether the Phase 4 validity and viability thresholds passed or failed;
- Phase 5 positive-feature subplan exists and has been reviewed for
  consistency, correctness, feasibility, artifact coverage, and boundary
  safety;
- no human-required stop condition is active.

## Stop Conditions

Stop and write/update the stop handoff if:

- the Phase 1 baseline artifact is missing, inconsistent, or no longer matches
  the implementation;
- the planned TensorFlow route cannot represent a Nystrom transport object;
- source anchors contradict the planned factor/scaling/application operation;
- the implementation would require package installation, network fetch, GPU
  evidence, credentials, destructive action, or non-TensorFlow default code;
- local checks reveal a hard veto that is not localized to a repair trigger;
- Claude and Codex do not converge after five focused review rounds for the
  same material blocker;
- user direction is needed to decide whether to revise the mathematical target,
  tolerances, source route, or implementation backend.

## End-Of-Phase Checklist

1. Run the required local checks.
2. Write the Phase 4 result/close record.
3. Draft or refresh the Phase 5 positive-feature prototype subplan.
4. Review the Phase 5 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
