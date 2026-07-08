# SIR Gradient Reparameterization Root-Cause Visible Execution Ledger

Date: 2026-07-01

Status: `COMPLETED`

## Ledger

### 2026-07-01T04:45:00+08:00 - Program Draft - PRECHECK

Evidence contract:

- Question: Which SIR dynamic-parameter score component explains the
  budget-10 manual-score vs FD mismatch?
- Baseline/comparator: existing raw/physics/whitened budget-10 route
  artifacts.
- Primary criterion: each phase must produce a result or blocker artifact that
  preserves its evidence contract.
- Veto diagnostics: CPU-only material route, missing chain-rule checks,
  unsupported scientific claims, undocumented route drift.
- Non-claims: no HMC readiness, posterior correctness, SIR gradient
  correctness, production default, or global reparameterization claim.

Actions:

- Drafted master program, phase subplans, visible runbook, review ledger, and
  stop handoff.
- Ran Claude plan review until convergence.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-master-program-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-visible-gated-execution-runbook-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-claude-review-ledger-2026-07-01.md`

Gate status:

- `PASSED`

### 2026-07-01T05:10:00+08:00 - Phase 0 - ASSESS_GATE

Question:

- Are the ladder, baseline, phase gates, and first implementation target
  correctly scoped before code changes?

Actions:

- Ran local heading/path checks.
- Ran code-anchor inventory.
- Ran Python compile check for existing SIR diagnostic harnesses.
- Recorded Claude review convergence.

Artifact:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase0-scope-route-result-2026-07-01.md`

Gate status:

- `PASSED`

### 2026-07-01T05:27:06+08:00 - Phase 1 - PRECHECK/REPAIR

Question:

- Does decomposing scalar `log_kappa_scale` into per-region kappa scores
  localize the mismatch or reveal scalar aggregation failure?

Skeptical audit:

- A prior Phase 1 run did not preserve seed microbatch size `1`; this was a
  route-comparison flaw because the frozen budget diagnostic used seed
  microbatches.
- Patched the Phase 1 route to aggregate seed microbatch contexts before
  rerunning material evidence.

Local checks:

- `python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_regional_kappa_gradient_decomposition.py`
- `bash -n scripts/run_sir_gradient_reparam_rootcause_phase1_regional_kappa_budget10.sh`
- `pytest -q tests/test_p8p_regional_kappa_gradient_decomposition.py`
- `pytest -q tests/test_ledh_pfpf_ot_p7_manual_score.py`

Gate status:

- `REPAIRED_AND_RAN`

### 2026-07-01T05:31:15+08:00 - Phase 1 - ASSESS_GATE

Material command:

- `bash scripts/run_sir_gradient_reparam_rootcause_phase1_regional_kappa_budget10.sh`

Result:

- Chain-rule reconstruction passed exactly: scalar manual
  `-205.1933135986328`, regional manual sum `-205.1933135986328`, delta `0.0`.
- Regional FD sum was `-263.2179145812988`, leaving FD-manual gap
  `-58.024600982666016`.
- Scalar aggregation failure is ruled out.

Artifacts:

- `docs/benchmarks/benchmark_p8p_regional_kappa_gradient_decomposition.py`
- `tests/test_p8p_regional_kappa_gradient_decomposition.py`
- `scripts/run_sir_gradient_reparam_rootcause_phase1_regional_kappa_budget10.sh`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase1-regional-kappa-budget10-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase1-regional-kappa-result-2026-07-01.md`

Gate status:

- `PASSED`

### 2026-07-01T05:37:36+08:00 - Phase 1/2 Claude Review - REPAIR_LOOP

Claude review:

- Iteration 1 returned `VERDICT: REVISE`.
- Material fixes requested: remove unsupported XLA wording, replace parity
  placeholder with the actual command, and anchor whitened-direction
  discussion to the exact prior artifact.

Patch response:

- Replaced route language with GPU/TF32 unless explicit compiler status is
  captured.
- Inserted actual parity-check command.
- Anchored whitened-direction discussion to
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-whitened-budget10-2026-07-01.json`.

Gate status:

- `PATCHED`

