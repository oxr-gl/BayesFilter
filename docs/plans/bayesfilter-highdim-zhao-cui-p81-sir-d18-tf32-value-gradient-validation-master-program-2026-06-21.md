# P81 Master Program: SIR d=18 TF32 Value/Gradient Validation

status: BLOCKED_PENDING_LANE_DIRECTION
date: 2026-06-21
supervisor_executor: Codex
readonly_reviewer: Claude Opus, bounded packet review only

## Objective

Validate the Zhao-Cui fixed-variant value and gradient lane for the actual
d=18 SIR target before any broader performance or likelihood comparison.  The
candidate is the fixed-branch score route with TensorFlow
`ForwardAccumulator` JVPs for local model-log-density directional derivatives.
It is not a closed-form hand derivative.  LEDH-PFPF-OT is reserved as the
later stochastic comparator.

## Phase Ladder

| Phase | Objective | Status |
|---|---|---|
| 1 | Refresh governance, boundaries, and source anchors for the P81 continuation. | complete by refresh |
| 2 | Restore and test fixed-branch/JVP-backed SIR d=18 wiring: parameterized model wrapper, public API, and derivative surfaces. | complete |
| 3 | Run a bounded d=18 horizon-0 fixed-branch/JVP-backed score smoke and direct model-term sensitivity checks. | passed, Claude R3 agree |
| 4 | Draft and, after review, run a tiny GPU/TF32 smoke for the same fixed-branch/JVP-backed candidate path. | passed, Claude agree |
| 5 | Audit and plan the missing multistate full-history score surface before any comparator run. | passed, Claude subplan agree |
| 6 | If Phase 5 passes, implement/test bounded multistate full-history score propagation. | tiny pass; d=18 all-grid transition complexity-gated |
| 7 | Resolve d=18 transition scaling blocker before any LEDH/PFPF-OT comparison. | recommends streamed all-pairs prototype |
| 8 | Prototype bounded streamed transition route with tiny dense parity and optional budget-vetoed d=18 smoke. | tiny streaming parity passed; d=18 full-grid still blocked |
| 9 | Design/select representation or transition-application scaling route because streamed all-pairs still leaves quadratic d=18 work. | passed; selected parameterized local-route tie-out |
| 10 | Repair parameterized local-route semantics and tie out tiny value/theta derivatives against dense transition reference. | passed, execution review pending |
| 11 | Resolve memory/rank/compression policy before any d=18 candidate full-history route. | blocked direct implementation; derivation needed |
| 12 | Derive/select or block compressed deterministic transition operator/contraction route. | blocked; no sufficiently defined compressed route exists |
| 13 | If Phase 12 selects a route, implement lower-rung compressed-route tie-out. | not authorized |
| 14 | Only after a candidate d=18 full-history score route passes, compare candidate value/gradient evidence against LEDH-PFPF-OT with agreed seeds and particle budget. | not authorized |
| 15 | Close with decision table, limitations, and next master-program handoff. | blocked by lane decision |

## Standing Evidence Contract

The scientific question is whether the fixed-variant Zhao-Cui
fixed-branch/JVP-backed candidate can produce finite, branch-stable
value/gradient evidence on the d=18 SIR target under the same parameter
convention later used for comparison.

The primary comparator for validation phases is not a failed training ladder.
For candidate correctness, Phase 3 uses same-branch finite-difference checks and
direct model-term sensitivity.  Later stochastic comparison uses the default
batched TF32 LEDH-PFPF-OT lane under the same parameter convention.

Veto diagnostics include nonfinite values, branch-hash drift during fixed-branch
finite differences, shape/parameter convention mismatch, unsupported claims of
full likelihood correctness from horizon-0 smoke, unreviewed GPU runs, and
source-faithfulness claims without paper/source anchors.

Explanatory diagnostics include runtime, local residuals, condition warnings,
and model-term sensitivity magnitudes.

Phase 3 establishes only horizon-0, one-row, observation-term engineering
wiring under same-branch finite-difference stability.  It does not establish
multistate score correctness for transitions, full-likelihood gradients,
HMC/NUTS readiness, LEDH/P8p parity, scientific validity, source-faithfulness,
production default readiness, or posterior validity.

## Repair Loop

Each material subplan and result packet is reviewed with Claude as read-only
reviewer until convergence or five rounds for the same blocker.  Codex remains
the supervisor and executor.  Claude cannot authorize crossing human, runtime,
GPU, model-file, funding, product-capability, or scientific-claim boundaries.

Fixable review findings are patched visibly in the same subplan or result
packet, then focused checks are rerun.  If a blocker does not converge after
five rounds, write a blocker result and stop for human direction.
