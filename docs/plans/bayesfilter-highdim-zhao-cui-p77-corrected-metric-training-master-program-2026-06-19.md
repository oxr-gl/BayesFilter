# P77 Master Program: UKF-Warm-Started Corrected-Metric Training

metadata_date: 2026-06-19
status: PHASE6_LOCAL_CHECKS_PASS_PENDING_CLAUDE_REVIEW
predecessor_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
predecessor_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-result-2026-06-19.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Objective

P77 governs the next problem after P76: whether a UKF-warm-started fixed
branch can be trained with fresh mini-batches and evaluated by the corrected
target-only heldout density cross-entropy without leakage or proxy-metric
overclaim.

P77 is not a Zhao--Cui source-faithfulness program.  It is an
`extension_or_invention` fixed-variant training program that consumes the P76
prerequisites:

- true UKF-moment warm start, not source-route prefit;
- failed P75 random, calibrated-constant, and source-prefit routes fenced off;
- corrected target-only heldout density metric;
- generated-sample corrected-metric plumbing with Phase 6 bridge tieout;
- no optimizer/training leakage in the metric path.

## Central Mathematical Contract

The trainable density is
\[
  q_\theta(z)
  =
  \frac{\rho_\theta(z)}{Z_\theta},
  \qquad
  \rho_\theta(z)=h_\theta(z)^2+\tau q_0(z),
  \qquad
  Z_\theta=\int \rho_\theta(z)\,dz .
\]

For an evaluation cloud with integration weights \(w_i\) and target
square-root values \(s_i\), the primary heldout metric is
\[
  \alpha_i^{\rm eval}
  =
  \frac{w_i s_i^2}{\sum_j w_j s_j^2},
  \qquad
  \widehat{\mathcal L}_{\rm eval}(\theta)
  =
  -\sum_i \alpha_i^{\rm eval}\log \rho_\theta(z_i)+\log Z_\theta .
\]

Training may use a stochastic objective, but fit-quality promotion must use
the corrected target-only heldout CE above.  Raw square-root residuals,
training loss, bridge diagnostics, replay diagnostics, line probes, and
runtime are explanatory or veto diagnostics unless a later reviewed phase
explicitly makes them part of a frozen gate.

## Training Budget Rule

Any run interpreted as fixed-branch regression/training evidence must satisfy
the P77 training-budget rule:
\[
  N_{\rm train}
  \ge
  20\,P_\theta,
\]
where \(P_\theta\) is the number of trainable TT scalar parameters:
\[
  P_\theta
  =
  \sum_{k=1}^d r_{k-1} b_k r_k .
\]

For the current P76 candidate \(d=36\), degree \(2\) so \(b_k=3\), and rank
tuple \((1,4,\ldots,4,1)\):
\[
  P_\theta
  =
  1\cdot 3\cdot 4
  +
  34\cdot 4\cdot 3\cdot 4
  +
  4\cdot 3\cdot 1
  =
  1656 .
\]
Thus
\[
  N_{\rm train}^{\min}=20\cdot 1656=33120.
\]

With mini-batches of 1024, the minimum evidence run is
\[
  \lceil 33120/1024\rceil = 33
\]
fresh training batches.  P77's preferred first proper test budget is
`1024 x 40 = 40960` fresh training samples, which exceeds the hard minimum.
Validation, replay, and audit samples do not count toward \(N_{\rm train}\).

Small mechanics smokes may use fewer samples only if they are explicitly
non-evidence checks and cannot tune, select, or promote fit quality.

## Phase Index

Only Phase 0 is executable at master-program creation.  Each later phase must
receive a dedicated reviewed subplan before execution.

