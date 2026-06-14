# BayesFilter Highdim Zhao--Cui P30 Overnight Gated Self-Recovery Runbook

metadata_date: 2026-06-05

parent_plans:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-remaining-phases-gated-execution-master-plan-2026-06-05.md`

primary_governing_sources:
- P30 mathematical specification:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
- source-governance charter:
  `docs/plans/bayesfilter-highdim-zhao-cui-source-governance-charter-2026-06-05.md`
- traceability ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md`
- MATLAB reference audit:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p34-zhao-cui-reference-implementation-audit-result-2026-06-03.md`
- P10 MATLAB code audit:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-code-audit-ledger-2026-05-30.md`

current_checkpoint:
- M0 governance/schema: complete; anchored by
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase0-governance-fixtures-result-2026-06-05.md`
  and
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase0-governance-fixtures-claude-review-ledger-2026-06-05.md`.
- M1 exact LGSSM references: complete; anchored by
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase1-lgssm-exact-reference-result-2026-06-05.md`
  and
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase1-lgssm-exact-reference-claude-review-ledger-2026-06-05.md`.
- M2 dense P30 synthetic stochastic-volatility references: complete; anchored
  by
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2-stochastic-volatility-result-2026-06-05.md`
  and
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2-stochastic-volatility-claude-review-ledger-2026-06-05.md`.
- M2.5 scalar dense nonlinear BayesFilter value path: complete; anchored by
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p5-nonlinear-value-path-result-2026-06-05.md`
  and
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p5-nonlinear-value-path-claude-review-ledger-2026-06-05.md`.
- M2.6a fixed-design functional TT fitting for scalar SV adjacent square-root
  targets: complete and Claude-reviewed; anchored by
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-result-2026-06-05.md`
  and
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-claude-review-ledger-2026-06-05.md`.

next_gate:
- M2.6b squared-density normalizer and retained marginalization for fitted
  adjacent SV targets.

## Purpose

This runbook governs an overnight or unattended execution of the remaining
P37/P30 Zhao--Cui gates.  It authorizes the agent to make reviewed, fixable
repairs inside each phase, but it does not authorize the agent to weaken the
scientific contract, relax a veto, or convert proxy diagnostics into promotion
criteria.

The run is intentionally autonomous only inside a strict gate:

```text
reviewed plan -> implementation -> evidence audit -> reviewed repair if needed
-> re-execution -> result ledger -> Claude code/governance review
```

The run stops only when the remaining issue requires human scientific judgment,
license/governance approval, infrastructure access that is unavailable, or a
failed veto that neither Codex nor Claude can fix without changing the contract.

## Source-Governance Status

- P30 anchors identified: yes.  This runbook delegates phase-specific exact
  equation anchors to the reviewed subplans and requires M2.6b to begin from
  `eq:p33-square-mass`, `eq:p33-mass-recursion`, `eq:p33-mass-final`,
  `eq:p33-density-with-floor`, `eq:p33-full-normalizer`,
  `eq:p33-retained-marginal`, and `eq:p33-retained-normalized`.
- Zhao--Cui paper anchors identified: yes, at the algorithm/model-suite level
  through the parent master program; each phase must refine paper anchors
  before coding.
- MATLAB behavioral anchors identified: yes, through the P34 reference audit
  and P10 MATLAB audit ledger; each phase must refine file/function anchors
  before making behavioral-reference claims.
- BayesFilter code/test anchors identified: partial.  M0--M2.6a have result
  and test anchors listed in their ledgers.  Later phases must add or update
  code/test anchors before promotion.
- Deviations listed: yes.  Fixed-design fitting, branch replay, repair-loop
  governance, and stress-only ladders are BayesFilter governance or
  engineering extensions unless a phase-specific ledger proves source matching.
- Clean-room boundary respected: yes.  MATLAB code is audit/reference material
  only and must not be copied, line-translated, or used to dictate production
  structure.
- Unsupported claims removed: yes.  This runbook does not claim sequential
  TT/SIRT filtering, paper-scale reproduction, derivative/HMC/DSGE/GPU
  readiness, or high-dimensional scalability.
- Reviewer verdict: `PASS_OVERNIGHT_RUNBOOK`, recorded in
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-overnight-gated-self-recovery-runbook-claude-review-ledger-2026-06-05.md`.

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW_BEFORE_EXECUTION`.

