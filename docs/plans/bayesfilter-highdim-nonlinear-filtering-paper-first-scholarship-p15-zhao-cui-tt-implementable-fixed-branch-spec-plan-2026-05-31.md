# P15 Plan: Zhao-Cui TT Implementable Fixed-Branch Filtering Specification

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao-Cui code audit, paper-code crosswalk, filtering-scalar, reproducibility, and gradient-feasibility ledgers.
- P11 fixed-branch derivative note.
- P12 self-contained proof expansion note.
- P13 human-readable note and ledgers.
- P14 pedagogical mathematical note and ledgers.

what_is_not_concluded:
- No posterior accuracy claim.
- No claim that the adaptive Zhao-Cui companion code has a global analytical gradient.
- No HMC convergence claim.
- No production BayesFilter implementation.
- No default-method recommendation.
- No numerical validation on the target high-dimensional nonlinear model unless a later executed artifact actually implements and tests it.

## Purpose

P14 teaches the squared tensor-train filtering idea, but it is still not an
implementation specification.  The next document must close the remaining gap:

> If the document is given to Codex or Claude Code alone, it should be possible
> to implement the declared fixed-branch TT filter and its analytical gradient
> without opening Zhao--Cui, Cui--Dolgov, the companion code, or background TT
> references.

This plan therefore narrows the target.  P15 will not try to specify every
possible Zhao--Cui-style adaptive TT filter.  It will specify one concrete
minimal fixed-branch squared-TT filtering algorithm, prove the filtering and
same-scalar gradient claims for that algorithm, and give a minimal runnable
example plus finite-difference parity test.

## Reader And Reviewer Standard

The reader is an educated academic from chemistry, physics, numerical analysis,
or applied mathematics.  The document must teach with mathematics first and
prose second:

1. define the mathematical object;
2. derive the formula;
3. show how it is computed;
4. explain in words why the formula matters;
5. state the failure mode in mathematical or numerical terms.

Source/code audit language belongs in ledgers and appendices, not in the main
teaching flow.

## Allowed Writes For P15 Execution

- New P15 artifacts under `docs/plans/`.
- A compiled P15 PDF beside the P15 LaTeX source.
- A minimal runnable P15 reference example under `docs/plans/`, preferably a
  small pure-Python/NumPy script unless the execution plan explicitly chooses
  Octave.
- Do not overwrite P10--P14 artifacts.
- Do not edit `docs/chapters/` unless the human explicitly asks to promote the
  result into a chapter later.
- Do not edit production `bayesfilter/`.
- Do not edit DPF lane, student-baseline, controlled-DPF, public APIs, or
  unrelated dirty files.
- Do not commit.

## Required P15 Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-note-2026-05-31.tex`
- compiled PDF beside it
- `...p15-zhao-cui-tt-implementable-fixed-branch-spec-ledger-2026-05-31.md`
- `...p15-zhao-cui-tt-algorithm-choices-ledger-2026-05-31.md`
- `...p15-zhao-cui-tt-gradient-derivation-ledger-2026-05-31.md`
- `...p15-zhao-cui-tt-reference-example-ledger-2026-05-31.md`
- `...p15-zhao-cui-tt-source-support-ledger-2026-05-31.md`
- `...p15-zhao-cui-tt-citation-venue-metadata-ledger-2026-05-31.md`
- `...p15-zhao-cui-tt-backward-snowball-ledger-2026-05-31.md`
- `...p15-zhao-cui-tt-forward-snowball-ledger-2026-05-31.md`
- `...p15-zhao-cui-tt-claim-support-ledger-2026-05-31.md`
- `...p15-zhao-cui-tt-omitted-paper-risk-ledger-2026-05-31.md`
- `...p15-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md`
- `...p15-zhao-cui-tt-claude-review-ledger-2026-05-31.md`
- `...p15-zhao-cui-tt-discrepancy-report-2026-05-31.md`
- `...p15-zhao-cui-tt-implementable-fixed-branch-spec-result-2026-05-31.md`
- minimal runnable example:
  `...p15-zhao-cui-tt-fixed-branch-minimal-example-2026-05-31.py`

