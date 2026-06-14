# Filtering Value/Gradient Benchmark Gap-Closure Master Program

metadata_date: 2026-06-10
program: filtering-value-gradient-benchmark-gap-closure
status: PLAN_REVIEW_CONVERGED
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Close the pre-benchmark gaps that would otherwise make a full filtering
comparison table misleading.  The downstream benchmark will compare BayesFilter
filters on common observations, common parameter settings, common horizons, and
common value/gradient definitions before the project moves from filtering to
Bayesian estimation.

The benchmark must not exclude non-LGSSM models merely because UKF, SVD, CUT4,
Zhao-Cui, bootstrap DPF, or Algorithm 1 UKF LEDH-PFPF are approximations there.
Exactness is a cell attribute, not a global admission gate.  LGSSM has an exact
Kalman oracle.  Other models may use dense numerical references, transformed-SV
references, Gaussian-mixture references, or diagnostic references with explicit
labels.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What must be repaired before running a useful all-filter, all-model value and gradient benchmark for the filtering part of BayesFilter? |
| Baseline/comparator | Current BayesFilter filters and runners; P30/P43/P44/P50/P51/P53 result ledgers; current DPF Algorithm 1 UKF route; LGSSM Kalman oracle; dense or transformed references for non-LGSSM rows. |
| Primary pass criterion | Every identified pre-benchmark gap has a phase subplan, exit criterion, artifact path, stop condition, and Claude read-only review loop rule. |
| Veto diagnostics | Same-target exactness imposed outside LGSSM; old LEDH-PFPF-OT used as current evidence; stale scalar-only Zhao-Cui blockers retained in the benchmark registry; DPF gradients hidden instead of reported; proxy smoke tests treated as benchmark evidence; any phase lacking a concrete output artifact. |
| Explanatory diagnostics | Existing tests and result ledgers, small adapter smokes, dense lower-rung tie-outs, finite-gradient checks, Monte Carlo standard errors, ESS and resampling diagnostics, runtime metadata. |
| Not concluded | This plan alone does not run the full benchmark, rank algorithms, certify DPF gradients, certify HMC readiness, or claim production Bayesian-estimation readiness. |
| Artifacts | This master program, phase subplans, Claude review ledger, future phase result notes, benchmark registry JSON, benchmark output matrices. |

## Skeptical Plan Audit

Status: REQUIRED_BEFORE_EXECUTION.

- Wrong baseline risk: the benchmark must compare every filter to the declared
  row reference, not to another approximation silently promoted to truth.
- Proxy promotion risk: adapter smoke tests may unlock the full benchmark, but
  they are not benchmark results.
- Missing stop-condition risk: each phase has explicit pass/block tokens and
  human-required blockers.
- Unfair comparison risk: algorithms may be approximate on non-Gaussian rows,
  but they must receive the same observations, theta, horizon, dtype, and error
  metric for the row.
- Hidden assumption risk: "same target" means exact only for rows whose
  reference is exact.  For SV Gaussian-mixture and transformed rows, the target
  identity must be recorded cell-by-cell.
- Environment mismatch risk: CPU-only TensorFlow validation must hide GPUs with
  `CUDA_VISIBLE_DEVICES=-1`; GPU or Claude commands require trusted/elevated
  execution under project policy.
- Artifact-answer risk: no phase passes without a durable artifact under
  `docs/plans` or `experiments/.../outputs`.

## Phase Index

