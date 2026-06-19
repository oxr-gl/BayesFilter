# P77 Phase 2 Result: Parameter Count, Budget, And Tuning Protocol

metadata_date: 2026-06-19
status: PHASE2_CLAUDE_AGREE_READY_FOR_PHASE3_SCOPED_CODE_EDITS
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-subplan-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-result-2026-06-19.md
phase: 2
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Summary

Phase 2 makes the P77 budget and tuning protocol operational before any
implementation or training phase.

Phase 2 is design-only.  It did not edit implementation code, construct an
optimizer, call `train_step`, generate samples, run training, run a mechanics
smoke, use GPU/CUDA, use network, install packages, or change defaults.

The central rule is unchanged:
\[
  N_{\rm train}\ge20P_\theta
\]
for any fixed-branch regression/training evidence claim.  For the current
degree-2/rank-4/d=36 candidate, \(P_\theta=1656\), so the hard minimum is
33120 fresh training samples and the preferred first proper budget is
`1024 x 40 = 40960`.

## Parameter Count Source Of Truth

For a dense trainable TT with basis counts \(b_k\) and rank tuple
\((r_0,\ldots,r_d)\), the scalar trainable-parameter count is
\[
  P_\theta=\sum_{k=1}^d r_{k-1}b_kr_k .
\]

For the current candidate:

- dimension \(d=36\);
- degree \(2\), hence \(b_k=3\) for every coordinate;
- rank tuple \((1,4,\ldots,4,1)\);
- all TT core entries trainable.

Thus
\[
  P_\theta
  =
  1\cdot3\cdot4
  +
  34\cdot4\cdot3\cdot4
  +
  4\cdot3\cdot1
  =
  1656 .
\]

This formula is the planning source of truth.  The Phase 3 implementation
surface must also record a runtime parameter-count manifest from actual
trainable variables.  If dimension, rank, degree, basis count, trainable mask,
frozen-core policy, or parameterization changes, \(P_\theta\) must be
recomputed from the actual trainable scalar variables before any evidence run.

## Budget Arithmetic

The evidence gate is
\[
  N_{\rm train}\ge20P_\theta .
\]

For \(P_\theta=1656\),
\[
  N_{\rm train}^{\min}=20\cdot1656=33120.
\]

With `batch_size = 1024`,
\[
  \lceil33120/1024\rceil = 33
\]
fresh training batches are the minimum evidence count.  The first proper P77
diagnostic should use `batch_size = 1024` and `batches = 40`, so
\[
  N_{\rm train}=40960>33120 .
\]

The 40960 budget is the first proper budget, not a large scaling run.  Any
smaller run is a non-evidence mechanics smoke.  Validation, replay, and audit
samples do not count toward \(N_{\rm train}\).

## Tuning Protocol

The tuning protocol is intentionally small.  The goal is not to optimize the
method exhaustively; it is to run a scientifically interpretable first proper
test without arbitrary post-hoc choices.

### Fixed A Priori Values

For the first proper evidence run:

- dimension, degree, rank: `d = 36`, `degree = 2`, `rank = 4`;
- initialization: UKF-initialized untrained TT candidate;
- batch size: `1024`;
- minimum evidence batches: `33`;
- first proper batch budget: `40`;
- optimizer family: Adam, because the current training surface already exposes
  `make_adam_optimizer`;
- gradient clipping: use the current config default unless Phase 3 exposes it
  as an explicit manifest field;
- regularization weights: no new regularization sweep in the first proper
  evidence run; use current configured defaults unless Phase 3 records a
  reviewed opt-in field;
- evaluation metric: corrected validation CE with target-only
  \(\alpha_i\propto w_i s_i^2\);
- comparator: untrained UKF baseline on the same validation/replay/audit
  roles.

### Learning-Rate Candidates

Phase 3 should support a small validation-only learning-rate candidate set:

\[
  \eta\in\{10^{-4},3\cdot10^{-4},10^{-3}\}.
\]

Justification: \(10^{-3}\) is the existing config default; \(3\cdot10^{-4}\)
and \(10^{-4}\) test whether the corrected-metric training is sensitive to
over-aggressive steps without turning Phase 6 into a broad sweep.

These candidates are selected before any new P77 training result is observed.
They may be narrowed only by a reviewed Phase 3/5 mechanics failure, not by
audit data.

### Validation Stopping And Selection Protocol

For each learning-rate candidate:

- start from the same UKF-initialized untrained candidate;
- use fresh training mini-batches with disjoint seeds;
- evaluate corrected validation CE at the untrained baseline and after the
  completed budgeted run;
- if Phase 3 exposes periodic validation without violating runtime bounds,
  checkpoints may be recorded every 10 batches, but the first proper protocol
  selects only among predeclared final or checkpointed candidates using
  validation CE;
