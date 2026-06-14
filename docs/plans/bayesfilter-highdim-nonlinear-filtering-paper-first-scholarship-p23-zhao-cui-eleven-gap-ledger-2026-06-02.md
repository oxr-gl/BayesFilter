# P23 Zhao--Cui Eleven-Gap Closure Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P22 integrated readable companion and fixed-branch gradient note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive branches.
- No HMC convergence claim.
- No production implementation readiness claim.
- No executable prototype claim.

## Decision

Decision: `ELEVEN_GAP_CLOSURES_DRAFTED_WITH_EXACT_PAYLOAD_ANCHORS`.

## Exact Payload Checklist

| Gap | Required payload item | Exact P23 anchor(s) | Payload satisfied? | Evidence note | Failure flag |
|---|---|---|---|---|---|
| 1 threaded nonlinear example | model equations | P23-E1 | yes | scalar nonlinear state-space model declared | none |
| 1 threaded nonlinear example | exact transition and observation densities | P23-E2, P23-E3 | yes | Gaussian transition and sine-observation likelihood written explicitly | none |
| 1 threaded nonlinear example | time-1 target | P23-E5 | yes | time-1 adjacent-state Bayes numerator shown | none |
| 1 threaded nonlinear example | squared-TT target | P23-E6, P23-E7, P23-E8 | yes | square-root approximation, defensive density, evidence, and carried filter shown | none |
| 1 threaded nonlinear example | time-2 filtering recurrence | P23-E9 | yes | carried time-1 filter enters time-2 target | none |
| 1 threaded nonlinear example | preconditioned residual | P23-E10 | yes | bridge-ratio transformed residual written | none |
| 1 threaded nonlinear example | gradient scalar and derivative | P23-E11, P23-E12 | yes | two-time fixed-branch scalar and derivative displayed | none |
| 1 threaded nonlinear example | recurrence table | P23-E13 | yes | filtering, squared-TT, preconditioning, and gradient reuse listed | none |
| 2 worked two-dimensional KR example | joint density | P23-KR2-1 | yes | normalized approximate density stated | none |
| 2 worked two-dimensional KR example | marginal density | P23-KR2-2 | yes | first marginal integral shown | none |
| 2 worked two-dimensional KR example | conditional density | P23-KR2-3 | yes | second conditional ratio shown | none |
| 2 worked two-dimensional KR example | two CDFs | P23-KR2-4, P23-KR2-5 | yes | marginal and conditional CDFs shown | none |
| 2 worked two-dimensional KR example | triangular map | P23-KR2-6 | yes | lower triangular map displayed | none |
| 2 worked two-dimensional KR example | Jacobian determinant | P23-KR2-7, P23-KR2-8 | yes | triangular Jacobian and determinant identity displayed | none |
| 2 worked two-dimensional KR example | squared-TT conditional derivation | P23-KR2-8a, P23-KR2-8b, P23-KR2-8c, P23-KR2-8d, P23-KR2-8e | yes | mass contraction to conditional density evaluator derived | none |
| 2 worked two-dimensional KR example | inverse sampling equations | P23-KR2-9 | yes | inverse equations for uniform draws shown | none |
| 2 worked two-dimensional KR example | endpoint diagnostics | P23-KR2-10 | yes | endpoint values listed | none |
| 2 worked two-dimensional KR example | monotonicity diagnostics | P23-KR2-11 | yes | nonnegative derivative conditions listed | none |
| 3 preconditioning flattening | before target | P23-PREC1 | yes | untransformed target declared | none |
| 3 preconditioning flattening | bridge and residual ratio | P23-PREC2, P23-PREC3 | yes | \(q=\rho m\) and log split shown | none |
| 3 preconditioning flattening | bridge map identity | P23-PREC4 | yes | bridge pushforward to product reference displayed | none |
| 3 preconditioning flattening | transformed residual | P23-PREC5, P23-PREC6 | yes | transformed target and square-root factorization displayed | none |
| 3 preconditioning flattening | rank-pressure explanation | P23-PREC7 | yes | weaker coupling condition stated mathematically | none |
| 3 preconditioning flattening | failure case | P23-PREC8 | yes | near-zero bridge with positive target identified | none |
| 3 preconditioning flattening | failure diagnostic | P23-PREC9 | yes | bridge-support ratio diagnostic shown | none |
| 3 preconditioning flattening | running-example substitution | P23-PREC10, P23-PREC11 | yes | nonlinear example factors instantiated after generic bridge formula | none |
| 4 Proposition 2 dependency diagram | target-to-core value path | P23-GDAG1 | yes | target values, LS rows, solves, and cores chained | none |
| 4 Proposition 2 dependency diagram | target-to-core derivative path | P23-GDAG2 | yes | differentiated LS solve path shown | none |
| 4 Proposition 2 dependency diagram | derivative conditioning caveat | P23-GDAG2a | yes | ill-conditioned solve warning added to same-scalar graph | none |
| 4 Proposition 2 dependency diagram | core-to-normalizer value path | P23-GDAG3 | yes | cores to mass contraction to normalizer shown | none |
| 4 Proposition 2 dependency diagram | core-to-normalizer derivative path | P23-GDAG4 | yes | derivative mass and normalizer path shown | none |
| 4 Proposition 2 dependency diagram | carried-filter value path | P23-GDAG5 | yes | carried filter closes recursion | none |
| 4 Proposition 2 dependency diagram | carried-filter derivative path | P23-GDAG6 | yes | quotient derivative shown in graph | none |
| 4 Proposition 2 dependency diagram | log-likelihood derivative | P23-GDAG7 | yes | scalar and derivative summation shown | none |
| 4 Proposition 2 dependency diagram | running-example derivative callback | P23-GDAG8 | yes | generic target derivative instantiated for the nonlinear example | none |
| 5 rank-count plausibility | full-grid count | P23-RANK1, P23-RANK2 | yes | \(p^D\) and \(8^{20}\) example shown | none |
| 5 rank-count plausibility | TT storage count | P23-RANK3, P23-RANK4 | yes | \(DpR^2\) and numeric example shown | none |
| 5 rank-count plausibility | contraction cost | P23-RANK5 | yes | \(O(DpR^3)\) mass cost shown | none |
| 5 rank-count plausibility | empirical small-rank hinge | P23-RANK6 | yes | moderate-rank condition stated explicitly | none |
| 6 deterministic fixed-rank sweep | initialization and branch settings | P23-SWEEP1 | yes | fitting points, weights, ranks, basis sizes, ridge, sweeps, tolerances, rescaling declared | none |
| 6 deterministic fixed-rank sweep | pointwise target values | P23-SWEEP1a | yes | shifted square-root target vector defined inside sweep protocol | none |
| 6 deterministic fixed-rank sweep | core matrices at fitting points | P23-SWEEP1b | yes | current local core matrix construction shown | none |
| 6 deterministic fixed-rank sweep | environment recursions | P23-SWEEP1c, P23-SWEEP1d, P23-SWEEP1h | yes | left/right environments and post-solve updates shown | none |
| 6 deterministic fixed-rank sweep | design-row construction | P23-SWEEP1e, P23-SWEEP1f | yes | local basis row and Kronecker design row shown | none |
| 6 deterministic fixed-rank sweep | normal-equation construction | P23-SWEEP1g | yes | \(N_k\) and \(d_k\) defined in protocol block | none |
| 6 deterministic fixed-rank sweep | forward sweep order and ridge solve | P23-SWEEP2 | yes | forward core order and normal equation shown | none |
| 6 deterministic fixed-rank sweep | backward sweep order | P23-SWEEP3 | yes | reverse core order shown | none |
| 6 deterministic fixed-rank sweep | residual calculation | P23-SWEEP4 | yes | weighted relative residual displayed | none |
| 6 deterministic fixed-rank sweep | stopping rule | P23-SWEEP5 | yes | max sweep, relative residual, and stagnation rule shown | none |
| 6 deterministic fixed-rank sweep | frozen sweep count | P23-SWEEP6 | yes | same branch uses same realized sweep count | none |
| 6 deterministic fixed-rank sweep | optional rescaling | P23-SWEEP7 | yes | core normalization and shift update shown | none |
| 6 deterministic fixed-rank sweep | fixed-rank failure recovery | P23-SWEEP8 | yes | residual failure blocks silent rank increase | none |
| 7 domain-selection policy | pilot location and scale | P23-DOM1 | yes | pilot center and scale declared | none |
| 7 domain-selection policy | expansion interval | P23-DOM2, P23-DOM3 | yes | expansion factor and Gaussian tail example shown | none |
| 7 domain-selection policy | model hard bounds | P23-DOM4 | yes | interval intersection rule shown | none |
| 7 domain-selection policy | out-of-domain diagnostic | P23-DOM5, P23-DOM6 | yes | diagnostic fraction and acceptance threshold shown | none |
| 7 domain-selection policy | branch-freezing rule | P23-DOM7 | yes | perturbed-parameter domains fixed | none |
| 8 stabilization defaults | reference density | P23-STAB1 | yes | uniform reference on box displayed | none |
| 8 stabilization defaults | \(\tau_t\) and density floor | P23-STAB2, P23-STAB3, P23-STAB4 | yes | floor contribution and floored target values shown | none |
| 8 stabilization defaults | shift \(c_t\) | P23-STAB5 | yes | base-parameter max-log shift shown | none |
| 8 stabilization defaults | ridge scaling | P23-STAB6 | yes | trace-scaled ridge rule shown | none |
| 8 stabilization defaults | diagnostic vector | P23-STAB7 | yes | defensive mass, floor fraction, condition number, and shift magnitude shown | none |
| 8 stabilization defaults | threshold failure rules | P23-STAB8, P23-STAB9 | yes | defensive dominance and floor-fraction vetoes shown | none |
| 9 operational KR construction | conditional density evaluator | P23-KROPS1 | yes | conditional density object stored | none |
| 9 operational KR construction | CDF representation | P23-KROPS2, P23-KROPS3 | yes | quadrature CDF and baseline quadrature shown | none |
| 9 operational KR construction | clipping rule | P23-KROPS4 | yes | clipping is diagnostic, not density repair | none |
| 9 operational KR construction | inverse root equation | P23-KROPS5 | yes | inverse CDF equation shown | none |
| 9 operational KR construction | bisection/Newton fallback baseline | P23-KROPS6, P23-KROPS7, P23-KROPS8, P23-KROPS9 | yes | bisection interval update and stopping rule shown | none |
| 9 operational KR construction | endpoint, monotonicity, inverse diagnostics | P23-KROPS10 | yes | diagnostic vector includes endpoints, monotonicity, inverse residual, clip count | none |
| 10 multidimensional retained filter | retained coordinates and product features | P23-MD1, P23-MD2 | yes | tensor-product basis and dimension shown | none |
| 10 multidimensional retained filter | coefficient tensor/matrix shape | P23-MD3, P23-MD4 | yes | numerator and derivative matrices shown | none |
| 10 multidimensional retained filter | derivation of \(Q_t\) from contractions | P23-MD4a, P23-MD4b, P23-MD4c, P23-MD4d, P23-MD4e | yes | retained interface, non-retained mass, and exact coefficient matrix derived | none |
| 10 multidimensional retained filter | normalization and derivative normalization | P23-MD5 | yes | quotient derivative for matrix stored filter shown | none |
| 10 multidimensional retained filter | query basis matrix | P23-MD6 | yes | query matrix shape displayed | none |
| 10 multidimensional retained filter | evaluator and derivative evaluator | P23-MD7, P23-MD8 | yes | pointwise retained filter and derivative returns shown | none |
| 10 multidimensional retained filter | next-step query rule | P23-MD9 | yes | previous-state block of next fitting table specified | none |
| 11 branch manifest schema | manifest partition | P23-MAN1 | yes | frozen, differentiable, and report groups declared | none |
| 11 branch manifest schema | frozen fields | P23-MAN2 | yes | domains, bases, points, ranks, tolerances, shifts, floors, and initialization listed | none |
| 11 branch manifest schema | differentiable fields | P23-MAN3 | yes | target, LS, cores, masses, normalizer, carried filter listed | none |
| 11 branch manifest schema | report fields | P23-MAN4 | yes | residuals, condition numbers, ranks, failures listed | none |
| 11 branch manifest schema | manifest equality rule | P23-MAN5 | yes | branch equality iff frozen fields match | none |
| 11 branch manifest schema | finite-difference branch comparison | P23-MAN6, P23-MAN7 | yes | frozen fields equal; differentiable fields recomputed | none |

