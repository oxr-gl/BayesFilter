# P0 Result: Target-Route Registry and Claim Classes

metadata_date: 2026-06-08
phase: P0
status: PASS_P0_TARGET_ROUTE_REGISTRY_READY_FOR_P1

## Question

Which model targets can support later DPF value and gradient comparison against
Kalman, UKF, SVD/sigma-point, CUT4, Zhao-Cui/fixed-design TT, bootstrap-OT DPF,
and LEDH-PFPF-OT DPF routes, and what claim class is allowed for each route?

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Build a governed target-route registry for later value and gradient comparisons without promoting non-oracles. |
| Baseline/comparator | P42 validation rules, P45 registry schema/blocker pattern, local code/test/document inventory, and master-program claim classes. |
| Primary criterion | Valid registry with every required target-route row, explicit claim class, tolerance/catalog band, gradient statistic where needed, blocker rows, and phase eligibility. |
| Veto diagnostics | Missing target identity, missing route status, missing tolerance or certification band, missing gradient statistic for P5-gradient-eligible rows, approximate route labeled exact, blocked route omitted, DPF row without seed/evaluator-variance policy. |
| Explanatory diagnostics | Route availability, governing source paths, route eligibility counts, blocked-row counts, implementation path strings, and target-family distribution. |
| Not concluded | No numerical filter comparison, DPF value or gradient correctness, HMC readiness, production readiness, GPU readiness, or paper-scale claim. |
| Preserving artifact | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-target-route-registry-2026-06-08.json` and `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p0_target_route_registry_2026-06-08.json`. |

## Skeptical Audit

Status: `PASS_FOR_P0_REGISTRY_VALIDATION`.

Wrong-baseline risk is controlled by making P0 a classification phase only.
Kalman, dense quadrature, CUT4, UKF, SVD/sigma-point, Zhao-Cui, and DPF rows are
not interchangeable references; each row carries its own claim class.

Proxy-promotion risk is controlled by requiring `promotion_tolerance`,
`certification_band`, `primary_gradient_statistic`, and nonclaims before later
execution. P0 counts and schema validity do not become value or gradient
evidence.

Missing-stop-condition risk is controlled by explicit `BLOCKED` rows and the
phase review loop. A blocked route is represented as evidence of non-execution,
not silently omitted.

Unfair-comparison risk is controlled by separating deterministic routes from
stochastic DPF routes and requiring DPF seed/evaluator-variance policy before
P5 comparisons.

Environment risk is low for P0 because the validator is pure Python, sets
`CUDA_VISIBLE_DEVICES=-1`, and does not import TensorFlow.

## Pre-Mortem

The registry could pass while misleading us if a target identity is too vague,
if an approximation row is later treated as exact, or if implementation-contract
evidence from prior DPF work is mistaken for same-target oracle evidence. The
mitigation is row-level claim classes, nonclaims, tolerances, and a read-only
Claude gate before advancing to P1.

The registry could fail for implementation reasons rather than scientific
reasons if the JSON schema and validator disagree. The cheap diagnostic is the
pure-Python validator plus `json.tool`, which passed.

## Commands Run

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

The same validator output was observed for the seed-registry validate-only run
and the summary-writing run.

After Claude review iteration 1, the validator and generated artifacts were
patched and the same command sequence was rerun. The rerun again produced:

```text
P0_REGISTRY_VALID targets=13 route_rows=104 blocked_rows=58
```

Repair checks:

- registry JSON now includes top-level `run_manifest`;
- summary JSON and registry JSON now carry the same manifest fields;
- non-DPF rows are rejected by the validator if they carry a DPF
  seed/evaluator policy;
- `lgssm_2d_h25_rich/kalman_exact` now has
  `N/A: deterministic, blocked, or not P1/P5 DPF execution row`;
- `lgssm_2d_h25_rich/dpf_bootstrap_ot` and
  `lgssm_2d_h25_rich/dpf_ledh_pfpf_ot` retain the paired seed/evaluator
  variance policy.

## Artifacts

- Registry JSON:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-target-route-registry-2026-06-08.json`
- Validator:
  `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p0_registry_tf.py`
