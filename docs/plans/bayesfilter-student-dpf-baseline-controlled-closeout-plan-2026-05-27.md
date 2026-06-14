# Plan: student DPF controlled-baseline closeout

## Date

2026-05-27

## Scope

This is a narrow closeout plan for the quarantined student differentiable
particle filter / student DPF experimental-baseline lane.

Owned surfaces for this plan:

- `docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md`;
- student-lane closeout plan, audit, result, and review notes under
  `docs/plans/`;
- `experiments/controlled_dpf_baseline/README.md`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-final-archive-result.md`.

Out of scope:

- production `bayesfilter/` code;
- monograph chapter files and references;
- vendored student snapshots;
- new broad experiments, sweeps, training, HMC, neural OT, kernel PFF, dPFPF, or
  production-readiness runs.

## Evidence contract

Question:

Can the student DPF lane be brought to a clean closeout state using existing
MP5--MP7 controlled-baseline artifacts?

Baseline/comparator:

- Current reset memo and master-program continuity state;
- existing MP5 smoke, MP6 fixed-grid, MP7 comparison-audit artifacts;
- future-work usability gates.

Primary pass criterion:

- continuity documents and controlled-baseline README/report accurately record
  that MP5 smoke, MP6 fixed-grid, and MP7 proxy comparison are complete and that
  the lane is closed as a quarantined experimental baseline archive.

Veto diagnostics:

- any required edit touches production `bayesfilter/`, monograph chapters,
  references, or vendored student code;
- evidence for MP5--MP7 is missing or inconsistent;
- the closeout would promote proxy metrics into correctness, production,
  monograph, HMC, or model-risk claims;
- the missing MP5 implementation-plan reference cannot be resolved without
  inventing nonexistent evidence.

Explanatory diagnostics only:

- exact RMSE/runtime values in MP5--MP7;
- qualitative same-regime labels in MP7;
- future-work family decisions.

What this plan will not conclude:

- no production BayesFilter correctness or readiness;
- no monograph evidence without separate review;
- no HMC, DPF-HMC, neural OT, dPFPF, kernel PFF, or differentiable-resampling
  validation;
- no claim that student agreement certifies correctness.

Preserved artifact:

- final closeout result and review/audit notes under `docs/plans/`;
- final archive report under `experiments/controlled_dpf_baseline/reports/`.

## Skeptical pre-execution audit checklist

The separate audit note must check:

- stale context: reset memo/master versus MP5--MP7 artifacts;
- wrong baseline: final status compared against the actual controlled baseline,
  not student code alone;
- proxy-metric overclaim: MP7 same-regime labels stay proxy-only;
- missing stop conditions: stop on production, monograph, vendor, or evidence
  gaps;
- unfair comparison: no student agreement as correctness;
- environment mismatch: no new runtime evidence claimed;
- artifact sufficiency: every closeout claim points to an existing result;
- README authority mismatch: missing MP5 plan reference is resolved by replacing
  it with existing authoritative artifacts, not by fabricating a plan.

## Execution steps

1. Create and pass a skeptical audit before continuity edits.
2. Update the reset memo header and append a controlled-baseline closeout log.
3. Update the master-program current-next-move section so it records final
   archive status rather than implementation-plan handoff.
4. Update the controlled-baseline README authority list to cite existing
   specification and MP5--MP7 result artifacts, removing the missing MP5 plan
   reference.
5. Add a final archive report under
   `experiments/controlled_dpf_baseline/reports/`.
6. Add a result note and post-execution review/audit under `docs/plans/`.
7. Run verification:
   - import-boundary search over `bayesfilter` and `tests`;
   - `git diff --check`;
   - `git status --short --branch`;
   - `py_compile` only if Python files are edited.

## Stop rules

Stop and ask for direction if:

- MP5--MP7 artifacts are missing or contradict their stated decisions;
- the README reference cannot be fixed without inventing an artifact;
- any required edit leaves the student DPF lane;
- generated outputs or broad experiments become necessary;
- verification reveals production/test imports of student-baseline code.
