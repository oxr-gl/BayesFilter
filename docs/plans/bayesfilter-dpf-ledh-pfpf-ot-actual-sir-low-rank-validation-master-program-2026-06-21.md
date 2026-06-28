# Actual-SIR Low-Rank LEDH/PFPF-OT Validation Master Program

Date: 2026-06-21

Status: `STOPPED_TUNING_REQUIRED_AFTER_P03`

Supervisor/executor: Codex in this conversation.

Claude role: read-only reviewer only. Claude cannot authorize crossing human,
runtime, model-file, funding, product-capability, default-policy, public API, or
scientific-claim boundaries.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can the low-rank coupling solver route make actual-SIR d18 LEDH/PFPF-OT more efficient on paired feasible actual-SIR rows, and can it extend the executable envelope toward `N=50000` to `N=100000` without validity vetoes? |
| Candidate/mechanism | Replace the per-step streaming OT resampling route with the existing TensorFlow low-rank solver-route resampler in an actual-SIR d18 validation harness. |
| Comparator | Existing streaming TF32/GPU actual-SIR route from `docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py`. |
| Existing high-N anchor | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n50000-chunk2048-2026-06-18.md`. |
| Expected failure mode | Low-rank route may run but fail paired comparability, factor diagnostics, route-fired evidence, runtime benefit, or large-N feasibility. |
| Promotion criterion | `LOW_RANK_ACTUAL_SIR_D18_EFFICIENCY_SUPPORTED_BOUNDED` requires valid actual-SIR route evidence, at least two adjacent paired feasible rows with no hard vetoes, paired comparability pass, and predeclared warm-time evidence. Same-row timeout-boundary evidence may support only a resource-boundary addendum after at least two adjacent smaller paired rows pass validity/comparability. Low-rank-only `N=50000/100000` rows can support only executable-envelope language unless streaming also runs or times out under the same predeclared row policy. |
| Promotion veto | Nonfinite outputs; GPU/TF32 mismatch for GPU claim; missing actual-SIR semantics; route fallback; dense `N x N` materialization in low-rank; invalid low-rank factors; paired comparability failure for rows used in the claim. |
| Continuation veto | Shared contract/API change required; package install/network/POT required; trusted GPU context unavailable for GPU evidence; corrupted artifacts; benchmark commands cannot preserve artifacts answering the research question. |
| P03 stop/handoff rule | The P03 subplan is the controlling phase handoff: advance to P04 only if P03 produces a valid paired basis for large-N continuation; if low-rank runs but paired comparability or practical resource evidence fails on an attempted required P03 paired row, stop as `TUNING_REQUIRED` unless a reviewed repair is already in scope. |
| Repair trigger | Fixable harness bug, missing diagnostic, malformed Claude prompt, or bounded threshold/reporting issue that does not require changing the research question after seeing results. |
| Explanatory diagnostics | Runtime, memory, compile time, warm-call time, ESS values, log-likelihood deltas, filtered-summary deltas, projection iterations, and factor residual magnitudes outside hard thresholds. |
| Not concluded | No posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or statistically supported ranking. |

## Predeclared Gates And Thresholds

These gates are engineering validity/comparability screens only. They do not
establish posterior correctness or scientific adequacy.

| Gate | Threshold / protocol | Role |
| --- | --- | --- |
| Finite outputs | log likelihood, filtered means, filtered variances, ESS, final particles, final log weights all finite | hard veto |
| Actual-SIR semantics | row id `zhao_cui_spatial_sir_austria_j9_T20`; `D=18`, `M=9`; actual callback metadata present | hard veto |
| Route-fired evidence | active resampling invocation count equals active mask count for each executed route | hard veto |
| Low-rank nonmaterialization | every low-rank transport matrix shape ends in `[0, 0]` and `transport_matrix_materialized == false` | hard veto |
| Low-rank factor validity | all factors finite; `Q,R >= 0`; `g > 0`; max factor marginal residual `<= 5e-3` | hard veto |
| Log-weight normalization | final log-sum-exp residual `<= 1e-5` | hard veto |
| ESS floor | ESS fraction min `>= 0.01` | hard veto |
| Paired log-likelihood agreement | max absolute per-seed delta `<= 10.0` and mean absolute per-seed delta `<= 5.0` | paired comparability veto |
| Paired filtered-mean agreement | relative L2 over all filtered means `<= 0.20` or absolute RMS `<= 2.5` state units | paired comparability veto |
| Paired filtered-variance agreement | relative L2 over all filtered variances `<= 0.75` or absolute RMS `<= 25.0` squared-state units | paired comparability veto |
| Paired final-particle mean agreement | final state-mean relative L2 `<= 0.20` or absolute L2 `<= 25.0` | paired comparability veto |
| Warm-time protocol | compile/first call recorded separately; P03 speed screen uses exact `warmups=1`, `repeats=3`, same route/physical GPU UUID/dtype/shape/seeds, and the median of those three post-warmup calls | promotion screen |
| Warm-time improvement | streaming warm median / low-rank warm median `>= 1.25` on at least two adjacent paired rows that pass comparability | bounded efficiency support |
| Timeout boundary | P03/P04 timeout-boundary commands use exact outer wall-clock timeout `3600s` per route-row command, measured from process launch and including TF import, compile/first call, warmups/repeats, diagnostics, and artifact writes. Streaming timeout evidence is usable only if low-rank passes the same `B,T,N,seeds,dtype,TF32,physical GPU UUID` under the same timeout. A timeout row cannot supply same-row paired comparability and is resource-boundary evidence only, not posterior/comparability evidence. |
| Memory | recorded as explanatory unless a later reviewed plan declares a memory screen | explanatory only |
| Large-N executable timing | P04 low-rank-only envelope rows may use exact `warmups=0`, `repeats=1`; these timings are executable-envelope diagnostics, not paired speed evidence | explanatory only |
| GPU provenance | GPU artifacts must record requested `CUDA_VISIBLE_DEVICES`, selected physical GPU index, GPU name, GPU UUID when available, `nvidia-smi` status, logical TensorFlow device names, and explicit fallback status. Any paired row used for promotion must run streaming and low-rank on the same physical GPU UUID; otherwise that row is explanatory-only or must be rerun. | hard veto for GPU claims |

## Source Anchors

- Actual-SIR workload harness:
  `docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py`.
- Actual-SIR existing high-N feasibility result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n50000-chunk2048-2026-06-18.md`.
- Low-rank solver route:
  `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`.