- Summary JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p0_target_route_registry_2026-06-08.json`
- Visible ledger:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p0-claude-review-ledger-2026-06-08.md`

## Registry Summary

| Metric | Value |
| --- | ---: |
| Targets | 13 |
| Route IDs | 8 |
| Target-route rows | 104 |
| Blocked rows | 58 |
| DPF rows with seed/evaluator policy | 8 |

Claim classes:

| Claim class | Count |
| --- | ---: |
| `EXACT_ORACLE` | 6 |
| `CERTIFIED_APPROXIMATION` | 7 |
| `SURROGATE_USEFULNESS` | 2 |
| `DIAGNOSTIC_ONLY` | 31 |
| `BLOCKED` | 58 |

Phase eligibility:

| Phase | Eligible rows |
| --- | ---: |
| P1 | 7 |
| P2 | 15 |
| P3 | 5 |
| P4 | 5 |
| P5 | 12 |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `137f6ba5a03ebab199c8ab4699354d50bd560123` |
| Git branch | `main` |
| Command | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p0_registry_tf` |
| Environment | `active Python environment; observed executable is recorded in command` |
| Python version | `3.11.14` |
| CPU/GPU status | `pure_python_cpu_only; CUDA_VISIBLE_DEVICES=-1 set before validation; TensorFlow not imported` |
| CUDA visible devices | `-1` |
| Seeds | N/A: P0 is schema/governance validation only |
| Particle counts | N/A: P0 does not run DPF filters |
| Data version | N/A: no external data loaded |
| Timestamp UTC | `2026-06-08T15:51:41Z` |
| Wall time | `0.000668081920593977` seconds for the summary-writing validation |
| Registry path | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-target-route-registry-2026-06-08.json` |
| Summary path | `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p0_target_route_registry_2026-06-08.json` |
| Output artifact | `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p0_target_route_registry_2026-06-08.json` |
| Plan file | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p0-target-route-registry-subplan-2026-06-08.md` |
| Result file | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p0-target-route-registry-result-2026-06-08.md` |
| Scoped dirty state | P0 registry, summary, validator, result, Claude review ledger, and visible execution ledger were untracked/modified at validation time; broader dirty tree is pre-existing and not interpreted by P0. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `PASS_P0_TARGET_ROUTE_REGISTRY_READY_FOR_P1` | Passed: registry has 13 targets, 8 route IDs, 104 target-route rows, top-level manifest, and route-id-based DPF seed policy. | No validator veto fired after repair; blocked rows and nonclaims are explicit. Claude iteration 2b found no material P0 blockers. | P1 may still find execution or reference-binding issues specific to LGSSM numerical comparison. | Start P1 precheck only after restating the P1 evidence contract. | No numerical value/gradient closeness, DPF correctness, HMC readiness, or production readiness. |

## Post-Run Red-Team Note

Strongest alternative explanation: the registry may be internally complete but
too permissive for a later numerical phase if one of the approximation routes
is not tied to a same-target reference strongly enough.

Result that would overturn this P0 decision: Claude or a later precheck finds a
target-route row where an approximate or diagnostic route is mislabeled as
`EXACT_ORACLE`, a DPF row lacks a seed/evaluator-variance policy despite P5
eligibility, or a blocked native/non-Gaussian route was omitted.

Weakest part of the evidence: P0 validates governance structure and local
source references, not numerical correctness.

## Gate Status

P0 exits with `PASS_P0_TARGET_ROUTE_REGISTRY_READY_FOR_P1`.

Claude review iteration 1 returned `VERDICT: REVISE`; accepted findings were
patched and revalidated. Claude review iteration 2 hung with no output and was
recorded as a review-execution issue. Claude review iteration 2b returned
`VERDICT: AGREE` with no material P0 blockers.
