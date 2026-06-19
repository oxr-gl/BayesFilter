# P76 Phase 7 v2 Result: Corrected Fit-Diagnostic Protocol

metadata_date: 2026-06-18
status: PHASE7V2_CLAUDE_AGREE_READY_FOR_PHASE8
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6b-corrected-evidence-contract-result-2026-06-18.md
next_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-subplan-2026-06-18.md
phase: 7
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Scope

Phase 7 v2 executed the reviewed docs/protocol-only diagnostic-planning phase.
It did not edit implementation code, generate new samples, run a diagnostic,
tune hyperparameters, use GPU/CUDA, use network, change defaults, revive
source-prefit, or make fit-quality/lower-gate claims.

## Result

The smallest justified next action is Phase 8: design and implement, under a
separate reviewed subplan, an opt-in corrected heldout metric surface for the
P76 lane.  The current P76/P75 training helper computes
\[
  \alpha_i \propto w_i(s_i^2+\tau q_0(z_i)),
\]
which remains part of the historical Phase 6 training trace but is not the
approved primary heldout metric.

The future Phase 8 surface must compute the target-only heldout metric
\[
  u_i=s_i^2,\qquad
  \alpha_i^B=\frac{w_i u_i}{\sum_j w_j u_j},
\]
and
\[
  \mathcal L_B(\theta)
  =
  -\sum_i\alpha_i^B\log\rho_\theta(z_i)+\log Z_\theta .
\]

Phase 8 must be opt-in and must preserve the existing helper boundary.  It may
add implementation and tests only after its reviewed subplan permits them.

## Diagnostic Surface Required For Phase 8

Phase 8 should define an artifact that can evaluate a trained or initialized
P76 `TrainableFunctionalTT` or compatible density snapshot on a generated
target batch with fields:

- `points`: local coordinates \(z_i\), conventionally shaped like
  `P75ObjectiveBatch.points`;
- `target_values`: shifted square-root target values \(s_i\);
- `weights`: target-generator weights \(w_i\);
- `role`: one of `train`, `validation`, or `audit/test`;
- provenance fields for seed, frame hash, construction label, and disjointness.

The opt-in metric surface must report:

- target-only mass \(M_B=\sum_i w_i s_i^2\);
- target-only alpha min/max/sum and effective sample size;
- heldout cross-entropy
  \(-\sum_i\alpha_i^B\log\rho_\theta(z_i)+\log Z_\theta\);
- finite flags for target mass, alpha, rho, normalizer, log density, and loss;
- veto reasons for nonfinite or nonpositive target mass, invalid weights,
  invalid target values, audit leakage, role misuse, or use of the old helper
  alpha as the primary heldout metric;
- secondary diagnostics only: raw square-root residual, optimal-scale
  square-root residual, and centered log-shape residual.

Secondary residuals must remain explanatory.  Raw or sign/scale-adjusted
square-root residuals must not become promotion metrics.

## Train/Validation/Audit Protocol

Any later substantive training or fit-quality pilot must declare before
execution:

- train stream, validation stream, and audit/test stream with disjoint seeds;
- finite candidate set for learning rate, regularization, gradient clipping,
  batch size, batch count, degree, rank, validation cadence, and stopping rule;
- validation-selection rule based on the corrected density-aligned validation
  metric;
- one-touch audit/test rule;
- instability vetoes for nonfinite loss, gradient, rho, normalizer, log
  density, invalid target mass, or audit leakage.

For degree `2`, rank `4`, dimension `36`, the raw trainable parameter count is
`1656`.  Any substantive fit-quality pilot for this setting needs at least
`16560` training samples.  This `10 N_theta` rule is a minimum necessary
condition, not a sufficient condition for validation, scaling, HMC readiness,
or final rank/sample policy.

## Phase 8 Handoff

Phase 8 should be titled `Corrected Heldout Metric Surface`.  It may be an
implementation phase only if the user approves the scoped implementation edits
after reviewing the Phase 8 subplan.

Phase 8 must not:

- run a training pilot;
- generate new diagnostic samples except tiny synthetic/unit-test fixtures;
- use GPU/CUDA;
- install or fetch packages;
- use network;
- change defaults;
- revive source-prefit as a live repair method;
- use audit/test samples for training, stopping, hyperparameter selection, or
  metric selection;
- claim lower-gate repair, validation readiness, HMC readiness, scaling,
  source-faithfulness, final rank/sample policy, UKF success, or UKF rejection.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Draft Phase 8 corrected heldout metric surface subplan | Passed locally pending Claude review: Phase 7 v2 stayed docs-only and produced a bounded next subplan | No implementation edits, new samples, diagnostics, tuning, GPU/CUDA, network, default changes, source-prefit revival, or fit-quality claims | Whether the existing code can support the corrected metric cleanly with a small opt-in helper and focused tests | Review this result and Phase 8 subplan with Claude; if agreed, request/confirm approval for Phase 8 implementation edits before executing them | No fit-quality result, no algorithmic success/rejection, no lower-gate repair, no validation/HMC readiness, no scaling, no final rank/sample policy |

## Local Checks

Actual local checks:

```bash
rg -n "docs-only|density-aligned heldout|alpha_i|target-only|not approved primary heldout metric|train/validation/audit|minimum necessary|no implementation edits|no new diagnostic|finite candidate set|predeclared|stopping rule|s_i\\^2\\+\\tau q0|reviewed target bridge" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-result-v2-2026-06-18.md
rg -n "Corrected Heldout Metric Surface|target-only|weighted_empirical_cross_entropy_weights|finite candidate set|source-prefit revival|no training pilot|no GPU" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-subplan-2026-06-18.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-result-v2-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-stop-handoff-2026-06-18.md
```

Result:

- Phase 7 v2 result contains the docs-only, target-only, helper-boundary,
  train/validation/audit, minimum necessary, finite candidate set,
  predeclared, stopping-rule, and reviewed target-bridge terms.
- Phase 8 subplan contains the corrected heldout metric surface, target-only,
  old-helper boundary, finite candidate set, source-prefit revival, no training
  pilot, and no-GPU terms.
- Runbook, execution ledger, review ledger, stop handoff, and master program
  contain Phase 7 v2 / Phase 8 routing and review-pending status.
- `git diff --check` passed for tracked touched files.  A trailing-whitespace
  scan across touched new and tracked files produced no hits.

## Claude Subplan Review

Claude reviewed the Phase 7 v2 subplan before execution and returned
`VERDICT: AGREE` with no material blockers.

Claude verified that Phase 7 v2 is docs/protocol-only, preserves target-only
heldout density cross-entropy, keeps the helper-alpha boundary explicit,
retains the sample-to-parameter rule as necessary not sufficient, preserves
train/validation/audit separation and predeclared tuning, and gives a bounded
Phase 8 gate with separate approval for edits/runs/target changes.

## Next Step

Claude execution review returned `VERDICT: AGREE` with no material blockers.

Phase 7 v2 is closed.  The next eligible step is Phase 8 under:

- `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-subplan-2026-06-18.md`

Phase 8 includes scoped implementation edits only if approved under its
reviewed subplan.  It must preserve the helper-boundary and tuning-boundary
language from this result and the Phase 8 subplan.