- select the candidate with the lowest corrected validation CE among candidates
  whose veto diagnostics pass.

For the first proper run, a candidate may be promoted to audit only if:

\[
  \widehat{\mathcal L}_{\rm val}(\theta_{\rm trained})
  <
  \widehat{\mathcal L}_{\rm val}(\theta_{\rm UKF})
\]
and all veto diagnostics pass.  No minimum effect size is imposed in Phase 2
because this is the first corrected-metric training evidence run, but the
decision table must report the absolute and relative CE change.

If no candidate improves corrected validation CE against the untrained UKF
baseline, Phase 6 must report a negative or tuning-blocked result rather than
using replay/audit to rescue the run.

### Replay Role

Replay is a robustness diagnostic after validation selection.

Replay may veto if:

- replay corrected CE is nonfinite;
- replay CE reconstruction fails;
- replay target-only alpha mass fails tolerance;
- replay uses the wrong role or provenance;
- replay is worse than the untrained UKF baseline by a predeclared severe
  degradation threshold in Phase 5.

Until Phase 5 freezes a numeric severe-degradation threshold, replay is
explanatory only except for nonfinite, reconstruction, alpha-mass, role, or
provenance failures.

Replay cannot select learning rate, stopping time, rank, degree, sample budget,
optimizer settings, or regularization.

### Audit Exclusion

Audit is final-only.  Audit may be evaluated only after:

- learning-rate candidates are frozen;
- stopping and selection rules are frozen;
- the selected candidate is chosen by validation;
- replay has been evaluated under its predeclared role;
- no further changes to rank, degree, sample count, learning rate, optimizer,
  gradient clipping, regularization, seeds, or thresholds are allowed.

Audit cannot tune, select, stop, rescue, or reinterpret a candidate.  It can
only report the final corrected CE and veto nonfinite/invalid metric
construction.

## Required Reporting Fields For Later Diagnostics

A later proper diagnostic JSON/result must record:

- `P_theta`;
- `parameter_count_formula`;
- `trainable_variable_count_runtime`;
- `degree`, `rank`, `dimension`, and rank tuple;
- `batch_size`, `batches`, `N_train`, and `N_train_over_P_theta`;
- `hard_budget_gate_passed`;
- fresh training seed policy and disjoint role seed manifest;
- optimizer family, learning rate, gradient clip norm, regularization weights;
- UKF-initialized untrained baseline corrected validation CE;
- trained candidate corrected validation CE;
- absolute and relative validation CE change;
- replay corrected CE for baseline and trained candidate;
- audit corrected CE for baseline and trained candidate, only after selection;
- corrected alpha sums, CE reconstruction errors, finite flags, normalizer,
  rho range, alpha ESS, and runtime;
- nonclaims: not source-faithful Zhao--Cui, not lower-gate repair evidence,
  not HMC readiness, not scaling evidence, not default-policy evidence.

## Failed Historical Route Fence

Random initialization, calibrated-constant initialization, and source-route
prefit remain failed historical routes.  They must not appear as live
comparators, fallback candidates, tuning anchors, baselines, or promotion
references in the P77 runner, tests, JSON, or result notes.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | Can P77 freeze a non-arbitrary budget and tuning protocol that makes a later training run scientifically interpretable? |
| Exact baseline/comparator | UKF-initialized untrained TT candidate evaluated by corrected validation/replay/audit CE under the same role definitions as trained candidates. |
| Primary criterion | Passed locally pending Claude review: Phase 2 defines \(P_\theta\), recomputation rule, \(20P_\theta\) evidence gate, first proper budget, validation-only tuning/stopping/selection, replay role, audit exclusion, failed-route fences, and required Phase 3 implementation-surface fields. |
| Veto diagnostics | No arbitrary/post-hoc hyperparameter choices; no under-budget evidence allowance; audit excluded from tuning; replay cannot hide selection leakage; random/constant/source-prefit not revived; no implementation/training action occurred. |
| Explanatory only | Learning-rate family justification, possible runtime tradeoffs, mechanics-smoke needs, and P76 CE values. |
| What will not be concluded | No training improvement, no final hyperparameter selection from data, no implementation result, no training-run approval, no lower-gate repair, no validation/HMC readiness, no scaling. |
| Artifact preserving result | This Phase 2 result and the drafted Phase 3 implementation-surface subplan. |

## Skeptical Plan Audit

