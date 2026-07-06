# P04C2A Subplan: Harness Exception Artifact Repair

Date: 2026-06-26

Status: `P04C2A_DRAFT_LOCAL_REVIEW_PENDING`

## Phase Objective

Repair the range-bearing benchmark harness so planned TensorFlow route
exceptions can be serialized as structured JSON and Markdown diagnostic
artifacts during explicit diagnostic runs.

The repair must preserve default behavior: route exceptions must still raise
normally unless an explicit exception-capture option is provided. P04C2A is a
harness artifact-contract repair only; it must not tune SVD-Nystrom, repair the
streaming math, resume calibration, freeze a threshold, launch P05, or authorize
promotion.

## Entry Conditions Inherited From Previous Phase

- P04C0 emitted `P04C0_HARNESS_CONTROL_PASS_TO_P04C_PREFLIGHT`.
- P04C emitted `P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT`.
- P04C1 emitted `P04C1_GPU_TF32_OR_JIT_SPECIFIC_DIAGNOSTIC`.
- P04C2 emitted `P04C2_BLOCKED_INVALID_DIAGNOSTIC_ARTIFACT`.
- The P04C2 first row `gpu-tf32-nojit-84101` exited with TensorFlow
  `InvalidArgumentError` before writing JSON/Markdown artifacts.
- P04C calibration remains blocked.
- P05 remains blocked.
- No HMC readiness claim is in scope.

## Required Artifacts

- P04C2A subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2a-harness-exception-artifact-repair-subplan-2026-06-26.md`
- P04C2A result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2a-harness-exception-artifact-repair-result-2026-06-26.md`
- Modified harness:
  `docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py`
- Focused tests:
  `tests/test_svd_nystrom_range_bearing_gate.py`
- Updated execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-execution-ledger-2026-06-25.md`
- Updated Claude review ledger if Claude is used:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-claude-review-ledger-2026-06-25.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-stop-handoff-2026-06-25.md`

## Required Checks, Tests, And Reviews

- Local pre-implementation audit:
  - Confirm P04C2 stopped only because row artifacts were missing/malformed.
  - Confirm the repair is artifact capture, not a numerical fix or tuning
    change.
  - Confirm exception capture is opt-in and default behavior remains to raise.
  - Confirm structured exception rows carry hard vetoes and cannot be counted
    as pass rows.
- Implementation checks:
  - Add an explicit CLI option such as `--capture-route-exceptions`.
  - When disabled, preserve current exception behavior.
  - When enabled, catch route-level exceptions, write a row with `status:
    FAIL`, exception metadata, route hard veto, timing metadata available up to
    the exception, and no fabricated route outputs.
  - Prevent paired-comparability computation when either paired route has an
    exception row or missing log-likelihood output.
  - Keep existing nonfinite-output hard veto behavior unchanged.
- Focused tests:
  - Existing tiny CPU route smoke still passes.
  - Record-only and gate paired-threshold tests still pass.
  - New test verifies opt-in TensorFlow exception capture produces structured
    failure rows and aggregate hard vetoes.
  - New test verifies default non-capture mode re-raises route exceptions.
- Required local command:

```bash
/home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest tests/test_svd_nystrom_range_bearing_gate.py -q
```

- Claude read-only review is required for this material subplan before
  implementation if Claude is available under the approved scope. Claude may
  review only this exact subplan and the P04C2 result unless a separate prompt
  explicitly authorizes additional exact documents. Claude may not read source
  code, tests, logs, unrelated paths, credentials, model files, or run commands;
  may not edit files; and may not authorize promotion/default/scientific/HMC
  boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the range-bearing benchmark preserve planned TensorFlow route exceptions as structured artifacts without masking default failures? |
