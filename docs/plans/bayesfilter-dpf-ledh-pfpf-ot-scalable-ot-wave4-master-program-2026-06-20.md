# Wave 4 Master Program: Replicated Downstream Validation

Date: 2026-06-20
Supervisor/executor: Codex in the current conversation
Read-only reviewer: Claude Opus max effort for material plan and claim issues

## Supersession Notice

`SUPERSEDED_AS_ACTIVE_PARALLEL_EXECUTION_MODEL`

This master program is a historical record of an over-coupled Wave 4
coordination attempt.  It should not be used to make the peer low-rank lane
wait for the current positive-feature lane or to require shared fixture/seed
synchronization during independent algorithm execution.

For active cross-agent coordination, use:

`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-independent-lane-clarification-to-peer-2026-06-20.md`

## Status

`WAVE4_MASTER_PROGRAM_LAUNCHED_STOPPED_WAITING_FOR_PEER_LOW_RANK_ARTIFACTS`

## Purpose

Wave 4 is the first statistically disciplined downstream validation program
after Wave 3.  Wave 3 showed that the two Wave 2 candidates pass a common
deterministic hard-veto smoke.  Wave 4 asks whether each candidate remains
viable on replicated deterministic filtering-style resampling fixtures with a
predeclared evidence contract.

This program uses exactly two active algorithm agents:

- current agent: positive-feature Sinkhorn semantic-replacement lane;
- peer agent: low-rank coupling solver-route lane.

The two lane executions are intentionally independent.  They communicate only
through Markdown and structured artifacts under `docs/plans` and
`docs/benchmarks`.  The coordinator merge runs only after both lane close
records exist.

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the positive-feature and low-rank coupling candidate lanes remain viable under replicated deterministic downstream resampling screens that compare post-transport uniform estimates with pre-transport weighted reference estimates? |
| Baseline/comparator | Exact weighted input estimates are the downstream reference for each fixture.  A naive uniform-no-transport estimator is recorded as an explanatory sanity comparator only.  Wave 2 and Wave 3 artifacts are entry evidence, not promotion evidence. |
| Primary pass criterion | Each lane must produce a lane JSON/Markdown artifact and result note with empty hard vetoes, finite transported particles, valid shapes, normalized uniform output log weights, finite nonmaterialized transport-object diagnostics, predeclared residual thresholds satisfied, and predeclared weighted-moment downstream screen thresholds satisfied across the lane fixture ladder. |
| Veto diagnostics | Missing/invalid entry artifacts; nonfinite particles, weights, factors, features, or diagnostics; shape mismatch; log-weight normalization residual above `1.0e-10`; transport residual above lane threshold; weighted-mean error above `3.0e-1`; weighted second-moment error above `1.0`; schema/manifest mismatch; unsupported claim; changing thresholds after seeing results; public/default/shared-schema boundary crossing. |
| Explanatory diagnostics | Naive uniform estimator error, candidate-vs-naive deltas, wall time, per-fixture errors, residual magnitudes, per-seed tables, and descriptive uncertainty summaries. |
| Statistical ranking rule | No ranking is supported unless both lane artifacts predeclare and compute a valid paired uncertainty analysis over the same fixture/seed grid and the final coordinator verifies the ranking rule.  Wave 4 launch does not assume ranking will be possible. |
| Not concluded | No speedup, superiority, production/default readiness, public API readiness, HMC readiness, posterior correctness, dense Sinkhorn equivalence, broad scalable-OT selection, or scientific claim beyond the stated hard screen. |
| Artifacts | Wave 4 master/subplans/results, current-lane script/test/JSON/Markdown, peer-lane task note and expected peer artifacts, Claude review ledger, visible runbook, execution ledger, final merge or stop handoff. |

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Can the two candidate transport families survive a replicated downstream resampling hard screen before any larger ranking/default discussion? |
| Candidate/mechanism | Positive-feature Sinkhorn semantic replacement and low-rank coupling solver-route semantic replacement. |
| Expected failure mode | A candidate may satisfy internal transport diagnostics but distort weighted downstream moments on replicated filtering-style fixtures. |
| Promotion criterion | For Wave 4, promotion means "remains viable for a later, larger validation"; it does not mean default selection. |
| Promotion veto | Any hard veto in a lane artifact prevents that lane from being promoted to later validation. |
| Continuation veto | Invalid artifacts, unsupported claims, changed thresholds after observing results, missing peer result for final merge, or boundary crossing. |
| Repair trigger | Fixable script/test/reporting bug inside the lane write set, missing nonclaim, or reviewer-identified ambiguity that does not require changing criteria after results. |
| Explanatory diagnostics | Runtime, naive baseline deltas, per-seed descriptive summaries, and residual magnitudes. |
| Must not conclude | No candidate is better, faster, production ready, HMC ready, posterior correct, or default ready from Wave 4 alone. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| W4-0 | Launch Packet And Review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p00-launch-review-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p00-launch-review-result-2026-06-20.md` |
| W4-1 | Peer Low-Rank Lane Handoff | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p01-peer-low-rank-handoff-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p01-peer-low-rank-handoff-result-2026-06-20.md` |
| W4-2 | Current Positive-Feature Lane | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p02-current-positive-feature-validation-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-positive-feature-result-2026-06-20.md` |
| W4-3 | Final Merge And Inference Status | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p03-final-merge-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-final-merge-result-2026-06-20.md` |

