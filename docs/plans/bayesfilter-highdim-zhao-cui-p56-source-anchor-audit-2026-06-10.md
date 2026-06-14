# P56 Zhao-Cui Source-Anchor Audit

metadata_date: 2026-06-10

status: REVISED_AFTER_CLAUDE_REVIEW

auditor: Codex, with Claude Code Opus max-effort read-only comparison

scope: BayesFilter implementation versus Zhao--Cui JMLR paper and bundled author
MATLAB source, excluding adaptive-route parity as a BayesFilter requirement but
requiring every fixed/HMC adaptation to preserve the author route.

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Do not declare BayesFilter source-faithful as "can solve paper-scale high-dimensional spatial SIR" yet. |
| Primary criterion status | FAIL for full source-faithful filtering; PASS only for partial one-step/source-target substrate and some fixed-branch diagnostics. |
| Veto diagnostic status | VETO: the implemented multistate grid/operator routes are not the author SIRT/IRT retained-object route and must be classified as `extension_or_invention` unless explicitly approved. |
| Main uncertainty | The production fixed-HMC transport object can still be implemented faithfully, but it must be grounded in the paper/source route, not in local grid/operator substitutes. |
| Next justified action | Implement the full fixed-HMC adaptation of the source route: sequential retained-object marginalization, transport fit/evaluation, proposal correction, and then d=18 SIR validation. |
| What is not concluded | No claim about adaptive TT-cross parity, S&P reproduction, or smoothing readiness. Generalized SV is not a Zhao--Cui source-faithfulness target unless separately scoped as an extension. |

## Source-Anchor Gate

The binding governance rule is `BLOCK_SOURCE_UNGROUNDED`.  For this lane,
faithfulness means paper/source anchoring before any implementation choice is
accepted.  Classifications used below:

| Classification | Meaning |
| --- | --- |
| `source_faithful` | Matches a cited operation in the Zhao--Cui paper and author source. |
| `fixed_hmc_adaptation` | Preserves the author algorithmic route but freezes randomness, rank choices, sample draws, bases, schedules, ESS-enhancement stop conditions, and resampling policy so the likelihood is differentiable and replayable. |
| `extension_or_invention` | Not present in the paper/source. It may be useful, but it cannot close a source-faithfulness gap without explicit approval. |

Adaptive Zhao--Cui parity is not a required missing gap for BayesFilter unless
explicitly requested.  But replacing the author retained-object SIRT/IRT route
with a different local-neighborhood, all-grid, or pairwise transition route is
not a fixed-HMC adaptation; it is `extension_or_invention`.

## Paper Anchors

| Paper operation | Checked anchor |
| --- | --- |
| Recursive posterior over adjacent states | PDF text `/tmp/zhao_cui_jmlr_2024.txt:339-366`: equations (9)--(11) define recursion over `p(theta,x_t,x_{t-1}|y_{1:t})` and marginalization over `x_{t-1}`. |
| Basic TT route | `/tmp/zhao_cui_jmlr_2024.txt:457-520`: Algorithm 1 builds nonseparable `q_t`, reapproximates by TT, integrates, and carries the marginal to the next step. |
| Squared TT defensive density | `/tmp/zhao_cui_jmlr_2024.txt:549-559`: equation (13), `phi(x)^2 + tau lambda(x)`. |
| Squared-TT marginalization and normalizer | `/tmp/zhao_cui_jmlr_2024.txt:592-626`: Proposition 2, equation (14), accumulated mass/Cholesky recursion and normalizer. |
| Conditional KR maps and inverse maps | `/tmp/zhao_cui_jmlr_2024.txt:627-670`: conditional densities, CDFs, KR map, inverse-root solve, and complexity. |
| Squared-TT sequential estimation | `/tmp/zhao_cui_jmlr_2024.txt:693-719`: Algorithm 2, equations (15)--(16), source route for `q_t` and integration of `x_{t-1}`. |
| Proposal sampling and correction | `/tmp/zhao_cui_jmlr_2024.txt:835-924`: equations (21)--(23), Algorithm 3 conditional KR proposal and weight correction. |
| Preconditioning | `/tmp/zhao_cui_jmlr_2024.txt:1461-1548`, `/tmp/zhao_cui_jmlr_2024.txt:1581-1608`, `/tmp/zhao_cui_jmlr_2024.txt:1636-1706`: equations (30)--(35), Algorithm 5, retained marginal step (c.2). |
| Paper-scale SIR | `/tmp/zhao_cui_jmlr_2024.txt:2249-2365`: state is `(S_1,I_1,...,S_9,I_9) in R^18`, `T=20`, observations of `I_j`, rank ladder `{10,20,40}`, and linear preconditioning. |

