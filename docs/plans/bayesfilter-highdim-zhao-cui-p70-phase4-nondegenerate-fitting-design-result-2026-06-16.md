# P70 Phase 4 Result: Nondegenerate Initialization And Fitting Design

metadata_date: 2026-06-16
status: PHASE4_PASSED_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 4
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded; MathDevMCP
diagnostic-only for short algebraic obligations

## Scope

Phase 4 designs the fitting rule \(\mathcal A_t\) used after the Phase 3
branch builder has fixed
\((\mu_t,L_t,\Omega_t,\mathcal D_t,c_t)\).  It does not edit algorithmic code,
does not edit p50, and does not run P69/P70 diagnostics.

The target of the fit remains the Zhao--Cui adjacent square-root target on the
frozen branch:
\[
  y_j(\beta)
  =
  \exp\left[-\frac12\{U_t(z_j;\beta)-c_t\}\right],
  \qquad
  z_j\in\operatorname{supp}\mathcal D_t .
\]
The UKF scout has already been confined by Phase 3 to branch construction.  It
is not used as a Gaussian surrogate target, rank oracle, correctness
certificate, or validation result.

## Skeptical Audit

The Phase 4 plan survives the skeptical audit with the following controls.

| Risk checked | Phase 4 control |
| --- | --- |
| Wrong baseline | Baseline is the current P59/P69 source-route fixed fit: constant-path initialization, one forward sweep, and post-fit diagnostics. |
| Proxy metric promoted to gate | In-sample residual is explanatory only.  Later admission requires structural channel activity, finite/bounded normalizers, holdout/replay predicates, condition-number predicates, and row adequacy. |
| Missing stop condition | Phase 5 blocks if the design cannot be implemented on the named surfaces or if focused tests cannot expose the predicates below. |
| Unfair comparison | No rank/degree ladder is run.  Later rank/degree comparison may compare admitted branches only. |
| Hidden assumption | Literal channel activity is tied to the stored gauge created by the fixed initialization and ALS schedule; it is not claimed to be gauge invariant. |
| Stale context | Phase 4 consumes Phase 1 fixed-branch contract, Phase 2 code gap audit, Phase 3 branch-builder design, p50 zero-environment and constant-path propositions, and P69 Phase 5c. |
| Environment mismatch | No GPU, HMC, network, package installation, or long diagnostic is required. |
| Artifact mismatch | The required artifacts are this design result and the Phase 5 subplan, not a repaired implementation. |

## Source And Claim Boundary

| Operation | Classification | Anchors | Consequence |
| --- | --- | --- | --- |
| Adjacent target fitted by \(\mathcal A_t\) | `source_faithful` mathematical route component | Zhao--Cui Eqs. (9)--(11), Algorithm 1/Eq. (12); author route `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43`, `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:84-124` | The fitted values are still the adjacent filtering target, not a UKF surrogate. |
| Squared square-root density and normalizer | `source_faithful` mathematical route component | Zhao--Cui Eq. (13), Algorithm 2, Proposition 2/Eq. (14), Eqs. (15)--(16); author TTSIRT/marginalization anchors listed in Phase 1 | The density remains \(\phi_t^2+\tau_t\lambda_t\) with squared-TT marginalization. |
| Constant-path initialization as current baseline | current fixed-branch baseline, not enough for P70 rank-capacity evidence | p50 Proposition `prop:p50-constant-path-initialization`; `source_route.py:3606-3628`; P69 Phase 5c | Positive constant mass is preserved as a baseline component, but it is not sufficient for declared-channel activity. |
| Nondegenerate seeded-channel initialization, alternating sweeps, channel-activity gates, row-adequacy gates | `fixed_hmc_adaptation` | p50 fixed-branch definition and zero-environment proposition; current fitter surfaces `fitting.py:25-79`, `fitting.py:223-291`, `fitting.py:573-646` | These are deterministic fixed-branch admissibility rules.  They are not adaptive Zhao--Cui parity. |

## Fitting-Space Contract

