# Neural OT Implementation-Fit Note For BayesFilter

## Date
2026-06-18

## Context

The OT/neural-OT survey phase is complete enough that the next step is
implementation planning.  We now have a source-code availability ledger, but that
ledger only records where code appears to exist.  It does not yet say which
repositories are the best implementation starting points for BayesFilter.

The immediate implementation goal is narrow:

> implement the retained-teacher neural OT route, where a neural network predicts
> a solver-relevant latent object for the retained entropic OT / Sinkhorn teacher,
> and a corrective Sinkhorn phase remains in the loop.

This note therefore compares the code-backed candidate repositories by how well
they fit that implementation target.

## Scope

Primary code-backed candidates reviewed at the note level:
- `Meta OT` — `https://github.com/facebookresearch/meta-ot`
- `UNOT` — `https://github.com/GregorKornhardt/UNOT`
- `OT-ICNN` — `https://github.com/AmirTag/OT-ICNN`
- `FlowOT` — `https://github.com/hamrel-cxu/FlowOT`
- `TrajectoryNet` — `https://github.com/KrishnaswamyLab/TrajectoryNet`

The first two are the main candidates for the retained-teacher implementation
lane.  The last three are useful comparison or secondary-branch sources.

## Evaluation criteria

For BayesFilter’s first implementation pass, the most important fit questions are:
1. Does the code predict a latent teacher object or a final map?
2. Is the predicted object close to the retained entropic OT / Sinkhorn teacher
   we defined in the monograph?
3. Is there a clear training-time versus deployment-time split?
4. How hard is the adaptation to BayesFilter’s TensorFlow / TFP implementation
   conventions likely to be?
5. Does the repository look like a primary implementation source or more like a
   benchmark / research comparison source?

## Implementation-fit comparison

| Candidate | Primary framework | Predicted / learned object | Training vs inference split | Fit to retained-teacher route | Likely BayesFilter adaptation burden |
|---|---|---|---|---|---|
| Meta OT | JAX-based research code (per paper note and repo naming) | OT-relevant latent solution information / amortized optimization state | Clear in concept: training on many OT problems, then inference on new OT problems | **High** | Medium to high. Strong conceptual fit, but likely requires translating JAX implementation patterns into TensorFlow/TFP and adapting from paper task setup to BayesFilter particle-cloud tasks. |
| UNOT | Neural-operator codebase with published model weights | Dual potential / Sinkhorn-relevant discrete OT object | Clear: train operator, then predict OT distances/plans/initializations | **High** | Medium to high. Strong conceptual fit for discrete entropic OT; likely requires adapting operator input representation and translating framework/runtime assumptions into BayesFilter’s stack. |
| OT-ICNN | Direct-map research code | Direct transport map via convex potential | Training/inference split present, but map is the main object | **Moderate** | High. This is a direct-map route, not a retained-teacher acceleration route. Useful as a secondary branch after the main implementation lane, not the first target. |
| FlowOT | Direct flow-based transport code | Learned transport flow / direct transport map | Training/inference split present | **Moderate to low** for the retained-teacher route | High. Conceptually farther from the retained Sinkhorn teacher and likely requires substantial reinterpretation to fit BayesFilter’s declared transport object. |
| TrajectoryNet | Dynamic path / neural ODE code | Dynamic path / trajectory object | Clear for its own scientific task | **Low** for the immediate BayesFilter route | Very high. Useful as a dynamic-path comparison source, but not a natural first implementation source for retained-teacher entropic OT. |

## Ranking for the first BayesFilter implementation pass

### 1. Meta OT
**Best use:** first retained-teacher warm-start implementation study.

Why it fits:
- It is closest in spirit to the question “can we learn how to solve many related
  OT problems faster?”
- The learner targets solver-relevant information rather than replacing the whole
  OT teacher object.
- This matches the monograph’s main implementation-bearing neural chapter.

Main adaptation tasks:
- determine exactly what latent object to predict in BayesFilter
  (dual potentials, scaling vectors, or another initialization object),
- adapt training data generation to BayesFilter-style weighted particle clouds,
- translate the implementation from its original framework assumptions into
  TensorFlow/TFP conventions.

### 2. UNOT
**Best use:** second retained-teacher candidate, especially if we want a more
operator-style discrete OT predictor.

Why it fits:
- It is strongly aligned with the discrete entropic OT / Sinkhorn object itself.
- It predicts OT-relevant structure in a way that is naturally closer to the
  EOT/Sinkhorn layer than direct-map methods are.
- It may be especially useful if the BayesFilter transport layer is treated as a
  family of discrete OT problems over varying particle sets.

Main adaptation tasks:
- decide whether to reuse the dual-potential prediction framing directly,
- design the BayesFilter particle-cloud representation so it matches what the
  operator expects,
- port or reimplement the relevant route in TensorFlow/TFP.

### 3. OT-ICNN
**Best use:** secondary direct-map branch after the retained-teacher route is
scoped.

Why it is not first:
- The learned object is the direct transport map itself, not a warm start for a
  retained teacher.
- That changes the implementation question and the target burden.
- It is still the clearest code-backed direct-map source if we choose to explore
  that branch later.

### 4. FlowOT
**Best use:** dynamic/direct transport comparison source after the main route.

Why it is not first:
- It is farther from the retained entropic OT object.
- It likely requires a more radical reinterpretation of what BayesFilter is
  learning and using at inference time.

### 5. TrajectoryNet
**Best use:** conceptual dynamic-path comparison only.

Why it is not first:
- It is built around a path-learning scientific task that is not the same as the
  current BayesFilter equal-weighting bottleneck.

## Immediate implementation recommendation

For the first implementation pass, do **not** branch widely.  Use a staged policy:

1. **Primary track:** `Meta OT`
   - study exactly what solver-relevant latent object it predicts,
   - map that object to the retained-teacher BayesFilter chapter definition,
   - decide whether BayesFilter should predict duals, scaling vectors, or another
     initialization representation.

2. **Secondary track:** `UNOT`
   - study whether its discrete entropic OT object is closer to our teacher than
     Meta OT’s framing is,
   - especially if we want a more operator-like representation of OT problems over
     particle clouds.

3. **Deferred branches:** `OT-ICNN`, `FlowOT`, `TrajectoryNet`
   - keep for later direct-map or dynamic-path experiments only after the retained-
     teacher route is well specified.

## What this note does not yet establish

This note does **not** yet establish:
- that any repository is easy to run today,
- that any repository is well maintained,
- that any repository has a compatible license,
- that any repository’s exact implementation matches the mathematical variant we
  want in BayesFilter,
- that JAX-to-TensorFlow/TFP adaptation is trivial,
- that the first implementation should copy code rather than reimplement the
  mathematics cleanly.

## Suggested next steps

1. For `Meta OT`, write a **target-object extraction note**:
   - what exact latent variable is predicted,
   - how it maps to the teacher/student chapter equations,
   - what BayesFilter data generation would look like.
2. For `UNOT`, write a **discrete entropic OT fit note**:
   - whether its dual-potential/operator framing is a closer match than Meta OT
     for our teacher object.
3. Then write the first **implementation plan** for the retained-teacher route,
   explicitly choosing between a Meta-OT-style or UNOT-style predicted latent
   object.
