# P3 Result: Minimal Source-Faithful Port Or Decomposition

Date: 2026-06-27

## Status

`PASS_P3_DONOR_CORE_DECOMPOSED_READY_FOR_P4`

## Decision

`PASS_P3_DONOR_CORE_DECOMPOSED_READY_FOR_P4`

BayesFilter now has a minimal donor-core decomposition for the chosen primary donor, **Meta OT**.

The narrowest retained-teacher donor-core route is the **discrete Meta OT path** implemented by:
- `train_discrete.py`
- `meta_ot/models.py`
- `meta_ot/data.py`
- the discrete evaluation/corrective path in `eval_discrete.py`

This decomposition is sufficient to state what must be preserved for a source-faithful first adaptation and what is merely experiment shell.

However, the donor repo also exposes an immediate blocker for any direct code import or code-translation path into BayesFilter: the visible repo license is **CC BY-NC 4.0**, which requires a separate human license/reuse decision before code-level porting beyond read-only decomposition.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter port or faithfully decompose the narrowest runnable retained-teacher route from the chosen donor repo before creating further custom neural-OT machinery? |
| Baseline/comparator | The chosen donor from P2 and its source-anchor audit from P1. |
| Primary pass criterion | A result artifact identifies the minimum donor-core path, separates donor-core logic from donor benchmark scaffolding, and records the first runnable/reconstructible retained-teacher route. |
| Veto diagnostics | Starting with a BayesFilter-specific redesign before donor decomposition; no donor-component map; no distinction between source core and benchmark shell. |
| Explanatory diagnostics | Dependency friction, helper modules, data loaders, and optional performance code. |
| Not concluded | P3 does not yet declare BayesFilter adaptation complete. |

## Donor-Core Route Identified

### Core retained-teacher mechanism
The narrowest donor-core retained-teacher mechanism in Meta OT is:

1. sample a discrete entropic OT problem `(a,b)` from a repeated problem distribution,
2. hold a fixed entropic geometry / cost object,
3. predict a **single dual half** `f_pred` from `(a,b)`,
4. recover the complementary dual half `g_pred` using the teacher-side update rule,
5. train the predictor by the teacher's own dual objective,
6. deploy by using `(f_pred, g_pred)` as a warm start for a corrective Sinkhorn solve.

This is the minimal retained-teacher route BayesFilter must preserve if it wants a source-faithful Meta OT adaptation.

## Donor Component Map

| Donor component | Source path | Role in donor route | Core or shell? |
| --- | --- | --- | --- |
| Discrete training entry point | `/tmp/meta-ot/train_discrete.py` | Drives the discrete Meta OT training loop | Core orchestration |
| Potential predictor | `/tmp/meta-ot/meta_ot/models.py` (`PotentialMLP`) | Predicts the donor latent object `f_pred` | Core method |
| Pair samplers and entropic geometry | `/tmp/meta-ot/meta_ot/data.py` | Creates repeated OT problems and the fixed geometry/cost object | Core method support |
| Objective-based training loss | `/tmp/meta-ot/train_discrete.py` (`dual_obj_from_f`, `dual_obj_loss`) | Trains by the teacher objective rather than only supervised labels | Core method |
| Complementary dual recovery | `/tmp/meta-ot/train_discrete.py` (`g_from_f`) | Recovers `g` from `f` using the teacher update rule | Core method |
| Corrective teacher deployment | `/tmp/meta-ot/eval_discrete.py` (`run_meta`) | Uses predicted duals as Sinkhorn initialization and runs the corrective teacher solve | Core method |
| Hydra config | `/tmp/meta-ot/conf/train_discrete.yaml` | Experiment configuration | Shell / scaffolding |
| Logging, plotting, videos | `eval_discrete.py` plotting sections, `plot_*.py`, `create_video_*.py` | Analysis and visualization | Shell / scaffolding |
| Color-transfer path | `train_color_meta.py`, `eval_color.py` | Separate donor experiment family | Out of current scope |
| Continuous / conjugate / ICNN utilities | `meta_ot/conjugate.py`, `MetaICNN` in `models.py` | Other donor route families | Out of current scope for first retained-teacher closure |