### 2026-07-01T05:47:00+08:00 - Phase 1/2 Claude Review - PASS_REVIEW

Claude focused re-review:

- `VERDICT: AGREE`

Gate status:

- `PHASE1_CLOSED_PHASE2_CLEARED`

### 2026-07-01T05:49:14+08:00 - Phase 2 - EXECUTE_MINIMAL/ASSESS_GATE

Question:

- Is the problematic dynamic score direction better described as regional
  infection-vs-recovery contrast or common-rate direction?

Local checks:

- `python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_regional_orthogonal_gradient_decomposition.py`
- `bash -n scripts/run_sir_gradient_reparam_rootcause_phase2_regional_orthogonal_budget10.sh`
- `pytest -q tests/test_p8p_regional_orthogonal_gradient_decomposition.py`
- `pytest -q tests/test_p8p_regional_kappa_gradient_decomposition.py`

Material command:

- `bash scripts/run_sir_gradient_reparam_rootcause_phase2_regional_orthogonal_budget10.sh`

Result:

- Chain-rule reconstruction passed for kappa, nu, rho, and tau.
- Aggregate gaps: kappa `-58.0246`, nu `19.6446`, rho `-55.1641`, tau
  `-26.3071`.
- Classification: dominant infection-vs-recovery contrast with secondary
  common-rate discrepancy.

Artifacts:

- `docs/benchmarks/benchmark_p8p_regional_orthogonal_gradient_decomposition.py`
- `tests/test_p8p_regional_orthogonal_gradient_decomposition.py`
- `scripts/run_sir_gradient_reparam_rootcause_phase2_regional_orthogonal_budget10.sh`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase2-regional-orthogonal-budget10-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase2-regional-orthogonal-result-2026-07-01.md`

Gate status:

- `PASSED_PENDING_REVIEW`

### 2026-07-01T06:04:00+08:00 - Phase 2/3 Claude Review - REPAIR_LOOP

Claude review:

- `VERDICT: REVISE`

Material findings:

- Phase 3 prematurely introduced non-centered/process-noise as an automatic
  next branch.
- Phase 3 tolerance/pass criterion was underspecified.
- CPU-only transition checks needed an explicit boundary.
- Transport-adjoint and stopped-scale-key alternatives needed to remain live.

Patch response:

- Tightened Phase 3 to transition-only algebra.
- Added exact float64 CPU tolerances: max absolute residual `<= 1.0e-8` and
  relative L2 residual `<= 1.0e-7`.
- Removed pre-authorization of non-centered/process-noise.
- Preserved transport-adjoint/stopped-scale-key alternatives.

Gate status:

- `PATCHED`

### 2026-07-01T06:11:04+08:00 - Phase 2/3 Claude Review - PASS_REVIEW

Claude focused re-review:

- `VERDICT: AGREE`

Gate status:

- `PHASE2_CLOSED_PHASE3_CLEARED`

### 2026-07-01T06:11:04+08:00 - Phase 3 - PRECHECK

Question:

- Is the manual RK4 transition derivative for kappa/nu correct before LEDH
  transport terms enter?

Skeptical audit:

- CPU-only execution is allowed because Phase 3 is local transition algebra,
  not material LEDH evidence.
- Passing Phase 3 cannot eliminate transport-adjoint or stopped-scale-key
  explanations.

Gate status:

- `IN_PROGRESS`

### 2026-07-01T06:40:00+08:00 - Phase 5 - ASSESS_GATE

Actions:

- Wrote Phase 5 synthesis result.
- Preserved local transition/transport VJP passes as local evidence only.
- Classified the remaining issue as unresolved full-route score mismatch.

Artifact:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase5-synthesis-result-2026-07-01.md`

Gate status:

- `PENDING_FINAL_CLAUDE_REVIEW`

### 2026-07-01T06:44:00+08:00 - Phase 5 - PASS_REVIEW/CLOSE

Claude final review:

- `VERDICT: AGREE`
- No material findings.

Final status:

- Root-cause program completed with unresolved full-route score mismatch.
- Phase 5 recommends a new tiny full-route score-assembly parity plan as the
  next smallest diagnostic.

Gate status:

- `COMPLETED`

