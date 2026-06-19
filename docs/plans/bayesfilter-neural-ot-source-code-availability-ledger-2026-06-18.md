# Neural OT Source-Code Availability Ledger

## Date
2026-06-18

## Context

The OT/neural-OT monograph block is now mature enough that the next step is
implementation.  Before implementation starts, we need a durable note stating
which surveyed algorithms appear to have publicly available source code, where
that code lives, and whether the repository is likely to help with direct
BayesFilter implementation.

This note is not a code-quality review.  It is a source-availability and
implementation-relevance ledger so that future sessions do not have to rediscover
which papers are code-backed and which are theory-only or paper-only.

## Scope

This note covers the papers downloaded into:

- `/home/chakwong/BayesFilter/.research/ra-bayesfilter-monograph/local_research/papers/neural_ot_ledh_pfpf_2026-06-17/`

and the surrounding OT/neural-OT chapter block in the monograph.

## Availability classes

- `OFFICIAL_REPO_CONFIRMED` — the paper page or PDF clearly names an official code repository.
- `REPO_MENTIONED_IN_PDF` — the PDF text contains a repository URL or code claim, but the paper page did not clearly expose it in the fetch used here.
- `NO_REPO_FOUND_IN_CURRENT_CHECK` — no official repository was found in the paper page or the PDF checks already run.
- `NOT_A_PRIMARY_IMPLEMENTATION_TARGET` — conceptually relevant, but not one of the main BayesFilter implementation routes we currently plan to build first.

## Source-code ledger

| Paper / route | Local artifact | Availability class | Repository / source location | Implementation relevance for BayesFilter |
|---|---|---|---|---|
| Meta Optimal Transport | `amos23_meta_optimal_transport.pdf` | `OFFICIAL_REPO_CONFIRMED` | `https://github.com/facebookresearch/meta-ot` | High. Closest code-backed route for retained-teacher warm-started acceleration of entropic OT solves. |
| Universal Neural Optimal Transport (UNOT) | `geuter25_universal_neural_optimal_transport.pdf` | `OFFICIAL_REPO_CONFIRMED` | `https://github.com/GregorKornhardt/UNOT` | High. Strong code-backed route for predicting dual potentials / Sinkhorn initialization across discrete OT problems. |
| Optimal Transport Mapping via Input Convex Neural Networks | `makkuva20_icnn_ot_mapping.pdf` | `OFFICIAL_REPO_CONFIRMED` | `https://github.com/AmirTag/OT-ICNN` | Moderate to high. Most relevant direct-map implementation source for the ICNN/Brenier chapter. |
| Computing High-Dimensional Optimal Transport by Flow Neural Networks | `xu25_flow_neural_networks_highdim_ot.pdf` | `OFFICIAL_REPO_CONFIRMED` | `https://github.com/hamrel-cxu/FlowOT` | Moderate. Useful for the dynamic/direct transport branch, but farther from the retained-teacher BayesFilter route. |
| TrajectoryNet | `tong20_trajectorynet_dynamic_ot.pdf` | `OFFICIAL_REPO_CONFIRMED` | `https://github.com/KrishnaswamyLab/TrajectoryNet` | Moderate. Dynamic/path learner reference; not the main near-term BayesFilter implementation route. |
| Input Convex Neural Networks | `amos17_input_convex_neural_networks.pdf` | `REPO_MENTIONED_IN_PDF` | PDF text says source code exists in an `icml2017` GitHub branch, but the paper page did not expose a clean official repo URL in the checks run here. | Moderate. Useful architectural background, but not itself the transport algorithm we would implement first. |
| Do Neural Optimal Transport Solvers Work? A Continuous Wasserstein-2 Benchmark | `korotin21_do_neural_ot_solvers_work.pdf` | `REPO_MENTIONED_IN_PDF` | `https://github.com/iamalexkorotin/Wasserstein2Benchmark` | Moderate as a benchmark/diagnostic source, not a primary implementation template. |
| Do Neural Optimal Transport Solvers Work? related code references | `korotin21_do_neural_ot_solvers_work.pdf` | `REPO_MENTIONED_IN_PDF` | `https://github.com/iamalexkorotin/Wasserstein2GenerativeNetworks`, plus referenced third-party repos in the benchmark discussion | Low to moderate. Useful for reproducing benchmark context, not a direct BayesFilter implementation lane. |
| The Monge Gap: A Regularizer to Learn All Transport Maps | `uscidda23_monge_gap.pdf` | `REPO_MENTIONED_IN_PDF` | PDF text references `https://github.com/ott-jax/ott` as the computational OT library used; the paper page did not expose an official dedicated repo in the checks run here. | Moderate. Relevant for the Monge-gap chapter, but likely needs adaptation rather than direct reuse. |
| GeONet | local seed PDF in `.localsource/neural operator/` | `NO_REPO_FOUND_IN_CURRENT_CHECK` | No official software repository was exposed by the page checks; only LaTeX source was visible on the OpenReview page. | Conceptually relevant, but currently not code-backed in our notes. |
| Neural solver for Wasserstein Geodesics and Optimal Transport Dynamics | `liu_chen26_wasserstein_geodesics_dynamics.pdf` | `NO_REPO_FOUND_IN_CURRENT_CHECK` | No official repository found in the checks run here. | Conceptually relevant for dynamic path learning, but currently paper-only in our notes. |
| Riemannian Neural Optimal Transport | `micheli26` seed/downloaded reference | `NO_REPO_FOUND_IN_CURRENT_CHECK` | No official repository found in the checks run here. | Boundary-marker family, not a primary implementation target. |
| SICNN | `sicnn24_sparse_icnn_ot.pdf` | `NO_REPO_FOUND_IN_CURRENT_CHECK` | No official repository found in the checks run here. | Interesting structured direct-map variant, but currently not code-backed in our notes and not a first implementation target. |
| Particle Flow Bayes' Rule | `chen_dai_song19_particle_flow_bayes_rule.pdf` | `NO_REPO_FOUND_IN_CURRENT_CHECK` | No official repository found in the checks run here. | Filtering-adjacent conceptual source, not the immediate OT implementation route. |
| Progressive Bayesian Particle Flows Based on OT Map Sequences | `hanebeck23_progressive_bayesian_particle_flows_ot_sequences.pdf` | `NO_REPO_FOUND_IN_CURRENT_CHECK` | No official repository found in the checks run here. | Filtering-adjacent conceptual source, not a first implementation source. |
| Invertible Particle Flow PF | `li_coates17_invertible_particle_flow_pf.pdf` | `NO_REPO_FOUND_IN_CURRENT_CHECK` | No public repository surfaced in the checks run here. | Important algorithmic context for PF-PF/LEDH, but not code-backed in this pass. |
| OT formulation of Bayes' law / FPF OT methods | `taghvaei_hosseini22_ot_bayes_law_filtering.pdf`, `taghvaei_mehta21_feedback_particle_filter_ot_methods.pdf` | `NO_REPO_FOUND_IN_CURRENT_CHECK` | No official repository found in the checks run here. | Important conceptual context, not first implementation source. |

