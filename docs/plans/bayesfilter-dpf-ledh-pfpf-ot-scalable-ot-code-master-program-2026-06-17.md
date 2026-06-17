# Master Program: Source-Grounded Scalable OT Code Evaluation for LEDH-PFPF-OT

Date: 2026-06-17

## Status

`VISIBLE_GATED_EXECUTION_READY_FOR_PHASE_0_REVIEW`

## Purpose

Design and execute a staged code program for testing scalable optimal-transport
schemes that may replace or augment the dense/all-pairs OT step in
LEDH-PFPF-OT.

This master program is stricter than a literature ranking.  Every candidate
must be audited against:

1. the original paper math and claims;
2. the local survey/note interpretation;
3. the downloaded source code in `.localsource`;
4. the BayesFilter TensorFlow implementation contract;
5. the measured execution value on common fixtures.

The goal is not only to find a fast OT distance.  The BayesFilter filter needs
a usable transport object: a coupling, a barycentric projection, or a directly
transported particle cloud that maps weighted particles to approximately
equal-weight transported particles.

## Source Corpus

| Artifact | Path | Role |
| --- | --- | --- |
| Self-contained survey paper | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex` and `.pdf` | Main written note explaining the problem, equations, method families, and code-availability table |
| Expanded survey result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-expanded-literature-survey-result-2026-06-16.md` | Earlier method-family classification and local baseline diagnosis |
| Literature manifest | `.localsource/scalable_ot_survey/MANIFEST.md` | Downloaded paper/text corpus |
| Code audit manifest | `.localsource/scalable_ot_code_audit/MANIFEST.md` | Downloaded source-code corpus, commits, code anchors, and reuse risk |
| Target Nystrom paper source | `.localsource/1812.05189-src/sections/nystrom.tex`, `.localsource/1812.05189-src/sections/sinkhorn.tex`, `.localsource/1812.05189.txt` | Original paper/source anchor for Nystrom Sinkhorn |
| Current BayesFilter OT baseline | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py` | Dense/streaming TensorFlow transport baseline |
| Current batched LEDH-PFPF-OT code | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`, `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py` | Downstream filter/value integration target |
| Current test/benchmark harnesses | `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`, `tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py`, `docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_correctness.py`, `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py` | Existing correctness and execution-value scaffolding |

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Which scalable OT schemes are worth implementing and testing for LEDH-PFPF-OT, after comparing paper claims, local survey interpretation, downloaded code, and execution value? |
| Mechanism under test | Replace the dense/all-pairs transport step by exact online/GPU, Nystrom, positive-feature, direct low-rank coupling, sparse/localized, sliced/subspace, or minibatch-style alternatives. |
| Expected failure mode | A scheme computes only a scalar distance, cannot expose a particle transport, silently changes filter semantics, depends on a non-TensorFlow backend as a default implementation, or is fast only on a proxy benchmark. |
| Promotion criterion | A candidate passes paper-note-code triangulation, implements a TensorFlow/TFP transport interface, passes small dense-reference checks, has finite diagnostics, and shows execution value on a common fixture without violating semantics. |
| Promotion veto | No usable transport object; source-code checkout invalid and no user-provided archive; paper-code mismatch not declared; dense-reference check fails on small fixtures; marginal residual invalid; nonfinite output; TensorFlow backend violation; speed-only evidence. |
| Continuation veto | Baseline dense/streaming reference is invalid; common fixture generation is not deterministic; execution artifacts are missing; candidate cannot be compared under the declared transport object; three repeated source-fetch failures block a source-required candidate. |
| Repair trigger | A mismatch is localized to normalization, transpose convention, epsilon schedule, landmark selection, feature scaling, dtype, or batch shape and can be tested with a small fixture. |
| Explanatory diagnostics | Runtime, peak memory/proxy memory, transport residuals, cost gap, transported-particle error, dense plan error when available, effective rank/features, gradient finite checks, downstream LGSSM value error. |
| Must not conclude | No production default, no posterior correctness, no categorical-resampling gradient, no HMC readiness, no statistically supported ranking from one-seed or short-run diagnostics. |