| Phase | Name | Must consume | Must produce for next phase |
| --- | --- | --- | --- |
| 0 | P76 closeout and P77 boundary reset | P76 Phase 10 result, P76 runbook/ledgers, current training/metric code surfaces | P77 boundary result and reviewed Phase 1 objective/split subplan |
| 1 | Objective, split, and leakage contract | Phase 0 result, P76 metric surface, P75/P76 training helpers | Mathematical train/eval contract, train/validation/replay/audit roles, and reviewed Phase 2 budget/tuning subplan |
| 2 | Parameter-count, budget, and tuning protocol | Phase 1 contract, current candidate rank/degree/dimension | Exact parameter-count helper or manifest, budget formulas, candidate hyperparameter protocol, and reviewed Phase 3 implementation-surface subplan |
| 3 | Implementation surface for budgeted training | Phase 2 protocol, current P76 runner/metric code | Scoped code/test plan for a P77 runner, manifests, and reviewed Phase 4 mechanics-smoke subplan |
| 4 | Tiny training mechanics smoke | Phase 3 surface/implementation | CPU-only no-evidence smoke proving optimizer/metrics/manifests wire correctly, and reviewed Phase 5 proper-test subplan |
| 5 | Proper budgeted training diagnostic design | Phase 4 mechanics result, Phase 2 budget protocol | Exact command(s) for a 20x-or-better training run, evaluation gates, runtime bounds, and required approvals |
| 6 | Budgeted corrected-metric training diagnostic | Phase 5 reviewed command and approvals | JSON/result for the 20x-or-better run, corrected heldout CE comparison to the UKF-initialized untrained candidate, and reviewed Phase 7 decision subplan |
| 7 | Decision and next-scale boundary | Phase 6 result | Decision to stop, repair objective/training, repeat with new reviewed budget, or request larger/GPU/scaling approval |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does UKF-warm-started mini-batch training improve the corrected target-only heldout density CE under enough fresh training samples and clean train/eval separation? |
| Exact baseline/comparator | The UKF-initialized untrained TT candidate evaluated by the same corrected heldout CE on the same validation/replay/audit roles. Historical P75 failures are boundary references, not live competitors. |
| Primary pass criterion | A later proper training run may pass only if it uses at least \(20P_\theta\) fresh training samples, preserves disjoint train/validation/replay/audit roles, improves corrected validation CE against the untrained UKF initializer under a predeclared rule, and survives veto diagnostics. |
| Veto diagnostics | Training samples below \(20P_\theta\) for evidence; audit leakage; selection/tuning on audit; source-prefit revival; proxy metrics promoted to fit quality; nonfinite loss/gradient/rho/normalizer/CE; bridge/tieout failure; seed overlap; default change; GPU/network/package install without approval; large run without approval. |
| Explanatory diagnostics | Training loss, gradient norm, raw square-root residuals, centered log-shape RMS, alpha ESS, rho range, normalizer, runtime, TensorFlow import warnings, and short mechanics-smoke values. |
| Not concluded | No source-faithful Zhao--Cui claim, no validation/HMC readiness, no lower-gate repair, no production/default policy, no final rank/sample policy, and no scaling claim unless a later reviewed phase explicitly establishes that claim. |
| Artifacts | P77 master program, visible runbook, execution ledger, Claude review ledger, stop handoff, phase subplans/results, runner/tests, JSON diagnostics. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| P77 is a new master program | P76 Phase 10 closeout | P76 repaired prerequisites but did not govern a proper training-evidence run. | Continuing P76 as if metric plumbing proved training. | Phase 0 boundary reset. | draft |
| Corrected heldout CE is primary fit metric | P76 Phases 8-10 | It matches the target-only density metric and avoids \(\tau q_0\) helper contamination. | Training loss or residuals promoted as fit quality. | Phase 1 objective/split contract. | active |
| \(N_{\rm train}\ge 20P_\theta\) | User direction and sample-to-parameter discipline | Prevents under-sampled regression evidence. | Calling tiny smokes evidence. | Phase 2 budget manifest and Phase 5 gate. | active |
| UKF initializer is baseline | P76 UKF initializer and Phase 10 metric diagnostic | Training must beat the actual warm-started initial candidate on the same corrected metric. | Comparing against failed P75 baselines only. | Phase 1/2 comparator contract. | active |
| Audit remains untouched by tuning | Scientific coding policy and P76 leakage repairs | Audit must be final-check only. | Hyperparameters selected on audit. | Phase 1 split manifest. | active |

## Global Forbidden Actions

- Do not treat mechanics smokes as training evidence.
- Do not run a training-evidence command with fewer than \(20P_\theta\) fresh
  training samples.
- Do not tune, select, or stop on audit samples.
- Do not revive random, calibrated constant, or source-route prefit as live
  candidate methods.
- Do not change defaults.
- Do not launch detached or nested agents.
- Do not use GPU/CUDA, network, package installs, or large training runs
  without separate approval.
- Do not claim source-faithful Zhao--Cui parity without paper and author-source
  anchors.

## Anticipated Approvals

At master-program creation, Codex needs approval only for local `docs/plans`
writes, bounded local source/doc reads, Claude read-only review through the
approved wrapper, and Phase 0 execution.

Later phases will require separate approval before:

- any training run interpreted as evidence;
- any `1024 x 40` or larger fresh-batch run;
- any GPU/CUDA use;
- any run expected to be long or resource-intensive;
- any default behavior change;
- any network/package/environment operation.

Scoped implementation-code edits do not require separate human approval when
they are exactly the file and behavior edits named in a Claude-reviewed phase
subplan, are executed visibly by Codex, and do not include training evidence,
GPU/CUDA, network/package operations, default changes, destructive actions, or
large diagnostics.

## Skeptical Plan Audit

The main risk is repeating the old error: using a tiny or proxy run and then
speaking as if it answered the training question.  P77 blocks that path by
separating mechanics smokes from evidence runs and requiring
\(N_{\rm train}\ge20P_\theta\) before any fixed-branch regression/training
claim.  The second risk is arbitrary tuning after seeing results.  P77 pushes
all hyperparameter choices into a predeclared Phase 2/5 protocol before any
proper training run.
