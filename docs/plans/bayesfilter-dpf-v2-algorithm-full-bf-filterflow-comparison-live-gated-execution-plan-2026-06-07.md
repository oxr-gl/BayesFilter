# DPF V2 Algorithm Full BF/FilterFlow Live Gated Execution Plan

metadata_date: 2026-06-07
plan_status: SUPERSEDED_BY_VISIBLE_GATED_EXECUTION_RUNBOOK

superseded_by:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-visible-gated-execution-runbook-2026-06-08.md`

## Supersession Note

This live/detached execution plan is no longer the active route for the DPF V2
algorithm full BF/FilterFlow comparison. On 2026-06-08 the user clarified that
the intended execution is a visible gated runbook run inside the current
dialogue, with Codex as the in-dialogue supervisor/executor and Claude as a
read-only reviewer.

Do not use this plan to launch `codex exec`, the live supervisor scripts,
`setsid`, `nohup`, detached `tmux`, background phase runners, or copied
workspaces for this task. This file remains a historical record only.

parent_program:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-master-program-2026-06-07.md`

reviewed_master_ledger:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-claude-review-ledger-2026-06-07.md`

live_execution_review_ledger:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-live-gated-execution-claude-review-ledger-2026-06-07.md`

human_risk_acceptance_amendment:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-live-gated-execution-human-risk-acceptance-amendment-2026-06-08.md`

## Purpose

Run the reviewed DPF V2 full algorithm BayesFilter/FilterFlow comparison from
P0 through P8 from the live workspace, with Codex as supervisor and Claude as a
critical read-only reviewer. The live shell supervisor launches bounded Codex
phase workers for execution/repair and then launches Claude separately through
a read-only reviewer wrapper; nested Codex workers do not launch Claude.

This plan intentionally does not use a copied isolated workspace. The reason is
recoverability: phase artifacts, repair amendments, logs, and result ledgers
should be immediately visible in `/home/chakwong/BayesFilter` so a later agent
can resume from the latest gated phase without discovering hidden `/tmp`
workspace state.

The plan borrows the useful pattern from
`/home/chakwong/python/claudecodex/scripts/overnight_gated_launch.sh` and the
P44 gated run:

- phase-by-phase execution;
- explicit run id and logs;
- dirty-worktree manifests before launch;
- machine-checkable pass tokens;
- Claude review loops with a five-iteration cap;
- stop on unreviewed repair, contract weakening, missing artifacts, or reviewer
  blocker.

It deliberately omits the copied-root mount namespace and replaces that safety
control with live-workspace write allowlists, protected dirty tracked files,
and exact artifact gates.

## Scope

Required phases:

| Phase | Required pass token |
|---|---|
| P0 | `PASS_P0_READY_FOR_P1` |
| P1 | `PASS_P1_ARCHITECTURE_READY_FOR_P2` |
| P2 | `PASS_P2_BOOTSTRAP_OT_CONTRACTS_READY_FOR_P3` |
| P3 | `PASS_P3_BOOTSTRAP_OT_VALUES_READY_FOR_P4` |
| P4 | `PASS_P4_BOOTSTRAP_OT_GRADIENTS_READY_FOR_P5` |
| P5 | `PASS_P5_LEDH_PFPF_OT_CONTRACTS_READY_FOR_P6` |
| P6 | `PASS_P6_LEDH_PFPF_OT_VALUES_READY_FOR_P7` |
| P7 | `PASS_P7_LEDH_PFPF_OT_GRADIENTS_READY_FOR_P8` |
| P8 | `PASS_FULL_COMPARISON` or `BLOCKED_WITH_REVIEWED_CLASSIFICATION` |

Required V2 rows, in order:

1. `lgssm_2d_h25_rich`
2. `sv_1d_h18_rich`
3. `range_bearing_4d_h20_rich`
4. `structural_ar1_quadratic_h16`
5. `spatial_sir_j3_rk4`
6. `predator_prey_rk4`

## Evidence Contract

Question:

- Can Codex execute the reviewed DPF V2 full algorithm comparison in the live
  workspace, repairing only reviewed fixable blockers, while Claude provides
  read-only critical review at every phase gate?

Baseline or comparator:

- BayesFilter and BayesFilter-owned FilterFlow-side adapters execute the same
  frozen JSON contracts. Neither side is an oracle.

Primary promotion criteria:

- P0 confirms governance, artifacts, no-oracle policy, `.localsource/filterflow`
  no-mutation policy, CPU-only TensorFlow policy, and all phase files.
- P1 freezes the BF/FF adapter architecture for both algorithms and all six V2
  rows.
- P2 freezes bootstrap-OT contracts for all six rows before P3 or P4 evidence.
- P3 matches bootstrap-OT values and ledgers for all six rows.
- P4 matches bootstrap-OT fixed-branch AD gradients for all required physical
  knobs.
- P5 freezes LEDH-PFPF-OT contracts for all six rows before P6 or P7 evidence.
- P6 matches LEDH-PFPF-OT values and ledgers for all six rows.
- P7 matches LEDH-PFPF-OT fixed-branch AD gradients for all required physical
  knobs.
- P8 closes only as `PASS_FULL_COMPARISON` when every required row and gradient
  knob passes, otherwise only as `BLOCKED_WITH_REVIEWED_CLASSIFICATION` with
  reviewer-approved blocker classification.

Veto diagnostics:

- mutation of `.localsource/filterflow`;
- modifying protected pre-existing dirty tracked files;
- running student implementation commands or deriving student metrics;
- treating BayesFilter, FilterFlow, students, TT, dense quadrature, paper
  tables, or simulated truth as an oracle;
- using old closed V2 deterministic evidence as a substitute for this algorithm
  comparison;
- changing fixtures, tolerances, scalar definitions, branch masks, OT settings,
  gradient knobs, or model semantics after seeing results without reviewed
  amendment;
- finite differences used as a gradient promotion gate;
- missing phase artifact, missing run manifest, missing checksum, missing row,
  or full-comparison success with an unexecuted row or gradient knob;
- nonfinite value, density, transport matrix, PF-PF correction, Jacobian/logdet,
  or AD gradient;
- Claude reviewer returns a material blocker that is not repaired through a
  reviewed amendment;
- five review iterations are exhausted without explicit PASS.

Explanatory-only diagnostics:

- ESS, filtered moments, RMSE to simulated or reference paths, runtime, FD
  ladders, FD pass/fail booleans, seed robustness, local linearization
  residuals, transport residuals, and stochastic smoke summaries.

What will not be concluded:

- no BayesFilter correctness proof;
- no FilterFlow correctness proof;
- no proof that bootstrap-OT or LEDH-PFPF-OT is scientifically correct;
- no stochastic resampling distribution correctness claim;
- no gradients through random seeds, random sampling, Boolean trigger decisions,
  or random/discrete ancestor selection;
- no student implementation claim;
- no TT/SIRT, paper-table, HMC, DSGE, GPU, scalability, deployment, or
  production-readiness claim.

Artifacts preserving the result:

- this execution plan and Claude plan-review ledger;
- one live run directory under `docs/plans/logs/<run_id>/`;
- prelaunch dirty tracked and full git status manifests;
- one prompt, output log, and command manifest per phase;
- P0--P8 result ledgers under `docs/plans/`;
- phase JSON and markdown reports under `experiments/dpf_implementation/reports`;
- phase Claude read-only review ledgers under `docs/plans/`;
- final live execution closeout result under `docs/plans/`.

## Skeptical Plan Audit

Status: `PASS_AS_LIVE_EXECUTION_POLICY_DRAFT`.

Wrong-baseline risk:

- The live run could accidentally use the closed deterministic BF/FilterFlow
  tie-out as evidence for this algorithm comparison. Control: phase prompts and
  gates require the new algorithm-specific P0--P8 artifacts and pass tokens.

Proxy-metric risk:

- ESS, RMSE, runtime, FD diagnostics, and stochastic smoke results could be
  promoted into pass criteria. Control: they remain explanatory-only in the
  evidence contract and reviewer prompt.

Missing stop-condition risk:

- In-place execution can keep editing through a real blocker. Control: stop on
  `.localsource/filterflow` mutation need, contract weakening, unclassified
  mismatch, missing row, unrepaired Claude blocker, or max-five review
  exhaustion.

FilterFlow mutation risk:

- A phase could mutate `.localsource/filterflow` and restore it before a simple
  status check. Control: each Codex phase worker runs in a mount namespace where
  `.localsource/filterflow` is bind-remounted read-only, and the supervisor also
  compares the recorded FilterFlow HEAD, status, and file checksums after each
  phase.

Unfair comparison risk:

- BF and FF adapters could consume different branch masks, noise, scalar, or
  OT settings. Control: P2 and P5 freeze shared contract bytes and later phases
  must verify runtime branch masks and checksums against those contracts.

Hidden assumption risk:

- Local FilterFlow does not appear to provide native LEDH proposal support.
  Control: P1/P5 must classify LEDH as BayesFilter-owned FilterFlow-side
  adapter work and must not mutate `.localsource/filterflow`.

Stale context risk:

- The source workspace is dirty and contains many unrelated untracked DPF and
  high-dimensional artifacts. Control: prelaunch dirty tracked files are
  protected, staging is out of scope, and writes are limited to the lane's
  docs/plans, experiments/dpf_implementation, scripts support, and logs.

Environment mismatch risk:

- Non-escalated GPU probes can mislead, and GPU is not needed here. Control:
  TensorFlow commands must be CPU-only with `CUDA_VISIBLE_DEVICES=-1` before
  import. No GPU command is authorized by this plan.

Artifact adequacy risk:

- Console output alone would not answer the question. Control: every phase must
  write JSON, markdown, result ledger, review ledger, and command logs with a
  run manifest.

Audit decision:

- No material flaw was found in launching from the live workspace after Claude
  reviews this execution plan. The live approach is less isolated than the
  copied-workspace launcher but more recoverable, and the added path/dirty-file
  controls answer the main live-execution risks.

## Launch Preconditions

Launch may begin only after:

- this execution plan receives Claude read-only review PASS;
- `git diff --check` passes for this plan and the launcher/gate scripts;
- `.localsource/filterflow` is clean before launch and remains at the recorded
  commit and checksum after each phase;
- all P0--P8 subplans exist;
- the reviewed master/subplan ledger is `CLOSED_PASS_ROUND_1`;
- prelaunch `git status --short`, `git diff --name-only`, and
  `.localsource/filterflow` commit/status are recorded;
- pre-existing untracked file checksums are recorded and must remain unchanged
  unless the path is inside the live execution write allowlist;
- ignored file checksums are recorded and newly created ignored files must be
  inside the live execution write allowlist;
- the launcher records the current root commit:
  `137f6ba5a03ebab199c8ab4699354d50bd560123`;
- the launcher records `.localsource/filterflow` commit:
  `1e5fbc288c1c11fc18ba01bb4842832e2088b800`;
- Claude review is invoked read-only, with no edit/write tools and no shell
  commands that mutate files.

Protected pre-existing dirty tracked files at draft time:

- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md`
- `docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md`
- `docs/references.bib`
- `experiments/controlled_dpf_baseline/README.md`
- `experiments/student_dpf_baselines/reports/outputs/student_baseline_panel_2026-05-10.json`

