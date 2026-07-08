# Review Bundle: Minimal SSL-LSTM Zhao-Cui HMC Next Phase 0/1

Date: 2026-07-06

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex is supervisor and executor. Claude is read-only reviewer only.

## Review Scope

Review the compact plan summary below for consistency, correctness,
feasibility, artifact coverage, and boundary safety. Do not inspect the whole
repository.

Primary artifacts:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-program-master-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-visible-gated-execution-runbook-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase0-governance-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase1-internal-adapter-subplan-2026-07-06.md`

Context:

- The predecessor minimal scalar CPU-hidden HMC ladder completed.
- It established only debug/reference mechanics evidence.
- GPU/XLA smoke and longer diagnostics were not previously run.
- The current program has three branches: internal reusable surface, trusted
  GPU/XLA runtime smoke, and longer sampler diagnostics.

## Evidence Contract To Audit

| Field | Contract |
| --- | --- |
| Question | Can the minimal scalar `zhaocui_fixed` HMC mechanics surface move from benchmark-only code to an internal reusable module, then be exercised by trusted GPU/XLA and longer diagnostic gates without evidence inflation? |
| Baseline/comparator | Completed CPU-hidden HMC ladder harness and artifacts. |
| Primary pass criterion | Phase 1 preserves benchmark behavior through an internal module; Phase 2 CPU regression passes; later phases pass their own reviewed gates or stop with deferral/blocker records. |
| Veto diagnostics | Missing skeptical audit, invalid artifact, unsupported claim, target-path NumPy/autodiff bridge, public API/default-policy change, source-faithfulness claim without anchors, GPU command without trusted boundary, long run without reviewed evidence contract, nonfinite target value/score, HMC runtime exception, nonfinite samples, or missing next-phase handoff. |
| Explanatory diagnostics | Runtime, score norm, log probability, acceptance, sampler metadata, device provenance, TF32/XLA settings, and dirty-worktree summaries. |
| Not concluded | Posterior correctness, HMC convergence, statistical ranking, method superiority, source-faithful Zhao-Cui parity, public API/package readiness, default readiness, GPU/XLA production readiness, or LEDH result. |

## Phase 0 Summary

Objective: establish governance, review path, evidence contract, and boundary
gates before runtime-code extraction.

Required checks:

- `git status --short`
- compile existing minimal ladder benchmark and tests
- forbidden-claim scan across new plan/review files
- material review with Claude gate, or documented fresh Codex-agent fallback if
  Claude is unavailable or denied

Phase 0 may not edit runtime code, run HMC/GPU/XLA/long diagnostics, or make
scientific/default/source-faithful claims.

## Phase 1 Summary

Objective: extract benchmark-only `MinimalZhaoCuiHMCTargetAdapter` and minimal
fixture helpers into:

- `bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py`

The benchmark harness should consume the internal module. New focused tests
should cover the internal module. The module is internal only and should not be
top-level public API in Phase 1.

Phase 1 is mechanical extraction only. Existing ladder tests may be updated
only for import-path migration or an explicitly documented schema repair. A
predecessor comparator must preserve schema version, fixture dimensions,
`log_prob`, score vector, scalar score shape `(24,)`, batch score shape
`(2, 24)`, capability metadata, nonclaims, and adapter signature against the
pre-extraction harness/artifact unless a reviewed non-behavioral schema-only
repair is recorded.

No new Zhao-Cui route choice may be introduced. If extraction requires changing
fixed replay/recentering behavior, likelihood, seeds, prior geometry, HMC
settings, or route classification, the phase must stop and classify the choice
as `source_faithful`, `fixed_hmc_adaptation`, or `extension_or_invention` with
required anchors or explicit human approval.

Required Phase 1 checks:

- compile internal module, benchmark harness, new tests, existing ladder tests
- CPU-hidden pytest for new and existing tests
- immutable predecessor comparator check
- forbidden implementation scan for `GradientTape`, `tf.py_function`,
  `import numpy`, and `np.` in the target path
- `git diff --check`
- material review of implementation diff and Phase 2 handoff

The `GradientTape` scan is a conservative Phase 1 mechanical-extraction guard:
new explicit autodiff use would change the predecessor manual score authority
and requires a separate reviewed plan. This is not a repository-wide ban on
TensorFlow autodiff.

## Specific Review Questions

1. Does the plan have a wrong baseline or stale predecessor assumption?
2. Does it promote proxy metrics, smoke tests, or CPU-hidden checks into
   convergence, posterior correctness, ranking, GPU/default readiness, or
   source-faithfulness?
3. Are stop conditions and exact next-phase handoff conditions sufficient?
4. Are artifact requirements sufficient to recover the work after interruption?
5. Does Phase 1 avoid public API/default-policy/model-file/GPU/long-run
   boundaries?
6. Are the review fallback rules safe if Claude is unavailable or denied?
7. Is any material number treated as sacred without provenance?
8. Does the repaired Phase 1 baseline freeze prevent adapter, harness, and
   tests from drifting together?

Findings first. End with exactly:

VERDICT: AGREE

or

VERDICT: REVISE
