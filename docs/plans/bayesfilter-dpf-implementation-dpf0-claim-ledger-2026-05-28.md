# DPF0 Claim Ledger

## Status

DPF0 execution artifact.  This ledger extracts implementation-relevant claims
from the DPF monograph and DPF monograph evidence reports after DPF0-A
adjudication.  Student work is comparison-only and is not used as authority.

## Skeptical Plan Audit

| Check | Status | Notes |
| --- | --- | --- |
| DPF0-A prerequisite | pass | `docs/plans/bayesfilter-dpf-implementation-dpf0a-student-doc-crosswalk-result-2026-05-28.md` records `DPF0 may start: yes`. |
| Stale context | pass | DPF0-A ledger, result, patch register, master, and DPF0 plan were re-read. |
| Wrong baseline | pass | The baseline is the BayesFilter DPF monograph, references, source map, and DPF evidence reports. |
| Proxy overclaim | pass | Proxy metrics, student agreement, finite-gradient checks, and speedups are not correctness criteria. |
| Missing stop conditions | pass | Unsupported claims become deferred items or phase blockers, not obligations. |
| Hidden production/monograph drift | pass | No production or monograph edits are authorized in DPF0. |
| Vendored-code contamination | pass | No vendored student code is edited, executed, imported, or copied. |
| High-dimensional-lane contamination | pass | The high-dimensional nonlinear filtering lane is not read or used. |
| Artifact fitness | pass | The ledger separates mathematical, engineering, numerical, gradient, HMC, performance, and production ledgers. |

## Claim Ledger