## Immediate implementation ranking

### Strongest code-backed candidates for the first implementation pass

1. **Retained-teacher warm-started entropic OT**
   - Main code-backed papers:
     - `Meta OT` — `https://github.com/facebookresearch/meta-ot`
     - `UNOT` — `https://github.com/GregorKornhardt/UNOT`
   - Why first:
     - This is the most aligned with the monograph’s implementation-bearing core.
     - It preserves the EOT/Sinkhorn teacher while learning a solver-relevant latent state.

2. **Direct-map ICNN/Brenier route**
   - Main code-backed paper:
     - `OT-ICNN` — `https://github.com/AmirTag/OT-ICNN`
   - Why second:
     - It is the clearest code-backed direct-map baseline if we decide to implement a map-learning branch after the retained-teacher route.

3. **Dynamic/direct flow route**
   - Main code-backed paper:
     - `FlowOT` — `https://github.com/hamrel-cxu/FlowOT`
   - Why later:
     - Conceptually useful, but it is farther from the current BayesFilter retained-teacher route and likely requires more adaptation.

### Useful benchmark / reproduction support

- `Wasserstein2Benchmark` — `https://github.com/iamalexkorotin/Wasserstein2Benchmark`
  - useful for testing or sanity benchmarking, not as the first implementation target.

## What is not yet documented here

This note does **not** yet assess:
- repo quality,
- language/framework maturity,
- whether the code still runs,
- whether licenses are compatible with reuse,
- whether the repo implements the exact paper version used in the monograph,
- whether the code is easy to adapt to TensorFlow/TFP BayesFilter conventions.

Those are implementation-phase questions and should be checked before copying or reusing external code.

## Suggested next steps

1. Start the implementation plan with the retained-teacher route only:
   - use `Meta OT` and `UNOT` as the first code-backed references.
2. For each candidate repo, create a short implementation-fit note recording:
   - framework,
   - training vs inference separation,
   - what exact latent object is predicted,
   - what BayesFilter adaptation would be required.
3. Only after the retained-teacher route is scoped should the direct-map (`OT-ICNN`) and dynamic-route (`FlowOT`) repos be reviewed for possible secondary branches.
