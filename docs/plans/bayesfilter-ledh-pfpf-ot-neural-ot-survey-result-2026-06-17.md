# Neural OT Survey Result For LEDH-PFPF-OT

Date: 2026-06-17

metadata_date: 2026-06-17

plan_file: `docs/plans/bayesfilter-ledh-pfpf-ot-neural-ot-survey-plan-2026-06-17.md`

result_status: `DRAFTED_AND_COMPILED`

## Objective

Produce a self-contained survey chapter block on neural-network techniques for optimal transport, focused on whether learned or amortized neural OT could alleviate the expensive OT subproblem in LEDH-PFPF-OT for high-dimensional BayesFilter use.  After user feedback that the first draft was too dense, the final objective became more specific: expand the topic into a decompressed OT mini-block that teaches the nearest implementation path in enough detail that a reader can almost implement it without reopening the source papers.

## Skeptical Audit Outcome

`PASSED_WITH_GUARDRAILS_RETAINED`

The draft stayed within the planned scope:
- it compared neural OT families against the explicit OT/EOT/Sinkhorn baseline from `ch32_diff_resampling_neural_ot`;
- it did not promote proxy transport metrics into filtering validity claims;
- it treated warm-started dual prediction, map surrogates, and dynamic geodesic learners as different approximation objects;
- it ended with a conservative decision ledger and non-conclusion boundary.

## Files Written Or Updated

