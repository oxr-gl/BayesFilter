# DPF Common Model Suite V2 Production Overnight Gated Execution Plan

metadata_date: 2026-06-07
plan_status: CLAUDE_REVIEWED_LAUNCH_READY

parent_program:

- `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-master-plan-2026-06-07.md`

phase_subplans:

- P0: `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p0-governance-subplan-2026-06-07.md`
- P1: `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p1-declarative-spec-subplan-2026-06-07.md`
- P2: `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p2-density-tieout-subplan-2026-06-07.md`
- P3: `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p3-noresampling-paths-subplan-2026-06-07.md`
- P4: `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p4-fixed-ancestor-paths-subplan-2026-06-07.md`
- P5: `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p5-fixed-branch-gradients-subplan-2026-06-07.md`
- P6: `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p6-retirement-regression-subplan-2026-06-07.md`
- P7: `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p7-terminal-student-planning-subplan-2026-06-07.md`

review_ledgers:

- master/subplan review:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-claude-review-ledger-2026-06-07.md`
- this execution-plan review:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-overnight-gated-execution-claude-review-ledger-2026-06-07.md`

## Purpose

This plan governs an overnight or unattended execution of the reviewed DPF
common model suite v2 production program.  It authorizes Codex to handle
fixable implementation, artifact, and governance blockers with Claude-reviewed
repair loops, while preserving the v2 scientific contract:

```text
Build v2 production common suite -> tie out BayesFilter/FilterFlow values and
gradients -> retire old standalone fixture production path -> only then plan
student repetition by static inventory.
```

The run stops only when the remaining issue requires human judgment, unavailable
infrastructure, forbidden `.localsource/filterflow` mutation, or a scientific
contract change that Codex and Claude cannot resolve within five review rounds.

## Skeptical Plan Audit

Status: `PASS_AS_EXECUTION_POLICY_DRAFT`.

Main drift risks:

- an unattended loop could accidentally execute the old three-row v1 suite and
  call it v2;
- a runner could write old 2026-06-06 artifact names;
- SIR or predator-prey could run through an adapter that is only similar, not
  exactly contract-equal;
- ESS, filtered moments, RMSE, runtime, or finite-difference magnitudes could
  become implicit pass criteria;
- retirement could be misread as deleting every legacy import rather than only
  removing production-v2 dependency on the standalone fixtures;
- student code could be touched before v2 BF/FF closure;
- a repair could relax tolerance, scalar, branch, fixture, model, or
  parameterization after seeing results.

Controls:

- P1 must produce exactly the six declared v2 model ids or fail closed;
- P2--P5 must use new v2 runners and new `dpf_common_model_suite_v2_` artifact
  prefixes only;
- old v1 `common_model_specs()` and old 2026-06-06 artifact names are vetoes in
  v2 execution except explicit v1 validation-only checks in P6;
- P1 must freeze a pre-run row classification table before P2 execution;
- SIR and predator-prey require no-lookup adapter contract certification before
  execution, otherwise they are `CONTRACT_BLOCKED`;
- P2--P5 reports must separate `primary_criterion_fields`,
  `veto_diagnostics`, and `explanatory_only_fields`;
- every phase and repair artifact must record `review_round`,
  `open_material_blockers`, `repair_amendment_required`, and
  `next_allowed_action`;
- P7 is static inventory only and may not run student commands or derive
  student metrics.

No material flaw was found in using this plan as an execution-policy draft.
It still requires Claude review before overnight launch.

## Evidence Contract

Question:

- can Codex execute the reviewed v2 production common-suite program in gated
  overnight form, repairing fixable issues with Claude review and stopping only
  when Codex and Claude cannot proceed without human intervention?

Primary comparator:

- P0--P6: BayesFilter and executable local float64 FilterFlow as peers on the
  same frozen v2 contracts;
- P7: no execution comparator, static student adapter inventory only.

Primary pass criteria:

- P0 records governance and launch conditions.
- P1 produces a v2 manifest with exactly six model ids:
  `lgssm_2d_h25_rich`, `sv_1d_h18_rich`,
  `range_bearing_4d_h20_rich`, `structural_ar1_quadratic_h16`,
  `spatial_sir_j3_rk4`, `predator_prey_rk4`.
- P2 density tie-out passes or classifies every row before execution.
- P3 no-resampling path tie-out passes or classifies every row before
  execution.
- P4 fixed-ancestor path tie-out passes or classifies every row before
  execution.
- P5 fixed-branch gradient tie-out passes or classifies every required knob
  before execution.
- P6 retirement/regression validates v1 and v2 artifacts, records import
  inventory, and removes production-v2 dependency on old standalone fixtures.
- P7 produces static student repetition planning only, with zero student
  commands and zero derived student metrics.

Veto diagnostics:

