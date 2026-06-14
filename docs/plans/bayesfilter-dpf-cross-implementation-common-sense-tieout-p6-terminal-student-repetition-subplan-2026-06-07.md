# P6 Terminal Student Repetition Subplan

metadata_date: 2026-06-07
parent_program: `bayesfilter-dpf-cross-implementation-common-sense-tieout-plan-2026-06-06.md`
phase_status: terminal_deferred

## Phase Question

After P0--P5 have closed the BayesFilter-vs-executable-FilterFlow comparator,
can the same closed fixture campaign be repeated against the two student
implementations, with every agreement or discrepancy classified without
treating any implementation as an oracle?

## Entry Gate

P6 may begin only after all of the following are true:

- P0 governance has converged under Claude review;
- P1 common density contracts are `MATCHED` or classified;
- P2 deterministic no-resampling value paths are `MATCHED` or classified;
- P3 fixed-ancestor resampling value paths are `MATCHED` or classified;
- P4 fixed-branch gradients are `MATCHED` or classified;
- P5 remaining BayesFilter/FilterFlow coverage has no unclassified surface;
- the closed BayesFilter/FilterFlow fixture bundle has a manifest listing
  model specs, scalar objectives, parameters, observations, particles,
  innovations, ancestor maps, branch timing, dtype, tolerances, seeds, and
  artifact checksums.

If any P0--P5 gate is open, P6 is blocked.  Student outputs must not be used to
revise the BayesFilter/FilterFlow comparator before that closure.

## Evidence Contract

Primary comparator:

- the closed P1--P5 fixture bundle and its BayesFilter/FilterFlow ledgers;
- student implementation adapters only as peer implementations of the same
  declared fixtures.

Primary pass criterion:

- each student-repeat cell is assigned one of:
  `MATCHED`, `EXPLAINED_MISMATCH`, `INTERFACE_BLOCKED`, or `OUT_OF_SCOPE`, with
  a concrete reason and artifact.  A cell is `MATCHED` only when the student
  implementation uses the same mathematical model, scalar objective, physical
  parameterization, branch schedule, particles, innovations, observations,
  dtype policy, and tolerance as the closed fixture.

Veto diagnostics:

- P0--P5 not closed;
- missing closed-fixture manifest field;
- using a student output to change the BayesFilter/FilterFlow comparator;
- treating BayesFilter, FilterFlow, either student repo, TT, paper tables, or
  dense quadrature as an oracle;
- running a student model that is not the same mathematical object while
  calling it a match attempt;
- unclassified student discrepancy;
- forcing a near-miss into `MATCHED` by changing tolerances after seeing the
  result;
- missing command manifest, repository provenance, seed, dtype, or adapter
  checksum;
- CPU-only TensorFlow import without `CUDA_VISIBLE_DEVICES=-1`.

Explanatory diagnostics:

- per-cell deltas, interface notes, finite-difference self-checks, source-code
  pointers, parameter-transform notes, branch ledgers, and student repository
  provenance.  These explain a classification; they do not by themselves prove
  filtering correctness.

Non-claims:

- agreement with a student implementation is not scientific correctness;
- disagreement with a student implementation is not a student failure unless
  the mismatch is traced to a concrete bug in that implementation;
- interface blocking is not a scientific result;
- P6 does not validate TT filters, paper-scale tables, random resampling
  distributions, HMC, DSGE, GPU execution, or production readiness.

## Planned Work Items

1. Freeze the closed P1--P5 fixture bundle into a P6-ready manifest.
2. Inventory student adapter surfaces and map each one to the closed fixture
   cells it can honestly run.
3. Run student repeats only for cells with the same mathematical object and
   scalar objective.
4. Classify every executed student cell as `MATCHED` or
   `EXPLAINED_MISMATCH`.
5. Classify unavailable or incompatible student surfaces as
   `INTERFACE_BLOCKED` or `OUT_OF_SCOPE`.
6. Preserve separate terminal ledgers for student comparisons so they cannot
   back-propagate into the BayesFilter/FilterFlow closure.

## Planned Artifacts

- Result ledger:
  `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p6-terminal-student-repetition-result-2026-06-07.md`
- Closed-fixture manifest:
  `experiments/dpf_implementation/reports/outputs/dpf_cross_impl_closed_fixture_manifest_2026-06-07.json`
- Student repetition output:
  `experiments/dpf_implementation/reports/outputs/dpf_cross_impl_terminal_student_repetition_2026-06-07.json`

## Command Policy

No P6 execution command is approved by this subplan until P0--P5 are closed and
the closed-fixture manifest exists.  When P6 is opened, commands must use the
same CPU-only TensorFlow policy as the BayesFilter/FilterFlow tie-outs unless a
new evidence contract justifies GPU use:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m <p6_student_repeat_runner>
CUDA_VISIBLE_DEVICES=-1 python -m <p6_student_repeat_runner> --validate-only
```

The placeholder runner name is intentional.  A concrete runner should be named
only after the P6 manifest and student adapter inventory determine the exact
executable surface.

## Exit Gate

P6 exits when every eligible student-repeat cell has a terminal classification,
all discrepancies are either explained or interface-blocked, and the result
ledger states clearly that this is common-sense cross-implementation evidence,
not correctness evidence for any filter algorithm or repository.