Every ledger must contain:
- `metadata_date`
- `seed_papers`
- `what_is_not_concluded`

## Evidence Contract

Question:

Can P15 turn the Zhao--Cui-style fixed-branch squared-TT filter from a teaching
derivation into a self-contained implementation specification for a declared
approximate filtering likelihood and its analytical same-scalar gradient?

Baseline:

- P14 pedagogical mathematical note.
- P10 inspected Zhao--Cui companion-code scalar path and source anchors.
- Fixed sparse-grid Gaussian projection filter from `ch34` as the competing
  high-dimensional candidate.

Primary pass criteria:

- The note specifies one exact algorithmic value path, not a family of
  underspecified TT filters.
- The note defines domain maps, reference measure, basis functions, mass
  matrices, fitting points, TT core construction, rank protocol, defensive
  density, defensive mass, scaling shift, marginalization, saved branch
  objects, gradient recursion, stabilization diagnostics, finite-difference
  parity test, and a minimal runnable example.
- Each of the five P14 gaps is explicitly repaired:
  1. TT fitting is no longer a black box.
  2. The filter recursion is operational, including how the next filter object
     is represented and evaluated.
  3. The gradient is derived through the chosen fitting algorithm.
  4. A complete worked example is included.
  5. Persuasive diagnostics and failure tests are specified.
- Each item in the user's missing-implementation list is explicitly mapped to a
  section/equation/pseudocode block in the note.
- The main text uses human mathematical language, not governance labels.
- Claude accepts after hostile plan and execution review, or remaining issues
  are minor editorial/layout issues.

Veto diagnostics:

- Any remaining phrase equivalent to "fit a TT" without a fully specified
  fitting algorithm.
- Any use of "fixed branch" without listing the exact branch objects that are
  frozen and saved.
- Any likelihood-gradient formula that does not differentiate the same scalar
  computed by the forward pass.
- Any adaptive rank, pivot, fitting-point, truncation, or sign change treated
  as globally smooth.
- Any claim that normalized approximate filtering implies posterior accuracy.
- Any reliance on source-paper pointers instead of a derivation in the P15
  notation.
- Any missing minimal runnable example or missing finite-difference parity
  protocol.
- LaTeX or reference-example validation failure.

Explanatory diagnostics:

- Fit residuals, rank storage, conditioning, defensive-mass ratio, and
  finite-difference parity errors explain failure modes; they do not establish
  scientific validity by themselves.
- A scalar or low-dimensional runnable example tests implementability, not
  high-dimensional performance.

Artifact preserving the result:

- The P15 note, runnable example, ledgers, Claude review ledger, discrepancy
  report, and result file.

## Chosen Minimal Fixed-Branch Variant

P15 will specify this concrete algorithm.  Deviations require a plan patch and
Claude re-review.

### Variables And Domain

At time \(t\), the augmented physical variable is
\[
  r_t=(x_t,\vartheta,x_{t-1})\in\mathbb R^D.
\]
The fixed branch chooses a finite hyperrectangle
\[
  \Omega_t=\prod_{k=1}^D [\ell_{t,k},u_{t,k}]
\]
and affine coordinate maps
\[
  r_{t,k}=a_{t,k}+h_{t,k} z_k,\qquad
  a_{t,k}=\frac{u_{t,k}+\ell_{t,k}}2,\qquad
  h_{t,k}=\frac{u_{t,k}-\ell_{t,k}}2,\qquad
  z_k\in[-1,1].
\]
The reference domain is \([-1,1]^D\) with Lebesgue measure \(\mathrm dz\).
The transformed unnormalized density is
\[
  \widetilde q_t(z;\alpha)
  =
  q_t(\Psi_t(z);\alpha)\prod_{k=1}^D h_{t,k}.
\]
For the fixed-branch derivative, \(\ell_{t,k},u_{t,k},a_{t,k},h_{t,k}\) are
branch objects frozen at the declared branch.  The note may explain how a
nominal branch can be selected, but the derivative target freezes it.

### Basis And Mass Matrices

