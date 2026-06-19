# P77 Phase 1 Result: Objective, Split, And Leakage Contract

metadata_date: 2026-06-19
status: PHASE1_CLAUDE_AGREE_READY_FOR_PHASE2
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-subplan-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase0-boundary-reset-result-2026-06-19.md
phase: 1
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Summary

Phase 1 freezes the objective, data roles, comparator, and leakage contract for
P77 before any implementation or training phase.

Phase 1 is design-only.  It did not edit implementation code, construct an
optimizer, call `train_step`, generate samples, tune hyperparameters, run a
training diagnostic, use GPU/CUDA, use network, install packages, or change
defaults.

The live P77 question is not whether the P75 failed routes can be improved.
Random initialization, calibrated-constant initialization, and source-route
prefit remain failed historical routes only.  They are not live routes,
baselines, comparators, fallback candidates, tuning anchors, or promotion
references.

The only live comparator for training evidence is the UKF-initialized untrained
TT candidate evaluated on the same corrected target-only heldout CE and the
same data-role definitions.

This is the Phase 1 validation metric and forbidden leakage contract: corrected
target-only heldout CE is the validation metric for fit quality, audit is final
only, and there is no under-budget evidence route.

## Mathematical Contract

The trainable density remains
\[
  q_\theta(z)
  =
  \frac{\rho_\theta(z)}{Z_\theta},
  \qquad
  \rho_\theta(z)
  =
  h_\theta(z)^2+\tau q_0(z),
  \qquad
  Z_\theta
  =
  \int \rho_\theta(z)\,dz .
\]

Here \(h_\theta\) is the trainable fixed-branch square-root TT, \(q_0\) is the
defensive reference density, and \(\tau q_0\) is a positive density floor.  The
normalizer \(Z_\theta\) is computed from the squared TT normalizer plus the
defensive mass contribution.

### Training Objective

The current stochastic training surface is represented by `P75ObjectiveBatch`
and `TrainableFunctionalTT.objective()`.  For a generated training batch
\[
  B_{\rm train}=\{(z_i,s_i,w_i)\}_{i=1}^m,
\]
with target square-root values \(s_i\), integration weights \(w_i\), and
defensive density values \(q_0(z_i)\), the implemented training weights are
\[
  \alpha_i^{\rm train}
  =
  \frac{w_i\{s_i^2+\tau q_0(z_i)\}}
       {\sum_j w_j\{s_j^2+\tau q_0(z_j)\}} .
\]

The per-batch stochastic loss is
\[
  \widehat{\mathcal L}_{\rm train}(\theta;B_{\rm train})
  =
  -\sum_i \alpha_i^{\rm train}\log\rho_\theta(z_i)
  +\log Z_\theta
  +R(\theta),
\]
where \(R(\theta)\) is the configured regularization term.  In the current
code surface, \(R(\theta)\) may include configured L2 and log-normalizer-anchor
terms when their weights are nonzero.

This loss is allowed to drive optimization in later phases, but it is not the
primary fit-quality metric.  It includes the defensive \(\tau q_0\) helper in
the empirical training measure, so it cannot substitute for the corrected
target-only heldout CE.

### Corrected Validation Metric

For any non-training evaluation cloud
\[
  B_{\rm eval}=\{(z_i,s_i,w_i)\}_{i=1}^n,
\]
the corrected target-only weights are
\[
  \alpha_i^{\rm eval}
  =
  \frac{w_i s_i^2}{\sum_j w_j s_j^2}.
\]

The primary fit metric is
\[
  \widehat{\mathcal L}_{\rm eval}(\theta)
  =
  -\sum_i \alpha_i^{\rm eval}\log\rho_\theta(z_i)
  +\log Z_\theta.
\]

This is implemented by `P76CorrectedHeldoutMetricBatch` and
`TrainableFunctionalTT.corrected_heldout_density_metric()`.  The metric is
target-only because \(\alpha_i^{\rm eval}\) does not contain the defensive
\(\tau q_0\) helper.

## Data Roles

P77 uses four disjoint roles:

| Role | Use | May tune or select? | Counts toward \(N_{\rm train}\)? |
| --- | --- | --- | --- |
| Training | Fresh generated mini-batches used by the optimizer. | No direct promotion; drives gradients only. | Yes. |
| Validation | Corrected CE for learning-rate, batch-count, stopping, and candidate selection. | Yes, under a predeclared Phase 2/5 protocol. | No. |
| Replay | Fixed robustness diagnostic using corrected CE after validation choices. | May veto only if Phase 2 says so; otherwise explanatory. | No. |
| Audit | Final-only corrected CE check after all choices are frozen. | Never. | No. |

