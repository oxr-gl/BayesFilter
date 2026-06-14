# Audit: student DPF master program and final subplans

## Date

2026-05-13, reviewed again 2026-05-14 and 2026-05-15

## Scope

This audit reviews the student DPF experimental-baseline master program and the
remaining subplans from clean-room implementation through final closeout.

Reviewed documents:

- `docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-clean-room-controlled-baseline-spec-2026-05-13.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-clean-room-controlled-baseline-spec-result-2026-05-13.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-mp5-clean-room-implementation-plan-2026-05-13.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-mp6-clean-room-fixed-grid-execution-plan-2026-05-13.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-mp7-clean-room-comparison-audit-plan-2026-05-13.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-mp8-final-archive-and-closeout-plan-2026-05-13.md`.

This audit does not authorize execution.  It checks consistency and gap
coverage only.

## Audit result

Decision: `program_and_subplans_consistent_for_mp5_start`.

Blocking findings: none.

Readiness clarification from the 2026-05-15 Codex/Claude supervisor review:
the 2026-05-13 audit decision meant planning consistency, not unattended
execution readiness.  Before the 2026-05-15 tightening, MP5-MP8 did not pin
enough exact runner paths, command lines, artifact filenames, blocker schemas,
or comparison-input paths.  Those gaps are now treated as resolved at the plan
level, but the actual implementation remains unproven until MP5 runs.

Final bounded Claude acceptance check on 2026-05-15 returned `ACCEPT` after the
third tightening pass.  Codex independently verified the same plan-level
readiness with path-scoped diff and whitespace checks.

Second-review tightening applied on 2026-05-14:

- master MP5 was renamed from broad controlled-baseline extraction to a concrete
  clean-room implementation scaffold phase;
- MP5 now specifies the first clean-room algorithm shape as a regularized
  particle-flow/bootstrap-particle hybrid with explicit flow-step control;
- MP5 now lists required implementation files, smoke-only scope, artifact gates,
  and vendored-dirt checks;
- MP6 now states the exact planned record count, required record schema,
  required finite metrics, runtime gates, and artifact-size gates;
- MP7 now defines a qualitative comparison rubric and default coarse 2.0x proxy
  regime threshold for position RMSE and observation proxy RMSE;
- MP8 now defines required closeout sections and final verification checks.

Third-review tightening applied on 2026-05-15:

- MP5 now states that `experiments/controlled_dpf_baseline/` is currently README
  scaffolding and that MP6-MP8 are non-executable until MP5 creates exact
  package, runner, validation, and artifact surfaces;
- MP5 now pins required files, canonical smoke command, canonical validation
  command, smoke pass contract, and fixed smoke artifact names;
- MP6 now pins the canonical fixed-grid command, canonical validation command,
  exact fixed-grid artifact names, allowed status values, and allowed blocker
  taxonomy;
- MP7 now pins the frozen student aggregate Markdown/JSON inputs, frozen MP6
  inputs, deterministic comparison edge-case rules, exact comparison artifact
  names, and the `mixed_proxy_regime` caveat path;
- MP8 now includes an exact artifact checklist and hard-stop rule for missing
  MP5-MP7 outputs;
- MP5-MP8 now use phase-stable canonical artifact paths rather than wall-date
  filenames; reruns require an explicit replacement record or revision plan;
- MP7 now compares each clean-room cell separately against each frozen student
  implementation aggregate and then derives a final class by deterministic
  aggregation rules;
- MP7 required JSON outputs now preserve per-student classes, denominators, the
  final class, and the aggregation rule for each clean-room cell;
- the master program now states the same per-student-then-aggregate MP7
  comparison protocol as the MP7 subplan;
- the controlled-baseline README placeholders now state the two-fixture
  clean-room scope and prohibit broad fixture/prototype drift;
- the master program now distinguishes plan consistency from implementation
  readiness and carries the exact-command dependency across MP5-MP8.

Remaining nonblocking notes:

- MP5 should receive a separate phase-specific audit immediately before
  execution, as required by the normal plan-execute-test-audit-tidy-reset cycle.
- MP5 should not run the full fixed grid; that belongs to MP6.
- MP7 should not mutate MP6 outputs except through a documented revision path.
- MP8 should close the program, not silently authorize new experiments.
- `experiments/controlled_dpf_baseline/README.md` and
  `experiments/controlled_dpf_baseline/fixtures/README.md` must remain aligned
  with the two-fixture clean-room contract before MP6 treats the package as
  authoritative.

## Phase coverage