## Program Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can any source-grounded scalable OT scheme improve the LEDH-PFPF-OT transport bottleneck while preserving or explicitly replacing the required particle-transport object? |
| Baseline/comparator | Current TensorFlow dense/streaming FilterFlow-style transport in `annealed_transport_tf.py`, plus current batched LEDH-PFPF-OT benchmarks. |
| Primary pass criterion | Each candidate receives a completed paper-note-code audit and a small deterministic execution-value result before it can be ranked or recommended for deeper implementation. |
| Veto diagnostics | Wrong baseline; scalar loss treated as transport; proxy speed promoted to correctness; missing source anchors; missing stop conditions; non-TensorFlow default implementation; stochastic differences interpreted as superiority; invalid or dirty source checkout used as decisive evidence. |
| Explanatory diagnostics | Library maturity, backend mismatch, code availability, paper theorem relevance, local API complexity, implementation effort, runtime/memory, dense-reference discrepancy, downstream filter value. |
| What will not be concluded | Literature/code availability alone does not establish correctness. Dense parity alone does not establish posterior validity. Runtime alone does not establish algorithmic superiority. |
| Required artifact | For every executed phase: subplan, run manifest, JSON/MD result, decision table, source-anchor table, and explicit non-claims. |

## Skeptical Plan Audit

This plan passes the skeptical audit only under the following constraints:

- Wrong baselines are blocked by requiring dense/streaming TensorFlow
  `annealed_transport_tf.py` as the first comparator.
- Proxy metrics are blocked by classifying runtime, memory, and paper benchmark
  speed as explanatory until transport correctness and finite diagnostics pass.
- Missing stop conditions are blocked by per-candidate promotion vetoes and
  continuation vetoes.
- Unfair comparisons are blocked by a common fixture ladder and by separating
  exact-Sinkhorn approximations from intentional new-resampling semantics.
- Hidden assumptions are blocked by the paper-note-code triangulation table.
- Environment mismatches are blocked by the TensorFlow/TFP default rule and by
  labeling PyTorch/JAX/Triton/C++ code as reference/prototype material.
- Commands whose artifacts would not answer the question are blocked: no
  benchmark counts unless the artifact includes the transport object,
  diagnostics, baseline, candidate commit/spec, and interpretation.

Skeptical audit status: `PASSED_FOR_MASTER_PROGRAM_DRAFT`; individual phases
still require their own pre-run evidence contracts before execution.

## Common Transport Interface

Every candidate implementation should be adapted to a common experimental
interface before comparison:

```text
transport_result = candidate_transport(
    particles: [B, N, D],
    log_weights: [B, N],
    *,
    epsilon: float,
    iterations: int,
    candidate_config: Mapping,
)
```

Required outputs:

| Output | Required meaning |
| --- | --- |
| `particles` | Transported particles `[B, N, D]` or documented alternative projected/subspace output |
| `transport_object` | Dense matrix, lazy operator, factors, sparse plan, projection plan, or explicit `not_materialized_reason` |
| `diagnostics` | Marginal residuals, finite checks, transport mass, iteration count, cost estimate, and candidate-specific metrics |
| `source_route` | `source_faithful`, `fixed_hmc_adaptation`, or `extension_or_invention` with paper/source anchors |
| `execution_manifest` | Backend, dtype, device, seed, fixture, command, wall time, artifact paths |

For BayesFilter-owned algorithmic implementation paths, the implementation
backend must be TensorFlow/TFP unless a reviewed exception is written first.
NumPy/POT/PyTorch/JAX/C++ can be used as independent references, comparison
fixtures, or source-code guides.

## Candidate Triangulation Gate

Before any candidate receives code beyond a tiny probe, write a candidate
audit note with this table:

