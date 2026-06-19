# Positive-Feature Independent Lane Master Program

Date: 2026-06-20
Owner: current agent
Lane: positive-feature Sinkhorn semantic-replacement

## Status

`POSITIVE_FEATURE_INDEPENDENT_LANE_MASTER_PROGRAM_CREATED`

## Purpose

Take the current-agent positive-feature Sinkhorn semantic-replacement lane to
an independent closeout without waiting for the peer low-rank coupling
solver-route lane.  This program corrects the over-coupled Wave 4 framing:
shared fixture/seed synchronization belongs only to a later coordinator
comparison after both independent lane closeouts exist.

The peer agent owns the low-rank coupling solver-route lane.  This program does
not direct peer-agent execution.

## Entry Context

- Active cross-agent clarification:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-independent-lane-clarification-to-peer-2026-06-20.md`
- Positive-feature audit:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-audit-2026-06-17.md`
- Phase 5 positive-feature prototype result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p05-positive-feature-prototype-result-2026-06-17.md`
- Wave 2 positive-feature result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-positive-feature-result-2026-06-19.md`
- Wave 4 current-lane positive-feature result, retained as current-lane
  evidence only:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-positive-feature-result-2026-06-20.md`
- TensorFlow implementation:
  `experiments/dpf_implementation/tf_tfp/resampling/positive_feature_transport_tf.py`

## Whole-Lane Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the positive-feature Sinkhorn semantic-replacement lane close independently with finite transport objects, focused tests, replicated downstream resampling hard-screen evidence, and explicit nonclaims? |
| Baseline/comparator | Exact weighted input estimates are the downstream reference for the independent hard screen.  Dense/streaming and naive uniform diagnostics are explanatory only.  Peer low-rank artifacts are not inputs. |
| Primary pass criterion | Independent replay checks pass; official independent-lane JSON/Markdown artifact exits with `PASS`, empty hard vetoes, finite shape-valid transported particles, normalized uniform output log weights, finite positive features/scalings, residual and moment thresholds satisfied, and complete run manifest. |
| Veto diagnostics | Missing entry artifacts, nonfinite outputs/features/scalings, nonpositive features, shape mismatch, log-weight normalization residual above `1.0e-10`, residual above `5.0e-2`, weighted-mean error above `3.0e-1`, weighted second-moment error above `1.0`, missing manifest field, unsupported claim, public/default/API edit, or peer-lane dependency. |
| Explanatory diagnostics | Dense-reference deltas, naive uniform errors, candidate-minus-naive deltas, feature count, epsilon, wall time, per-fixture/per-seed rows. |
| Not concluded | No ranking, speedup, superiority, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, or broad scalable-OT selection. |
| Artifact preserving result | Independent master/subplan/result, independent JSON/Markdown diagnostics, focused test output, and final lane closeout. |

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Does the positive-feature semantic-replacement route remain viable enough, on its own evidence, for a later coordinator comparison or larger validation plan? |
| Candidate/mechanism | TensorFlow positive-feature transport with deterministic positive features and scaling updates. |
| Expected failure mode | Valid-looking feature scaling may still distort weighted downstream moments or violate transport residual/log-weight screens. |
| Promotion criterion | "Viable for later validation" only: empty hard vetoes under the independent replay contract. |
| Promotion veto | Any hard veto in the independent artifact prevents lane closeout as viable. |
| Continuation veto | Invalid artifacts, peer dependency, threshold change after results, unsupported claim, public/default/API edit, or required package/network/GPU evidence. |
| Repair trigger | Focused reporting/test bug, manifest path mismatch, localized denominator/residual reporting issue, or missing nonclaim. |
| Explanatory diagnostics | Runtime, per-row moment errors, dense/naive deltas, and feature settings. |
| Must not conclude | No candidate ranking, default selection, speedup, posterior/HMC correctness, or dense Sinkhorn equivalence. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| PF-I0 | Entry Audit And Independent Plan Lock | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-p00-entry-audit-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-p00-entry-audit-result-2026-06-20.md` |
| PF-I1 | Independent Replay And Closeout | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-p01-replay-closeout-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-closeout-result-2026-06-20.md` |

## Phase Advancement Rule

Each phase may start only after:

- its dedicated subplan exists;
- inherited entry conditions are satisfied;
- required local checks pass or a blocker result is written;
- no human-required stop condition is active.

At the end of each phase, the current agent must:

1. run required local checks;
2. write the phase result or close record;
3. draft or refresh the next subplan when one remains;
4. review the next subplan or final closeout for consistency, correctness,
   feasibility, artifact coverage, and boundary safety.

## Stop Conditions

Stop if continuing requires package installation, network fetch, credentials,
GPU evidence, external solver execution, public API/default/export changes,
peer-lane edits, changing thresholds after seeing results, using descriptive
metrics for ranking, or making a forbidden claim.

## Skeptical Plan Audit

| Audit item | Control |
| --- | --- |
| Wrong baseline risk | Exact weighted input estimates are the independent downstream reference; dense/naive diagnostics are explanatory. |
| Proxy promotion risk | Runtime and dense/naive deltas cannot establish speedup, ranking, or correctness. |
| Missing stop condition risk | Stop conditions block peer dependency, public/default edits, threshold changes, and unsupported claims. |
| Unfair comparison risk | No peer comparison occurs in this lane. |
| Hidden assumption risk | Semantic-replacement status and deterministic feature settings are preserved in artifacts. |
| Stale context risk | Entry audit requires current Wave 2/Wave 4 positive-feature artifacts before replay. |
| Environment mismatch risk | TensorFlow diagnostic is CPU-scoped with `CUDA_VISIBLE_DEVICES=-1`; GPU warnings are environment noise only. |
| Artifact-answer mismatch risk | Independent JSON/Markdown answer only positive-feature lane viability under a hard screen. |

Audit decision: `PASSED_FOR_INDEPENDENT_POSITIVE_FEATURE_LANE_EXECUTION`.
