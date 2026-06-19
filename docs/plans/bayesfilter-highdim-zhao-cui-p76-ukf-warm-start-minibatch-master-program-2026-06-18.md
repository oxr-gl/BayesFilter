# P76 Master Program: UKF Warm Start With Mini-Batch Density Training

metadata_date: 2026-06-18
status: PHASE7V2_CLAUDE_AGREE_READY_FOR_PHASE8
predecessor_erratum: docs/plans/bayesfilter-highdim-zhao-cui-p75-closeout-erratum-ukf-hypothesis-untested-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Objective

Implement and test the remaining live hypothesis for the Zhao--Cui fixed
variant:
\[
  \text{UKF-informed geometry warm start}
  \longrightarrow
  \text{mini-batch stochastic density training}.
\]

The target is not source-faithful Zhao--Cui.  It is an
`extension_or_invention` / fixed-variant repair hypothesis.  The UKF contributes
geometry only: mean, covariance, scales, orientation, and effective-dimension
diagnostics.  It is not truth, not validation, not exact likelihood, and not
HMC readiness evidence.

## Supersession Boundary

P76 supersedes P75 for the initialization hypothesis.  P75 established that
random, calibrated constant, and source-route square-root prefit are failed
routes for the lower-gate geometry problem.  P76 must not repeat those methods
as live candidate ladder arms.  They may appear only as historical references
or as minimal safety sentinels when a phase explicitly justifies them.

## Mathematical Target

Let \(z\) be the fixed local coordinate, \(q_0(z)\) the defensive density, and
\[
  \rho_\theta(z)=h_\theta(z)^2+\tau q_0(z).
\]
Let the UKF scout provide finite moments for the adjacent physical variable,
then mapped or restricted to the fixed local coordinate:
\[
  m_U,\qquad P_U.
\]
The Phase 1 design must choose one explicit initialization target, for example
\[
  h_0(z)
  \approx
  \sqrt{\frac{\pi_U(z)}{q_{\rm ref}(z)}}
  \quad\text{or}\quad
  h_0(z)\approx C\exp\{-\tfrac14(z-m_U)^\top P_U^{-1}(z-m_U)\},
\]
with all measure, truncation, flooring, scaling, and TT-projection choices
specified before implementation.

After initialization, P76 trains by mini-batch stochastic density training:
\[
  \theta_{k+1}
  =
  \theta_k-\eta\nabla_\theta \widehat{\mathcal L}_{B_k}(\theta_k),
\]
where \(B_k\) are training-eligible generated batches and all audit/holdout/line
samples remain excluded from initialization, training, stopping, and
hyperparameter selection.

## Phase Index

Only Phase 0 is executable at master-program creation.  Each later phase must
receive a dedicated subplan before execution.

| Phase | Name | Must consume | Must produce for next phase |
| --- | --- | --- | --- |
| 0 | Closeout and boundary reset | P75 erratum, P75 Phase 10 result, p50 UKF scout section, current UKF scout code | Boundary result and reviewed Phase 1 mathematical UKF-initializer subplan |
| 1 | Mathematical UKF initializer contract | Phase 0 result, p50/P70 UKF scout contracts, current code inventory | Exact \(m_U,P_U\) route, target \(h_0\), projection/fitting objective, audit split, and reviewed Phase 2 implementation-surface subplan |
| 2 | Implementation surface and test plan | Phase 1 design | Concrete code/test surface for UKF initializer, mini-batch training reuse, manifests, and reviewed Phase 3 implementation subplan |
| 3 | Opt-in UKF initializer implementation | Phase 2 surface | Opt-in implementation, focused unit tests, no default behavior change, reviewed Phase 4 smoke subplan |
| 4 | Tiny UKF-initializer smoke | Phase 3 implementation | CPU-only tiny diagnostic comparing UKF initializer against historical failure criteria, not a broad ladder; reviewed Phase 5 decision subplan |
| 5 | Mini-batch training pilot decision | Phase 4 result | Decision: stop, repair, or draft a bounded mini-batch pilot; no large pilot without separate approval |

