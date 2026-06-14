# DPF Cross-Implementation Common-Sense Tie-Out Master Program

metadata_date: 2026-06-07
program_status: active_master_program

## Program Question

Can BayesFilter and executable float64 FilterFlow be tied out on the same
declared small filtering computations across density components, deterministic
value paths, fixed resampling branches, and fixed-branch gradients before any
student implementation is touched?

Only after the BayesFilter-vs-FilterFlow matrix is closed should the same
fixture campaign be repeated against the two student implementations.  No
student output is an oracle, and no student output should shape the
BayesFilter/FilterFlow comparator while that comparator is still being defined.

## Program Evidence Contract

Primary engineering question:

- can BayesFilter and executable float64 FilterFlow be tied out on declared
  small filtering computations before larger validation, correctness claims, or
  student-repository comparisons?

Primary comparator:

- executable local float64 FilterFlow under `.localsource/filterflow` for
  BayesFilter-vs-FilterFlow cells where FilterFlow has a comparable model and
  filter surface.

Deferred comparator:

- existing student-baseline adapters under
  `experiments/student_dpf_baselines` are excluded from active comparator work.
  They become eligible only in the terminal student-repetition phase.

Primary pass criterion:

- each BayesFilter/FilterFlow cell is either `MATCHED` within declared
  tolerance, `EXPLAINED_MISMATCH` with a concrete mismatch class, or
  `INTERFACE_BLOCKED` with a concrete interface reason.  No unclassified
  executed mismatch may remain before entering the student phase.

Veto diagnostics:

- nonfinite scalar or gradient in an executed cell;
- missing manifest, dtype, seed, branch, scalar, or parameterization fields;
- unclassified mismatch;
- treating BayesFilter, FilterFlow, TT, paper tables, dense quadrature, or
  student output as an oracle;
- gradient comparison across incompatible branches or scalar objectives;
- `.localsource/filterflow` mutation without explicit approval;
- CPU-only TensorFlow import before `CUDA_VISIBLE_DEVICES=-1`;
- any student-repository command before BayesFilter/FilterFlow closure.

Explanatory diagnostics:

- Kalman references, dense quadrature, finite differences, residuals, ESS,
  runtime, row residuals, Monte Carlo standard errors, and implementation
  inventory notes.  These explain or veto only under a phase-specific contract;
  they are not correctness criteria by default.

Non-claims:

- no filtering-algorithm correctness;
- no claim that BayesFilter, FilterFlow, or a student repo is scientifically
  correct;
- no TT-filter correctness;
- no paper-scale validation;
- no HMC/DSGE/GPU/production readiness;
- no claim that interface-blocked models have failed.

## Phase Gates

| Phase | Subplan | Active comparator | Exit gate |
|---|---|---|---|
| P0 Governance and Scope | `bayesfilter-dpf-cross-implementation-common-sense-tieout-p0-governance-subplan-2026-06-07.md` | BayesFilter/FilterFlow only | evidence contract, vetoes, and no-oracle policy are explicit |
| P1 Common Model Contracts | `bayesfilter-dpf-cross-implementation-common-sense-tieout-p1-common-model-contracts-subplan-2026-06-07.md` | BayesFilter/FilterFlow only | shared density contracts exist and match or are classified |
| P2 Deterministic Value Paths | `bayesfilter-dpf-cross-implementation-common-sense-tieout-p2-value-paths-subplan-2026-06-07.md` | BayesFilter/FilterFlow only | fixed-noise no-resampling paths match or are classified |
| P3 Fixed Resampling Branches | `bayesfilter-dpf-cross-implementation-common-sense-tieout-p3-fixed-resampling-subplan-2026-06-07.md` | BayesFilter/FilterFlow only | fixed-ancestor branch paths match or are classified |
| P4 Fixed-Branch Gradients | `bayesfilter-dpf-cross-implementation-common-sense-tieout-p4-fixed-branch-gradients-subplan-2026-06-07.md` | BayesFilter/FilterFlow only | fixed-branch gradients match and pass finite-difference checks or are classified |
| P5 Remaining BayesFilter/FilterFlow Coverage | `bayesfilter-dpf-cross-implementation-common-sense-tieout-p5-remaining-bf-ff-coverage-subplan-2026-06-07.md` | BayesFilter/FilterFlow only | uncovered surfaces are matched, explained, or interface-blocked |
| P6 Terminal Student Repetition | `bayesfilter-dpf-cross-implementation-common-sense-tieout-p6-terminal-student-repetition-subplan-2026-06-07.md` | BayesFilter/FilterFlow/student peers | starts only after P0--P5 closure |

## Current Completed Evidence

The following artifacts already support the BayesFilter/FilterFlow ladder:

- density contracts:
  `docs/plans/bayesfilter-dpf-common-model-suite-implementation-result-2026-06-06.md`;
- fixed-noise no-resampling path:
  `docs/plans/bayesfilter-dpf-common-filter-path-noresampling-result-2026-06-06.md`;
- fixed-ancestor resampling path:
  `docs/plans/bayesfilter-dpf-common-filter-path-fixed-resampling-result-2026-06-06.md`;
- fixed-branch gradients:
  `docs/plans/bayesfilter-dpf-common-fixed-branch-gradient-result-2026-06-06.md`;
- non-LGSSM density/gradient and interface inventory:
  `docs/plans/bayesfilter-dpf-nonlgssm-cross-implementation-matching-result-2026-06-06.md`.

These artifacts are consistency evidence only.  They do not close remaining
BayesFilter/FilterFlow surfaces not yet represented in the common model suite.

## Program Execution Rules

- Execute phases in order unless a later phase is strictly documentation-only.
- Do not run student commands before P0--P5 closure.
- Preserve all command manifests and JSON artifacts for executed phases.
- Prefer small deterministic fixtures before stochastic sweeps.
- Use CPU-only TensorFlow for these tie-outs unless a later phase explicitly
  justifies GPU use.
- Treat interface blockers as outcomes, not failures.
- Do not mutate `.localsource/filterflow` without explicit approval and a
  provenance note.

## Program Stop Conditions

- Stop before execution if the phase evidence contract cannot name the scalar,
  branch, parameterization, and comparator.
- Stop if a mismatch is unclassified.
- Stop if a student command is about to run before P0--P5 closure.
- Stop if validation artifacts cannot answer the phase question.

## Review Loop Requirement

This master program and all phase subplans require Claude review.  Review loops
must run until convergence or five total rounds, whichever comes first.  A
review round converges when Claude reports no material blockers, or when all
material blockers have been patched and the remaining issues are explicitly
classified as scope notes.

Claude review ledger:

- `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-master-program-claude-review-ledger-2026-06-07.md`

## Skeptical Plan Audit

Status: `PASS_WITH_STUDENT_PHASE_DEFERRED`.

Wrong baseline risk:

- the program excludes TT, paper tables, dense quadrature, BayesFilter,
  FilterFlow, and student outputs as oracles.  Each phase must declare its own
  executable comparator.

Proxy metric risk:

- residuals, finite differences, runtime, ESS, and reference filters are
  explanatory unless a phase contract explicitly promotes them to pass/fail or
  veto diagnostics.

Unfair comparison risk:

- models without comparable FilterFlow surfaces are marked
  `INTERFACE_BLOCKED`; they are not counted as scientific failures.

Hidden assumption risk:

- gradient tie-outs are restricted to fixed branches and the same scalar
  objective.  Random or differentiable resampling gradients require a separate
  later program.

Premature-student risk:

- any student command before BayesFilter/FilterFlow closure is a veto.  Student
  outputs cannot become accidental baselines or repair targets.
