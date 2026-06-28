# Low-Rank LEDH/PFPF-OT TF32 Efficiency Validation Master Program

Date: 2026-06-21

Status: `DRAFT_REVIEW_REQUIRED_ROUND_2`

## Purpose

This program tests whether the low-rank solver-route integration makes the
LEDH/PFPF-OT TF32 filtering route more efficient for very large particle
counts.  It is not another route-fired diagnostic.  The target claim is
bounded:

> Under a shared synthetic LGSSM-shaped LEDH/PFPF-OT benchmark, the low-rank
> route materially reduces transport resource proxies relative to the current
> streaming TF32 route only at sizes where both routes are paired on the same
> GPU, with matching TF32 state and bounded output-comparability checks.  Rows
> beyond the last completed streaming comparator are executable-envelope
> evidence only, not evidence of superiority over streaming at that size.

Codex in this conversation is the supervisor and executor.  Claude is a
read-only reviewer only.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can the low-rank route make LEDH/PFPF-OT TF32 more efficient for large particle counts? |
| Mechanism under test | Replace all-pairs/dense transport work with `P = Q diag(1/g) R^T` lazy low-rank resampling in the LEDH/PFPF-OT filter loop. |
| Baseline/comparator | Existing TF32 streaming LEDH/PFPF-OT route on the same harness, same physical GPU, same `CUDA_VISIBLE_DEVICES`, same TF32 state, same synthetic fixture, and same row timeout.  Dense is used only for tiny sanity if needed.  Low-rank-only `N=50000/100000` rows are unpaired executable-envelope evidence, not streaming superiority evidence. |
| Candidate | Low-rank integration route using the prior selected setting `rank=16`, `assignment_epsilon=0.015625`, unless P01 tuning repair is explicitly triggered. |
| Primary promotion criterion | For a bounded resource-proxy efficiency claim, at least two adjacent paired sizes in the upward ladder must pass validity, bounded output-comparability, TF32 parity, and same-GPU gates for both routes, and low-rank must show either `>=2x` lower peak allocator delta or `>=1.25x` lower warm-call median against streaming.  If streaming reaches a fixed timeout/OOM/failure at a predeclared ladder row while low-rank completes that same row without hard veto, the result supports executable-envelope improvement for that row only. |
| Promotion veto | Any candidate hard validity failure; bounded output-comparability failure for a row used in an efficiency claim; missing route-fired evidence; invalid comparator artifact; GPU not trusted; TF32 mismatch or disabled TF32 for TF32 claims; mixed physical GPU within a paired claim; unsupported public/default/API/HMC/posterior claim; or insufficient paired evidence for an efficiency claim. |
| Continuation veto | Shared harness cannot run both routes on a common fixture at small sanity size; GPU1 and GPU0 both unavailable in trusted context; commands would require network/package/POT/external solver; or needed change crosses shared contract/public default boundary. |
| Repair trigger | Harness mismatch or missing metrics triggers implementation repair; no viable low-rank row at small sanity size triggers bounded tuning repair; GPU1 busy before phase start triggers fallback to GPU0 with manifest note; GPU fallback mid-phase invalidates paired rows already collected for that phase and requires restart or bounded blocker. |
| Explanatory diagnostics | Runtime, peak/current GPU allocator deltas, wall time, compile time, ESS, finite outputs, route invocation counts, and memory info that are not part of a predeclared pass/veto criterion. |
| Not concluded | No posterior correctness, dense Sinkhorn equivalence, HMC readiness, public API readiness, production/default readiness, broad scalable-OT selection, statistical ranking beyond the predeclared paired screen, or 50k/100k streaming superiority unless streaming is actually paired at those sizes. |

## Source And Implementation Boundaries

Owned files for this program:

- `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py`
- `tests/test_low_rank_ledh_pfpf_efficiency.py`
- `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-*.json`
- `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-*.md`
- `docs/benchmarks/logs/low-rank-ledh-pfpf-efficiency-*.log`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-*.md`

Read-only anchors:

- `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_integration_smoke.py`
- `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`

Forbidden edits:

- BayesFilter public exports/defaults/package metadata;
- shared ledgers, shared stop handoffs, shared schema artifacts;
- positive-feature lane artifacts;
- Agent A Nystrom artifacts;
- low-rank integration result artifacts except as read-only context.

## Fixed Efficiency And Validity Criteria

These criteria are fixed before execution and may not be widened after seeing
results.

| Diagnostic | Threshold | Role |
| --- | ---: | --- |
| Low-rank active route invocations | `> 0` and equal to active mask count | hard veto |
| Low-rank transport matrix shape | sentinel `[B, 0, 0]` | hard veto if materialized in scale rows |
| All outputs finite | `true` | hard veto |
| Low-rank factor residuals | `<= 5.0e-3` | hard veto |
| Output log-weight normalization | `<= 1.0e-6` | hard veto |
| TF32 state | enabled and identical for both routes in paired GPU rows | hard veto for TF32 efficiency claim |
| Same physical GPU | one physical GPU for every row contributing to a paired claim | hard veto; restart phase if fallback happens mid-phase |
| Paired ladder | `[1024, 2048, 4096, 8192, 16384, 32768, 50000, 100000]`, stopping streaming after first predeclared timeout/OOM/failure and treating larger rows as unpaired unless streaming is explicitly completed | required for large-N efficiency question |
| Paired row timeout | `900s` wall time per route per `N` in P02; timeout is a recorded row outcome, not an implementation failure by itself | hard boundary against post-hoc timeout choices |
| Large-N low-rank row timeout | `1200s` wall time per row in P03 | hard boundary against post-hoc timeout choices |
| Output-comparability gate | same output tensor shapes, finite output summaries for both routes, log-weight normalization `<= 1.0e-6`, ESS fraction `>= 0.01` for both routes, and low-rank-vs-streaming state-mean proxy relative L2 `<= 0.5` or absolute L2 `<= 1.0` for rows used in an efficiency claim | hard veto for efficiency claim; not posterior correctness |
| Feasible paired sizes | at least two adjacent sizes from the paired ladder if streaming completes | required for speed/memory claim |
| Memory improvement screen | low-rank peak allocator delta at least `2x` lower than streaming median/proxy on at least two adjacent feasible sizes | efficiency support |
| Speed improvement screen | low-rank warm-call median at least `1.25x` lower than streaming on at least two adjacent feasible sizes | efficiency support |
| Executable-envelope screen | streaming fails/OOM/times out at a predeclared size where low-rank passes | envelope support for that size |
| Large low-rank-only rows | `50000`, `100000` | unpaired large-N envelope evidence only |
| Runtime/memory without paired screen | descriptive only | no promotion by itself |

## GPU Selection Rule

Use trusted/elevated GPU context.  Prefer GPU1 by setting
`CUDA_VISIBLE_DEVICES=1`; use GPU0 only if GPU1 is busy, unavailable, or
unsuitable, and record the fallback reason in the run manifest.  All rows used
for one paired claim must run on the same physical GPU.  If the selected GPU
changes mid-phase, paired rows from the old GPU are invalid for that phase and
the phase must restart on one GPU or write a bounded blocker.

## Phase Index

| Phase | Name | Subplan | Result |
| --- | --- | --- | --- |
| P00 | Governance, plan review, and GPU selection preflight | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p00-governance-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p00-governance-result-2026-06-21.md` |
| P01 | Common efficiency harness and small sanity checks | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p01-harness-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p01-harness-result-2026-06-21.md` |
| P02 | Feasible-N paired GPU efficiency screen | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p02-paired-gpu-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p02-paired-gpu-result-2026-06-21.md` |
| P03 | Large-N low-rank executable-envelope ladder | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p03-large-n-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p03-large-n-result-2026-06-21.md` |
| P04 | Final efficiency closeout and claim audit | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p04-closeout-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-result-2026-06-21.md` |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Common harness instead of reusing separate prior harnesses directly | Existing harnesses use different fixture/execution details | Needed for fair efficiency evidence | Harness diverges from production-like streaming route | Small sanity and source-anchor checks | planned |
| Streaming route as primary comparator | Current default scalable route avoids dense storage but keeps all-pairs OT compute | Fairer than dense at feasible sizes | Streaming may still be too slow at high N | Paired feasible-N screen with timeouts | planned |
| Dense route only tiny sanity if used | Dense `[N,N]` memory wall | Avoids unfair/impossible comparator | Dense absence misread as superiority | Explicit comparator boundary | planned |
| GPU1 preferred | User instruction in this conversation, inlined here as an operative rule | Keeps GPU0 free unless GPU1 busy | GPU1 busy/unavailable | Trusted `nvidia-smi`/TF device preflight | planned |
| Rank 16 / epsilon 0.015625 | Prior integration lane selected viable setting | Fixed candidate avoids post-hoc tuning | Setting not efficient/valid in common harness | P01 sanity; bounded repair if validity fails | planned |

## Skeptical Plan Audit

Pre-execution audit target: `PASSED_AFTER_ROUND_2_REPAIR`.

Audit note: round-1 review found that the prior plan could answer
executability without answering efficiency at large particle counts.  This
revision fixes the baseline drift by extending the paired ladder upward until
streaming reaches a fixed timeout/OOM/failure, makes large low-rank-only rows
explicitly unpaired envelope evidence, adds TF32 and same-GPU hard gates, adds
numeric row timeouts, and adds bounded output-comparability gates so resource
proxies cannot support a usability-adjacent efficiency claim after an obvious
output-comparability failure.

Required audit checks before each phase:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If a material issue appears, the phase must be repaired before execution.

## Claude Review Protocol

Claude is read-only reviewer only.  Use this self-contained path-only review
pattern: set Claude's working directory to `/tmp`; provide one absolute
master-program path,
`/home/ubuntu/python/BayesFilter/docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-master-program-2026-06-21.md`;
instruct Claude to inspect only same-prefix `docs/plans` paths named inside
the master program; use read-only review only; write the output log under
`docs/benchmarks/logs/`; require an exact terminal verdict of
`VERDICT: AGREE` or `VERDICT: REVISE`.  Claude cannot authorize crossing
human, runtime, model-file, funding, product-capability, public API/default, or
scientific claim boundaries.

If review finds a fixable problem:

1. patch the same artifact visibly;
2. rerun focused local checks;
3. request another path-only Claude review;
4. stop after five rounds for the same blocker and write a blocker result.

## Program Exit States

- `LOW_RANK_LEDH_EFFICIENCY_SUPPORTED_BOUNDED`
- `LOW_RANK_LEDH_EXECUTABLE_ENVELOPE_SUPPORTED_ONLY`
- `LOW_RANK_LEDH_EFFICIENCY_NOT_SUPPORTED_CURRENT_EVIDENCE`
- `LOW_RANK_LEDH_EFFICIENCY_BLOCKED_GPU_UNAVAILABLE`
- `LOW_RANK_LEDH_EFFICIENCY_BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED`
- `LOW_RANK_LEDH_EFFICIENCY_BLOCKED_REVIEW_NONCONVERGENCE`