| Phase | Name | Subplan | Required result artifact | Pass/block token |
| --- | --- | --- | --- | --- |
| P0 | Benchmark Contract And Gap Lock | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p0-contract-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p0-contract-result-2026-06-10.md` | `PASS_FILTER_BENCH_P0_CONTRACT` or `BLOCK_FILTER_BENCH_P0_CONTRACT` |
| P1 | Target Registry And Reference Taxonomy | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p1-target-registry-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p1-target-registry-result-2026-06-10.md` | `PASS_FILTER_BENCH_P1_TARGET_REGISTRY` or `BLOCK_FILTER_BENCH_P1_TARGET_REGISTRY` |
| P2 | Unified Filter Adapter Protocol | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p2-adapter-protocol-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p2-adapter-protocol-result-2026-06-10.md`; concrete adapter schema/interface artifact | `PASS_FILTER_BENCH_P2_ADAPTER_PROTOCOL` or `BLOCK_FILTER_BENCH_P2_ADAPTER_PROTOCOL` |
| P3 | Reference Oracle Wiring | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p3-reference-oracles-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p3-reference-oracles-result-2026-06-10.md` | `PASS_FILTER_BENCH_P3_REFERENCE_ORACLES` or `BLOCK_FILTER_BENCH_P3_REFERENCE_ORACLES` |
| P4 | Deterministic Filter Wiring | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p4-deterministic-filters-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p4-deterministic-filters-result-2026-06-10.md` | `PASS_FILTER_BENCH_P4_DETERMINISTIC_FILTERS` or `BLOCK_FILTER_BENCH_P4_DETERMINISTIC_FILTERS` |
| P5 | DPF Filter Wiring And Supersession Guard | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p5-dpf-filters-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p5-dpf-filters-result-2026-06-10.md` | `PASS_FILTER_BENCH_P5_DPF_FILTERS` or `BLOCK_FILTER_BENCH_P5_DPF_FILTERS` |
| P6 | Gradient Semantics And Status Taxonomy | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p6-gradient-semantics-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p6-gradient-semantics-result-2026-06-10.md` | `PASS_FILTER_BENCH_P6_GRADIENT_SEMANTICS` or `BLOCK_FILTER_BENCH_P6_GRADIENT_SEMANTICS` |
| P7 | Preflight Matrix Coverage | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p7-preflight-matrix-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p7-preflight-matrix-result-2026-06-10.md` | `PASS_FILTER_BENCH_P7_PREFLIGHT_MATRIX` or `BLOCK_FILTER_BENCH_P7_PREFLIGHT_MATRIX` |
| P8a | Synthetic-Truth Benchmark Contract Preflight | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-synthetic-truth-runner-subplan-2026-06-11.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-synthetic-truth-runner-result-2026-06-11.md`; old blocked matrix result retained as historical context | `PASS_FILTER_BENCH_P8_SYNTHETIC_TRUTH_CONTRACT` and `BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING` |
| P8b | Numeric Benchmark Execution And Tables | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-master-plan-2026-06-11.md` plus a 2026-06-12 execution update before launch | reviewed value, componentwise score, curvature/status, failure, and stochastic uncertainty artifacts | `PASS_P8_B7_NUMERIC_BENCHMARK_RUNNER` and `PASS_P8_B8_REVIEWED_CLOSEOUT`, or `BLOCK_P8_B7_NUMERIC_BENCHMARK_RUNNER` |
| P9 | Integration Closeout | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p9-closeout-subplan-2026-06-10.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p9-closeout-result-2026-06-11.md` | `PASS_FILTER_BENCH_P9_CLOSEOUT` or `BLOCK_FILTER_BENCH_P9_NUMERIC_BENCHMARK_PENDING` |

## Phase Dependency DAG

```text
P0 contract
  -> P1 target registry
    -> P2 adapter protocol and exercised schema fixtures
      -> P3 reference oracles
        -> P4 deterministic filter wiring
        -> P5 DPF filter wiring
          -> P6 gradient semantics and status taxonomy
            -> P7 preflight matrix
              -> P8a synthetic-truth contract preflight
                -> P8b numeric benchmark runner and tables
                  -> P9 closeout
