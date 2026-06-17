# Phase 4 Blocker - Active Transport Repair Subplan Nonconvergence - 2026-06-17

## Status

`PHASE_4_REPAIR_SUBPLAN_BLOCKED_CLAUDE_NONCONVERGED`

## Objective

Create a reviewed, bounded repair subplan before editing gradient-bearing active
OT transport code for XLA/JIT score support.

## Result

The active-transport score/JIT diagnostic failed with a fixable XLA TensorList
blocker, but the focused repair subplan did not converge under the required
Claude read-only review loop within the allowed review rounds.

No active-transport implementation code was edited after this blocker.

## Review Trail

| Round | Artifact | Result |
| --- | --- | --- |
| 01 | streamed Claude worker session | Nonconverged. Claude over-read source, emitted large stream output, and did not return a verdict. |
| 02 | `docs/benchmarks/logs/p4-active-transport-score-jit-repair-subplan-claude-review-r2-2026-06-17.log` | Timed out with empty log. |
| Probe | `docs/benchmarks/logs/p4-active-transport-claude-probe-2026-06-17.log` | Returned `PROBE_OK`, showing Claude availability. |
| 03 | `docs/benchmarks/logs/p4-active-transport-score-jit-repair-subplan-claude-review-r3-2026-06-17.log` | `VERDICT: BLOCKED` for missing non-binding iteration-cap proof and active-odd eager-vs-JIT semantic check. |
| 04 | `docs/benchmarks/logs/p4-active-transport-score-jit-repair-subplan-claude-review-r4-2026-06-17.log` | `VERDICT: BLOCKED` for missing full bounded-loop audit and non-binding cap evidence plan. |
| 05 | `docs/benchmarks/logs/p4-active-transport-score-jit-repair-subplan-claude-review-r5-2026-06-17.log` | `VERDICT: BLOCKED` for ambiguous promotion and audit scope. |

## Final Unresolved Material Issues

Claude round 05 identified these remaining material gaps:

1. Promotion must explicitly require an executed
   `tf.function(jit_compile=True)` gradient call with finite value and score,
   not just a loosely described score-path pass.
2. The loop audit cannot stop at explicit `tf.while_loop` calls unless the
   plan proves no JIT-reachable `tf.scan`, `tf.map_fn`, or AutoGraph-lowered
   loop can introduce TensorList state on the active-transport score path.
3. Dense-vs-streaming structure agreement must name the exact test/artifact and
   tolerance used as the gate.
4. FP32-no-TF32 should be classified as descriptive/guardrail evidence unless
   it is part of the primary promotion contract.

These are fixable planning issues, but they remained after the allowed review
loop, so implementation should not proceed until a human or a fresh session
reconciles the subplan.

## Current Technical Diagnosis

The active-odd FP64 CPU score/JIT command failed before JSON/Markdown
serialization with:

`XLA compilation requires a fixed tensor list size`

The failure stack points through the active transport branch of
`streaming_batched_ledh_pfpf_ot_value_core_tf` into
`annealed_transport_tf.py`.

Known likely repair surface:

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- explicit `tf.while_loop` sites around lines found by:
  `rg -n "tf\\.while_loop\\(" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- graph-unsafe diagnostics found by:
  `rg -n "\\.numpy\\(|bool\\(" experiments/dpf_implementation/tf_tfp/resampling`

## Recommended Next Action

Before editing code, patch the repair subplan to address the final unresolved
issues exactly:

- Define the primary promotion command/artifact as the existing gradient
  structure harness invocation that calls the score/gradient entry point under
  `tf.function(jit_compile=True)` and records finite value/score.
- Add an audit step for all JIT-reachable TensorList sources:
  `tf.while_loop`, `tf.scan`, `tf.map_fn`, Python loops that AutoGraph may
  lower, and TensorArray use.
- Name the dense-vs-streaming tolerance gate:
  `structure_value_atol`, `structure_value_rtol`, `structure_score_atol`, and
  `structure_score_rtol` from
  `docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_gradient_structure.py`.
- Classify FP32-no-TF32 active-odd as a guardrail/descriptive precision lane
  unless it is promoted into the primary criterion explicitly.

Then rerun a compact read-only review or ask the user to approve proceeding
without further Claude review.

## Nonclaims

No HMC readiness, posterior validity, production readiness, public API
readiness, active-transport score correctness, or performance claim is made.
