# Master Program: Fixed-SGQF Leaderboard Promotion and Analytical-Gradient Certification

metadata_date: 2026-06-23
program_id: fixed-sgqf-leaderboard-promotion
status: PROGRAM_COMPLETE_FIXED_SGQF_PROMOTION

## Date

2026-06-23

## Status

`PROGRAM_COMPLETE_FIXED_SGQF_PROMOTION`

## Purpose

This program governs the promotion of the repaired TensorFlow fixed-SGQF lane
into the BayesFilter leaderboard-style deterministic benchmark infrastructure at
a standard comparable to the currently governed SVD, LEDH, and Zhao-Cui lanes.

This is **not** a request for ad hoc extra tests.
It is a governed promotion program that must:

1. preserve the repo's existing benchmark scope, registry, and artifact
   contracts;
2. promote fixed SGQF only on rows where it is honestly same-target and
   evidence-supported;
3. require **analytical gradients / analytical scores** wherever gradient-bearing
   leaderboard participation is claimed;
4. treat autodiff as **diagnostic-only** and never as the promoted SGQF gradient
   implementation or primary promotion oracle;
5. keep blocked and diagnostic-only families explicit rather than silently
   omitted.

This master program supersedes by **aggregation and governance** the earlier
fixed-SGQF testing, model-suite comparison, broader nonlinear placement, and
KSC-surrogate analytical-score planning artifacts.  It does **not** delete or
erase those artifacts; it organizes them into one leaderboard-promotion route.

## Governing Artifacts

### Fixed-SGQF evidence and planning lineage
- `docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-p0-inventory-and-evidence-contract-result-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-final-status-summary-2026-06-15.md`
- `docs/plans/bayesfilter-fixed-sgqf-repaired-lane-reset-memo-2026-06-15.md`
- `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-master-program-2026-06-15.md`
- `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-closeout-result-2026-06-16.md`
- `docs/plans/bayesfilter-fixed-sgqf-broader-nonlinear-comparison-master-program-2026-06-16.md`
- `docs/plans/bayesfilter-fixed-sgqf-broader-nonlinear-comparison-closeout-result-2026-06-16.md`
- `docs/plans/bayesfilter-fixed-sgqf-structural-adapter-result-2026-06-16.md`
- `docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-analytic-score-plan-2026-06-18.md`

