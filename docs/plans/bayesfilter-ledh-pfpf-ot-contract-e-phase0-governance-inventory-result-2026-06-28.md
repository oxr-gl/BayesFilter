# Phase 0 Result: Contract E governance, math anchors, and route inventory

Date: 2026-06-28

Status: `PHASE0_PASSED`

Master program:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-residual-affine-testing-master-program-2026-06-28.md`

Runbook:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-visible-gated-execution-runbook-2026-06-28.md`

## Phase Objective

Freeze the exact Contract E test target and inventory the current math,
diagnostic, and implementation paths before any implementation edit.

## Commands Run

Contract E LaTeX anchor inventory:

```bash
rg -n "Contract E|prop:bf-eot-positive-spread-gap|prop:bf-eot-residual-expected-covariance|prop:bf-eot-residual-support-repair|prop:bf-eot-residual-affine-restoration|eq:bf-eot-residual-affine-map" \
  docs/chapters/ch32c_entropic_ot_sinkhorn.tex
```

Existing diagnostic path check:

```bash
test -s docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_reset_variants.py &&
test -s docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py &&
test -s tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py
```

Route inventory scan:

```bash
rg -n "streaming_batched_ledh_pfpf_ot_value_core_tf|streaming_batched_ledh_pfpf_ot_value_and_score_tf|transport_ad_mode|jit_compile|tf\\.while_loop|while_loop|sinkhorn_iterations|row_chunk|col_chunk|particle_chunk" \
  experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py \
  experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py \
  tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py \
  docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_reset_variants.py \
  docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py
```

Comparator/forbidden-action scan:

```bash
rg -n "Zhao-Cui|transport_ad_mode=full|central FD|13-point|FD regression|same-scalar|Kalman" \
  docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-*.md \
  docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-reset-root-cause-debug-plan-2026-06-27.md \
  docs/plans/bayesfilter-p8p-sir-sinkhorn-budget-hypothesis-diagnostic-plan-2026-06-27.md
```

Targeted Contract E content inspection:

```bash
sed -n '886,930p' docs/chapters/ch32c_entropic_ot_sinkhorn.tex
sed -n '958,972p' docs/chapters/ch32c_entropic_ot_sinkhorn.tex
sed -n '1046,1060p' docs/chapters/ch32c_entropic_ot_sinkhorn.tex
sed -n '1098,1110p' docs/chapters/ch32c_entropic_ot_sinkhorn.tex
sed -n '1160,1184p' docs/chapters/ch32c_entropic_ot_sinkhorn.tex
```

No GPU, long benchmark, production-code edit, or numerical evidence command was
run in Phase 0.

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Passed: Phase 0 confirms the documented Contract E target and scoped evidence boundaries. |
| Baseline/comparator | Existing barycentric reset diagnostics and Contract E LaTeX anchors were used. |
| Primary pass criterion | Passed: exact math anchors, targeted content inspection, diagnostic paths, route candidates, forbidden comparators/actions, reviewed master/runbook status, ledgers, and Phase 1 handoff are recorded below. |
| Veto diagnostics | No missing Contract E anchor, missing existing diagnostic path, Zhao-Cui oracle, or full-transport AD plan was found in Phase 0.  No CPU/GPU evidence command was run, and no CPU result is claimed as GPU evidence. |
| Explanatory diagnostics | Worktree is dirty and contains many unrelated existing changes; Phase 0 added only scoped Contract E plan/result artifacts. |
| Not concluded | Preserved: no implementation correctness, value/gradient correctness, production readiness, HMC readiness, or posterior correctness. |

## Contract E Math Anchors

The exact Contract E target for this program is anchored in:

- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex:886`
  `Contract E: positive spread, residual noise, and affine restoration`
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex:964`
  `prop:bf-eot-positive-spread-gap`
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex:1051`
  `prop:bf-eot-residual-expected-covariance`
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex:1103`
  `prop:bf-eot-residual-support-repair`
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex:1163`
  `eq:bf-eot-residual-affine-map`
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex:1179`
  `prop:bf-eot-residual-affine-restoration`

