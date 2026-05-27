# P7 Transport-Preconditioned HMC, NeuTra, And TT-KR Bridge Rewrite Plan

## Objective

Rewrite HMC acceleration as a primary-source bridge between transport maps,
TT/KR representations, NeuTra, and fixed-trajectory corrected HMC for nonlinear
SSMs.

## Inputs

- P1 source ledger entries for transport-map accelerated MCMC, NeuTra HMC, deep
  inverse Rosenblatt transports using tensor trains, Zhao-Cui conditional KR
  transports, and HMC diagnostic sources.
- Existing `ch36`.

## Execution Precondition

Execution is forbidden unless every HMC, transport-map MCMC, NeuTra, TT/KR, and
inverse Rosenblatt source used by P7 is `LOCAL_FULL_TEXT_CHECKED` in the P1
ledger with local artifact path, inspected technical sections, inspected
equation/theorem/algorithm identifiers where available, and chapter consumers
recorded.  `LOCAL_SUMMARY_ONLY` NeuTra material may guide intake only; it cannot
support the chapter derivation.

## Required Content

1. Posterior target for nonlinear SSM parameters/states and approximate
   likelihood boundary.
2. Change-of-variables derivation for transported HMC targets.
3. NeuTra target and correction derivation.
4. TT/KR inverse Rosenblatt bridge: how a triangular transport can be
   represented or approximated by tensor machinery.
5. Fixed-HMC same-scalar condition and diagnostics.
6. Algorithmic ladder: plain dense/diagonal mass matrix, transport-preconditioned
   HMC, NeuTra, TT/KR proposal, learned dynamics as corrected proposal only.
7. Complexity and failure modes: map training cost, inverse/Jacobian stability,
   divergence, E-BFMI, R-hat, ESS, acceptance, energy error, and posterior
   reference checks.
8. Paper-by-paper mapping from source equation/theorem/algorithm to chapter
   subsection and derivation/proof sketch.

## Outputs

- Rewritten `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`.
- P7 result note.
- Paper-by-paper exposition checklist and source-to-chapter mapping table.

## Stop Conditions

- Stop if transport/HMC primary sources are not locally inspected.
- Stop if any wording suggests HMC convergence or production readiness.

## Verification

- `rg -n "NeuTra|transport|Rosenblatt|Hamiltonian|Jacobian|divergence|E-BFMI" docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
- `docs/references.bib` only for checked sources consumed by P7.
- `docs/source_map.yml` only for P7 provenance entries.

## What Must Not Be Concluded

P7 treats HMC as a per-model research problem.  No HMC, NeuTra, TT/KR, or HNN
path is validated for BayesFilter or NAWM.
