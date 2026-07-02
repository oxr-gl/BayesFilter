# Streaming Manual VJP Phase 7R Subplan: Metadata Remediation

status: READY_FOR_CLAUDE_REVIEW
date: 2026-06-23
phase: S7R-METADATA-REMEDIATION

## Phase Objective

Repair the S7 actual-gradient harness metadata contract, then rerun the
trusted GPU ladder from N100 only after the remediation subplan passes bounded
review.  The goal is to make the JSON artifacts emit the exact keys required by
the reviewed S7 validation contract without changing the scientific question,
route, defaults, or pass/fail criteria.

## Entry Conditions

- S7 result status is `BLOCKED_N100_METADATA_CONTRACT`.
- S7 blocker result passed bounded Claude review.
- N100 compute evidence was finite on GPU but did not satisfy metadata keys.
- No valid N10000 actual-gradient artifact exists.
- S8/P82 FD remains prohibited.

## Required Artifacts

- Remediation result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7r-metadata-remediation-result-2026-06-23.md`
- Updated S7 rung JSON artifacts if rerun under this remediation.
- Updated execution ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-execution-ledger-2026-06-23.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-claude-review-ledger-2026-06-23.md`
- Updated visible stop handoff:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-stop-handoff-2026-06-23.md`

## Required Checks/Tests/Reviews

Patch only `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
and `tests/highdim/test_p82_regression_fd_harness_protocol.py` unless a
focused check proves another file is necessary.

Required harness metadata keys to add or prove present:

- top-level `status`;
- top-level `primary_pass`;
- top-level `batch_seeds`;
- `transport.dense_transport_matrix_materialized`.

Add focused protocol tests that construct or parse a tiny no-run artifact path
or inspect the harness result-building logic to prove these keys are emitted
without launching GPU work.

CPU-hidden checks:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q
```

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
```

```text
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7r-metadata-remediation-subplan-2026-06-23.md
```

After CPU-hidden checks pass, write the remediation result and obtain bounded
Claude review of that result.  Only a reviewed remediation result may authorize
rerunning the exact S7 GPU ladder from N100 under trusted/elevated permissions.
Do not skip N100.  Do not advance past any rung whose JSON fails exact
validation.

Claude review required:

- bounded exact-path review of this remediation subplan before edits;
- bounded exact-path review of the remediation result after CPU-hidden metadata
  checks and before any GPU rerun;
- if a reviewed remediation result authorizes and completes a GPU rerun, update
  the same remediation result with rerun outcomes and request a second bounded
  exact-path review before any S8 handoff.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can we repair the S7 harness metadata so actual-gradient JSON artifacts satisfy the predeclared exact validation keys without changing the route or scientific criteria? |
| Baseline/comparator | S7 N100 blocker artifact and S7 reviewed validation contract. |
| Primary pass criterion | CPU-hidden tests and compile/diff checks pass; emitted/rerun JSON contains the four missing keys with correct values; rerun rungs, if launched, satisfy the original S7 exact metadata validation before advancement. |
| Veto diagnostics | Route changed away from the new blockwise route; defaults changed; `transport_ad_mode=full`; FD launched; metadata keys added post hoc to old JSON without rerun; GPU rerun before the CPU-hidden remediation result passes bounded review; N100 skipped; any rerun rung fails exact validation. |
| Explanatory only | Runtime, allocator warnings, N100 finite values, and smaller-rung trends. |
| Not concluded | No FD agreement, no N10000 feasibility unless the rerun reaches and validates N10000, no HMC/default readiness, no production readiness. |

## Forbidden Claims/Actions

- Do not edit old JSON artifacts by hand to make them pass.
- Do not launch P82 FD.
- Do not use `transport_ad_mode="full"`.
- Do not change the S7 route, default route, default policy, public API
  exposure, HMC policy, model/funding boundaries, or scientific criteria.
- Do not skip N100 on rerun.
- Do not claim N10000 feasibility unless a rerun creates a valid N10000 JSON
  satisfying the original S7 validation contract.

## Exact Next-Phase Handoff Conditions

If remediation passes and rerun reaches a valid N10000 artifact, refresh/review
S8 with that exact artifact path.

If remediation fails or any rerun rung fails, write the remediation result as
blocked, update the stop handoff, and keep S8/P82 FD prohibited.

## Stop Conditions

Stop if:

- the harness cannot emit required metadata without broad refactoring;
- tests fail and cannot be repaired within this narrow metadata scope;
- a GPU rerun would require changing route, criteria, defaults, or scientific
  claims;
- Claude review does not converge within five rounds for the same blocker.

## Skeptical Plan Audit

Audit result before execution: pass.  The S7 blocker was caused by missing
metadata keys, not by failed N100 compute.  This remediation is narrowly scoped
to harness artifact metadata and rerun validation.  It must not relax the
reviewed S7 validation contract or reuse the old N100 JSON as if it passed.

## End-Of-Phase Protocol

1. Review this subplan with Claude using one exact path.
2. Patch the harness/tests if review passes.
3. Run CPU-hidden checks.
4. Write the remediation result.
5. Review the CPU-hidden remediation result with Claude.
6. Only then rerun trusted GPU rungs from N100 if the reviewed result
   explicitly authorizes it, stopping at the first failed rung.
7. Update the remediation result with rerun outcomes and request a second
   bounded Claude result review before any S8 handoff.