Let \(D=2m\) be the adjacent target dimension for the current author-SIR lane.
For a polynomial degree \(p\) and declared rank \(R\), use the tensor-product
basis already used by the source route:
\[
  \psi_k(z_k)=(\psi_{k,0}(z_k),\ldots,\psi_{k,p}(z_k)),
  \qquad
  \psi_{k,0}\equiv 1,
  \qquad
  \Omega_t=[-1,1]^D .
\]
The rank tuple is
\[
  (1,R,\ldots,R,1).
\]
The P70 default diagnostic branch is
\[
  p=1,\qquad R=2.
\]
Higher degree or rank may be run only in a later phase after the same
admissibility predicates are frozen.  Degree \(p=2\) remains blocked from
validation because P69 Phase 5c observed normalizer, holdout, and replay
instability despite improved in-sample residuals.

## Numerical Gate Provenance

All numerical thresholds introduced in Phase 4 are BayesFilter engineering
safeguards for the fixed-HMC adaptation.  They are predeclared before Phase 5
implementation and before Phase 6 repaired diagnostics.  They are not
Zhao--Cui source-faithful theory, not posterior correctness evidence, not rank
truth, and not validation evidence by themselves.

| Threshold family | Values | Role | What it cannot prove |
| --- | --- | --- | --- |
| Seed size | \(\varepsilon_{\rm init}=10^{-6}\) | Gives extra channels a nonzero initial path while keeping the constant path dominant. | Does not prove the final fit uses extra channels. |
| Row adequacy | \(n_{\rm hard},n_{\rm preferred}\) below | Blocks obviously underdetermined fits and labels small-row fits diagnostic-only. | Does not prove sample coverage or convergence. |
| Ridge/conditioning | \(\rho=10^{-10}\), \(\kappa_{\rm warn}=10^{10}\), \(\kappa_{\rm veto}=10^{14}\) | Prevents nonfinite or severely ill-conditioned least-squares updates from being admitted. | Does not prove the approximation is accurate. |
| Channel activity | \(10^{-12}\), \(10^{-8}\), \(b_{\min}\) below | Rejects stored TT fits whose declared extra channels are effectively unused in the fixed gauge. | Does not prove gauge-invariant rank necessity. |
| Normalizer | \(10^{-14}\), \(10^{-6}\), \(|F_t^B|\le10^6\) | Rejects defensive-only, nonfinite, or extreme evidence-scale branches. | Does not validate the filtering likelihood. |
| Holdout/replay | normalized residual at most \(10\) | Rejects catastrophic off-training behavior in Phase 6. | Does not establish correctness or HMC readiness. |

P69 Phase 5c motivated the need for these safeguards by exposing rank-channel
collapse and degree-normalizer instability.  It did not tune the values by
running the P70 repaired algorithm, because that algorithm does not yet exist.

## Nondegenerate Initialization

Let \(C_1,\ldots,C_D\) be the initial tensor-train cores, with
\[
  C_k\in\mathbb R^{R_{k-1}\times(p+1)\times R_k},
  \qquad
  R_0=R_D=1,\quad R_1=\cdots=R_{D-1}=R.
\]
Let
\[
  \bar y=
  \frac{\sum_j w_j y_j}{\sum_j w_j},
  \qquad
  a_0=\max\{\bar y,10^{-300}\}.
\]
The constant channel is preserved:
\[
  C_1[0,0,0]=a_0,\qquad
  C_k[0,0,0]=1\quad(k=2,\ldots,D).
\]
For every extra channel \(a=1,\ldots,R-1\), insert a small deterministic path.
Let
\[
  \varepsilon_{\rm init}=10^{-6},\qquad
  b_a=\frac{\varepsilon_{\rm init}a_0}{R-1}\quad(R>1),
\]
and define the seeded basis index
\[
  \nu(k,a)=
  \begin{cases}
    1+((k+a-2)\bmod p), & p\ge 1,\\
    0, & p=0 .
  \end{cases}
\]
For \(R>1\), set
\[
  C_1[0,\nu(1,a),a]=b_a,
  \qquad
  C_k[a,\nu(k,a),a]=1\quad(2\le k\le D-1),
  \qquad
  C_D[a,\nu(D,a),0]=1 .
\]
All other entries are zero.  The initialization rule name is:

`fixed_hmc_seeded_channel_paths_v1`

The seeded channel paths are small relative to the positive constant path.
They are not a new scientific target.  Their purpose is to prevent the
zero-environment mechanism in p50 Proposition
`prop:p50-zero-environment-cascade` from making nonfirst declared channels
unavailable before ALS has a chance to update them.

### Proposition 1: Nonzero Environments For Seeded Channels

Assume \(p\ge1\), \(R>1\), \(a_0>0\), and
\(\varepsilon_{\rm init}>0\).  For each extra channel
\(a=1,\ldots,R-1\), the initial tensor train contains a nonzero path through
channel \(a\).  Consequently, before any ALS update, every core on that path
has nonzero left and right environments as a polynomial function on
\(\Omega_t\).

#### Proof

For fixed \(a\), the scalar
\[
  b_a=\frac{\varepsilon_{\rm init}a_0}{R-1}
\]
is strictly positive because \(\varepsilon_{\rm init}>0\), \(a_0>0\), and
\(R-1>0\).  The stored entries
\[
  C_1[0,\nu(1,a),a],\quad
  C_k[a,\nu(k,a),a]\ (2\le k\le D-1),\quad
  C_D[a,\nu(D,a),0]
\]
are therefore all nonzero.  Consider the internal channel sequence
\[
  0\to a\to a\to\cdots\to a\to 0 .
\]
The tensor-train expansion is a sum over all internal channel sequences.  The
coefficient associated with this particular sequence is nonzero, and its basis
product is
\[
  b_a\prod_{k=1}^{D}\psi_{k,\nu(k,a)}(z_k).
\]
Each normalized Legendre basis function is a nonzero polynomial on
\([-1,1]\).  A product of nonzero polynomials in separate variables is not the
zero polynomial on the product domain.  Hence this channel sequence contributes
a nonzero polynomial path to the initial tensor train.

For an ALS update of any core \(k\) on this path, the left environment contains
the product of the nonzero stored coefficients and basis factors from cores
\(1,\ldots,k-1\), while the right environment contains the analogous product
from cores \(k+1,\ldots,D\).  The same nonzero-polynomial argument shows that
neither environment is identically zero.  Thus the initial design matrices for
the seeded channel are not forced to zero by construction.  This proves only
an opportunity for activation; it does not prove that the final fitted branch
will use the channel.

For \(p=0\), the same rule uses constant extra-channel paths.  That case can
exercise rank channels but cannot exercise nonconstant basis directions; it is
allowed only as a shape/replay smoke case, not as a P70 rank-capacity
diagnostic.

## Sweep Policy And Replay Identity

The P70 fitting rule uses the deterministic canonical alternating ALS update
schedule:
\[
  \mathcal O
  =
  (1,2,\ldots,D,D,D-1,\ldots,1)
\]
in one-based mathematical notation, implemented as
\[
  (0,1,\ldots,D-1,D-1,\ldots,0).
\]
The fixed fit uses
\[
  n_{\rm sweeps}=4
\]
full passes over this order.  There is no early stop based on in-sample
residual improvement in P70 Phase 5/6.  The only early terminations are
predeclared fitter status vetoes: nonfinite values, complexity gate,
condition-number veto, or holdout residual veto when holdout is passed into the
generic fitter.

Current `FixedTTFitter` validation accepts only a permutation of the coordinate
axes as `sweep_order`.  Therefore Phase 5 is explicitly authorized to update
`fitting.py` validation with this exact rule:

- a schedule is valid if every entry is an integer in \(\{0,\ldots,D-1\}\);
- every axis must appear at least once;
- legacy permutation schedules of length \(D\) remain valid;
- the P70 repeated-axis schedule is exactly
  \((0,1,\ldots,D-1,D-1,\ldots,0)\), of length \(2D\);