- `docs/plans/bayesfilter-ledh-pfpf-ot-neural-ot-survey-plan-2026-06-17.md`
- `docs/chapters/ch32a_soft_differentiable_resampling.tex`
- `docs/chapters/ch32b_deterministic_ot_equalweighting.tex`
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`
- `docs/chapters/ch32d_retained_teacher_neural_ot.tex`
- `docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex`
- `docs/chapters/ch32f_dynamic_geodesic_operator_learning_target_contract.tex`
- `docs/chapters/ch19f_dpf_debugging_crosswalk.tex`
- `docs/main.tex`
- `docs/references.bib`
- `docs/plans/bayesfilter-ledh-pfpf-ot-neural-ot-survey-result-2026-06-17.md`

## Downloaded Source Workspace

Downloaded papers were stored under:
- `/home/chakwong/BayesFilter/.research/ra-bayesfilter-monograph/local_research/papers/neural_ot_ledh_pfpf_2026-06-17/`

The bounded set included:
- ICNN / Brenier line: Amos 2017, Makkuva et al. 2020, Uscidda--Cuturi 2023, Vesseron--Cuturi 2024, SICNN 2024, Korotin et al. 2021.
- Amortized / operator line: Amos et al. 2023, Geuter et al. 2025, GeONet 2024, Liu--Chen 2026, Xu--Cheng--Xie 2025.
- Filtering-adjacent context: Li--Coates 2017, Taghvaei--Hosseini 2022, Taghvaei--Mehta 2021, Hanebeck 2023, Chen--Dai--Song 2019.

## Source Support Status

### Accepted primary sources used in the chapter

- `LOCAL_FULL_TEXT_CHECKED` / `DOWNLOADED_FULL_TEXT_CHECKED`
  - Amos, Xu, Kolter (2017), *Input Convex Neural Networks*.
  - Makkuva, Taghvaei, Lee, Oh (2020), *Optimal Transport Mapping via Input Convex Neural Networks*.
  - Korotin et al. (2021), *Do Neural Optimal Transport Solvers Work? A Continuous Wasserstein-2 Benchmark*.
  - Uscidda, Cuturi (2023), *The Monge Gap: A Regularizer to Learn All Transport Maps*.
  - Amos, Luise, Cohen, Redko (2023), *Meta Optimal Transport*.
  - Vesseron, Cuturi (2024), *On a Neural Implementation of Brenier's Polar Factorization*.
  - Chen, Xie, Zhang (2024), *SICNN* workshop paper.
  - Gracyk, Chen (2024), *GeONet*.
  - Geuter et al. (2025), *Universal Neural Optimal Transport*.
  - Xu, Cheng, Xie (2025), *Computing High-Dimensional Optimal Transport by Flow Neural Networks*.
  - Liu, Chen (2026), *Neural Solver for Wasserstein Geodesics and Optimal Transport Dynamics*.
  - Li, Coates (2017), *Particle Filtering with Invertible Particle Flow*.
  - Taghvaei, Mehta (2021), *Optimal Transportation Methods in Nonlinear Filtering: The Feedback Particle Filter*.
  - Taghvaei, Hosseini (2022), *An Optimal Transport Formulation of Bayes' Law for Nonlinear Filtering Algorithms*.
  - Hanebeck (2023), *Progressive Bayesian Particle Flows Based on Optimal Transport Map Sequences*.
  - Chen, Dai, Song (2019), *Particle Flow Bayes' Rule*.

### Adjacent sources included as boundary markers rather than core evidence

- Vandergrift et al. (2026), *Measure-to-Measure Regression with Transformers*.
- Girshfeld, Chen (2025), *Neural Local Wasserstein Regression*.
- Micheli et al. (2026), *Riemannian Neural Optimal Transport*.

These were used to delimit nearby learned-measure and manifold-OT lanes, not to support direct claims that LEDH-PFPF-OT is already solved by neural OT.

## Main Supported Conclusions

1. **Best-supported immediate candidate:** if BayesFilter keeps the current entropic/discrete OT layer, the strongest literature-supported next step is a learned dual or initialization layer that still ends in a corrective OT solve. The main sources are `Meta OT` and `UNOT`.
2. **Pedagogic rewrite outcome:** the material now reads as a six-chapter OT/neural-OT block rather than a compressed survey chapter sequence:
   - `ch32a_soft_differentiable_resampling`
   - `ch32b_deterministic_ot_equalweighting`
   - `ch32c_entropic_ot_sinkhorn`
   - `ch32d_retained_teacher_neural_ot`
   - `ch32e_icnn_brenier_monge_gap_map_learning`
   - `ch32f_dynamic_geodesic_operator_learning_target_contract`
3. **Implementation-bearing core:** the chapters now make the strongest near-implementable spine explicit:
   - soft differentiable resampling,
   - deterministic OT equal-weighting,
   - entropic OT / Sinkhorn with barycentric projection,
   - retained-teacher warm-started neural acceleration.
4. **Human-monograph refocus:** the latest editorial pass removed or softened promotion-ladder, veto, bank-facing, and governance-heavy framing so that the OT/neural-OT material reads more like mathematical exposition and implementation guidance for human readers.
5. **Direct-map chapter deepening:** the ICNN/Brenier and Monge-gap chapter now contains fuller procedural contracts, including a more detailed ICNN training algorithm and a separate Monge-gap training algorithm.
6. **Dynamic/operator chapter deepening:** the dynamic/operator chapter now contains both a dynamic-path training algorithm and a same-scalar consistency-check procedure presented as mathematical interpretation rather than institutional gating.
7. **Broader neural OT is now visibly secondary:** direct learned map families and dynamic/operator learners have been split away from the retained-teacher acceleration route so that they can be read more slowly and as comparison/target-burden chapters rather than as coequal implementation chapters.
8. **Most principled structured map family:** ICNN/Brenier methods are the cleanest map-learning route when the relevant subproblem is genuinely a quadratic-cost Monge map, but the current sources do not justify saying that they have removed the repeated high-dimensional OT burden in BayesFilter workloads.
9. **Best practical surrogate family:** Monge-gap regularization is the clearest source-supported alternative when strict ICNN structure is too rigid, but it is a map surrogate route, not an equivalence proof to the original OT object.
10. **Strongest caution source:** the Korotin et al. benchmark is a real caution against promoting neural OT from proxy metrics alone.
11. **Dynamic/operator methods:** GeONet, Liu--Chen, and related dynamic transport learners are promising as larger re-architecture ideas, but they are weaker immediate substitutes for the current repeated OT solve than Meta OT or UNOT.

## Open Blockers And Uncertainties

- The chapter does not prove that the BayesFilter transport subproblem is exactly Brenier/Wasserstein-2 in the sense required by the ICNN literature.
- The chapter does not establish the training-distribution regularity needed for amortization across real filtering updates.
- The chapter does not validate any learned OT method on the actual BayesFilter scalar, same-scalar gradient contract, or HMC-facing target.
- Several dynamic/geodesic sources are recent and less settled than the ICML/PMLR foundational line.
- The SICNN evidence is workshop-level and should not be treated as mature default-policy support.

## What Was Not Concluded

This result note does not conclude:
- that any neural OT method is already correct for LEDH-PFPF-OT,
- that any learned map preserves the current scalar/gradient semantics,
- that static OT or image-style benchmark speedups transfer to repeated filtering,
- that a neural OT component is ready for BayesFilter defaults,
- that operator-learning geodesics answer the same question as warm-starting a retained OT solver.

## Verification

### Chapter integration
- `docs/main.tex` now includes a six-chapter OT/neural-OT block:
  - `docs/chapters/ch32a_soft_differentiable_resampling.tex`
  - `docs/chapters/ch32b_deterministic_ot_equalweighting.tex`
  - `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`
  - `docs/chapters/ch32d_retained_teacher_neural_ot.tex`
  - `docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex`
  - `docs/chapters/ch32f_dynamic_geodesic_operator_learning_target_contract.tex`
- The expanded block sits immediately before `docs/chapters/ch19e_dpf_hmc_target_suitability.tex`.
- The latest pass slowed the learned/neural-OT material further by separating retained-teacher acceleration from direct learned-map families, and direct learned-map families from dynamic/operator target-contract material.

### Bibliography
- Added the citation keys actually used by the new chapter to `docs/references.bib`.

### Build
- Ran:
  ```bash
  cd /home/chakwong/BayesFilter/docs && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
  ```
- Result: build succeeded and `latexmk` reported `main.pdf` up to date on the final pass.
- Notes: the build logs still contain pre-existing layout warnings elsewhere in the monograph, but no undefined citations or fatal errors from the new chapter were detected on the final pass.

## Next Justified Step

If the user wants to move from survey to experimentation, the most evidence-disciplined next step is **not** a generic learned transport replacement. It is a bounded experiment plan testing whether a learned dual / initialization layer can warm-start the retained entropic OT solve for families of related BayesFilter particle clouds, with explicit downstream veto diagnostics on the actual filtering scalar.