| Baseline/comparator | Current P04C2 failure: TensorFlow `InvalidArgumentError` before JSON/Markdown write. |
| Primary criterion | Focused local tests pass and the harness has opt-in exception capture that emits hard-veto row artifacts while default behavior still re-raises. |
| Veto diagnostics | Default exception behavior changed; exception rows can be interpreted as passes; paired deltas computed from exception rows; missing tests; unrelated source edits; unsupported threshold/promotion claims; source code disclosed to Claude without explicit approval. |
| Explanatory diagnostics | Exception type, module, message, traceback tail, route, timing until exception, device/GPU/TF32/JIT manifest. |
| Not concluded | No streaming numerical repair, no SVD-Nystrom quality conclusion, no threshold calibration, no P04C resume, no P05 launch, no default promotion, no posterior correctness, no HMC readiness, and no statistical superiority. |
| Artifact | P04C2A result and focused pytest output. |

## Forbidden Claims And Actions

- Do not tune SVD-Nystrom rank, epsilon, solver, rcond, kernel mode, scaling
  mode, thresholds, seeds, fixture, shape, dtype, or transport policy.
- Do not change the streaming route implementation in P04C2A.
- Do not change the meaning of existing nonfinite-output vetoes.
- Do not make exception rows eligible for PASS.
- Do not compute paired log-likelihood deltas from exception rows.
- Do not resume P04C rows `84102..84111`.
- Do not rerun P04C2 runtime rows until P04C2A closes.
- Do not launch P05.
- Do not send source code or tests to Claude without explicit approval.
- Do not make default, product, HMC-readiness, posterior-correctness,
  statistical-superiority, or broad scientific-validity claims.

## Exact Next-Phase Handoff Conditions

- `P04C2A_PASS_TO_P04C2_RERUN`: opt-in exception capture is implemented,
  default re-raise behavior is tested, focused tests pass, and P04C2A result is
  written.
- `P04C2A_BLOCKED_SOURCE_REVIEW_SCOPE`: required review would need Claude to
  inspect source/test files without explicit approval.
- `P04C2A_BLOCKED_DEFAULT_BEHAVIOR_RISK`: exception capture cannot be added
  without changing default harness behavior.
- `P04C2A_BLOCKED_TEST_FAILURE`: focused tests fail in a way not fixed inside
  the P04C2A scope.

After `P04C2A_PASS_TO_P04C2_RERUN`, the next phase is a repaired P04C2 rerun
subplan or refreshed P04C2 command set that adds the explicit exception-capture
option and reruns rows one at a time with JSON parsing after each row.

## Stop Conditions

- The proposed implementation would hide route exceptions by default.
- The proposed implementation would treat exception rows as successful route
  evidence.
- Focused tests fail and the fix would require streaming-route math changes,
  SVD-Nystrom tuning, threshold changes, fixture changes, package installation,
  network fetches, commits, pushes, destructive actions, or source disclosure to
  Claude.
- A broader harness redesign is required.
- Continuing would require P04C calibration continuation, P05 execution,
  threshold freeze, default/product/scientific/HMC authorization, or dropping
  seed `84101`.

## End-Of-Phase Requirements

At P04C2A close, Codex must:

1. run the required local checks;
2. write the P04C2A result/close record;
3. update the execution ledger and stop handoff;
4. draft or refresh the repaired P04C2 rerun instructions if P04C2A passes;
5. review the next subplan locally and, when authorized and useful, with
   Claude.

## Local Self-Review Of This Subplan

Skeptical audit:

- Wrong baseline: the baseline is the missing-artifact P04C2 failure, not a
  method-quality comparator.
- Proxy metric: exception capture is a harness validity repair, not promotion
  evidence.
- Missing stop conditions: default-behavior drift, pass-row confusion, paired
  delta misuse, and source-review scope are explicit stops.
- Unfair comparison: no runtime method comparison occurs in P04C2A.
- Hidden assumption: the repair assumes route-level exception capture is enough
  to preserve the next diagnostic; tests must verify that default behavior is
  unchanged.
- Environment mismatch: required tests are CPU-hidden/unit-level and do not
  claim GPU runtime success.
- Artifact fit: P04C2A result and focused pytest output directly answer
  whether the harness can produce structured exception artifacts.
