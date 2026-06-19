# P70 Phase 1 Result: Mathematical Fixed-Branch Contract

metadata_date: 2026-06-16
status: PHASE1_PASSED_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 1
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded; MathDevMCP for derivation checks

## Decision

Phase 1 records the mathematical contract that P70 must implement before any
repair code or diagnostic run.  No algorithmic code was changed.  The p50
chapter was not edited in this phase because its fixed-branch propositions
already contain the needed base results; this artifact binds those results into
the P70 UKF-guided fixed-branch contract and assigns the next code-audit
handoff to Phase 2.

## Paper And Source Anchors

Author-source anchors in this table are relative to
`third_party/audit/zhao_cui_tensor_ssm_p10/source/`.

| Claim | Paper anchor | Author-source anchor | P70 class |
| --- | --- | --- | --- |
| Sequential filtering target is built from adjacent states and old-state marginalization. | Zhao--Cui Eqs. (9)--(11); P18 BF-9--BF-11 | `models/full_sol.m:21-43`, `models/full_sol.m:72-80`, `models/full_sol.m:132-135` | `source_faithful` route component |
| Square-root approximation is squared and combined with defensive mass. | Zhao--Cui Eq. (13), Algorithm 2; P18 S1--S3 | `deep-tensor.dev/src/@TTSIRT/TTSIRT.m:185-188`, `deep-tensor.dev/src/@TTSIRT/marginalise.m:81-85` | `source_faithful` density form |
| Squared-TT marginalization and normalizer contractions determine retained densities. | Zhao--Cui Proposition 2/Eq. (14); P18 M1--M9 | `deep-tensor.dev/src/@TTSIRT/marginalise.m:26-51`, `deep-tensor.dev/src/@TTSIRT/marginalise.m:54-85`; `deep-tensor.dev/src/@TTSIRT/eval_potential_reference.m:12-33` | `source_faithful` route component |
| Conditional KR maps are built from fitted density marginals. | Zhao--Cui Eqs. (17)--(20), Proposition 4; P18 K1--K8 | `deep-tensor.dev/src/@TTSIRT/eval_irt_reference.m:16-42`, `deep-tensor.dev/src/@TTSIRT/eval_irt_reference.m:73-180`; `deep-tensor.dev/src/@TTSIRT/eval_cirt_reference.m:43-100`, `deep-tensor.dev/src/@TTSIRT/eval_cirt_reference.m:101-154`; `deep-tensor.dev/src/@TTSIRT/eval_rt_reference.m:13-56`; `deep-tensor.dev/src/@TTSIRT/eval_rt_jac_reference.m:17-113`, `deep-tensor.dev/src/@TTSIRT/eval_rt_jac_reference.m:115-180` | `source_faithful` route component |
| Author SIR source row uses propagated samples, local coordinates, TTSIRT, and log-normalizer recursion. | Paper anchor pending for the specific benchmark row; Algorithm 2 supplies only the general squared-TT route context. | `eg3_sir/mainscript.m:14-17`, `eg3_sir/mainscript.m:39-56`; `models/full_sol.m:49-124`; `models/computeL.m:24-47` | author-source benchmark anchor; not promoted to `source_faithful` until Phase 2 or later cites the exact paper benchmark anchor |
| UKF-guided branch construction. | Not a Zhao--Cui paper operation; p50 UKF scout section only. | No Zhao--Cui author-source UKF route. | `fixed_hmc_adaptation` |

No operation newly introduced in P70 may be called `source_faithful` unless it
has both a Zhao--Cui paper anchor and an author-source anchor.  The
UKF-guided branch builder remains `fixed_hmc_adaptation`.

## Base Mathematical Objects

For one filtering time \(t\), let the fixed branch be
\[
    B_t=
    \{\mathcal D_t,T_t,\Omega_t,c_t,\mathcal V_t,\mathcal R_t,\mathcal A_t,
      \lambda_t,\tau_t,\eta_t\},
\]
as in p50 Definition \(\ref{def:p50-fixed-branch}\).  Here
\(\mathcal D_t=\sum_{j=1}^{m_t}w_j\delta_{z_j}\) is the frozen design measure,
\(T_t(z)=\mu_t+L_tz\) is the frozen affine coordinate map, \(\Omega_t\) is the
local domain, \(c_t\) is the frozen log-scale shift, \(\mathcal V_t\) and
\(\mathcal R_t\) define the tensor-train approximation space and rank tuple,
\(\mathcal A_t\) is the deterministic fitting rule, \(\lambda_t\) is the
reference density, \(\tau_t>0\) is the shifted-scale defensive mass, and
\(\eta_t\) is the admissibility record.

