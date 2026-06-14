# P8d Visible Repair Execution Plan

Date: `2026-06-13`

## Status

`PLAN_REVIEWED_READY_FOR_IMPLEMENTATION`

## Role Contract

Codex in this conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only. Claude must not edit files, run
experiments, launch agents, or change state.

No detached Codex agents, background supervisors, copied-workspace execution,
`setsid`, `nohup`, or overnight launcher scripts are allowed for this repair.

## Problem Being Fixed

P8c is the current valid numeric baseline and is partial by design:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-results-2026-06-13.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-summary-2026-06-13.md`

A P8d draft runner was created to close remaining cells, but it was not ready:

- the P8d plan incorrectly claimed execution readiness;
- the draft runner still had P8c metadata/status strings;
- `build_artifact()` still dispatched only the P8c executed cells;
- most non-LGSSM helper sketches were unused;
- non-LGSSM DPF callbacks were not complete;
- no P8d focused tests or Claude review had passed.

The current safety state is intentional: the P8d plan is paused and the P8d
runner refuses execution until the gates below pass.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we safely repair P8d so target-compatible remaining P8c holes are filled with reviewed numeric value/score cells, while preserving true not-applicable cells? |
| Baseline/comparator | P8c numeric artifact and the P8 source scope/adapter matrix. |
| Primary pass criterion | P8d emits a JSON/CSV/Markdown artifact with no silent holes: every executable deterministic cell has finite value and finite score when score is contractually meaningful; every executed DPF value cell is averaged over exactly five seeds; true invalid cells remain structured not-applicable. |
| Veto diagnostics | Exact Kalman outside LGSSM/KSC; spatial SIR gradient filled despite no free theta; old LEDH-PFPF-OT evidence used; proxy route reported as native/source-faithful; DPF value without five seeds; nonfinite value or score hidden as executed; stale P8c metadata in P8d artifact; Claude review `VERDICT: REVISE` unresolved after five rounds. |
| Explanatory diagnostics | Runtime, ESS, MC standard error, score norms, finite-difference spot checks, hessian availability, and route nonclaims. |
| Not concluded | Full filter ranking, exact nonlinear truth for non-Gaussian models, Bayesian estimation readiness, DPF gradient validity, or production Zhao-Cui TT/SIRT equivalence unless explicitly evidenced. |
| Artifacts | This plan, Claude review ledgers, P8d tests, P8d JSON/CSV/Markdown outputs, and final result note. |

## Skeptical Plan Audit

Status: `PASS_REVIEWED_BEFORE_EXECUTION`.

The plan must not treat the phrase "fill cells" as permission to fabricate
values. Some cells are real not-applicable:

- exact Kalman outside LGSSM or the declared KSC Gaussian-mixture surrogate;
- spatial SIR scores and Hessians because the P8 row has `truth_theta=[]`;
- DPF scores and Hessians because there is no reviewed P8 DPF gradient
  contract.

The remaining holes split into adapter work and callback work. A cell may be
filled only if a focused smoke check produces finite output and the artifact
names the route honestly.

## Claude Plan Review

Claude review status: `VERDICT: AGREE`.

Review note:

- Opus/max file-reading review prompts stalled twice after a successful
  one-line Claude liveness probe (`PROBE_OK`).
- A bounded inline read-only review returned `VERDICT: AGREE`.
- Claude's caveats are adopted as implementation gates:
  - P8c must be labeled as partial comparator-only evidence, not a full
    scientific baseline.
  - target compatibility must be enforced mechanically from the current source
    scope/adapter matrix, not by convenience at edit time.
  - non-executed cells must remain explicitly unfilled by policy, not inferred
    or backfilled from prior artifacts.

## Phase Index

| Phase | Name | Gate |
| --- | --- | --- |
| 0 | Plan review | Claude read-only review returns `VERDICT: AGREE`, or this plan is revised up to five rounds. |
| 1 | Runner metadata and safety | P8d artifact schema/phase/status are P8d; runner remains disabled until tests pass. |
| 2 | Deterministic adapters | UKF/SVD/CUT4 and safe dense/Zhao-Cui-style routes produce finite smoke values/scores where claimed. |
| 3 | DPF value callbacks | Bootstrap and LEDH Alg1 value cells run exactly seeds `[81120, 81121, 81122, 81123, 81124]` for each model whose callbacks pass finite smoke checks. |
| 4 | Focused tests and local audit | Pytest, compile, JSON/CSV checks, and `git diff --check` pass. |
| 5 | Claude implementation review | Claude read-only implementation review returns `VERDICT: AGREE`, or repairs converge in at most five rounds. |
| 6 | Enable and run P8d | Remove the draft safety stop only after gates pass; run CPU-only P8d; write final result note. |

## Cell Policy

| Cell family | Policy |
| --- | --- |
| LGSSM exact Kalman | Keep P8c differentiated-Kalman value/score/Hessian path. |
| LGSSM UKF/SVD/CUT4 | Use affine-equivalence differentiated-Kalman score/Hessian only after value tieout; do not claim native eigensystem sigma-point derivative. |
| KSC SV Kalman/UKF/SVD/CUT4 | Use declared KSC Gaussian-mixture surrogate routes; label as surrogate, not native SV. |
| Raw SV UKF/SVD/CUT4 | Use raw-observation augmented-noise structural route only if smoke value/score finite; label as sigma-point approximation, not exact likelihood. |
| Predator-prey UKF/SVD/CUT4 | Use additive-Gaussian structural route only if finite; label as P8 synthetic fixture route. |
| Generalized SV UKF/SVD/CUT4 | Use prior-mean generalized-SV synthetic route only if finite; label route and approximation. |
| Spatial SIR UKF/SVD/CUT4 | Value-only if finite; score/Hessian remain `not_applicable_no_free_theta`. |
| Zhao-Cui scalar/multistate | Fill only routes backed by existing reviewed fixed-branch/source-route code; otherwise leave explicit route gap. Do not claim adaptive MATLAB TT-cross/SIRT reproduction unless actually implemented. |
| DPF bootstrap/LEDH Alg1 | Value-only, five seeds, MC SE required. No score/Hessian promotion. |

## Stop Conditions

Stop and write a blocker note if:

- a route requires new algorithmic implementation rather than adapter wiring;
- a focused smoke run is nonfinite;
- a claimed same-target route is actually a diagnostic/proxy;
- a cell would require changing pass criteria after seeing results;
- Claude and Codex do not converge after five review rounds;
- continuing requires package installation, network fetch, credentials, GPU use,
  destructive git action, or detached execution.

## Planned Commands

CPU-only local checks:

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-visible-repair-execution-plan-2026-06-13.md scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

Claude review wrapper:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name p8d-readonly-review --model opus --effort max "<prompt>"
```

## Final Artifact Targets

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-numeric-results-2026-06-13.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-value-table-2026-06-13.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-score-table-2026-06-13.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-curvature-table-2026-06-13.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-status-table-2026-06-13.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-stochastic-uncertainty-table-2026-06-13.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-numeric-summary-2026-06-13.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-repair-execution-result-2026-06-13.md`
