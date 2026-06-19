# P67 Plan: Adjacent Fixed-Branch Ladder Execution

metadata_date: 2026-06-15
status: DRAFT_REVISED_AFTER_R1
parent_result: docs/plans/bayesfilter-highdim-zhao-cui-p66-phase3-closeout-result-2026-06-15.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Objective

Execute the bounded adjacent fixed-branch diagnostics that P66 intentionally
left as schema-only rows.

P67 tests whether the repaired fixed-HMC branch remains admissible and whether
one-factor adjacent comparisons pass a first fixed-budget diagnostic screen
under the reviewed P66 contract:

- candidate branch: `(degree=1, rank=2)`;
- adjacent rank branch: `(degree=1, rank=3)`;
- adjacent degree branch: `(degree=2, rank=2)`.

This is not a structural rank/degree convergence proof, not a d18 correctness
experiment, not an adaptive Zhao--Cui parity experiment, and not an HMC
readiness experiment.

## Entry Conditions

- P66 closeout status:
  `P66_FIXED_BRANCH_VALIDATION_LADDER_REPLACEMENT_PASSED` for schema/contract
  implementation only.
- P66 implemented source-invariant gates, sample-adequacy gates,
  fit-budget resolution, sentinel preservation, and schema-only adjacent rows.
- P66 focused tests passed.
- P60/P65 route-backed regression tests passed.

## Execution Design

All runs are CPU-only unless a separate reviewed GPU plan is written.

Use the existing P59 source-route assembly function for every branch:

```text
p59_author_sir_step_spec_assembly(
    sample_count=1,
    fit_degree=<degree>,
    fit_rank=<rank>,
    fit_sample_count=<budget>,
)
```

The retained `sample_count=1` keeps P67 bounded and comparable to the P60/P65
route-backed diagnostic.  It is a first executed adjacent fixed-budget screen,
not a statistical validation run.

Fit budgets:

| Row | Degree | Rank | Fit samples |
| --- | ---: | ---: | ---: |
| base admissibility candidate | 1 | 2 | 16 |
| rank-ladder candidate | 1 | 2 | 36 |
| rank-ladder stronger row | 1 | 3 | 36 |
| degree-ladder candidate | 1 | 2 | 24 |
| degree-ladder stronger row | 2 | 2 | 24 |

The candidate is reassembled within each comparison at the same fit-sample
budget as the stronger row.  This prevents the ladder result from mixing rank
or degree changes with a fit-budget change.  Equal within-pair budgets are only
a necessary fairness condition.  They do not prove the stronger row is fully
fit-resolved.

