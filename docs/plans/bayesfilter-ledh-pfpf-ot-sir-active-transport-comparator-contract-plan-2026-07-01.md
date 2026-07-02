# SIR Active-Transport Comparator Contract Plan

Date: 2026-07-01

Status: `IN_PROGRESS`

## Question

Does the apparent SIR `log_kappa_scale` gradient discrepancy come from a real
manual-score bug, or from comparing the stopped-gradient active-transport score
against finite differences of the literal active-transport value?

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Separate the stopped-gradient surrogate gradient from the literal fully differentiated active-transport gradient on a tiny SIR route. |
| Baseline/comparator | CPU float64 tiny SIR route with fixed seeds, fixed stateless process noise, and active/no-resampling masks. Compare manual reverse, TensorFlow tape through the custom stopped-gradient route, literal finite difference, and `raw/full` TensorFlow tape. |
| Primary criterion | For `no-resampling`, manual stopped-gradient and literal FD agree. For active transport, manual stopped-gradient matches TensorFlow tape through the same stopped-gradient route, while literal FD matches `raw/full` tape and can differ from the stopped-gradient route. |
| Veto diagnostics | Nonfinite values, manual route not matching same-route TensorFlow tape, `raw/full` not matching literal FD, no-resampling mismatch, or treating CPU tiny evidence as GPU/TF32 material evidence. |
| Explanatory diagnostics | Magnitude of active-policy stopped-vs-literal gap, seed-level score variation, and which parameter carries the largest discrepancy. |
| What will not be concluded | No full SIR gradient correctness, no HMC readiness, no posterior correctness, no material GPU/TF32 claim, and no production/default policy change. |
| Artifact preserving result | JSON under `docs/plans` plus this plan/result note. |

## Planned Artifacts

- Diagnostic script:
  `docs/benchmarks/diagnose_p8p_sir_active_transport_comparator_contract.py`
- Focused test:
  `tests/test_p8p_sir_active_transport_comparator_contract.py`
- Result JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-active-transport-comparator-contract-2026-07-01.json`
- Result note:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-active-transport-comparator-contract-result-2026-07-01.md`

## Planned Checks

```bash
python -m py_compile docs/benchmarks/diagnose_p8p_sir_active_transport_comparator_contract.py
pytest -q tests/test_p8p_sir_active_transport_comparator_contract.py
python docs/benchmarks/diagnose_p8p_sir_active_transport_comparator_contract.py \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-active-transport-comparator-contract-2026-07-01.json
```

## Skeptical Audit

- Wrong baseline: avoided by comparing each gradient only to its matching
  derivative contract: stopped-gradient tape to manual reverse, and `raw/full`
  tape to literal finite difference.
- Proxy metrics: tiny CPU parity is diagnostic only; it cannot certify the
  material GPU/TF32 SIR route.
- Missing stop conditions: stop on nonfinite values, same-route tape mismatch,
  `raw/full` FD mismatch, or no-resampling mismatch.
- Unfair comparison: all arms share the same seeds, `T`, `N`, theta, process
  noise, observations, and finite-difference step.
- Hidden assumptions: the active-policy stopped-gradient objective is a
  surrogate derivative contract, not the derivative of the literal value map.
- Environment mismatch: CPU-only route is intentional and must be recorded as
  such.
- Artifact adequacy: JSON records route settings, tolerances, per-policy
  gradients, and pass/fail predicates.

## Stop Conditions

- If no-resampling manual-vs-FD does not match, stop and investigate transition
  or log-weight score assembly.
- If active manual reverse does not match TensorFlow tape through the same
  custom stopped-gradient route, stop and investigate the manual reverse route.
- If `raw/full` tape does not match literal FD, stop and investigate the
  finite-difference or TensorFlow full-gradient comparator.
- If the diagnostic cannot run in CPU float64 with finite outputs, stop and
  record blocker.

## Nonclaims

- No SIR gradient correctness claim.
- No HMC readiness claim.
- No posterior correctness claim.
- No GPU/TF32 material evidence claim.
- No production/default-policy change.
