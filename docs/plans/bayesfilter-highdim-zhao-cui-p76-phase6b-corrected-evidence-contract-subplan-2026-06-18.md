# P76 Phase 6b Subplan: Corrected Evidence Contract

metadata_date: 2026-06-18
status: DRAFT_CLAUDE_REVIEW_PENDING
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-result-2026-06-18.md
supersedes_draft_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-2026-06-18.md
phase: 6b
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Correct the P76 post-Phase-6 evidence contract before any further fitting
diagnostic or larger run.

Phase 6 remains valid as mechanics evidence: the UKF-frame bridge passed, the
CPU-only mini-batch loop completed, fresh training batches were used, and
finite training quantities were recorded.  Phase 6 must not be used as
learning-capacity evidence because its effective sample budget and audit metric
were not scientifically adequate for that claim.

Phase 6b is documentation/protocol correction only.  It must produce an
erratum/result note and a corrected Phase 7 subplan.  It must not edit
implementation code, run a new pilot, tune hyperparameters, or reinterpret the
Phase 6 residuals as a lower-gate decision.

## Entry Conditions Inherited From Phase 6

Phase 6b may begin only after:

- the Phase 6 result exists and records
  `CLAUDE_AGREE_PHASE6_CLOSED_READY_FOR_PHASE7`;
- the Phase 6 pilot JSON exists and parses;
- the UKF-frame bridge passed;
- the Phase 6 run completed `20` fresh batches of size `128`;
- Phase 6 records raw TT parameter count `1656` for degree `2`, rank `4`,
  dimension `36`;
- Phase 6 records that audit square-root residuals are explanatory only under
  the Phase 6 evidence contract;
- Claude agreed the Phase 6 implementation/result after the R3 repair;
- no Phase 7 execution has started.

## Required Artifacts

Phase 6b must produce:

- Phase 6b result/erratum:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6b-corrected-evidence-contract-result-2026-06-18.md`;
- corrected Phase 7 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md`;
- visible revocation of the earlier "Phase 7 may begin" handoff under
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-2026-06-18.md`
  by adding the literal status marker
  `SUPERSEDED_BY_PHASE6B_CORRECTED_EVIDENCE_CONTRACT_DO_NOT_EXECUTE`;
- updates to:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md`,
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md`,
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md`,
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-stop-handoff-2026-06-18.md`;
- if needed, a master-program status update only.  Phase 6b must not rewrite
  the P76 scientific objective or erase the prior Phase 6 result.

## Required Checks/Tests/Reviews

Pre-execution checks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json
rg -n "CLAUDE_AGREE_PHASE6_CLOSED_READY_FOR_PHASE7|raw TT core parameters|1656|total fresh training draws seen|audit square-root residuals|explanatory only" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-result-2026-06-18.md
rg -n "weighted_empirical_cross_entropy_weights|raw = batch.weights|target_values|tau \\* q0|weighted_empirical_cross_entropy" bayesfilter/highdim/stochastic_density_training.py
```

Subplan review:

- Send this Phase 6b subplan to Claude for read-only review.
- Loop repair to convergence or max five rounds for the same material blocker.
- Claude may review consistency, correctness, feasibility, artifact coverage,
  and boundary safety only; Claude is not an execution authority.

Execution checks:

```bash
rg -n "mechanics-only|density-aligned heldout|alpha|10 N|16560|train/validation/audit|predeclared hyperparameter|no implementation code edits|Phase 7 v2" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6b-corrected-evidence-contract-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md
rg -n "SUPERSEDED_BY_PHASE6B_CORRECTED_EVIDENCE_CONTRACT_DO_NOT_EXECUTE" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-2026-06-18.md
rg -n "Phase 7 v2" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-2026-06-18.md
rg -n "PHASE6B|phase6b|Phase 6b|Phase 7 v2" docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-stop-handoff-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6b-corrected-evidence-contract-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6b-corrected-evidence-contract-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-stop-handoff-2026-06-18.md
```

Execution review:

- Send the Phase 6b result, legacy Phase 7 revocation, Phase 7 v2 subplan, and
  ledger/runbook updates to Claude for read-only execution review.
- Repair fixable documentation/protocol issues visibly and rerun focused
  checks.

## Corrected Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | What evidence contract must govern P76 after the Phase 6 mechanics pilot, so that future fitting diagnostics answer density-learning questions without repeating the underpowered and metric-misaligned Phase 6 interpretation? |
| Exact baseline/comparator | Phase 6 mechanics result and JSON only. Historical P75 failures remain boundary context, not live candidate methods. |
| Primary criterion | Produce a reviewed erratum and Phase 7 v2 subplan that reclassify Phase 6 as mechanics-only, define a density-aligned heldout objective, impose sample-to-parameter minimums for any fit-quality claim, require train/validation/audit separation, and require predeclared tuning before audit/test use. |
| Diagnostics that can veto Phase 6b | Missing Phase 6 parse/tieout; treating raw square-root residual as primary density criterion; using audit samples for training/tuning; allowing arbitrary heldout weights or post-hoc hyperparameters; authorizing a new pilot; editing implementation code; claiming lower-gate repair, validation readiness, HMC readiness, scaling, or source-faithfulness. |
| Explanatory only | The already observed Phase 6 loss trace, gradient norm, rho range, normalizer, square-root audit residuals, and line diagnostic. |
| What will not be concluded | Phase 6b does not prove the UKF warm start works, does not reject it, does not tune the method, does not choose final degree/rank/sample policy, and does not authorize a large run. |
| Artifact preserving result | Phase 6b result/erratum and Phase 7 v2 subplan. |

