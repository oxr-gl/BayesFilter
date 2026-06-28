# Actual-SIR Low-Rank Repair Classification Result

Date: 2026-06-22
Status: `BOTH_REPAIRS_ROUTE_PERFORMANCE_FIRST_HANDOFF`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Final classifier is `BOTH_REPAIRS`. The prior tuning P03 artifact set contains a route-performance repair signal for comparable-but-slow candidates and a tuning/comparability/ESS repair signal for the rest. The next smallest safe program is route-performance-first because classification P02 found source-supported timing asymmetry. |
| Primary criterion status | Passed: P01 artifact classifier and P02 code-path classifier both wrote preserved results; P03 microprobe was not needed. |
| Veto diagnostic status | No missing artifacts, stale source anchors, unsupported promotion claim, route-internal edit, or GPU/runtime requirement occurred in the classification program. |
| Main uncertainty | The route-performance repair may fail or require solver-internal changes; tuning/comparability/ESS repair remains open even if route overhead is repaired. |
| Next justified action | Launch only the dedicated route-performance repair subplan after review; do not run held-out support or earlier P04/P05/P06. |
| What is not concluded | No speedup, candidate freeze, held-out support, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, production readiness, or statistical ranking. |

## Phase Evidence

| Phase | Result | Artifact |
| --- | --- | --- |
| P00 | Governance launch passed | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p00-governance-result-2026-06-22.md` |
| P01 | Artifact classifier: `BOTH_REPAIRS_NEEDS_SOURCE_INSPECTION` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p01-artifact-classifier-result-2026-06-22.md` |
| P02 | Code-path classifier: `ROUTE_TIMING_ASYMMETRY_SUPPORTED` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p02-code-path-classifier-result-2026-06-22.md` |
| Classification P03 | Conditional microprobe not launched | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p03-conditional-microprobe-result-2026-06-22.md` |

Prior tuning P03 source artifact:
`docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22.json`

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Supported only for two P03 candidates hard-vetoed on `low_rank:ess_fraction_min_threshold`. |
| Statistically supported ranking | Not supported. P03 was one tuning seed/shape with no uncertainty analysis. |
| Descriptive-only differences | Comparable candidates were descriptively about 54x to 73x slower than streaming on warm median; this is classification evidence, not speedup/superiority evidence. |
| Route timing asymmetry | Supported by source anchors: streaming has compiled-core timing, low-rank uses diagnostic loop and eager diagnostics. |
| Default-readiness | Not supported. |
| Next evidence needed | A reviewed route-performance repair/probe result, followed by a separate tuning/comparability/ESS repair subplan if route overhead is reduced or isolated. |

## Why `BOTH_REPAIRS`

P01 artifact evidence from the prior tuning P03 Stage A artifact set:

- `7` comparable-but-slow candidates.
- `11` incomparable candidates.
- `2` ESS hard-vetoed candidates.
- `0` freeze-nominated candidates.

Classification P02 source evidence:

- The streaming comparator uses an XLA compiled-core timing path.
- The low-rank route is timed through a diagnostic loop and diagnostic solver.
- The low-rank solver has eager `.numpy()` diagnostics and a Python break on a
  tensor-valued projection error.

Therefore, the performance lane is real enough to repair next, but the tuning
lane remains real: route repair alone would not make incomparable or ESS-vetoed
candidates freeze-eligible.

## Next Handoff

Next subplan:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-route-performance-repair-subplan-2026-06-22.md`

Boundary:

- This next subplan is not launched by this result.
- It must be reviewed before execution.
- It must not edit low-rank solver internals unless a later reviewed
  implementation subplan authorizes that boundary.
- It must preserve the tuning/comparability/ESS repair lane in any result.

## Nonclaims

- No candidate was nominated or frozen.
- No held-out support was run.
- No speedup claim is supported.
- No posterior correctness claim is supported.
- No HMC readiness claim is supported.
- No public API/default readiness claim is supported.
- No dense Sinkhorn equivalence claim is supported.
- No production readiness claim is supported.
- No statistical ranking is supported.