### Benchmark scope, registry, and machine-checked governance backbone
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-reference-oracles-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-preflight-matrix-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-results-2026-06-13.json`

### Comparator evidence-bar examples to match in honesty and rigor
- `docs/plans/bayesfilter-v1-svd-cut-branch-diagnostic-gate-2026-05-11.md`
- `docs/plans/bayesfilter-structural-svd-final-execution-result-2026-05-06.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-master-program-2026-06-10.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p51-gap-closure-master-program-2026-06-09.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4-same-route-rank-degree-ladder-result-2026-06-16.md`

### Core code and benchmark surfaces expected to participate
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`
- `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
- `bayesfilter/testing/fixed_sgqf_diagnostics_tf.py`
- `bayesfilter/highdim/sv_mixture_cut4.py`
- `docs/benchmarks/benchmark_bayesfilter_v1_nonlinear_filters.py`
- `docs/benchmarks/benchmark_highdim_nonlinear_filtering_smoke.py`
- `tests/test_fixed_sgqf_*.py`
- `tests/test_nonlinear_benchmark_models_tf.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_target_registry.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_preflight_matrix.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_runner_matrices.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/highdim/test_p47_generalized_sv_equality.py`

## Governing Constraints

1. **Reuse the existing benchmark governance backbone.**
   Fixed SGQF must enter the leaderboard through the existing registry,
   deterministic-coverage matrix, preflight matrix, and numeric-result ledgers
   rather than through a disconnected ad hoc scoreboard.

2. **Same-target comparisons only.**
   No fixed-SGQF row may be ranked against SVD, CUT4, LEDH, Zhao-Cui, or any
   other route unless value scalar meaning, observation law, state law,
   parameterization, and row semantics match.

3. **Analytical gradient means analytical gradient.**
   Any claimed fixed-SGQF score / gradient leaderboard row must be backed by an
   explicit analytical derivative implementation in BayesFilter-owned code.  A
   gradient obtained by `tf.GradientTape`, wrapper autodiff, or equivalent
   automatic differentiation is **not** a promoted SGQF gradient route.

4. **Autodiff is diagnostic-only.**
   Autodiff may be used only as a validation oracle or explanatory cross-check
   for an already implemented analytical gradient.  It may not serve as:
   - the SGQF gradient implementation,
   - the main leaderboard gradient route,
   - the primary promotion criterion,
   - or a substitute for missing analytical wrapper derivatives.

5. **Finite differences are the primary local score-promotion oracle.**
   Analytical SGQF score promotion requires a stable same-scalar,
   accepted-branch finite-difference window on the declared fixture.  Autodiff,
   if run, is secondary diagnostic evidence only.

6. **Accepted-branch / same-scalar discipline is mandatory for score rows.**
   If value and score do not preserve the same branch signature or do not report
   the same scalar, the row is blocked from leaderboard score admission and must
   be classified separately.

7. **The first declared leaderboard SGQF variant remains `fixed_sgqf_level_2`.**
   Higher sparse levels remain separate evidence ladders unless a later reviewed
   subplan explicitly promotes them.

8. **Controlled labels remain binding.**
   The labels `exact`, `dense-reference`, `baseline-only`, `analytical-score`,
   `diagnostic-only`, and `blocked` are controlled labels and must be used only
   when the row's evidence and semantics justify them.

9. **Blocked families must stay explicit.**
   The program must preserve honest `blocked_not_same_target`,
   `blocked_missing_analytical_wrapper_score`, `blocked_branch_inconsistent`, or
   related statuses rather than silently dropping inconvenient SGQF cells.

10. **Production-code edits are allowed only in support of the evidence
    contract.**
    The default objective is governed tests, benchmark integration, and durable
    artifacts.  Production code should change only when a reviewed phase finds a
    genuinely missing same-target SGQF route, missing analytical derivative
    route, or missing required diagnostics.

11. **CPU-only diagnostics must declare hidden GPUs.**
    Any CPU-only fixed-SGQF test or benchmark command must set
    `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import unless a trusted GPU plan
    explicitly opens a GPU execution lane.

12. **Leaderboard admission does not imply HMC readiness or production-default
    status.**
    Fixed SGQF may be admitted into value or analytical-score benchmark cells
    without any implied claim about HMC readiness, source-faithfulness outside
    its route, or default production promotion.

## Current Evidence Base

The repaired fixed-SGQF lane is not starting from zero.

### Strong local support already exists for
- affine exact-reference rows;
- a selected scalar nonlinear dense-reference row;
- repaired higher-level cloud-construction behavior on tested fixtures;
- accepted-branch analytical score versus finite-difference parity on selected
  fixed-branch rows;
- selected-fixture baseline positioning against existing deterministic methods;
- branch/failure contract tests and diagnostic snapshot helpers.

### Known remaining gaps from the earlier gap-closure program
- multistep nonlinear dense-reference accuracy;
- broader accepted-path coverage beyond the smallest existing cases;
- cloud exactness ladders across more `(dim, sparse_level)` cells;
- later-time / later-stage failure coverage;
- broader multi-parameter, multistep analytical-score evidence;
- multidimensional affine exact-vs-Kalman parity;
- governed same-target baseline ladders;
- sparse-level ladders against the same dense reference.

### Current broader admission status
Under the current additive-state fixed-SGQF lane, broader repo-wide admission is
still partial.  The affine anchor and selected narrow benchmark rows are already
admitted, while several literature-backed families remain blocked or require a
new same-target SGQF wrapper / route contract.

### Most important currently open wrapper gap
The KSC Gaussian-mixture surrogate stochastic-volatility row still needs a true
**analytical outer SGQF score** plus same-target comparison support, so that the
SGQF route is not value-only on that literature-backed family.