- old three-row `common_model_specs()` used as v2 execution source;
- any v2 runner writes old `dpf_common_*_2026-06-06.json` names;
- v2 manifest row-count/model-id gate fails;
- missing pre-run row classification table;
- unclassified mismatch;
- nonfinite scalar, density, path ledger, or gradient in an executed row;
- SIR/predator-prey adapter equality cannot be certified before execution;
- primary/veto/explanatory report fields are not separated;
- v1 validation commands rebind to changed v1 semantics or checksums;
- tolerance, fixture, model, scalar objective, branch semantics, comparator, or
  parameterization changes after seeing results without reviewed amendment;
- any `.localsource/filterflow` mutation need;
- any student filter, density, path, gradient, validation, or derived-metric
  command before a separate reviewed student execution plan;
- treating BayesFilter, FilterFlow, students, TT, dense quadrature, simulated
  truth, or paper tables as an oracle;
- exhausting five Claude review iterations with a material blocker still open.

Explanatory diagnostics:

- ESS, filtered mean/variance, RMSE, runtime, finite-difference magnitudes,
  source inventory, interface notes, legacy artifact validation, and
  nonproduction import inventory.

What will not be concluded:

- no filter correctness proof;
- no proof that BayesFilter or FilterFlow is correct;
- no TT/SIRT correctness or adaptive MATLAB equivalence claim;
- no paper-scale Zhao--Cui reproduction claim;
- no stochastic-resampling distribution correctness claim;
- no student implementation match, mismatch, correctness, or failure claim;
- no HMC, DSGE, GPU, scalability, or deployment-readiness claim.

Artifacts preserving the result:

- this execution plan;
- one phase result ledger per executed phase;
- one Claude review ledger per phase or repair cycle;
- v2 JSON output manifests and markdown reports;
- v2 manifest and row-classification artifact;
- P6 retirement/import inventory manifest;
- final overnight execution closeout ledger.

## Launch Preconditions

The overnight launcher may start only after:

- this execution plan passes Claude review to `PASS`;
- the master/subplan review ledger is closed at PASS:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-claude-review-ledger-2026-06-07.md`;
- P0--P7 subplans are marked reviewed-ready;
- local `git diff --check` passes for governing plan files and any files edited
  before launch;
- the executor records current git commit or dirty-worktree status;
- the executor records CPU-only intent for TensorFlow runs:
  `CUDA_VISIBLE_DEVICES=-1` before any TensorFlow import;
- no `.localsource/filterflow` mutation is needed for launch;
- the executor acknowledges the artifact-adequacy phase-pass gate below:
  no phase may be marked `PHASE_PASS_OR_CLASSIFIED` unless the reviewed
  subplan's required artifact bundle exists and contains the mandated
  top-level sections/fields.

## Standing Permissions And Prohibitions

Allowed without further human approval during this execution:

- write/edit files under `/home/chakwong/BayesFilter` and `/tmp` within the
  reviewed file scopes;
- create v2 runners, tests, manifests, reports, ledgers, and repair amendments;
- run CPU-only TensorFlow commands with `CUDA_VISIBLE_DEVICES=-1`;
- run Claude review commands with escalated/trusted permissions according to
  the cross-agent policy;
- run validation and test commands required by reviewed phase plans.

Prohibited without specific new human approval:

- mutate `.localsource/filterflow`;
- weaken tolerances, pass/fail criteria, fixtures, scalar definitions, branch
  semantics, model equations, comparator definitions, or physical
  parameterizations after seeing results;
- run any student implementation command in P0--P7;
- use network or install dependencies unless a reviewed repair plan states that
  infrastructure is required and the user grants approval;
- write outside `/home/chakwong/BayesFilter` or `/tmp`;
- run GPU/CUDA jobs unless a reviewed repair or phase amendment requires GPU
  and the user grants explicit GPU approval.

## Execution State Machine

Each phase runs through:

```text
PHASE_READY
  -> PLAN_AND_PRIOR_ARTIFACTS_LOADED
  -> SKEPTICAL_PHASE_AUDIT
  -> CLAUDE_PHASE_PLAN_REVIEW_IF_NEEDED
  -> LOCAL_EVIDENCE_RUN
  -> EVIDENCE_AUDITED
  -> RESULT_LEDGER_WRITTEN
  -> ARTIFACT_ADEQUACY_CHECKED
  -> CLAUDE_RESULT_REVIEWED
  -> PHASE_PASS_OR_CLASSIFIED
```

Failure transition:

```text
LOCAL_EVIDENCE_RUN or EVIDENCE_AUDITED or CLAUDE_RESULT_REVIEWED
  -> BLOCKER_CLASSIFIED
  -> REPAIR_PLAN_OR_AMENDMENT_WRITTEN
  -> CLAUDE_REPAIR_REVIEWED
  -> REPAIR_IMPLEMENTED
  -> LOCAL_EVIDENCE_RUN