## What The Donor-Core Actually Learns

The donor-core learned object for the discrete route is a **single dual half** `f_pred`, produced by `PotentialMLP` from the problem representation `(a,b)`.

The complementary dual state is not freely learned as a second independent output. It is recovered teacher-consistently by `g_from_f(...)` through the geometry-side potential update.

This is an important closure point for BayesFilter:
- the donor-core route is not “predict both arbitrary dual vectors,”
- it is not “predict the final transport plan,”
- and it is not “predict the final answer and skip correction.”

## Training / Deployment Split From The Donor-Core

### Training
In `train_discrete.py`, the discrete donor-core route:
- samples batches of repeated OT problems,
- predicts `f_pred`,
- evaluates the teacher-side dual objective through `dual_obj_loss`,
- and updates the model parameters with JAX/Flax/Optax.

This is an **objective-based** retained-teacher training route, not a simple label-regression-only route.

### Deployment
In `eval_discrete.py`, the discrete donor-core route:
- predicts `f_pred`,
- reconstructs `g_pred`,
- initializes Sinkhorn with `(f_pred, g_pred)`,
- and runs a corrective Sinkhorn solve (`run_meta`).

This preserves the retained-teacher semantics required by BayesFilter's chapter definition.

## Core vs Shell Boundary

### Core that must be preserved for a faithful first adaptation
- repeated discrete OT problem distribution,
- fixed teacher-side entropic geometry,
- single-dual prediction,
- teacher-side complementary dual recovery,
- objective-based teacher loss,
- corrective Sinkhorn deployment.

### Shell that should not define BayesFilter architecture
- Hydra experiment scaffolding,
- donor plotting/video scripts,
- donor-specific MNIST/world/color experiment shell,
- non-discrete donor branches not needed for the first retained-teacher closure path.

## Blocker Checks Answered

### 1. Exact donor-core object
Answered: the discrete donor-core predicts a **single dual half** `f_pred`.

### 2. Complementary-state recovery path
Answered: `g_from_f(...)` recovers the complementary dual half via the teacher-side geometry update.

### 3. Corrective teacher closure path
Answered: `eval_discrete.py` warm-starts Sinkhorn with the predicted dual state and still runs the corrective teacher solve.

### 4. Core vs benchmark separation
Answered: `train_discrete.py`, `meta_ot/models.py`, `meta_ot/data.py`, and the warm-start/corrective parts of `eval_discrete.py` are the relevant donor core; plotting/video/color branches are shell or out of scope.

### 5. License / runability blocker check
Answered enough to expose a blocker:
- the visible repo license is **CC BY-NC 4.0**,
- the donor stack is JAX/OTT-based,
- so direct code reuse or translation into BayesFilter requires an explicit human license/reuse decision.

The donor is readable and decomposable, but direct code-port execution is not something BayesFilter should assume is already cleared.

## Practical Consequence For BayesFilter

The first source-faithful BayesFilter adaptation target should preserve the donor-core logic above before reopening:
- the earlier BayesFilter-native dual-pair route,
- the later annealed four-potential route,
- or other custom retained-teacher inventions.

In particular, if BayesFilter adapts Meta OT faithfully first, the default target should be:
- a **single dual-half retained-teacher route**,
- not a custom two-half or four-potential redesign on day one.

## What P3 Does Not Conclude

P3 does **not** conclude:
- that the donor code may be copied directly into BayesFilter,
- that the donor license is already cleared for code porting,
- that the discrete donor route is already adapted to BayesFilter particle clouds,
- or that the annealed LEDH route is already covered by the donor-core decomposition.

P3 only identifies the faithful donor-core route and the blocker boundary for actual code-level porting.

## Next Step

Advance to P4 adapter design under:
- `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p4-adapter-design-subplan-2026-06-27.md`

P4 must now define the narrowest BayesFilter adapter that preserves the Meta OT donor-core semantics while explicitly classifying every change as `fixed_adaptation` or `extension_or_invention`.
