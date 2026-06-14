# P3 Result: Reference Oracle Wiring

metadata_date: 2026-06-10
phase: FILTER_BENCH_P3
status: PASS_FILTER_BENCH_P3_REFERENCE_ORACLES
supervisor: Codex
reviewer: Claude Code read-only

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Does each model row have a reference route suitable for value and gradient error reporting? |
| Baseline/comparator | LGSSM Kalman, P44 dense nonlinear references, exact transformed SV reference, KSC Gaussian-mixture enumeration, native generalized SV dense reference, P47/P51/P53 spatial SIR and predator-prey route evidence. |
| Primary criterion | Met after Claude review: every P1 row is bound to a reference route or explicit blocked-only reason, row class, reference type, value policy, gradient policy, diagnostics, evidence tests, and nonclaims. |
| Veto diagnostics | Not fired locally in the manifest: UKF/CUT4/Zhao-Cui are not reference truths; transformed SV actual and KSC surrogate rows are distinct; native raw-y generalized SV is not confused with transformed SV; d=18 spatial SIR is retained as blocked-only. |
| Nonclaims | No algorithm ranking, no DPF gradient certification, no HMC/GPU/Bayesian-estimation readiness, and no closed-form exactness for dense numerical references. |

## Artifacts

- Reference-oracle manifest: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-reference-oracles-2026-06-10.json`
- Focused manifest test: `tests/highdim/test_filtering_value_gradient_benchmark_reference_oracles.py`
- Visible ledger: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-execution-ledger-2026-06-10.md`

## Row Policy Summary

| Row family | Reference policy | Gradient-error policy |
| --- | --- | --- |
| LGSSM | exact Kalman | reference gradient available |
| P44 cubic/quadratic/nonlinear h2 | dense numerical same-target references | reference gradients available |
| P44 nonlinear h4 | diagnostic dense reference | diagnostic value/gradient only, no Zhao-Cui horizon-4 promotion |
| transformed SV actual | dense actual non-Gaussian transformed reference | reference gradient available |
| KSC SV surrogate | Gaussian-mixture Kalman enumeration | surrogate lane only, reference gradient available for surrogate target |
| native generalized SV | lower-rung dense raw-y reference | reference gradient available |
| spatial SIR J=1 | lower-rung dense reference | value-only, no theta-gradient coordinate |
| spatial SIR d=18 | blocked-only | `BLOCK_P53_M5_RANK_SELECTION_INTEGRATION` |
| predator-prey lower rung/h25 | dense references | value-only until a certified reference gradient exists |

## Validation

Commands planned/run:

```bash
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-reference-oracles-2026-06-10.json >/dev/null
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_reference_oracles.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_filtering_value_gradient_benchmark_reference_oracles.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-reference-oracles-2026-06-10.json tests/highdim/test_filtering_value_gradient_benchmark_reference_oracles.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p3-reference-oracles-result-2026-06-10.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-execution-ledger-2026-06-10.md
```

Results:

```text
json.tool exited 0
initial pytest found one validator false positive on a row id containing cut4
test repaired to inspect reference route fields only
5 passed in 0.05s
compileall exited 0
git diff --check exited 0
Claude minor repair applied: evidence nodeids now verify exact test functions, and the h4 diagnostic row is `diagnostic_only`
post-repair json.tool exited 0
post-repair 5 passed in 0.06s
post-repair compileall exited 0
post-repair git diff --check exited 0
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | dirty worktree; P3 artifacts uncommitted |
| Environment | local Python environment |
| CPU/GPU status | CPU-only manifest validation with `CUDA_VISIBLE_DEVICES=-1`; no GPU conclusion |
| Random seeds | N/A, manifest/schema validation only |
| Wall time | focused pytest 0.06s after Claude minor repair |
| Plan | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p3-reference-oracles-subplan-2026-06-10.md` |
| Result | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p3-reference-oracles-result-2026-06-10.md` |
| Manifest | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-reference-oracles-2026-06-10.json` |

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass P3 | Reference-oracle manifest covers every P1 row with value/gradient policy; local validation passed; Claude returned `VERDICT: AGREE`; minor cautions repaired | No approximate filter promoted to reference truth; no SV target mix-up; blocked d=18 row retained | Later phases must wire executable filter adapters and compute actual benchmark cells | Advance to P4 deterministic filter wiring | Filter ranking, DPF gradient correctness, HMC/GPU/Bayesian-estimation readiness |

## Claude Read-Only Review

Claude iteration 1 returned:

```text
VERDICT: AGREE
```

Minor repairs applied after review:

- the focused validator now parses cited Python files and verifies the exact
  evidence test function exists;
- the h4 nonlinear-transition diagnostic row is explicitly classified as
  `diagnostic_only`, while keeping `reference_type=diagnostic` and
  `reference_value_policy=diagnostic_reference_value_available`.

Required token:

`PASS_FILTER_BENCH_P3_REFERENCE_ORACLES`