| Check | Required content | Pass condition |
| --- | --- | --- |
| Paper equation anchor | Original paper section/equation/algorithm for the candidate transport object | The paper explicitly provides or implies a usable coupling/operator/transported cloud |
| Survey/note anchor | Section of the local survey explaining the method and its risk | The local note does not overstate the paper and classifies semantic changes |
| Downloaded code anchor | Local `.localsource` path, commit, function/class names, and backend | Relevant implementation is present and readable, or candidate is blocked/pending user archive |
| Paper-code consistency | Compare notation, normalization, coupling orientation, epsilon, weights, and returned object | Mismatches are either resolved or explicitly classified as extensions |
| BayesFilter implementation contract | Candidate TensorFlow interface, dtype, batch shape, transport output, gradient route | Contract is implementable without changing production defaults |
| Execution-value hypothesis | What metric would justify continuing after correctness checks | Hypothesis is not a proxy promoted to correctness |

Candidate audit notes should live under:

```text
docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-{candidate}-audit-YYYY-MM-DD.md
```

## Mandatory Paper-Note-Code-Execution Comparison

Every candidate must be compared across four evidence sources before it can be
prioritized for implementation.  The comparison is not optional, and the code
column is the strongest practical gate because LEDH-PFPF-OT needs a usable
transport object, not only a literature claim or scalar OT loss.

| Evidence source | Required question | Required artifact | Decision effect |
| --- | --- | --- | --- |
| Original paper | What mathematical object is solved for, and what complexity/accuracy claim is actually made? | Paper section, equation, theorem, or algorithm anchor; explicit statement of whether the object is a dense coupling, lazy operator, low-rank factor, sparse plan, projected map, or scalar loss. | Blocks unsupported mathematical claims and prevents treating a different OT problem as an acceleration of dense Sinkhorn. |
| Local survey/note | How did the local note interpret the method for LEDH-PFPF-OT? | Survey section/equation anchor plus classification as exact semantics, approximate kernel, semantic replacement, or exploratory surrogate. | Blocks stale or over-strong conclusions from the note; mismatches must be corrected before coding. |
| Downloaded source code | What does the inspected implementation actually compute and return? | `.localsource` path, commit when available, file and line/function/class anchors, backend, return type, and whether the code exposes plan application or only a loss/dual values. | Hard gate for candidate priority.  Valid GitHub code is not enough; the implementation must expose or imply the transport needed by the filter. |
| Execution value | Does the method produce useful value on BayesFilter fixtures after correctness checks? | Reproducible command, run manifest, dense/streaming baseline comparator, candidate configuration, JSON/MD diagnostics, and decision table. | Required before ranking.  Runtime or memory without transport validity is explanatory only. |

Each candidate audit/result must contain this comparison matrix:

| Comparison item | Original paper | Local note | Downloaded code | Execution-value test | Required resolution |
| --- | --- | --- | --- | --- | --- |
| Problem solved | OT objective, regularization, constraints | Local semantic class | Function/class objective and backend | Fixture objective/comparator | Same problem, or declared semantic replacement |
| Transport object | Coupling/operator/factors/projected map/loss | Required BayesFilter object | Returned object and plan-application route | Inspected returned result fields | Blocks if no particle transport can be produced |
| Marginals/orientation | Source and target marginal convention | Local row/column convention | Code orientation, normalization, target weights | Row/column residuals and transported-particle shape | Must be reconciled before parity claims |
| Cost/kernel/epsilon | Cost, kernel, entropy parameterization | Local parameter map | Code parameter names and scaling | Candidate config and dense baseline config | Blocks if epsilon/cost mismatch is unclassified |
| Approximation knob | Rank/features/sparsity/projections/minibatches | Local expected failure mode | Code knob, initialization, randomness | Fixed deterministic setting and sensitivity hook | Random/proxy settings cannot decide defaults |
| Backend and gradients | Paper differentiability/algorithm assumptions | BayesFilter TF/TFP rule | Code backend and autodiff route | Gradient smoke only when claimed | Non-TF code is reference/comparator unless exception approved |
| Execution value | Paper benchmark claim | Local value hypothesis | Whether code can be run or ported | Correctness-first runtime/memory/downstream result | Ranking only after hard vetoes pass |

Audit outcomes use these labels:

