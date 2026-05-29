# Plan: MP5 clean-room implementation scaffold

## Date

2026-05-13

## Status

Planned.  Do not execute until explicitly instructed.

This is a student DPF experimental-baseline lane plan.  It is not a production
BayesFilter implementation plan and is not part of the DPF monograph writing
lane.

Execution-readiness caveat: as of the 2026-05-15 supervisor review,
`experiments/controlled_dpf_baseline/` contains only README scaffolding.
Therefore MP6-MP8 are not executable until MP5 creates the exact package
surfaces, runner entry points, validation helper, and artifact layout listed
below.

## Governing inputs

- master program:
  `docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md`;
- reset memo:
  `docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md`;
- clean-room specification:
  `docs/plans/bayesfilter-student-dpf-baseline-clean-room-controlled-baseline-spec-2026-05-13.md`;
- clean-room specification result:
  `docs/plans/bayesfilter-student-dpf-baseline-clean-room-controlled-baseline-spec-result-2026-05-13.md`.

## Goal

Create the BayesFilter-owned experimental scaffold for a clean-room controlled
baseline under `experiments/controlled_dpf_baseline/` without importing,
copying, or editing student code.

This phase should implement only the infrastructure needed to run the later
fixed target grid:

- fixture generator or fixture loader;
- result schema;
- metric functions;
- clean-room import guards;
- one minimal regularized particle-flow/bootstrap-particle hybrid scaffold with
  explicit flow-step control;
- syntax and small deterministic smoke checks.

It should not run the full comparison grid.  Full-grid execution belongs to
MP6.

## Owned write set

Allowed:

- `experiments/controlled_dpf_baseline/`;
- `docs/plans/bayesfilter-student-dpf-baseline-mp5-clean-room-implementation-plan-2026-05-13.md`;
- MP5 audit/result notes whose filenames begin with
  `docs/plans/bayesfilter-student-dpf-baseline-mp5-`;
- `docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md`.

Out of scope:

- production `bayesfilter/`;
- `docs/chapters/ch19*.tex`;
- `docs/references.bib`;
- DPF monograph rebuild/enrichment plans or reset memos;
- `experiments/student_dpf_baselines/vendor/`;
- copying student classes, functions, control flow, tuning tricks, or numerical
  shortcuts.

## Hypotheses

### MP5-H1: fixture generation can be implemented clean-room

Criterion:

- generated fixture arrays exactly match the BayesFilter-owned nonlinear
  fixtures, or numerical differences are recorded and the phase chooses stored
  BayesFilter-owned arrays for MP6.

Veto:

- fixture implementation requires reading or copying student vendor source.

### MP5-H2: metric and result schema are independent of student adapters

Criterion:

- metrics can evaluate synthetic candidate trajectories and produce finite
  values or structured blockers.

Veto:

- metrics call student adapters or assume student-specific fields.

### MP5-H3: a minimal flow-assisted baseline scaffold can be written without
student code

Criterion:

- the algorithm object exposes particle count, seed, and flow-step or
  integration-step controls and runs one short smoke case.

Veto:

- the implementation imports from `experiments/student_dpf_baselines/vendor/`,
  `advanced_particle_filter`, `2026MLCOE`, or student `src.*` modules.

## Required implementation shape

The first clean-room controlled-target scaffold should be deliberately small
and mathematically explicit:

- transition proposal: sample particles from the fixture transition model;
- observation update: evaluate the Gaussian range-bearing likelihood using the
  fixture observation covariance;
- flow update: apply a deterministic EKF-style innovation displacement over
  `flow_steps` substeps before or during weighting, using the fixture
  range-bearing Jacobian;
- resampling: use a locally implemented, documented resampler such as systematic
  resampling with a labeled ESS threshold;
- outputs: filtered means shaped for the metric contract, optional covariances,
  ESS sequence, resampling count, runtime, and diagnostics.

The scaffold does not need to be optimal.  It must be auditable, bounded, and
independent.  Any numerical stabilization must be explained in comments or
diagnostics and must not come from student source.

Plain bootstrap PF, EKF, or UKF sanity references are allowed only as
separately labeled references.  They must not be reported as satisfying the
clean-room N128/steps10 or N128/steps20 controlled target.

## Required files and fixed surfaces

MP5 must create or update exactly these implementation surfaces unless it stops
with `mp5_needs_revision` and records why the surface contract is wrong:

- `experiments/controlled_dpf_baseline/__init__.py`;
- `experiments/controlled_dpf_baseline/fixtures/__init__.py`;
- `experiments/controlled_dpf_baseline/fixtures/range_bearing.py`;
- `experiments/controlled_dpf_baseline/metrics.py`;
- `experiments/controlled_dpf_baseline/results.py`;
- `experiments/controlled_dpf_baseline/prototypes/__init__.py`;
- `experiments/controlled_dpf_baseline/prototypes/particle_flow_baseline.py`;
- `experiments/controlled_dpf_baseline/runners/__init__.py`;
- `experiments/controlled_dpf_baseline/runners/run_smoke.py`;
- `experiments/controlled_dpf_baseline/runners/run_fixed_grid.py`;
- `experiments/controlled_dpf_baseline/runners/validate_results.py`;
- `experiments/controlled_dpf_baseline/reports/README.md`;
- `experiments/controlled_dpf_baseline/reports/outputs/README.md`.