Let \(\beta\) be the external model parameter at which the approximate
likelihood is evaluated.  For a fixed branch \(B_t\), the design measure,
affine coordinate map, approximation space, ranks, fitting rule, reference
density, defensive mass, and log-scale shift are held fixed while the target
values supplied to the fitting rule may vary with \(\beta\).  Let
\(q_t^{\rm phys}(r;\beta)\) be the unnormalized physical target and
\(\ell_t(r;\beta)=-\log q_t^{\rm phys}(r;\beta)\).  The local shifted target is
\[
    U_t^B(z;\beta)=\ell_t(\mu_t+L_tz;\beta)-\log|\det L_t|,
    \qquad
    s_t^{B,{\rm sh}}(z;\beta)=\exp\{-(U_t^B(z;\beta)-c_t)/2\}.
\]
The deterministic fit \(\mathcal A_t\) returns a stored tensor-train
representation
\[
    \phi_t^B(\cdot;\beta)
    =
    \mathcal A_t\bigl(s_t^{B,{\rm sh}},\mathcal D_t,\mathcal V_t,\mathcal R_t\bigr).
\]
The shifted fixed-branch density and normalizer are
\[
    q_t^{B,{\rm sh}}(z;\beta)=\phi_t^B(z;\beta)^2+\tau_t\lambda_t(z),
    \qquad
    \zeta_t^B(\beta)=\int_{\Omega_t} q_t^{B,{\rm sh}}(z;\beta)\,dz.
\]
The original-scale evidence increment, and hence the scalar to be
differentiated by the fixed-branch likelihood, is
\[
    F_t^B(\beta)=\log\overline Z_t^B(\beta)
    =\log\zeta_t^B(\beta)-c_t.
\]
These equations are the p50 fixed-branch scalar, grounded in Zhao--Cui
Eq. (13), Algorithm 2, and Proposition 2 for the density and marginalization
form, but with the adaptive choices conditioned on rather than reselected.

## Proposition 1: Fixed Scalar And Normalized Retained Density

Fix \(B_t\) and \(\beta\).  Suppose \(L_t\) is nonsingular, \(\mathcal D_t\)
has finite positive mass, \(s_t^{B,{\rm sh}}(\cdot;\beta)\) is finite at the
design points, the deterministic fit returns finite
\(\phi_t^B(\cdot;\beta)\in L^2(\Omega_t)\), \(\lambda_t\) is a probability
density on \(\Omega_t\), and \(\tau_t>0\).  Then
\(q_t^{B,{\rm sh}}(\cdot;\beta)\ge0\),
\(0<\zeta_t^B(\beta)<\infty\), and the retained density obtained by
marginalizing
\[
    q_t^{B,{\rm sh}}(\cdot;\beta)/\zeta_t^B(\beta)
\]
is normalized.  Consequently \(F_t^B(\beta)=\log\zeta_t^B(\beta)-c_t\) is a
well-defined fixed-branch scalar.

### Proof

This is p50 Proposition \(\ref{prop:p50-fixed-square-root-normalized}\) and
Proposition \(\ref{prop:p50-fixed-adaptive-relation}\).  Since
\(\phi_t^B(\cdot;\beta)^2\ge0\), \(\tau_t>0\), \(\lambda_t\ge0\), and
\(\int_{\Omega_t}\lambda_t=1\),
\[
    \zeta_t^B(\beta)
    =
    \int_{\Omega_t}\phi_t^B(z;\beta)^2\,dz+\tau_t
    >
    0.
\]
The \(L^2\) assumption gives finiteness.  Normalization and marginalization
then follow from Tonelli's theorem.  The adaptive objects
\(\mathcal D_t,T_t,c_t,\mathcal V_t,\mathcal R_t,\mathcal A_t\) are entries of
\(B_t\).  Thus later differentiation, if the deterministic fitting map and
dominated-differentiation assumptions are supplied, is differentiation of
\(F_t^B(\beta)\) with \(B_t\) held fixed, not differentiation through the
adaptive mechanism that selected \(B_t\).  This proves the normalization and
fixed-scalar claim.

## Proposition 2: UKF-Guided Frozen Branch

Let a deterministic scout map \(G_t\) take the UKF summaries
\((m_{t|t},P_{t|t})\), fixed hyperparameters, and fixed random seeds or design
identities, and return
\[
    G_t(m_{t|t},P_{t|t})
    =
    (\mu_t,L_t,\Omega_t,\mathcal D_t,c_t).
\]
Assume \(G_t\) returns finite \(\mu_t\), nonsingular \(L_t\), a measurable local
domain \(\Omega_t\), a finite positive design measure \(\mathcal D_t\), and a
finite shift \(c_t\).  Once these objects are recorded inside \(B_t\), the
resulting scalar is a fixed branch in the sense of Proposition 1.  The UKF
summaries are scout evidence only; they do not certify the fixed-branch
likelihood, the approximation rank, d18 correctness, or HMC readiness.

### Proof

The output of \(G_t\) supplies entries of \(B_t\).  If those entries satisfy the
regularity assumptions in Proposition 1 and remain unchanged during the
likelihood evaluation or same-branch derivative check, the scalar is fixed.
The proof uses only determinism and finiteness of the branch objects.  It does
not use any statement that the UKF posterior approximation is exact or that it
is a Zhao--Cui adaptive step.  Therefore this construction is a
`fixed_hmc_adaptation`, not a `source_faithful` Zhao--Cui operation.