## Author Source Anchors

| Source operation | Checked anchor |
| --- | --- |
| SIR example settings | `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-17`, `:39-56`: `m=18`, `T=20`, `N=5e3`, `tau=10`, squared TTSIRT, Lagrange/algebraic basis, max rank 40, `full_sol(...); solve(...)`. |
| Full sequential loop | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43`: prior samples, `push_samples`, augment `[theta; x_t; x_{t-1}]`, `reapprox`, inverse SIRT sampling, proposal correction. |
| Previous retained marginal | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:72-81`: for `t>1`, `marginalise(sirt_temp,1)` and `eval_pdf` define the previous retained density. |
| Recenter and fit | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:46-124`: ESS enhancement, `computeL`, shift constant, `InputData`, `TTIRT`/`TTSIRT`, log marginal `log(sirt.z)-const`. |
| Target formula | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:132-135`: previous/prior term minus transition and likelihood logs, with nonfinite values set to infinity. |
| Preconditioned route | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m:33-260`: ESS enhancement, preconditioner fit, maps `Tu2x`/`Tx2u`, residual fit, proposal correction. |
| Push samples | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/ssmodel.m:45-59`: transition push and likelihood weight normalization. |
| SIRT construction | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/SIRT.m:50-86`: potential-to-square-root-density conversion, CDF construction, `marginalise`. |
| IRT/KR surface | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m:152-188`, `:192-213`, `:217-270`, `:299-354`: inverse/forward/conditional maps, pdf, potential, random samples. |
| TTSIRT marginalization | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:1-87`: mass-matrix/QR recursion and `obj.z = obj.fun_z + obj.tau`. |
| TTSIRT potential/pdf | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_potential_reference.m:1-36`: normalized potential `log(obj.z)-log(fx+tau)+mlogw`. |

## Existing BayesFilter Implementation Classification