```

P4 and P5 may be implemented in parallel after P2 and P3 both pass.  P6 cannot
pass until P4 and P5 expose enough exercised cells to classify deterministic and
particle-filter gradients.  P7 cannot pass until P4, P5, and P6 pass.  P8a
cannot freeze the benchmark contract until P7 passes.  P8b cannot run the full
numeric comparison until P8a passes and the numeric evidence contract is
restated.

2026-06-11 amendment: P8 is now the synthetic-truth benchmark contract gate.
The full numeric benchmark remains blocked until accepted truth draws,
synthetic datasets, horizon/seed calibration, and reviewed evaluator outputs
exist.

2026-06-12 planning correction: the previous wording made the P8 contract gate
look too much like Phase 8 completion.  `PASS_FILTER_BENCH_P8_SYNTHETIC_TRUTH_CONTRACT`
is only the P8a preflight pass.  Phase 8 is not complete until P8b emits the
actual numeric value, componentwise score, curvature/status, failure, and
stochastic uncertainty tables and those artifacts pass read-only review.  Until
then, `BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING` remains the
controlling status for downstream closeout.

2026-06-11 source-paper scope amendment: after the P10 truth-prior literature
audit, promoted source-paper benchmark execution no longer uses the earlier
P44-inclusive diagnostic roster.  The old P1/P7/P8 roster remains historical
provenance for the diagnostic gap-closure pass.  Future promoted source-paper
numeric tables must use
`docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`.
P44 cubic, P44 quadratic, and P44 tanh-transition diagnostic rows are excluded
from promoted source-paper tables.  Exact Zhao--Cui paper/code values are the
test values for the promoted source-paper rows.  Lower-rung and project-only
fixtures may remain as engineering diagnostics only when labeled as such.

## Required Benchmark Rows

Historical P1/P7/P8 diagnostic gap-closure target registry included at least:

- LGSSM exact Kalman row;
- P44 cubic additive-Gaussian panel row;
- P44 quadratic observation row;
- P44 nonlinear transition row;
- SV transformed/log-additive non-Gaussian row;
- SV Gaussian-mixture approximation row;
- native generalized SV lower-rung dense-reference row when in scope;
- spatial SIR lower-rung and admitted scaling-route rows;
- predator-prey lower-rung and production-tuning rows.

P1 may split rows by dimension, horizon, or reference type, but it must not drop
a model/filter pair solely because a filter is approximate on that model.

Promoted source-paper benchmark execution supersedes that diagnostic list with
the source-paper scope contract:

- Zhao--Cui LGSSM/Kalman `m=n=3`, `T=50`, truth `(a,d)=(0.8,0.5)`;
- Zhao--Cui synthetic SV actual transformed non-Gaussian row with `T=1000`,
  `sigma=1`, truth `(gamma,beta)=(0.6,0.4)`;
- Zhao--Cui/KSC Gaussian-mixture SV surrogate row with the same SV truth and a
  surrogate-target label;
- Zhao--Cui spatial SIR `J=9`, `d=18`, `T=20`, fixed `kappa=0.1`, `nu=18`
  row, blocked from numeric performance until the d=18 value route is repaired;
- Zhao--Cui predator-prey `T=20`, `x0=(50,5)`, physical truth
  `(r,K,a,s,u,v)=(0.6,114,25,0.3,0.5,0.5)`;
- Zhao--Cui generalized SV `svmodels` synthetic row: use Zhao--Cui
  reported/estimated parameter values as the truth vector, generate synthetic
  benchmark data from those values, and block numeric execution until the
  estimated vector is extracted, digitized, or regenerated from the author
  pipeline.  Do not use SP500 returns directly as the benchmark data and do
  not substitute the old native generalized SV project fixture.

P44 cubic/quadratic/tanh rows are explicitly excluded from promoted
source-paper numeric tables.

## Required Algorithm Rows

The algorithm registry must include at least:

- Kalman where the model is LGSSM or a declared Gaussian-mixture enumeration row;
- UKF;
- SVD sigma-point;
- CUT4;
- Zhao-Cui scalar or multistate route, using the new multistate route where
  applicable rather than stale scalar-only blockers;
- bootstrap DPF;
- source-faithful Algorithm 1 UKF LEDH-PFPF no-resampling/current route;
- optional resampling-enabled DPF rows with explicit gradient status.

Historical `LEDH-PFPF-OT` rows are forbidden as current evidence.  They may
appear only as superseded historical comparison records.

## Repair Loop Rule

Codex remains supervisor and executor.  Claude Code is read-only reviewer.
For each phase and for the whole plan:

1. Codex drafts or implements the phase artifact.
2. Codex runs focused local validation if the phase touches code or structured
   data.
3. Codex asks Claude for read-only review.
4. If Claude returns `VERDICT: REVISE`, Codex fixes material findings and
   resubmits.
5. Stop early on `VERDICT: AGREE`.
6. Stop after five review iterations.  If a major blocker remains at iteration
   five, record a block token and do not proceed to dependent phases.

Fixable issues include stale labels, missing metadata, adapter wiring bugs,
failed focused tests with a clear repair path, and incomplete result matrices.

Human-required blockers include package installation, network fetches,
credentials, broad filesystem edits outside this repo, destructive git actions,
GPU claims without trusted approval, and changing benchmark criteria after
seeing full benchmark results.

## Claude Review Prompt Contract

Each Claude prompt must ask for:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
MAJOR:
- ...
MINOR:
- ...
```

Claude must review as read-only.  If Claude does not respond, Codex must run a
small probe.  If the probe responds, Codex must shorten or split the review
prompt and retry rather than declaring Claude unavailable.

## Approval Needs For Later Execution

The execution phase will need approval or existing approval for:

- trusted Claude Code wrapper use for read-only review;
- CPU-only TensorFlow/TFP tests with `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`;
- focused `pytest`, `python -m compileall`, and `git diff --check`;
- no network fetch, package install, GPU run, detached Codex agent, or
  destructive git command unless separately approved.
