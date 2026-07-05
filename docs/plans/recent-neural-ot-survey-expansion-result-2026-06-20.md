# Recent neural OT survey expansion result

## Date
2026-06-20

## Objective
Expand the OT/neural-OT chapter block into a more recent-work-aware, mathematically self-contained survey while preserving the existing six-chapter pedagogic structure, and provide a durable code-availability / borrowability matrix backed by a local paper shelf.

## Local paper shelf created
New local folder:
- `/.localsource/neural_operator2/`

The current recent-paper shelf has been normalized into `Paper Title Author(Year).pdf` style and populated from the existing local set.

Normalized paper set currently present:
- Conditional Optimal Transport on Function Spaces — Hosseini(25)
- Displacement-Sparse Neural Optimal Transport — Chen(25)
- Efficient Neural Network Approaches for Conditional Optimal Transport with Applications in Bayesian Inference — Wang(25)
- Fixed-Point Neural Optimal Transport without Implicit Differentiation — Park(26)
- GeONet: A Neural Operator for Learning the Wasserstein Geodesic — Gracyk(24)
- GradNetOT Learning Optimal Transport Maps with GradNets — Chaudhari(25)
- Learning Monge Maps by Lifting and Constraining Wasserstein Gradient Flows — Dumont(26)
- Light Unbalanced Optimal Transport — Gazdieva(24)
- Measure-to-measure Regression with Transformers — Vandergrift(26)
- Meta Optimal Transport — Amos(23)
- Neural Local Wasserstein Regression — Girshfeld(25)
- Neural Solver for Wasserstein Geodesics and Optimal Transport Dynamics — Chen(25)
- Nonlinear Filtering with Brenier Optimal Transport Maps — Al-Jarrah(25)
- Optimal Transport Mapping via Input Convex Neural Networks — Makkuva(20)
- Progressive Entropic Optimal Transport Solvers — Kassraie(24)
- Riemannian Neural Optimal Transport — Micheli(26)
- Supervised Training of Conditional Monge Maps — Bunne(22)
- Unbalanced Low-Rank Optimal Transport Solvers — Scetbon(23)
- Universal Neural Optimal Transport — Geuter(25)

## New durable artifacts
### Code-availability / borrowability matrix
- `docs/plans/recent-neural-ot-code-availability-matrix-2026-06-20.md`

This matrix now records:
- paper title and family grouping,
- code availability (yes / unclear / no),
- rough borrowability assessment,
- and BayesFilter fit.

### Source/provenance update
- `docs/source_map.yml`

Added entries for:
- the new `neural_operator2` local shelf,
- the code-availability matrix artifact.

## Chapter updates made
The recent-work surfacing was added directly into the existing OT block rather than creating a new compressed survey chapter.

Updated chapters:
- `docs/chapters/ch32d_retained_teacher_neural_ot.tex`
- `docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex`
- `docs/chapters/ch32f_dynamic_geodesic_operator_learning_target_contract.tex`

### ch32d changes
Added a recent retained-teacher / conditional OT subsection that surfaces:
- Meta OT
- UNOT
- nearby conditional transport literature

Also added a compact table explaining how these recent retained-teacher-adjacent families relate to BayesFilter.

### ch32e changes
Added a recent direct-map literature subsection that now frames:
- OT-ICNN
- Monge-gap
- Brenier-factorization / benchmark context
- direct-map family caution

This makes the direct-map chapter read more like a recent-work survey instead of only a theory exposition.

### ch32f changes
Added a recent dynamic/geodesic/operator subsection and compact family table that now surface:
- GeONet / neural geodesic learners
- dynamic OT solvers
- neural operator families
- sliced / subspace families as target-changing routes

## What was preserved
The six-chapter OT block structure in `docs/main.tex` was kept intact.

The pedagogic decomposition remains:
1. soft differentiable resampling
2. deterministic OT equal-weighting
3. entropic OT / Sinkhorn
4. retained-teacher neural warm starts
5. direct map learning via ICNN/Brenier/Monge-gap
6. dynamic geodesic/operator learners

This preserves the strongest part of the current monograph structure while adding the missing recent-work visibility.

## Verification
Rebuilt the LaTeX document with BibTeX after the chapter and bibliography updates:
```bash
cd /home/chakwong/BayesFilter/docs && latexmk -pdf -bibtex -interaction=nonstopmode -halt-on-error -g main.tex
```

Result:
- build completed successfully,
- no remaining missing bibliography-entry warnings,
- no undefined citation warnings from this recent-work expansion pass,
- `main.pdf` is up to date.

## Current limitations
This pass improves chapter-facing visibility and source traceability, but it does not yet add an exhaustive broader modern corpus beyond the current bounded shelf. In particular, the shelf still looks lighter on:
- filtering-native OT papers,
- diffusion / Schrödinger-bridge / flow-matching transport families,
- broader operator-learning work for posterior update maps.

So the recent-work survey is now substantially better than before, but it is still bounded rather than exhaustive.

## Supported conclusion
The OT chapter block is now in a much better state for reader understanding:
- the recent paper set is visible,
- code-backed visibility is documented,
- and the monograph now better reflects that OT-ICNN is only one older direct-map baseline inside a broader recent literature landscape.