| BayesFilter component | Classification | Evidence |
| --- | --- | --- |
| `bayesfilter/highdim/source_route.py` push/recenter/normalizer helpers | `fixed_hmc_adaptation` partial substrate | Required operations and forbidden markers are declared at lines 20-44; push/augment mirrors source shape at lines 1022-1092; recenter mirrors `computeL` at lines 1211-1283; normalizer update exists at lines 1325-1337. |
| `bayesfilter/highdim/source_route.py` transport protocol and retained manifest contracts | governance/interface substrate only, with proposal-density semantic risk | `SourceRouteTransportProtocol` and manifest checks are necessary boundaries, but they are not an implemented fixed-HMC source transport. They do not yet provide author-equivalent marginalization, `eval_pdf`, forward KR, or conditional KR semantics. The current proposal-density hook uses reference-density semantics and must be repaired before a real SIRT/KR transport can be source-faithful. |
| `source_route_one_step_reapproximation` | `fixed_hmc_adaptation` boundary only | Lines 1173-1208 deliberately refuse `t != 1` and any previous retained object. |
| `source_route_retained_object_manifest` | `fixed_hmc_adaptation` governance substrate | Lines 1411-1480 forbid all-grid retained storage and pairwise-grid propagation for `SOURCE_FAITHFUL_ROUTE_LABEL`. |
| `bayesfilter/highdim/squared_tt.py` | mixed: source-like density, not source-faithful marginalization/KR | Lines 144-181 implement `h^2 + tau q0` and normalizer; lines 183-201 require all axes retained; lines 203-225 label marginal as metadata; lines 227-285 use tensor-product grid integration for conditionals. |
| `bayesfilter/highdim/transport.py` | `extension_or_invention` diagnostic | Lines 1-3 call it grid-based KR diagnostics; lines 61-149 build grid CDF/inversion from `SquaredTTDensity.conditional_density`, not author CDFconstructor/mass-matrix KR. |
| `bayesfilter/highdim/fitting.py` `FixedTTFitter` | `extension_or_invention` candidate until proven otherwise | Lines 181-302 implement fixed-rank deterministic ALS; lines 595-600 explicitly do not claim adaptive TT-cross, rank adaptation, filtering, or derivative correctness. No inspected paper/source anchor proves this fitter preserves the author `TTFun`/`TTSIRT` Proposition-2/KR semantics. |
| `multistate_nonlinear_fixed_design_tt_value_path` | `extension_or_invention` for source-faithfulness | Lines 1002-1008 say all-state tensor-product grid and not adaptive TT-cross, SIRT, or paper-scale Zhao--Cui; lines 1130-1138 and 1190-1198 exclude high-dimensional scalability. |
| `multistate_tt_grid_retained_filter` and predictive propagation | `extension_or_invention` | Lines 1353-1368 build all-axes retained grid; lines 2246-2356 propagate through pairwise grid transition. This is explicitly forbidden by `source_route.py` for source-faithful retained objects. |
| `bayesfilter/highdim/transition_route.py` and `rank_budget.py` | `extension_or_invention` | `transition_route.py:1-48` is a memory-bounded local-neighborhood/operator route; `rank_budget.py` uses `R_eff` memory forecasts. The author paper/source route uses SIRT/IRT retained marginalization and conditional maps, not this operator route. |
| P55 result | partial substrate, not closure | `docs/plans/bayesfilter-highdim-zhao-cui-p55-source-paper-code-repair-result-2026-06-10.md:13-18` accepts a partial source substrate and states no complete sequential fixed/source-contract implementation; lines 110-121 list retained-object marginalization, full sequential loop, fixed transport integration, preconditioning, and SIR d=18 as open. |

## Discrepancy Ledger And Fixes

### D01: Full Sequential Source-Route Loop Missing

Classification: source-faithfulness gap.

Evidence: The author loop is `full_sol.solve` lines 21-43: initialize, push,
augment, reapproximate, inverse-map sample, correct weights.  BayesFilter has
the one-step boundary `source_route_one_step_reapproximation` at
`source_route.py:1173-1208`, which refuses `t>1`.

Fix: Implement a fixed-HMC adaptation of `full_sol.solve` over `t=1..T`.  The
loop must store a retained transport object, affine frame, normalizer increment,
samples, correction weights, and previous-step manifest.  Every stochastic
author draw must be replaced by predeclared/frozen reference draws.

### D02: Previous Retained-Object Marginalization Missing

Classification: source-faithfulness gap.

Evidence: Paper equations (10)--(11) and Algorithm 2(c) require the previous
retained density `p(theta,x_t|y_{1:t})` for the next step.  Author source
implements this by `marginalise(sirt_temp,1)` and `eval_pdf` in `full_sol.m:72-81`.
BayesFilter explicitly states `previous retained-object marginalization is not
implemented` in `source_route.py:506-510` and `:1183-1196`.

Fix: Add a retained transport object with a `marginalize_retained()` or
equivalent source-route method that evaluates the previous marginal
`p(theta,x_{t-1}|y_{1:t-1})` in the recentered/reference coordinates, including
the previous affine determinant.  The implementation must be based on
Proposition 2 mass-matrix/QR marginalization or a documented fixed-HMC
adaptation of it.

### D03: Production TTSIRT/TTIRT-Equivalent Transport Fit Missing

Classification: source-faithfulness gap with fixed-HMC adaptation allowed.

Evidence: Author code constructs `TTIRT`/`TTSIRT` in `full_sol.m:101-121` and
uses `eval_irt` and `eval_pdf` in lines 33-38.  Deep-tensor source exposes
`eval_irt`, `eval_rt`, `eval_cirt`, `eval_pdf`, and `random` in `AbstractIRT.m`.
BayesFilter has only `SourceRouteTransportProtocol` plus analytic test
transports; the protocol does not require forward KR or conditional KR
interfaces, and `FixedTTFitter` is a fixed-rank ALS for square-root functions,
not a retained SIRT object with marginal/KR/eval_pdf semantics.

