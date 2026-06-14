# P57-M9 Result: Spatial SIR Validation Ladder

metadata_date: 2026-06-11
status: BLOCK_P57_M9_SPATIAL_SIR_VALIDATION_LADDER

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can the repaired source route run and validate the Zhao-Cui spatial SIR example at d=18, then stress d=50/d=100 without overclaiming? |
| Baseline/comparator | Author SIR settings, M1 callback parity, M6 source-loop skeleton, M7 source-rank policy, M8 preconditioned Algorithm 5 surface, and the M9 subplan claim tiers. |
| Primary criterion | d=18 must use the source-route pipeline and pass a declared comparator tier before any correctness-style claim. |
| Veto diagnostics | A d=18 run through the old local/operator/all-grid route would violate source faithfulness; a contract-double M6 loop would not be the author spatial SIR pipeline; UKF/rank/memory diagnostics cannot substitute for a source-route d=18 result. |
| Not concluded | No d=18 spatial SIR success, no d=50/d=100 scaling success, no HMC readiness, no correctness candidate, and no same-route rank convergence. |

## Decision

M9 is blocked, not passed.

The repo has the prerequisite pieces from P57-M1 through P57-M8, but no
assembled fixed-HMC source-route spatial SIR pipeline that:

1. builds the author d=18 SIR adjacent target using the M1 source callback;
2. fits a fixed TT/SIRT transport object for that target at the declared rank;
3. carries retained objects through the M6 sequential loop;
4. uses the M8 preconditioned route where required by the author example;
5. produces a comparator-tier result under the M7 rank policy; and
6. emits a d=18 run manifest with value, gradient, replay, ESS, normalizer,
   rank, memory, and wall-time diagnostics.

Running the old P46/P47/P50/P51 local/operator/all-grid spatial-SIR path would
answer the wrong route question. Running only the M6 contract-double source
loop would prove the skeleton again but would not validate author spatial SIR.

## Skeptical Audit

Status: `BLOCK`.

- Wrong-baseline risk: detected. The existing older spatial-SIR production
  route is the all-grid/local route previously classified as a blocker for
  paper-scale source-faithful claims.
- Proxy-risk: detected and rejected. UKF scout, memory budget, finite values,
  and M8 analytic source-surface checks cannot become the M9 d=18 comparator.
- Missing-stop risk: continuing to M10 with a hidden M9 pass would violate the
  runbook and M11 claim gate.
- Artifact-risk: this result emits the required block token and preserves the
  missing implementation boundary.

## Searches And Checks

Commands run:

```text
find . -path './.git' -prune -o -type f \( -name '*p57*m9*' -o -name '*spatial*sir*source*' -o -name '*sir*source*route*' \) -print
```

Result: only the M9 subplan exists; no M9 implementation/result artifact was
present before this result.

```text
rg -n "source-route pipeline|source_route pipeline|fixed TT/SIRT spatial|author SIR.*FixedTTSIRT|sir_austria.*FixedTTSIRT|d18_execution_only|d18_same_route|d18_correctness|BLOCK_P57_M9|PASS_P57_M9" docs/plans bayesfilter tests experiments scripts
```

Result: no assembled d=18 source-route pipeline or comparator-tier M9 result
was found.

```text
rg -n "source_route_run_sequential_fixed_hmc\(|SourceRouteSequentialStepSpec\(|SourceRoutePreconditionedMap\(|source_route_preconditioned_proposal_correction\(" . --glob '!docs/plans/bayesfilter-dpf-*' --glob '!experiments/dpf_implementation/reports/outputs/*.json'
```

Result: source-route sequential usage is limited to the M6 contract-double
tests; M8 preconditioned usage is limited to M8 analytic tests.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m1_author_sir_callback_parity.py tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py tests/highdim/test_p57_m7_source_faithful_rank_ukf_calibration.py tests/highdim/test_p57_m8_preconditioned_algorithm5.py tests/highdim/test_p51_spatial_sir_route_preflight.py
```

Result:

```text
24 passed, 2 warnings
```

Interpretation: supporting gates pass, but they do not assemble or validate
the d=18 source-route spatial SIR ladder.

## Human-Required Or Repairable?

This is not a request for a new scientific direction, but it is a real
implementation gap beyond a local test repair. The next required work is a new
implementation phase or amendment that assembles the author SIR source-route
fitting pipeline from the existing pieces and then runs the M9 ladder.

Until that exists, P57 cannot declare:

- `d18_spatial_sir_same_route_rank_convergence`;
- `d18_spatial_sir_correctness_candidate`;
- `d50_or_d100_scaling_stress`; or
- `HMC_readiness`.

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Block M9 after precheck. | Not met: no assembled source-route d=18 spatial SIR pipeline and comparator tier. | Veto triggered for using old local/all-grid route or contract doubles as a d=18 source-route result. | How to assemble the fixed TT/SIRT fitting pipeline for author d=18 SIR without inventing a non-source route. | Write a reviewed implementation amendment before rerunning M9. | No spatial SIR validation or scaling claim. |

## Token

`BLOCK_P57_M9_SPATIAL_SIR_VALIDATION_LADDER`
