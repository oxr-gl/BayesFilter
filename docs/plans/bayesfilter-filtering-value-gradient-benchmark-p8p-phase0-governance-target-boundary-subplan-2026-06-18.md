# P8p Phase 0 Subplan: Governance And Target Boundary

Date: 2026-06-18

Status: `DRAFT_PENDING_REVIEW`

## Phase Objective

Lock the P8p lane boundary before any implementation or experiment:

- confirm this is the DPF/SIR d18 gradient/HMC-mechanics lane;
- inherit P8o value-only SIR d18 evidence without treating it as gradient
  evidence;
- define the initial diagnostic theta target boundary;
- record that the existing score helper can mask disconnected gradients and
  therefore cannot be the only gradient-connectivity diagnostic;
- record forbidden claims and exact handoff to Phase 1.

## Entry Conditions Inherited From Previous Phase

There is no previous P8p phase.  Entry requires:

- P8o value-only SIR d18 DPF cell exists and is marked pass;
- current repo contains the actual-SIR batched streaming harness;
- current repo contains streaming LEDH-PFPF-OT value/score hooks;
- user direction excludes bootstrap comparator and scalar route parity from
  this lane;
- Zhao-Cui fixed-branch and monograph rewrite work remain out of scope.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-sir-d18-gradient-hmc-master-program-2026-06-18.md`
- Phase 0 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase0-governance-target-boundary-result-2026-06-18.md`
- Visible runbook:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-visible-gated-execution-runbook-2026-06-18.md`
- Execution ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-visible-execution-ledger-2026-06-18.md`
- Claude review ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-claude-review-ledger-2026-06-18.md`
- Phase 1 subplan draft:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase1-parameterized-sir-objective-subplan-2026-06-18.md`

## Required Checks, Tests, And Reviews

Local checks:

```bash
python -m py_compile docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-sir-d18-gradient-hmc-master-program-2026-06-18.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase0-governance-target-boundary-subplan-2026-06-18.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase1-parameterized-sir-objective-subplan-2026-06-18.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-visible-stop-handoff-2026-06-18.md
rg -n "PASS_SELECT_N10000|not DPF gradient correctness|not HMC/NUTS readiness" docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8o-sir-d18-dpf-particle-adequacy-leaderboard-result-2026-06-18.md
rg -n "streaming_batched_ledh_pfpf_ot_value_and_score_tf|GradientTape|pre_flow_step_fn|prior_mean_fn" experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
rg -n "UnconnectedGradients.ZERO|zeros_like\\(theta\\)" experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py
```

Review:

- Claude read-only review of the master program, Phase 0 subplan, Phase 1
  subplan draft, and visible runbook.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is P8p scoped correctly as a new parameterized SIR d18 diagnostic-gradient lane, with P8o used only as value-only entry evidence? |
| Baseline/comparator | P8o value-only SIR d18 result and current actual-SIR streaming harness. |
| Primary pass criterion | Phase 0 passes if local checks locate the required artifacts/hooks, the result records exact lane boundaries, Claude review converges, and Phase 1 has a concrete target-design subplan. |
| Veto diagnostics | Missing P8o artifact; missing streaming value/score hook; treating P8o as gradient/HMC evidence; including bootstrap/scalar parity as required work; Zhao-Cui fixed-branch/monograph drift; allowing stochastic categorical resampling or variable random streams in the theta target; claiming posterior validity. |
| Explanatory diagnostics | Search hits, harness file names, dirty-worktree summary. |
| Not concluded | Any gradient correctness, finite-difference correctness, HMC readiness, posterior convergence, exact likelihood correctness, or production/default readiness. |
| Artifact | Phase 0 result and review ledger. |

## Forbidden Claims And Actions

- Do not claim DPF gradient correctness or HMC/NUTS readiness in Phase 0.
- Do not treat `streaming_batched_ledh_pfpf_ot_value_and_score_tf` as sufficient
  connectivity evidence, because it currently zero-fills unconnected gradients.
- Do not run long experiments in Phase 0.
- Do not execute GPU benchmarks in Phase 0.
- Do not edit Zhao-Cui fixed-branch or monograph files.
- Do not change model defaults, pass/fail criteria, or git state.
- Do not include bootstrap comparator or scalar route parity as required P8p
  work.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- local checks pass;
- Claude review returns `VERDICT: AGREE`, or fixable review issues are patched
  and re-reviewed to agreement;
- Phase 0 result explicitly states that P8p is a diagnostic parameterized
  target separate from the fixed-parameter SIR d18 leaderboard row;
- Phase 0 result records that Phase 2 must include an explicit per-theta
  connectivity diagnostic, not only the existing zero-filled score helper;
- Phase 1 subplan is present and names the theta, fixed-randomness contract,
  implementation files, and review boundary.

## Stop Conditions

Stop and write a blocker if:

- P8o value-only evidence is absent or contradicted;
- the streaming value/score hook is absent;
- the theta target requires a scientific decision not already authorized by the
  user;
- Claude/Codex review does not converge after five rounds;
- continuing would require package installation, network, credentials,
  destructive git/filesystem action, or unrelated dirty-worktree edits.