Fix: Build a deterministic `FixedTTSIRTTransport` around fixed TT cores, source
bases, defensive density, normalizer, mass recursions, and KR maps.  It should
expose the source-route protocol methods plus `eval_pdf`/potential,
marginalization, forward KR, inverse KR, conditional KR, and a
Jacobian-aware proposal log density on transported/local samples needed by
Algorithm 3, Algorithm 5, filtering, and later smoothing.

### D04: Proposition 2 Mass-Matrix/QR Marginalization Not Implemented

Classification: source-faithfulness gap.

Evidence: Paper Proposition 2 lines 596-626 and author
`@TTSIRT/marginalise.m:25-85` use accumulated mass matrices and QR/Cholesky-like
recursions to integrate dimensions and compute `z`.  BayesFilter
`SquaredTTDensity.marginal_density` lines 203-225 returns metadata and says
squared marginal values are evaluated by grid integration; `conditional_density`
lines 227-285 integrates suffix axes on a tensor-product grid.

Fix: Implement source-style squared-TT marginal contractions for all retained
prefix/suffix orders used by the author route.  The result must provide
normalized marginal potential/pdf and normalizer semantics matching
`eval_potential_reference.m:1-36`, not only metadata.

### D05: Grid-Based KR Diagnostics Are Not Author KR Maps

Classification: extension/invention relative to source route.

Evidence: Paper lines 637-670 describe CDF construction from Proposition 2
conditional densities, with algebraic/pseudospectral CDF evaluation and fixed
root finding.  Author source constructs per-axis CDF objects in `SIRT.m:80-85`
and uses `eval_irt_reference`, `eval_rt_reference`, and `eval_cirt_reference`.
BayesFilter `transport.py` is explicitly "Grid-based KR transport diagnostics"
and uses trapezoid CDFs on fixed grids.

Fix: Keep `transport.py` as a diagnostic lower rung.  Do not use it to claim
Zhao--Cui source faithfulness.  Add source-style CDF constructors/inversion for
the fixed transport object, or explicitly classify any grid CDF as a reviewed
fixed-HMC approximation with its own error tests and nonclaims.

### D06: Retained Sampling And Proposal Correction Are Not Source-Closed

Classification: source-faithfulness gap.

Evidence: Paper Algorithm 3 and equation (23) require conditional proposal
sampling and weight correction.  Author source lines `full_sol.m:33-38` use
`eval_irt`, affine recovery, and `exp(-fun_post(r))./eval_pdf(sirt,r)`.
BayesFilter has `source_route_generate_retained_samples` lines 1116-1170, but it
depends on a real source-route transport object that does not yet exist.  It
also computes proposal density through `transport.log_reference_density` before
or alongside inverse transport; this may be equivalent for a correctly
implemented analytic test double, but it is not the source SIRT semantics by
itself.  The author denominator is `eval_pdf(sirt,r)` after `eval_irt`, i.e. an
approximate-density/KR-Jacobian density on local transported samples.  The
current API risks baking in base/reference density in its place.

Fix: After D03/D04/D05, wire retained sample generation into the sequential loop
and add tests that verify the correction sign, determinant policy, proposal
density semantics, and normalizer identities against small analytic targets and
a reduced author-code stage.

Immediate API fix: change the transport protocol so proposal correction can call
an `eval_pdf`-equivalent method on local transported samples, or a documented
Jacobian-aware `log_proposal_density(local_samples, reference_samples)` method.
Do not use base/reference density alone for real source-route transports.

### D07: ESS Enhancement And Sample Reuse Are Incomplete Under Fixed-HMC Policy

Classification: fixed-HMC adaptation gap.

Evidence: Author `full_sol.reapprox` lines 49-67 and `pre_sol.reapprox` lines
33-104 increase samples when ESS is low, draw from previous SIRT, push samples,
resample by weights, and compute recentering.  BayesFilter has ESS and recenter
helpers, but no full deterministic enhancement loop coupled to the sequential
transport object.

Fix: Define a fixed enhancement schedule: predeclared maximum enhancement
rounds, frozen reference draws for each round, frozen ESS stop conditions,
frozen resampling policy, fixed stopping diagnostics, and a rule that the
likelihood computation never mutates rank/basis/sample schedules.  This
preserves the author mechanism while satisfying HMC replayability.