| ID | Claim cluster | Source/proof support | Status | Assumptions | Required later evidence | Non-implications |
| --- | --- | --- | --- | --- | --- | --- |
| DPF0-C01 | Nonlinear SSM filtering recursion and marginal likelihood factorization define the statistical target. | `ch19_particle_filters.tex`, filtering recursion and marginal-factorization equations. | accepted mathematical identity | Dominated kernels, finite integrals, stated model densities. | DPF1 target/proposal log-density checks and LGSSM reference tests. | Does not imply finite-particle correctness or differentiability. |
| DPF0-C02 | Bootstrap/SIR PF gives an unbiased estimator of marginal likelihood under the chapter assumptions. | `prop:bf-pf-bootstrap-likelihood-status`; `doucet2001sequential`, `andrieu2010particle`. | accepted theorem in monograph notation | Bootstrap proposal, integrability, support, conditionally unbiased resampling. | DPF1 likelihood-estimator schema, log-normalizer separation, seed/MC uncertainty policy. | Not unbiased log likelihood, not unbiased score, not pathwise differentiable likelihood. |
| DPF0-C03 | Classical categorical resampling blocks naive pathwise differentiation. | `sec:bf-pf-differentiability-boundary`; `ch32` discontinuous-map section. | accepted mathematical/algorithmic boundary | Realized ancestor selection is discrete. | DPF1 hard-resampling boundary; DPF2 relaxed-resampling contracts. | Does not make relaxed resampling exact or posterior preserving. |
| DPF0-C04 | Soft resampling preserves affine/mean summaries in conditional expectation but biases nonlinear summaries. | `eq:bf-dr-soft-resampling`, `eq:bf-dr-soft-mean-preserved`, `eq:bf-dr-soft-test-bias`; IE5 soft-resampling result. | accepted local derivation with clean-room arithmetic support | Fixed weighted cloud, named alpha, smooth test functions for bias expansion. | DPF2 bias/proxy ledger and tests that name observable class. | Not categorical-law preservation, not nonlinear unbiasedness, not posterior validity. |
| DPF0-C05 | EOT/Sinkhorn resampling is a relaxed transport object distinct from categorical resampling. | `ch32` EOT/Sinkhorn derivation; `corenflos2021differentiable`, `cuturi2013sinkhorn`, `peyre2019computational`; IE5 Sinkhorn residual result. | accepted component claim | Positive marginals, finite cost, epsilon, iteration budget, stabilization, residual tolerance, named gradient path. | DPF2 component spec and residual/marginal tests. | Not exact unregularized OT at finite epsilon, not categorical resampling, not posterior preservation. |
| DPF0-C06 | Learned/amortized OT is an additional approximation layer requiring provenance-bearing teacher/student artifacts. | `ch19d`; `ch32` learned-later section; IE6 deferred no approved artifact. | deferred evidence gap | Teacher type, training distribution, checkpoint/provenance, residual metrics, downstream checks must exist. | DPF2 deferred-neural register; future learned-OT component plan. | No learned-OT surrogate-quality, posterior, HMC, or production claim. |
| DPF0-C07 | PF-PF/particle flow must be treated as a proposal transformation with a Jacobian/proposal-density correction. | `ch19c`, especially corrected-weight equations; `li2017particle`; IE4 affine PF-PF algebra parity. | accepted implementation obligation | Flow map invertible/differentiable on support; proposal and target densities evaluated on the same path; log determinant convention fixed. | DPF3 flow/PF-PF spec, affine parity, corrected log-weight tests. | Affine parity does not validate nonlinear flow integration or full filtering correctness. |
| DPF0-C08 | EDH exactness is limited to linear-Gaussian/special-case recovery; nonlinear EDH/LEDH evidence is diagnostic. | `ch19b`; IE3 linear-Gaussian recovery; IE4 affine evidence. | accepted boundary | Linear-Gaussian assumptions for exact recovery; nonlinear fixtures need separate diagnostics. | DPF3 controlled nonlinear fixture contract; DPF5 validation ladder. | No universal nonlinear exactness, no production/default claim. |
| DPF0-C09 | Differentiated scalar and gradient semantics must be named before HMC or optimization interpretation. | `ch19e`; `ch32` gradient-object distinctions; IE7 fixed-scalar value-gradient result. | accepted boundary | Same scalar for value/gradient, seed policy, stopped-gradient/reparameterized/relaxed path named. | DPF4 objective classification and gradient contract. | Finite gradient is not posterior validity, HMC convergence, or likelihood-score correctness. |
| DPF0-C10 | Relaxed or learned DPF likelihoods define changed targets unless a correction/error argument returns to the intended target. | `ch19e` method-family comparison and recommendation. | accepted boundary | Target class named: original, relaxed, learned, corrected, or proxy. | DPF4 downstream evidence requirements; DPF5 posterior/reference gates if ever pursued. | No real DPF-HMC, DSGE/MacroFinance posterior, banking, or model-risk claim. |
| DPF0-C11 | Existing monograph evidence supports only controlled fixtures and governance labels. | DPF monograph evidence note; IE3-IE7 reports. | accepted evidence ceiling | Current artifacts are clean-room, bounded, mostly CPU-only and not production paths. | DPF5 harness must separate correctness, numerical, gradient, proxy, and performance ledgers. | No production `bayesfilter` validation or public API readiness. |
| DPF0-C12 | Student and controlled-baseline reports may identify comparison surfaces but cannot certify BayesFilter correctness. | DPF0-A ledger/result; controlled final archive and student reports. | accepted quarantine rule | Student code and reports remain comparison-only/proxy-only. | DPF1-DPF5 comparison-context registers only. | Student agreement is not source support, not validation, and not implementation authority. |

## Deferred Or Blocked Claim Families

| Family | Status | Reason |
| --- | --- | --- |
| Kernel PFF | excluded pending debug | Student/debug reports mark kernel PFF unsuitable for routine panels; no BayesFilter-owned debug gate exists. |
| Stochastic flow | deferred clean-room spec | Needs target/proposal/Jacobian and validation contract before entering DPF3. |
| Neural/transformer resampling | deferred component spec | Current support is method-surface inventory; no BayesFilter-owned objective/provenance contract. |
| Learned/amortized OT | deferred artifact provenance | IE6 could not run residual diagnostics because no approved teacher/student artifact exists. |
| DPF-HMC posterior validity | blocked pending separate evidence | Requires named target, same-scalar value/gradient, posterior/reference diagnostics, and sampler diagnostics. |

## DPF0 Decision

The extracted claims are sufficient to proceed to DPF1-DPF5 planning artifacts.
No DPF0 claim authorizes production code edits, monograph edits, vendored-code
edits, broad experiments, HMC validation, posterior claims, or model-risk use.