### 2026-07-01T06:17:00+08:00 - Phase 3 - ASSESS_GATE

Local checks:

- `python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/diagnose_p8p_sir_rk4_sensitivity_vjp.py`
- `pytest -q tests/test_p8p_sir_rk4_sensitivity_vjp.py`
- `python docs/benchmarks/diagnose_p8p_sir_rk4_sensitivity_vjp.py --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-2026-07-01.json`

Result:

- Diagnostic status: `PASS`.
- Failure localization: `pass`.
- Largest max absolute residual: `3.410605131648481e-13`.
- Largest full-RK4 max absolute residual: `2.842170943040401e-14`.
- Regional log-kappa/log-nu chain-rule checks both passed against regional
  autodiff.

Artifacts:

- `docs/benchmarks/diagnose_p8p_sir_rk4_sensitivity_vjp.py`
- `tests/test_p8p_sir_rk4_sensitivity_vjp.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-subplan-2026-07-01.md`

Gate status:

- `PASSED_PENDING_PHASE4_REVIEW`

### 2026-07-01T06:22:00+08:00 - Phase 3/4 Claude Review - REPAIR_LOOP

Claude review:

- Iteration 1 returned `VERDICT: REVISE`.

Material findings:

- Phase 4 needed to bind the independent comparator to an exact
  non-custom-gradient symbol/path.
- Phase 4 needed an explicit branch for a clean-comparator failure that does
  not localize.

Patch response:

- Pinned comparator to
  `annealed_transport_tf._filterflow_manual_streaming_finite_transport_value_stopped_scale_keys`.
- Added `diffuse_transport_mismatch` handoff/stop conditions.

Gate status:

- `PATCHED`

### 2026-07-01T06:27:00+08:00 - Phase 3/4 Claude Review - PASS_REVIEW

Claude focused re-review:

- `VERDICT: AGREE`

Gate status:

- `PHASE3_CLOSED_PHASE4_CLEARED`

### 2026-07-01T06:27:00+08:00 - Phase 4 - PRECHECK

Question:

- Does the P8p manual transport VJP wrapper match autodiff for the same
  stopped-scale-key forward transport before full-filter score assembly?

Skeptical audit:

- The comparator is pinned to a non-custom-gradient value helper.
- Passing Phase 4 clears only local transport wrapper algebra, not full score
  assembly or material GPU/TF32 behavior.
- Failing without localization has a precommitted
  `diffuse_transport_mismatch` branch.

Gate status:

- `IN_PROGRESS`

### 2026-07-01T06:32:00+08:00 - Phase 4 - ASSESS_GATE

Local checks:

- `python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/diagnose_p8p_sir_transport_adjoint_vjp.py`
- `pytest -q tests/test_p8p_sir_transport_adjoint_vjp.py`
- `python docs/benchmarks/diagnose_p8p_sir_transport_adjoint_vjp.py --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-2026-07-01.json`

Result:

- Diagnostic status: `PASS`.
- Failure localization: `pass`.
- Comparator guard passed with zero calls to forbidden custom-gradient
  transport routes.
- Largest max absolute residual: `2.3314683517128287e-15`.
- Largest relative L2 residual: `7.470158257190283e-16`.

Artifacts:

- `docs/benchmarks/diagnose_p8p_sir_transport_adjoint_vjp.py`
- `tests/test_p8p_sir_transport_adjoint_vjp.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase5-synthesis-subplan-2026-07-01.md`

Gate status:

- `PASSED_PENDING_PHASE5_SYNTHESIS`

### 2026-07-01T06:36:00+08:00 - Phase 5 - PRECHECK

Question:

- What is the best-supported current root-cause classification and next
  action?

Local checks:

- `rg -n "Status:|Decision|BLOCK|No SIR gradient correctness|No HMC readiness|not concluded|Nonclaims" docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase*-result-2026-07-01.md docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-visible-stop-handoff-2026-07-01.md`
- Phase artifact inventory script over phases `0..4`.

Result:

- Every phase from 0 to 4 has a result artifact.
- Phase 5 synthesis is ready to draft.

Gate status:

- `IN_PROGRESS`
