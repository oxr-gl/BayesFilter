# P1 Result: Donor Source Anchor Audit

Date: 2026-06-27

## Status

`PASS_P1_DONOR_AUDIT_READY_FOR_P2`

## Decision

`PASS_P1_DONOR_AUDIT_READY_FOR_P2`

BayesFilter now has a donor-audit artifact precise enough to force a P2 donor decision.

The audit confirms that both `Meta OT` and `UNOT` remain serious retained-teacher candidates, but they are not interchangeable:
- `Meta OT` is the cleaner retained-teacher warm-start conceptual donor for amortizing solver-native state and preserving corrective teacher iterations.
- `UNOT` is the stronger discrete entropic / dual-potential operator donor, but it carries a larger representation bridge from grid/resolution-centric inputs to BayesFilter's unordered particle-cloud route.

P1 does **not** choose the donor. It prepares the evidence needed for P2.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter audit Meta OT and UNOT at the paper+official-repo level tightly enough to identify the exact learned object, retained correction mechanism, training/inference split, donor modules/functions, and major adaptation blockers before any further custom retained-teacher implementation proceeds? |
| Baseline/comparator | Current donor evidence in `docs/plans/bayesfilter-neural-ot-source-code-availability-ledger-2026-06-18.md`, `docs/plans/bayesfilter-neural-ot-implementation-fit-note-2026-06-18.md`, and conceptual route notes in `docs/chapters/ch32d_retained_teacher_neural_ot.tex`. |
| Primary pass criterion | A result artifact records, for both Meta OT and UNOT, a paper anchor table, official repo anchor table, predicted object, retained correction/deployment semantics, training/inference split, framework/license/runability notes, and a first BayesFilter fit classification. |
| Veto diagnostics | No official repo anchor; no distinction between paper-level claim and repo-level implementation; no explicit predicted-object entry; no distinction between core algorithm and benchmark scaffolding; no license/framework notes. |
| Explanatory diagnostics | Repo layout, dependency stack, benchmark assets, model-weight availability, and convenience comments only. |
| Not concluded | P1 does not choose the primary donor and does not yet port code. |

## BayesFilter Retained-Teacher Route To Match

The target BayesFilter route remains the chapter definition in `docs/chapters/ch32d_retained_teacher_neural_ot.tex`:
- learn a **teacher-native latent state** rather than the final transport answer,
- keep the **corrective teacher solve** in deployment,
- judge success by the corrected teacher output and residual contract rather than by raw predictor loss alone.

This is the benchmark against which both donors are evaluated.

## Donor 1: Meta OT

### Paper anchors already recorded in BayesFilter notes
The in-repo candidate comparison note reconstructs Meta OT as follows:
- discrete entropic teacher dual and plan recovery: Equation (6), see `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex:1771-1787`
- Sinkhorn teacher updates: Algorithm 1 substance, see `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex:1789-1797`
- single-dual amortization objective: Equation (16), see `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex:1799-1815`
- objective-based amortization loss: Equation (17), see `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex:1816-1821`
- retained correction semantics: corrected Sinkhorn still closes the loop, see `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex:1878-1890`
- implementation contract: learned object is a solver-native latent state, deployed object is the corrected teacher output, see `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex:1956-1975`

### What the paper-level route appears to learn
At the paper level, the clearest discrete route is:
- predict one dual half `f` (or equivalent solver-native dual state),
- recover the complementary dual half from the teacher-side first-order condition,
- run corrective Sinkhorn afterwards.

This is the cleanest direct match to BayesFilter's retained-teacher semantics.