Use normalized Legendre basis functions on \([-1,1]\):
\[
  b_{k,a}(z)=\sqrt{\frac{2a+1}{2}}\,P_a(z),\qquad a=0,\ldots,p_k-1.
\]
The note must give the recurrence for evaluating \(P_a\):
\[
  P_0(z)=1,\qquad P_1(z)=z,\qquad
  (a+1)P_{a+1}(z)=(2a+1)zP_a(z)-aP_{a-1}(z).
\]
The mass matrices are
\[
  M_k[a,b]=\int_{-1}^1 b_{k,a}(z)b_{k,b}(z)\,\mathrm dz=\delta_{ab}.
\]
No other primary basis family is allowed in the P15 value path.  Any mention
of unnormalized Legendre, Lagrange, Hermite, Fourier, wavelet, or piecewise
bases must be confined to an out-of-scope appendix and marked
`OPTIONAL_NOT_USED`.

### Fixed Fitting Points

Use this deterministic fixed design and no other primary design.  Let
\(p_1,\ldots,p_D\) be the first \(D\) primes and let
\[
  \operatorname{radinv}_{p}(j)
  =
  \sum_{m=0}^{M(j,p)} d_m p^{-(m+1)},
  \qquad
  j=\sum_{m=0}^{M(j,p)} d_m p^m,\quad d_m\in\{0,\ldots,p-1\}.
\]
For \(j=1,\ldots,N_{\rm fit}\),
\[
  z^{(j)}_k=2\,\operatorname{radinv}_{p_k}(j)-1.
\]
The fit weights are fixed uniform weights
\[
  W_t=\frac{1}{N_{\rm fit}}I.
\]
The points, coordinate primes, and weights are saved branch objects and are
not resampled or changed during differentiation.

### Fixed-Rank Ridge ALS TT Fit

Use fixed TT ranks
\[
  r_0=r_D=1,\qquad r_k\ \text{declared for }k=1,\ldots,D-1.
\]
Ranks are not adapted inside the gradient target.

Fit the shifted square-root target
\[
  y_j(\alpha)
  =
  \exp(c_t/2)
  \sqrt{\widetilde q_t(z^{(j)};\alpha)}
\]
by a fixed number \(S\) of alternating least-squares sweeps.  Holding all
cores except core \(k\) fixed, solve the ridge normal equations
\[
  N_{t,k}^{(s)}g_{t,k}^{(s)}
  =
  d_{t,k}^{(s)},\qquad
  N_{t,k}^{(s)}
  =
  A_{t,k}^{(s)\top}W_t A_{t,k}^{(s)}+\rho I,\qquad
  d_{t,k}^{(s)}
  =
  A_{t,k}^{(s)\top}W_t y_t.
\]
The note must derive the design row using left environment, local basis vector,
and right environment:
\[
  A_{j,\cdot}
  =
  R_j^\top\otimes b_k(z^{(j)}_k)^\top\otimes L_j.
\]
The primary path uses one explicit initialization:

- set all entries of every core to zero;
- set the basis-index-zero slice \(C_{t,k,0}[1,1]=1\) along the rank-chain
  diagonal where dimensions allow;
- multiply the first core by the weighted mean
  \(\bar y=N_{\rm fit}^{-1}\sum_j y_j\);
- set every other admissible diagonal constant entry to one and all
  nonconstant entries to zero.

If ranks exceed one, the constant component is placed on diagonal index one and
all other rank channels are initialized to zero.  The primary sweep order is
left-to-right cores \(1,\ldots,D\), then right-to-left cores \(D,\ldots,1\),
repeated for exactly \(S\) full bidirectional sweeps.  The core vectorization
order is lexicographic in \((\ell_{\rm left},a,\ell_{\rm right})\), with the
right rank index varying fastest.  Ridge \(\rho>0\), ranks, \(S\), and
\(N_{\rm fit}\) are declared branch constants.  Alternatives are out of scope
unless the plan is patched and re-reviewed.

### Defensive Density, Defensive Mass, And Shift

