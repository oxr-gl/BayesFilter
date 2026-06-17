# Phase 4 Claude Boundary Review: Batched Value+Score

Date: 2026-06-15

Reviewer: Claude Opus via bounded read-only worker.

## Prompt Scope

Claude reviewed a compact digest only. It was not asked to authorize execution
or inspect whole files. Codex remains supervisor and executor.

Digest reviewed:

- Phase 3 value parity passed for B=1 and B=20 under fixed deterministic
  tensors and masks.
- Phase 4 score target is TensorFlow autodiff gradient of the summed row-local
  relaxed batched values with respect to `theta_batch`.
- The score is not a classical particle-filter likelihood score.
- Finite-difference comparator uses the same fixed deterministic tensors and
  masks with predeclared `rtol=2e-4, atol=2e-4`.
- Finite-difference equivalence uses `raw` transport gradients only.
- No GPU, HMC/NeuTra, posterior-validity, production, or public API claims.

## Verdict

```text
VERDICT: AGREE
```

Key caveat accepted into execution:

- Row-locality must be enforced before interpreting
  `grad(sum(value), theta_batch)` as a per-row score tensor `[B,p]`.

## Phase 4 Impact

Execution will include an explicit row-locality test that perturbs a different
row's parameter and verifies the selected row value does not change within the
Phase 4 finite-difference tolerance.
