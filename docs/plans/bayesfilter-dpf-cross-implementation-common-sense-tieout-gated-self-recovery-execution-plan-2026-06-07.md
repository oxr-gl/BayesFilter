# DPF Cross-Implementation Gated Self-Recovery Execution Plan

metadata_date: 2026-06-07
plan_status: claude_reviewed_launch_ready

parent_program:
- `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-plan-2026-06-06.md`

phase_subplans:
- P0: `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p0-governance-subplan-2026-06-07.md`
- P1: `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p1-common-model-contracts-subplan-2026-06-07.md`
- P2: `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p2-value-paths-subplan-2026-06-07.md`
- P3: `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p3-fixed-resampling-subplan-2026-06-07.md`
- P4: `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p4-fixed-branch-gradients-subplan-2026-06-07.md`
- P5: `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p5-remaining-bf-ff-coverage-subplan-2026-06-07.md`
- P6: `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p6-terminal-student-repetition-subplan-2026-06-07.md`

review_ledger:
- `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-gated-self-recovery-execution-claude-review-ledger-2026-06-07.md`

## Purpose

This plan governs an overnight or unattended execution of the DPF
cross-implementation common-sense tie-out master program.  It authorizes Codex
to handle fixable blockers with Claude-reviewed repair loops, while preserving
the program's scientific contract:

```text
BayesFilter/FilterFlow closure first -> terminal student repetition only after P0--P5 close
```

The execution stops only when the remaining issue requires human judgment,
unavailable access, explicit approval, or a scientific-contract change that
Codex and Claude cannot resolve within five review rounds.

## Skeptical Plan Audit

Status: `PASS_AS_EXECUTION_POLICY_DRAFT`.

Main drift risk:

- an unattended recovery loop can silently weaken the comparison by relaxing
  tolerances, replacing fixtures, changing scalar objectives, changing branch
  semantics, or letting student outputs influence the BayesFilter/FilterFlow
  comparator.

Controls:

- every blocker must be classified before repair;
- every repair must preserve or explicitly amend the phase evidence contract;
- every amendment requires Claude review to convergence or max five rounds;
- tolerance, fixture, comparator, scalar, model, and branch changes are vetoes
  unless the phase plan is explicitly amended and reviewed before execution;
- P6 student work cannot start until P0--P5 are closed and a closed-fixture
  manifest exists.

No material flaw was found in using this plan as an execution-policy draft.
It still requires Claude plan review before unattended launch.

## Evidence Contract

Question:

- can Codex execute the DPF cross-implementation master program in gated
  overnight form, repairing fixable issues with Claude review and stopping only
  when Codex and Claude cannot proceed without human intervention?

Primary comparator:

- P0--P5: BayesFilter against executable local float64 FilterFlow only;
- P6: BayesFilter, FilterFlow, and student implementations as peers, only
  after P0--P5 closure and fixture freeze.

Primary pass criterion:

- every phase reaches a result ledger where each executed cell is classified as
  `MATCHED`, `EXPLAINED_MISMATCH`, `INTERFACE_BLOCKED`, or `OUT_OF_SCOPE`, and
  where Claude review reports no material blocker.

Veto diagnostics:

- unclassified mismatch;
- nonfinite scalar or gradient in an executed cell;
- missing manifest, dtype, seed, branch, scalar, parameterization, or artifact;
- gradient comparison across incompatible branches or scalar objectives;
- treating BayesFilter, FilterFlow, TT, paper tables, dense quadrature, or a
  student implementation as an oracle;
- changing tolerance, fixture, model, branch, scalar objective, comparator, or
  parameterization after seeing results without a reviewed plan amendment;
- mutating `.localsource/filterflow` without explicit human approval and a
  provenance note;
- CPU-only TensorFlow import before `CUDA_VISIBLE_DEVICES=-1`;
- running any student command before P0--P5 closure;
- exhausting five Claude review iterations with a material blocker still open.

Explanatory diagnostics:

- finite differences, Kalman references, dense quadrature, residuals, ESS,
  runtime, row residuals, Monte Carlo standard errors, source inventory, and
  interface notes.  These explain classifications; they do not prove filtering
  correctness by default.

What will not be concluded:

- no claim that any filter algorithm is correct;
- no claim that BayesFilter, FilterFlow, or a student implementation is an
  oracle;
- no TT-filter correctness claim;
- no paper-scale reproduction claim;
- no HMC, DSGE, GPU, or production-readiness claim.

Artifacts preserving the result:

- this execution plan;
- one phase result ledger per executed phase;
- one Claude review ledger per phase or repair cycle;
- JSON output manifests for executed runners;
- closed-fixture manifest before P6;
- final execution closeout ledger.

