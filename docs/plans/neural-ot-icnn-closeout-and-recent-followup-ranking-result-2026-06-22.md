# Experiment result: OT-ICNN closeout and recent neural-OT follow-up ranking

## Plan reference
- `docs/plans/neural-ot-algorithm-search-reset-memo-2026-06-22.md`
- `docs/plans/recent-neural-ot-code-availability-matrix-2026-06-20.md`
- `docs/plans/recent-neural-ot-survey-expansion-result-2026-06-20.md`

## Command actually run
```bash
No experiment command. This was a document-side closeout and literature-triage pass using existing notes plus direct reading of the local PDFs.
```

## Result summary
- OT-ICNN should be closed as an **unfaithful bridge/direct-map benchmark**, not as a demonstrated failure of the original Makkuva et al. (2020) algorithm.
- The existing BayesFilter negative result applies only to the bridge-style surrogates we actually benchmarked, which did not beat the stronger trivial weighted-mean baseline on the expanded artifact.
- The strongest newer candidates to examine much more seriously are:
  1. **Efficient Neural Network Approaches for Conditional Optimal Transport with Applications in Bayesian Inference** — Wang et al. (2025)
  2. **Conditional Optimal Transport on Function Spaces** — Hosseini, Hsu, Taghvaei (2025)
  3. **Nonlinear Filtering with Brenier Optimal Transport Maps** — Al-Jarrah et al. (2025)
  4. **Universal Neural Optimal Transport (UNOT)** — Geuter et al. (2025)
- GeONet remains interesting, but more as a comparison family than the next primary implementation lane for BayesFilter’s current repeated-OT/filtering bottleneck.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| Faithful OT-ICNN replication status | 0 | No faithful Makkuva-style replication was completed. |
| Bridge benchmark usefulness vs stronger trivial baseline | failed | The tested direct-map bridge variants did not beat weighted-mean repeated on the expanded artifact. |
| Newer papers read directly this pass | 5 | Enough to support a bounded reprioritization, not an exhaustive field-wide ranking. |
| Filtering/Bayesian relevance among top-ranked follow-ups | high | The top 3 newer papers all explicitly target conditional OT, Bayesian inference, or filtering. |

## Engineering observations
- The existing reset memo already preserved the key boundary: we benchmarked executable bridge variants, not a faithful OT-ICNN port.
- The recent local shelf is good enough to rank a next serious reading/implementation queue without adding new sources yet.
- The strongest newer candidates are not all equally code-backed in the current notes, so “scientifically central” and “easiest immediate borrow” remain different rankings.

## Empirical evidence
- Existing BayesFilter notes report that the bridge-style OT-ICNN/direct-map variants underperformed the stronger trivial weighted-mean repeated baseline on the expanded artifact.
- This is empirical evidence against the specific bridge benchmark route that was tried.
- It is not empirical evidence that the original Makkuva et al. minimax ICNN method fails in BayesFilter.

## Mathematical claims
- Makkuva et al. (2020) explicitly formulate OT-map learning through paired convex potentials and a minimax objective, with the learned map recovered as a gradient of a convex function.
- Wang et al. (2025) explicitly target conditional optimal transport maps for Bayesian inference, with both a static conditional Brenier-style map (PCP-Map) and a dynamic conditional OT flow (COT-Flow).
- Hosseini et al. (2025) explicitly formulate conditional OT on function spaces through block-triangular/conditional Monge and Kantorovich problems, aimed at amortized Bayesian inference.
- Al-Jarrah et al. (2025) explicitly formulate nonlinear filtering through Brenier optimal transport maps and show filtering-specific numerical results.
- No claim is made here that any of these newer methods already satisfy BayesFilter’s downstream scalar/gradient or HMC-facing contracts without further derivation and experiment.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Close OT-ICNN lane as an unfaithful benchmark | met | no veto conflict | Whether a faithful TensorFlow OT-ICNN port would behave differently | Do not iterate more bridge variants; archive the lane with a boundary note | Not concluding that original OT-ICNN does not work |
| Promote Wang(25) for serious follow-up | met | none triggered in this document pass | Current code availability/borrowability not yet fully audited from repo side | Write a focused fit note and inspect implementation surfaces | Not concluding it is ready for BayesFilter defaults |
| Promote Hosseini(25) for serious follow-up | met | none triggered in this document pass | Function-space formulation may require a substantial representation bridge to particles | Write a theory-to-BayesFilter fit note before implementation work | Not concluding it is the easiest executable lane |
| Promote Al-Jarrah(25) for serious follow-up | met | none triggered in this document pass | Need to inspect whether the reported filtering OT architecture and assumptions transfer to BayesFilter’s transport object | Write a filtering-specific implementation-fit note | Not concluding its current method is already faithful to our target semantics |
| Keep UNOT in the serious queue | met | prior representation-mismatch caution remains | Variable-resolution/operator framing may still be awkward for particle clouds | Reassess with the newer candidate set in view | Not concluding UNOT should be dropped |

## Pre-mortem
- A newer paper can look central scientifically while still being a poor direct implementation source for BayesFilter.
- A filtering-native paper can still mismatch our exact transport object, scalar semantics, or deployment constraints.
- A strong conditional-OT theory paper can still require a large representation bridge from function-space or diffeomorphic settings to weighted particle clouds.
- A paper with impressive figures can still fail the downstream BayesFilter criterion even if it wins on proxy metrics like sample quality or OT cost.

## Post-run red-team note
- Strongest alternative explanation: the ranking may still overweight Bayesian/filtering relevance relative to direct borrowability into the current TensorFlow/GPU production lane.
- Result that would overturn the present recommendation: a repo-level audit showing one of the top-ranked newer methods has no usable implementation surface, or that another recent family has a much cleaner direct fit to weighted particle-cloud OT.
- Weakest part of the evidence: code-availability for several newer papers remains only partially checked in the current notes.

## Decision
- Close OT-ICNN with the conclusion that we **did not faithfully replicate the original algorithm**, so we should draw **no concrete algorithm-level conclusion** beyond failure of the bridge benchmark we actually ran.
- Reprioritize the recent set toward Wang(25), Hosseini(25), and Al-Jarrah(25), with UNOT still kept in the serious follow-up queue and GeONet treated mainly as a comparison family.

## Next step
- Write a short synthesis/fit note ranking the newer candidates in implementation order, explicitly separating:
  1. scientific centrality,
  2. BayesFilter target match,
  3. code-borrowability,
  4. representation-bridge burden.