## Corrected Mathematical Evaluation Protocol

For an evaluation batch
\[
  B=\{(z_i,w_i,s_i)\}_{i=1}^n,
\]
where \(z_i\) are fixed local coordinates, \(w_i\ge0\) are the
target-generator quadrature/Monte-Carlo weights, and \(s_i\) are the shifted
square-root target values already emitted by the target generator, define
\[
  u_i=s_i^2,\qquad
  \alpha_i^B=\frac{w_i u_i}{\sum_{j=1}^n w_j u_j}.
\]

This is not an arbitrary model-dependent choice.  It is the empirical target
measure for the declared density target
\[
  p_\star(z) \propto u(z).
\]
The model is
\[
  \rho_\theta(z)=h_\theta(z)^2+\tau q_0(z),
  \qquad
  p_\theta(z)=\rho_\theta(z)/Z_\theta .
\]
The primary heldout metric for density fit is the target-measure
cross-entropy estimate
\[
  \mathcal L_B(\theta)
  =
  -\sum_i \alpha_i^B\log \rho_\theta(z_i)
  + \log Z_\theta .
\]

Rules:

- \(\alpha_i^B\) must be computed from the heldout target batch only.
- \(\alpha_i^B\) must not use \(h_\theta\), \(\rho_\theta\), \(Z_\theta\),
  training loss, validation loss, or audit/test outcomes.
- \(\tau q_0\) is a model floor in \(\rho_\theta\), not target mass for the
  primary heldout metric.  A future run may choose a defensive-mixture target
  only if a reviewed plan declares that different scientific target before
  execution.
- If \(\sum_j w_j u_j\le0\), nonfinite, or dominated by invalid target values,
  the batch is invalid and the run is vetoed; no fallback target weights may be
  invented after seeing results.

Secondary diagnostics may include:

\[
  \min_a\sum_i w_i(a\,h_\theta(z_i)-s_i)^2
\]

and the centered log-shape residual
\[
  r_i=\log \rho_\theta(z_i)-\log u_i-c^\star,
\]
where \(c^\star\) is the weighted constant that minimizes the chosen heldout
log residual.  These diagnostics may explain sign, scale, and shape mismatch,
but they are not the primary density-fit criterion.  Post-hoc sign/scale
adjusted square-root residuals must not be promoted to pass/fail or
fit-quality promotion metrics.

## Sample-To-Parameter Rule

For a tensor train with basis degree \(p\), dimension \(d\), and ranks
\((r_0,\ldots,r_d)\), the raw trainable parameter count is
\[
  N_\theta=\sum_{j=1}^d r_{j-1}(p+1)r_j.
\]

For the Phase 6 degree-2, rank-4, 36-dimensional run,
\[
  N_\theta = 1\cdot 3\cdot 4
  + 34\cdot 4\cdot 3\cdot 4
  + 4\cdot 3\cdot 1
  = 1656.
\]

The Phase 6 run used
\[
  N_{\rm train}=128\cdot 20=2560,
\]
or about \(1.55\) fresh training samples per raw parameter.  This is below the
user-declared minimum standard of \(10\) samples per parameter for any
fit-quality claim.

Operational rule:

- A mechanics smoke may use fewer samples, but then it may claim mechanics
  only.
- Any substantive fit-quality pilot for this degree/rank must satisfy
  \[
    N_{\rm train}\ge 10N_\theta = 16560.
  \]
  This is a minimum necessary condition for a fit-quality claim, not a
  sufficient condition for validation, scaling, or HMC readiness.
- Any validation set used for hyperparameter selection must also be generated
  before selection and must have its exact size justified in the reviewed plan.
- Any final audit/test set must be generated independently, touched once after
  hyperparameter/early-stopping selection, and must have its exact size
  justified in the reviewed plan.
- A larger Neutra-scale budget may be scientifically reasonable, but Phase 6b
  does not authorize it.

## Train/Validation/Audit Split

Future P76 fitting phases must use three disjoint roles:

- `train`: fresh generated batches used for gradient updates only;
- `validation`: generated target batches used for learning-rate,
  regularization, gradient-clip, batch-size, and early-stopping selection;
- `audit` or `test`: generated target batches touched once after selection for
  the reported density-aligned heldout result.

Before moving from training/validation to final audit/test, a future phase
must check:

- every training loss used for optimization is finite;
- training loss did not fail the predeclared instability veto;
- validation density cross-entropy is finite for all candidates that remain
  eligible;