Audit samples may not choose hyperparameters, stopping time, rank, degree,
sample count, learning rate, optimizer settings, candidate selection,
thresholds, or post-hoc interpretation rules.

Validation, replay, and audit must use corrected target-only CE on
`P76CorrectedHeldoutMetricBatch`-style batches.  Training batches may use
`P75ObjectiveBatch` and the stochastic training objective, but training loss is
not a promotion metric.

## Comparator

The comparator is
\[
  \theta_0=\theta_{\rm UKF},
\]
the UKF-initialized untrained TT candidate from the P76 lane, evaluated without
optimizer steps on the same corrected validation, replay, and audit role
definitions as any trained candidate.

Training evidence may compare only against this UKF-initialized untrained
candidate unless a later reviewed phase explicitly adds a scientifically valid
comparator.  The failed random, calibrated-constant, and source-prefit routes
remain historical context only.

## Training Budget Rule

No P77 run may be interpreted as fixed-branch regression or training evidence
unless
\[
  N_{\rm train}\ge20P_\theta.
\]

For the current degree-2/rank-4/d=36 candidate,
\[
  P_\theta
  =
  1\cdot3\cdot4
  +
  34\cdot4\cdot3\cdot4
  +
  4\cdot3\cdot1
  =
  1656,
\]
so the hard minimum is
\[
  20P_\theta=33120.
\]

With batch size 1024, the first proper budget should use at least 33 fresh
training batches.  P77's preferred first proper budget remains `1024 x 40 =
40960` fresh training samples.  Validation, replay, and audit samples do not
count toward \(N_{\rm train}\).

Under-budget mechanics smokes may be used only for wiring.  They cannot tune,
select, promote, or support a training-evidence claim.

## Leakage Rules

- Training, validation, replay, and audit roles must be seed-disjoint and
  provenance-disjoint.
- Audit is final-only and cannot be inspected to tune or select.
- Replay cannot become a hidden validation set unless the Phase 2 protocol
  predeclares a veto-only role.
- Training loss, raw square-root residuals, centered log-shape RMS, alpha ESS,
  runtime, and P76 CE values are explanatory or veto diagnostics only.
- The corrected validation CE is the primary fit-quality surface before audit.
- Random, calibrated-constant, and source-prefit routes are failed historical
  routes, not live routes.
- A later phase must stop if it cannot preserve \(N_{\rm train}\ge20P_\theta\)
  for evidence.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | What objective and data split must govern P77 training so later evidence cannot be contaminated by proxy metrics or leakage? |
| Exact baseline/comparator | The UKF-initialized untrained TT evaluated with corrected target-only CE on the same validation/replay/audit role definitions. |
| Primary criterion | Passed locally pending Claude review: Phase 1 freezes the training objective, corrected validation CE, replay role, audit final-only rule, seed/data-role rules, comparator, failed-route fences, and nonclaim boundaries before training. |
| Veto diagnostics | No role split missing; audit excluded from tuning/selection/stopping; training loss not primary fit quality; raw residuals not pass criterion; random/calibrated-constant/source-prefit not revived; no under-budget evidence allowed; no implementation/training action occurred. |
| Explanatory only | Possible optimizer/hyperparameter families, P76 CE values, mechanics-smoke roles, and training-loss behavior. |
| What will not be concluded | No training improvement, no hyperparameter choice, no budget approval, no implementation surface, no lower-gate repair, no validation/HMC readiness, no scaling, no source-faithful Zhao--Cui claim. |
| Artifact preserving result | This Phase 1 result and the drafted Phase 2 budget/tuning protocol subplan. |

## Skeptical Plan Audit

| Checklist item | Phase 1 answer |
| --- | --- |
| wrong baselines | The only live comparator is the UKF-initialized untrained candidate. Random, calibrated-constant, and source-prefit remain failed historical routes. |
| proxy metrics | Training loss, raw residuals, replay values, mechanics smokes, and P76 CE values cannot become promotion criteria. |
| missing stop conditions | Audit leakage, under-budget evidence, implementation/training action, weakened \(20P_\theta\), or unconverged Claude review stop the phase. |
| unfair comparisons | Trained and untrained candidates must use the same corrected CE formula and the same validation/replay/audit role definitions. |
| hidden assumptions | \(P_\theta\), budget arithmetic, role split, comparator, and audit exclusion are made explicit before training. |
| stale context | P76 Phase 10 is metric plumbing and prerequisite context, not training evidence. |
| environment mismatch | Phase 1 is docs-only and does not depend on CPU/GPU, generated samples, optimizer state, package state, or network state. |
| artifact adequacy | This result and the Phase 2 subplan contain enough constraints to prevent arbitrary tuning or under-budget promotion. |
| under-budget mechanics smokes | Any later smoke below \(20P_\theta\) is mechanics-only and cannot tune, select, promote, or support evidence. |

## Artifacts

- Phase 1 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-subplan-2026-06-19.md`
- Phase 2 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-subplan-2026-06-19.md`
- P77 master program:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md`
- P77 runbook:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md`
- P77 execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-execution-ledger-2026-06-19.md`
- P77 Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-claude-review-ledger-2026-06-19.md`
- P77 stop handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-stop-handoff-2026-06-19.md`

