# P49-M7 Deterministic Gradient-Lane Boundary Result

metadata_date: 2026-06-09
phase: P49-M7
status: PASS_P49_M7_GRADIENT_LANE_BOUNDARY

## Decision Table

| Field | Decision |
| --- | --- |
| Gate decision | Pass M7 for an honest deterministic gradient-bearing adaptation contract. |
| Primary criterion status | Passed: tests enforce adaptation labeling, source-fidelity non-claim, adaptive-random-branch differentiation block, HMC non-promotion by default, allowed HMC readiness statuses, and explicit recognized HMC tier requirements. |
| Veto diagnostic status | Passed: analytical-gradient necessity cannot claim source fidelity; adaptive random source branches cannot be differentiated without a separate contract; HMC readiness cannot be promoted by finite gradients alone. |
| Main uncertainty | M7 is a contract/gate, not a fresh full gradient-accuracy ladder over all models. |
| Next justified action | Advance to M8 integration closeout. |
| Not concluded | No source-faithful filtering accuracy, production score API readiness, production HMC readiness, or adaptive source-route differentiability. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What evidence is required before the fixed branch is used for HMC or score-based inference? |
| Baseline/comparator | P42/P43/P47 score readiness rules plus route-governance matrix. |
| Primary pass criterion | Branch replay, value-gradient consistency, likelihood variance calibration policy, adaptation labels, and HMC non-promotion rules are explicit. |
| Diagnostics that can veto | Gradient necessity used to claim source fidelity; finite-difference instability used uncritically; adaptive random branches differentiated without contract. |
| Explanatory diagnostics | CPU-only pytest, compileall, static diff whitespace check. |
| What will not be concluded | Source-faithful filtering accuracy or HMC readiness. |
| Artifact preserving result | This file plus `tests/highdim/test_p49_gradient_lane_boundary.py`. |

## Implemented Scope

M7 added `GradientLaneEvidenceContract` in
`bayesfilter/highdim/score_api.py`.

The contract requires:

- `route_label = gradient_bearing_adaptation`;
- branch replay status;
- value/gradient status;
- likelihood variance calibration status;
- HMC readiness status;
- non-claims including `no source-faithful filtering claim` and
  `no HMC readiness by default`.

The contract rejects:

- source-fidelity claims from gradient evidence;
- differentiating adaptive random source branches without a separate contract;
- HMC readiness promotion without explicit HMC tiers;
- unknown HMC readiness statuses, empty tiers, or unrecognized HMC tiers;
- source-route labels on gradient-lane evidence.

No HMC sampling, production score API, or full model-wide gradient ladder was
run in M7.

## Local Validation

Commands run CPU-only with `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`:

```text
pytest -q tests/highdim/test_p49_gradient_lane_boundary.py tests/highdim/test_public_api_highdim.py tests/highdim/test_phase0_contracts.py tests/highdim/test_p49_source_route_smoothing_boundary.py tests/highdim/test_p49_source_route_preconditioned_predator_prey.py tests/highdim/test_p49_source_route_recenter_normalizer.py tests/highdim/test_p49_source_route_sample_proposal.py tests/highdim/test_p49_source_route_retained_object.py
```

Result:

```text
59 passed, 2 TensorFlow Probability deprecation warnings
```

```text
python -m compileall -q bayesfilter/highdim/score_api.py bayesfilter/highdim/source_route.py tests/highdim/test_p49_gradient_lane_boundary.py tests/highdim/test_p49_source_route_smoothing_boundary.py
```

Result: passed.

```text
git diff --check -- bayesfilter/highdim/score_api.py bayesfilter/highdim/__init__.py tests/highdim/test_p49_gradient_lane_boundary.py docs/plans/bayesfilter-highdim-zhao-cui-p49-visible-execution-ledger-2026-06-09.md
```

Result: passed.

## Interpretation

M7 makes the user-requested distinction mechanical: analytical gradients are
allowed and useful in the deterministic adaptation lane, but they do not make
that lane source-faithful Zhao--Cui.  Any future HMC claim must pass explicit
HMC tiers and remain tied to the declared target and route label.
