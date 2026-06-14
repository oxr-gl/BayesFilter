# BayesFilter Float64 Reference Branch

This local branch is a BayesFilter audit reference variant of filterflow.

- Branch: `bayesfilter-py311-float64-reference`
- Base executable reference: `bayesfilter-py311-compat`
- Purpose: use float64 TensorFlow/NumPy data paths for BayesFilter versus
  filterflow difference audits.
- Status: local reference branch, not pristine upstream filterflow and not a
  BayesFilter implementation.
- Reproduction setting: executable filterflow `I_2` transition covariance for
  the Section-5.1-style LGSSM table.

The branch exists because the float32 executable path showed machine-precision
trace/recompute sensitivity in transport replay diagnostics.  A prior
BayesFilter probe found that the float64 execution variant preserves the
Section-5.1-style table scale within the canonical float32 Monte Carlo band.