Use the uniform defensive density on the reference domain:
\[
  \lambda_t(z)=2^{-D}.
\]
Use the mandatory fixed defensive mass
\[
  \tau_t=\epsilon_\tau\, 2^D,\qquad \epsilon_\tau>0
\]
with \(\epsilon_\tau\) declared once in the branch.  This gives a uniform
defensive floor \(\epsilon_\tau\) on \([-1,1]^D\).  The primary fixed-branch
target has \(\partial_i\tau_t=0\).  Any differentiable \(\tau_t(\alpha)\)
extension is out of scope for the primary P15 algorithm and must be marked
`OPTIONAL_NOT_USED`.

Use the mandatory fixed stabilizing shift \(c_t\), computed at nominal branch
creation from the fixed design points:
\[
  c_t=-\max_j \log \widetilde q_t(z^{(j)};\alpha_0).
\]
For the primary fixed-branch derivative, \(c_t\) is frozen and
\(\partial_i c_t=0\).  The note must state that finite-difference parity tests
reuse this frozen \(c_t\) at \(\alpha_0\) for all \(\alpha_0\pm h e_i\).
Any differentiable shift is a different scalar and is out of scope for the
primary P15 algorithm.

### Squared-TT Normalizer And Marginalization

The fitted square-root TT is
\[
  \phi_t(z)=G_{t,1}(z_1)\cdots G_{t,D}(z_D).
\]
The approximate density is
\[
  \widehat q_t(z)=\phi_t(z)^2+\tau_t2^{-D}.
\]
The normalizer is
\[
  \widehat z_t=\int_{[-1,1]^D}\widehat q_t(z)\,\mathrm dz
  =R_{t,0}+\tau_t,
\]
where \(R_{t,0}\) is obtained by mass contraction.

The note must derive marginalization in squared-TT form.  For the square term,
define square cores
\[
  H_{t,k}(z_k)=G_{t,k}(z_k)\otimes G_{t,k}(z_k).
\]
Integrating a coordinate replaces \(H_{t,k}\) by its mass contraction.  Kept
coordinates retain \(H_{t,k}(z_k)\).  The next filter is represented as a
normalized numerator object:
\[
  a_t(z_{\rm keep})
  =
  \int \phi_t(z)^2\,\mathrm dz_{\rm old}
  +
  \tau_t \int 2^{-D}\,\mathrm dz_{\rm old},
  \qquad
  \widehat p_t(z_{\rm keep})=a_t(z_{\rm keep})/\widehat z_t.
\]
The saved next-filter object must include enough information to evaluate
\(\widehat p_t\), \(\partial_i\widehat p_t\), \(\log \widehat p_t\), and
\(\partial_i\log\widehat p_t\) at fitting points for the next time step.
This must not be left abstract.  The P15 note and runnable example must use
one concrete next-filter representation:

- store square-root TT cores \(G_{t,k}\);
- store square cores \(H_{t,k}=G_{t,k}\otimes G_{t,k}\) for kept
  coordinates;
- store integrated environments for every old-state coordinate;
- store the uniform defensive kept-coordinate mass
  \(\tau_t 2^{-D}\prod_{k\in{\rm old}}2\);
- store \(\widehat z_t\);
- evaluate \(a_t(z_{\rm keep})\) by contracting kept square cores with the
  precomputed old-coordinate environments and adding the defensive kept term;
- evaluate
  \[
    \log \widehat p_t(z_{\rm keep})
    =
    \log a_t(z_{\rm keep})-\log\widehat z_t;
  \]
- evaluate derivatives by storing and contracting \(\dot H_{t,k}\),
  differentiated old-coordinate environments, \(\dot a_t\), and
  \(\dot{\widehat z}_t\), then using
  \[
    \partial_i\log \widehat p_t
    =
    \frac{\partial_i a_t}{a_t}
    -
    \frac{\partial_i\widehat z_t}{\widehat z_t}.
  \]

The plan must stop if this representation cannot be specified and implemented
without reading the original papers.

### Conditional/KR Maps

The minimal P15 filtering likelihood and gradient do not require conditional
Knothe--Rosenblatt maps.  If the note includes them, it must put them in a
clearly optional section:

- define conditionals by repeated squared-TT marginal contractions;
- compute one-dimensional CDFs by fixed quadrature on \([-1,1]\);
- invert CDFs by a declared deterministic root finder;
- state that this optional map is for sampling/diagnostics, not needed for the
  declared likelihood scalar or gradient.

