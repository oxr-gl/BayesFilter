# P8k Phase 4 Subplan: Inactive-Transport Skip Path

metadata_date: 2026-06-17
status: DRAFT
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md
phase: 4

## Phase Objective

Repair or implement the generic `skip_transport_when_no_active` behavior so a
time step with no active resampling mask does not call the OT transport core.
This phase fixes and verifies already-advertised function semantics
(`skip_transport_when_no_active=True` already exists in the streaming core
signature); it does not broaden default policy or introduce a new default.

## Entry Conditions Inherited From Previous Phase

- Phase 3 focused checks passed.
- The configuration contract keeps the skip behavior opt-in or preserves the
  existing default if already declared.

## Required Artifacts

- Phase 4 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase4-inactive-transport-skip-result-2026-06-17.md`
- Focused test output summary.

## Required Checks/Tests/Reviews

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py -q -k "inactive_transport or mixed_active_transport or transport or streaming or nonlinear_prior_mean"
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-*
```

Claude review is required for material implementation diffs before Phase 5.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the engine avoid OT work when no batch row is active at a time step? |
| Baseline/comparator | Current streaming core with static all-false shortcut only. |
| Primary criterion | Focused sentinel tests demonstrate no transport call for all-inactive dynamic mask steps when `skip_transport_when_no_active=True`, and a mixed active/inactive batch still calls transport rather than skipping the whole batch. |
| Veto diagnostics | Transport core called for all-inactive dynamic mask with skip enabled; transport skipped when any row is active; changed log-likelihood for equivalent active settings; hidden SIR logic; default-policy broadening beyond the advertised flag semantics. |
| Explanatory diagnostics | CPU smoke runtime and mask-path notes. |
| Not concluded | No GPU speedup claim until Phase 5, no particle adequacy. |

## Forbidden Claims/Actions

- Do not skip transport for mixed active/inactive masks unless the transport
  core handles row masks correctly.
- Do not change the interpretation of `fixed_resampling_mask`.
- Do not run long GPU profiling in Phase 4.
- Do not claim a new default policy; Phase 4 only repairs and verifies the
  existing `skip_transport_when_no_active` argument semantics.

## Exact Next-Phase Handoff Conditions

Phase 5 may proceed if local checks and Claude review pass, including:

- a monkeypatch/sentinel test proving `batched_annealed_transport_core_tf` is
  not called for an all-inactive dynamic mask when
  `skip_transport_when_no_active=True`;
- a mixed active/inactive mask test proving transport is still called when any
  batch row is active;
- log-likelihood equivalence or unchanged-value checks for active settings.

## Stop Conditions

Stop if the skip path cannot be implemented without changing resampling
semantics, if focused tests cannot distinguish active from inactive behavior,
or if the repair would broaden default policy beyond the advertised function
argument.