The old P60 `(degree=0, rank=1)` versus `(degree=1, rank=2)` comparison remains
sentinel evidence only and is not a pass/fail gate.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the adjacent fixed-branch comparisons execute and pass the bounded fixed-budget screen strongly enough to upgrade P66 from schema-only readiness to executed adjacent-ladder screen evidence? |
| Prior supporting evidence | P66 schema-ready result; P65 repaired high branch; old P60 sentinel gap remains explanatory. |
| Executed comparators | Rank pair `(degree=1, rank=2, fit samples=36)` versus `(degree=1, rank=3, fit samples=36)`; degree pair `(degree=1, rank=2, fit samples=24)` versus `(degree=2, rank=2, fit samples=24)`. |
| Primary pass criterion | Candidate, rank-ladder candidate/stronger, and degree-ladder candidate/stronger rows assemble successfully; source invariants pass; no row is defensive-only; fit-sample adequacy passes; row-level fit diagnostics do not flag budget-limited rows; both adjacent comparisons satisfy the declared delta thresholds. |
| Veto diagnostics | Source invariant drift; missing previous marginal; defensive-only row; zero/near-zero fitted TT collapse; nonfinite diagnostic; unauthorized comparison difference; runtime failure; old P60 sentinel promoted to primary evidence. |
| Explanatory diagnostics | Log-marginal deltas, normalizer-increment deltas, probe and retained log-density median deltas, ESS, correction ranges, square-root normalizers, core diagnostics, row-level fit/budget limitation flags. |
| Not concluded | No structural rank/degree convergence proof, no d18 correctness, no adjacent-ladder theorem, no d50/d100 scaling, no adaptive Zhao--Cui parity, no HMC readiness. |
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p67-adjacent-ladder-execution-result-2026-06-15.md` plus JSON payload. |

## Stability Thresholds

P67 uses the existing P60 engineering thresholds as the first adjacent-ladder
screen:

| Diagnostic | Threshold |
| --- | ---: |
| log marginal absolute delta | 5.0 |
| each normalizer-increment absolute delta | 5.0 |
| probe log-density median absolute delta | 10.0 |
| retained log-density median absolute delta | 10.0 |

These thresholds are diagnostic criteria only.  Passing them establishes only
that the row pair passed this bounded fixed-budget screen.  It does not
establish scientific correctness, structural rank/degree convergence, or that a
larger-budget run would agree.  Failing them does not by itself falsify the
method; it classifies the current fixed branch as not passing this bounded
adjacent fixed-budget screen.

## Row-Level Budget-Limitation Diagnostics

Each row must record fit/budget diagnostics available from the existing
assembly manifests, including at minimum:

- requested fit samples;
- diagnostic-minimum and preferred fit-sample counts;
- rank tuple;
- fit branch hashes and density branch hashes;
- square-root normalizers and defensive-only steps;
- near-zero core counts;
- any fit-status, condition-number, holdout, or warning field exposed in the
  row's transport/fit manifest.

If a row exposes a non-OK fit status, condition-number veto, missing fit
diagnostic, or other budget-limitation warning, P67 must not interpret the
adjacent delta as clean structural rank/degree evidence.  The result must be
`P67_ADJACENT_FIXED_BUDGET_SCREEN_INCONCLUSIVE` or blocked, depending on the
severity.

## Required Artifact

Add a bounded diagnostic runner:

- `scripts/p67_author_sir_adjacent_ladder_diagnostics.py`

The runner may use existing P59/P60/P66 helpers, including private diagnostic
helpers, because it is a reviewed diagnostic artifact rather than a public
library API.

Required JSON fields:

- `status`;
- `blockers`;
- `rows`;
- `sentinel`;
- `rank_ladder`;
- `degree_ladder`;
- `thresholds`;
- `source_invariants`;
- `nonclaims`;
- `run_manifest`.

Required artifact self-check:

- JSON has all required top-level fields.
- Each ladder has candidate and stronger rows.
- Every row records source invariants, sample adequacy, defensive-only status,
  and budget-limitation diagnostics.
- Any pass status is accompanied by `bounded_screen_only = true`.
- Nonclaims include no structural convergence proof, no d18 correctness, no
  HMC readiness, and no adaptive parity.

## Required Checks

Before execution:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  scripts/p67_author_sir_adjacent_ladder_diagnostics.py
```

Execution:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python \
  scripts/p67_author_sir_adjacent_ladder_diagnostics.py \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p67-adjacent-ladder-diagnostics-2026-06-15.json
```

Post-run:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py
```

Artifact self-check:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python \
  scripts/p67_author_sir_adjacent_ladder_diagnostics.py \
  --check-only \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p67-adjacent-ladder-diagnostics-2026-06-15.json
```

If runtime becomes excessive before producing a discriminating artifact, write a
blocker result instead of changing thresholds or silently shrinking the ladder.

## Skeptical Audit

- Wrong baseline: P67 does not use old P60 low/high closeness as the primary
  gate.
- Proxy metrics: sample adequacy permits interpretation but is not convergence;
  deltas are bounded-screen diagnostics, not correctness proof or structural
  rank/degree convergence proof.
- Unfair comparison: each adjacent comparison uses equal fit-sample budgets
  within the compared pair, and row-level budget-limitation diagnostics must be
  checked before interpreting the adjacent delta.
- Missing stop condition: source drift, defensive-only rows, runtime failure,
  and nonconvergent Claude review all stop execution.
- Environment mismatch: CPU-only intent must be set before TensorFlow import.
- Artifact mismatch: the JSON result must contain enough row-level diagnostics
  to support the markdown result; otherwise the run is inconclusive.

## Stop Conditions

- Claude plan review returns material `VERDICT: REVISE` not fixed within five
  rounds.
- The diagnostic runner needs a broader implementation than this plan
  authorizes.
- A required row fails to assemble.
- Any row is defensive-only or source invariants drift.
- Execution exceeds visible runtime without producing a result artifact.
- Results would require changing thresholds after seeing data.

## Review Protocol

Claude is read-only.  It may review this plan, the diagnostic runner, and the
result artifact.  It cannot authorize scientific overclaims or change the
pass/fail criteria after execution.
