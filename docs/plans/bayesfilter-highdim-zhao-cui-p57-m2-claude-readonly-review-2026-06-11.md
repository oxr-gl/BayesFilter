# P57-M2 Claude Read-Only Review

metadata_date: 2026-06-11
phase: P57-M2
reviewer: Claude Code Opus max-effort, read-only
supervisor: Codex

## Iteration 1

Verdict:

`VERDICT: REVISE`

Summary:

- Claude found a material artifact/evidence mismatch.
- The M2 subplan/result language required fixed TT cores and defensive density,
  but the initial implementation only enforced source-route method presence and
  finite normalizer.
- Codex accepted the stricter critique even though a tiny M2 prompt returned
  `VERDICT: AGREE`.

Disposition:

- Accepted.
- Added `source_contract_level` metadata.
- Added production `fixed_ttsirt` metadata requirements:
  `tt_cores_declared=True` and `defensive_density_declared=True`.
- Labeled analytic doubles as `contract_test_double`.
- Revised M2 result wording to avoid overstating TT-core/defensive-density
  implementation.

## Iteration 1 Verbatim Finding

```text
One material issue:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m2-fixed-ttsirt-transport-contract-subplan-2026-06-11.md:11` defines the M2 primary pass criterion as requiring fixed TT cores and defensive density in addition to the KR/eval/marginalization surface. But the actual contract implementation in `bayesfilter/highdim/source_route.py:383-407` and `bayesfilter/highdim/source_route.py:509-518` only enforces method presence plus a finite scalar `log_normalizer`; it does not check any TT-specific structure or any defensive-density/tau invariant. The passing transport double in `tests/highdim/test_p57_m2_fixed_ttsirt_transport_contract.py:26-68` is likewise a generic analytic scale map with no TT cores or defensive-density machinery, yet `docs/plans/bayesfilter-highdim-zhao-cui-p57-m2-fixed-ttsirt-transport-contract-result-2026-06-11.md:11-12` records the primary criterion as PASS. That makes the result broader than the evidence actually established. I would either narrow the stated primary criterion/result wording to the API-surface contract that was proven, or add explicit TT/defensive-density invariants and tests.

VERDICT: REVISE
```

## Tiny Prompt Result

A tiny fallback prompt returned `VERDICT: AGREE` for M2 as an API-surface
contract gate. Codex did not use that to close M2 because the fuller review
identified a real issue.

## Repair Review

Verdict:

`VERDICT: AGREE`

Summary:

- Claude agreed the repair closes the iteration-1 blocker.
- Claude verified `source_contract_level` is required.
- Claude verified production `fixed_ttsirt` transports require both
  `tt_cores_declared` and `defensive_density_declared`.
- Claude verified analytic doubles are labeled `contract_test_double`.
- Claude verified the result note no longer overclaims production TTSIRT.