No gradient claim may depend on optional KR sampling.

## Required P15 Note Structure

1. What This Specification Implements
2. State-Space Filtering Object And Approximate Likelihood
3. Fixed Computational Domain And Reference Measure
4. Legendre Basis, Evaluation Recurrence, And Mass Matrices
5. Tensor-Train Functions And Squared-TT Densities
6. Fixed Fitting Design Points
7. Fixed-Rank Ridge ALS Construction Of The Square-Root TT
8. Normalizer, Defensive Density, Shift, And Approximate Log-Likelihood
9. Marginalization In Squared-TT Form And The Next Filter Object
10. Saved Branch Data Structures
11. Forward Filtering Algorithm In Pseudocode
12. Derivative Of Target Values And Previous-Filter Evaluations
13. Derivative Through Fixed ALS Sweeps
14. Derivative Of Mass Contractions, Marginals, And The Likelihood Scalar
15. Complete Gradient Algorithm In Pseudocode
16. Numerical Stabilization And Failure Diagnostics
17. Finite-Difference Parity Test
18. Minimal Runnable Example
19. Relation To Zhao--Cui And What Remains To Be Tested
Appendix A. Source And Code Anchors
Appendix B. Symbol Table And Array Shapes

## Required Proposition-Proof Blocks

P15 must include these proposition-proof blocks with enough intermediate
equations for a fresh reader:

1. **Affine-domain transformation.**  The transformed density
   \(\widetilde q_t(z)=q_t(\Psi_t(z))|\det J_{\Psi_t}|\) preserves integrals
   over the fixed hyperrectangle.
2. **Legendre mass matrix.**  The normalized Legendre basis has
   \(M_k=I\), and the formula for non-identity \(M_k\) is stated.
3. **Squared-TT mass contraction.**  The recursion for \(R_{t,k}\) equals
   \(\int\phi_t^2\) over the contracted suffix coordinates.
4. **Squared-TT marginalization.**  Replacing integrated square cores by mass
   contractions gives the marginal numerator over kept coordinates.
5. **Fixed-rank ridge ALS solve derivative.**  For each stored ALS update,
   \[
     N g=d,\qquad
     N\dot g=\dot d-\dot N g,
   \]
   with explicit formulas for \(\dot A,\dot y,\dot N,\dot d\).
6. **Normalized approximate filtering.**  The squared-TT plus defensive term
   yields a nonnegative normalized approximate filter for every time step with
   \(0<\widehat z_t<\infty\).
7. **Same-scalar gradient.**  The gradient algorithm differentiates exactly
   \[
     \widehat\ell_T^{\rm TT}(\alpha;B)
     =
     \sum_{t=1}^T\{\log(R_{t,0}(\alpha;B)+\tau_t)-c_t\}
   \]
   for the saved fixed branch \(B\), not the adaptive branch-changing code.

## Required Data Structures

The note and reference example must define these structures or their exact
equivalents:

- `DomainMap`: lower bounds, upper bounds, centers, half-widths, Jacobian log.
- `Basis1D`: degree, evaluation routine, mass matrix.
- `FitDesign`: points, weights, generation rule, seed/primes if used.
- `TTCore`: array shape `(r_left, p_k, r_right)`.
- `TTFunction`: ordered cores, basis list, evaluation routine.
- `SquaredTTDensity`: root TT, defensive mass, defensive density, shift,
  normalizer, square-core contraction environments.
- `FilterObject`: numerator representation, normalizer, evaluation routine,
  log-evaluation routine, derivative-evaluation routine.
- `BranchObject`: all frozen choices: ordering, domain maps, basis degrees,
  ranks, fitting points, weights, ridge, ALS sweep count, initialization, shift,
  defensive mass, signs/gauges if any, saved linear systems.
- `SensitivityObject`: derivatives of target values, cores, environments,
  normalizers, marginal numerator, and score contributions.

## Required Mapping To User's Missing-Implementation List

The implementability ledger must include a table with one row for each item:

- exact choice of domain maps / reference measure;
- exact basis families and how basis functions are evaluated;
- construction of mass matrices \(M_k\);
- how fitting points are selected;
- exact TT-cross / interpolation / least-squares core construction algorithm;
- rank selection or fixed-rank protocol;
- how \(\tau_t\) and \(\lambda_t\) are chosen;
- how \(c_t\) is computed and differentiated;
- how marginalization is performed in TT form;
- how conditional/KR maps are constructed if used;
- exact data structures for TT cores, contractions, saved branch objects;
- exact gradient recursion through every stored object;
- numerical stabilization and failure diagnostics;
- finite-difference test protocol;
- minimal runnable example.

Each row must record:

- P15 section;
- equation/proposition/pseudocode anchor;
- implementation status: `FULLY_SPECIFIED`, `OPTIONAL_NOT_USED`, or `BLOCKER`;
- remaining caveat if any.

No row may be left as `BLOCKER` if P15 is called successful.

## Minimal Runnable Example Requirement

The reference example must implement a small version of the declared algorithm,
not a different algorithm.  It should use:

- a scalar nonlinear state model or another explicitly declared low-dimensional
  SSM;
- fixed domain bounds;
- normalized Legendre basis;
- fixed deterministic fitting points;
- fixed ranks and ridge ALS sweeps;
- squared-TT normalizer;
- one-step or short-sequence approximate likelihood;
- analytical same-scalar gradient through the same stored branch, or a clearly
  scoped one-parameter one-step gradient if full sequence code is too large;
- finite-difference parity against the frozen branch.

The result ledger must state whether the runnable example passed, failed for
environmental reasons, or failed for algorithmic reasons.  A passing toy
example does not prove high-dimensional performance.  The example and result
ledger must state explicitly that the script is a reference/prototype artifact,
not a BayesFilter production implementation path, not a TensorFlow/TFP default,
and not evidence of production readiness.

## Required Finite-Difference Parity Protocol

The note, runnable example, and result ledger must use this exact protocol.

Scalar under test:
\[
  \widehat\ell_T^{\rm TT}(\alpha;B_0)
  =
  \sum_{t=1}^T
  \{\log(R_{t,0}(\alpha;B_0)+\tau_t)-c_t\}.
\]

Frozen under all perturbations:

- domain maps;
- basis degrees and recurrence;
- fitting points and weights;
- ranks;
- ALS initialization;
- ALS sweep count and order;
- ridge \(\rho\);
- \(\tau_t\);
- \(c_t\);
- vectorization order;
- branch signs/gauges;
- any stored old-coordinate integration pattern.

For each tested parameter coordinate \(i\), use centered differences
\[
  D_i(h)=
  \frac{
  \widehat\ell_T^{\rm TT}(\alpha_0+h e_i;B_0)
  -
  \widehat\ell_T^{\rm TT}(\alpha_0-h e_i;B_0)}
  {2h}.
\]
Use the step ladder
\[
  h\in\{10^{-3},10^{-4},10^{-5},10^{-6}\}\max(1,|\alpha_{0,i}|).
\]
Report
\[
  e_i(h)=
  \frac{|D_i(h)-\partial_i\widehat\ell_T^{\rm TT}(\alpha_0;B_0)|}
       {1+|D_i(h)|+|\partial_i\widehat\ell_T^{\rm TT}(\alpha_0;B_0)|}.
\]
For the minimal example, pass if
\[
  \min_h e_i(h)\le 10^{-4}
\]
for every tested coordinate and no branch object changes.  Stop and record an
algorithmic blocker if parity fails after checking obvious arithmetic or
conditioning mistakes.  The result ledger must also record the raw ladder
values, not only pass/fail.

## MathDevMCP Protocol

Use MathDevMCP only for narrow obligations:

- affine change-of-variables identity in scalar/product form;
- Legendre orthogonality or mass-matrix identity when feasible;
- log-normalizer derivative;
- squared-density normalizer derivative;
- linear solve derivative \(Ng=d\Rightarrow N\dot g=\dot d-\dot N g\);
- simple Kronecker square-core identity;
- normalized-density derivative.

Record statuses:

- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

Do not claim broad machine certification of TT filtering, ALS convergence, or
posterior accuracy.

## Source-Discipline Protocol

Main-text claims must be supported as:

