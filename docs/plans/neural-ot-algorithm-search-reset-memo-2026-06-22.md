# Neural OT algorithm search reset memo

## Date
2026-06-22

## Scope of this memo
This memo is for a fresh agent whose only job is to continue the neural-OT / algorithm-selection side of the work.

Do **not** mix this task with OT chapter document repair or PDF page-count debugging. Those are covered by a separate reset memo.

## Executive summary
We explored three main code-backed neural OT directions so far:
1. retained-teacher warm-starts,
2. UNOT,
3. OT-ICNN.

Current result:
- none of the tested code-backed neural routes has yet earned status as a convincing future-default algorithm for BayesFilter’s large-scale batched OT path.

## 1. Retained-teacher warm-start lane
### What was implemented
Implemented successfully:
- fixed-target Sinkhorn warm-start state export/import
- canonicalized latent supervision `(log_u, log_v)`
- minimal DeepSets-style warm-start student
- teacher-data generation and heldout evaluation for scalar route
- batched annealed warm-start plumbing for the streaming GPU lane
- batched teacher-data generation
- batched training pipeline
- 50k GPU benchmark harness support

Important files include:
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py`
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_warmstart_student_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py`

### Family-level scalar-route results
Supported locally:
- LGSSM low-budget effect
- expanded LGSSM low-budget effect
- stochastic-volatility effect after family calibration

Null / no-benefit family result:
- range-bearing retained-teacher route implemented, but no measurable warm-start advantage over zero-init

### Batched GPU result
The decisive 50k batched GPU/TF32 benchmark was negative.

Cold-start vs heuristic vs trained warm-start warm-call median seconds:
- cold-start: ~265.5 s
- heuristic warm-start: ~281.2 s
- trained warm-start: ~326.5 s

Even after a larger dataset, wider model, and longer training, the batched retained-teacher warm-start design did **not** produce a 50k speed win.

### Strongest conclusion for this lane
- scientifically useful research lane,
- valid small/family-specific retained-teacher route,
- **not** a future-default batched 50k performance candidate.

Relevant result note:
- `docs/plans/batched-ledh-pfpf-ot-retained-teacher-warmstart-closeout-2026-06-20.md`
- `docs/plans/batched-annealed-warmstart-training-quality-result-2026-06-20.md`

## 2. UNOT intake
### Intake result
UNOT was not chosen as the next direct code-borrow lane.

Result:
- `UNOT_TOO_GRID_SPECIFIC_USE_OT_ICNN`

Reason:
- public code exists,
- conceptually interesting,
- but the runnable surfaces are too tied to grid/FNO-style representations to be the easiest direct borrow for unordered particle clouds.

Relevant notes:
- `docs/plans/unot-intake-plan-for-bayesfilter-2026-06-20.md`
- `docs/plans/unot-intake-result-for-bayesfilter-2026-06-20.md`

### Interpretation
UNOT remains a strong conceptual reference, but it is not the next easiest executable lane unless we are willing to do a representation bridge.

## 3. OT-ICNN lane
### Intake result
OT-ICNN was judged the most practical next code-backed direct-map family after UNOT.

Result:
- `OT_ICNN_MODERATE_BRIDGE_REQUIRED_BUT_HONEST`

Why:
- direct-map route,
- code-backed,
- less representation mismatch than UNOT,
- but still not a thin drop-in.

### Bridge and ladder results
We then executed:
- an explicit OT-ICNN bridge benchmark
- a comparator ladder on the tiny 7/2 LGSSM artifact
- a more rigorous benchmark on the expanded 13/9 LGSSM artifact

#### Tiny ladder result
- identity mean RMSE: 0.4895
- weighted-mean repeated mean RMSE: 0.1190
- direct_map_bridge mean RMSE: 0.3047

So the bridge beat identity but lost badly to the stronger trivial baseline.

#### Rigorous expanded result
On the expanded 13/9 artifact:
- identity mean RMSE: 0.4506
- weighted-mean repeated mean RMSE: 0.1256
- direct_map_bridge mean RMSE: 0.2792
- stronger OT-ICNN-style candidate mean RMSE: 0.2596

So the stronger candidate still:
- beat identity,
- improved over the weaker bridge,
- but still **did not beat weighted-mean repeated**.

### Strongest conclusion for this lane
The current BayesFilter OT-ICNN work should be closed as a **bridge/direct-map benchmark only**. It shows that the tested bridge-style surrogates did not beat the stronger trivial baseline on the expanded artifact.

### Why this is not a concrete verdict on original OT-ICNN
We still did **not** run a faithful OT-ICNN implementation of:
- paired convex potentials `f,g` trained by the paper's minimax/saddle formulation,
- gradient-of-convex-map inference from the learned convex potential,
- the original ICNN convexity-constrained optimization contract.

Makkuva et al. (2020) is not just "some direct map." The paper's method is specifically a Brenier/ICNN construction with paired convex functions and alternating minimax training; see the paper's dual/minimax formulation and Algorithm 1. Therefore the current negative result is only a negative result for the **bridge benchmark we actually ran**. It is **not** a concrete scientific conclusion that the original OT-ICNN algorithm fails for BayesFilter.

Relevant notes:
- `docs/plans/ot-icnn-intake-plan-for-bayesfilter-2026-06-20.md`
- `docs/plans/ot-icnn-intake-result-for-bayesfilter-2026-06-20.md`
- `docs/plans/ot-icnn-bridge-benchmark-plan-2026-06-20.md`
- `docs/plans/ot-icnn-direct-map-ladder-plan-2026-06-21.md`
- `docs/plans/ot-icnn-direct-map-benchmark-plan-2026-06-20.md`

## 4. Recent-work survey expansion
The newer local shelf and code matrix were expanded to reduce over-focus on OT-ICNN as the central modern direction.

Key artifacts:
- `/.localsource/neural_operator2/`
- `docs/plans/recent-neural-ot-code-availability-matrix-2026-06-20.md`
- `docs/plans/recent-neural-ot-survey-expansion-result-2026-06-20.md`

Important interpretation:
- OT-ICNN is now clearly framed as an older code-backed direct-map baseline,
- not as the obvious main modern direction.

## Current overall conclusion
At this point, the code-backed neural OT search supports the following:
- retained-teacher warm-starts are scientifically useful in controlled small/family-specific settings but not a 50k default-performance win,
- UNOT is too grid-specific for the easiest direct borrow,
- OT-ICNN bridges are executable but currently blocked by weak benchmark performance relative to a stronger trivial baseline,
- and no tested code-backed neural route has yet earned default-candidate status for BayesFilter’s large-scale batched OT path.

## Suggested next options for a fresh agent
A fresh algorithm-search agent should choose explicitly among:
1. stop the current neural-OT search and write a final closure/synthesis note,
2. attempt a **faithful OT-ICNN TensorFlow port** (a larger, more serious task),
3. or reopen the recent-work candidate ranking from `neural_operator2` to identify a newer family to test next.

Most important warning:
- do not keep iterating on the same retained-teacher batched warm-start route,
- and do not keep running OT-ICNN bridge variants without explicitly deciding whether to invest in a faithful OT-ICNN implementation.
