# P21 Zhao--Cui Implementation Readiness Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.

what_is_not_concluded:
- No executable prototype claim.
- No numerical finite-difference pass claim.
- No production implementation readiness claim.
- No full adaptive Zhao--Cui implementation claim.
- No HMC convergence claim.

## Readiness Checklist

| Requirement | Status | Evidence |
|---|---|---|
| fixed branch manifest | `SPECIFIED` | P21-66, P21-82 |
| array shapes | `SPECIFIED` | P21-65 and ledger rows |
| basis table | `SPECIFIED` | P21-72--P21-75 |
| target values | `SPECIFIED` | P21-6--P21-8, P21-58--P21-61 |
| core solve pseudocode | `SPECIFIED` | P21-76--P21-78 |
| mass contraction | `SPECIFIED` | P21-35--P21-39 |
| carried filter | `SPECIFIED` | P21-51--P21-57 |
| derivative pass | `SPECIFIED` | P21-80 |
| diagnostics | `SPECIFIED` | P21-81 |
| finite-difference protocol | `SPECIFIED` | P21-82--P21-87 |
| equation-to-spec traceability | `SPECIFIED` | equation-to-specification ledger |

## Readiness Decision

Decision before Claude review: `IMPLEMENTATION_READY_FOR_MINIMAL_FIXED_BRANCH_SPEC_ONLY`.

The artifact is ready for a later coding phase for the minimal fixed-branch
two-coordinate case.  It is not ready as a full adaptive Zhao--Cui production
implementation.