### D08: Preconditioned Algorithm 5 Route Missing As An Implementation

Classification: source-faithfulness gap for paper-scale SIR/predator-prey.

Evidence: The paper says SIR uses Algorithm 2 with linear preconditioning
(`/tmp/zhao_cui_jmlr_2024.txt:2362-2365`).  Section 5 and Algorithm 5 define the
preconditioned route and retained marginal step (c.2).  Author `pre_sol.m:131-181`
selects bridging/preconditioning formulas; lines 187-243 fit preconditioner and
residual SIRTs; lines 245-255 generate samples and correction weights.
BayesFilter has residual identity helpers in `source_route.py:1340-1376`, but not
the two-layer preconditioner/residual retained object.

Fix: Implement preconditioning only after D01-D06 are working.  Start with the
paper/source linear Gaussian preconditioner, then add the fixed-HMC version of
the residual SIRT and Algorithm 5(c.2) retained marginal.

### D09: Paper-Scale Spatial SIR Is Not Implemented

Classification: source-faithfulness gap.

Evidence: Paper lines 2249-2365 and author `eg3_sir/mainscript.m:14-56` define
the d=18 state, T=20, rank ladder, and preconditioning settings.  BayesFilter
P52/P53 work introduced a local-neighborhood/rank-budget operator route, but
that route is not in Zhao--Cui paper/source and `transition_route.py:1-48`
contains nonclaims for filtering correctness and d=18 readiness.

Fix: Validate d=18 only through the source-route retained-object pipeline.  Use
the author settings as target anchors: state dimension 18, T=20, observation of
infectious compartments, rank ladder 10/20/40 or fixed-HMC predeclared ranks
grounded in that ladder.  Do not substitute the local-neighborhood operator
route as the source-faithful SIR implementation.

### D10: Multistate Fixed-Design Grid Route Is A Useful Diagnostic But Wrong Source Route

Classification: extension/invention.

Evidence: `filtering.py:1002-1008` says the P46 adapter is all-state
tensor-product grid and not SIRT or paper-scale Zhao--Cui; `filtering.py:1353-1368`
builds all-axes retained grids; `filtering.py:2246-2356` performs pairwise grid
transition propagation.  These storage/transition choices are forbidden for
source-faithful retained objects in `source_route.py:1459-1480`.

Fix: Quarantine this route in documentation/tests as a small diagnostic
comparator.  It may help test low-dimensional value paths, but it must not be
used as evidence that Zhao--Cui filtering is implemented.

### D11: Rank/Memory Calibration Is Being Applied To The Wrong Route

Classification: extension/invention for source-faithfulness.

Evidence: Author SIR rank control is the TT/SIRT rank ladder in
`mainscript.m:48-51` and paper lines 2359-2365.  BayesFilter `rank_budget.py`
forecasts `R_eff` for a local/operator route, and `transition_route.py` defines
local-neighborhood sparse transition metadata.

Fix: For source faithfulness, rank selection must be tied to fixed TT/SIRT
transport cores and author rank ladder/basis settings.  Memory budgets are still
important, but they should budget the fixed transport fit, marginalization/KR
state, and sample batches, not an invented transition operator.

### D12: Source Model Callback Parity Needs Explicit Tests

Classification: source-faithfulness test gap.

Evidence: Author model shell uses `st_process`, `transition`, `like`, `priorpdf`,
and `priorsam` through `ssmodel.m:45-59` and `full_sol.fun_into_sirt`.
BayesFilter has Python model callbacks, but the current audit did not establish
line-by-line equality for SIR/predator-prey/SV source model formulas.

Fix: Add source-anchor tests or ledgers for each production model: parameters,
state ordering, observation model, process noise, prior, transition density,
likelihood density, and time indexing.  This must precede model-scale claims.

### D13: Smoothing/Backward Conditionals Are Not Filtering-Likelihood Closure

Classification: out-of-current-scope unless requested.

Evidence: Paper and author source include smoothing (`full_sol.smooth`), and the
P10 crosswalk lists smoothing as code-present.  User has scoped current needs to
HMC-compatible filtering likelihood/gradients and has excluded adaptive parity
and S&P reproduction.