## Promotion Target

The target of this program is:

> Promote fixed SGQF into the BayesFilter leaderboard infrastructure as a
> governed deterministic algorithm lane on every row where it is same-target,
> reference-policy compliant, and evidence-supported, while keeping all blocked,
> diagnostic-only, and value-only cells explicit.

This means:
- value-row admission may precede analytical-score admission;
- family-by-family admission may proceed even while some broader families remain
  blocked;
- leaderboard participation is row-specific and evidence-specific, not a blanket
  repo-wide compatibility claim.

## Admission Classes

Every fixed-SGQF × target-family cell must receive one explicit admission class.

- `admit_exact`
  - same-target exact row with authoritative exact reference
- `admit_dense_reference_only`
  - same-target row with declared dense numerical comparator only
- `admit_value_baseline_only`
  - same-target benchmark value row without analytical-score promotion
- `admit_analytical_score`
  - same-target row with explicit analytical score route plus branch-stable
    finite-difference validation
- `diagnostic_only`
  - informative SGQF execution outside rankable benchmark semantics
- `blocked_not_same_target`
  - current SGQF route changes target semantics or scalar meaning
- `blocked_missing_analytical_wrapper_score`
  - value route exists but promoted analytical wrapper score route does not
- `blocked_branch_inconsistent`
  - value and score cannot be compared on the same accepted branch / scalar
- `blocked_unstable_fd_window`
  - analytical score exists but stable finite-difference promotion evidence does
    not
- `historical_only`
  - preserved for lineage but not current leaderboard evidence

No fixed-SGQF row may be left without one of these classes or a reviewed,
newly introduced equivalent.

## Skeptical Plan Audit

Status: `PASS_TO_SUBPLAN_CREATION_WITH_ANALYTICAL_GRADIENT_GATES`

### Wrong-baseline risk
Exact Kalman is exact only on affine Gaussian rows.  Dense nonlinear references
remain local numerical comparators on tractable low-dimensional fixtures.
Leaderboard rows must not silently reinterpret dense-reference evidence as exact
or paper-scale truth.

### Proxy-promotion risk
Finite values, stable clouds, finite gradients, smoke runs, or improved timing
are useful diagnostics.  They do not by themselves justify leaderboard
promotion, analytical-score admission, HMC readiness, or production-default
claims.

### Gradient overclaim risk
The largest current promotion risk is quietly treating autodiff as if it were an
analytical SGQF gradient route.  This program blocks that move.  A row is not an
analytical-score row until the derivative is implemented explicitly in
BayesFilter-owned code and validated by branch-stable finite differences.

### Branch-leakage risk
Finite-difference score evidence is promotable only when the declared scalar and
branch signature remain the same.  Branch-leaving FD rows are diagnostic or
blocked; they are not promotion rows.

### Family-admission inflation risk
The broader literature-backed family roster is larger than the currently
admitted SGQF lane.  The program must not upgrade partial compatibility into
blanket admission merely to fill leaderboard cells.

### Artifact-answer mismatch risk
A phase that runs tests but does not update the required matrix/registry/result
artifacts has not answered the leaderboard-promotion question durably.

### Environment mismatch risk
CPU-only diagnostics remain valid only when GPU devices are intentionally
hidden.  Any future trusted GPU benchmark lane must be explicitly planned and
recorded.

### Pre-mortem
How the program could appear to pass while misleading us:
1. SGQF is added to benchmark markdown outputs but not to the machine-checked
   registry/matrix backbone;
2. a wrapper autodiff score is mistaken for a promoted analytical score route;
3. a dense-reference row is described like an exact or paper-scale result;
4. blocked families disappear from artifacts rather than being classified
   explicitly;
5. one-step or low-dimensional success is over-interpreted as general
   literature-family readiness.

Cheapest discriminators:
- machine-check every SGQF matrix cell,
- require explicit analytical derivative entrypoints,
- require score rows to cite the finite-difference validation fixture,
- require blocked-family ledgers,
- require closeout notes to state nonclaims.