| Label | Meaning |
| --- | --- |
| `source_locked` | Paper, note, and code anchors are valid and internally consistent enough to design a BayesFilter fixture. |
| `source_reference_only` | Code is valid and informative, but backend/API/semantics make it reference material rather than a default BayesFilter implementation path. |
| `source_partial_user_needed` | The literature lane remains plausible, but downloaded code is incomplete or missing; ask the user for a clean archive/source before decision-grade use. |
| `paper_note_code_mismatch` | Paper, note, or code disagree on the solved object, scaling, orientation, or returned transport; resolve before implementation. |
| `execution_value_pending` | Static audit passed, but no BayesFilter fixture has been run.  This is not a ranking. |
| `execution_value_passed` | Candidate passed declared hard vetoes and showed useful runtime/memory/downstream value on a recorded fixture. |
| `execution_value_failed` | Candidate failed a hard veto or did not justify continuation under the evidence contract. |

Static source evidence may nominate baseline-gated test candidates, but it must
not be reported as an empirical ranking or implementation priority.  Execution
value begins only when a candidate returns finite transported particles or an
explicitly declared replacement object on a common fixture, with dense/streaming
baseline diagnostics recorded beside it.

## Candidate Lanes

| Lane | Candidate | Original paper anchors | Downloaded code anchors | First implementation target | Decision posture |
| --- | --- | --- | --- | --- | --- |
| A | Dense/streaming exact TensorFlow reference | Cuturi Sinkhorn; Corenflos differentiable OT resampling; local FilterFlow-style notes | `annealed_transport_tf.py`; `.localsource/scalable_ot_code_audit/filterflow/.../plan.py`; `.../sinkhorn.py` | No new algorithm; freeze fixture and diagnostics | Required baseline, not a scaling winner |
| B | Exact online/GPU Sinkhorn | GeomLoss/KeOps; FlashSinkhorn; fast log-domain GPU Sinkhorn | `geomloss/src/geomloss/ot/_ot_result.py`; `flash-sinkhorn/API.md`; `flash-sinkhorn/src/.../sinkhorn_solvers.py`; `ott-sparse/src/ott/geometry/pointcloud.py` | TensorFlow streaming/operator refactor or benchmark-only reference | Semantics-preserving but still all-pairs compute |
| C | Nystrom kernel Sinkhorn | `1812.05189` Nystrom/Sinkhorn sections | `POT/ot/bregman/_empirical.py`; `POT/ot/lowrank.py`; `LinearSinkhorn/FastSinkhorn.py`; `ott-sparse/src/ott/geometry/low_rank.py` | TensorFlow fixed-rank Nystrom transport application | Baseline-gated approximate-kernel candidate |
| D | Positive-feature Sinkhorn | Scetbon-Cuturi positive-feature paper | `LinearSinkhorn/FastSinkhorn.py`; `LinearSinkhorn/EXP_GAN/torch_lin_sinkhorn.py` | TensorFlow positive-feature kernel matvec and transported cloud | Baseline-gated feature-kernel candidate; source API is research-script style |
| E | Direct low-rank coupling OT | Forrow; Scetbon low-rank Sinkhorn/factored OT; Halmos FRLC/hierarchical | `POT/ot/lowrank.py`; `POT/ot/factored.py`; `ott-sparse/src/ott/solvers/linear/sinkhorn_lr.py` | TensorFlow factorized coupling transport, initially small fixtures | Baseline-gated semantic-replacement candidate, not dense-Sinkhorn approximation |
| F | Sparse/screened/multiscale OT | Schmitzer sparse/multiscale/stabilized; Screenkhorn | `schmitzer-MultiScaleOT/src/Sinkhorn`; `src/ShortCutSolver`; `POT/ot/bregman/_screenkhorn.py` | Locality diagnostic first; sparse TF prototype only if locality holds | Conditional on post-flow sparsity/locality |
| G | Sliced/subspace OT | Sliced/subspace OT papers | `POT/ot/sliced/_sliced_plans.py` | Projection diagnostic and alternative resampling experiment | New semantics, downstream validation required |
| H | Mini-batch / BoMb OT | BoMb-OT and partial mini-batch OT papers | `Mini-batch-OT-sparse/ABC/utils.py`; `ColorTransfer/utils.py`, but checkout partial | Blocked until clean source or user archive; concept probe only | Not decision-grade yet |

## Execution-Value Ladder

Each executable candidate must climb this ladder in order.  A later rung cannot
repair a failed earlier veto by being faster.