| Phase | Status | Subplan | Coverage |
| --- | --- | --- | --- |
| MP0 governance | Completed | master/reset records | Lane separation and governance established. |
| MP1 MLCOE particle adapter gate | Completed | existing MP1 plan/audit | Closed particle diagnostic asymmetry. |
| MP2 nonlinear reference/proxy spine | Completed | existing MP2 plan/audit | Closed immediate nonlinear proxy-metric gap. |
| MP3 kernel PFF debug gate | Completed with exclusion | existing MP3 plan/audit | Kernel PFF excluded from routine panels pending later debug. |
| MP4 flow/DPF readiness review | Completed | existing MP4 plan/audit | Selected bounded EDH/PFPF comparison path. |
| EDH/PFPF adapter and panels | Completed | adapter spike, replicated, sensitivity, confirmation plans | Produced confirmed student aggregate evidence with caveats. |
| Clean-room specification | Completed | clean-room spec plan/audit/result | Fixed fixture, metric, target, caveat, and gate contracts. |
| MP5 clean-room scaffold | Planned | MP5 plan | Fixture/schema/metric/scaffold implementation and smoke checks before full-grid execution. |
| MP6 fixed-grid execution | Planned | MP6 plan | Runs exactly 15 fixed-grid records for one clean-room controlled algorithm. |
| MP7 comparison audit | Planned | MP7 plan | Compares clean-room results to student aggregates with a proxy-only qualitative rubric. |
| MP8 final archive | Planned | MP8 plan | Defines final finish line, claim ledger, artifact index, and closeout labels. |

## Consistency checks

### Lane boundary

Result: pass.

MP5-MP8 keep work under `experiments/controlled_dpf_baseline/`, existing
student-baseline reports, and student-baseline docs.  Production `bayesfilter/`,
monograph files, `docs/references.bib`, and vendored student files remain out of
scope.

### Clean-room boundary

Result: pass.

The subplans prohibit importing student vendor snapshots, calling student
adapters from the clean-room algorithm, copying student implementation code, and
editing vendored student snapshots.

The first clean-room controlled target is now concrete enough to execute: a
small regularized particle-flow/bootstrap-particle hybrid using fixture
transition proposals, Gaussian range-bearing likelihoods, EKF-style innovation
flow over explicit flow steps, and a locally implemented resampler.

### Phase ordering

Result: pass.

The ordering is explicit:

1. MP5 implementation scaffold;
2. MP6 fixed-grid execution;
3. MP7 comparison audit;
4. MP8 archive and closeout.

Each phase has exit labels that gate the next phase.

MP5 is explicitly smoke-only and cannot run the full fixed grid.  MP6 is the
first full-grid phase.  MP7 is interpretation-only and cannot silently mutate
MP6 outputs.  MP8 closes the stream and cannot authorize new experiments.

### Finish line

Result: pass.

MP8 defines a concrete program finish line: final archive, artifact index, claim
ledger, prohibited uses, complete or complete-with-caveats status, and no
ambiguous active phase.

### Hypothesis coverage

Result: pass.

The clean-room result hypotheses I1-I4 are mapped:

- I1 fixture generation parity: MP5;
- I2 minimal flow-assisted baseline fixed grid: MP5 scaffold and MP6 execution;
- I3 comparison to student aggregates: MP7;
- I4 clean-room gates: MP5-MP8 audit checks.

### Moderate-noise caveat

Result: pass.

MP6 requires both moderate N128/steps10 and N128/steps20.  MP7 prevents a
universal winner claim before comparison audit.

### No broad grid expansion

Result: pass.

MP6 fixes the grid and lists the allowed fixture/particle/flow-step/seed cells:
three cells times five seeds, for 15 planned records.  Any broader experiment
would need a separate plan.

### Comparison thresholds

Result: pass.

MP7 now has a default qualitative threshold: 2.0x on median position RMSE and
observation proxy RMSE for proxy-regime classification, with ESS/resampling and
runtime kept as diagnostic context.

### Reset memo continuity

Result: pass.

The reset memo now points to MP5 as the active next phase.  Later phases must
update the reset memo after each cycle.

## Remaining risks

- The clean-room algorithm itself remains unspecified until MP5 execution.  This
  is expected and should be resolved in MP5, not in the master audit.
- Fixture reproduction may depend on NumPy random behavior.  MP5 includes an
  exact-match or documented-difference gate.
- Full-grid runtime is unknown until MP6.  MP6 includes runtime-warning and
  structured-blocker requirements.
- Final usefulness depends on whether MP6 outputs are interpretable.  MP7 and
  MP8 provide stop/revision paths.

## Recommendation

Proceed next with MP5 only.  Before execution, run a focused MP5 audit against
the tightened required implementation shape and file list, then follow the
cycle: plan, execute, test, audit, tidy, update reset memo, and path-scoped
commit if requested.