- the selected candidate is chosen only by the predeclared validation rule;
- no audit/test value has been inspected for tuning, early stopping, or metric
  selection.

## Hyperparameter Tuning Protocol

No learning-rate, regularization, clip, degree, rank, batch-size, or stopping
choice may be arbitrary in an executed fitting phase.  Each must be either:

- inherited from a previous reviewed phase as a fixed mechanics default; or
- listed before execution in a finite candidate set with a stated reason; or
- explicitly declared exploratory, in which case its results cannot be used
  for promotion.

For the immediate P76 Phase 7 v2 planning step, no tuning run is authorized.
Phase 7 v2 may only design the minimal diagnostic surface needed to compute
the corrected density-space metrics on existing Phase 6 artifacts and on
future artifacts whose generation must be separately reviewed before
execution.  Phase 7 v2 must visibly declare whether it is docs-only or whether
it proposes future implementation changes; any implementation changes remain
blocked pending a reviewed subplan and separate approval.  Any later tuning
phase must predeclare:

- candidate learning rates;
- candidate \(L^2\), log-normalizer-anchor, or other stabilizing penalties;
- candidate gradient clipping rules;
- batch size and number of batches;
- validation cadence and early-stopping rule;
- random seeds and sample-stream disjointness;
- primary validation metric;
- audit/test metric and one-touch rule;
- instability vetoes.

The audit/test metric must be the density-aligned heldout cross-entropy above
unless a reviewed plan changes the scientific target before execution.

## Forbidden Claims/Actions

- Do not edit implementation code in Phase 6b.
- Do not run a new training, diagnostic, or pilot command in Phase 6b beyond
  local documentation checks and JSON parsing.
- Do not use GPU/CUDA.
- Do not install or fetch packages.
- Do not use network.
- Do not launch detached agents.
- Do not change defaults.
- Do not revive random, calibrated constant, or source-route prefit as live
  repair candidates.
- Do not use audit/test samples for training, stopping, hyperparameter
  selection, or metric selection.
- Do not treat raw square-root residuals as the primary density-fit metric.
- Do not claim lower-gate repair, validation readiness, HMC readiness, scaling,
  source-faithfulness, or final rank/sample policy.

## Exact Next-Phase Handoff Conditions

Phase 7 v2 may begin only if:

- Phase 6b result exists and explicitly reclassifies Phase 6 as
  mechanics-only;
- Phase 6b visibly revokes the earlier handoff that Phase 7 may begin under
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-2026-06-18.md`
  with the literal marker
  `SUPERSEDED_BY_PHASE6B_CORRECTED_EVIDENCE_CONTRACT_DO_NOT_EXECUTE`;
- Phase 7 v2 subplan exists and uses the corrected density-aligned heldout
  objective as primary for fit-quality interpretation;
- Phase 7 v2 preserves raw square-root residuals as secondary/explanatory;
- Phase 7 v2 records the sample-to-parameter rule and forbids fit-quality
  promotion from the existing Phase 6 sample budget;
- Phase 7 v2 defines what it may inspect and what it may not inspect;
- local documentation checks pass;
- Claude returns `VERDICT: AGREE` on the Phase 6b execution artifacts.

## Stop Conditions

Stop and write a blocker result if:

- Phase 6 JSON cannot be parsed;
- Phase 6 result does not contain the claimed mechanics evidence;
- the corrected target-measure objective cannot be stated without ambiguity;
- Claude identifies a material issue that cannot be repaired within five
  rounds;
- executing the correction would require implementation edits, a new pilot,
  GPU/CUDA, network, package installation, or a default-policy change;
- a future phase would still permit post-hoc target weights, post-hoc
  hyperparameter tuning, audit leakage, or raw square-root residual promotion.

## Skeptical Plan Audit

Material flaw found in the existing post-Phase-6 path: the current Phase 7
draft asks the right diagnostic questions, but it does not yet operationally
bind the primary fit metric to the target density, does not freeze the
heldout target weights, does not impose the user-declared sample-to-parameter
minimum, and does not specify a tuning/validation/audit split tightly enough
to prevent post-hoc promotion.

Phase 6b repairs that planning flaw before further execution.  Because Phase
6b is docs/protocol only, its artifacts can answer the phase question without
new implementation or numerical runs.

## Current Helper Boundary

The current implementation helper
`TrainableFunctionalTT.weighted_empirical_cross_entropy_weights` computes
\[
  \alpha_i \propto w_i(s_i^2+\tau q_0(z_i)).
\]
That helper may remain part of the historical Phase 6 training trace, but it is
not the approved primary heldout metric for Phase 7 v2 because it mixes target
mass with the model-floor mass.  Phase 7 v2 may not reuse that helper as the
primary heldout metric unless a reviewed bridge explicitly changes the
scientific target before execution.  The default Phase 7 v2 primary heldout
metric must compute the target-only weights
\[
  \alpha_i^B \propto w_i s_i^2
\]
from the heldout target batch.