## Evidence Contract

### Question
Can the repaired fixed-SGQF lane be promoted into the BayesFilter
leaderboard-style deterministic benchmark infrastructure, with **analytical
score support only where an explicit analytical gradient route exists**, while
preserving honest same-target admission boundaries and blocked-family ledgers?

### Baselines and comparators
- exact Kalman on affine Gaussian rows;
- declared dense numerical references on tractable low-dimensional nonlinear
  rows;
- existing repo deterministic same-target routes where eligible:
  - cubature,
  - UKF,
  - CUT4,
  - SVD sigma-point routes;
- broader literature-backed route families only where same-target semantics are
  actually aligned;
- branch/failure contract rows that may intentionally fail and still pass their
  contract phase.

### Primary promotion criterion
The program succeeds only if:
1. fixed SGQF receives an explicit admission class for every intended benchmark
   cell;
2. every promoted SGQF value row is same-target and reference-policy compliant;
3. every promoted SGQF gradient row is backed by an explicit analytical score
   implementation and stable accepted-branch finite-difference evidence;
4. autodiff appears only as diagnostic/explanatory evidence, never as the SGQF
   gradient route;
5. machine-checked registry, coverage, preflight, and numeric artifacts all
   contain the admitted SGQF cells with no silent holes;
6. blocked families and score-blocked rows remain explicit.

### Veto diagnostics
- any SGQF leaderboard row changes target semantics relative to its comparators;
- any SGQF score row relies on autodiff as the implementation or main promotion
  oracle;
- value and score cannot preserve same-scalar / accepted-branch comparability;
- finite-difference promotion evidence is missing or unstable on a claimed
  analytical-score row;
- matrix / registry artifacts omit a needed SGQF cell or blocker reason;
- closeout artifacts imply universal family compatibility or universal gradient
  readiness.

### Explanatory-only diagnostics
- point count;
- runtime;
- memory;
- branch metadata;
- sparse-level metadata;
- smoke-harness skip behavior;
- autodiff agreement checks run only as secondary diagnostics.

### What will not be concluded even if the program passes
- no universal SGQF superiority claim;
- no claim that all literature-backed nonlinear families are now SGQF-admitted;
- no claim that autodiff and analytical gradients are interchangeable;
- no HMC readiness claim;
- no production-default promotion claim;
- no claim that higher sparse levels are leaderboard-admitted merely because
  `fixed_sgqf_level_2` is admitted.

### Artifact that preserves the result
The durable answer must live in:
- this master program,
- phase subplans and result notes,
- updated benchmark registry/coverage/preflight/numeric artifacts,
- and a final leaderboard-promotion closeout with explicit admitted and blocked
  SGQF families.

## Phase Map

