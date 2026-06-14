# P0 Claude Review Ledger: Target-Route Registry

metadata_date: 2026-06-08
phase: P0
status: PASS_P0_TARGET_ROUTE_REGISTRY_READY_FOR_P1

## Role Contract

Codex is supervisor and executor in this dialogue.

Claude is a read-only critical reviewer only. Claude must not edit files, run
experiments, launch agents, or change state.

## Reviewed Artifacts

- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-master-program-2026-06-08.md`
- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p0-target-route-registry-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-target-route-registry-2026-06-08.json`
- `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p0_registry_tf.py`
- `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p0_target_route_registry_2026-06-08.json`
- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p0-target-route-registry-result-2026-06-08.md`
- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md`

## Review Protocol

Claude must check wrong baselines, proxy metrics being treated as promotion
criteria, missing stop conditions, unfair comparisons, hidden assumptions, stale
context, environment mismatches, unsupported oracle claims, missing P0 artifacts,
and whether the artifacts answer the P0 question.

Claude must end with exactly:

```text
VERDICT: AGREE
```

or:

```text
VERDICT: REVISE
```

Codex must classify every Claude finding as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
`CLARIFY`. Accepted material findings require a patch and another review
iteration. Maximum review iterations: 5.

## Iteration 1

Status: `VERDICT: REVISE`.

Claude findings:

- Primary registry JSON lacked a required top-level `run_manifest`.
- Summary JSON manifest was incomplete relative to the markdown result
  manifest and did not satisfy the master-program same-manifest rule.
- `lgssm_2d_h25_rich/kalman_exact` carried a DPF seed/evaluator policy because
  the generator keyed on `"dpf"` in `route_path` rather than on `route_id`.

Codex-supervisor classification:

| Finding | Classification | Patch/control added |
| --- | --- | --- |
| Registry missing top-level `run_manifest` | `ACCEPT` | Validator now writes and requires top-level registry `run_manifest`; existing-registry validation requires it. |
| Summary and markdown manifests did not match the required fields | `ACCEPT` | Manifest now includes environment, seeds, particle counts, data version, registry path, summary/output path, plan path, result path, and scoped dirty state. Result manifest was updated to summarize the same fields. |
| Non-DPF Kalman row carried DPF seed/evaluator policy | `ACCEPT` | Seed/evaluator policy assignment now keys on `route_id.startswith("dpf_")`; validator rejects DPF policy text on non-DPF rows and on non-execution DPF rows. |

Repair validation:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p0_registry_tf.py
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p0_registry_tf --write-seed-registry --validate-only
python -m json.tool docs/plans/bayesfilter-dpf-filter-oracle-comparison-target-route-registry-2026-06-08.json
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p0_registry_tf
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p0_target_route_registry_2026-06-08.json
```

Observed validator output:

```text
P0_REGISTRY_VALID targets=13 route_rows=104 blocked_rows=58
```

Decision after patch: rerun Claude P0 gate review iteration 2.

## Iteration 2

Status: `REVIEW_EXECUTION_HUNG_STOPPED_NO_VERDICT`.

Claude output: none before timeout/stop.

Codex-supervisor classification:

| Issue | Classification | Control |
| --- | --- | --- |
| Claude read-only review process stayed alive for more than eight minutes with no output | `REVIEW_EXECUTION_ISSUE` | Stopped only the stuck review process and will retry with a smaller prompt as iteration 2b. No P0 evidence is inferred from the hung call. |

## Iteration 2b

Status: `VERDICT: AGREE`.

Claude output summary:

- No material P0 blockers found.
- Registry JSON has top-level `run_manifest`.
- Summary JSON carries the same manifest field set.
- `lgssm_2d_h25_rich/kalman_exact` has `N/A` seed/evaluator policy.
- LGSSM DPF rows retain paired-seed policy.
- Validator keys policy assignment on `route_id.startswith("dpf_")` and
  rejects non-`N/A` DPF policy on non-DPF rows and non-execution DPF rows.
- Final line: `VERDICT: AGREE`.

Codex-supervisor classification:

| Finding | Classification | Decision |
| --- | --- | --- |
| No remaining material P0 blocker | `ACCEPT` | P0 gate passes. |

Outcome: `PASS_P0_TARGET_ROUTE_REGISTRY_READY_FOR_P1`.
