# Actual-SIR Low-Rank Tuning And Held-Out Validation Master Program

Date: 2026-06-22
Status: `DRAFT_FOR_REVIEW`

Supervisor/executor: Codex in this conversation.

Claude role: read-only reviewer only. Claude cannot authorize crossing human,
runtime, model-file, funding, product-capability, default-policy, public API, or
scientific-claim boundaries. Claude review prompts must be path-only and must not
send whole file contents.

## Reset Anchor

This program restarts from:

`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-restart-reset-memo-2026-06-21.md`

The previous actual-SIR low-rank validation stopped at `TUNING_REQUIRED`. The
failed row rejects promotion of the previously configured candidate, not the
low-rank research direction.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can a tuned low-rank solver route make actual-SIR d18 LEDH/PFPF-OT more efficient at large particle counts while preserving predeclared engineering comparability? |
| Candidate/mechanism | Existing TensorFlow low-rank solver route with actual-SIR-specific tuning of exposed parameters. |
| Comparator | Existing compiled streaming actual-SIR TF32/GPU route from `docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py`, accessed through `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`. |
| Tuning target | Actual-SIR d18 rows only. Synthetic or proxy rows may debug harness mechanics but cannot nominate or promote. |
| Expected failure mode | Low-rank factors remain valid but paired log-likelihood comparability or warm-time support depends on rank, assignment epsilon, alpha, or projection iterations. |
| Promotion criterion | A frozen tuned candidate must pass held-out paired actual-SIR rows with hard validity, paired comparability, same physical GPU UUID, TF32 provenance, and warm-time support after validity/comparability pass. |
| Promotion veto | Nonfinite outputs, invalid factors, dense transport materialization, missing actual-SIR semantics, route-fired mismatch, paired comparability failure on held-out support rows, same-GPU provenance failure, or speed support failure after comparability. |
| Continuation veto | Shared contract/API change, package install/network/POT, trusted GPU unavailable for GPU evidence, corrupted artifacts, missing required diagnostics, or inability to preserve evidence answering the phase question. |
| Repair trigger | Tuning rows show finite valid factors but fail comparability or speed in a parameter-dependent way; harness emits incomplete but fixable diagnostics; Claude finds a fixable plan inconsistency. |
| Explanatory diagnostics | Runtime, memory, first-call time, warm-call time, ESS, log-likelihood deltas, filtered-summary deltas, projection iterations, factor residuals, GPU memory metadata. |
| Not concluded | No posterior correctness, HMC readiness, public API/default/production readiness, dense Sinkhorn equivalence, broad scalable-OT selection, statistical ranking, or production default change. |

## Tuning And Promotion Discipline

- Tuning rows may nominate candidates but cannot promote them.
- A candidate must be frozen in Phase 4 before any held-out support evidence is
  interpreted.
- The prior failed row may be reused as a regression row, but held-out support
  must include at least one shape/seed set not used to select parameters.
- Runtime can guide tuning only after hard validity and paired comparability are
  inspected.
- A faster but incomparable candidate is not promotable.
- A comparable but slower candidate may justify route repair, not promotion.
- Low-rank-only large-N rows can support executable-envelope language only after
  held-out paired support passes.

## Exposed Tuning Knobs

Tune only parameters already exposed by the validation harness unless a reviewed
subplan explicitly authorizes route repair:

- `low_rank_rank`: bounded grid starting with `16,32,64,128`, respecting
  `rank <= N`;
- `low_rank_assignment_epsilon`: coarse grid such as
  `0.25,0.125,0.0625,0.03125,0.015625`;
- `low_rank_alpha`: only within `alpha * rank < 1`;
- `low_rank_max_projection_iterations`: `120,240,480` only when runtime budget
  permits or residual/iteration diagnostics justify it;
- `low_rank_convergence_threshold`: only if projection iterations hit the cap or
  residuals are near threshold;
- `low_rank_denominator_floor`: fixed unless nonfinite/floor diagnostics show it
  is active.

Route-repair knobs requiring a separate reviewed implementation plan:
deterministic landmark selection, cost scaling or whitening, adaptive rank
schedule, or graph compilation of the low-rank loop.

## Fixed Gates

Carry forward the reset memo gates unless a reviewed plan changes them before
execution:

| Gate | Threshold / protocol | Role |
| --- | --- | --- |
| Finite outputs | log likelihood, filtered means/variances, ESS, final particles, final log weights all finite | hard veto |
| Actual-SIR semantics | row id `zhao_cui_spatial_sir_austria_j9_T20`, `D=18`, `M=9`, actual callback metadata | hard veto |
| Route-fired evidence | route invocation count equals active resampling steps | hard veto |
| Low-rank nonmaterialization | low-rank transport matrix shape suffix `[0, 0]` and materialized flag false | hard veto |
| Low-rank factor validity | finite factors, `Q,R >= 0`, `g > 0`, max factor marginal residual `<= 5e-3` | hard veto |
| Log-weight normalization | final log-sum-exp residual `<= 1e-5` | hard veto |
| ESS floor | ESS fraction min `>= 0.01` | hard veto |
| Log-likelihood comparability | max abs delta `<= 10.0`, mean abs delta `<= 5.0` | paired veto |
| Filtered means | relative L2 `<= 0.20` or absolute RMS `<= 2.5` | paired veto |
| Filtered variances | relative L2 `<= 0.75` or absolute RMS `<= 25.0` | paired veto |
| Final particle mean | relative L2 `<= 0.20` or absolute L2 `<= 25.0` | paired veto |
| Warm-time support | streaming warm median / low-rank warm median `>= 1.25` after paired comparability passes | promotion screen |
| Same GPU provenance | paired support rows must use same physical GPU UUID for both routes | hard veto for GPU support |

## Phase Index

| Phase | Name | Subplan | Required result |
| ---: | --- | --- | --- |
| 0 | Governance, audit, and review convergence | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p00-governance-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p00-governance-result-2026-06-22.md` |
| 1 | Harness and tuning-grid readiness | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p01-harness-grid-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p01-harness-grid-result-2026-06-22.md` |
| 2 | Tiny actual-SIR tuning smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p02-tiny-smoke-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p02-tiny-smoke-result-2026-06-22.md` |
| 3 | Actual-SIR tuning screen | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p03-tuning-screen-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p03-tuning-screen-result-2026-06-22.md` |
| 4 | Candidate freeze | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p04-candidate-freeze-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p04-candidate-freeze-result-2026-06-22.md` |
| 5 | Held-out paired support ladder | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p05-heldout-support-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p05-heldout-support-result-2026-06-22.md` |
| 6 | Large-N envelope | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p06-large-n-envelope-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p06-large-n-envelope-result-2026-06-22.md` |
| 7 | Closeout and claim classification | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p07-closeout-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-result-2026-06-22.md` |

## Owned Write Set

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-*.md`
- `docs/benchmarks/actual-sir-low-rank-tuning-*.json`
- `docs/benchmarks/actual-sir-low-rank-tuning-*.md`
- `docs/benchmarks/logs/actual-sir-low-rank-tuning-*.log`
- A small tuning-grid wrapper under `docs/benchmarks/` only if P01 shows that
  repeated direct harness commands would not preserve aggregate evidence safely.
- Focused tests under `tests/` only if P01 implements or repairs a wrapper.

## Forbidden Writes

- BayesFilter public exports.
- Existing actual-SIR benchmark source except read-only use.
- Existing low-rank solver source except read-only use.
- Shared schemas, package metadata, dependency lock files, model files, or
  unrelated dirty worktree files.

## Skeptical Plan Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: comparator is the compiled streaming actual-SIR route, not synthetic/proxy low-rank evidence. |
| Proxy metrics promoted | Guarded: tuning/proxy/smoke rows nominate or debug only; held-out paired rows promote. |
| Missing stop conditions | Guarded by phase stop conditions and continuation vetoes. |
| Unfair comparison | Guarded by same seeds, shape, dtype, TF32 mode, physical GPU UUID, and route semantics for paired support rows. |
| Hidden assumptions | Guarded: existing low-rank route is a candidate; tuning does not certify dense Sinkhorn equivalence or posterior correctness. |
| Stale context | Guarded by P00 source-anchor check and reset-memo ingestion. |
| Environment mismatch | Guarded: GPU evidence requires trusted execution and recorded GPU provenance. |
| Artifact mismatch | Guarded: every phase predeclares JSON/Markdown/log/result paths before execution. |

Audit conclusion: the program may proceed to P00 review. Benchmark execution is
blocked until the visible runbook and P01 readiness checks pass.

## Repair Loop Protocode

For each phase:

1. Read the subplan and restate the evidence contract.
2. Run the smallest command that answers the phase question.
3. Preserve full output in a log path declared in the subplan.
4. Assess hard vetoes before descriptive metrics.
5. Write the phase result or blocker result.
6. Draft or refresh the next subplan.
7. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
8. Use Claude read-only review for material subplans/results.
9. If the blocker is fixable, patch the same subplan visibly, rerun focused
   checks, and rerun Claude review.
10. Stop after five Claude review rounds for the same blocker.

Expected tuning failure is not by itself a continuation veto. If a later planned
phase is designed to repair exactly the observed failure, continue to that
repair unless a true continuation veto fires.

## Claude Review Protocol

Use:

`bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh --cwd /home/ubuntu/python/BayesFilter --name actual-sir-lr-tuning-review --model opus --effort max "<path-only prompt>"`

The prompt must be read-only, path-only, and end-requested with exactly one of:

- `VERDICT: AGREE`
- `VERDICT: REVISE`

If Claude does not respond, run a small read-only probe. If the probe responds,
redesign the review prompt and retry. If review finds a fixable problem, patch
the same subplan visibly and rerun focused checks. Stop after five rounds for
the same blocker.
