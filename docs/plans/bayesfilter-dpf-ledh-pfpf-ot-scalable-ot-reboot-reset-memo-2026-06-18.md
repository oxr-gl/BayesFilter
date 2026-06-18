# Reboot Reset Memo: Scalable OT For LEDH-PFPF-OT

Date: 2026-06-18
Timestamp: 2026-06-18T04:25:00+08:00

## Reboot Status

The scalable OT master program is complete through Phase 10.

Final status:
`PHASE_10_COMPARATIVE_DECISION_COMPLETED_NO_DEFAULT_ALGORITHM_YET`

No BayesFilter default algorithm was changed.

## Final Decision

Do not select a production/default scalable OT algorithm yet.

The next justified program is a reviewed reduced-rank Nystrom ladder.  This is
only a next diagnostic target because Phase 4 validated the full-rank
TensorFlow factor route; it is not a speedup, ranking, scalability, posterior
correctness, or default-readiness claim.

## Lane State After Reboot

| Lane | State |
| --- | --- |
| Dense/streaming | Phase 1 comparator remains the local reference. |
| Nystrom | Full-rank factor route passed; reduced-rank ladder is next. |
| Positive-feature | Semantic-replacement diagnostic passed; not dense OT equivalence. |
| Low-rank coupling | `Q,R,g` transport-object diagnostic passed; solver fidelity untested. |
| Exact online/GPU | Reference-only; no GPU/external execution evidence. |
| Sparse/localized | Blocked for now by Phase 8 locality diagnostic on Phase 1 fixtures. |
| Sliced/subspace | Semantic-replacement diagnostic passed; dense discrepancy is explanatory. |
| Mini-batch/BoMb | Source-blocked; needs clean source/archive before decision-grade use. |

## Key Files

- Final decision:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p10-comparative-decision-result-2026-06-17.md`
- Detailed reset memo:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-reset-memo-2026-06-17.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-visible-stop-handoff-2026-06-17.md`
- Ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-visible-execution-ledger-2026-06-17.md`
- Survey:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex`

## Verification Already Run

- Phase 8 and Phase 9 diagnostic scripts compile.
- Phase 8 and Phase 9 official diagnostics ran and wrote JSON/Markdown.
- Phase 10 result/reset content check passed:
  `P10_RESULT_RESET_CONTENT_PASS`.
- Final artifact/status checks passed:
  `FINAL_ARTIFACTS_EXIST_PASS` and `FINAL_STATUS_CONTENT_PASS`.
- Claude read-only review for Phase 10 returned `VERDICT: AGREE`.

## Dirty Worktree Warning

Before this commit, unrelated dirty worktree files existed in BayesFilter
HMC/linear/test areas.  They were intentionally not part of the scalable OT
commit and must not be reverted after reboot unless the user explicitly asks.

## Next Safe Action

If continuing the research program after reboot, create a new reviewed subplan
for the reduced-rank Nystrom ladder with Phase 1 plus LEDH-specific fixtures,
predeclared dense-reference validity gates, memory/runtime proxy roles, and
explicit non-claims.