The strongest risk in an overnight run is drift: once a phase fails, an agent
may be tempted to relax tolerance, switch fixtures, use a tuned holdout, skip a
guardrail, or promote an explanatory diagnostic because it lets the run
continue.  M2.6a already exposed this risk: the original degree-12 fixture
failed, and the acceptable recovery required a new fixture ID, a fresh audit
holdout, and Claude review before promotion.

This runbook therefore treats failure recovery as a governed subphase rather
than an informal debugging session.  A fixable blocker may be repaired only
after:

- the failure is classified;
- the phase plan or a plan amendment states the solution and evidence contract;
- Claude reviews the plan amendment to explicit `PASS`; max five exhausted
  rounds create a stop note, not launch or repair authority;
- the implementation reruns the original and amended evidence checks;
- the result ledger records the failed attempt, repair, and non-claims.

The runbook blocks:

- post hoc tolerance relaxation;
- reusing a tuned holdout as promotion evidence;
- changing fixtures without a new fixture ID and ledger entry;
- treating fit residuals, smoke tests, validation loss, ESS, rank trends, or
  wall time as correctness evidence unless the phase contract says so;
- moving to M3--M7 before M2.6b--M2.6d close the SV TT/SIRT-like value path;
- copying MATLAB code or line-translating reference implementation structure;
- claiming sequential filtering, high-dimensional scalability, derivative,
  HMC, DSGE, GPU-production, or paper-scale Zhao--Cui reproduction without
  direct phase evidence.

No material flaw was found in using this runbook as a governing artifact.  It
must still receive Claude plan review before unattended execution begins.

## Evidence Contract

Question: can Codex execute the remaining P37/P30 Zhao--Cui phases overnight in
a way that makes reviewed progress, repairs fixable failures, and stops only
for issues requiring human intervention, while preserving source governance and
scientific claim discipline?

Baseline/comparator:

- phase-specific dense, exact, finite-difference, replay, or stress baselines
  from the reviewed subplans;
- P30 equations and validation ladder;
- Zhao--Cui paper sections/equations as mathematical source;
- audited MATLAB files as behavioral anchors only;
- current M0--M2.6a BayesFilter result ledgers and tests as guardrails.

Primary promotion criterion:

- each phase reaches a reviewed `PASS` result ledger whose claims match the
  phase evidence and traceability ledger statuses.

Veto diagnostics:

- missing P30 or paper anchor for a mathematical claim;
- missing MATLAB audit anchor for a behavioral reference claim;
- missing BayesFilter code/test anchor for an implementation claim;
- MATLAB code copied, line-translated, or used to dictate production structure;
- nonfinite target, likelihood, normalizer, marginal, replay, derivative,
  resource, or downstream scalar diagnostic where finite values are required;
- exact-reference, M2/M2.5, M2.6a, or public API guardrail regression;
- fixture, holdout, rank, basis, tolerance, or baseline changed without a
  reviewed plan amendment;
- tuned diagnostic data reused as independent promotion evidence;
- branch or replay mismatch in fixed-branch phases;
- lower-phase veto left open while a later phase tries to promote;
- Claude blocker unresolved after five review iterations;
- scientific claim requires a human choice between incompatible interpretations.

Explanatory-only diagnostics:

- fit residuals, holdout residuals, ranks, basis degree, ALS sweeps, condition
  numbers, wall time, memory, target-evaluation counts, ESS trends, resource
  trends, branch hashes, plots, and smoke-test timing, unless a reviewed phase
  contract explicitly promotes one of them for a narrow stress-only claim.

What will not be concluded even if the overnight run reaches M7:

- no claim of full adaptive Zhao--Cui MATLAB TT-cross reproduction unless a
  dedicated gate supplies that evidence;
- no stable top-level public API;
- no DSGE or HMC readiness;
- no GPU production readiness unless escalated GPU tests pass;
- no claim that all high-dimensional nonlinear filters have low TT rank;
- no permission to copy MATLAB code into BayesFilter.

Artifacts preserving the result:

- this runbook;
- one subplan, result ledger, and Claude review ledger per phase or repair
  amendment;
- updated traceability ledger rows for every promoted implementation claim;
- command manifests with CPU/GPU status, seeds, environment, and dirty-worktree
  status.

## Authorization And Supersession

This runbook does not by itself supersede the remaining-phases master plan.  It
becomes an executable unattended-launch authority only after:

- the remaining-phases master plan records that `PASS_M2P6A` has been achieved;
- the remaining-phases master plan explicitly authorizes this runbook to
  govern M2.6b onward;
- this runbook receives substantive Claude review to
  `PASS_OVERNIGHT_RUNBOOK`.

Until those conditions pass, this artifact is a plan and launch prompt only.

## Subplan Prerequisites

The overnight launch requires these subplans to exist before starting:

- M2.6b:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6b-squared-density-normalizer-marginal-subplan-2026-06-05.md`
- M2.6c:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6c-short-sequential-sv-tt-value-path-subplan-2026-06-05.md`
- M2.6d:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6d-sv-tt-lane-closeout-subplan-2026-06-05.md`

M2.6b must be reviewed to `PASS` before implementation.  M2.6c and M2.6d may
remain planned until their own gates, but they must exist so the unattended
launcher cannot jump from M2.6a directly to M3 without closing the SV TT lane.

## Execution State Machine

Each phase runs through the following states.  A phase may not skip a state
unless the result ledger records a reviewed reason.

```text
READY
  -> PLAN_DRAFTED_OR_UPDATED
  -> SKEPTICAL_PLAN_AUDITED
  -> CLAUDE_PLAN_REVIEWED
  -> IMPLEMENTED
  -> LOCAL_EVIDENCE_RUN
  -> EVIDENCE_AUDITED
  -> RESULT_LEDGER_WRITTEN
  -> CLAUDE_CODE_GOVERNANCE_REVIEWED
  -> TRACEABILITY_UPDATED
  -> PHASE_PASS
```

Failure transitions:

```text
LOCAL_EVIDENCE_RUN or EVIDENCE_AUDITED
  -> BLOCKER_CLASSIFIED
  -> REPAIR_PLAN_AMENDMENT
  -> CLAUDE_REPAIR_PLAN_REVIEWED
  -> REPAIR_IMPLEMENTED
  -> LOCAL_EVIDENCE_RUN
```

Stop transitions:

```text
BLOCKER_CLASSIFIED
  -> HUMAN_INTERVENTION_REQUIRED

CLAUDE_REPAIR_PLAN_REVIEWED
  -> STOP_MAX_REVIEW_ROUNDS

EVIDENCE_AUDITED
  -> STOP_FAILED_VETO_UNFIXABLE
