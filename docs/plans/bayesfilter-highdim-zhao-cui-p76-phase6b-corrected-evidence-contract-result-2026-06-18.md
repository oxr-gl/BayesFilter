# P76 Phase 6b Result: Corrected Evidence Contract

metadata_date: 2026-06-18
status: PHASE6B_CLAUDE_AGREE_READY_FOR_PHASE7V2
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6b-corrected-evidence-contract-subplan-2026-06-18.md
superseded_phase7_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-2026-06-18.md
next_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md
phase: 6b
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Scope

Phase 6b corrects the post-Phase-6 evidence contract before any further P76
fit diagnostic is executed.

Phase 6 remains valid as mechanics-only evidence: the UKF-frame bridge passed,
the CPU-only mini-batch loop completed, fresh training batches were used, and
finite training quantities were recorded.  Phase 6 is not valid as
learning-capacity or fit-quality evidence.  It used `128 * 20 = 2560` fresh
training samples for `1656` raw TT parameters, about `1.55` samples per
parameter, and its inherited audit metric was a raw square-root residual.

## Corrective Decision

The original Phase 7 draft is superseded and must not be executed:

- `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-2026-06-18.md`

It now contains the literal revocation marker:

- `SUPERSEDED_BY_PHASE6B_CORRECTED_EVIDENCE_CONTRACT_DO_NOT_EXECUTE`

The only Phase 7 subplan eligible for future launch is:

- `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md`

Phase 7 v2 is a docs/protocol diagnostic-planning phase.  It does not authorize
implementation edits, new generated diagnostic artifacts, a training pilot,
tuning, GPU/CUDA, network, package installation, default changes, or a large
run.

## Corrected Metric

For an evaluation batch
\[
  B=\{(z_i,w_i,s_i)\}_{i=1}^n,
\]
where \(z_i\) are local coordinates, \(w_i\) are target-generator weights, and
\(s_i\) are shifted square-root target values, define
\[
  u_i=s_i^2,\qquad
  \alpha_i^B=\frac{w_i u_i}{\sum_j w_j u_j}.
\]

The model is
\[
  \rho_\theta(z)=h_\theta(z)^2+\tau q_0(z),
  \qquad
  p_\theta(z)=\rho_\theta(z)/Z_\theta .
\]

The primary density-aligned heldout metric for future fit-quality
interpretation is
\[
  \mathcal L_B(\theta)
  =
  -\sum_i\alpha_i^B\log\rho_\theta(z_i)+\log Z_\theta.
\]

The target weights \(\alpha_i^B\) must be computed from the heldout target
batch only.  They must not depend on \(h_\theta\), \(\rho_\theta\),
\(Z_\theta\), validation loss, training loss, audit/test outcomes, or any
post-hoc model term.

## Current Helper Boundary

The current helper
`TrainableFunctionalTT.weighted_empirical_cross_entropy_weights` computes
\[
  \alpha_i \propto w_i(s_i^2+\tau q_0(z_i)).
\]

That helper may remain part of the historical Phase 6 training trace, but it is
not the approved primary heldout metric for Phase 7 v2 because it mixes target
mass with model-floor mass.

## Sample-To-Parameter Rule

For a tensor train with basis degree \(p\), dimension \(d\), and ranks
\((r_0,\ldots,r_d)\),
\[
  N_\theta=\sum_{j=1}^d r_{j-1}(p+1)r_j.
\]

For degree `2`, rank `4`, and dimension `36`,
\[
  N_\theta
  =
  1\cdot3\cdot4
  +34\cdot4\cdot3\cdot4
  +4\cdot3\cdot1
  =1656.
\]

Any substantive fit-quality pilot at this degree/rank must satisfy
\[
  N_{\rm train}\ge 10N_\theta=16560.
\]
This is a minimum necessary condition for fit-quality claims, not a sufficient
condition for validation, scaling, HMC readiness, or final rank/sample policy.

## Required Future Split

Future P76 fitting phases must keep separate:

- `train`: fresh generated batches used for gradient updates;
- `validation`: generated batches used for learning-rate, regularization,
  clipping, batch-size, and early-stopping selection;
- `audit` or `test`: generated batches touched once after selection for the
  reported density-aligned heldout result.

No audit/test sample may be used for training, stopping, hyperparameter
selection, or metric selection.

## Hyperparameter Rule

No learning-rate, regularization, gradient clip, degree, rank, batch-size,
batch count, validation cadence, or stopping rule may be arbitrary in a future
fitting phase.  Each must be either inherited from a reviewed mechanics
default, predeclared in a finite candidate set with a stated reason, or marked
exploratory with no promotion claim.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Reclassify Phase 6 as mechanics-only and replace the Phase 7 gate with Phase 7 v2 | Passed locally pending Claude review: result, legacy revocation, and Phase 7 v2 subplan were drafted | No new pilot, implementation edit, GPU/CUDA, network, package install, default change, or source-prefit revival occurred | Whether later code has the metric surface needed to compute the corrected heldout objective without using the old helper | Send Phase 6b execution artifacts to Claude; if agreed, Phase 7 v2 may begin as a docs/protocol planning phase | No UKF success/rejection, no fit-quality claim, no lower-gate repair, no validation/HMC readiness, no scaling, no final rank/sample policy |

## Local Checks

Actual local checks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json
rg -n "mechanics-only|density-aligned heldout|alpha|10 N|16560|train/validation/audit|predeclared hyperparameter|no implementation code edits|Phase 7 v2" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6b-corrected-evidence-contract-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md
rg -n "SUPERSEDED_BY_PHASE6B_CORRECTED_EVIDENCE_CONTRACT_DO_NOT_EXECUTE" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-2026-06-18.md
rg -n "docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-2026-06-18.md
rg -n "PHASE6B|phase6b|Phase 6b|Phase 7 v2" docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-stop-handoff-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6b-corrected-evidence-contract-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6b-corrected-evidence-contract-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-stop-handoff-2026-06-18.md
```

Result:

- Phase 6 JSON parsed.
- Corrected metric, sample-budget, split, tuning, and Phase 7 v2 terms were
  found in the Phase 6b result and Phase 7 v2 subplan.
- The legacy Phase 7 file contains the literal supersession marker.
- The legacy Phase 7 file contains the exact successor v2 path.
- Runbook, execution ledger, review ledger, and stop handoff contain Phase 6b
  or Phase 7 v2 routing terms.
- `git diff --check` on the existing tracked files passed.  New untracked
  files were additionally checked for trailing whitespace with `rg -n
  "[ \\t]+$"` and produced no hits.

## Claude Subplan Review

Claude reviewed the Phase 6b subplan through four bounded read-only rounds.

- R1: `VERDICT: REVISE/BLOCK`; blockers were current-helper alpha mismatch,
  missing visible revocation of old Phase 7, and loose language about bounded
  new diagnostic artifacts.
- R2: `VERDICT: REVISE/BLOCK`; blocker was that revocation was required but
  not operationally checked.
- R3: `VERDICT: REVISE/BLOCK`; blocker was that the revocation check could
  pass by matching `Phase 7 v2` without the literal marker.
- R4: `VERDICT: AGREE`; no material blockers.

## Next Step

Claude execution review returned `VERDICT: AGREE` with no material blockers.

Phase 6b is closed.  The next eligible step is Phase 7 v2 under:

- `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md`
