# Phase 2 Subplan: Fixed Randomness Tensorization

Date: 2026-07-02

Status: `DRAFT_FOR_CLAUDE_REVIEW`

## Phase Objective

Move P8p SIR process-noise generation out of the compiled value/score route and
into fixed tensors built once with the existing stateless seed policy. The
compiled route should consume `tensors["transition_noise"]` by time index
instead of looping over `args.batch_seeds` and calling
`tf.random.stateless_normal` inside the route.

## Entry Conditions Inherited From Previous Phase

- Phase 1 static audit exists and reports the current route as
  `FAIL_CURRENT_ROUTE`.
- The Phase 1 audit detects `SIR-MANUAL-SEED-LOOP` as a current-veto pattern at
  `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:1221`,
  `:1222`, and `:1232`.
- No claim has been made that the route is clean XLA.

## Required Artifacts

- Implementation changes scoped to:
  `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- Static audit script/test updates only if needed to reflect the removed seed
  loop:
  - `scripts/audit_ledh_clean_xla.py`
  - `tests/test_audit_ledh_clean_xla.py`
- Phase 2 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase2-fixed-randomness-tensorization-result-2026-07-02.md`
- Updated static audit artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase2-static-audit-2026-07-02.json`
- Draft Phase 3 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase3-rk4-loop-hygiene-subplan-2026-07-02.md`
- Updated execution and Claude review ledgers.

## Required Checks, Tests, Reviews

Before implementation:

- Codex skeptical audit of this subplan.
- Claude read-only review of the Phase 1 result and this Phase 2 subplan.

After implementation:

- `CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_clean_xla.py --format json --output docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase2-static-audit-2026-07-02.json`
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py`
- Focused import/shape check for the new fixed tensor helper, preferably as a
  small test added to `tests/test_audit_ledh_clean_xla.py` or a new focused
  test if cleaner.
- A small CPU-hidden deterministic parity check that compares the previous
  stateless-noise construction with the new `transition_noise` tensor for at
  least two seeds and two time steps. This is a semantic preservation check,
  not a GPU/XLA claim.
- Claude read-only review of the Phase 2 result before Phase 3 execution.

GPU/XLA runtime checks are not required in Phase 2.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can process-noise randomness be tensorized outside the compiled route without changing the existing stateless seed policy? |
| Baseline/comparator | Existing per-time/per-seed `tf.random.stateless_normal` policy: seed `[batch_seed % 2147483647, (1140 + time_index) % 2147483647]`, shape `[num_particles, state_dim]`, dtype `DTYPE`. |
| Primary pass criterion | New fixed `transition_noise` tensor exactly matches the old stateless construction for the checked seeds/time steps; `SIR-MANUAL-SEED-LOOP` is absent or reported as clean by the static audit; local tests pass. |
| Veto diagnostics | Change in seed policy, shape, dtype, or time/seed ordering; random generation remains inside `_manual_value_and_score_from_components`; tensorization changes the validated same-scalar target without being recorded; audit no longer reports the remaining current-veto classes; unrelated loop/Sinkhorn/RK4 edits are made. |
| Explanatory diagnostics | Updated audit counts, tensor shape, parity max absolute difference, and source line anchors. |
| Not concluded | No RK4 cleanup, no time-scan cleanup, no Sinkhorn cleanup, no HLO evidence, no numerical FD rerun, no clean-XLA claim. |
| Artifact | Phase 2 result markdown and Phase 2 static audit JSON. |

## Implementation Details

Add a fixed transition-noise tensor with shape:

`[batch_size, time_steps, num_particles, state_dim]`

where `batch_size == len(args.batch_seeds)` and `state_dim == 18` for the P8p
SIR diagnostic.

The tensor must preserve the existing seed policy exactly:

```text
seed = [batch_seed % 2147483647, (1140 + time_index) % 2147483647]
noise[batch, time] = tf.random.stateless_normal([num_particles, state_dim], seed)
```

Use that tensor in:

- `_make_sir_callbacks_from_scaled_parameters(...).pre_flow_step`;
- `_manual_value_and_score_from_components`.

The value path and the manual score path must consume the same
`transition_noise` tensor. Do not introduce a second noise source.

The static audit should continue to return `FAIL_CURRENT_ROUTE` after Phase 2,
because RK4, time scan, reverse scan, and Sinkhorn findings remain. The expected
change is that `SIR-MANUAL-SEED-LOOP` is no longer a found current-veto pattern
for `_manual_value_and_score_from_components`.

## Forbidden Claims And Actions

- Do not claim clean XLA after Phase 2.
- Do not edit RK4 loops, time scans, reverse scans, or Sinkhorn loops in this
  phase.
- Do not change finite-difference tolerances, gradient acceptance rules, or
  score definitions.
- Do not call stopped partial derivatives scores.
- Do not run long GPU jobs or HLO metrics in Phase 2.
- Do not replace the existing seed policy with a new random stream.

## Exact Next-Phase Handoff Conditions

Phase 2 may hand off to Phase 3 only if:

- the new `transition_noise` tensor is built once outside the compiled route;
- parity with the previous stateless construction is recorded;
- `_manual_value_and_score_from_components` no longer contains the Python seed
  loop or `tf.random.stateless_normal`;
- the static audit still detects the remaining current-veto classes;
- Phase 2 result and Phase 3 subplan exist;
- Claude read-only review returns `VERDICT: AGREE`, or fixable findings are
  patched and rereviewed.

## Stop Conditions

Stop and write a blocker result if:

- parity with the old stateless policy fails;
- the required tensor shape cannot be represented without changing route
  semantics;
- source changes spill into RK4, time-scan, or Sinkhorn refactors;
- tests require GPU, network, package installation, or unrelated file changes;
- Claude and Codex do not converge after five rounds.

## Skeptical Pre-Execution Audit

Result: `PASS_PENDING_CLAUDE_REVIEW`

- Wrong baseline: avoided by preserving the exact old stateless seed policy.
- Proxy promotion: avoided because Phase 2 only removes one static unclean
  surface and cannot claim clean XLA.
- Missing stop conditions: explicit above.
- Unfair comparison: parity compares old and new noise construction, not full
  runtime performance.
- Hidden assumption: the plan states the expected audit decision remains
  `FAIL_CURRENT_ROUTE`.
- Environment mismatch: CPU-hidden parity/source checks only; GPU evidence is
  deferred.
- Artifact mismatch: Phase 2 result must include updated audit JSON and parity
  evidence.
