# Review Loop: 1D-to-Smoothness LGSSM Continuation Ladder

## Scope

This artifact records Claude Code review rounds and Codex-supervisor
classifications for
`docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-plan-2026-06-02.md`
and the corresponding result artifact.

Reviewer command:

```bash
claude -p --model claude-opus-4-7 --effort max
```

## Plan Review Round 1

Claude status: `REJECT`.

Codex-supervisor audit: all findings below are classified independently before
patching. No finding is silently ignored.

| Finding | Codex classification | Control added |
| --- | --- | --- |
| R1 handoff rule ambiguous; R2 should be evidence-bearing only if R1 clears fixed `1e-4` residual veto. | `ACCEPT` | Added explicit R1 rule that R2 is evidence-bearing only after fixed `1e-4` row/column residual pass. |
| If T=4 row residual around `5.23e-4` persists after R1, R1 is first failing rung and R2-R8 are blocked. | `ACCEPT` | Added `blocked_by_R1_residual_veto` rule. |
| Comparator manifest must record filterflow branch, commit SHA, and diff status. | `ACCEPT` | Added comparator manifest requirement and evidence scope limitation. |
| R4 "as closely as feasible" is too loose. | `ACCEPT` | Replaced with exact matched variables and diagnostic-only treatment for unavoidable unmatched variables. |
| R6/R7 gradient/scalar overclaim risk. | `ACCEPT` | Added scalar/forward/residual-only promotion policy for R6/R7. |
| Tolerance weakening too loose. | `ACCEPT` | Added fixed evidence-bearing residual tolerance and diagnostic-only weakened tolerance policy. |
| CPU-only must be a rung execution contract. | `ACCEPT` | Added rung-level CPU-only manifest requirement. |
| Comparator checkout must remain unchanged during ladder. | `ACCEPT` | Added restart requirement if comparator checkout changes. |
| Runner/result must record no student/vendored/highdim/DSGE/NAWM code paths were used. | `ACCEPT` | Added per-rung path-use manifest requirement. |

Patch applied to:

- `docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-plan-2026-06-02.md`

Next action: resubmit the patched plan to Claude.

## Plan Review Round 5

Claude status: `REJECT`.

Codex-supervisor audit: the finding is accepted. It is not a major blocker
after patching because it adds a deterministic tie-breaker without changing the
evidence question or weakening governance. Under the max-5 plan review rule,
the patched plan proceeds for user-inspection execution, not as Claude-accepted
plan text.

| Finding | Codex classification | Control added |
| --- | --- | --- |
| R1-to-R2 handoff did not define how to choose among multiple passing R1 cells. | `ACCEPT` | Added deterministic R1 selected-cell rule: least `max_iterations`, then loosest `convergence_threshold`, then smallest maximum absolute row residual; selected cell must be recorded for R2-R8. |

Patch applied to:

- `docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-plan-2026-06-02.md`

Plan review final status: `REJECT_patched_for_user_inspection_after_round_5`.

## Execution Summary Before Result Review

Execution proceeded after the max-5 plan review with the final Claude finding
patched. This is recorded as user-inspection execution, not as a
Claude-accepted plan.

Artifacts created:

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_to_smoothness_ladder_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-1d-to-smoothness-ladder-2026-06-02.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_to_smoothness_ladder_2026-06-02.json`
- `docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-result-2026-06-02.md`

Execution command:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_to_smoothness_ladder_tf
```

Execution decision: `one_d_to_smoothness_ladder_R2_veto`.

Main result:

- `R1_T4_residual_ladder`: pass after bounded sweep; selected inherited
  setting is `convergence_threshold=1e-6`, `max_iterations=500`.
- `R2_1d_horizon_ladder`: direct evidence-bearing veto at horizon `T=32`.
- `R3` through `R8`: blocked by `blocked_by_R2_horizon_32_veto`.

Verification completed before result review:

| Command | Result |
| --- | --- |
| `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_to_smoothness_ladder_tf.py` | pass |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_to_smoothness_ladder_tf` | pass; decision `one_d_to_smoothness_ladder_R2_veto` |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_to_smoothness_ladder_tf --validate-only` | pass |
| `python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_to_smoothness_ladder_2026-06-02.json` | pass |
| explicit JSON CPU manifest invariant check | pass |
| NumPy import gate on touched runner | pass; no matches |
| forbidden import-boundary search on touched runner | pass; no matches |
| lane-scoped trailing whitespace check | pass; no matches |
| `git diff --check` | pass |
| `git status --short -- bayesfilter tests docs/chapters` | pass; no output |

