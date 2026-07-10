# Review Bundle: Phase 2S Result And Phase 2T TF32 Correctness Policy

Date: 2026-07-09

Reviewer role: read-only. Codex remains supervisor and executor.

## Objective

Review whether Phase 2S correctly stops before a full `N=10000,T=50` LGSSM
score run, and whether Phase 2T is a valid next phase for resolving the
default-TF32 correctness blocker.

## Artifacts Under Review

- Phase 2S result:
  `docs/plans/bayesfilter-ledh-n10000-score-admission-repair-phase2s-lgssm-score-procedure-repair-result-2026-07-09.md`
- Phase 2T subplan:
  `docs/plans/bayesfilter-ledh-n10000-score-admission-repair-phase2t-lgssm-tf32-correctness-policy-subplan-2026-07-09.md`
- Runner:
  `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
- Tests:
  `tests/highdim/test_ledh_lgssm_score_phase2_contract.py`
  `tests/test_ledh_lgssm_manual_score_phase4.py`

## Key Evidence

Phase 2S implemented:

- value-only same-scalar FD route;
- score-specific GPU memory reset and memory fields;
- score artifact memory diagnostics from `score_gpu_memory_info_after`;
- nested `score_artifact` emission for full-row score runs;
- tests that fail if FD calls the score route or score memory is copied from
  value-route memory.

Local checks:

```text
52 passed, 2 warnings
```

CPU prefix smoke:

```text
score_status = executed_compact_score_fd_pass_but_material_gate_blocked
score_admission_status = blocked_material_gate_not_full_gpu_row
same_scalar_fd.status = pass
```

Trusted GPU TF32 smoke at `N=256,T=3`:

```text
score_runtime_gate_applicable = true
score_gpu_memory_stats_reset = true
score_gpu_memory_info_after.peak = 139720704 bytes
same_scalar_fd.status = fail
same_scalar_fd.max_abs_error = 3.4168434143066406
same_scalar_fd.max_relative_error = 0.21000058948993683
```

Trusted GPU no-TF32 smoke at same size:

```text
score_runtime_gate_applicable = true
same_scalar_fd.status = pass
same_scalar_fd.max_abs_error = 0.0009069442749023438
same_scalar_fd.max_relative_error = 0.0010520674986764789
```

TF32 FD-step diagnostic:

```text
step 0.001: fail, max_abs_error 3.4168434143066406
step 0.003: fail, max_abs_error 0.7971048355102539
step 0.01: fail, max_abs_error 0.1394672393798828
```

## Proposed Phase 2T

Phase 2T must select a reviewed correctness policy before any full run. It may
evaluate:

1. TF32 production score/value execution with a disclosed no-TF32 correctness
   arm for same-scalar FD;
2. bounded TF32 FD calibration, only if it remains sensitive enough to catch
   route mismatches;
3. an exact/reference correctness check, only if it certifies the finite LEDH
   target rather than exact Kalman likelihood alone.

## Review Questions

1. Is Phase 2S right to stop before full `N=10000,T=50` admission?
2. Is Phase 2T the right next phase?
3. Are the three candidate policies safely bounded?
4. Should any candidate be forbidden before execution?
5. Are stop conditions and nonclaims sufficient?

## Pass/Block Criteria

Return `VERDICT: AGREE` only if Phase 2T is safe to execute as the next repair
phase.

Return `VERDICT: REVISE` if Phase 2T should be patched before execution.

Forbidden nonclaims:

- no LGSSM score admission yet;
- no full leaderboard completion;
- no compact-math rejection;
- no exact Kalman score validation of finite LEDH without derivation;
- no HMC/posterior/scientific/runtime claims.

End with exactly one verdict line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
