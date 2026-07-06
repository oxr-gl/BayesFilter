# BayesFilter DPF LEDH-PFPF-OT Default Quality Validation Master Program - 2026-06-20

## Status

`COMPLETED_P03_MEDIUM_GPU_QUALITY_SCREEN_PASSED_WITH_NONCLAIMS`

## Objective

Run the next, better validation rung for the promoted GPU-oriented
LEDH-PFPF-OT TF32 default: a paired downstream filter-quality screen on the
current streaming TensorFlow route.

This program tests whether the default `float32` plus TF32 route preserves
downstream filter outputs within a predeclared engineering tolerance relative
to an FP64 reference arm on the same synthetic LGSSM-shaped fixture and paired
seeds.

This is stronger than the completed operational smoke ladder because it checks
the actual filter outputs across paired seeds. It is still not a posterior
correctness proof, not HMC readiness evidence, not a statistical ranking, and
not a scientific claim.

## Research Intent Ledger

| Field | Ledger |
| --- | --- |
| Main question | Does the promoted GPU TF32 streaming LEDH-PFPF-OT default preserve downstream filter outputs within a predeclared tolerance on paired medium LGSSM-shaped runs? |
| Candidate/mechanism | `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py` with `dtype=float32`, TF32 enabled, streaming transport, callback proposal mode, and GPU placement. |
| Comparator | FP64 reference arm with TF32 disabled, plus an FP32 TF32-disabled arm as a diagnostic comparator. |
| Expected failure mode | The default route may stay finite and GPU placed but drift too far from FP64 in log likelihood, filtered means, filtered variances, or ESS. |
| Promotion criterion | The `fp32_tf32_enabled` arm passes every child hard screen and every preserved per-seed/per-output max-relative drift to FP64 is `<= 1.0e-2` across paired seeds in P02. |
| Promotion veto | Child failure, nonfinite output, GPU placement mismatch, missing output arrays, config mismatch across arms, paired-seed count mismatch, missing per-seed/per-output drift fields, missing default precision metadata, or TF32-enabled downstream drift above tolerance. |
| Continuation veto | Broken harness, corrupted artifacts, criteria changed after seeing results, untrusted GPU evidence used as GPU evidence, or Claude/Codex non-convergence after five rounds on the same material blocker. |
| Repair trigger | Fixable artifact/schema mismatch, wrong path, stale title/nonclaim, child timeout at the selected shape, or too-broad Claude prompt. |
| Explanatory diagnostics | Runtime, memory, compile time, warm-call timing, FP32-no-TF32 drift, TF32-vs-no-TF32 extra drift, per-seed drift spread, and child stderr tails. |
| Must not conclude | Posterior correctness, HMC readiness, sampler convergence, statistical superiority, speedup, dense Sinkhorn equivalence, public API readiness, target-shape HMC viability, or rejection of the low-rank peer lane. |

## Phase Index