```

Stop transitions:

```text
BLOCKER_CLASSIFIED
  -> HUMAN_INTERVENTION_REQUIRED

CLAUDE_REPAIR_REVIEWED
  -> STOP_MAX_REVIEW_ROUNDS

EVIDENCE_AUDITED
  -> STOP_FAILED_VETO_UNFIXABLE

ARTIFACT_ADEQUACY_CHECKED
  -> STOP_MISSING_REQUIRED_ARTIFACT_BUNDLE
```

## Phase Order

Required order:

```text
P0 -> P1 -> P2 -> P3 -> P4 -> P5 -> P6 -> P7
```

P7 is blocked until P0--P6 all have reviewed result ledgers.

## Blocker Classification

Every failure must be classified before repair.

### Fixable By Codex And Claude

These issues may be repaired autonomously after a reviewed repair plan or
phase-plan amendment:

- coding bug with unchanged mathematical model, scalar objective, branch,
  comparator, tolerance, and parameterization;
- missing manifest field, checksum, dtype record, seed, command record,
  CPU-only record, report section, or result-ledger entry;
- incorrect import, shape, dtype, batching, seed, path, or CPU-only setup;
- missing validation command for a runner already named by the phase plan;
- old v1 API leakage into v2 when the correct v2 declarative source is clear;
- old artifact-name leakage when replacing it with the predeclared v2 artifact
  name;
- SIR/predator-prey adapter certification gap that can be resolved by static
  contract recording without changing equations;
- missing pre-run row classification when classification can be made from
  already-declared interfaces before evidence execution;
- documentation overclaim that can be removed or downgraded;
- report-field mixing that can be repaired by restructuring the artifact
  without changing results;
- classification gap that can be resolved as `INTERFACE_BLOCKED`,
  `CONTRACT_BLOCKED`, `SCIENTIFIC_CONTRACT_BLOCKED`, or
  `EXPLAINED_MISMATCH` without changing evidence;
- tolerance-enforcement bug where the intended tolerance was already declared
  in the reviewed phase plan.

### Requires Human Intervention

The execution must stop for:

- relaxing a primary tolerance or pass/fail criterion after seeing results;
- choosing a new scientific comparator or baseline;
- accepting a failed veto as acceptable;
- changing model equations, scalar objectives, branch semantics, or parameter
  meanings in a nontrivial way;
- mutating `.localsource/filterflow`;
- using student output to revise BayesFilter/FilterFlow fixtures;
- starting student execution before a separate reviewed student execution plan;
- accepting weaker evidence for a stronger claim;
- infrastructure failure that blocks required execution and has no reviewed
  CPU-only fallback;
- unresolved Codex/Claude disagreement after five review rounds.

### Must Be Recorded As Negative Or Boundary Evidence

These cannot be hidden:

- interface gap;
- resource timeout;
- nonfinite diagnostic;
- unstable finite-difference window;
- fixed-branch mismatch;
- exact-reference mismatch;
- adapter-certification failure;
- row or knob classified blocked before execution.

The result ledger must separate implementation failure, interface limitation,
contract blocker, diagnostic failure, and evidence against an attempted common
fixture.

## Artifact-Adequacy Phase-Pass Gate

A phase may not be marked `PHASE_PASS_OR_CLASSIFIED` unless the reviewed
subplan's required artifact bundle exists and is complete.

For each phase, the executor must check:

- the phase result ledger under `docs/plans/` exists;
- every JSON artifact required by the reviewed subplan exists under
  `experiments/dpf_implementation/reports/outputs/`, when applicable;
- every markdown report required by the reviewed subplan exists under
  `experiments/dpf_implementation/reports/`, when applicable;
- required manifest, row-classification, checksum, import-inventory, or static
  student-inventory artifacts exist when the phase declares them;
- required top-level sections/fields are present, including
  `primary_criterion_fields`, `veto_diagnostics`,
  `explanatory_only_fields`, `review_round`, `open_material_blockers`,
  `repair_amendment_required`, and `next_allowed_action` whenever the subplan
  requires them;
- the result ledger records command manifest, CPU/GPU status, non-claims,
  decision table, repair history, and post-run red-team note when required by
  this execution plan.

Console PASS, pytest PASS, or a successful runner exit code is insufficient
without the reviewed artifact bundle.  Missing or incomplete required artifacts
are a material blocker.  If the missing artifact can be generated without
changing evidence, it is fixable by Codex and Claude through the repair loop.
If artifact generation would require changing the scientific contract, the run
stops for human intervention.

## Repair Loop Rules

For each fixable blocker:

1. Record the failed command, observed evidence, and blocker classification in
   the phase result or review ledger.
2. Write a repair plan or phase-plan amendment with:
   - failure evidence;
   - proposed repair;
   - unchanged contract fields checked against the prior phase ledger,
     manifest, or reviewed subplan;
   - changed contract fields, if any;
   - fresh evidence required after repair;
   - non-claims.
3. If the proposed repair changes tolerance, fixture, comparator, scalar
   objective, model declaration, physical parameterization, branch semantics, or
   the BF/FF equality contract, stop and require human intervention unless the
   user explicitly approves a new scientific-contract plan.
4. If the proposed repair needs `.localsource/filterflow` mutation, stop for
   human intervention.
5. Run Claude repair-plan review until `PASS` or five rounds.
6. Implement only the reviewed repair.
7. Rerun the failed focused command and the phase validation command.
8. Run `git diff --check` for changed files.
9. Update the result ledger with failed attempt, repair, rerun result, and
   decision.
10. Run Claude result/code/governance review until `PASS` or five rounds.

If Claude identifies a material blocker, patch and loop.  If Codex disputes the
finding, ask Claude once more with the relevant source and artifact evidence.
A persistent dispute after five rounds stops the run.

## Standard Claude Commands

Claude commands require trusted or escalated execution.

Preferred command shape:

```bash
claude -p "<bounded phase/review prompt>"
```

or, if wrapper-based review is desired:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name dpf-v2-<phase>-<review-kind>-iter<N> \
  "<bounded review prompt>"
```