## Threaded Example Recurrence

| Required recurrence | P23 anchors | How the example is reused |
|---|---|---|
| filtering target | P23-E5, P23-E9 | Shows time-1 and time-2 adjacent-state Bayes numerators. |
| squared-TT density | P23-E6--P23-E8 | Shows square-root fit, defensive density, evidence, and carried filter. |
| preconditioning | P23-E10 | Shows the bridge residual used later in the preconditioning section. |
| gradient | P23-E11--P23-E12 | Shows the fixed-branch scalar and its derivative for \(T=2\). |

## Non-Gap Controls

| Control | P23 anchor or artifact | Status |
|---|---|---|
| P23 does not replace P22 | P23-C1, P23-C2 | `DRAFTED` |
| no executable-code scope | P23-C3 | `DRAFTED` |
| inherited exact-posterior non-claim | P19-90 | `PRESERVED` |
| inherited rank-stability non-claim | P19-91 | `PRESERVED` |
| inherited adaptive-derivative non-claim | P19-92 | `PRESERVED` |
| inherited HMC-convergence non-claim | P19-93 | `PRESERVED` |
| P22 preservation exact-anchor ledger | p22-preservation-ledger exact inherited-anchor table | `DRAFTED` |
| count validation | result artifact count-validation table; measured by `wc -l` and `pdfinfo`; P22 4815 TeX lines/55 pages, P23 5966 TeX lines/67 pages | `PASSED_AFTER_FINAL_BUILD` |