### Official repo snapshot
Official repo: [facebookresearch/meta-ot](https://github.com/facebookresearch/meta-ot)

Visible repo-level facts from the README/repo page fetch:
- license appears as **CC BY-NC 4.0**,
- README states the repo builds on **JAX and OTT**,
- visible top-level files/directories include:
  - `conf/`
  - `meta_ot/`
  - `train_discrete.py`
  - `train_color_meta.py`
  - `train_color_single.py`
  - `eval_discrete.py`
  - `eval_color.py`
- training is organized around dedicated `train_*.py` entry points,
- evaluation/inference is organized around dedicated `eval_*.py` entry points.

### Repo-level implementation reading from available evidence
From the README/page fetch and the in-repo notes, the repo appears to implement:
- explicit training vs inference separation,
- a Meta OT model family for discrete OT and color-transfer experiments,
- a retained-teacher framing where the model predicts solver-relevant state rather than directly replacing the teacher solve.

What is still unresolved at the repo-code level from the current visible evidence:
- exact internal module/function names for the predicted discrete dual object,
- exact decomposition between core retained-teacher mechanism and experiment shell,
- exact license implications for reuse inside BayesFilter.

### First BayesFilter fit classification
`Meta OT` remains the strongest **retained-teacher warm-start** donor.

Strengths:
- closest match to “predict solver-native state, then correct with teacher,”
- conceptually clean retained-correction semantics,
- strongest fit to the chapter’s semantic conservatism.

Main adaptation blockers:
- JAX/OTT donor stack versus TensorFlow/TFP BayesFilter stack,
- unresolved exact target-object mapping into particle-cloud retained-teacher BayesFilter data,
- repo-level licensing and runnable-core extraction still need explicit audit.

## Donor 2: UNOT

### Paper anchors already recorded in BayesFilter notes
The in-repo candidate comparison note reconstructs UNOT as follows:
- discrete entropic teacher via Sinkhorn scaling variables and plan recovery: Algorithm 1 substance, see `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex:2021-2034`
- learned dual-derived latent quantity `g` / log-scaling route, see `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex:2036-2047`
- synthetic generator and supervised target generation: Equation (6), Equation (7), Algorithm 2, see `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex:2048-2055`
- quotient-space / dual nonuniqueness issue, see `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex:2093-2109`
- deployment route may still use corrected Sinkhorn warm-starting, see `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex:2176-2213`

### What the paper-level route appears to learn
At the paper level, UNOT learns a **dual-derived latent quantity** (log-scaling / dual potential style object) over discrete OT problems, with training built around:
- a synthetic problem generator,
- Sinkhorn-generated target refinement,
- operator-style prediction over varying discretizations.

It still stays close to a retained discrete entropic OT teacher, but is less obviously “minimal warm-start MLP” and more clearly “operator over problem families.”

### Official repo snapshot
Official repo: [GregorKornhardt/UNOT](https://github.com/GregorKornhardt/UNOT)

Visible repo-level facts from the README/repo page fetch:
- license appears as **MIT**,
- visible top-level files/directories include:
  - `Data/geonet`
  - `Models`
  - `scripts`
  - `src`
  - `requirements.txt`
- visible runtime hints include:
  - `torch.device(...)` in README examples,
  - mention of `FNO` and `MLP` models,
  - pretrained weights stored under `Models` with `git lfs pull`,
  - entry points like `src.evaluation.import_models.load_fno` and `load_fno_var_epsilon`.

### Repo-level implementation reading from available evidence
From the README/page fetch and in-repo notes, the repo appears to implement:
- a discrete entropic OT operator-learning route,
- explicit training scripts (`scripts/main_neural_operator.py`, data generation scripts),
- explicit model-loading / inference entry points,
- an operator-style representation closer to grid/resolution-centric measure pairs than to unordered BayesFilter particle clouds.

What is still unresolved at the repo-code level from current visible evidence:
- exact code-level decomposition between dual-potential prediction and downstream corrected Sinkhorn deployment,
- exact target-representation conventions used during training,
- exact minimal core route that should be ported independent of synthetic data scaffolding.

### First BayesFilter fit classification
`UNOT` remains a strong **discrete entropic OT latent-state** donor, especially for dual-potential/log-scaling prediction.

Strengths:
- clearer dual/log-scaling object than many other candidates,
- explicit pretrained-model and inference surface,
- MIT license is more permissive than the Meta OT README-visible license.

Main adaptation blockers:
- grid/resolution-centric operator input format versus unordered particle clouds,
- synthetic generator is part of the method story and would need a BayesFilter analogue,
- the route is less obviously the narrowest faithful warm-start donor than Meta OT because the representation bridge is larger.

## Side-by-Side Donor Comparison For P2

| Field | Meta OT | UNOT |
| --- | --- | --- |
| Official repo confirmed in BayesFilter ledger | Yes | Yes |
| Visible license from repo page | CC BY-NC 4.0 | MIT |
| Primary framework/runtime signal | JAX + OTT research stack | Python + Torch/FNO-style operator stack |
| Predicted object at paper/note level | single dual half / solver-native dual state | dual-derived latent quantity / log-scaling / dual-potential object |
| Teacher retained after prediction? | Yes; corrective Sinkhorn remains central | Yes; retained discrete entropic OT / corrected Sinkhorn-style deployment remains possible |
| Training vs inference split | clear in concept and repo layout | clear in concept and repo layout |
| Strongest BayesFilter fit | retained-teacher warm-start semantics | discrete entropic dual-potential/operator semantics |
| Main representation risk | exact particle-cloud target-object mapping | much larger grid/resolution-to-particle-cloud bridge |
| Main framework risk | JAX/OTT to TF/TFP translation | Torch/FNO/operator-style to TF/TFP translation |
| Main donor advantage | cleanest retained-correction story | clearer dual/log-scaling operator route and permissive visible license |
| Main donor limitation | licensing / stack / exact runnable-core extraction still unresolved | representation bridge is larger and may force more adaptation sooner |

## Most Supported Interim Reading

1. **Meta OT** is the stronger semantic donor for BayesFilter's retained-teacher chapter definition.
2. **UNOT** is the stronger discrete dual-potential/operator donor if BayesFilter later decides that log-scaling/operator structure is closer to the intended learned object.
3. Neither donor has yet been decomposed enough at the repo-code level to claim BayesFilter has already ported or faithfully mapped it.
4. P2 must now choose one donor and defer the other.

## What P1 Does Not Conclude

P1 does **not** conclude:
- that Meta OT must be the final donor,
- that UNOT is unusable,
- that either donor can be copied directly without a blocker audit,
- that BayesFilter has already achieved source faithfulness,
- that the donor paper results transfer automatically to the annealed LEDH branch.

## Commands / Sources Used

Local sources inspected in the current dialogue:
- `docs/plans/bayesfilter-neural-ot-source-code-availability-ledger-2026-06-18.md`
- `docs/plans/bayesfilter-neural-ot-implementation-fit-note-2026-06-18.md`
- `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex`

External repo pages fetched in the current dialogue:
- [https://github.com/facebookresearch/meta-ot](https://github.com/facebookresearch/meta-ot)
- [https://github.com/GregorKornhardt/UNOT](https://github.com/GregorKornhardt/UNOT)

## Next Step

Advance to P2 donor decision under:
- `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p2-primary-donor-decision-subplan-2026-06-27.md`

P2 must now choose one primary donor route and explicitly defer the other.