Next action: submit result artifacts to Claude review.

## Result Review Round 1

Claude status: `REJECT`.

Codex-supervisor audit: all result findings are accepted. The evidence is useful
but the wording needed to distinguish the executed scalar-prefix result from
the unexecuted full 1D-to-smoothness ladder.

| Finding | Codex classification | Control added |
| --- | --- | --- |
| Result overclaimed the R2 failure as answering the broader smoothness path rather than the executed scalar-horizon prefix. | `ACCEPT` | Changed JSON question and added `answer_scope` stating the run localizes only the executed R1/R2 scalar prefix. |
| Result lacked a strong caveat that R3-R8 were not exercised and therefore smoothness-relevant axes remain untested. | `ACCEPT` | Added markdown `Scope Caveat` and revised interpretation for R2. |
| Markdown collapsed direct R2 veto and inherited blockers into one `blocker_reason` column. | `ACCEPT` | Added separate `Inherited blocker` column to the rung ledger table. |
| Markdown omitted decisive R2 horizon-level evidence. | `ACCEPT` | Added `R2 Horizon Summary` table with horizon, status, scalar delta, residuals, and residual pass flag. |
| CPU-only, forbidden-lane, and NumPy-backend concerns were adequately addressed. | `ACCEPT` | No patch required beyond preserving existing controls. |

Patch applied to:

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_to_smoothness_ladder_tf.py`

Next action: rerun the ladder and verification to regenerate JSON/report/result
from the patched generator, then resubmit result review.

## Result Review Round 4

Claude status: `REJECT`.

Codex-supervisor audit: the finding is accepted. The artifact needs the
standard scientific decision table even though the governance-blocking language
is otherwise adequate.

| Finding | Codex classification | Control added |
| --- | --- | --- |
| Missing project-required decision table with decision, primary criterion status, veto diagnostic status, main uncertainty, next justified action, and what is not concluded. | `ACCEPT` | Added a `Decision Table` section to the generated markdown result/report. |
| Governance-safe blocking language is materially honest. | `ACCEPT` | No patch required beyond preserving the blocking language. |

Patch applied to:

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_to_smoothness_ladder_tf.py`

Next action: rerun the ladder and verification to regenerate JSON/report/result
from the patched generator, then resubmit final result review.

## Result Review Round 5

Claude status: `REJECT`.

Codex-supervisor audit: the finding is accepted and patched for inspection, but
the result review does not converge by the max-5 loop. The final status remains
`REJECT_patched_for_user_inspection_after_round_5`; downstream use remains
blocked unless the human explicitly authorizes it or review is reopened.

| Finding | Codex classification | Control added |
| --- | --- | --- |
| Human-readable result/report did not emit the full canonical per-rung ledger required by the plan, even though JSON did. | `ACCEPT` | Added generated `Canonical Per-Rung Ledger` sections for every rung, including comparator fingerprints, fixed/varied variables, primary metrics, veto diagnostics, and explanatory diagnostics. |

Patch applied to:

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_to_smoothness_ladder_tf.py`

Result review final status: `REJECT_patched_for_user_inspection_after_round_5`.

## Result Review Round 3

Claude status: `REJECT`.

Codex-supervisor audit: both findings are accepted. The technical diagnostic is
useful, but the result must not appear protocol-clean because plan review ended
at round 5 without Claude `ACCEPT`.

| Finding | Codex classification | Control added |
| --- | --- | --- |
| Result artifact was generated from a non-accepted plan state, which is a material protocol blocker. | `ACCEPT` | Changed top-level decision to `one_d_to_smoothness_ladder_protocol_blocked_inspection_only`, added `technical_observation_decision`, `protocol_status`, `downstream_use`, and a `Governance Blocker` section. |
| Review-loop did not record a fresh post-round-2 result-review section. | `ACCEPT` | Added this Result Review Round 3 section with classifications and controls. |

Patch applied to:

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_to_smoothness_ladder_tf.py`
- `docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-review-loop-2026-06-02.md`

