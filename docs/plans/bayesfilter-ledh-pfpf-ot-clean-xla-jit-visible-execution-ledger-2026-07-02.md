# Clean XLA JIT Visible Execution Ledger

Date: 2026-07-02

Status: `OPEN`

## Ledger

### 2026-07-02 - Launch - PRECHECK

Evidence contract:

- Question: Can the corrected full total-derivative LEDH-PFPF-OT route be made
  mechanically clean for GPU/XLA compilation?
- Baseline/comparator: current corrected full route and current
  compiler-hygiene inventory.
- Primary criterion: static guardrails, HLO/compiler-size gates, GPU/XLA smoke,
  same-scalar FD sentinel, and validation gates pass under reviewed subplans.
- Veto diagnostics: hidden stopped partial derivative, Python-unrolled compiled
  loops, non-GPU or non-XLA GPU gates, HLO growth consistent with unrolling,
  nonfinite numerical output, same-scalar FD failure, or review
  nonconvergence.
- Nonclaims: no posterior correctness, exact nonlinear likelihood correctness,
  production HMC readiness, all-model validation, or stopped-route score claim.

Actions:

- Wrote launch artifacts for Claude review.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-master-program-2026-07-02.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-visible-gated-execution-runbook-2026-07-02.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase0-inventory-target-freeze-subplan-2026-07-02.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Claude read-only launch review.

### 2026-07-02 - Launch - BLOCKED

Evidence contract:

- Question: Can the corrected full total-derivative LEDH-PFPF-OT route be made
  mechanically clean for GPU/XLA compilation?
- Primary gate before execution: Claude read-only launch review convergence.

Actions:

- Ran multiple bounded Claude review attempts, including health probes,
  packet-read probe, packet-only review, and no-file compact review.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-launch-review-packet-2026-07-02.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-launch-review-blocker-2026-07-02.md`

Gate status:

- `REOPENED_AFTER_PROMPT_REPAIR`

Next action:

- Run a smaller embedded-packet read-only review.

### 2026-07-02 - Launch - PASS_REVIEW

Evidence contract:

- Question: Is Phase 0 a valid first executable phase before implementation?
- Primary gate: Claude read-only review must return a verdict.

Actions:

- Retried with a no-file embedded mini packet after fixed-path packet read
  hung.
- Claude returned `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-launch-review-minipacket-2026-07-02.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-claude-review-ledger-2026-07-02.md`

Gate status:

- `PASSED`

Next action:

- Execute Phase 0 inventory.

### 2026-07-02 - Claude Probe Repair - PASS

Evidence contract:

- Question: Is Claude unavailable, or did the previous fixed-path review prompt
  have a scope/path-read problem?
- Primary criterion: a tiny Claude read-only health probe returns the exact
  requested token.

Actions:

- Ran a fresh Claude worker health probe with trusted/escalated permissions.

Result:

- Claude returned `CLEAN_XLA_CURRENT_PROBE_OK`.

Interpretation:

- Claude is working.  If a fixed-path review hangs, treat it as a prompt,
  scope, or file-read surface issue and switch to a bounded embedded packet or
  exact line-range packet rather than calling it a network outage.

Gate status:

- `PASSED`

### 2026-07-02 - Phase 0 - PASS

Evidence contract:

- Question: What exactly is unclean in the current compiled route, and what
  must later phases repair?
- Primary criterion: line-anchored inventory of Python-unrolled and stopped
  partial-derivative surfaces.

Actions:

- Inspected P8p SIR manual score route, streaming Sinkhorn helpers, clean value
  core counterexample, and existing nearby static tests.
- Ran CPU-hidden focused source/static checks.
- Wrote Phase 0 result.
- Drafted Phase 1 static guardrails subplan.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase0-inventory-target-freeze-result-2026-07-02.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-guardrails-subplan-2026-07-02.md`

Local check:

- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py::test_streaming_module_source_is_gpu_oriented tests/test_contract_e_phase3_gradient_route_audit.py::test_phase3_r12_gpu_manual_score_route_is_explicit_reverse_scan tests/test_contract_e_phase3_gradient_route_audit.py::test_phase3_r14_manual_dense_sinkhorn_recursions_use_tf_while_loop`
- Result: `3 passed in 4.15s`.

Gate status:

- `PASS_PENDING_PHASE1_CLAUDE_REVIEW`

Next action:

- Claude read-only review of the Phase 1 subplan using a bounded packet.

### 2026-07-02 - Phase 1 Subplan Review - PASS

Evidence contract:

- Question: Is the Phase 1 static-guardrail subplan consistent, bounded,
  feasible, and explicit enough to execute?
- Primary gate: Claude read-only review returns `VERDICT: AGREE`, or fixable
  findings are patched and rereviewed.

Actions:

- Ran exact fixed-path Claude read-only review.
- Iteration 1 returned `VERDICT: REVISE`; patched a closed required-pattern
  checklist and line-anchoring rules.
- Iteration 2 returned `VERDICT: REVISE`; patched current-veto versus
  warning-only missing-symbol behavior and corrected the warning helper symbol.
- Iteration 3 returned `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-guardrails-subplan-2026-07-02.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-claude-review-ledger-2026-07-02.md`

Gate status:

- `PASSED`

Next action:

- Execute Phase 1 static audit script/test implementation.

### 2026-07-02 - Phase 1 Execution - PASS

Evidence contract:

- Question: Can a static guardrail detect the known unclean compiled-path
  patterns before refactoring begins?
- Primary criterion: audit reports the current route as `FAIL_CURRENT_ROUTE`
  with line-anchored findings for every current-veto Phase 0 pattern class, and
  tests pass.

Actions:

- Added `scripts/audit_ledh_clean_xla.py`.
- Added `tests/test_audit_ledh_clean_xla.py`.
- Wrote static audit artifact.
- Wrote Phase 1 result and drafted Phase 2 subplan.

Artifacts:

- `scripts/audit_ledh_clean_xla.py`
- `tests/test_audit_ledh_clean_xla.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-audit-2026-07-02.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-guardrails-result-2026-07-02.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase2-fixed-randomness-tensorization-subplan-2026-07-02.md`

Local checks:

- `CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_clean_xla.py --format json --output docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-audit-2026-07-02.json`
  returned audit decision `FAIL_CURRENT_ROUTE`, 19 current-veto findings, 2
  warning findings, and no missing required patterns.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py`:
  `4 passed in 0.09s`.
- Existing nearby static checks: `3 passed in 6.57s`.

Gate status:

- `PASS_PENDING_PHASE2_CLAUDE_REVIEW`

Next action:

- Claude read-only review of the Phase 1 result and Phase 2 subplan.

### 2026-07-02 - Phase 1 Result And Phase 2 Subplan Review - PASS

Evidence contract:

- Question: Did Phase 1 close correctly, and is Phase 2 safe to execute?
- Primary gate: Claude read-only review returns `VERDICT: AGREE`, or fixable
  findings are patched and rereviewed.

Actions:

- Ran exact two-file Claude read-only review for Phase 1 result and Phase 2
  subplan.

Result:

- Claude returned `VERDICT: AGREE`.
- Non-blocking nit: Phase 2 result should spell out exact ledger paths.

Gate status:

- `PASSED`

Next action:

- Execute Phase 2 fixed randomness tensorization.

### 2026-07-02 - Phase 2 Execution - PASS

Evidence contract:

- Question: Can process-noise randomness be tensorized outside the compiled
  route without changing the existing stateless seed policy?
- Primary criterion: the new fixed `transition_noise` tensor matches the old
  stateless policy, and the manual score route no longer contains the Python
  seed loop.

Actions:

- Added `_make_transition_noise_tensor(...)`.
- Added `tensors["transition_noise"]` in base tensor construction.
- Updated the value callback path and manual score route to consume the fixed
  transition-noise tensor.
- Updated audit tests for the Phase 2 state and added a parity test for the old
  stateless seed formula.
- Wrote Phase 2 static audit artifact.
- Wrote Phase 2 result and drafted Phase 3 subplan.

Artifacts:

- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- `tests/test_audit_ledh_clean_xla.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase2-static-audit-2026-07-02.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase2-fixed-randomness-tensorization-result-2026-07-02.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase3-rk4-loop-hygiene-subplan-2026-07-02.md`

Local checks:

