# Recent neural OT paper shelf and code-availability matrix

## Date
2026-06-20

## Purpose
This note records the recent neural OT / conditional transport / operator-learning paper shelf for BayesFilter, using the normalized local folder:

- `/.localsource/neural_operator2/`

It also provides a durable code-availability / borrowability matrix so the monograph and implementation decisions can distinguish clearly between:
- mathematically interesting papers,
- code-backed papers,
- and papers whose code is practically easy or hard to borrow.

## Local paper shelf
Location:
- `/.localsource/neural_operator2/`

Normalized filenames now present:
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

## Family grouping
### Retained-teacher / amortized OT / conditional OT
- Meta Optimal Transport — Amos(23)
- Universal Neural Optimal Transport — Geuter(25)
- Efficient Neural Network Approaches for Conditional Optimal Transport with Applications in Bayesian Inference — Wang(25)
- Conditional Optimal Transport on Function Spaces — Hosseini(25)
- Supervised Training of Conditional Monge Maps — Bunne(22)

### Direct static map learning
- Optimal Transport Mapping via Input Convex Neural Networks — Makkuva(20)
- GradNetOT Learning Optimal Transport Maps with GradNets — Chaudhari(25)
- Learning Monge Maps by Lifting and Constraining Wasserstein Gradient Flows — Dumont(26)
- Displacement-Sparse Neural Optimal Transport — Chen(25)

### Dynamic / geodesic / operator / measure-to-measure
- GeONet: A Neural Operator for Learning the Wasserstein Geodesic — Gracyk(24)
- Neural Solver for Wasserstein Geodesics and Optimal Transport Dynamics — Chen(25)
- Measure-to-measure Regression with Transformers — Vandergrift(26)
- Neural Local Wasserstein Regression — Girshfeld(25)
- Riemannian Neural Optimal Transport — Micheli(26)

### Scalable / unbalanced / solver-side
- Progressive Entropic Optimal Transport Solvers — Kassraie(24)
- Light Unbalanced Optimal Transport — Gazdieva(24)
- Unbalanced Low-Rank Optimal Transport Solvers — Scetbon(23)
- Fixed-Point Neural Optimal Transport without Implicit Differentiation — Park(26)

### Filtering-specific / closest application match
- Nonlinear Filtering with Brenier Optimal Transport Maps — Al-Jarrah(25)

## Code-availability and borrowability matrix

| Paper | Code? | Repo / source | Borrowability quick read | BayesFilter fit |
|---|---|---|---|---|
| Meta Optimal Transport — Amos(23) | yes | `facebookresearch/meta-ot` | usable_but_bridge_required | retained-teacher / amortized solver |
| Universal Neural Optimal Transport — Geuter(25) | yes | `GregorKornhardt/UNOT` | usable_but_bridge_required; grid/FNO-specific | retained-teacher/operator-ish but representation-mismatched |
| Optimal Transport Mapping via Input Convex Neural Networks — Makkuva(20) | yes | `AmirTag/OT-ICNN` | usable_but_bridge_required; direct-map and older stack | direct-map baseline |
| Computing High-Dimensional OT by Flow Neural Networks / FlowOT family | yes in broader notes | code-backed but not on this local shelf | likely usable_but_bridge_required | dynamic/direct map alternative |
| GeONet — Gracyk(24) | unclear/partial from current local notes | recent work, code visibility not yet confirmed here | unclear | dynamic/geodesic/operator |
| Neural Solver for Wasserstein Geodesics and OT Dynamics — Chen(25) | unclear from current local notes | recent work, code visibility not yet confirmed here | unclear | dynamic/geodesic/operator |
| Conditional OT on Function Spaces — Hosseini(25) | unclear from current local notes | not yet confirmed in this pass | unclear | conditional OT / Bayesian inference |
| Efficient Neural Network Approaches for Conditional OT with Applications in Bayesian Inference — Wang(25) | unclear from current local notes | not yet confirmed in this pass | unclear | conditional OT / Bayesian inference |
| Supervised Training of Conditional Monge Maps — Bunne(22) | unclear from current local notes | not yet confirmed in this pass | unclear | conditional direct-map |
| Nonlinear Filtering with Brenier Optimal Transport Maps — Al-Jarrah(25) | unclear from current local notes | not yet confirmed in this pass | unclear but highly relevant | filtering-specific direct-map |
| Displacement-Sparse Neural OT — Chen(25) | unclear | not yet confirmed in this pass | unclear | direct-map / structured |
| GradNetOT — Chaudhari(25) | unclear | not yet confirmed in this pass | unclear | direct-map |
| Learning Monge Maps by Lifting and Constraining Wasserstein Gradient Flows — Dumont(26) | unclear | not yet confirmed in this pass | unclear | direct-map |
| Light Unbalanced Optimal Transport — Gazdieva(24) | unclear | not yet confirmed in this pass | unclear | unbalanced/scalable |
| Measure-to-measure Regression with Transformers — Vandergrift(26) | unclear | not yet confirmed in this pass | unclear | operator / measure-to-measure |
| Neural Local Wasserstein Regression — Girshfeld(25) | unclear | not yet confirmed in this pass | unclear | local operator/regression |
| Progressive Entropic Optimal Transport Solvers — Kassraie(24) | unclear | not yet confirmed in this pass | unclear but potentially useful | solver-side acceleration |
| Riemannian Neural OT — Micheli(26) | unclear | not yet confirmed in this pass | unclear | manifold OT |
| Unbalanced Low-Rank OT Solvers — Scetbon(23) | unclear | not yet confirmed in this pass | unclear but likely more solver-side than direct borrow | scalable/unbalanced |
| Fixed-Point Neural OT without Implicit Differentiation — Park(26) | unclear | not yet confirmed in this pass | unclear | solver/direct-map hybrid |

## Practical reading of the matrix
### Easiest currently confirmed code-backed lanes
1. Meta OT
2. UNOT
3. OT-ICNN

### Most central to BayesFilter’s current interests
1. Efficient Neural Network Approaches for Conditional OT with Applications in Bayesian Inference — Wang(25)
2. Conditional Optimal Transport on Function Spaces — Hosseini(25)
3. Nonlinear Filtering with Brenier Optimal Transport Maps — Al-Jarrah(25)
4. Universal Neural Optimal Transport — Geuter(25)
5. GeONet / neural geodesic/operator routes as comparison families

### Important caution
The easiest confirmed code-backed lanes are not automatically the most scientifically central recent work. OT-ICNN and Meta OT are older/easier to borrow, but the local recent shelf suggests the monograph should now emphasize newer conditional, operator, and filtering-specific work more visibly.

## Immediate recent-work gaps still worth filling
The local shelf is already strong, but still comparatively light on:
- more filtering-native transport work,
- diffusion / Schrödinger-bridge / flow-matching transport families,
- broader operator-learning work for posterior-update maps,
- sequential simulation-based posterior transport.

These should be filled only in a bounded way, with a clear reason for each addition.

## Intended use in the monograph
This matrix should support:
- recent-work subsections in `ch32d`, `ch32e`, and `ch32f`,
- chapter-local code-backed visibility notes,
- and later implementation triage without confusing “has code” with “good candidate for BayesFilter.”
