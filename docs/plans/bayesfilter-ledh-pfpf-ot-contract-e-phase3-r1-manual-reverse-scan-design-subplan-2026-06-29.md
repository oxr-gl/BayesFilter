# Phase R1 Subplan: Contract E Manual Reverse-Scan Design

Date: 2026-06-29

Status: `DRAFT_FOR_CLAUDE_REVIEW`

Parent plan:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-gradient-route-repair-plan-2026-06-29.md`

## Phase Objective

Design the full manual likelihood reverse-scan route for the Contract E LGSSM
Phase 3 gradient gate before implementing any new gradient code or rerunning
material evidence.

The immediate goal is not to pass the gradient gate.  The goal is to bind the
future score route, every derivative boundary, and the Contract E reset
derivative decision point so that the previous outer-`GradientTape` wiring bug
cannot recur.

## Entry Conditions Inherited From Previous Phase

- R0 containment passed:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-gradient-route-repair-r0-result-2026-06-29.md`.
- The current Phase 3 material gate is blocked by
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`.
- The current Phase 3 reverse diagnostic may still run only as a
  transport-VJP-only taped smoke/localization diagnostic.
- Existing manual LGSSM score pattern is available in
  `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py`.

## Required Artifacts

- R1 design note:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r1-manual-reverse-scan-design-2026-06-29.md`
- R1 route manifest:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r1-manual-reverse-scan-route-manifest-2026-06-29.json`
- R1 artifact audit test:
  `tests/test_contract_e_phase3_r1_design_artifacts.py`
- R1 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r1-manual-reverse-scan-design-result-2026-06-29.md`

## Required Checks, Tests, And Reviews

- Claude bounded read-only review of this subplan before execution.
- Static artifact test checking that:
  - the route manifest is design-only and material-gate authorization remains
    false;
  - the route is named `manual_likelihood_reverse_scan_no_autodiff`;
  - all derivative boundaries are listed;
  - every Contract E reset sub-boundary is listed individually and unresolved
    reset sub-boundaries are blocked pending R2;
  - generic score autodiff is forbidden.
- `python -m pytest tests/test_contract_e_phase3_r1_design_artifacts.py -q`
- `git diff --check` on R1 artifacts.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the future Contract E Phase 3 material score route specified with every derivative boundary accounted for before implementation? |
| Baseline/comparator | Existing old LGSSM manual score pattern and current Contract E forward scalar. |
| Primary pass criterion | R1 design and manifest list all derivative boundaries, identify available manual VJPs, and classify Contract E reset as blocked pending a local VJP decision. |
| Veto diagnostics | Any implicit derivative boundary; any material authorization; any generic score `GradientTape` allowed in the material route; any claim that Contract E gradient is repaired; missing route manifest. |
| Explanatory diagnostics | Source line anchors and implementation notes. |
| Not concluded | No gradient correctness, no reset VJP correctness, no FD/Kalman agreement, no GPU/XLA material readiness. |
| Artifact | R1 design note, manifest, artifact test, and R1 result. |

## Derivative Boundaries That Must Be Classified

- parameterization of LGSSM transition/observation quantities;
- stateless fixed noises and transition sampling reparameterization;
- LEDH affine flow;
- transition and observation log densities;
- log-weight correction identity;
- log-weight normalization and log floor;
- Sinkhorn transport matrix and/or transported cloud;
- Contract E weighted target moments;
- Contract E barycentric first-stage map `y_plus = matrix @ post_flow`;
- Contract E plus-cloud uniform moments;
- Contract E covariance gap construction;
- Contract E target covariance projector and rank/eigenvalue classification;
- Contract E residual covariance construction;
- Contract E residual covariance square root;
- Contract E residual-noise recentering and injection;
- Contract E tilde-cloud uniform moments;
- Contract E target covariance square root;
- Contract E tilde covariance pseudo-inverse square root;
- Contract E affine moment-restoration map;
- Contract E final recentering to `y_star`;
- Contract E diagnostic moment/conditioning monitors;
- time-reverse recurrence and score accumulation;
- diagnostic outputs and non-gradient monitors.

## Forbidden Claims And Actions

- Do not implement a Contract E reset VJP in R1.
- Do not remove the Phase 3 material blocker.
- Do not weaken the material blocker after R2 merely chooses a reset policy.
  Material mode may be unblocked only in a later phase after the full manual
  likelihood reverse scan is implemented in code, audited, and reviewed.
- Do not run GPU, FD, Kalman comparison, or material Phase 3 gradient commands.
- Do not claim the Contract E gradient is fixed.
- Do not authorize generic `tf.GradientTape`, `ForwardAccumulator`,
  `transport_ad_mode=full`, or Python loops in the material score route.
- Do not hide Contract E eigensystem, square-root, or pseudo-inverse-square-root
  derivatives inside TensorFlow autodiff.

## Exact Next-Phase Handoff Conditions

Advance to R2 only if:

- Claude review of this R1 subplan is `VERDICT: AGREE` or all material
  `REVISE` findings are patched and rereviewed;
- R1 design and manifest exist;
- local artifact tests pass;
- R1 result states that Contract E reset remains blocked pending a local VJP
  decision.

R2 must isolate the Contract E reset map and decide between
`manual_vjp_implemented`, `stop_gradient_by_design`, or `blocked`.
That R2 decision alone cannot remove or weaken
`PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`; a later
implemented-and-audited full manual likelihood reverse scan is required before
material mode can be re-enabled.

## Stop Conditions

Stop and write a blocker if:

- Claude identifies a material flaw in the subplan that cannot be patched
  locally;
- the design cannot name every derivative boundary;
- the manifest would accidentally authorize material evidence;
- the artifact test cannot enforce the intended boundary conditions.
- the artifact test does not classify every Contract E reset sub-boundary
  individually.

## End-Of-Phase Protocol

1. Run the required local static checks.
2. Write the R1 result.
3. Draft or refresh the R2 local Contract E reset VJP-decision subplan.
4. Do not advance to implementation until R2 has its own reviewed subplan.
