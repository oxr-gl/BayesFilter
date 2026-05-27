# P3 Tensor-Train Nonlinear Filtering Rewrite Plan

## Objective

Rewrite tensor-train filtering material into a full paper-first exposition
covering direct TT nonlinear filtering, TT grid filtering, correlated-noise
extensions, TT sequential learning, conditional KR transports, and tensor
substrate papers.

## Inputs

- P1 source ledger entries for Li-Wang-Yau-Zhang, Zhao-Cui, functional TT grid
  filtering, Meng-Yau-Zhang, TT sampling, TT Gaussian rank bounds,
  Fokker-Planck TT cross approximation, and tensor-network integration.
- Existing `ch35` and `ch37`.

## Execution Precondition

Execution is forbidden unless every TT paper used by P3 is
`LOCAL_FULL_TEXT_CHECKED` in the P1 ledger with local artifact path, inspected
technical sections, inspected equation/theorem/algorithm identifiers where
available, and chapter consumers recorded.  Mixed ledgers are not sufficient:
any `LOCAL_SUMMARY_ONLY`, `METADATA_ONLY`, `NEEDS_NETWORK_INTAKE`, or
`PAYWALL_OR_ACCESS_BLOCKED` entry needed by P3 blocks chapter editing.

## Required Content

For each inspected TT paper:

1. Problem setting and model class.
2. Main equation or approximation object.
3. TT representation and rank assumptions.
4. Derivation from filtering/PDE/transport equation to TT approximation.
5. Algorithmic offline/online or sequential update.
6. Complexity and memory in dimension, mode size, rank, and time horizon.
7. Failure modes: rank explosion, positivity, normalization, grid error,
   truncation, correlated noise, boundary conditions, and likelihood distortion.
8. Relevance and limits for nonlinear DSGE/NAWM-like use.

Each paper must also receive a mapping row from source
section/equation/theorem/algorithm to chapter subsection and derivation/proof
sketch.

## Outputs

- Rewritten TT portions in `ch35` or, if chapter organization changes, a
  documented reassignment in the P3 result note.
- Citation ledger updates if P1 permits bibliography changes.
- Paper-by-paper exposition checklist covering problem setting, notation
  translation, main equations, derivation/proof sketch, algorithm, complexity,
  failure modes, and no-overclaim boundary.

## Stop Conditions

- Stop if any TT primary paper is not locally inspected.
- Stop if a theorem or algorithm cannot be reproduced beyond abstract-level
  description.

## Verification

- `rg -n "tensor train|TT|Knothe|Rosenblatt|Fokker|DMZ|rank" docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- MathDevMCP label lookup after labels are introduced.

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex` only for
  synthesis cross-references introduced by P3.
- `docs/references.bib` only for checked sources consumed by P3.
- `docs/source_map.yml` only for P3 provenance entries.

## What Must Not Be Concluded

P3 may present TT methods as serious candidates, but may not claim TT solves
high-dimensional filtering generally or validates BayesFilter/NAWM performance.