## Launch Preconditions

The overnight launcher may start only after:

- this execution plan passes Claude review to `PASS`;
- the master program review ledger remains converged;
- P0--P6 subplans exist;
- local `git diff --check` passes for the governing plan files;
- the executor records the current git commit or dirty-worktree status;
- the executor records CPU-only intent for TensorFlow runs, or obtains trusted
  GPU approval if a later reviewed phase explicitly requires GPU execution.

## Standing Human Approvals

Approval date: 2026-06-07.

The following standing approvals are granted for this execution plan:

- Approval A: Codex may make non-semantic instrumentation edits inside
  `.localsource/filterflow` for debugging and evidence extraction, provided
  every such edit is recorded, does not alter computation semantics, and
  patched-comparator results are labeled as instrumented evidence.
- Approval B: Codex may make local environment or shim edits inside
  `.localsource/filterflow` needed to execute the existing comparator, provided
  they do not alter model math, filtering semantics, scalar objectives,
  resampling behavior, RNG behavior, or gradients.
- Approval C: Codex may create temporary comparator-preserving bug-isolation
  patches inside `.localsource/filterflow`, but must record provenance and must
  not treat results as unpatched upstream FilterFlow evidence.
- Approval D: Codex may run GPU/CUDA/NVIDIA detection, initialization,
  TensorFlow/JAX/PyTorch GPU probes, GPU smoke tests, and GPU
  benchmark/HMC jobs with escalated or trusted permissions when a reviewed phase
  plan or repair plan calls for GPU execution.  All GPU artifacts must record
  trusted GPU status, command, environment, and whether GPU use was required or
  exploratory.

These approvals do not authorize semantic FilterFlow edits.  Any change to
FilterFlow model math, proposal semantics, resampling order, weight update,
scalar objective, RNG behavior, or gradient computation remains a
human-intervention blocker requiring specific approval.

## Execution State Machine

Each phase runs through these states:

```text
PHASE_READY
  -> PLAN_AND_PRIOR_ARTIFACTS_LOADED
  -> SKEPTICAL_PHASE_AUDIT
  -> CLAUDE_PLAN_REVIEWED
  -> LOCAL_EVIDENCE_RUN
  -> EVIDENCE_AUDITED
  -> RESULT_LEDGER_WRITTEN
  -> CLAUDE_RESULT_REVIEWED
  -> PHASE_PASS
```

Failure transitions:

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
```

## Phase Order

Required order:

```text
P0 -> P1 -> P2 -> P3 -> P4 -> P5 -> P6
```

Phase purposes:

- P0: confirm governance, no-oracle policy, and no-premature-student policy.
- P1: tie out common density/model contracts between BayesFilter and
  FilterFlow.
- P2: tie out deterministic fixed-noise no-resampling value paths.
- P3: tie out fixed-ancestor resampling value paths.
- P4: tie out fixed-branch gradients against finite-difference self-checks.
- P5: classify remaining BayesFilter/FilterFlow surfaces as matched,
  explained, interface-blocked, or out of scope.
- P6: repeat the closed fixture campaign against student implementations as
  terminal peers only.

P6 is blocked until P0--P5 all have reviewed result ledgers and a
closed-fixture manifest.

## Blocker Classification

Every failure must be classified before repair.

### Fixable By Codex And Claude

These issues may be repaired autonomously after a reviewed plan amendment:

- coding bug with unchanged mathematical model, scalar objective, branch, and
  comparator;
- missing manifest field, fixture checksum, dtype record, seed, command
  record, or result-ledger entry;
- incorrect import, shape, dtype, batching, seed, or CPU-only setup;
- missing validation command for a runner already named by the phase plan;
- adapter mismatch where the correct existing adapter surface is clear and the
  mathematical object is unchanged;
- `.localsource/filterflow` edits that fall strictly under standing Approvals
  A--C, provided they receive a reviewed amendment, provenance label, and
  patched-comparator evidence label before any rerun;
- documentation overclaim that can be removed or downgraded;
- classification gap that can be resolved as `INTERFACE_BLOCKED`,
  `OUT_OF_SCOPE`, or `EXPLAINED_MISMATCH` without changing evidence;
- tolerance-enforcement bug where the intended tolerance was already declared
  in the reviewed phase plan.

### Requires Human Intervention

The execution must stop for:

- relaxing a primary tolerance or pass/fail criterion after seeing results;
- choosing a new scientific comparator or baseline;
- deciding that a failed veto is acceptable;
- changing model equations, scalar objectives, branch semantics, or parameter
  meanings in a nontrivial way;
- mutating `.localsource/filterflow` outside standing Approvals A--C;
- treating any `.localsource/filterflow` edit under Approvals A--C as
  unpatched upstream FilterFlow evidence;
- using student output to revise BayesFilter/FilterFlow fixtures;
- starting P6 before P0--P5 closure;
- accepting weaker evidence for a stronger claim;
- infrastructure failure that blocks required execution and has no reviewed
  CPU-only fallback;
- unresolved Codex/Claude disagreement after five review rounds.

### Must Be Recorded As Negative Evidence

These are not necessarily human blockers, but they cannot be hidden:

- interface gap;
- resource timeout;
- nonfinite diagnostic;
- unstable finite-difference window;
- fixed-branch mismatch;
- Monte Carlo uncertainty too large for a comparison;
- exact-reference mismatch;
- student implementation mismatch after P6 opens.

The result ledger must separate implementation failure, interface limitation,
diagnostic failure, and evidence against the attempted common fixture.

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
   objective, model declaration, physical parameterization, or branch
   semantics, stop and require a pre-rerun reviewed phase-plan amendment.  No
   evidence rerun may occur until that amendment passes Claude review.
4. If the proposed repair touches `.localsource/filterflow` under Approvals
   A--C, the amendment must state the approval class, provenance label,
   semantic non-change check, and patched-comparator evidence label before any
   rerun.
5. Run Claude repair-plan review until `PASS` or five rounds.
6. Implement only the reviewed repair.
7. Rerun the failed focused command and the phase validation command.
8. Run `git diff --check` for changed files.
9. Update the result ledger with the failed attempt, repair, rerun result, and
   decision.
10. Run Claude result/code/governance review until `PASS` or five rounds.

If Claude identifies a material blocker, patch and loop.  If Codex disputes the
finding, ask Claude once more with the relevant source and artifact evidence.
A persistent dispute after five rounds stops the run.

## Standard Claude Commands

Claude commands require trusted or escalated execution under the cross-agent
policy.

Plan review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name dpf-tieout-<phase>-plan-review-iter<N> \
  "<bounded phase plan review prompt>"
```