The launch script must regenerate this list immediately before launch and fail
if a phase changes any protected tracked file.

Pre-existing untracked regular files are also protected by default. Pre-existing
untracked directory paths do not grant directory-wide write permission: the
launcher expands them to regular-file checksums, and the supervisor must fail
if a new or changed file appears under such a directory unless the file path is
inside the allowed write scope.

Ignored files are treated the same way. The launcher snapshots ignored regular
files using Git's exclude rules, and the supervisor fails if a phase creates a
new ignored file, such as a `__pycache__` or `*.pyc`, outside the allowed write
scope.

## Allowed Writes

Allowed live-workspace writes:

- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-*`;
- `docs/plans/logs/dpf-v2-algorithm-full-comparison-*`;
- `experiments/dpf_implementation/reports/dpf-v2-*`;
- `experiments/dpf_implementation/reports/outputs/dpf_v2_*`;
- `experiments/dpf_implementation/tf_tfp/**` files needed to implement
  BayesFilter-owned comparison runners and adapters;
- `scripts/dpf_v2_algorithm_full_comparison_*` support scripts.

Forbidden writes:

- `.localsource/filterflow/**`;
- student implementation directories and student report outputs;
- docs chapters, bibliography, or unrelated plans;
- git staging, commits, pushes, resets, restores, or rebases;
- environment/dependency installation files unless a separate reviewed repair
  amendment and explicit user approval authorize them.

## Claude Read-Only Reviewer Contract

Claude is a critical reviewer only. It is launched by the live supervisor after
the Codex phase worker returns. It may:

- read files;
- search files;
- inspect logs and JSON/markdown artifacts;
- return `PASS` or material blocker findings.

Claude may not:

- edit files;
- write ledgers directly;
- run mutation-capable shell commands;
- repair code;
- launch phase runners;
- relax contracts.

The live supervisor records Claude's review output in the phase Claude review
ledger. If Claude blocks a phase, the supervisor relaunches a Codex repair
worker with the read-only review output as blocker evidence. Codex may repair
only after writing a repair amendment and getting Claude read-only review PASS
on that amendment.

## Execution State Machine

Each phase runs through:

```text
PHASE_READY
  -> PRIOR_ARTIFACTS_LOADED
  -> LOCAL_SKEPTICAL_PHASE_AUDIT_RECORDED
  -> LOCAL_EVIDENCE_OR_IMPLEMENTATION_RUN
  -> ARTIFACTS_WRITTEN
  -> LOCAL_GATE_CHECK
  -> SUPERVISOR_CLAUDE_READ_ONLY_REVIEW
  -> PHASE_PASS_OR_CLASSIFIED
```

Failure transition:

```text
LOCAL_EVIDENCE_OR_IMPLEMENTATION_RUN or LOCAL_GATE_CHECK or SUPERVISOR_CLAUDE_READ_ONLY_REVIEW
  -> BLOCKER_CLASSIFIED
  -> REPAIR_AMENDMENT_WRITTEN
  -> CLAUDE_READ_ONLY_REPAIR_REVIEW
  -> REVIEWED_REPAIR_IMPLEMENTED
  -> RERUN_AFFECTED_PHASE_EVIDENCE
```

Stop transitions:

```text
BLOCKER_CLASSIFIED -> HUMAN_INTERVENTION_REQUIRED
SUPERVISOR_CLAUDE_READ_ONLY_REVIEW -> STOP_MAX_REVIEW_ROUNDS
LOCAL_GATE_CHECK -> STOP_ARTIFACT_CONTRACT_FAILURE
```

## Phase Artifact Map

| Phase | Subplan | Required result artifact | Required JSON artifact |
|---|---|---|---|
| P0 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-result-2026-06-07.md` | `experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_p0_governance_2026-06-07.json` |
| P1 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p1-architecture-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p1-architecture-result-2026-06-07.md` | `experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_p1_architecture_2026-06-07.json` |
| P2 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p2-bootstrap-ot-contracts-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p2-bootstrap-ot-contracts-result-2026-06-07.md` | `experiments/dpf_implementation/reports/outputs/dpf_v2_bootstrap_ot_contracts_2026-06-07.json` |
| P3 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p3-bootstrap-ot-values-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p3-bootstrap-ot-values-result-2026-06-07.md` | `experiments/dpf_implementation/reports/outputs/dpf_v2_bootstrap_ot_values_2026-06-07.json` |
| P4 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p4-bootstrap-ot-gradients-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p4-bootstrap-ot-gradients-result-2026-06-07.md` | `experiments/dpf_implementation/reports/outputs/dpf_v2_bootstrap_ot_gradients_2026-06-07.json` |
| P5 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-result-2026-06-07.md` | `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_contracts_2026-06-07.json` |
| P6 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p6-ledh-pfpf-ot-values-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p6-ledh-pfpf-ot-values-result-2026-06-07.md` | `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_values_2026-06-07.json` |
| P7 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p7-ledh-pfpf-ot-gradients-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p7-ledh-pfpf-ot-gradients-result-2026-06-07.md` | `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_gradients_2026-06-07.json` |
| P8 | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p8-closeout-subplan-2026-06-07.md` | `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-closeout-result-2026-06-07.md` | `experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_closeout_2026-06-07.json` |

Each phase must also have a phase review ledger with suffix
`-claude-review-ledger-2026-06-07.md`, written by the live supervisor from the
Claude read-only review output, and a phase command manifest under the run log
directory named `<phase>-command-manifest.json`.

The JSON phase artifact must expose `required_v2_model_ids` exactly equal to
the six required rows. P0/P1/P2/P3/P5/P6 must expose the phase-specific
`*_gate_status_by_row` map with `PASS` for every row. P4 and P7 must also
expose `required_gradient_knobs_by_row` with a nonempty list for every row. P8
must expose `phase_gate_statuses` for P0--P7 and, for a full pass, row-status
maps for both algorithms' value and gradient gates plus
`required_gradient_knobs_by_algorithm_and_row`; for a blocked closeout it must
set `blocker_classification_reviewed: true` and list `blocked_items`.

The command manifest must include `run_id`, `phase`, and a nonempty `commands`
list. Each command record must include `command`, `exit_code: 0`, and a
relative `log_path` under the run directory. Each command log must contain
`run_id`, `phase`, `command_index`, and `exit_code: 0` markers.

## Launch Command

The live launcher is:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_live_gated_launch.sh
```

The launcher must:

- run from `/home/chakwong/BayesFilter`;
- create `docs/plans/logs/<run_id>/`;
- write prelaunch dirty manifests;
- launch the live supervisor in the current workspace;
- use `scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh`
  for Claude review;
- record PID, log file, and run id;
- stop immediately if the plan has not been Claude-reviewed to PASS.

## Resume Policy

Because artifacts are live in the repository, recovery should resume from the
latest phase whose result ledger, JSON artifact, command manifest, local gate,
and Claude read-only review ledger all agree on the required token.

A phase with a result note but no reviewer PASS is not complete. A phase with a
reviewer PASS but a failed local gate is not complete. A stopped blocker must
be resumed from the blocker classification and repair amendment, not by
rerunning downstream phases.

## Final Closeout

The final live execution closeout must state:

- run id;
- executed phases;
- final status;
- whether P8 is `PASS_FULL_COMPARISON` or
  `BLOCKED_WITH_REVIEWED_CLASSIFICATION`;
- exact artifact list;
- `.localsource/filterflow` commit and dirty status before and after;
- protected dirty tracked files before and after;
- strongest alternative explanation;
- what would overturn the conclusion;
- all preserved non-claims.