Fix: Keep smoothing as a future optional paper-feature gap, not a blocker to
filtering likelihood once D01-D12 pass.

### D14: Generalized SV Is Not A Zhao-Cui Source-Faithfulness Gap

Classification: extension/same-target comparator.

Evidence: Zhao--Cui examples include stochastic volatility, SIR, predator-prey,
and Kalman; generalized SV as discussed in this project is not an author-code
paper model.  It can still be a good comparison target for CUT4 vs fixed
source-route machinery, but not a missing Zhao--Cui source implementation.

Fix: Label generalized SV tests as BayesFilter extensions or equality-target
comparators.  Do not use them to close or block the source-faithful spatial SIR
implementation claim.

## Required Fix Order

1. Lock route claims: any use of `transition_route.py`, `rank_budget.py`, or
   all-grid retained storage must be marked `extension_or_invention`.
2. Implement fixed source-route transport object: fixed TT square-root fit,
   defensive density, source normalizer, source marginalization, pdf, inverse
   KR, forward KR, conditional KR maps, and source-correct proposal-density
   semantics.
3. Implement previous retained-object marginalization and previous-density
   evaluation with affine determinant handling.
4. Implement full sequential loop over `t=1..T` using frozen random/reference
   draws, fixed ranks/bases/schedules, frozen ESS stop conditions, and frozen
   resampling policy.
5. Wire proposal correction and log normalizer updates into the sequential loop.
6. Add source model parity ledgers/tests for SV, SIR, predator-prey.
7. Run small reference ladders: one-step analytic target, two-step scalar
   nonlinear target, reduced Kalman/SV, then SIR d=18.
8. Implement preconditioning after the full route passes, starting with the
   paper/source linear preconditioner.
9. Only after d=18 source route passes should d=50/d=100 be considered; those
   dimensions are extrapolation tests, not paper-faithfulness prerequisites.

## Hostile Review Notes

- A deterministic fixed-rank ALS implementation is not automatically faithful.
  It becomes a fixed-HMC adaptation only if it fits the same square-root target,
  provides the same retained marginal/KR/pdf semantics, and freezes rather than
  replaces the author route.
- A good low-dimensional grid result does not validate the source route.  Grid
  routes are diagnostics unless tied back to the author retained-object route.
- A memory-feasible local transition operator is not evidence for Zhao--Cui
  SIRT scalability.  It answers a different design question.
- The key blocker for paper-scale SIR is not just rank choice.  The missing
  pieces are retained-object marginalization, real transport fit/evaluation,
  and a sequential source loop.

## Claude Comparison

Claude Opus max-effort read-only audit was run and recorded in
`docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-claude-review-2026-06-10.md`.
Claude returned `VERDICT: REVISE`.  The main negative decision was accepted, but
Claude required stricter classification and three material additions:

1. Fixed-HMC adaptation must freeze ESS-enhancement stop conditions and
   resampling policy, not only random draws/ranks/bases/schedules.
2. The source-route transport protocol is interface/governance substrate only
   until it has forward KR and conditional KR interfaces in addition to inverse
   transport, proposal density, and normalizer methods.
3. `FixedTTFitter` is not a fixed-HMC adaptation candidate by itself.  It is an
   `extension_or_invention` candidate until a source/paper-grounded proof or
   test ladder shows that it preserves the author `marginalise`, `eval_pdf`,
   `eval_rt`, and `eval_cirt` semantics.
4. A late full-prompt Claude response found a sharper issue: the current
   `source_route_generate_retained_samples` denominator uses
   `transport.log_reference_density(reference) - log|det L|`, whereas the
   author correction divides by `eval_pdf(sirt,r)` after `eval_irt`.  For real
   SIRT/KR transports, source faithfulness requires an `eval_pdf`-equivalent or
   Jacobian-aware proposal density on transported/local samples, not base
   reference density alone.

All three corrections are incorporated above.  The reconciled conclusion is:
BayesFilter has a partial source-route substrate, but it still lacks the
transport/marginalization/KR/sequential machinery required to claim a faithful
paper-scale Zhao--Cui spatial SIR implementation.
