# SIR Active-Transport Comparator Contract Result

Date: 2026-07-01

Status: `PASSED`

## Decision

The apparent active-transport SIR gradient discrepancy is explained as a
derivative-contract mismatch.

The manual reverse route matches TensorFlow tape for the same stabilized
stopped-gradient transport route.  Literal finite differences instead match
the fully differentiated `raw/full` active-transport route.  Therefore, the
previous active-transport FD gap should not be interpreted as a manual-score
bug unless the intended comparator is explicitly the literal fully
differentiated value map.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the active-transport `log_kappa_scale` discrepancy reflect a real manual-score bug or a comparator-contract mismatch? |
| Baseline/comparator | CPU float64 tiny SIR route, fixed seeds `81120,81121,81122`, `T=3`, `N=3`, theta `(0.02,-0.01,0.01)`. |
| Primary criterion | No-resampling manual/FD agree; active manual stopped-gradient matches same-route tape; literal FD matches `raw/full` tape; active stopped-gradient can differ from literal FD. |
| Veto diagnostics | Nonfinite values, same-route manual/tape mismatch, `raw/full`/FD mismatch, no-resampling mismatch, or CPU tiny result claimed as material GPU/TF32 evidence. |
| Not concluded | No full SIR gradient correctness, HMC readiness, posterior correctness, material GPU/TF32 claim, or production/default policy change. |

## Commands Run

```bash
python -m py_compile docs/benchmarks/diagnose_p8p_sir_active_transport_comparator_contract.py
pytest -q tests/test_p8p_sir_active_transport_comparator_contract.py
python docs/benchmarks/diagnose_p8p_sir_active_transport_comparator_contract.py \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-active-transport-comparator-contract-2026-07-01.json
```

## Artifacts

- Plan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-active-transport-comparator-contract-plan-2026-07-01.md`
- Diagnostic:
  `docs/benchmarks/diagnose_p8p_sir_active_transport_comparator_contract.py`
- Test:
  `tests/test_p8p_sir_active_transport_comparator_contract.py`
- JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-active-transport-comparator-contract-2026-07-01.json`

## Check Results

- Compile check: passed.
- Focused tests: `2 passed`.
- Diagnostic status: `PASS`.
- Environment: intentional CPU-only float64 route with `CUDA_VISIBLE_DEVICES=-1`.

TensorFlow printed CUDA plugin registration and `cuInit` messages during import.
Those messages are not material GPU evidence; CUDA was intentionally hidden for
this local comparator diagnostic.

## Key Numbers

No-resampling, where stopped-gradient and literal-value contracts coincide:

| Quantity | Value |
| --- | ---: |
| Manual stopped-gradient kappa | `-264.0752229380851` |
| Same-route tape kappa | `-264.075222938085` |
| Literal FD kappa | `-264.0752232196064` |
| Manual stopped vs literal FD max abs | `2.8152129516456625e-07` |

Active-all, where the contracts differ:

| Quantity | Value |
| --- | ---: |
| Manual stopped-gradient kappa | `-307.4602758965205` |
| Same-route tape kappa | `-307.4602758965241` |
| Literal FD kappa | `-275.2256122299457` |
| `raw/full` tape kappa | `-275.07523878170434` |
| `raw/full` tape vs literal FD max abs | `2.907598855017568e-07` |
| Manual stopped vs literal FD max abs | `32.23466366657482` |

The active-all manual stopped-gradient score is not failing its matching
TensorFlow comparator.  The literal FD is measuring a different derivative:
the fully differentiated active-transport map.

## Mathematical Interpretation

The stabilized active-transport route treats centering, scaling, and related
transport-key quantities as stopped for differentiation.  Its score is the
gradient of the stopped-gradient surrogate, not the gradient of the literal
map that recomputes those quantities under a finite perturbation of theta.

Therefore a central finite difference of the ordinary value answers:

```text
d/dtheta value(theta, center(theta), scale(theta), keys(theta), ...)
```

while the stabilized score answers:

```text
partial_theta value(theta, stop(center), stop(scale), stop(keys), ...)
```

These are the same only when the stopped transport quantities do not influence
future likelihoods or when transport is inactive.  Once active transport feeds
future SIR steps, they can differ substantially, especially in the nonlinear
infection-rate direction.

## Decision Table

| Item | Status |
| --- | --- |
| Primary criterion | Passed. |
| Veto diagnostics | No veto. |
| Main uncertainty | Material GPU/TF32 behavior and downstream HMC usefulness still need separately contracted checks. |
| Next justified action | Update the SIR gradient gate so FD checks are contract-aware: stopped-gradient routes compare to same-route tape/manual parity, while literal FD is paired only with `raw/full` comparators. |
| What is not concluded | No posterior correctness, HMC readiness, production reparameterization, or full SIR score correctness. |

## Nonclaims

- No SIR gradient correctness claim.
- No HMC readiness claim.
- No posterior correctness claim.
- No material GPU/TF32 evidence claim.
- No production/default-policy change.
