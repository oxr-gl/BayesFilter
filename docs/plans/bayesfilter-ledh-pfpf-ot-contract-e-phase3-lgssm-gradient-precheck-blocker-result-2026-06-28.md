# Phase 3 Precheck Blocker Result: Contract E LGSSM gradient

Date: 2026-06-28

Status: `PHASE3_BLOCKED_BEFORE_MATERIAL_GATE`

Master program:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-residual-affine-testing-master-program-2026-06-28.md`

Runbook:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-visible-gated-execution-runbook-2026-06-28.md`

## Phase Objective

Test the Contract E LGSSM gradient against exact Kalman and an independent
same-scalar 13-point finite-difference regression diagnostic.

## Blocker Summary

Phase 3 did not reach the material GPU/XLA gradient gate.  The CPU-hidden
precheck shows finite 13-point FD regression slopes for the Contract E scalar,
but the current reverse diagnostic route returns `NaN` gradients for all three
LGSSM parameters.  Because nonfinite gradients are a Phase 3 veto diagnostic,
the material gate must not be launched from this state.

The evidence supports this narrower conclusion only: the current reverse
diagnostic route is invalid.  It does not by itself prove that a manual reverse
scan is the only possible repair.  A manual reverse extension is a plausible
next repair target because the existing LGSSM statistical harness already uses
a manual reverse scan for the old stopped-key OT path, but that repair still
requires a reviewed subplan before execution.

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Blocked before material answer. |
| Baseline/comparator | Exact Kalman and same-scalar FD were computed in the smoke artifacts; material comparison was not run. |
| Primary criterion | Not evaluated materially because reverse gradients were nonfinite in precheck. |
| Veto diagnostics | Triggered: current reverse diagnostic gradients are `NaN`. |
| Explanatory diagnostics | FD slopes are finite; localization probes indicate the NaNs are not removed by value-only transport probing or by skipping/stopping the Contract E reset computation. |
| Not concluded | No Contract E gradient correctness, no SIR/SV correctness, no production/HMC/posterior claim. |

## Artifacts

- Phase 3 diagnostic script:
  `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py`
- Main CPU-hidden smoke:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-smoke-2026-06-28.json`
- Value-only transport probe:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-smoke-value-only-probe-2026-06-28.json`
- Non-XLA value-only probe:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-smoke-nonxla-value-only-probe-2026-06-28.json`
- Stop-affine probe:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-probe-stop-affine-2026-06-28.json`
- Stop-residual probe:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-probe-stop-residual-2026-06-28.json`
- Stop-reset probe:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-probe-stop-reset-2026-06-28.json`
- Skip-reset-computation probe:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-probe-skip-reset-computation-2026-06-28.json`

## Focused Results

The main CPU-hidden smoke used `N=32`, `T=10`, 10 seeds, state dimension 1,
`epsilon=0.5`, 4 Sinkhorn steps, and the frozen Phase 3 FD steps
`[5e-4, 1e-3, 1e-3]`.  It is a wiring/precheck artifact only.

| Route | Reverse gradient mean | FD slopes | Status |
| --- | --- | --- | --- |
| Main stopped-key route | `[NaN, NaN, NaN]` | `[-2.479169, -1.959500, -2.765825]` | `smoke_failed` |
| Value-only transport probe | `[NaN, NaN, NaN]` | `[-2.479169, -1.959500, -2.765825]` | `smoke_failed` |
| Non-XLA value-only probe | `[NaN, NaN, NaN]` | `[-2.479197, -1.959450, -2.765769]` | `smoke_failed` |
| Stop-reset probe | `[NaN, NaN, NaN]` | `[-2.479197, -1.959450, -2.765769]` | `smoke_failed` |
| Skip-reset-computation probe | `[NaN, NaN, NaN]` | `[-1.303899, -1.989313, -2.730528]` | `smoke_failed` |

The skip-reset-computation probe is not a Contract E gradient claim.  It is a
localization probe showing that merely bypassing the Contract E restoration
computation does not make the current reverse diagnostic finite.

## Commands Run

Compile/static checks:

```bash
python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py
git diff --check -- docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py
```

Main CPU-hidden smoke:

```bash
python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  --device-scope cpu \
  --num-particles 32 \
  --seed-count 10 \
  --time-steps 10 \
  --state-dims 1 \
  --settings 0.5:4 \
  --gate-mode smoke \
  --xla \
  --tf32-mode enabled \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-smoke-2026-06-28.json \
  --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-smoke-2026-06-28.md
```

Focused probes were CPU-hidden and non-promotable.  They varied only
`--reverse-transport-gradient-route`, `--reverse-contract-e-gradient-probe`,
and XLA on/off.

## Claude Review

Claude bounded review of the first, broader prompt hung.  A small probe returned
`PROBE_OK`, so Codex retried with a smaller exact-path prompt.  Claude returned
`VERDICT: REVISE`.

Claude agreed that:

- the main smoke has finite FD slopes but `NaN` reverse gradients;
- the skip-reset-computation probe still has `NaN` reverse gradients;
- the material gate should not be launched from this evidence.

Claude requested a wording correction:

- do not claim these artifacts prove that the next step must be a manual
  reverse scan;
- state instead that the current reverse diagnostic is blocked and that a
  manual reverse extension is only a plausible repair target requiring its own
  reviewed plan.

This result incorporates that correction.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Stop Phase 3 before material GPU/XLA gate. | Not evaluated materially. | Failed precheck: reverse gradients are nonfinite. | The exact NaN source inside the current reverse diagnostic remains unresolved. | Draft a Phase 3 repair subplan before any material run. | No gradient correctness or production claim. |
| Treat FD as informative, not sufficient. | FD slopes are finite and close to exact Kalman in the smoke. | FD cannot rescue a nonfinite reverse-gradient gate. | FD smoke is small `N=32`, state dimension 1 only. | Preserve FD protocol for the repair plan. | FD alone does not certify the differentiable gradient route. |
| Manual reverse scan is plausible, not proven mandatory. | Existing repo harness has a manual reverse scan for the old OT route. | No Contract E manual reverse VJP has been implemented or reviewed here. | Contract E reset VJP may require its own derivation or a safer differentiable restoration. | Review a dedicated repair plan focused on the smallest discriminating implementation path. | This blocker does not choose the final repair. |

## Stop Conditions Triggered

- Nonfinite reverse gradients in precheck.
- Material Phase 3 GPU/XLA gate would not answer the phase question until the
  reverse diagnostic route is repaired or replaced by a reviewed route.

## Next Safe Action

Draft a Phase 3 repair subplan.  It should freeze the current evidence, choose
the smallest discriminating repair target, and review that plan with Claude
before implementing.  Candidate repair targets include:

- extending the existing LGSSM manual reverse scan to the Contract E reset;
- deriving and testing a local Contract E reset VJP before integrating it into
  the scan;
- classifying Contract E gradient support as blocked if a differentiable reset
  VJP cannot be made finite without changing the mathematical contract.
