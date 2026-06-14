# DPF LEDH-PFPF Source-Faithful Repair Claude Review Ledger

Date: 2026-06-10

Plan:
`docs/plans/bayesfilter-dpf-ledh-pfpf-source-faithful-repair-plan-2026-06-10.md`

Reviewer: Claude Code read-only.

Supervisor/executor: Codex.

## Iteration 1

Command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name dpf-ledh-pfpf-source-faithful-repair-plan-review-iter1 \
  "<bounded read-only plan review prompt>"
```

Verdict: `VERDICT: REVISE`.

Accepted findings:

- Forbid the escape hatch where the current collapsed shortcut is retained and
  only its exact/autodiff determinant is substituted.
- Require a run manifest in the result artifact.
- Add a pre-mortem separating wrong-algorithm, numerical, and implementation
  failures.
- Require the result artifact to preserve a decision table and nonclaims.

Codex action: patched the plan.

## Iteration 2

Command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name dpf-ledh-pfpf-source-faithful-repair-plan-review-iter2 \
  "<bounded read-only plan rereview prompt>"
```

Verdict: `VERDICT: AGREE`.

Claude agreed that the plan:

- correctly reclassifies the P8 M3 LEDH-PFPF issue as a source-faithfulness
  implementation bug;
- forbids the exact-Jacobian-of-the-wrong-collapsed-shortcut route;
- includes sufficient evidence contract, vetoes, run manifest, pre-mortem,
  decision-table, CPU-only controls, and nonclaims;
- remains consistent with the TensorFlow/TFP backend policy.

## Plan Review Decision

`PLAN_REVIEW_CONVERGED_VERDICT_AGREE_ITERATION_2`

Execution may proceed visibly under the reviewed plan.

## Result Review Iteration 1

Command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name dpf-ledh-pfpf-source-faithful-repair-result-review-iter1 \
  "<bounded read-only result review prompt>"
```

Verdict: `VERDICT: AGREE`.

Claude agreed that:

- execution followed the accepted source-faithful auxiliary-flow LEDH/PF-PF
  plan;
- the runner enforces CPU-only before TensorFlow import;
- the M3 route computes coefficients from `bar_eta`, migrates actual particle
  `eta` by the same affine step, and accumulates
  `log |1 + epsilon_j A_j^i|`;
- branch diagnostics and veto logic exclude both the collapsed shortcut and the
  exact-Jacobian-of-collapsed-shortcut escape hatch;
- run manifest, decision table, determinant diagnostics, nonclaims, and the P8
  amendment are present and consistent with the accepted scope.

## Result Review Decision

`RESULT_REVIEW_CONVERGED_VERDICT_AGREE_ITERATION_1`