- arbitrary extra repeats are not admitted by the P70 design;
- schedules with a missing axis, an out-of-range axis, an empty tuple, or a
  repeated-axis pattern different from the canonical alternating P70 pattern
  are invalid for Phase 5.

The canonical schedule includes one consecutive duplicate at the turning point
\((D-1,D-1)\).  That duplicate is intentional: it updates the last core at the
end of the forward pass and again at the start of the reverse pass.  The full
schedule must be recorded in the branch identity and preserved through
manifest round-trips.  This is an implementation-support change for the
fixed-HMC adaptation, not a scientific change to the fitted target.

The branch identity must include:

- initialization rule and \(\varepsilon_{\rm init}\);
- sweep order and sweep count;
- rank tuple, degree, ridge, dtype, and condition thresholds;
- design row hash and weight hash;
- target-value hash at the evaluated \(\beta\);
- branch-builder manifest hash from Phase 3;
- channel-activity thresholds below.

Replaying the same fixed branch with the same \(\beta\), data, design rows,
weights, initialization rule, and sweep policy must reproduce the same branch
hash and fitted values.  Recomputing the UKF branch builder or changing any of
those objects is a different branch.

## Row Adequacy

Let
\[
  n=|\operatorname{supp}\mathcal D_t|
\]
be the number of weighted raw pushed rows admitted by the Phase 3 coverage
gate.  Let
\[
  c_{\max}=(p+1)R^2
\]
be the largest number of coefficients in an interior core update.  Define
\[
  n_{\rm hard}=\max\{4,\lceil D/4\rceil,c_{\max}\},
  \qquad
  n_{\rm preferred}=\max\{D,2c_{\max}\}.
\]
The branch blocks before fitting if \(n<n_{\rm hard}\) with status
`branch_fit_row_adequacy_failed`.  If
\[
  n_{\rm hard}\le n<n_{\rm preferred},
\]
the branch may be run only as a bounded diagnostic.  It cannot be used to
promote rank, promote degree, launch d18 validation, or claim HMC readiness.
If \(n\ge n_{\rm preferred}\), row adequacy does not by itself admit the
branch; it only removes the row-count veto.

Weights must be finite, nonnegative, and have strictly positive total mass
after Phase 3 in-domain renormalization.  The weighted effective sample size
\[
  E_{\rm fit}=\frac{1}{\sum_j w_j^2}
\]
is explanatory in Phase 6 unless a later reviewed subplan freezes a stricter
ESS veto before observing repaired output.

## Ridge And Condition-Number Policy

The ridge is fixed at
\[
  \rho=10^{-10}.
\]
The condition-number warning and veto thresholds are
\[
  \kappa_{\rm warn}=10^{10},\qquad
  \kappa_{\rm veto}=10^{14}.
\]
For every core update, if the normal-equation condition number is nonfinite or
exceeds \(\kappa_{\rm veto}\), the branch blocks as
`condition_number_veto`.  If it exceeds \(\kappa_{\rm warn}\) but not
\(\kappa_{\rm veto}\), the branch may continue, but the warning must be
recorded.  A branch with any warning cannot be promoted by a rank/degree ladder
unless Phase 7 explicitly records that the warning is explanatory and all
primary admissibility gates pass.

These thresholds are frozen before Phase 5 implementation and before any
repaired diagnostic output is observed.

## Channel-Activity Predicate

The predicate is defined on the stored TT cores in the deterministic gauge
created by the initialization and ALS schedule above.  It is not claimed to be
gauge invariant.

