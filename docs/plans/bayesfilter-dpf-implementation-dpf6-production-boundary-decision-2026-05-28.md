# DPF6 Production Boundary Decision

## Status

DPF6 execution artifact.  This is a read-only production/API boundary review.
It does not edit production code and does not create a production patch.

## Read-Only Package Facts

| Area | Observation | Consequence |
| --- | --- | --- |
| `bayesfilter/filters/particles.py` | Existing structural bootstrap particle filter with `monte_carlo_value_only` metadata and systematic/multinomial resampling. | Existing code is a classical structural PF reference, not a differentiable DPF implementation. |
| `bayesfilter/__init__.py` | Public API exports linear, nonlinear sigma-point, structural, and diagnostics APIs; no DPF API. | No DPF public API exists. |
| `tests/` | Tests cover structural particles, linear/nonlinear filters, HMC readiness, etc.; no DPF implementation harness from DPF1-DPF5. | DPF validation harness remains future work. |
| `README.md` | Minimal title only. | No DPF user-facing documentation exists. |
| `.github/workflows/` | Not present. | DPF6 cannot infer CI policy. |
| `pyproject.toml`, `setup.cfg`, `tox.ini`, `noxfile.py` | Not present at repo root in read-only check. | DPF6 records config absence rather than inventing packaging/runtime policy. |

## Component Classification

| Component / artifact | DPF6 classification | Required before production movement |
| --- | --- | --- |
| Existing structural bootstrap PF | existing production/reference code, outside new DPF implementation lane | Do not relabel as DPF; preserve current metadata and tests. |
| DPF1 classical PF baseline spec | documentation/planning only | Implement experimental harness and tests under a separate plan. |
| DPF2 soft/EOT/Sinkhorn components | experimental-only future components | Component code, residual tests, bias/proxy labels, dtype/device contracts. |
| DPF2 learned/neural paths | blocked/deferred | Provenance-bearing teacher/student artifacts and component specs. |
| DPF3 PF-PF flow proposal correction | experimental-only future component | Proposal/Jacobian/corrected-weight implementation and affine parity tests. |
| DPF3 stochastic flow | blocked/deferred | Clean-room stochastic-flow spec and density correction. |
| Kernel PFF | excluded pending debug | Separate convergence/debug gate. |
| DPF4 objective/gradient contract | documentation/planning only | Same-scalar gradient fixtures before any optimizer/sampler API. |
| DPF5 validation harness | documentation/planning only | Implement harness and pass required veto tiers. |
| DPF-HMC/posterior path | blocked | Separate target, posterior/reference, and sampler diagnostics plan. |

## Production Boundary Decision

`no_dpf_component_ready_for_production_patch`

No DPF component is ready to move into production `bayesfilter/` APIs from this
planning lane alone.  The appropriate next implementation step is a separate,
reviewed experimental patch plan under `experiments/dpf_implementation/` or a
similarly isolated namespace, with tests that satisfy DPF1-DPF5 contracts before
any DPF6 production reconsideration.

## Future Patch-Plan Shape

A future patch plan may propose:

- experimental package path: `experiments/dpf_implementation/`;
- no public `bayesfilter` API export in the first patch;
- classical PF reference harness using DPF1 contracts;
- component modules for soft/Sinkhorn only after DPF2 tests are written;
- PF-PF algebra fixture before nonlinear flow integration;
- no learned/neural implementation until provenance gates pass;
- no HMC sampler integration until DPF4/DPF5 downstream evidence gates pass.

## Non-Implications

DPF6 does not conclude that production code is broken, incomplete, or ready for
DPF.  It concludes only that this planning lane has not produced the evidence
required to edit production APIs.