Phase 1 must test the finite weighted-cloud algebra implied by these anchors:
positive first-order transform input, positive residual gap, residual support
repair, affine restoration, and conditioning gates.

The targeted `sed` inspection confirmed the substantive Contract E text:

- the three-stage map \(D_B\to D^+\to\widetilde Y\to Y^\star\);
- the non-overclaim that the exact hybrid was not found in inspected sources;
- the residual gap definition \(G_+=\Sigma_w-\Sigma_+\);
- the residual expected-covariance proposition;
- the support-repair proposition;
- the affine restoration map and proposition.

## Existing Diagnostic Anchors

The current evidence baseline remains:

- `docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-reset-root-cause-debug-plan-2026-06-27.md`
- `docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_reset_variants.py`
- `docs/plans/bayesfilter-p8p-sir-sinkhorn-budget-hypothesis-diagnostic-plan-2026-06-27.md`
- `docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py`
- `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py`

Those artifacts are baselines and scaffolding.  They do not already implement
or validate Contract E.

## Route Inventory

Candidate implementation/test paths identified for later phases:

- Streaming production-oriented route:
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- Non-streaming/transport helper route:
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- LGSSM value/gradient test harness:
  `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py`
- Existing LGSSM reset diagnostic:
  `docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_reset_variants.py`
- Existing SIR Sinkhorn/FD diagnostic:
  `docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py`

The route scan found existing `tf.while_loop`, `jit_compile=True`, chunk-size,
and `transport_ad_mode` controls in the relevant implementation/test paths.
The SIR diagnostic sets `transport_ad_mode = "stabilized"` rather than full
transport AD.  Phase 1 is still required to build a separate Contract E
moment-level diagnostic before model-level integration.

## Frozen Comparator And Boundary Rules

- LGSSM may use exact Kalman value/gradient.
- SIR/SV/nonlinear targets must use same-scalar FD regression only.
- Zhao-Cui is not an oracle in this program.
- Central FD may be logged only as sanity/explanatory evidence.
- The promoted FD protocol is 13 points, drop highest and lowest objective
  values, regress the remaining points, and report standard error.
- `transport_ad_mode=full` is forbidden for Contract E evidence routes.
- GPU/XLA/TF32 claims require trusted/elevated GPU evidence under `AGENTS.md`.
- CPU-hidden smoke is wiring evidence only.

## Phase 1 Handoff

Phase 1 should implement the smallest synthetic weighted-cloud diagnostic:

- expected path:
  `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_reset_moments.py`
- JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.json`
- Markdown:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.md`
- result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-result-2026-06-28.md`

Phase 1 entry condition is satisfied only after this Phase 0 result and the
Phase 1 subplan pass bounded review.  The master program and visible runbook
already passed bounded Claude review in round 3, recorded in:

- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-claude-review-ledger-2026-06-28.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-visible-execution-ledger-2026-06-28.md`

The current Phase 0 review gate must confirm this result and the Phase 1
handoff before Phase 1 starts.

## Decision Table

| Decision | Status |
| --- | --- |
| Contract E anchors exist and are exact enough for Phase 1 | `passed` |
| Existing LGSSM/SIR diagnostics present | `passed` |
| Wrong-comparator risk controlled in plan | `passed` |
| Full transport AD risk controlled in plan | `passed` |
| GPU/CPU evidence boundary controlled in plan | `passed` |
| Execution ledger exists and records launch/review state | `passed` |
| Claude review ledger exists and records master/runbook convergence | `passed` |
| Phase 1 ready to review | `passed_review_ready_to_start` |

## Nonclaims

Phase 0 does not conclude:

- Contract E works;
- implementation exists;
- LGSSM value or gradient correctness;
- SIR/SV gradient correctness;
- production readiness;
- HMC readiness;
- posterior correctness;
- broad nonlinear certification.

## Next Action

Advance to Phase 1 under the visible runbook.  Phase 0 result / Phase 1
handoff review converged in Claude round 4 with `VERDICT: AGREE`, recorded in
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-claude-review-ledger-2026-06-28.md`.