For an internal bond \(k=1,\ldots,D-1\) and a channel
\(a=0,\ldots,R_k-1\), define the incident-channel score
\[
  A_{k,a}
  =
  \|C_k[:,:,a]\|_F\,\|C_{k+1}[a,:,:]\|_F .
\]
Let
\[
  A_{\rm ref}=\max\{A_{k,0}:1\le k\le D-1\},
  \qquad
  \epsilon_{\rm chan,abs}=10^{-12},
  \qquad
  \epsilon_{\rm chan,rel}=10^{-8}.
\]
The channel \(a\) is active at bond \(k\) if
\[
  A_{k,a}\ge
  \max\{\epsilon_{\rm chan,abs},\epsilon_{\rm chan,rel}A_{\rm ref}\}.
\]
If \(A_{\rm ref}\) is nonfinite or nonpositive, the channel-activity predicate
fails before inspecting extra channels.
The fitted branch passes the structural channel gate for rank \(R\) only if
each extra channel \(a=1,\ldots,R-1\) is active on at least
\[
  b_{\min}=\max\{1,\lceil 0.25(D-1)\rceil\}
\]
internal bonds.  Otherwise the branch status is
`rank_channel_activity_failed`.

A branch that fails this predicate may still be useful as a debugging artifact,
but it cannot be used as evidence that higher rank is unnecessary or that a
rank ladder has converged.

## Normalizer Predicates

Let
\[
  S_t=\int_{\Omega_t}\phi_t(z)^2\,d\lambda_t(z),
  \qquad
  Z_t^{\rm sh}=S_t+\tau_t,
  \qquad
  F_t^B=\log Z_t^{\rm sh}-c_t .
\]
The defensive-only tolerance is
\[
  \epsilon_{\rm def}=10^{-14}.
\]
The branch passes the normalizer gate only if:

1. \(S_t,Z_t^{\rm sh},c_t,F_t^B\) are finite;
2. \(S_t>\epsilon_{\rm def}\);
3. \(Z_t^{\rm sh}>0\);
4. the fitted square-root mass fraction
   \[
      \frac{S_t}{S_t+\tau_t}
   \]
   is at least
   \[
      \rho_{\rm fitmass}=10^{-6};
   \]
5. \(|F_t^B|\le 10^6\) for bounded diagnostics.

Failure of item 1, 2, 3, or 4 is a branch-admissibility veto.  Failure of item
5 blocks validation and ladder promotion; it may still be recorded as a
bounded diagnostic if the Phase 6 subplan explicitly labels it as a failed
branch rather than a passed branch.

## Holdout And Replay Predicates

Holdout and replay rows must be frozen before evaluating residuals.

For Phase 5 focused unit tests, holdout may use small synthetic fixtures and
the generic fitter's built-in holdout veto.

For Phase 6 repaired source-route diagnostics, holdout and replay residuals
are post-fit diagnostics on the same frozen branch.  Let
\[
  r_{\rm fit},\quad r_{\rm hold},\quad r_{\rm replay}
\]
be weighted root-mean-square residuals for fit, holdout, and replay rows,
respectively, on the shifted square-root target scale.  Define the target RMS
on a diagnostic row set \(H\) by
\[
  s_H=\left(\sum_{j\in H}w_j y_j^2\right)^{1/2}.
\]
The normalized residual is \(r_H/\max\{s_H,10^{-300}\}\).

The Phase 6 source-route branch passes the holdout/replay gate only if:

- holdout and replay row sets both exist and are disjoint from the training
  row identity set;
- all target values and residuals are finite;
- normalized holdout residual is at most \(10\);
- normalized replay residual is at most \(10\).

These are loose veto thresholds, not proof of correctness.  They are chosen to
reject catastrophic off-training behavior like the P69 Phase 5c degree-2
instability while avoiding a false claim that a small holdout residual validates
the filter.

## Later Rank/Degree Interpretation

Phase 6 may say a repaired branch is structurally admissible only if row
adequacy, condition-number, channel-activity, normalizer, holdout, and replay
gates all pass.  Phase 7 may compare ranks or degrees only among branches that
pass those gates.

In-sample residual can explain why a branch is interesting, but it cannot:

- admit a branch after channel or normalizer failure;
- select a degree after holdout/replay failure;
- justify d18 validation;
- support HMC readiness;
- support a claim that Zhao--Cui's adaptive method fails.

## Phase 5 Implementation Surface

Phase 5 may edit only these BayesFilter-owned implementation surfaces unless a
new reviewed blocker explicitly expands the scope:

- `bayesfilter/highdim/source_route.py`;
- `bayesfilter/highdim/fitting.py` for repeated-axis update-schedule
  validation and manifest/diagnostic payload support;
- `bayesfilter/highdim/__init__.py` only if a new helper must be public;
- `tests/highdim/test_fixed_branch_fit.py`;
- a new focused test file under `tests/highdim/` for P70 source-route fitting
  design, if needed.

Phase 5 must not edit p50, run P69 Phase 5c, run repaired diagnostics, run
validation ladders, run GPU/HMC commands, or change default rank/degree policy
outside the P70 route.

## Required Phase 5 Tests

Phase 5 must add or update focused tests that establish:

1. the seeded-channel initializer preserves the positive constant path and
   inserts nonzero extra-channel paths for \(R>1\);
2. initial extra-channel incident scores are nonzero under the P70 stored
   gauge;
3. P70 fit configuration uses alternating sweep order and
   \(n_{\rm sweeps}=4\);
4. the generic fitter accepts repeated-axis update schedules whose visited-axis
   set is exactly the full coordinate set, while still rejecting schedules that
   omit an axis or contain an out-of-range axis;
5. branch identity or diagnostics record initialization rule, sweep policy,
   channel thresholds, row-adequacy thresholds, ridge, and condition thresholds;
6. row-adequacy failure blocks fitting below \(n_{\rm hard}\);
7. channel-activity predicate fails an all-constant-path rank-2 core tuple;
8. normalizer predicate fails a defensive-only or nonfinite branch summary;
9. deterministic replay produces the same branch hash for the same fixed
   inputs and changes the branch hash when initialization rule or sweep order
   changes;
10. the old one-sweep constant-path route remains available only as historical
   baseline or explicitly named legacy behavior, not as the P70 default.

Focused tests may use small synthetic TensorFlow fixtures.  They must not run
the long P69 Phase 5c diagnostic or any d18 validation ladder.

## Forbidden Shortcuts

- Do not simulate channel activity by changing only diagnostics while leaving
  the fitted cores on the constant path.
- Do not clip Phase 3 source rows into the local cube.
- Do not double-count source weights through both row multiplicity and
  explicit weights.
- Do not tune thresholds after seeing repaired diagnostic output.
- Do not use low/high branch closeness as an admissibility gate.
- Do not call the seeded initializer source-faithful.
- Do not promote degree 2 on in-sample residual improvement alone.
- Do not use UKF moments as target values for the TT fit.

## Phase 5 Handoff

Phase 5 may begin only after this Phase 4 result and the refreshed Phase 5
subplan receive Claude `VERDICT: AGREE`.  The exact inherited products are:

- initialization rule `fixed_hmc_seeded_channel_paths_v1`;
- \(\varepsilon_{\rm init}=10^{-6}\);
- alternating sweep order `(0, 1, ..., D-1, D-1, ..., 0)`;
- `max_sweeps=4`;
- row thresholds \(n_{\rm hard}\) and \(n_{\rm preferred}\);
- ridge and condition thresholds \(\rho=10^{-10}\),
  \(\kappa_{\rm warn}=10^{10}\), \(\kappa_{\rm veto}=10^{14}\);
- channel thresholds \(\epsilon_{\rm chan,abs}=10^{-12}\),
  \(\epsilon_{\rm chan,rel}=10^{-8}\), and
  \(b_{\min}=\max\{1,\lceil0.25(D-1)\rceil\}\);
- normalizer thresholds \(\epsilon_{\rm def}=10^{-14}\),
  \(\rho_{\rm fitmass}=10^{-6}\), and \(|F_t^B|\le10^6\);
- holdout/replay normalized residual veto \(10\);
- exact implementation and test surfaces listed above.

## Not Concluded

- No implementation has been changed.
- No p50 prose has been edited.
- No repaired diagnostic or validation ladder has been run.
- No claim is made that the repair fixes the bug.
- No UKF correctness, adaptive Zhao--Cui parity, d18 validation, scaling,
  HMC readiness, or author-code failure claim is made.