- Prior low-rank efficiency result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-result-2026-06-21.md`.
- Visible gated execution template:
  `/home/ubuntu/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`.

## Owned Write Set

- `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`
- `tests/test_actual_sir_low_rank_route_validation.py`
- `docs/benchmarks/actual-sir-low-rank-route-validation-*.json`
- `docs/benchmarks/actual-sir-low-rank-route-validation-*.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-*.md`

## Forbidden Writes

- BayesFilter public exports.
- Shared schema, shared ledger, or unrelated stop handoff files.
- Existing actual-SIR benchmark source except read-only use.
- Existing low-rank solver source except read-only use.
- Agent A/Nystrom/positive-feature artifacts.
- Model files, package metadata, or dependency lock files.

## Algorithm Classification

| Component | Classification | Notes |
| --- | --- | --- |
| `Q diag(1/g) R^T` factor form | `source_faithful` for the anchored factor form only | Existing solver diagnostics report this component. |
| Lazy low-rank apply | `source_faithful` for factor application only | Must not claim dense Sinkhorn equivalence. |
| Factor marginal diagnostics | `source_faithful` | Diagnostics are hard gates. |
| Dykstra-style projection | `source_faithful` only as mirrored by existing solver route diagnostics | Do not upgrade the whole solver to source-faithful. |
| Deterministic rank/grid/floors/schedules | `fixed_hmc_adaptation` | Tuned/fixed implementation choices. |
| Simplified objective/update/stabilization | `extension_or_invention` | Cannot close source-faithfulness gap. |

## Phase Index

| Phase | Name | Subplan | Required result |
| ---: | --- | --- | --- |
| 0 | Governance and skeptical audit | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p00-governance-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p00-governance-result-2026-06-21.md` |
| 1 | Harness integration | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p01-harness-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p01-harness-result-2026-06-21.md` |
| 2 | Tiny actual-SIR route smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p02-smoke-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p02-smoke-result-2026-06-21.md` |
| 3 | Paired actual-SIR ladder | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p03-paired-ladder-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p03-paired-ladder-result-2026-06-21.md` |
| 4 | Large-N actual-SIR envelope | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p04-large-n-envelope-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p04-large-n-envelope-result-2026-06-21.md` |
| 5 | Closeout and claim classification | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p05-closeout-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-result-2026-06-21.md` |

## Skeptical Plan Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: comparator is the existing streaming actual-SIR route, not synthetic LGSSM. |
| Proxy metrics promoted | Guarded: runtime/memory are promotion evidence only after validity and paired comparability gates. |
| Missing stop conditions | Guarded by phase-specific stop conditions and continuation vetoes. |
| Unfair comparison | Guarded: paired rows must use same seeds, observations, callbacks, dtype, TF32 mode, physical GPU UUID, and shape. |
| Hidden assumptions | Guarded: low-rank route is diagnostic semantic replacement; no dense Sinkhorn equivalence. |
| Stale context | Guarded: source anchors and existing result paths are explicit and must be rechecked in Phase 0. |
| Environment mismatch | Guarded: GPU claims require trusted GPU context, TF32 recorded true, GPU output devices, and physical GPU provenance in the artifact manifest. |
| Artifact mismatch | Guarded: each command must write JSON/Markdown artifacts with route, semantics, diagnostics, and manifest. |

Audit conclusion: the plan may proceed to review and Phase 0. Material
benchmark execution remains blocked until the harness exists and Phase 2 smoke
passes.

## Phase Outcome Labels

- `LOW_RANK_ACTUAL_SIR_D18_EFFICIENCY_SUPPORTED_BOUNDED`
- `EXECUTABLE_ENVELOPE_ONLY`
- `TUNING_REQUIRED`
- `REJECT_CURRENT_ROUTE`
- `BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED`

## Claude Review Protocol

Claude prompts must send paths only. Claude may read the master program and
same-prefix `docs/plans` paths named inside it for read-only review. Claude must
end with exactly `VERDICT: AGREE` or `VERDICT: REVISE`. If Claude does not
respond, Codex must run a small probe; if the probe responds, redesign the
review prompt and retry. Stop after five review rounds for the same blocker.
