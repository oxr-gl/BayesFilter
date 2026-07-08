# Phase 3 Result: Manual-VJP LGSSM Score Route Audit

Date: 2026-07-03

Status: `BLOCKED_TOTAL_TRANSPORT_VJP_STILL_NEEDS_NO_TAPE_REPAIR`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Do not admit an LEDH LGSSM leaderboard score row. |
| Primary criterion status | Failed before GPU score execution: no current route satisfies both total-derivative and no-tape requirements. |
| Veto diagnostic status | Veto triggered by transport derivative route mismatch. |
| Main uncertainty | Whether the full no-tape total VJP for finite streaming Sinkhorn transport can be implemented by adapting the existing hand-coded softmin/Sinkhorn VJPs without excessive compile or memory cost. |
| Next justified action | Repair the transport VJP first: replace stopped-scale/key transport adjoint with a no-`GradientTape` total VJP, then rerun same-scalar finite-difference and GPU/XLA smoke gates. |
| Not concluded | No LGSSM score admission, no nonlinear score readiness, no HMC readiness, no runtime ranking. |

## Evidence Contract Result

Question:

- Can the same LGSSM total-score route be computed by manual VJP without
  changing the target?

Answer:

- Not yet.  The value route exists, and no-tape manual reverse-scan scaffolds
  exist, but the currently available no-tape transport adjoint differentiates a
  stopped-scale/key scalar.  The currently available total-derivative transport
  helper still opens `GradientTape` inside its custom-gradient body.  Therefore
  neither route is admissible as the total derivative of the leaderboard LEDH
  value route under the Phase 3 rules.

## Exact Blocker

The public LEDH value+score wrappers are not admissible for this runbook:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:1747`
  defines `batched_ledh_pfpf_ot_value_and_score_tf`, and line 1762 opens
  `tf.GradientTape`.
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:681`
  defines `streaming_batched_ledh_pfpf_ot_value_and_score_tf`, and line 691
  opens `tf.GradientTape`.

The closest no-tape manual LGSSM statistical route is also not admissible as a
leaderboard total score:

- `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py:165` uses
  `tf.stop_gradient` on the transport center, scale, and `epsilon0`.
- `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py:176` calls
  `_filterflow_manual_streaming_finite_transport_stopped_scale_keys`.
- `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py:240` calls
  `_filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys`.
- Its own static audit at lines 840-851 requires the stopped-scale/key route.

The route that is named as total derivative is also not admissible under the
no-tape rule:

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:2342`
  defines `_filterflow_manual_streaming_finite_transport_total_vjp`.
- Its docstring says it differentiates the finite fixed-iteration transport
  value that it executes.
- Its custom-gradient body opens `tf.GradientTape` at line 2393 and calls
  `tape.gradient` at line 2416.

Plain scientific conclusion:

- The stopped-scale/key manual route computes the derivative of a different
  stopped computational target.  It is not the total derivative of the
  unstopped leaderboard LEDH scalar.
- The total-transport route targets the right finite transport map, but it is
  not a no-tape manual VJP route.
- Under the current Phase 3 rules, both are blocked for leaderboard score
  admission.

## Local Checks Run

- Resume amendment text check: passed for the Phase 3 subplan.
- `git diff --check` passed for the amended master program, runbook, Phase 3
  subplan, and visible ledger before this result was written.
- Claude probe returned `CLAUDE_PROBE_OK`.
- Phase 3 resume amendment review gate returned
  `REVIEW_STATUS=bounded_fallback_agree`, `VERDICT=AGREE`.

The Claude review was a bounded fallback signal, not a full primary material
review.  It did not certify code correctness.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Not recorded for this audit-only close record. |
| Commands | `rg`, `sed`, `nl`, local text check, `git diff --check`, Claude review gate. |
| Environment | Local repository audit; no GPU score run launched. |
| CPU/GPU status | GPU not used because pre-run audit vetoed score execution. |
| Data version | LGSSM row `benchmark_lgssm_exact_oracle_m3_T50`; dataset seed `81100`; no new data generated. |
| Random seeds | N/A, no numerical score run. |
| Wall time | N/A. |
| Output artifacts | This result file; Phase 3 resume review bundle; visible execution ledger. |
| Plan file | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase3-memory-safe-gpu-xla-score-subplan-2026-07-03.md` |

## Post-Run Red-Team Note

Strongest alternative explanation:

- One might argue that stopped-scale/key derivatives are an acceptable
  stabilized score.  That is not supported for this leaderboard score claim
  unless the stopped scalar is explicitly defined as the target.  The Phase 3
  target is the same scalar value route reported for the leaderboard row, so
  stopped partial derivatives are not admissible.

What would overturn this blocker:

- A no-`GradientTape`, no-`ForwardAccumulator` total VJP for finite streaming
  Sinkhorn transport that passes same-scalar finite differences and a trusted
  GPU/XLA tiny smoke.

Weakest part of the evidence:

- This phase did not implement the missing total transport VJP.  It only
  identified that current routes fail the admission contract.

## Phase 4 Handoff

Phase 4 may continue as a target-classification phase for fixed SIR, but it
must not treat LGSSM score repair as complete.  The LGSSM row remains:

- value status: same-target value-only evidence exists;
- score status: `blocked_total_transport_vjp_needs_no_tape_repair`;
- required next repair: no-tape total VJP for finite streaming Sinkhorn
  transport, then same-route value/score validation.