- Static audit decision remains `FAIL_CURRENT_ROUTE`; current-veto findings
  dropped from 19 to 16; `SIR-MANUAL-SEED-LOOP` is
  `ABSENT_CLEAN_OR_MOVED`.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py`:
  `5 passed, 2 warnings in 7.57s`.
- Existing nearby static checks: `3 passed in 3.57s`.
- Targeted AST check: manual score route no longer contains
  `tf.random.stateless_normal` or `for seed in args.batch_seeds`, and does read
  `transition_noise[:, time_index, :, :]`.

Gate status:

- `PASS_PENDING_PHASE3_CLAUDE_REVIEW`

Next action:

- Claude read-only review of Phase 2 result and Phase 3 RK4 subplan.

### 2026-07-02 - Phase 3 Subplan Review - PASS

Evidence contract:

- Question: Is the Phase 3 RK4 loop-hygiene plan safe to execute?
- Primary gate: Claude read-only review returns `VERDICT: AGREE`, or fixable
  findings are patched and rereviewed.

Actions:

- Exact two-file review attempt hung and was interrupted.
- Embedded no-file review returned `VERDICT: REVISE` because RK4 parity was
  underspecified.
- Patched Phase 3 subplan to require independent RK4 forward/aux reference and
  tape-based VJP comparison for points, kappa, and nu.
- Embedded patch review returned `VERDICT: AGREE`.

Gate status:

- `PASSED`

### 2026-07-02 - Phase 3 Execution - PASS

Evidence contract:

- Question: Can RK4 forward aux capture and reverse VJP be represented with
  TensorFlow loop state without changing local RK4 transition/VJP semantics?
- Primary criterion: RK4 static rows absent/clean; independent primal, aux, and
  VJP parity tests pass.

Actions:

- Refactored `_sir_transition_mean_with_aux_tf` to use `tf.while_loop` and
  `TensorArray`.
- Refactored `_sir_transition_mean_vjp_tf` to use reverse `tf.while_loop` over
  stacked aux tensors.
- Added independent RK4 reference and tape-based VJP test.
- Wrote Phase 3 static audit artifact, result, and Phase 4 subplan.

Artifacts:

- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- `tests/test_audit_ledh_clean_xla.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase3-static-audit-2026-07-02.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase3-rk4-loop-hygiene-result-2026-07-02.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-manual-scan-hygiene-subplan-2026-07-02.md`

Local checks:

- Static audit decision remains `FAIL_CURRENT_ROUTE`; current-veto findings
  dropped from 16 to 12; RK4 rows and seed-loop row are
  `ABSENT_CLEAN_OR_MOVED`.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py`:
  `6 passed, 2 warnings in 4.10s`.
- Existing nearby static checks: `3 passed in 3.37s`.

Gate status:

- `PASS_PENDING_PHASE4_CLAUDE_REVIEW`

Next action:

- Claude read-only review of Phase 3 result and Phase 4 manual-scan subplan.

### 2026-07-02 - Phase 4 Subplan Review - PASS

Evidence contract:

- Question: Is the Phase 4 manual-scan hygiene plan safe to execute?
- Primary gate: Claude read-only review returns `VERDICT: AGREE`, or fixable
  findings are patched and rereviewed.

Actions:

- Ran exact two-file Claude read-only review for Phase 3 result and Phase 4
  subplan.

Result:

- Claude returned `VERDICT: AGREE`.
- Watchpoint: Phase 4 result must name the comparator path and report exact
  value/score differences.

Gate status:

- `PASSED`

Next action:

- Execute Phase 4 manual scan hygiene.

### 2026-07-02 - Phase 4 Execution - PASS

Evidence contract:

- Question: Can the live manual P8p SIR forward/reverse time scans be
  represented with TensorFlow loop state without changing focused fixture
  values or gradients?
- Primary criterion: manual-scan audit rows are absent/clean and same-input
  parity against the pre-edit fixture and Python-record reference is zero.

Actions:

- Refactored the live `_manual_value_and_score_from_components` route to use
  `tf.while_loop` and `TensorArray` for forward and reverse time recursion.
- Renamed the old Python-record route to
  `_manual_value_and_score_from_components_python_record_reference` and kept it
  only as a comparator.
