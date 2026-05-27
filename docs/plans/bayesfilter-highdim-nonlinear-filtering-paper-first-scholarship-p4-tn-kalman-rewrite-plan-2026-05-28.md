# P4 Tensor-Network Kalman And Square-Root Tensor Filtering Rewrite Plan

## Objective

Rewrite tensor-network Kalman material from source-gap notes into scholarly
exposition of TNKF, lifted Volterra/state-space structure, square-root tensor
covariance safeguards, and low-rank tensor observation compression examples.

## Inputs

- P1 source ledger entries for Batselier-Chen-Wong TNKF, tensor-network
  square-root Kalman filter, and low-rank tensor UKF tractography paper.
- Existing `ch35`.

## Execution Precondition

Execution is forbidden unless every TN/TNKF paper used by P4 is
`LOCAL_FULL_TEXT_CHECKED` in the P1 ledger with local artifact path, inspected
technical sections, inspected equation/theorem/algorithm identifiers where
available, and chapter consumers recorded.  Any missing full-text inspection
blocks chapter editing.

## Required Content

1. Lifted linear or Volterra system setting and why tensor-network compression
   enters.
2. Kalman prediction/update in tensor-network format.
3. Square-root/factorized covariance proposition explaining why PSD structure is
   safer than direct rounded covariance.
4. Complexity in state dimension, lifted feature dimension, tensor ranks, and
   covariance/factor storage.
5. Failure modes: rank growth, loss of PSD, rounding drift, lifted-model
   mismatch, and observation-compression distortion.
6. Comparison with TT density filtering: covariance/factor compression versus
   full density/operator compression.
7. Paper-by-paper mapping from source equation/theorem/algorithm to chapter
   subsection and proof sketch.

## Outputs

- Rewritten TN material in `ch35` or documented chapter reassignment.
- P4 result note.
- Paper-by-paper exposition checklist and source-to-chapter mapping table.

## Stop Conditions

- Stop if source text is not locally inspected.
- Stop if square-root claims cannot be tied to source equations or general
  covariance-factor derivation.

## Verification

- `rg -n "tensor-network|TNKF|square-root|Volterra|positive semidefinite|PSD" docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/references.bib` only for checked sources consumed by P4.
- `docs/source_map.yml` only for P4 provenance entries.

## What Must Not Be Concluded

P4 does not validate TNKF for nonlinear DSGE filtering or claim tensor-network
covariance compression is stable without diagnostics.