- `PAPER_EXPLICIT`: checked Zhao--Cui or Cui--Dolgov technical section,
  equation, algorithm, proposition, or appendix;
- `PROJECT_DERIVATION`: derived in P15 or earlier P11--P14 notation;
- `IMPLEMENTATION_EVIDENCE`: observed in inspected companion-code path, used
  only to support code behavior;
- `DESIGN_CHOICE_FOR_P15`: a deliberate minimal fixed-branch specification not
  claimed to be exactly the adaptive companion implementation.

The source-support ledger must separate these classes.  P15 must not cite
abstracts, metadata, introductions, conclusions, citation counts, or venue
prestige as theorem or algorithm support.

Because this is literature-critical method work, P15 must also produce the
separate ledgers required by the scholarly audit policy:

- citation/venue metadata ledger, with dated metadata when available and
  `not available` rather than invented numbers when unavailable;
- backward-snowball ledger from the related-work/literature-survey sections of
  Zhao--Cui and Cui--Dolgov, classifying relevant references;
- forward-snowball ledger when metadata/network access is available, otherwise
  recording the access blocker;
- claim-support ledger mapping every important P15 claim to
  `PAPER_EXPLICIT`, `PROJECT_DERIVATION`, `IMPLEMENTATION_EVIDENCE`,
  `DESIGN_CHOICE_FOR_P15`, or `SOURCE_GAP_BLOCKER`;
- omitted-paper/reviewer-risk ledger for plausible missing TT filtering,
  transport, tensor approximation, and high-dimensional filtering competitors.

Before any paper-backed claim is accepted, the source-support ledger must
record publication status, local full-text status, inspected technical anchors,
and retraction/withdrawal/erratum/quarantine status.  Quarantined or
source-blocked papers cannot support theorem-level claims.

## Claude Review Loop

Claude Code is a bounded hostile reviewer only.  Codex is supervisor and final
authority.