| Phase | Name | Subplan | Result |
| --- | --- | --- | --- |
| P00 | Governance, evidence contract, and Claude review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p00-governance-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p00-governance-result-2026-06-20.md` |
| P01 | Paired quality harness implementation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p01-harness-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p01-harness-result-2026-06-20.md` |
| P02 | Trusted GPU paired medium quality screen | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p02-medium-gpu-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p02-medium-gpu-result-2026-06-20.md` |
| P03 | Closeout and next-rung handoff | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p03-closeout-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-result-2026-06-20.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific or engineering question | Does the promoted GPU TF32 streaming LEDH-PFPF-OT route preserve downstream LEDH filter outputs in a paired medium quality rung? |
| Exact baseline or comparator | FP64 TF32-disabled streaming arm from the same harness, shape, seed, transport settings, and GPU device; FP32 TF32-disabled is diagnostic. |
| Primary promotion or pass/fail criterion | P02 passes only if every child run passes its hard screen, the parent artifact preserves all per-seed/per-output drift fields and paired-seed count, and the default `fp32_tf32_enabled` arm has max-relative drift to FP64 `<= 1.0e-2` for log likelihood, filtered means, filtered variances, and ESS across all paired seeds. |
| Drift formula | For each output array and paired seed, `max_relative_to_max1_abs_reference = max(abs(candidate - reference) / max(1.0, abs(reference)))`, computed elementwise and maximized over the output array. The shared `1.0e-2` bound is a gross engineering sanity tolerance for this medium synthetic screen only; it is not a metric-specific scientific accuracy threshold. |
| Required default metadata assertions | The `fp32_tf32_enabled` child precision metadata must include `precision_default_policy=production_ledh_pfpf_ot_gpu_tf32`, `default_execution_target=gpu`, `default_algorithm_target=ledh_pfpf_ot_tf32`, `default_target_status=production_default_by_owner_directive`, `default_dtype=float32`, `active_dtype=float32`, `default_tf32_mode=enabled`, `tf32_mode=enabled`, and `tf32_execution_enabled=true`. |
| Diagnostics that can veto | Nonzero child exit, missing child artifact, nonfinite output, missing output arrays, mismatched fixture config, GPU placement mismatch, paired-seed count mismatch, missing per-seed/per-output drift fields, missing/default precision metadata mismatch, or TF32-enabled drift above tolerance. |
| Diagnostics that are explanatory only | Runtime, memory, compile time, warm timing, FP32-no-TF32 drift, TF32-vs-no-TF32 extra drift, and individual drift magnitudes below the hard threshold. |
| Not concluded even if the run passes | No posterior correctness, no HMC readiness, no sampler convergence, no statistical superiority, no speedup, no dense Sinkhorn equivalence, no public API readiness, and no target-shape scientific validity. |
| Artifact preserving result | P02 JSON/Markdown artifacts under `docs/benchmarks`, phase result under `docs/plans`, and the visible execution/review ledgers. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Streaming benchmark route | `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py` | It is the current GPU TF32 default route tested in the completed default-impact ladder. | Testing an obsolete path would not answer the current default question. | P01 imports and launches the existing streaming precision wrapper. | planned |
| FP64 arm as reference | Existing precision wrapper and P02 default-impact result | Gives a same-fixture high-precision comparator. | FP64 on GPU is still a numerical arm, not an exact Kalman oracle. | Nonclaims and result language preserve the boundary. | planned |
| Paired seeds | Research policy and existing PF MC harness pattern | Keeps each precision comparison on the same fixture seed. | Few seeds cannot support ranking. | Inference table must state no statistical ranking. | planned |
| Tolerance `1.0e-2` max-relative drift | Completed P02 used the same gross-drift sanity bound; formula is `max(abs(candidate-reference)/max(1,abs(reference)))` | Makes the rung an engineering quality screen, not a proof. | Tolerance could be too loose for future scientific claims. | Result records it as a screen only and preserves per-seed/per-output maxima. | planned |
| Medium shape first | Prior target-shape smoke was long and single-seed | Avoids running a long target-shape ladder before verifying the paired-quality harness. | Medium shape may not expose target-shape failure. | P03 must draft the next target-shape repeated stability subplan. | planned |

## Skeptical Plan Audit

- Wrong baseline: controlled by comparing each candidate arm against a paired
  FP64 arm from the same streaming harness, shape, seed, and GPU device. The
  plan does not claim FP64 equals exact posterior truth.
- Proxy metrics: timing, memory, and FP32-no-TF32 drift are explanatory only.
  The primary criterion is downstream output drift for the default arm plus
  hard child validity screens.
- Missing stop conditions: every subplan has stop conditions, and P02 stops on
  child failure, stale metadata, GPU placement mismatch, or drift above the
  predeclared tolerance.
- Unfair comparisons: arms run in fresh Python child processes and reuse the
  existing precision wrapper, preventing TensorFlow precision settings from
  leaking across arms.
- Hidden assumptions: GPU evidence must be trusted/elevated; sandbox GPU
  failure is not interpreted as machine failure.
- Stale context: unrelated dirty HMC files and peer low-rank artifacts are out
  of scope and must not be modified or interpreted.
- Artifact mismatch: P02 must preserve parent JSON/Markdown artifacts, child
  artifacts, per-seed/per-output drift records, paired seed count, exact
  tolerance formula, default metadata assertions, and actual commands.

Audit status: P00 passed after Claude read-only review round 2. Round 1 found
fixable evidence-contract gaps around per-seed/per-output drift records, drift
formula, default metadata assertions, and closeout evidence carry-forward. Those
gaps were patched and Claude returned `VERDICT: AGREE`.

## Repair Loop

For material Claude findings, Codex patches the same artifact visibly, reruns
focused local checks, and repeats read-only Claude review up to five rounds for
the same blocker. Claude is not an execution authority and cannot authorize
crossing human, runtime, model-file, funding, product-capability,
default-policy, or scientific-claim boundaries.
