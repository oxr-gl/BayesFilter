# P19 Zhao--Cui Finite-Difference Ledger

metadata_date: 2026-06-01

seed_papers:
- P15 fixed-branch implementation specification.
- P18 annotated companion.

what_is_not_concluded:
- No empirical validation has been run in P19.
- A finite-difference parity test would validate implementation consistency
  only for the declared fixed branch, not posterior accuracy.

## Same-Branch Test Specified In P19

Build the branch once at \(\beta_0\), save all branch objects \(B\), and compare
\[
  \frac{\widehat\ell_T(\beta_0+h e_i;B)
        -\widehat\ell_T(\beta_0-h e_i;B)}{2h}
\]
against the analytical derivative computed by the derivative pass on the same
branch \(B\).

Important clarification added during execution: the branch manifest freezes
structural choices, not differentiable fitted outputs.  At \(\beta_0+h\) and
\(\beta_0-h\), the implementation must recompute the fitted core values from
the same saved fitting equations.  Copying the numerical cores from
\(\beta_0\) would test the wrong scalar.

## Required Frozen Branch Manifest

The execution ledger must record the exact branch objects that remain identical
for \(\beta_0\), \(\beta_0+h\), and \(\beta_0-h\):

- coordinate domains and domain maps;
- fitting points and weights;
- basis family and basis degree;
- TT rank vector;
- sweep count and sweep order;
- ridge parameter;
- defensive reference and defensive mass;
- stabilizing shifts;
- initial cores or deterministic initialization rule;
- any map/root-solver tolerances used in the scalar path.

## Required Branch-Identity Check

The same-branch test must explicitly confirm that the saved branch identifier
or manifest hash is identical for all three value evaluations:
\[
  B(\beta_0)=B(\beta_0+h)=B(\beta_0-h)=B.
\]
Rebuilding any structural branch object makes the finite-difference test a test
of a different adaptive scalar.  Reusing fixed core values without resolving
the fixed fitting equations at the perturbed parameter also invalidates the
test.

## Required Epsilon Schedule

Use a small schedule such as
\[
  h\in\{10^{-2},10^{-3},10^{-4},10^{-5}\},
\]
with values adjusted if the scalar is noisy or ill-conditioned.

## Required Error Metric And Pass/Fail Rule

For each component \(i\), compute
\[
  e_i(h)
  =
  \left|
  \frac{\widehat\ell_T(\beta_0+h e_i;B)
        -\widehat\ell_T(\beta_0-h e_i;B)}{2h}
  -
  \partial_i\widehat\ell_T(\beta_0;B)
  \right|.
\]
Also record a relative error with denominator
\[
  1+\left|\partial_i\widehat\ell_T(\beta_0;B)\right|.
\]
A pass requires a stable decreasing-error window before roundoff dominates.
Failure means the value path and derivative path do not currently agree for the
declared fixed branch; it does not by itself prove that the TT idea is invalid.

## Current Status

The finite-difference protocol is specified in the P19 note, but no numerical
implementation test was run in P19.  This is intentional: P19 is a derivation
and review artifact, not a production implementation run.

Decision: `FINITE_DIFFERENCE_PROTOCOL_SPECIFIED_NOT_RUN`.