| Checklist item | Phase 2 answer |
| --- | --- |
| wrong baselines | The only live comparator remains the UKF-initialized untrained candidate. Random, calibrated-constant, and source-prefit remain failed historical routes. |
| proxy metrics | Training loss, residuals, replay values, mechanics smokes, runtime, and P76 CE values cannot become promotion criteria. |
| missing stop conditions | Ambiguous \(P_\theta\), weakened \(20P_\theta\), audit leakage, replay hidden-selection leakage, implementation/training action, or unconverged Claude review stop the phase. |
| unfair comparisons | Trained and baseline candidates must use the same corrected CE formula and the same validation/replay/audit role definitions. |
| hidden assumptions | \(P_\theta\), first proper budget, learning-rate candidates, selection rule, replay role, and audit exclusion are explicit before training. |
| stale context | P76 runner surfaces are implementation context, but P76 numeric CE values are not fit-quality evidence. |
| environment mismatch | Phase 2 is docs-only and does not depend on CPU/GPU, generated samples, optimizer state, package state, or network state. |
| artifact adequacy | This result and the Phase 3 subplan specify enough implementation fields to prevent arbitrary tuning or under-budget promotion. |
| under-budget mechanics smokes | Any later smoke below \(20P_\theta\) is non-evidence and cannot tune, select, promote, or support evidence. |

## Local Checks

Prechecks:

```bash
rg -n "PHASE1|training objective|corrected target-only|UKF-initialized untrained|20P|33120|40960|random|calibrated-constant|source-prefit|audit final" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-subplan-2026-06-19.md
rg -n "P76CorrectedHeldoutMetricBatch|corrected_heldout_density_metric|P75ObjectiveBatch|train_step|make_adam_optimizer" bayesfilter/highdim/stochastic_density_training.py
```

Results:

- Phase 1 handoff and Phase 2 subplan precheck passed.
- Local training/metric code-symbol precheck passed.

Context reads:

- Read `scripts/p76_bounded_ukf_minibatch_pilot.py`.
- Read `tests/highdim/test_p76_bounded_ukf_minibatch_pilot.py`.
- Read `scripts/p76_generated_corrected_metric_diagnostic.py`.
- Read `tests/highdim/test_p76_generated_corrected_metric_diagnostic.py`.
- These reads informed the Phase 3 implementation-surface draft but did not
  modify code or run training.

Documentation checks:

```bash
rg -n "P_theta|parameter count|rank|degree|basis|trainable mask|recompute|1656|33120|40960|20P|budget arithmetic|evidence gate|non-evidence|mechanics smoke" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-subplan-2026-06-19.md
rg -n "learning rate|batch count|validation stopping|selection protocol|audit exclusion|replay veto|untrained UKF baseline|comparator|corrected validation CE|random|calibrated-constant|source-prefit" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-subplan-2026-06-19.md
rg -n "wrong baselines|proxy metrics|missing stop conditions|unfair comparisons|hidden assumptions|stale context|environment mismatch|artifact adequacy|under-budget mechanics smokes" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-execution-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-claude-review-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-stop-handoff-2026-06-19.md
```

Results:

- Phase 2/Phase 3 parameter-count and budget coverage checks passed.
- Phase 2/Phase 3 tuning, comparator, audit-exclusion, replay, and
  failed-route fence checks passed.
- Phase 2 skeptical-audit coverage checks passed.
- `git diff --check` passed for the P77 Phase 2 touched artifacts.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 2 and advance to Phase 3 scoped code edits | Local checks pass and Claude agrees after bookkeeping repair | No Phase 2 action crossed into implementation/training | Phase 3 must implement the surface without accidentally running evidence or changing defaults | Execute only the scoped P77 runner/test implementation after Claude agrees the governance patch | No training improvement, no training-run approval, no lower-gate repair, no validation/HMC readiness |

## Claude Execution Review

- `p77-phase2-execution-review-r1` returned `VERDICT: BLOCK`.
- Claude agreed the substantive Phase 2/Phase 3 content passed: Phase 2 stayed
  docs-only; \(P_\theta\) source/recompute rule and arithmetic are correct;
  tuning is predeclared, validation-only, and not post-hoc; replay and audit
  roles are clear; failed random, calibrated-constant, and source-prefit
  routes remain fenced; and local checks are recorded.
- Claude blocked only on stale review-ledger top-level status.
- Patched the review ledger to record the R1 blocker and repair.
- `p77-phase2-execution-review-r2` returned `VERDICT: AGREE`.
- Claude agreed the bookkeeping blocker was repaired and no new state mismatch
  blocks closing Phase 2.

## Phase 3 Handoff

Phase 3 should create the implementation-surface plan for a P77 runner and
tests.  It should reuse the P76 UKF-frame and corrected-metric surfaces, add
parameter-count/budget manifests, corrected validation/replay/audit reporting,
and fail-closed fences for under-budget evidence and failed historical routes.
Scoped implementation-code edits in Phase 3 are governed by the reviewed
subplan and Claude review, not by a separate human approval, provided they do
not run training evidence or cross GPU/network/default/large-run/destructive
boundaries.
