# P26 Zhao--Cui Discrepancy Report

metadata_date: 2026-06-03

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.
- P25 Zhao--Cui chair and implementation bridge note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No adaptive global differentiability claim.
- No production implementation claim.
- No empirical validation claim.
- No unresolved discrepancy has been accepted as harmless.

## Status

status: `NO_UNRESOLVED_CLAUDE_CODEX_DISCREPANCY`

## Review Discrepancies

No Claude finding remains disputed.

Claude execution review iteration 1 returned `REVISE`. Codex classified the
findings as `ACCEPT` or `PARTIAL`; all accepted and partially accepted items
were patched.

Claude execution review iteration 2 returned `REVISE` with three remaining
human-facing wording blockers. Codex classified all three as `ACCEPT` and
patched the main note:

- Removed visible project branding from the main note.
- Removed visible `lane` wording from the main note.
- Retitled the implementation-facing section to `Fixed-Branch Objects And
  Array Shapes`.

## Remaining Non-Discrepancy Caveats

- P26 does not prove exact posterior accuracy.
- P26 does not prove global differentiability of adaptive TT-cross,
  rank-changing, or pivot-changing algorithms.
- P26 does not provide empirical evidence that the approximation is accurate
  for a particular high-dimensional chemistry or filtering model.
- P26 does not claim endorsement by an actual panel chair.

## Final Acceptance Condition

Final acceptance is limited to the documented scope: P26 is an expanded,
panel-readable mathematical and implementation-specification note with a
compiled PDF and reviewed cleanup of the requested P25 gaps.