### Program-wide ledgers shared across phases
- Visible execution ledger:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-execution-ledger-2026-06-23.md`
- Bounded review ledger:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-claude-review-ledger-2026-06-23.md`
- Visible stop handoff:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md`

| Phase | Subplan | Result / close record | Review ledger | Stop handoff | Purpose | Required outcome token |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p0-ledger-and-scope-freeze-subplan-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p0-ledger-and-scope-freeze-result-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-claude-review-ledger-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md` | consolidate prior fixed-SGQF evidence, freeze supersession map, and freeze intended SGQF leaderboard scope | `PASS_P0_FIXED_SGQF_LEADERBOARD_SCOPE_FROZEN` |
| P1 | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p1-admission-ledger-subplan-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p1-admission-ledger-result-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-claude-review-ledger-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md` | assign every SGQF × target-family cell an explicit admission class and blocker reason if needed | `PASS_P1_FIXED_SGQF_ADMISSION_LEDGER_WRITTEN` |
| P2 | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-subplan-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-result-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-claude-review-ledger-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md` | close or explicitly bound the earlier G1-G8 kernel/testing gaps needed for leaderboard-grade support | `PASS_P2_FIXED_SGQF_KERNEL_GAPS_CLASSIFIED` |
| P3 | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-subplan-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-result-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-claude-review-ledger-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md` | certify that SGQF score-bearing rows use analytical derivatives only and preserve same-branch finite-difference discipline | `PASS_P3_FIXED_SGQF_ANALYTICAL_SCORE_KERNEL_CERTIFIED` |
| P4 | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-subplan-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-result-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-claude-review-ledger-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md` | implement and certify the KSC-surrogate analytical outer SGQF score and same-target comparator support | `PASS_P4_FIXED_SGQF_KSC_ANALYTICAL_WRAPPER_SCORE_CERTIFIED` |
| P5 | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p5-family-by-family-admission-subplan-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p5-family-by-family-admission-result-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-claude-review-ledger-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md` | promote fixed SGQF through literature-backed families one admitted family at a time while preserving blockers elsewhere | `PASS_P5_FIXED_SGQF_FAMILY_ADMISSION_LEDGER_UPDATED` |
| P6 | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p6-deterministic-matrix-integration-subplan-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p6-deterministic-matrix-integration-result-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-claude-review-ledger-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md` | integrate admitted SGQF cells into the machine-checked deterministic benchmark coverage matrix and registry tests | `PASS_P6_FIXED_SGQF_MATRIX_INTEGRATION_COMPLETE` |
| P7 | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p7-preflight-and-smoke-subplan-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p7-preflight-and-smoke-result-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-claude-review-ledger-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md` | add SGQF cells to preflight and smoke artifacts without over-interpreting them as performance evidence | `PASS_P7_FIXED_SGQF_PREFLIGHT_COMPLETE` |
| P8 | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p8-numeric-ledger-and-runner-subplan-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p8-numeric-ledger-and-runner-result-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-claude-review-ledger-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md` | extend numeric runner matrices and refreshed benchmark outputs to admitted SGQF cells only | `PASS_P8_FIXED_SGQF_NUMERIC_LEDGER_UPDATED` |
| P9 | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p9-closeout-subplan-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p9-closeout-result-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-claude-review-ledger-2026-06-23.md` | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md` | summarize promoted SGQF leaderboard participation, analytical-score admissions, blocked rows, and nonclaims | `PASS_P9_FIXED_SGQF_LEADERBOARD_PROMOTION_CLOSEOUT` |

## Phase-Specific Outcome Requirements

### P0. Ledger and scope freeze
Must produce:
- a consolidated table of prior fixed-SGQF artifacts and whether each gap is
  `closed`, `partially_closed`, `blocked`, `superseded_by_scope`, or
  `reopened_as_wrapper_gap`;
- a frozen statement of the first intended SGQF leaderboard variant;
- a list of benchmark artifacts that must be touched later.

### P1. Admission ledger
Must produce, for every intended SGQF family cell:
- admission class;
- scalar meaning;
- reference policy;
- comparator eligibility;
- blocker reason when not admitted.

### P2. Kernel gap closure
Must revisit the earlier G1-G8 ladder and mark each item as:
- closed by existing test/result,
- requiring a new test,
- requiring a new analytical derivative route,
- or irreducibly outside current leaderboard scope.

### P3. Analytical-score kernel certification
Must certify that:
- score-bearing SGQF kernel rows use explicit analytical derivatives;
- finite differences are branch-stable on the promotion fixture;
- autodiff, if present, appears only as explanatory secondary evidence;
- no remaining promoted score row depends on automatic differentiation.

### P4. KSC surrogate analytical wrapper score
Must certify that:
- the outer SGQF wrapper score is analytical rather than autodiff;
- same-target UKF comparator routes exist where required by project policy;
- wrapper failure / branch policy is explicit;
- finite-difference validation is recorded on the declared tiny KSC-surrogate
  fixtures;
- autodiff comparisons, if run, are labeled diagnostic-only.

### P5. Family-by-family admission
Must produce a durable admitted/blocked ledger across the literature-backed
family set and preserve explicit blocker reasons for all unadmitted families.