MP5 may further update the existing README placeholders under
`experiments/controlled_dpf_baseline/` only to keep them aligned with this exact
clean-room contract.  `experiments/controlled_dpf_baseline/README.md` and
`experiments/controlled_dpf_baseline/fixtures/README.md` are package-boundary
gates: before MP6 can treat the package as authoritative, they must identify
only the two-fixture clean-room scope and must not advertise broad EDH/LEDH,
OT, AR(2), structural-SSM, stiffness, resampling-stress, HMC, kernel PFF, DPF,
dPFPF, neural-OT, or differentiable-resampling work as current scope.

The fixed MP5 smoke artifacts are:

- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke.json`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke_summary.json`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-smoke-result.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-mp5-clean-room-implementation-result.md`.

MP5 must not create MP6 fixed-grid artifacts.

These are phase-stable canonical paths, not wall-date claims.  A rerun or
repair must either replace them deliberately and record the replacement in the
MP5 result note and reset memo, or stop and create a documented MP5 revision
plan before downstream phases consume alternate filenames.

## Canonical MP5 smoke command

The MP5 implementation must make this command valid from the repository root:

```bash
python -m experiments.controlled_dpf_baseline.runners.run_smoke --fixture range_bearing_gaussian_moderate --seed 31 --num-particles 32 --flow-steps 2 --max-records 1 --max-wall-seconds 30 --records-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke.json --summary-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke_summary.json --report-md experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-smoke-result.md
```

Smoke pass contract:

- exactly one planned record;
- `fixture_name = range_bearing_gaussian_moderate`;
- `seed = 31`;
- `num_particles = 32`;
- `flow_steps = 2`;
- `horizon = 20`;
- runtime at or below `30` wall-clock seconds for the command;
- record status is `ok`;
- required metrics are present and finite;
- summary records `planned_records = 1`, `ok_records = 1`, and
  `fixed_grid_records = 0`.

If the command emits a structured blocker instead of `ok`, MP5 may exit only as
`mp5_ready_with_caveats` when all package, fixture, schema, validation, and
clean-room-boundary checks pass and the blocker is not caused by a lane,
student-import, schema, or full-grid violation.  Otherwise the exit must be
`mp5_needs_revision` or `mp5_blocked_or_excluded`.

## Canonical validation command

MP5 must also make this command valid from the repository root:

```bash
python -m experiments.controlled_dpf_baseline.runners.validate_results --records-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke.json --summary-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke_summary.json --expected-records 1 --require-finite-success-metrics --require-smoke-only
```

The validation helper is the schema and planned-record-count gate that MP6 and
MP7 will reuse.

## Phase cycle

1. Plan: restate the exact files to edit and the smoke checks to run.
2. Execute: implement fixture/schema/metrics/scaffold only.
3. Test: run syntax checks and bounded smoke checks.
4. Audit: inspect for student imports, copied-code risk, production drift, and
   fixture/metric contract drift.
5. Tidy: remove transient artifacts and keep outputs small.
6. Update reset memo: record results, interpretation, and whether MP6 is still
   justified.

## Required checks

- `python -m py_compile` on every Python file under
  `experiments/controlled_dpf_baseline/`;
- a bounded fixture parity or fixture-difference check recorded in the MP5
  result note;
- the canonical MP5 smoke command above;
- the canonical validation command above;
- planned-record guard proving MP5 did not run the full MP6 grid:
  `planned_records = 1` and `fixed_grid_records = 0`;
- output-size check for all smoke artifacts;
- production import-boundary search:

```bash
rg -n "experiments/student_dpf_baselines|advanced_particle_filter|2026MLCOE" bayesfilter tests
```

- clean-room import search over `experiments/controlled_dpf_baseline/`:

```bash
rg -n "experiments/student_dpf_baselines|advanced_particle_filter|2026MLCOE|from src\\.|import src\\." experiments/controlled_dpf_baseline
```

  Expected result: no matches.

- vendored student dirt check:

```bash
git status --short -- experiments/student_dpf_baselines/vendor
```

  Expected result: no dirty vendored student files.

- `git diff --check -- experiments/controlled_dpf_baseline docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md docs/plans/bayesfilter-student-dpf-baseline-mp5-clean-room-implementation-plan-2026-05-13.md`.

## Exit decision

Use one of:

- `mp5_ready_for_fixed_grid_execution`;
- `mp5_ready_with_caveats`;
- `mp5_needs_revision`;
- `mp5_blocked_or_excluded`.

Proceed to MP6 only if the implementation remains clean-room, fixture/metric
checks pass or blockers are structured, and smoke checks are bounded.