```

## Blocker Classification

Every failure must be classified before repair.

### Fixable By Codex And Claude

These may be repaired autonomously with reviewed amendments:

- coding bug with unchanged mathematical contract;
- missing assertion, missing fixture hash, missing manifest field, or missing
  result-ledger entry;
- incorrect import, dtype, shape, batching, seed, or CPU-only test setup;
- missing narrow test for an already planned behavior;
- numerical stabilization that preserves the P30 equation and phase baseline;
- fixture versioning problem that can be solved by a new fixture ID and fresh
  untouched audit evidence;
- tolerance specification bug where the correct threshold was already present
  in the reviewed plan but not enforced;
- documentation overclaim that can be removed without changing the result;
- traceability row status that can be downgraded to `REFERENCE_ONLY`,
  `BAYESFILTER_EXTENSION`, `DOCUMENTED_DEVIATION`, or `BLOCKED_UNVALIDATED`
  without promoting the claim.

### Requires Human Intervention

The overnight run must stop for:

- relaxing or replacing a primary pass/fail criterion;
- choosing a new scientific baseline or comparator;
- deciding whether a failed veto is acceptable;
- accepting weaker evidence for a stronger claim;
- changing a model equation, posterior convention, or P30 interpretation in a
  way that is not clearly a typo;
- changing clean-room or license policy;
- adding a stable public API;
- starting DSGE/HMC/GPU-production claims;
- deciding between two incompatible Claude/Codex interpretations after five
  review rounds;
- infrastructure failure that cannot be resolved by a CPU-only fallback already
  authorized in the phase plan.

### Must Be Recorded As Negative Evidence

These are not necessarily human blockers, but they cannot be hidden:

- rank saturation;
- conditioning failure;
- resource timeout;
- unstable finite-difference window;
- SMC/Monte Carlo uncertainty too large for a comparison;
- basis or coordinate-map policy that gives finite but poor accuracy;
- exact-reference mismatch.

The result ledger must separate implementation failure, tuning failure,
diagnostic failure, and evidence against the scientific idea.

## Repair Loop Rules

For each fixable blocker:

1. Create a repair note in the phase Claude review ledger.
2. Patch or create a phase-plan amendment with:
   - failure evidence;
   - blocker classification;
   - proposed repair;
   - unchanged versus changed contract fields;
   - fresh evidence required after repair;
   - non-claims.
3. Run Claude repair-plan review with max five iterations.
4. Implement only the reviewed repair.
5. Rerun:
   - the failed focused test or diagnostic;
   - the phase focused test set;
   - the broad highdim guardrail set;
   - `python -m compileall -q bayesfilter/highdim tests/highdim`;
   - `git diff --check` for changed files.
6. Write the failed attempt and repair result into the result ledger.
7. Run Claude code/governance review with max five iterations.

If Claude returns a blocker that Codex accepts, patch it and loop.  If Codex
disputes it, record the dispute and ask Claude once more with the relevant
source anchors.  A persistent dispute after five rounds stops the run.

## Phase Order

Required order for the overnight run:

```text
M2.6b -> M2.6c -> M2.6d -> M3 -> M4 -> M5 -> M6 -> M7
```

M2.6b primary purpose:
- squared-density normalizer and retained marginalization for fitted adjacent
  SV targets from M2.6a.

M2.6c primary purpose:
- short sequential SV TT/SIRT-like value path against dense M2/M2.5 oracle.

M2.6d primary purpose:
- SV TT lane replay, branch, governance, and traceability closeout.

M3 primary purpose:
- spatial SIR source-governed fixtures and small filtering rows.

M4 primary purpose:
- predator-prey preconditioning gate under matched comparison controls.

M5 primary purpose:
- stress ladders and failure/resource manifests, not correctness promotion.

M6 primary purpose:
- fixed-branch gradient only for value-validated scalar rows.

M7 primary purpose:
- integration closeout, traceability statuses, blocker list, and non-claims.

## M2.6b Required Anchors

M2.6b must identify exact anchors before implementation:

- square-mass contraction: `eq:p33-square-mass`;
- mass recursion: `eq:p33-mass-recursion`;
- mass finalization: `eq:p33-mass-final`;
- density with floor: `eq:p33-density-with-floor`;
- full normalizer: `eq:p33-full-normalizer`;
- retained marginal: `eq:p33-retained-marginal`;
- retained normalized density: `eq:p33-retained-normalized`.

M2.6b may not claim:

- sequential SV TT filtering;
- adaptive TT-cross reproduction;
- paper-scale `T=1000`;
- SMC or real-data validation;
- derivative/HMC/DSGE/GPU readiness.

## Standard Claude Commands

Plan review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p37-<phase>-plan-review-iter<N> \
  --model sonnet \
  --effort high \
  "<bounded phase plan review prompt>"
```

Repair-plan review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p37-<phase>-repair-plan-review-iter<N> \
  --model sonnet \
  --effort high \
  "<bounded repair plan review prompt>"
```

Code/governance review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p37-<phase>-code-governance-review-iter<N> \
  --model sonnet \
  --effort high \
  "<bounded governance, math, code, and evidence review prompt>"
```

Claude prompts must include:

```text
First perform governance review. Block if any mathematical or behavioral claim
lacks a P30 anchor, Zhao--Cui paper anchor, MATLAB anchor, BayesFilter
code/test anchor, or explicit deviation. Check the clean-room boundary. Only
after governance passes, review implementation quality. Return PASS only if
governance, math, implementation, and evidence contracts all pass.
```

Claude commands require trusted/elevated execution under the cross-agent policy.

## Standard Local Commands

Every phase begins with:

```bash
git diff --check
```

CPU-only focused tests must use:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q <focused tests>
```

Broad highdim guardrail:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py \
  tests/highdim/test_phase0_contracts.py \
  tests/highdim/test_bases.py \
  tests/highdim/test_tt_algebra.py \
  tests/highdim/test_squared_tt_density.py \
  tests/highdim/test_transport.py \
  tests/highdim/test_fixed_branch_fit.py \
  tests/highdim/test_failure_exits.py \
  tests/highdim/test_filtering_kalman_exact.py \
  tests/highdim/test_fixed_branch_derivatives.py \
  tests/highdim/test_scaling_smoke.py \
  tests/highdim/test_public_api_highdim.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/highdim/test_p30_lgssm_exact_reference.py \
  tests/highdim/test_p30_stochastic_volatility.py \
  tests/highdim/test_p30_sv_fixed_design_tt_target.py
```

