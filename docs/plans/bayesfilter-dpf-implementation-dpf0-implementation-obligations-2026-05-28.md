# DPF0 Implementation Obligations

## Status

DPF0 execution artifact.  These obligations translate accepted DPF0 claims into
phase inputs for the BayesFilter-owned DPF implementation lane.  They are not
code changes and do not authorize production edits.

## Obligation Ledger

| ID | Owner phase | Obligation | Source claims | Acceptance evidence required | Stop / defer condition |
| --- | --- | --- | --- | --- | --- |
| DPF0-O01 | DPF1 | Implement/specify a classical bootstrap/SIR PF baseline before any relaxed DPF component. | DPF0-C01, DPF0-C02, DPF0-C03 | Log weights, normalized weights, ESS, resampling, likelihood estimator, log-likelihood estimator, seeds, dtype/shape schema, and LGSSM reference tests. | Stop if likelihood/log-likelihood/score semantics are ambiguous. |
| DPF0-O02 | DPF1 | Keep the likelihood estimator, log likelihood, score, and differentiable surrogate as separate objects. | DPF0-C02, DPF0-C03 | Reference-test contract and artifact schema with non-implications. | Stop if any artifact treats log likelihood or gradient as unbiased by default. |
| DPF0-O03 | DPF2 | Specify hard, soft, EOT, finite Sinkhorn, and solver-gradient objects separately. | DPF0-C04, DPF0-C05 | Component spec naming alpha/epsilon/budget/stabilization/residuals/gradient path. | Defer neural/amortized components without provenance-bearing spec. |
| DPF0-O04 | DPF2 | Label soft-resampling evidence by observable class. | DPF0-C04; DPF0A-PATCH-002 | Bias/proxy ledger with affine/mean-preserving and nonlinear-biased rows. | Stop if "unbiased soft resampling" appears without observable scope. |
| DPF0-O05 | DPF2 | Keep learned/neural resampling and learned OT behind deferred component registers. | DPF0-C06 | Deferred-neural register with teacher, training distribution, residual, provenance, and non-implication requirements. | Defer if no approved teacher/student artifact exists. |
| DPF0-O06 | DPF3 | Specify proposal-corrected PF-PF weights with target/proposal densities and forward log determinant. | DPF0-C07 | Flow/PF-PF spec and affine closed-form parity contract. | Stop if Jacobian sign, proposal density, or pre/post-flow path binding is missing. |
| DPF0-O07 | DPF3 | Keep affine/special-case parity separate from nonlinear filtering claims. | DPF0-C07, DPF0-C08 | Excluded-flow risk register and range-bearing controlled-fixture diagnostics. | Stop if nonlinear flow correctness is inferred from affine-only evidence. |
| DPF0-O08 | DPF3 | Keep kernel PFF excluded and stochastic flow deferred until clean-room specs exist. | DPF0-A ledger; DPF0 deferred families | Kernel PFF exclusion check and stochastic-flow risk row. | Stop if kernel PFF enters routine panels without a debug gate. |
| DPF0-O09 | DPF4 | Classify every differentiated scalar before interpreting gradients. | DPF0-C09, DPF0-C10 | Objective classification ledger: filtering proxy, surrogate likelihood, transport residual, component loss, posterior/HMC candidate. | Stop if objective class is ambiguous or HMC is required for phase success. |
| DPF0-O10 | DPF4 | Ban "validated DPF-HMC pipeline" wording without target and sampler evidence. | DPF0-C09, DPF0-C10; DPF0A-PATCH-003 | Downstream evidence requirements with same-scalar, posterior/reference, sampler diagnostics. | Block HMC/posterior claims unless separate evidence contract passes. |
| DPF0-O11 | DPF5 | Build a validation ladder with independent reference rungs before proxy/performance comparison. | DPF0-C11, DPF0-C12 | LGSSM Kalman recovery, affine PF-PF parity, resampling residuals, gradient contract, controlled range-bearing fixture, proxy-only student context. | Stop if runtime or student agreement becomes promotion evidence. |
| DPF0-O12 | DPF5 | State Monte Carlo uncertainty and CPU/GPU runtime policy. | DPF0-C11 | Seed policy, artifact size/runtime bounds, GPU escalation/trusted-permission policy. | Stop if broad sweeps or GPU runs are proposed without phase evidence contract. |
| DPF0-O13 | DPF6 | Treat every component as experimental-only until DPF5 evidence exists and a production patch plan is accepted. | DPF0-C11 | Production-boundary decision: production-candidate, experimental-only, blocked, or documentation-only. | Stop if production code/API/default edits are required inside DPF6. |
| DPF0-O14 | DPF7 | Final handoff must preserve non-implications and unresolved risks. | DPF0-C12 and all deferred families | Final audit and implementation handoff with review records and verification summary. | Stop if handoff implies implementation, HMC, posterior, production, banking, or model-risk readiness. |

## Evidence Ledger Separation

| Ledger | DPF0 rule |
| --- | --- |
| Mathematical claims | Must trace to monograph equations/derivations or cited theory. |
| Source/literature support | Current ceiling is bibliography-spine unless later paper review upgrades it. |
| Engineering correctness | Requires BayesFilter-owned specs and tests, not student code or agreement. |
| Numerical validity | Requires independent references, residual tolerances, finite checks, and seed/uncertainty policy. |
| Gradient validity | Requires a named scalar, path semantics, and same-scalar value/gradient tests. |
| HMC/sampler validity | Not established in this lane; requires separate posterior/reference and sampler evidence. |
| Performance evidence | Runtime/speed are explanatory until veto diagnostics pass. |
| Production/API readiness | Blocked until DPF6 and a separate production patch plan. |

## Non-Implications

These obligations do not conclude that a DPF implementation exists, is correct,
is differentiable in the desired sense, is production-ready, preserves the
original posterior, supports HMC, or is suitable for banking/model-risk use.