| Rung | Fixture | Primary pass criterion | Veto | Explanatory metrics |
| --- | --- | --- | --- | --- |
| 0 | Source/code audit only | Candidate audit table complete | Missing paper or code anchor; unresolved paper-code mismatch | Implementation effort, backend mismatch |
| 1 | Tiny deterministic transport, e.g. `B=1,N<=8,D<=3` | Finite output; valid transport object; marginal residual within declared tolerance | Nonfinite output; wrong shape; no transport object | Cost gap, plan/factor inspection |
| 2 | Dense-reference parity, e.g. `B=2,N<=32,D<=5` | Transported particles close to dense/streaming reference for exact/approximation lanes, or declared semantic delta for replacement lanes | Silent semantic change; invalid marginals | Particle RMSE, plan/operator error, residuals |
| 3 | Gradient/score smoke for relaxed objective | Finite value/score where candidate claims differentiability | Gradient through categorical resampling claim; NaN/Inf; missing stop-gradient declaration | FD gaps on no-resampling and active-transport cases |
| 4 | Scaling microbenchmark | Runs on fixed CPU fixture with increasing `N,D` and writes manifest | Runtime-only artifact with no correctness diagnostics | Wall time, memory proxy, rank/features/sparsity |
| 5 | Batched LEDH-PFPF-OT integration | Candidate works inside experimental batched filter on LGSSM fixture | Value recursion invalid; active transport diagnostics invalid | Value delta, ESS, transport diagnostics |
| 6 | Multi-seed/downstream validation | Repeated fixtures with uncertainty-aware interpretation | One-seed ranking claim; failed hard veto | Descriptive intervals, viability classification |

## Execution-Value Metrics

Metrics must be classified before interpretation:

| Metric | Role |
| --- | --- |
| finite particles/log weights/value | hard veto |
| row/column marginal residual | hard veto for coupling-like candidates; explanatory for sliced/minibatch if semantics differ |
| transported-particle dense-reference error | promotion criterion for approximation-to-dense lanes; explanatory for semantic replacement lanes |
| effective rank/feature count/sparsity | explanatory and repair trigger |
| runtime and memory proxy | explanatory until correctness passes |
| LGSSM value delta | promotion criterion only after transport validity passes |
| finite-difference gradient gap | hard veto only for lanes claiming differentiable relaxed objective |
| posterior/filter accuracy | later validation criterion; not established by early rungs |

## Phase Index