Compile:

```bash
python -m compileall -q bayesfilter/highdim tests/highdim
```

Whitespace:

```bash
git diff --check -- <changed files>
```

GPU commands are not part of the overnight default.  If a reviewed phase
requires GPU detection or GPU execution, use escalated permissions and record
the trusted GPU status in the result ledger.

## Required Result Ledger Template

Every phase result ledger must include:

```text
metadata_date:
phase:
decision:

source_governance_status:
- P30 anchors identified:
- Zhao--Cui paper anchors identified:
- MATLAB behavioral anchors identified:
- BayesFilter code/test anchors identified:
- deviations listed:
- clean-room boundary respected:
- unsupported claims removed:
- reviewer verdict:

evidence_contract_status:
- primary criterion:
- veto diagnostics:
- explanatory diagnostics:
- main uncertainty:
- next justified action:
- what is not concluded:

run_manifest:
- git commit:
- dirty/untracked status:
- environment:
- CPU/GPU status:
- dtype:
- random seeds:
- commands:
- wall time:
- output artifacts:

failure_and_repair_log:
- failed attempt:
- blocker classification:
- plan amendment:
- Claude repair review:
- rerun evidence:

decision_table:
- decision:
- primary criterion status:
- veto diagnostic status:
- strongest uncertainty:
- next justified action:
- non-claims:

post_run_red_team:
- strongest alternative explanation:
- result that would overturn the decision:
- weakest part of the evidence:
```

Use `N/A` only where the field genuinely does not apply.

## Traceability Update Rule

After each phase:

- add or update traceability rows for every implementation claim;
- mark unsupported source claims `REFERENCE_ONLY`;
- mark implemented but insufficiently validated claims `BLOCKED_UNVALIDATED`;
- mark clean-room extensions `BAYESFILTER_EXTENSION`;
- mark intentional source differences `DOCUMENTED_DEVIATION`;
- never promote `BLOCKED_UNTRACEABLE` or `BLOCKED_UNVALIDATED` rows.

Traceability updates must be reviewed by Claude in the phase code/governance
review before the phase can pass.

## Overnight Stop Note Template

If the run stops, write a stop note in the active phase result ledger:

```text
stop_status:
- phase:
- state:
- reason:
- blocker classification:
- Codex attempts:
- Claude review iterations:
- last passing gate:
- files changed:
- commands run:
- evidence preserved:
- human decision needed:
- safest next prompt:
```

## Launch Prompt

Use this prompt to start the overnight run:

```text
Execute the overnight gated self-recovery runbook:
docs/plans/bayesfilter-highdim-zhao-cui-p30-overnight-gated-self-recovery-runbook-2026-06-05.md

Start at M2.6b. For each phase, follow the state machine exactly: write or
revise the phase subplan, perform skeptical plan audit, run Claude plan review
to explicit PASS. If five review rounds end without PASS, write a stop note
and do not implement that phase. After explicit plan PASS, implement only the
reviewed block, run focused tests and broad guardrails, audit evidence against
the contract, write the result ledger, run Claude code/governance review to
explicit PASS, update traceability, then proceed to the next phase. If five
code/governance review rounds end without PASS, write a stop note and do not
promote or continue the phase.

If a blocker appears, classify it. For fixable blockers, create a repair plan
amendment, send it through Claude review to explicit PASS, implement the
reviewed repair, rerun the failed diagnostic plus phase and broad guardrails,
and record the failed attempt and repair in the result ledger. If five repair
review rounds end without PASS, stop and preserve the blocker record.

Stop only for unresolved Claude/Codex blockers, failed veto diagnostics that
cannot be repaired without changing the scientific contract, clean-room or
license issues, infrastructure blockers that cannot use an already authorized
fallback, or decisions requiring human scientific judgment. Do not relax
tolerances, change fixtures, change baselines, reuse tuned holdouts, or promote
proxy metrics without a reviewed plan amendment.
```

## Exit Criteria For This Runbook

This runbook is ready to execute only after:

- Claude plan review returns explicit `PASS_OVERNIGHT_RUNBOOK` for this
  runbook and its prerequisite subplans;
- `git diff --check` passes for this file;
- the final launch message states that unattended execution is best-effort
  reviewed progress, not a guarantee that all phases will complete.

Five-round exhaustion may preserve the blocker record and stop note, but it
does not create launch authority for unattended execution.