Later corrective and execution phases are tracked in the visible runbook and
ledgers.  As of Phase 6b closeout, Phase 6 is reclassified as mechanics-only,
the original Phase 7 draft is superseded, and Phase 7 v2 is the next eligible
subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a true UKF-informed initializer provide usable geometry for subsequent mini-batch density training in the fixed variant? |
| Baseline/comparator | Historical P75 failures: random floor collapse, calibrated-constant scale-only failure, and source-route prefit weak failure.  They are references, not live ladder candidates. |
| Primary pass criterion | Each phase produces its required artifact, preserves the UKF-as-scout boundary, keeps audit data out of training/selection, and hands off to the next reviewed subplan without overclaiming. |
| Veto diagnostics | Source-route prefit substituted for UKF initialization; UKF promoted to truth/validation/HMC readiness; audit leakage; large-pilot launch; proxy metric promoted to lower-gate repair; stale P75 ladder repeated as live method. |
| Explanatory diagnostics | UKF moment finiteness, covariance conditioning, projected initializer residuals, mini-batch losses, gradients, heldout residuals, line residuals, runtime. |
| Not concluded | No lower-gate repair, validation readiness, HMC readiness, scaling, source-faithfulness, final rank/sample policy, or large-pilot authorization unless a later reviewed phase explicitly proves that claim under frozen gates. |
| Artifacts | P75 erratum, P76 master program, visible runbook, execution ledger, Claude review ledger, phase subplans/results, JSON diagnostics. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| P75 is superseded for the UKF hypothesis | P75 Phase 10 and erratum | P75 did not implement a true UKF warm start. | Treating P75 as evidence against UKF. | Phase 0 boundary result. | draft |
| UKF is `scout_not_truth` | p50 UKF scout section; `ukf_scout.py` | Prevents validation/HMC/correctness overclaim. | UKF moments promoted to proof. | Phase 0/1 nonclaim checks. | draft |
| Source-route prefit is forbidden as target substitute | P75 negative result | It already failed as a repair route. | Repeating the wrong method. | Phase 1 design veto. | active |
| UKF-whitened Gaussian square-root projection is the P76 initializer target | P76 Phase 1 result | This uses \(m_U,P_U\) as geometry and avoids source-route prefit. | Treating UKF as truth or using degree-one smoke as curvature evidence. | Phase 2/3 implementation tests. | active |
| Mini-batch training follows initialization | User direction and P75 machinery | The intended method is warm start plus stochastic batches. | Testing initializer only and calling it solved. | Phase 1 evidence contract. | active |

## Global Forbidden Actions

- Do not launch detached, nested, or copied-workspace execution.
- Do not use source-route prefit as the P76 target method.
- Do not run random/constant/source-prefit ladders as live candidate repairs.
- Do not run the degree-2/rank-4/batch-1024/500-batch pilot without a later
  reviewed plan and explicit human approval.
- Do not claim source-faithful Zhao--Cui parity without paper and author-source
  anchors.
- Do not use audit samples for initialization, training, stopping,
  hyperparameter selection, or metric switching.
- Do not interpret UKF as truth, exact likelihood, validation, HMC readiness,
  or lower-gate repair evidence.

## Anticipated Approvals And Boundaries

The user has requested visible execution in this session.  The planning spine
needs approval for:

- local writes under `docs/plans`;
- bounded local source/doc reads;
- Claude Code read-only review through the approved wrapper;
- MathDevMCP checks if mathematical derivation labels are introduced later.

Later phases may require separate approval for:

- implementation-code edits;
- any GPU/CUDA use;
- any run expected to exceed the reviewed visible bounds;
- any large mini-batch pilot;
- any change of default behavior.

## Skeptical Plan Audit

This draft corrects the P75 planning error by making the actual UKF initializer
the target.  The main remaining risk is designing a UKF initializer that is
only named UKF but still implemented as source-route prefit.  Phase 1 must
therefore bind the initializer mathematically to UKF moments \((m_U,P_U)\) and
define a projection or fitting objective for \(h_0\) before code changes.