Next action: rerun the ladder and verification to regenerate JSON/report/result
from the patched generator, then resubmit result review.

## Result Review Round 2

Claude status: `REJECT`.

Codex-supervisor audit: both findings are accepted. The JSON had the needed
comparator manifest, but the human-readable result did not expose it cleanly.

| Finding | Codex classification | Control added |
| --- | --- | --- |
| Human-readable result omitted comparator Python version, package manifest, exact command, and full local-diff status. | `ACCEPT` | Added comparator markdown block with path, HEAD commit, symbolic head, branch-status policy, Python version, diff digest, package-manifest digest, and exact filterflow command. |
| Markdown comparator table put multiline status inside one table cell. | `ACCEPT` | Moved local diff/status into a fenced text block. |

Patch applied to:

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_to_smoothness_ladder_tf.py`

Next action: rerun the ladder and verification to regenerate JSON/report/result
from the patched generator, then resubmit result review.

## Plan Review Round 4

Claude status: `REJECT`.

Codex-supervisor audit: all findings are accepted.

| Finding | Codex classification | Control added |
| --- | --- | --- |
| Comparator branch specification is stale because the symbolic branch may not be verifiable as a normal ref. | `ACCEPT` | Made HEAD commit plus local-diff/status fingerprint authoritative; branch string is descriptive only. |
| R1 finite sweep set and stop rule were missing. | `ACCEPT` | Added bounded R1 grid: `convergence_threshold in {1e-6,1e-7,1e-8}` and `max_iterations in {200,500,1000}`, with early stop only on fixed residual and scalar/ledger pass. |
| Result schema did not explicitly distinguish direct failure from inherited block. | `ACCEPT` | Added per-rung `failure_observed_directly` boolean in addition to `inherited_blocker`. |
| Verification did not explicitly check parent/subprocess CPU-only manifest fields. | `ACCEPT` | Added JSON invariant command checking parent and rung CPU-only manifests. |

Patch applied to:

- `docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-plan-2026-06-02.md`

Next action: resubmit the patched plan to Claude.

## Plan Review Round 3

Claude status: `REJECT`.

Codex-supervisor audit: three findings are accepted and one is partially
accepted. The stale-artifact finding is directionally useful, but the missing
runner is expected because the plan creates it; the patch clarifies that
distinction instead of replacing the planned artifact with the prior runners.

| Finding | Codex classification | Control added |
| --- | --- | --- |
| Allowed write set and verification reference a new runner that does not yet exist, while prior runners hold the R1 context. | `PARTIAL` | Added explicit statement that `run_filterflow_1d_to_smoothness_ladder_tf.py` and its JSON/report are new plan outputs, while prior 1D runners are read-only context inputs. |
| Comparator drift policy said both restart and block. | `ACCEPT` | Removed automatic restart language; canonical behavior is `blocked_by_comparator_drift` for current and later rungs. |
| CPU-only enforcement must include the filterflow subprocess manifest. | `ACCEPT` | Added subprocess inheritance of `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import and subprocess CPU-only manifest requirement. |
| Ledger could confuse first failing rung with first blocked rung. | `ACCEPT` | Added `first_blocked_rung` and `inherited_blocker` requirements at top level and per-rung level. |

Patch applied to:

- `docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-plan-2026-06-02.md`

Next action: resubmit the patched plan to Claude.

## Plan Review Round 2

Claude status: `REJECT`.

Codex-supervisor audit: both findings are materially correct and were patched.

| Finding | Codex classification | Control added |
| --- | --- | --- |
| Result artifacts could aggregate diagnostics without unambiguously answering where the continuation first fails. | `ACCEPT` | Added a canonical per-rung ledger contract with `rung`, `status`, `evidence_bearing`, `blocker_reason`, `first_failing_rung`, comparator fingerprints, fixed/varied variables, primary metrics, veto diagnostics, and explanatory diagnostics. |
| Comparator drift guard was not auditable without per-rung or start/end fingerprints. | `ACCEPT` | Added comparator fingerprint before R1 and after every rung, with `blocked_by_comparator_drift` if any field changes. |

Patch applied to:

- `docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-plan-2026-06-02.md`

Next action: resubmit the patched plan to Claude.