## Lane Artifact Contract

Each algorithm lane must write a JSON and Markdown diagnostic result with:

- `status`;
- `wave4_status`;
- `lane_id`;
- `candidate_id`;
- `hard_vetoes`;
- `settings`;
- `summary`;
- `rows`;
- `inference_status`;
- `manifest`;
- `evidence_contract`;
- `nonclaims`.

Each row must record fixture name, seed, particle count, state dimension,
candidate downstream errors, naive uniform-no-transport errors, transport
diagnostics, wall time, and row hard vetoes.

Each lane manifest must record git commit, exact command/argv, plan path, result
path, JSON output path, Markdown output path, fixture list, seed list, total wall
time, Python/platform/TensorFlow versions where applicable, CPU/GPU device
scope, and whether GPU devices were intentionally hidden.

## Phase Advancement Rule

Each phase may start only after:

- its dedicated subplan exists;
- inherited entry conditions are satisfied;
- required local checks pass or a blocker result is written;
- material Claude review has converged where required;
- no human-required stop condition is active.

At the end of each phase, Codex must:

1. run the required local checks;
2. write the phase result or close record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Claude Review Protocol

Claude is read-only reviewer only.  Claude cannot authorize crossing human,
runtime, model-file, funding, product-capability, public API/default, or
scientific-claim boundaries.

Do not send whole files to Claude.  Use compact review packets with paths,
summaries, evidence contracts, stop conditions, and targeted questions.  If
Claude does not respond, run a tiny probe.  If the probe responds, redesign the
prompt.  If a material issue is fixable, patch visibly and rerun focused
checks and review.  Stop after five rounds for the same blocker.

## Skeptical Plan Audit

| Audit item | Wave 4 control |
| --- | --- |
| Wrong baseline risk | Exact weighted input estimates are the reference for a resampling-step downstream screen; naive uniform-no-transport is explanatory only. |
| Proxy promotion risk | Runtime, candidate-vs-naive differences, and descriptive per-seed summaries cannot rank or promote defaults. |
| Missing stop condition risk | Phase and lane subplans include hard veto, repair, human-required, and peer-missing stops. |
| Unfair comparison risk | Lanes run independently against the same artifact contract; final merge cannot rank without same fixture/seed grid verification and valid paired uncertainty fields. |
| Hidden assumption risk | The program states that the screen is a resampling-step moment screen, not a full posterior or HMC validation. |
| Stale context risk | Wave 2 and Wave 3 artifacts are entry conditions and are rechecked before lane execution. |
| Environment mismatch risk | TensorFlow commands are CPU-scoped with `CUDA_VISIBLE_DEVICES=-1`; GPU warnings are not GPU evidence. |
| Artifact-answer mismatch risk | Lane artifacts answer viability under the hard screen only; final merge is blocked until both lane artifacts exist. |

Audit decision: Wave 4 may launch after W4-0 local checks and Claude compact
review pass.

## Stop Conditions

Stop if continuing requires package installation, network fetch beyond the
approved Claude reviewer wrapper, credentials, GPU evidence, external solver
execution, public API/default/export changes, Phase 1/Phase 3 shared edits,
changing thresholds after seeing results, using descriptive metrics for
ranking, making a forbidden claim, or final merge without the peer lane result.