| Phase | Name | Objective | Subplan | Required result artifact |
| ---: | --- | --- | --- | --- |
| 0 | Governance, Source Lock, And Runbook Gate | Review this master program, lock phase contracts, preserve the source audit, create the visible gated runbook, and obtain read-only Claude convergence before execution advances. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p00-governance-source-lock-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p00-governance-source-lock-result-2026-06-17.md` plus existing source lock result |
| 1 | Baseline Fixture Contract | Define deterministic transport fixtures and record dense/streaming baseline diagnostics. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p01-baseline-fixture-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p01-baseline-fixture-result-2026-06-17.md` |
| 2 | Candidate Audit Notes | Write paper-note-code audit notes for Nystrom, positive-feature, low-rank coupling, exact online/GPU, sparse, sliced/subspace, and minibatch lanes. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p02-candidate-audit-notes-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p02-candidate-audit-notes-result-2026-06-17.md` |
| 3 | Common Interface Harness | Implement the experimental candidate interface and JSON result schema without adding a new algorithm yet. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p03-common-interface-harness-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p03-common-interface-harness-result-2026-06-17.md` |
| 4 | Nystrom Prototype | Implement TensorFlow fixed-rank Nystrom transport application and compare to dense reference. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-result-2026-06-17.md` |
| 5 | Positive-Feature Prototype | Implement TensorFlow positive-feature transport application and compare to dense/Nystrom. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p05-positive-feature-prototype-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p05-positive-feature-prototype-result-2026-06-17.md` |
| 6 | Low-Rank Coupling Prototype | Implement factorized coupling transport as a declared semantic replacement. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p06-low-rank-coupling-prototype-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p06-low-rank-coupling-prototype-result-2026-06-17.md` |
| 7 | Exact Online/GPU Reference Study | Decide whether to port operator ideas or keep exact online/GPU sources as reference-only benchmarks. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p07-exact-online-gpu-reference-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p07-exact-online-gpu-reference-result-2026-06-17.md` |
| 8 | Sparse/Localized Diagnostic | Measure post-flow locality/sparsity and only then decide whether sparse prototype work is justified. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p08-sparse-localized-diagnostic-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p08-sparse-localized-diagnostic-result-2026-06-17.md` |
| 9 | Sliced/Subspace/Minibatch Exploratory Lane | Run only after semantic replacement criteria are written; keep Mini-batch blocked until source is clean. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p09-sliced-subspace-minibatch-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p09-sliced-subspace-minibatch-result-2026-06-17.md` |
| 10 | Comparative Decision | Produce the final decision table: viable candidates, hard vetoes, execution value, implementation risk, and next justified target. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p10-comparative-decision-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p10-comparative-decision-result-2026-06-17.md` and reset memo |

The visible runbook for this master program is:

```text
docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-visible-gated-execution-runbook-2026-06-17.md
```

The execution ledger is:

```text
docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-visible-execution-ledger-2026-06-17.md
```

## Required Subplan Contract

Every phase subplan must exist before that phase is executed and must contain:

- phase objective;
- entry conditions inherited from the previous phase;
- required artifacts;
- required checks, tests, and reviews;
- evidence contract;
- skeptical plan audit;
- forbidden claims and actions;
- exact next-phase handoff conditions;
- stop conditions;
- end-of-phase checklist.

The end-of-phase checklist is binding:

1. run the required local checks;
2. write a phase result or close record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.

For material subplans, Claude may be used only as a read-only reviewer.
Claude is not an execution authority and cannot authorize phase advancement or
crossing human, runtime, model-file, funding, product-capability,
default-policy, or scientific-claim boundaries.

## Claude Review And Repair Loop

Claude review is a gate for material governance, boundary, implementation, and
decision phases.  Codex remains the supervisor and executor.  Claude prompts
must be concise and path-based; do not paste whole long files into the prompt.

Review loop:

1. Run local checks first.
2. Ask Claude Opus at max effort for read-only review of the named artifacts.
3. Preserve the review output as a `docs/plans/...claude-review-round-XX...md`
   artifact.
4. Treat `VERDICT: AGREE` as review-convergence evidence, not as
   authorization.  Codex may advance only when the subplan gates, local checks,
   human-required boundaries, and review-convergence evidence all pass.
5. If Claude returns `VERDICT: REVISE`, patch the same subplan or artifact
   visibly, rerun focused local checks, and rerun a focused review.
6. Stop after five Claude review rounds for the same blocker and write a
   blocker result requesting human direction.
7. If Claude does not respond, run a tiny read-only probe.  If the probe
   responds, treat the earlier prompt as too broad or malformed, redesign it,
   and retry with a narrower scope.  If the probe fails, write a blocker result
   and ask for approval or environment help.

## Phase 0 Detailed Requirements

Phase 0 must produce a table with one row per candidate:

| Field | Required content |
| --- | --- |
| Candidate | Method family and local short name |
| Original paper anchor | Paper, section/equation/algorithm, and what is explicitly claimed |
| Local note anchor | Survey section and whether the note calls it exact approximation or semantic replacement |
| Code anchor | Repository path, commit, file/function/class |
| Source status | valid, partial, missing, or user-needed |
| Implementability | TensorFlow direct, TensorFlow port, comparison-only, or blocked |
| First execution-value test | Smallest command/artifact that would answer whether the lane deserves more work |
| Non-claims | What must not be inferred from the first test |

Mini-batch-OT must be recorded as `partial_source_blocked_for_decision` unless
a clean archive or checkout is provided.

## Phase 1 Baseline Fixture Contract

Baseline fixtures must include:

- tiny manually inspectable weighted particles;
- deterministic LGSSM-style particles;
- at least one high-dimensional synthetic cloud with configurable rank/locality;
- fixed log weights and fixed random seeds;
- explicit dtype and device;
- dense mode and streaming mode outputs from `annealed_transport_tf.py`;
- diagnostics including row residual, column residual, transported-particle
  norm, finite checks, and execution time.

The baseline fixture artifact is the comparator for every candidate.  If this
fixture fails or drifts, no candidate benchmark is interpretable.

## Implementation Boundaries

- New algorithmic code should live under experimental DPF implementation paths
  until it passes the comparative decision phase.
- No production default changes are allowed in this master program.
- No public API export is allowed without a separate reviewed plan.
- NumPy/POT/PyTorch/JAX/C++ may be used for independent reference scripts or
  source inspection, but BayesFilter-owned candidate implementations default to
  TensorFlow/TFP.
- Any non-TensorFlow default route must be classified as a reviewed exception.
- Each candidate must classify its route:
  - `source_faithful`: paper/code operation is preserved;
  - `fixed_hmc_adaptation`: route preserved but randomness/ranks/bases frozen
    for differentiability/reproducibility;
  - `extension_or_invention`: not in source paper/code and cannot close a
    source-faithfulness gap.

## Review And Audit Loop

For every material phase:

1. Write a subplan with evidence contract and skeptical audit.
2. Run only commands whose artifacts answer that phase.
3. Write a result note with a decision table.
4. Record a run manifest: git commit, command, environment, CPU/GPU status,
   seeds, wall time, artifact paths, plan path, result path.
5. Classify diagnostics as hard veto, promotion criterion, continuation veto,
   repair trigger, or explanatory.
6. If a candidate fails, state whether it is an implementation failure, tuning
   failure, diagnostic failure, source mismatch, or evidence against the idea.
7. Update a reset memo after any meaningful direction change.
8. Send material plans/results to read-only review when the phase affects
   candidate priority or implementation boundaries.

## Comparative Decision Table

The final comparative result must include:

| Candidate | Source audit | Transport validity | Dense/reference agreement | Execution value | TF implementation risk | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| Dense/streaming reference | required | required | baseline | baseline | low/current | keep as oracle |
| Exact online/GPU | pending phase results | pending transport check | exact semantics expected | pending execution-value result | medium/high | pending comparative decision |
| Nystrom Sinkhorn | pending phase results | pending transport check | expected approximate | pending execution-value result | medium | pending comparative decision |
| Positive-feature Sinkhorn | pending phase results | pending transport check | expected approximate | pending execution-value result | medium | pending comparative decision |
| Low-rank coupling OT | pending phase results | pending transport check | semantic replacement | pending execution-value result | medium/high | pending comparative decision |
| Sparse/localized OT | pending locality diagnostic | pending locality result | conditional | pending locality result | high | pending comparative decision |
| Sliced/subspace OT | exploratory | alternative semantics | not dense parity | pending exploratory result | medium | pending comparative decision |
| Mini-batch/BoMb OT | partial source | blocked | not decision-grade | blocked | unknown | ask user for clean source |

## Static Source-Lock Testing Hypothesis

Static source inspection suggests the following baseline-gated test candidates
after Phase 0 and Phase 1 gates pass.  This is not an empirical ranking or
implementation priority and carries no execution value until the required
fixtures run:

1. Baseline fixture and source-lock phases.
2. A TensorFlow fixed-rank Nystrom Sinkhorn transport-application candidate.
3. A positive-feature TensorFlow comparator.
4. A low-rank coupling candidate as a declared semantic replacement.
5. Locality diagnostic before any sparse/multiscale implementation.

Do not start with Mini-batch-OT until the source checkout is clean.  Do not
start with FlashSinkhorn as a TensorFlow implementation unless the immediate
goal is an exact GPU-kernel engineering project rather than subquadratic
algorithm selection.

## Final Handoff Requirements

The final handoff must state:

- which candidates passed paper-note-code triangulation;
- which candidates were blocked by missing or partial source code;
- which candidates produced a valid transport object;
- which candidates passed dense/reference checks;
- which candidates showed execution value after correctness checks;
- whether any ranking is statistically supported;
- which observed differences are descriptive only;
- the next justified implementation target;
- what is explicitly not being concluded.
