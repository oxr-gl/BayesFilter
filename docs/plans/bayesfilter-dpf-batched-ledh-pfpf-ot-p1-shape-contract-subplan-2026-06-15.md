# Phase 1 Subplan: Batched Callback And Shape Contract

Date: 2026-06-15

## Status

`READY_FOR_LOCAL_PRECHECK`

## Phase Objective

Define the experimental batch callback/data contract and minimal deterministic
fixtures for LEDH-PFPF-OT without changing production APIs.

## Entry Conditions Inherited From Previous Phase

- Phase 0 identified scalar LEDH-PFPF-OT baseline paths and graph blockers.
- Phase 0 established available scalar smoke/import tests.
- Phase 0 established fixed-contract parity policy: fixed particles or
  innovations, fixed observations, fixed ESS masks, fixed OT settings, and no
  RNG inside the value/score core.
- Phase 0 established starting parity tolerances: `atol=1e-10, rtol=1e-10`
  for scalar value/ledger tensors and `atol=1e-8, rtol=1e-8` for transport
  tensors unless a blocker review changes them before seeing results.
- No categorical PF gradient, production default, or public API change is
  authorized.

## Required Artifacts

- Experimental module skeleton under
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`.
- Focused tests under
  `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`.
- Dataclass or typed structure for a deterministic fixed-contract fixture with
  `[B,T,N,D]` pre-flow particles or innovations, `[T,O]` observations,
  `[B,T]` fixed ESS masks, `[B,N,D]` particles, `[B,N]` log weights, and
  `[B,p]` parameter rows where applicable.
- Shape validation helpers for value shape `[B]` and score shape `[B,p]`
  without implementing score recursion yet.
- Phase 1 result:
  `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p1-shape-contract-result-2026-06-15.md`
- Refreshed Phase 2 subplan.

## Required Checks, Tests, And Reviews

- Shape contract pytest for ranks `[B,N,D]`, `[B,N]`, `[B]`, `[B,p]`.
- Import smoke for the new experimental module.
- Local check that no top-level `bayesfilter` public export was added.
- Tests that fixture construction fails closed on hidden RNG callbacks,
  missing fixed ESS masks, or shape-incompatible parameter rows.
- Source check that the Phase 1 module does not call `tf.random`, `np.random`,
  or Python RNG inside the value/score contract.
- Claude read-only review if the callback contract changes after review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the experimental API express the batched LEDH-PFPF-OT contract without changing semantics or production exports? |
| Baseline/comparator | Phase 0 scalar path inventory and existing experimental batched value+score shape conventions. |
| Primary pass criterion | Shape tests and import smoke pass; deterministic fixed-contract fixture is explicit; no public API/default changes; Phase 2 handoff is explicit. |
| Veto diagnostics | Ambiguous callback shapes; hidden RNG in value core; missing fixed branch mask; public export drift; missing deterministic noise contract; tolerance policy omitted. |
| Explanatory diagnostics | Static shape availability, fixture dimensions, contract docstrings. |
| Not concluded | No value parity, no score correctness, no performance claim. |
| Artifact preserving result | Phase 1 result and tests. |

## Forbidden Claims And Actions

- Do not claim scalar parity yet.
- Do not implement full value recursion unless Phase 1 is explicitly amended.
- Do not add public exports.
- Do not use random ops inside the value/score core contract.
- Do not use runtime ESS branch decisions as a parity source.
- Do not loosen Phase 0 tolerances after seeing Phase 1+ results without a
  blocker note and review.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only when shape/import tests pass and the Phase 2 subplan
names the exact batched flow and transport core functions to implement, plus
the fixed-branch mask and transport tolerance policy they must preserve.

## Stop Conditions

Stop if the callback contract cannot preserve scalar semantics, if shape tests
require production API changes, if deterministic noise cannot be represented,
if fixed branch masks cannot be represented, or if hidden RNG is required for
the value/score core.

## End-Of-Phase Procedure

Run checks, write result, refresh Phase 2 subplan, and review Phase 2 for
consistency, feasibility, artifact coverage, and boundary safety.