- Wrote Phase 4 static audit and parity artifacts.
- Wrote Phase 4 result and drafted Phase 5 subplan.

Local checks:

- Phase 4 audit decision remains `FAIL_CURRENT_ROUTE`, now due only to
  Sinkhorn findings.
- Loop route versus pre-edit JSON fixture: objective, log-likelihood, gradient
  tensor, and per-seed gradient max absolute differences are all `0.0`.
- Loop route versus Python-record reference: objective, log-likelihood,
  gradient tensor, and per-seed gradient max absolute differences are all
  `0.0`.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py`:
  `8 passed, 2 warnings in 6.23s`.
- Manual/regional/audit combined checks: `20 passed, 2 warnings in 36.53s`.

Gate status:

- `PASS_PENDING_PHASE5_CLAUDE_REVIEW`

Next action:

- Claude read-only review of Phase 4 result and Phase 5 Sinkhorn subplan.

### 2026-07-02 - Phase 4 Result And Phase 5 Subplan Review Iteration 1 - REVISE

Evidence contract:

- Question: Is Phase 4 properly closed, and is Phase 5 safe to execute?
- Primary gate: Claude read-only review returns `VERDICT: AGREE`, or fixable
  findings are patched and rereviewed.

Actions:

- Fresh Claude health probe returned `CLEAN_XLA_CURRENT_PROBE_OK`.
- Exact two-file fixed-path review hung and was interrupted, so Codex switched
  to an embedded no-file packet.
- Embedded review returned `VERDICT: REVISE`.

Claude findings:

- Phase 4 is properly closed.
- Phase 5 must explicitly require parity for
  `_filterflow_streaming_finite_sinkhorn_potentials_total_vjp`.
- Phase 5 stop conditions must block semantic Python step iteration and Python
  Tensor state accumulation, not only the literal tokens `range(steps)`,
  `states = []`, and `states.append(...)`.

Repair:

- Patched the Phase 5 subplan to require focused total-VJP parity.
- Strengthened the Phase 5 veto and implementation language to forbid any
  Python step loop or Python state accumulator in the targeted helper symbols.

Gate status:

- `REVIEW_REPAIR_IN_PROGRESS`

Next action:

- Rerun a focused embedded Claude read-only review of the Phase 5 repair.

### 2026-07-02 - Phase 5 Subplan Review Iteration 2 - PASS

Evidence contract:

- Question: Did the Phase 5 subplan repair resolve Claude's total-VJP parity
  and semantic stop-condition blockers?
- Primary gate: focused Claude read-only patch review returns
  `VERDICT: AGREE`.

Actions:

- Sent an embedded no-file patch summary to Claude.

Result:

- Claude returned `VERDICT: AGREE`.
- Claude caveat: the parity reference or fixture must be frozen and matched to
  exact pre-refactor semantics during execution.

Gate status:

- `PASSED`

Next action:

- Execute Phase 5 streaming Sinkhorn loop hygiene.

### 2026-07-02 - Phase 5 Execution - PASS

Evidence contract:

- Question: Can targeted streaming finite Sinkhorn step iteration and stopped-key
  VJP state storage be represented with TensorFlow loop state without changing
  focused helper outputs?
- Primary criterion: targeted Sinkhorn loop/state audit rows are clean and
  focused stopped-value, total-route potential-value, and stopped-key VJP
  parity pass.

Actions:

- Replaced Python Sinkhorn step loops in the stopped-key potential value helper
  and total-route potential value helper with `tf.while_loop`.
- Replaced the stopped-key VJP Python `states` list and reverse Python loop
  with `TensorArray` state and reverse `tf.while_loop`.
- Added Phase 5 AST guard and pre-edit fixture parity test.
- Wrote Phase 5 pre-edit fixture, parity JSON, static audit JSON, result, and
  Phase 6 subplan.

Local checks:

- Focused Phase 5 tests: `2 passed, 2 warnings in 4.86s`.
- Phase 5 static audit decision remains `FAIL_CURRENT_ROUTE`; current-veto
  findings are now only `SINK-STOPPED-VALUE-KEY` and `SINK-STOPPED-VJP-KEY`.
- Phase 5 parity artifact overall max absolute difference: `0.0`.
- `tests/test_audit_ledh_clean_xla.py`: `10 passed, 2 warnings in 7.63s`.
- Streaming recursion VJP tests: `2 passed in 8.69s`.
- Manual/regional/audit combined checks: `22 passed, 2 warnings in 42.76s`.
- Nearby existing static checks: `3 passed in 3.63s`.

Interpretation:

- Phase 5 fixed the intended loop/state mechanics.
- Stopped-key helpers remain partial-derivative helpers. It remains wrong to
  call them scores unless missing total terms are included elsewhere and
  verified.

Gate status:

- `PASS_PENDING_PHASE6_CLAUDE_REVIEW`

Next action:

- Claude read-only review of Phase 5 result and Phase 6 compiler metrics
  subplan.

### 2026-07-02 - Phase 5 Result And Phase 6 Subplan Review - PASS_AFTER_REPAIR

Evidence contract:

- Question: Is Phase 5 properly closed, and is Phase 6 safe to execute?
- Primary gate: Claude read-only review returns `VERDICT: AGREE`, or fixable
  findings are patched and rereviewed.

Actions:

- Embedded no-file review returned `VERDICT: REVISE`.
- Patched Phase 6 to require actual call-path evidence, concrete HLO/retrace
  signatures, run manifest, decision table, and immediate
  environment-blocked classification on trusted GPU probe failure.
- Focused embedded patch review returned `VERDICT: AGREE`.

Gate status:

- `PASSED`

Next action:

- Execute Phase 6 compiler metrics gate, starting with trusted GPU/CUDA probe.

### 2026-07-02 - Phase 6 Execution - PASS

Evidence contract:

- Question: Does the actual full manual route compile and execute under trusted
  GPU/XLA, and is the compiled fixture the total-derivative route rather than
  the stopped-key partial-derivative route?
- Primary criterion: tiny trusted GPU/XLA full-route compile/run succeeds with
  finite outputs, `jit_compile=True`, GPU device evidence, route evidence for
  `transport_ad_mode="full"`, HLO while markers, and no same-signature retrace.

Actions:

- Ran trusted `nvidia-smi`; GPU probe passed.
- Added `scripts/collect_ledh_clean_xla_phase6_metrics.py`.
- Ran the tiny full-route GPU/XLA compiler metrics script with `T=1`, `N=16`,
  one seed, TF32 enabled, float32, streaming transport, and
  `transport_ad_mode="full"`.
- Reran Phase 5 static/parity checks after the GPU fixture.
- Wrote Phase 6 metrics JSON, result, and Phase 7 subplan.

Results:

- Metrics decision: `PASS_TINY_FULL_ROUTE_GPU_XLA_COMPILER_METRICS`.
- Outputs were all on `/GPU:0` and finite.
- Cold compile plus first call: 24.426s.
- Warm same-signature call: 0.041s.
- Concrete function count: `1`; unexpected retrace: `false`.
- HLO text length: 27,766,809; line count: 52,059; while marker count:
  199,199 lower-case matches.
- Route evidence: five source anchors for the `transport_ad_mode="full"` path
  through `_filterflow_manual_streaming_finite_transport_total_vjp`.
- Phase 5 focused checks still passed.

Interpretation:

- Phase 6 proves a tiny full-route GPU/XLA compiler fixture, not broad
  readiness.
- HLO size remains a scaling risk and must be watched in later validation.

Gate status:

- `PASS_PENDING_PHASE7_CLAUDE_REVIEW`

Next action:

- Claude read-only review of Phase 6 result and Phase 7 numerical validation
  subplan.

### 2026-07-02 - Phase 7 Subplan Review - PASS_AFTER_REPAIR

Evidence contract:

- Question: Is Phase 7 numerical validation safe to execute?
- Primary gate: Claude read-only review returns `VERDICT: AGREE`, or fixable
  findings are patched and rereviewed.

Actions:

- Embedded review returned `VERDICT: REVISE`.
- Patched Phase 7 to require runtime route manifest proof for the exact
  executed scalar, explicit `1.0e-5` repeat tolerance, concrete compile/HLO
  watchpoint, and explicit run manifest/decision table contents.
- Focused embedded patch review returned `VERDICT: AGREE`.

Gate status:

- `PASSED`

Next action:

- Execute Phase 7 bounded numerical validation.

### 2026-07-02 - Phase 7 Review Invocation Repair - PASS

Evidence contract:

- Question: Is Claude reachable, and if fixed-path review hangs, can the review
  be made bounded and usable without pretending the fixed-path prompt worked?
- Primary gate: small Claude probe succeeds, and a bounded packet review returns
  a verdict.

Actions:

- Ran a Claude worker health probe. It returned
  `CLEAN_XLA_CURRENT_PROBE_OK`, but output flushed only after interrupting the
  no-output wait.
- Ran direct `claude -p` health probe. It returned
  `DIRECT_CLAUDE_PROBE_OK`.
- Tried a fixed-path read-only review of the Phase 7 subplan. It hung/no-output
  and was stopped.
- Redesigned the review as an embedded bounded packet with the exact plan path
  named for provenance.
- Claude first returned `VERDICT: REVISE`; the Phase 7 plan was patched for a
  fixed FD rule, same-process warm-call determinism scope, and exact HLO
  comparator.
- A minimal repaired packet review returned `VERDICT: AGREE`.

Gate status:

- `PASSED`

Interpretation:

- Claude is reachable. The fixed-path review prompt was the unstable part, not
  network access. Bounded packet review is the stable review shape for this
  phase.

### 2026-07-02 - Phase 7 Execution - OWNER_ACCEPTED_WITH_FD_WAIVER

Evidence contract:

- Question: After clean-loop repairs, does the actual full GPU/XLA route
  produce finite, connected, same-scalar directional gradients on a bounded
  fixture?
- Primary criterion: finite trusted GPU/XLA full route, runtime route manifest
  selecting the total-VJP helper, same-process warm-call repeat determinism at
  `1.0e-5`, same-scalar FD sentinel pass, and HLO watchpoint pass.

Actions:

- Ran trusted `nvidia-smi`; GPU probe passed.
- Added `scripts/collect_ledh_clean_xla_phase7_validation.py`.
- Ran the Phase 7 validation fixture with `T=1`, `N=16`,
  `batch_seeds=[81120]`, `transport_ad_mode="full"`, TF32 enabled, and FD
  steps `0.002,0.001,0.0005`.
- Reran Phase 5 static/parity guardrail checks.
- Wrote the Phase 7 validation JSON and result.

Results:

- Decision: `FAIL_PHASE7_NUMERICAL_VALIDATION`.
- GPU/XLA route evidence passed: outputs were on `/GPU:0`, finite, one
  concrete function, no unexpected retrace, and the runtime route manifest
  selected `_filterflow_manual_streaming_finite_transport_total_vjp`.
- Repeat determinism passed with zero max absolute deltas for objective,
  log-likelihood, mean gradient, and per-seed gradient.
- HLO watchpoint passed: text length `27,766,809`, same as the Phase 6 fixture
  and below the `4x` bound.
- Same-scalar FD sentinel failed only for `log_obs_noise_scale`.
  - analytic score: `4.833810806274414`;
  - FD values: `4.935264587402344`, `4.9343109130859375`,
    `4.98199462890625`;
  - closest miss: absolute error `0.10050010681152344` versus tolerance
    `0.09968621826171875`.
- Phase 5/guardrail checks passed after the run:
  `tests/test_audit_ledh_clean_xla.py` had `10 passed`; the focused
  Sinkhorn VJP primitive check had `2 passed`.

Initial gate status:

- `BLOCKED_FD_SENTINEL`

Owner acceptance:

- On 2026-07-03, the owner explicitly approved treating this result as accepted
  and promoted because it is closed enough and not worth extra repair effort.
- Codex updated the Phase 7 JSON/result to mark
  `OWNER_ACCEPTED_WITH_FD_WAIVER` while preserving `primary_pass=false` for the
  original preregistered gate.

Final gate status:

- `OWNER_ACCEPTED_WITH_FD_WAIVER`

Next action:

- Close the bounded clean-XLA fixture program as owner-promoted with caveats.
  Do not claim the preregistered FD gate passed, HMC readiness, exact nonlinear
  likelihood correctness, or that stopped-key partial derivatives are scores.
