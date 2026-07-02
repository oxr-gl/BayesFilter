# Reset memo: correcting the interpretation of the earlier retained-teacher heldout report

## Date
2026-06-28

## Context
The earlier retained-teacher heldout report was written before the source-faithfulness closure program and before the Meta OT-aligned one-half refit. Its decision token and overall framing made it too easy to read a local non-promotion result as if it were evidence that the retained-teacher algorithm itself had failed.

That reading is now too strong in light of the later work:
- the source-faithfulness program established that the earlier branches were not yet donor-faithful,
- the Meta OT-aligned refit showed that a much more donor-aligned route can be implemented coherently,
- and the new donor-aligned route still ended in local non-promotion under the current tiny heldout / high-budget contract, which means the original headline failure should be read much more narrowly.

## Decision / policy
Future sessions should assume the following and should not re-litigate them unless new evidence appears:

1. The earlier retained-teacher heldout report should **not** be summarized as “the algorithm failed.”
2. The correct reading is:
   - under the old local heldout contract,
   - on a tiny teacher-data artifact,
   - and at a binding high corrective budget where zero-init could already be exact,
   - the route was **not promoted**.
3. The source-faithfulness question and the local-promotion question are separate.
4. The Meta OT-aligned fixed-target retained-Sinkhorn refit is the correct substrate for further donor-aligned evidence gathering.
5. The annealed four-potential branch remains a later extension route and should not be used to reinterpret the older heldout report as paper failure.

## What changed
- File: `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithfulness-gap-note-2026-06-27.md`
  - Recorded that the earlier BayesFilter-native route and the annealed branch were not yet source-faithful closure evidence.

- File: `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p5-faithfulness-audit-result-2026-06-27.md`
  - Classified the fixed-target route as a fixed adaptation with major extension components and the annealed route as extension/invention.

- File: `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p6-closeout-result-2026-06-27.md`
  - Locked the route boundary: fixed-target retained-Sinkhorn is the correct donor-faithful substrate; annealed route is later extension work.

- File: `docs/plans/bayesfilter-neural-ot-metaot-refit-p4-heldout-replay-result-2026-06-28.md`
  - Showed that the donor-aligned one-half route is implemented and coherent, but still not promoted under the current heldout primary-budget rule.

- File: `docs/plans/bayesfilter-neural-ot-metaot-refit-p5-closeout-result-2026-06-28.md`
  - Closed the refit program with the correct conclusion: donor-aligned route implemented, but locally non-promoted under the current heldout contract.

- File: `docs/plans/bayesfilter-neural-ot-metaot-refit-better-evidence-contract-plan-2026-06-28.md`
  - Added a follow-on plan that explicitly separates discriminating budgets from saturated high-budget zero-init baselines.

## Bugs / blockers resolved
- Symptom:
  The earlier heldout report was easy to read as if the retained-teacher algorithm itself had failed.
- Root cause:
  The report answered a narrow local promotion question, but its `FAILED` framing and headline structure were stronger than the evidence contract really supported. It also predated the later source-faithfulness separation work.
- Resolution:
  The branch now has a clearer interpretation boundary:
  - donor faithfulness and local promotion are separate questions,
  - saturated high-budget zero-init rungs must not be over-read as algorithm failure,
  - and the follow-on plan now requires a better evidence contract.

## Verification already run
```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_teacher_data_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_heldout_eval_tf
```

Observed:
- The donor-aligned one-half route is implemented and numerically runnable.
- The teacher-data runner still succeeds under the updated route contract.
- The heldout evaluation still fails at the primary budget because zero-init is already effectively exact there.
- Low-budget rungs remain favorable to the donor-aligned route.
- This pattern supports “local non-promotion under the current contract,” not “algorithm failure.”

## Current policy
- Describe the earlier heldout report as a **local non-promotion result**, not an algorithm-failure result.
- When a baseline rung is already saturated by zero-init, do not use failure to beat that rung as headline evidence that the algorithm failed.
- Keep the fixed-target donor-aligned retained-Sinkhorn route as the current substrate for follow-on evidence gathering.
- Use the better evidence-contract plan before making stronger claims about usefulness or failure.

## Known limitations / cautions
- The current teacher-data artifact remains tiny.
- The donor-aligned refit is still not promoted under the present local heldout rule.
- No direct numerical parity study against the original Meta OT code has yet been run.
- The corrective memo changes interpretation, not the raw historical metrics themselves.

## Suggested next steps
1. Execute the better evidence-contract plan under `docs/plans/bayesfilter-neural-ot-metaot-refit-better-evidence-contract-plan-2026-06-28.md`.
2. Use a budget ladder with at least one explicitly discriminating rung where zero-init is not already exact.
3. Report the next result with headline language that separates:
   - donor-aligned implementation status,
   - local low-budget usefulness,
   - saturated-budget non-promotion,
   - and algorithm-level conclusions.