## Proposition 3: Constant-Path Reconciliation

The p50 constant-path initialization guarantees a nonzero initial square-root
mass when \(y_j>0\) and \(w_j>0\), but it does not guarantee that the declared
higher-rank channels are active in the realized fitted tensor train.  In a
stored tensor-train representation with internal rank tuple
\((1,R_1,\ldots,R_{D-1},1)\), the p50 initialization uses only the first
internal channel and the constant basis channel.  Therefore a P70 admitted
branch needs a separate channel-activity diagnostic if rank-capacity evidence
is to be interpreted.

### Proof

p50 Proposition \(\ref{prop:p50-constant-path-initialization}\) sets
\(C_1[1,0,1]=\bar y_t\) and \(C_k[1,0,1]=1\) for \(k\ge2\), with all other
entries zero.  Its proof shows that the represented function is the constant
\(\bar y_t\), so the initial squared mass is \(\bar y_t^2>0\).  The same proof
also states that only the first rank channel and the constant basis channel
are nonzero.  Positive mass on that channel therefore does not imply nonzero
entries, nonzero environments, or nonzero contribution from the other declared
channels.  p50 Proposition \(\ref{prop:p50-zero-environment-cascade}\) explains
why zero environments can persist through a frozen ALS update.  Hence P70 must
test channel activity separately from total fitted mass.

## Channel-Activity Predicate

Channel activity is a diagnostic on the frozen stored representation, not a
gauge-invariant theorem about the represented function.  P70 must freeze the
storage convention or gauge convention before applying this predicate.

For a stored core tuple \(C_1,\ldots,C_D\), define the bond-channel activity
score for internal bond \(k\) and channel \(a\in\{1,\ldots,R_k\}\) by
\[
    A_{k,a}(C)
    =
    \|C_k[:,:,a]\|_F\,\|C_{k+1}[a,:,:]\|_F.
\]
A declared channel is active only if its score exceeds a threshold frozen
before the diagnostic run.  A rank ladder cannot use a higher-rank branch as
rank-capacity evidence if all extra declared channels fail this activity
predicate, even if the total fitted mass is nonzero.

This predicate is `fixed_hmc_adaptation`: it is an admissibility diagnostic for
the stored fixed branch.  It is not claimed to be part of the adaptive
Zhao--Cui algorithm.

## Normalizer, Holdout, And Replay Predicates

P70 separates four diagnostic ledgers:

| Predicate | Mathematical role | Threshold provenance |
| --- | --- | --- |
| fitted square-root mass \(S_t=\int\phi_t^2\) | rejects defensive-only fitted branches | numerical tolerance declared before any mass-based diagnostic is run |
| shifted normalizer \(\zeta_t^B=S_t+\tau_t\) and log increment \(\log\zeta_t^B-c_t\) | requires finite evidence-scale density | finite/bounded checks declared before any normalizer diagnostic is run |
| holdout residual on frozen holdout design | tests fit behavior away from training rows | holdout set and tolerance declared before holdout evaluation |
| replay residual on frozen replay rows | tests branch replay consistency | replay rows and tolerance declared before replay evaluation |
| rank/degree ladder deltas | compares admitted branches only | ladder criteria declared before branch comparison |

In-sample residual improvement alone is explanatory only.  It cannot admit a
branch, select a degree, launch d18 validation, or support HMC readiness if a
veto diagnostic fails.

## Boundary For Later Diagnostics

This contract defines mathematical predicates and their roles.  It does not
run a diagnostic, assign numerical tolerances, or approve any empirical ladder.
Any later execution must state its own evidence contract before observing the
corresponding diagnostic output.

## Implementation Surfaces For Phase 2 Audit

Phase 2 should audit at least:

- `bayesfilter/highdim/source_route.py:3212-3248` for current one-sweep fixed
  fit configuration;
- `bayesfilter/highdim/source_route.py:3606-3628` for constant-path initial
  cores;
- `bayesfilter/highdim/fitting.py:223-236` for the fixed ALS sweep loop;
- `bayesfilter/highdim/ukf_scout.py:13-22` for UKF nonclaims;
- `bayesfilter/highdim/rank_budget.py:330-365` for UKF rank-policy limits;
- tests covering P57/P59/P66/P69 current behavior and any existing
  holdout/replay diagnostics.

Phase 2 must not implement repairs.  Its result should map every required
mathematical object above to a current code surface, a missing surface, or a
blocked/source-ungrounded surface.

## Phase 2 Handoff

Phase 2 may start only after Claude review agrees that this mathematical
contract is coherent and that the Phase 2 subplan consumes it exactly.  Phase 2
must produce a current-code gap audit, not an implementation repair.

## Not Concluded

- No algorithmic code was changed.
- p50 was not edited.
- No diagnostic or ladder was run.
- No threshold value was frozen after seeing repaired diagnostic output.
- No UKF correctness, d18 validation, d50/d100 scaling, HMC readiness,
  adaptive parity, or author-code failure claim is made.
