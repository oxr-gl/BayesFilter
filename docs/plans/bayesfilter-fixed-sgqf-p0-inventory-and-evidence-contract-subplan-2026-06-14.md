# P0 Subplan: Fixed-SGQF Inventory and Evidence Contract

metadata_date: 2026-06-14
phase: P0
status: DRAFT_REVIEW_READY

## Date

2026-06-14

## Governing Master Program

This phase executes under:

```text
docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md
```

## Purpose

P0 freezes the current evidence base, the gap list, the comparator ladder, the
tolerance vocabulary, and the artifact expectations before any larger execution
ladder begins.  Its job is to stop future workers from improvising labels or
comparing convenience rows as though they answered the same question.

## Scope

This is an inventory and evidence-contract phase.  It does not aim to prove new
numerical behavior.  It aims to produce a durable map from known gaps to the
later phases that will close or block them.

P0 owns:

- current fixed-SGQF test coverage;
- gap-to-phase mapping for G1-G8;
- comparator eligibility rules;
- tolerance-label definitions;
- artifact naming and continuation tokens.

P0 does not own:

- new production algorithm behavior;
- broad runtime claims;
- any baseline ranking result.

## Governing Constraints

1. Inventory existing evidence first.  Do not create new rows merely because a
   future phase might need them.
2. Every comparator must be labeled as one of:
   - `exact_reference`
   - `dense_numerical_reference`
   - `baseline_only`
   - `contract_failure`
3. `dense_numerical_reference` is allowed only on low-dimensional, tractable,
   same-target fixtures.
4. `baseline_only` rows are for positioning only; they are not truth rows.
5. Every future phase must inherit P0's language and may only deviate through an
   explicit reviewed amendment.

## Evidence Contract

Question:

What exactly is already covered in the fixed-SGQF lane, what remains uncovered,
and what labels are allowed for future tests and comparisons?

Primary pass criterion:

- produce a coverage matrix that maps current evidence and gaps G1-G8 into
  specific later phases;
- freeze comparator labels and eligibility rules;
- define a shared tolerance vocabulary for later phase reports.

Veto diagnostics:

- a current one-step nonlinear row is labeled exact;
- a same-target requirement is omitted from the matrix;
- a baseline route is listed without saying what quantity it is allowed to
  compare;
- a future gap is missing or appears in no later phase.

Explanatory-only diagnostics:

- raw test counts;
- file counts;
- number of current fixtures;
- number of planned fixtures per phase.

What will not be concluded:

- no new fixed-SGQF accuracy claim;
- no closure of any numerical gap by inventory alone.

## Required Coverage Matrix Columns

P0 must produce a matrix with at least these columns:

- gap id;
- gap description;
- current evidence file(s);
- current label;
- missing surface;
- primary target phase;
- secondary dependent phases, if any;
- comparator class required;
- expected artifact class;
- nonclaim reminder.

## Comparator Eligibility Rules

### Exact-reference rows

Allowed when:

- the fixture is affine Gaussian and Kalman is genuinely exact for the declared
  scalar and parameterization.

### Dense numerical reference rows

Allowed when:

- the fixture is low-dimensional and numerically tractable;
- the dense comparator evaluates the same target scalar;
- the phase result preserves the dimension, horizon, node count, and why the row
  is treated as a local numerical reference rather than an analytic truth.

### Baseline-only rows

Allowed when:

- the comparator route is same-target and the row is explicitly framed as a
  selected-fixture comparison;
- the phase does not imply that the baseline provides ground truth.

### Contract/failure rows

Allowed when:

- the purpose is to validate branch identity, stage labeling, time indexing,
  diagnostics, or declared failure semantics.

## Tolerance Vocabulary

P0 should freeze the report vocabulary even if exact numbers are later tuned.

Required labels:

- `tight_numeric_parity`
- `local_dense_reference_agreement`
- `qualitative_positioning_only`
- `contract_stage_exactness`
- `blocked_due_to_reference_scope`

Later phases may instantiate numbers, but they should preserve these meanings.

## Execution Steps

1. Inventory current tests in `tests/test_fixed_sgqf_*.py`.
2. Map existing evidence into the four comparator classes.
3. Confirm the known gaps G1-G8 from the governing master.
4. Assign one primary phase to each gap.
5. Define the shared tolerance vocabulary and comparator eligibility rules.
6. Predeclare later-phase artifact stems and continuation tokens.
7. Write the P0 result and review ledger before any later phase claims closure.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-fixed-sgqf-p0-inventory-and-evidence-contract-result-2026-06-14.md`
- Phase review ledger:
  `docs/plans/bayesfilter-fixed-sgqf-p0-claude-review-ledger-2026-06-14.md`
- Optional structured matrix artifact if convenient:
  `docs/plans/bayesfilter-fixed-sgqf-p0-inventory-matrix-2026-06-14.json`

## Stop Rules

Stop if:

- any current evidence row cannot be assigned a label honestly;
- any gap G1-G8 has no primary owning phase;
- a future phase requires a comparator class that P0 cannot define clearly.

## Exit Criteria

P0 exits with `PASS_P0_FIXED_SGQF_INVENTORY_READY_FOR_EXECUTION_PHASES` only if:

- every gap G1-G8 is present and owned;
- every current evidence family is labeled;
- comparator eligibility rules are explicit;
- later phases inherit a stable vocabulary instead of ad hoc wording.
