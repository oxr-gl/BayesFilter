# Claude Pre-Review: BayesFilter-MacroFinance Stage 1 Latent Affine HMC Transform Round 01

Date: 2026-06-09

Reviewer: Claude via bounded read-only `claude_worker.sh` invocation
`bayesfilter-mf-stage1-pre-review-r1`

Scope:

- `docs/plans/bayesfilter_macrofinance_phase_1_latent_affine_hmc_transform_result_2026_06_09.md`
- `bayesfilter/inference/hmc.py`
- `tests/test_common_inference_runtime_contracts.py`
- `/home/ubuntu/python/MacroFinance/docs/plans/bayesfilter_macrofinance_hmc_filtering_consolidation_plan_2026_06_09.md`

Prompt constraints:

- read-only review only;
- do not edit files;
- do not run experiments;
- do not launch agents;
- do not run Codex;
- do not create a supervisor;
- do not invoke Claude internal skills/subagents;
- do not change repository state;
- Codex in the current conversation is supervisor and executor;
- Claude is a read-only reviewer only.

## Findings

Claude found three material precheck issues:

- The planned MacroFinance compatibility gate was weakened from the accepted
  plan's matched-DGP adapter check at `z=0` plus two Hessian-scaled stress
  directions to a possible small deterministic synthetic check.
- The precheck did not make inability to run the matched-DGP MacroFinance gate a
  repair trigger/stop condition; environment/import failure must be repaired,
  not used to weaken the baseline.
- The precheck did not explicitly require batched row-vector parity, so a
  scalar-only test could miss a left-multiply/column-vector bug.

Claude also noted that the statement about MacroFinance's exact
`tf.linalg.matvec(..., transpose_a=True)` implementation was unsupported within
the artifacts supplied for review and should be cited directly or softened.

Claude found no scalar-target or row-vector mismatch in the current BayesFilter
helpers, no proxy-metric promotion, and no broad BayesFilter/MacroFinance
ownership drift beyond the weakened compatibility gate.

## Raw Verdict

```text
VERDICT: NEEDS_REVISION
```

## Codex Disposition

Accepted all material findings. The Stage 1 precheck/result note was patched to
require the real matched-DGP MacroFinance compatibility gate, treat inability to
run it as a repair trigger, require batched parity, and soften/cite the
MacroFinance source assertion.