Repair-plan review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name dpf-tieout-<phase>-repair-review-iter<N> \
  "<bounded repair review prompt>"
```

Result/code/governance review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name dpf-tieout-<phase>-result-review-iter<N> \
  "<bounded result review prompt>"
```

Claude prompts must ask for material blockers first and must explicitly check:

- student work is terminal-only;
- no implementation is treated as an oracle;
- the scalar objective, branch, parameterization, and comparator match the
  phase contract;
- mismatch classifications are fair and concrete;
- no correctness claim exceeds the evidence.

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

Known P1--P4 runner commands:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_tieout_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_tieout_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_noresampling_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_noresampling_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_fixed_resampling_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_fixed_resampling_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_fixed_branch_gradient_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_fixed_branch_gradient_tf --validate-only
```

P5 and P6 commands are intentionally not fixed here.  P5 must first determine
the remaining BayesFilter/FilterFlow surface inventory.  P6 must wait for the
closed-fixture manifest and student adapter inventory.

GPU commands are not part of this execution plan by default.  If a reviewed
phase later requires GPU detection or GPU execution, it must use escalated
permissions and record trusted GPU status in the result ledger.

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
- fixture manifest:
- output artifacts:

result_summary:
- matched cells:
- explained mismatches:
- interface blockers:
- out of scope:
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

## Terminal Student Phase Rules

P6 cannot start until:

- P0--P5 result ledgers are reviewed and closed;
- no BayesFilter/FilterFlow executed mismatch is unclassified;
- every interface-blocked surface has a concrete reason;
- a closed-fixture manifest exists;
- the P6 student adapter inventory has been written.

In P6:

- student implementations are peers, not oracles;
- student near-misses must not force tolerance changes;
- student discrepancies must be classified as `EXPLAINED_MISMATCH`,
  `INTERFACE_BLOCKED`, `OUT_OF_SCOPE`, or `MATCHED`;
- student evidence must remain in terminal ledgers and must not retroactively
  define the BayesFilter/FilterFlow comparator.

## Final Closeout

The overnight execution closes with:

- final result:
  `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-gated-self-recovery-execution-result-2026-06-07.md`
- final Claude review ledger update;
- list of phases passed, blocked, or stopped for human intervention;
- list of artifacts produced;
- list of non-claims preserved.

The run is successful only if it makes reviewed progress without weakening the
master program's evidence contract.  A clean `STOP_FOR_HUMAN` is a valid
outcome when the remaining issue exceeds Codex and Claude authority.