Prompts must ask for material blockers first and explicitly check:

- v1/v2 isolation and six-row manifest gate;
- no old 2026-06-06 v2 artifact writes;
- no old three-row API use as v2 source;
- pre-run row/knob classification;
- SIR/predator-prey no-lookup adapter certification;
- primary/veto/explanatory separation;
- no `.localsource/filterflow` mutation;
- no student execution or derived student metrics;
- no oracle language or overclaim.

## Standard Local Commands

Every phase begins with local hygiene:

```bash
git diff --check
```

CPU-only TensorFlow commands must hide GPU devices before import:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m <phase_runner>
CUDA_VISIBLE_DEVICES=-1 python -m <phase_runner> --validate-only
```

Planned v2 runner names:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_density_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_noresampling_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_fixed_resampling_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_gradients_tf
```

P0/P1/P6/P7 may create manifest/validation runners as reviewed by their phase
subplans.  P6 may run v1 validation-only commands, but only to validate original
v1 artifact schemas and checksums.

GPU commands are not part of this execution plan by default.

## Required Result Ledger Template

Every executed phase result ledger must include:

```text
metadata_date:
phase:
decision:

question:
comparator:
primary_pass_criterion:
veto_diagnostics:
explanatory_diagnostics:
non_claims:

command_manifest:
- git_commit_or_dirty_status:
- command:
- environment:
- CPU/GPU status:
- random seeds:
- dtype:
- fixture or contract manifest:
- output artifacts:

primary_criterion_fields:
veto_diagnostics_result:
explanatory_only_fields:

review_round:
open_material_blockers:
repair_amendment_required:
next_allowed_action:

result_summary:
- matched cells:
- explained mismatches:
- interface blockers:
- contract blockers:
- scientific contract blockers:
- unclassified mismatches:

repair_history:
- failed attempt:
- blocker classification:
- reviewed repair:
- rerun evidence:

decision_table:
| Decision | Primary criterion | Veto status | Main uncertainty | Next action | Not concluded |
|---|---|---|---|---|---|

post_run_red_team:
- strongest alternative explanation:
- result that would overturn the decision:
- weakest evidence link:
```

## Terminal Student Boundary

P7 cannot start until:

- P0--P6 result ledgers are reviewed and closed;
- no BayesFilter/FilterFlow executed mismatch is unclassified;
- every blocked surface has a concrete reason;
- v2 manifest and P6 retirement/import inventory exist.

In P7:

- evidence boundary is `static_inventory_only`;
- `student_filter_commands_run = 0`;
- `student_density_commands_run = 0`;
- `student_path_commands_run = 0`;
- `student_gradient_commands_run = 0`;
- no student validation or derived-metric command may run;
- student implementations are not oracles;
- student planning must not retroactively define the BayesFilter/FilterFlow
  comparator.

## Final Closeout

The overnight execution closes with:

- final result:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-overnight-gated-execution-result-2026-06-07.md`
- final Claude review ledger update;
- list of phases passed, classified, blocked, or stopped for human
  intervention;
- list of artifacts produced;
- list of non-claims preserved.

The run is successful only if it makes reviewed progress without weakening the
v2 evidence contract.  A clean `STOP_FOR_HUMAN` is a valid outcome when the
remaining issue exceeds Codex and Claude authority.
