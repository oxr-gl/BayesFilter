# DPF V2 Algorithm Full Comparison P8 Closeout Subplan

metadata_date: 2026-06-07
phase: P8
status: REVIEWED_READY_FOR_PHASE_EXECUTION_AFTER_P7_PASS

## Question

After P0--P7, what can we responsibly say about bootstrap-OT and
LEDH-PFPF-OT BF/FilterFlow agreement across all V2 models?

## Inputs

- P0--P7 result ledgers.
- P0--P7 JSON and markdown artifacts.
- Claude phase review ledgers.

## Evidence Contract

Primary criterion:

- Close as `PASS_FULL_COMPARISON` only if:
  - bootstrap-OT contracts, values, and fixed-branch AD gradients passed for
    all six V2 rows;
  - LEDH-PFPF-OT contracts, values, and fixed-branch AD gradients passed for all
    six V2 rows;
  - no material veto remains open;
  - all non-claims are preserved.
- Close as `BLOCKED_WITH_REVIEWED_CLASSIFICATION` if any row or gradient knob is
  blocked after reviewed repair attempts.

Veto diagnostics:

- any unexecuted required row reported as success;
- any unresolved mismatch;
- any unsupported claim about stochastic resampling, mathematical correctness,
  student implementations, TT/SIRT, paper tables, GPU, HMC, DSGE, scalability,
  or production readiness;
- any missing command manifest or checksum.

Explanatory-only diagnostics:

- runtime summaries;
- row-level robustness diagnostics;
- optional stochastic smoke evidence if separately planned;
- comparison to closed deterministic V2 tie-out.

Non-claims:

- P8 does not convert agreement into correctness.

Artifacts:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-closeout-result-2026-06-07.md`
- `experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_closeout_2026-06-07.json`
- `experiments/dpf_implementation/reports/dpf-v2-algorithm-full-comparison-closeout-2026-06-07.md`

## Tasks

1. Validate every required phase artifact.
2. Build row-by-row and algorithm-by-algorithm decision tables.
3. State strongest alternative explanation.
4. State what would overturn the closeout.
5. Update DPF chapter only after a separate reviewed documentation amendment if
   scientific wording needs to change.
6. Run Claude closeout/governance review.

## Exit Criteria

- P8 result declares either `PASS_FULL_COMPARISON` or
  `BLOCKED_WITH_REVIEWED_CLASSIFICATION`.

## Stop Conditions

- Any human-intervention blocker remains unresolved.
- Any requested wording would overclaim beyond the evidence contract.