### P6. Deterministic matrix integration
Must update machine-readable benchmark artifacts so that no admitted SGQF cell
exists only in prose.  Every admitted or blocked SGQF cell must appear in the
registry and deterministic coverage matrix with a reason code.

### P7. Preflight and smoke
Must add SGQF cells to preflight and smoke artifacts while keeping the label
`not_performance_evidence` or its reviewed equivalent until real numeric runs
are executed.

### P8. Numeric ledger and runner integration
Must update benchmark result artifacts only for admitted SGQF cells whose
reference policy, value meaning, and score meaning have already been frozen.
Blocked cells must remain blocked rather than being filled with convenience
numbers.

### P9. Closeout
Must end with a decision table covering:
- promoted SGQF leaderboard cells;
- promoted analytical-score cells;
- blocked cells and reasons;
- main remaining uncertainty;
- next justified action;
- what is not concluded.

## Required Artifact Contract

Each phase must write, or explicitly block:
1. a subplan;
2. a phase result note;
3. a run manifest for serious commands or benchmark executions, including:
   - git commit,
   - command actually run,
   - environment / conda env,
   - CPU/GPU status,
   - seed(s),
   - wall time,
   - output artifact paths,
   - plan file,
   - result file;
4. a decision table stating decision, primary criterion status, veto diagnostic
   status, main uncertainty, next justified action, and what is not concluded;
5. when applicable, an updated machine-readable matrix / json artifact;
6. a post-run red-team note stating strongest alternative explanation, what
   result would overturn the conclusion, and weakest part of the evidence.

## Expected Test and Benchmark Surfaces by Program Layer

### Core SGQF kernel / contract layer
- `tests/test_fixed_sgqf_tf.py`
- `tests/test_fixed_sgqf_values_tf.py`
- `tests/test_fixed_sgqf_scores_tf.py`
- `tests/test_fixed_sgqf_branch_contract_tf.py`
- `tests/test_fixed_sgqf_verification_tf.py`
- `tests/test_fixed_sgqf_audit_tf.py`
- `tests/test_fixed_sgqf_testing_integration_tf.py`
- `tests/test_fixed_sgqf_integration_tf.py`

### Existing nonlinear model-suite benchmark layer
- `tests/test_nonlinear_benchmark_models_tf.py`
- `docs/benchmarks/benchmark_bayesfilter_v1_nonlinear_filters.py`

### High-dimensional / literature-backed wrapper layer
- `bayesfilter/highdim/sv_mixture_cut4.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/highdim/test_p47_generalized_sv_equality.py`

### Machine-checked leaderboard governance layer
- `tests/highdim/test_filtering_value_gradient_benchmark_target_registry.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_preflight_matrix.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_runner_matrices.py`

## Stop Rules

Stop if:
1. an intended SGQF leaderboard cell cannot be admitted without changing target
   semantics or scalar meaning;
2. a claimed SGQF score row depends on autodiff rather than explicit analytical
   derivatives;
3. finite-difference validation cannot be stabilized on a claimed
   analytical-score promotion row;
4. a family would need a richer SGQF route than the current additive-state lane
   but the artifact language starts to imply admission anyway;
5. a benchmark artifact would contain a silent SGQF hole or an unexplained
   blocked cell;
6. a phase result would imply HMC readiness, source-faithfulness outside scope,
   or production-default status without the required separate evidence.

## Exit Criteria

The program exits successfully only if:
- fixed SGQF has an explicit admission class for every intended benchmark cell;
- admitted value rows are integrated into the existing benchmark governance
  artifacts;
- admitted gradient rows are backed by **analytical** derivatives only, with
  branch-stable finite-difference promotion evidence;
- autodiff appears only as diagnostic support and never as the promoted SGQF
  gradient route;
- blocked families and blocked score rows remain explicit;
- the final closeout states exactly where fixed SGQF is leaderboard-admitted,
  where it is value-only, where it is analytical-score admitted, and where it
  remains blocked.