## Local Checks

Prechecks:

```bash
rg -n "PHASE0|20P|33120|40960|corrected heldout CE|UKF-initialized untrained|not training evidence|audit final" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase0-boundary-reset-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
rg -n "P76CorrectedHeldoutMetricBatch|corrected_heldout_density_metric|P75ObjectiveBatch|weighted_empirical_cross_entropy_weights|train_step|make_adam_optimizer" bayesfilter/highdim/stochastic_density_training.py
```

Results:

- P77 boundary/status precheck passed.
- Local training/metric code-symbol precheck passed.

Documentation checks:

```bash
rg -n "training loss|validation metric|replay|audit final|corrected target-only|UKF-initialized untrained|20P|no under-budget|forbidden leakage|Phase 2|random|calibrated-constant|source-prefit|failed historical routes|not live routes" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-subplan-2026-06-19.md
rg -n "P_theta|parameter count|rank|degree|budget arithmetic|evidence gate|non-evidence|validation stopping|selection protocol|audit exclusion|untrained UKF baseline|comparator" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-subplan-2026-06-19.md
rg -n "wrong baselines|proxy metrics|missing stop conditions|unfair comparisons|hidden assumptions|stale context|environment mismatch|artifact adequacy|under-budget mechanics smokes" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-result-2026-06-19.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-execution-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-claude-review-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-stop-handoff-2026-06-19.md
```

Results:

- Phase 1/Phase 2 coverage checks passed after a wording repair that moved
  required terms into substantive contract text rather than only command
  blocks.
- Phase 2 parameter-count, budget, tuning, audit-exclusion, and comparator
  coverage checks passed.
- Phase 1 skeptical-audit coverage checks passed.
- `git diff --check` passed for the P77 Phase 1 touched artifacts.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 1 and advance to Phase 2 | Local checks pass and Claude agrees | No Phase 1 action crossed into implementation/training | Phase 2 must make budget/tuning choices operational without arbitrary parameters | Execute Phase 2 only under the reviewed design-only subplan | No training improvement, no hyperparameter choice, no implementation approval, no lower-gate repair, no validation/HMC readiness |

## Claude Execution Review

- `p77-phase1-execution-review-r1` returned `VERDICT: AGREE`.
- Claude agreed Phase 1 stayed docs-only.
- Claude agreed the mathematics are coherent: the training objective uses
  defensive-mixture empirical weights, while corrected validation CE uses
  target-only weights \(\alpha_i^{\rm eval}\propto w_i s_i^2\).
- Claude agreed training/validation/replay/audit roles and audit final-only
  leakage fences are explicit.
- Claude agreed random, calibrated-constant, and source-prefit routes remain
  failed historical routes, not live baselines/comparators/fallbacks.
- Claude agreed \(P_\theta=1656\), \(20P_\theta=33120\), and preferred first
  proper budget `1024 x 40 = 40960` are preserved.
- Claude agreed local checks are recorded and the Phase 2 subplan is adequate
  to execute as a design-only phase.

## Phase 2 Handoff

Phase 2 should turn this contract into an operational parameter-count, budget,
and tuning protocol.  It must freeze how \(P_\theta\) is counted, how
\(20P_\theta\) is enforced, how learning-rate/batch-count/stopping choices are
made from validation only, whether replay can veto, and how audit remains
final-only.
