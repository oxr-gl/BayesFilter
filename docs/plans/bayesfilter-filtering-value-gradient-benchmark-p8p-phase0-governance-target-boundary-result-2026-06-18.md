# P8p Phase 0 Result: Governance And Target Boundary

Date: 2026-06-18

Status: `PASS_PHASE0_LAUNCH_PHASE1_READY`

## Phase Objective

Lock the P8p lane boundary before implementation or experiment:

- DPF/SIR d18 parameterized gradient and HMC-mechanics diagnostics only;
- P8o value-only evidence is an entry condition, not gradient/HMC evidence;
- initial diagnostic theta is the three global log-scale surface;
- Phase 1 must bind theta to exact actual-SIR harness edit points.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is P8p scoped correctly as a new parameterized SIR d18 diagnostic-gradient lane, with P8o used only as value-only entry evidence? |
| Baseline/comparator | P8o value-only SIR d18 result and current actual-SIR streaming harness. |
| Primary pass criterion | Local checks locate the required artifacts/hooks, the result records exact lane boundaries, Claude review converges, and Phase 1 has a concrete target-design subplan. |
| Veto diagnostics | Missing P8o artifact; missing streaming value/score hook; P8o treated as gradient/HMC evidence; bootstrap/scalar parity drift; Zhao-Cui fixed-branch/monograph drift; variable randomness or categorical resampling in theta target; posterior-validity claim. |
| Not concluded | Gradient correctness, finite-difference correctness, HMC readiness, posterior convergence, exact likelihood correctness, or production/default readiness. |

## Skeptical Audit

- Wrong baseline: P8o is used only as value-only entry evidence and shape/runtime
  provenance. It is not promoted to gradient or HMC evidence.
- Proxy metrics: finite differences, gradient norms, ESS, runtime, chunk deltas,
  and tiny HMC traces remain explanatory or veto-linked; they are not posterior
  validity proof.
- Missing stop conditions: the master program, Phase 0 subplan, and visible
  runbook now include trusted-GPU, unrelated-lane mutation, runtime-projection,
  destructive-action, criteria-drift, and review-nonconvergence stops.
- Hidden assumption: the existing streaming score helper zero-fills
  unconnected gradients. P8p now requires an explicit per-theta connectivity
  diagnostic before any connected-gradient gate can pass.
- Artifact fitness: Phase 1 is required to name exact theta-dependent edit
  points before code changes.

## Local Checks

Commands run:

```bash
python -m py_compile docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-sir-d18-gradient-hmc-master-program-2026-06-18.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase0-governance-target-boundary-subplan-2026-06-18.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase1-parameterized-sir-objective-subplan-2026-06-18.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-visible-stop-handoff-2026-06-18.md
rg -n "PASS_SELECT_N10000|not DPF gradient correctness|not HMC/NUTS readiness" docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-sir-d18-dpf-particle-adequacy-leaderboard-result-2026-06-18.md
rg -n "streaming_batched_ledh_pfpf_ot_value_and_score_tf|GradientTape|pre_flow_step_fn|prior_mean_fn" experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
rg -n "UnconnectedGradients.ZERO|zeros_like\\(theta\\)" experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py
rg -n "connectivity diagnostic|zero-filled score helper|theta-dependent edit points|runtime projection|mutating unrelated" docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-*.md
```

Results:

- `py_compile`: passed.
- `git diff --check`: passed.
- P8o pass-status search found the value-only pass artifact. The exact
  nonclaim phrase search was narrower than the artifact wording, so it was
  treated as a boundary-audit note rather than extra gradient evidence.
- Streaming harness and value/score hook search found:
  `prior_mean_fn`, `pre_flow_step_fn`,
  `streaming_batched_ledh_pfpf_ot_value_and_score_tf`, and `GradientTape`.
- Connectivity caveat search found the existing zero-fill behavior:
  `tf.UnconnectedGradients.ZERO` and `tf.zeros_like(theta)`.
- Revised P8p artifacts contain the required connectivity, edit-point, and
  stop-condition language.

## Claude Review

Claude read-only review:

- Iteration 1: `VERDICT: REVISE`.
- Iteration 2: `VERDICT: AGREE`.

Review ledger:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-claude-review-ledger-2026-06-18.md`

Material iteration-1 issues and repairs:

- Existing score helper can mask disconnected gradients as zeros:
  repaired by requiring explicit per-theta connectivity diagnostics in the
  master program, Phase 0, Phase 1, and runbook.
- Phase 1 needed exact theta-dependent edit points:
  repaired by naming `_make_actual_sir_callbacks`, `transition_mean`,
  `sir_rhs`, `pre_flow_step`, `transition_log_density_fn`,
  `observation_log_density_fn`, and the observation-covariance path.
- Runbook needed master stop-condition carry-through:
  repaired by adding runtime projection and unrelated-lane mutation stops.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Pass Phase 0 and launch Phase 1 planning. | Passed. | No Phase 0 veto remains after Claude iteration 2. | Phase 1/2 may still find the current harness needs more code repair than expected. | Execute Phase 1: write the parameterized objective contract and Phase 2 implementation subplan before code edits. | No gradient correctness, HMC readiness, posterior validity, exact likelihood correctness, production/default readiness, or Zhao-Cui TT/SIRT parity. |

## Handoff To Phase 1

Phase 1 must:

- preserve P8p as a diagnostic parameterized target separate from the fixed
  SIR d18 value leaderboard cell;
- define the theta transforms and fixed-randomness contract;
- name exact implementation files and tests before edits;
- require explicit per-theta connectivity diagnostics that are not satisfied by
  the current zero-filled score helper;
- draft Phase 2 only after the target contract is clear.