Plan review command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p15-zhao-cui-tt-implementable-spec-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Execution review command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p15-zhao-cui-tt-implementable-spec-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile implementation-spec review prompt>"
```

Claude must output `ACCEPT` or `REJECT` first.

After each Claude review round, Codex must independently classify every Claude
finding:

- `ACCEPT`: materially correct; patch required.
- `PARTIAL`: directionally correct but needs a narrower or different patch.
- `DISPUTE`: incorrect, over-scoped, inconsistent with policy, or would weaken
  the document.
- `CLARIFY`: more evidence or human direction is needed.

For every accepted or partially accepted finding, Codex must patch the relevant
file and record the exact control added.  For every disputed finding, Codex
must write a concise rebuttal with file/section evidence and carry it into the
next Claude prompt.  Codex must not silently drop a finding.

The Claude ledger must maintain a finding register:

- round;
- finding ID;
- Claude finding summary;
- Codex classification;
- action taken;
- evidence path;
- status: `open`, `resolved`, `disputed`, or `carried_forward`.

If Codex and Claude still disagree after round 5, record the disagreement in
the discrepancy report and stop unless the human explicitly decides.

## Plan Review History

Plan review iteration 1:

- Claude status: `REJECT`.
- Codex audit: all six findings classified `ACCEPT`.
- Findings patched:
  1. add full scholarly-audit ledgers and retraction/quarantine gates;
  2. make next-filter storage, evaluation, log-evaluation, and derivative path
     concrete;
  3. freeze the primary basis, fitting design, weights, initialization, sweep
     order, vectorization order, and shift rule;
  4. specify finite-difference parity scalar, frozen branch objects, step
     ladder, error metric, threshold, and stop-on-failure rule;
  5. make \(\tau_t\) and \(c_t\) operationally unique;
  6. require the runnable example to be labeled reference-only and not
     production evidence.

Plan review iteration 2:

- Claude status: `ACCEPT`.
- Codex audit: `ACCEPT`; residual risks are execution-quality risks, not plan
  blockers.
- Residual risks to enforce during execution:
  1. sections 7, 9, 13, and 15 must not under-deliver;
  2. the declared method is narrower than adaptive Zhao--Cui;
  3. literature completeness must not be claimed merely from plan acceptance.

## Plan Review Prompt Requirements

The P15 plan-review prompt must ask Claude specifically:

1. Does this plan close the five P14 gaps, or does it still permit another
   readable-but-not-implementable note?
2. Does the chosen fixed-rank ridge-ALS variant make the value path and
   gradient path explicit enough to derive?
3. Are any of the user's missing-implementation-list items still optional when
   they should be required?
4. Does the plan honestly separate Zhao--Cui paper content from P15 design
   choices?
5. Are the review, MathDevMCP, validation, and stop conditions strong enough?
6. Would an educated chemistry/physics reader still be forced to read the
   original paper or background TT references to implement the declared method?

## Execution Validation Requirements

P15 execution must run:

```text
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-note-2026-05-31.tex
latexmk -cd -c docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-note-2026-05-31.tex
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-*
pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-implementable-fixed-branch-spec-note-2026-05-31.pdf - | rg -n "Fixed-Rank Ridge ALS|Mass Matrices|Marginalization In Squared-TT Form|Same-scalar gradient|Minimal Runnable Example"
python docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-fixed-branch-minimal-example-2026-05-31.py
```

Also check the final LaTeX log for undefined references/citations and rerun
blockers before cleanup.

## Skeptical Plan Audit

The main flaw in P14 is not a lack of prose.  It is that the central
implementation operation, "fit a square-root TT," remains too abstract.  A
reader could understand why a squared TT filter is normalized but still fail to
implement the algorithm.  P15 therefore must declare a particular domain,
basis, design, fitting algorithm, rank protocol, stabilizer, saved branch
object, and gradient path.

The plan deliberately chooses fixed-rank ridge ALS rather than adaptive
TT-cross because a full global derivative through adaptive rank, pivot, or
truncation choices would change branches.  This is not a demotion of
Zhao--Cui; it is a precise fixed-branch variant of the squared-TT filtering
idea suitable for a same-scalar analytical gradient.  The source ledger must
say which parts are paper-explicit and which parts are P15 design choices.

Claude plan-review iteration 1 found six material weaknesses.  Codex
classifies all six as `ACCEPT`:

1. The first draft did not require all six scholarly-audit ledgers.  This patch
   adds citation/venue metadata, backward snowball, forward snowball,
   claim-support, omitted-paper-risk, and explicit retraction/quarantine gates.
2. The next-filter object was still partly abstract.  This patch requires a
   concrete stored squared-core/environments representation, exact evaluation
   and log-evaluation formulas, and exact derivative evaluation.
3. The value path still allowed live alternatives.  This patch freezes the
   primary basis, design, weights, initialization, sweep order, vectorization
   order, and shift.
4. The finite-difference parity gate lacked exact tolerances and branch-freeze
   invariants.  This patch adds the scalar, step ladder, error metric,
   threshold, frozen objects, and stop-on-failure rule.
5. \(\tau_t\) and \(c_t\) were not operationally unique.  This patch sets a
   mandatory uniform defensive floor rule and mandatory frozen max-log shift.
6. The runnable example might be overread as production evidence.  This patch
   requires reference-only and no-production-readiness caveats.

The planned artifacts answer the user's question because the note is the
human-facing specification, the runnable example tests whether the
specification can be implemented, the missing-list ledger prevents silent
omissions, the gradient ledger tracks same-scalar differentiation through all
stored objects, the full scholarly ledgers prevent unsupported source drift,
the MathDevMCP ledger records narrow algebraic checks, and the Claude ledger
enforces hostile review with Codex-supervisor audit.

## Stop Conditions

Stop and report a blocker if:

- the plan or execution cannot make the TT fitting algorithm fully explicit;
- the gradient cannot be derived through the chosen fixed ALS path;
- the minimal example cannot be made to run or its failure is algorithmic and
  unresolved;
- any user's missing-list item remains `BLOCKER`;
- Claude identifies a major implementability, derivation, or source-support
  blocker that Codex accepts and cannot patch in scope;
- Codex and Claude disagree after five rounds;
- LaTeX validation fails after focused repair.

Decision:
`PLAN_READY_FOR_CLAUDE_REVIEW`
