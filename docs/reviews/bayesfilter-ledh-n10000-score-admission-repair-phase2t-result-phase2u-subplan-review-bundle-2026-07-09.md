# Review Bundle: Phase 2T Result And Phase 2U Full LGSSM Run

Date: 2026-07-09

Reviewer role: read-only. Codex remains supervisor and executor.

## Objective

Review whether Phase 2T closes the TF32 correctness-policy blocker and whether
Phase 2U may launch the full trusted LGSSM `N=10000,T=50` score admission run.

## Phase 2T Evidence

Selected policy:

- production value/score execution remains `float32` with TensorFlow TF32
  enabled;
- same-scalar FD correctness uses the value-only scalar route with TF32
  disabled;
- score artifact discloses the split in `score_correctness`.

Checks:

```text
42 passed, 2 warnings
```

Trusted GPU smoke:

```text
score_runtime_gate_applicable = true
score_gpu_memory_info_after.peak = 139720704 bytes
same_scalar_fd.status = pass
same_scalar_fd.max_abs_error = 0.006190299987792969
same_scalar_fd.max_relative_error = 0.0004953071475028992
same_scalar_fd.tf32_mode = disabled
same_scalar_fd.production_tf32_execution_enabled = true
same_scalar_fd.tf32_execution_enabled = false
same_scalar_fd.uses_disclosed_separate_precision_arm = true
```

## Phase 2U Proposed Full Run

Command preserves:

- row `benchmark_lgssm_exact_oracle_m3_T50`;
- `N=10000`, `T=50`;
- seeds `81120,81121,81122,81123,81124`;
- target scalar `observed_data_log_likelihood_estimator`;
- output field `log_likelihood`;
- compact route `compact_forward_sensitivity_no_autodiff_same_scalar_lgssm_ledh_pfpf_ot`;
- `--dtype float32`, `--tf32-mode enabled`;
- `--score-fd-tf32-mode disabled`;
- score-specific memory gate;
- nested Phase 1 `score_artifact` validation.

Primary pass criterion:

```text
validate_ledh_score_artifact(score_artifact, source_value_artifact=value, expected_row_id=LGSSM_M3_T50_ROW_ID, require_admitted=True)
```

Vetoes:

- no artifact;
- nested score artifact absent;
- validator failure;
- same-scalar FD failure;
- score-specific memory peak above 14 GiB;
- hidden no-TF32 substitution;
- row/target/parameter mismatch;
- historical route;
- arbitrary reruns after failure.

## Review Questions

1. Is it safe to launch Phase 2U full run?
2. Does Phase 2U preserve the target/admission contract?
3. Does the disclosed no-TF32 FD arm avoid hidden precision overclaim?
4. Are stop conditions sufficient if runtime/memory/correctness fails?

Return `VERDICT: AGREE` only if Phase 2U may launch. Otherwise return
`VERDICT: REVISE`.

End with exactly one verdict line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
