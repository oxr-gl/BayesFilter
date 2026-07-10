# Review Packet: LEDH Shared Compact Score Memory Root-Cause Repair Plan

Date: 2026-07-09

## Role Contract

Codex is supervisor and executor. Claude or a fresh Codex agent is read-only
reviewer only. The reviewer must not edit files, run commands, approve boundary
crossings, or make scientific/admission claims.

## Objective

Review the plan:

`docs/plans/bayesfilter-ledh-shared-compact-score-memory-root-cause-repair-plan-2026-07-09.md`

The plan responds to a repeated `N=10000,T=50` LGSSM compact score no-artifact
blocker by tracing shared tensor-memory causes across all compact LEDH score
models and proposing a shared transport JVP contraction repair.

## Key Local Trace Facts

- `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py` carries
  `running_d_particles` and calls
  `_filterflow_manual_streaming_finite_transport_value_and_jvp_total`, which
  returns full `d_transported`.
- Fixed-SIR, actual-SV, predator-prey, generalized-SV, and KSC-SV compact score
  scripts have analogous `_compact_forward_transport_jvp_tf` wrappers and call
  the same shared transport JVP.
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  has avoidable 5D block temporaries in:
  - `_filterflow_streaming_softmin_jvp`;
  - `_filterflow_streaming_column_log_normalizer_jvp`;
  - `_filterflow_streaming_transport_from_potentials_jvp`.
- The plan distinguishes this contraction repair from a later true reduce-only
  score recurrence. It does not claim admission from score-only diagnostics.

## Reviewer Questions

1. Does the plan preserve the same finite-`N` LEDH log-likelihood scalar rather
   than substituting exact Kalman likelihood or a proxy objective?
2. Does the plan correctly identify the shared implementation hotspot and the
   similar per-model surfaces?
3. Is Phase 1 a value-preserving tensor-lifetime repair with adequate local
   tests before GPU rungs?
4. Are score-only GPU rungs correctly treated as diagnostic and not admission?
5. Are stop conditions and forbidden claims/actions sufficient?

## Required Verdict Format

Return concise findings, then end with exactly one of:

`VERDICT: AGREE`

or

`VERDICT: REVISE`
