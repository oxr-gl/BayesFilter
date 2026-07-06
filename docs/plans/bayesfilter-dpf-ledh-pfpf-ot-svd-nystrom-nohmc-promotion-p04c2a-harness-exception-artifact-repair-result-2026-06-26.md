# P04C2A Result: Harness Exception Artifact Repair

Date: 2026-06-26

Status: `P04C2A_PASS_TO_P04C2_RERUN`

## Phase Objective

Repair the range-bearing benchmark harness so planned TensorFlow route
exceptions can be serialized as structured JSON and Markdown diagnostic
artifacts during explicit diagnostic runs, while preserving default exception
behavior.

## Decision Table

| Field | Result |
| --- | --- |
| Decision | `P04C2A_PASS_TO_P04C2_RERUN` |
| Primary criterion status | PASS: opt-in exception capture was implemented and focused local tests passed. |
| Veto diagnostic status | No P04C2A veto fired. Default exception behavior remains tested as re-raise. |
| Main uncertainty | P04C2 runtime isolation remains unresolved until rows are rerun with `--capture-route-exceptions`. |
| Next justified action | Rerun P04C2 rows one at a time with explicit exception capture and JSON parsing after each row. |
| What is not concluded | No streaming numerical repair, no SVD-Nystrom quality conclusion, no threshold calibration, no P04C resume, no P05 launch, no default promotion, no posterior correctness, no HMC readiness, and no statistical superiority. |

## Evidence Contract Outcome

| Field | Contract Outcome |
| --- | --- |
| Question | Answered for harness behavior: the range-bearing benchmark can preserve planned route exceptions as structured artifacts only when explicitly requested. |
| Baseline/comparator | Current P04C2 failure: TensorFlow exception before JSON/Markdown write. |
| Primary criterion | Met: focused tests pass and exception capture is opt-in. |
| Veto diagnostics | No default-behavior drift, no pass-row confusion, no paired deltas from exception rows, and no source disclosure to Claude. |
| Explanatory diagnostics | Exception rows record exception type, module, message, traceback tail, route, stage, and available timing metadata. |
| Not concluded | No runtime isolation classification and no method promotion claim. |
| Artifact | This P04C2A result and focused pytest output. |

## Implementation Summary

Modified harness:
`docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py`

Implemented:

- Added explicit `--capture-route-exceptions` CLI switch.
- Preserved default route exception behavior: without the flag, exceptions
  still propagate.
- With the flag, route exceptions are serialized as row-level `FAIL` artifacts
  with `hard_vetoes: ["route_exception"]`.
- Exception rows do not fabricate `log_likelihood`, route outputs, or output
  devices.
- Paired comparability is not computed if either paired route has an exception
  row or lacks `log_likelihood`.
- Markdown output includes a route-exception section when present.
- Run manifest records `capture_route_exceptions`.

Focused tests:
`tests/test_svd_nystrom_range_bearing_gate.py`

Added tests:

- opt-in exception capture produces structured failure rows and aggregate hard
  vetoes;
- default non-capture mode re-raises route exceptions.

## Required Local Checks

Command:

```bash
/home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest tests/test_svd_nystrom_range_bearing_gate.py -q
```

Result:

```text
8 passed, 14572 warnings in 17.16s
```

The warnings are TensorFlow/TFP/gast deprecation warnings observed during
existing test execution; they did not fail the focused check.

## Claude Review

P04C2A plan review:

- Round: `P04C2A-R1`
- Scope: exact P04C2A subplan plus exact P04C2 result; no source/test/log reads.
- Verdict: `VERDICT: AGREE`
- Review summary: Claude agreed the subplan is correctly scoped as opt-in
  harness exception-artifact repair, treats P04C2 as missing structured
  diagnostics rather than SVD-Nystrom failure, preserves no-claim boundaries,
  and forbids paired deltas from exception rows.

Claude did not review source code or tests.

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | PASS for harness repair tests. P04C calibration remains blocked pending repaired P04C2 rerun. |
| Statistically supported ranking | NO |
| Descriptive-only differences | Runtime and route-exception metadata from later reruns will be diagnostic only. |
| Default-readiness | NO |
| Next evidence needed | Repaired P04C2 GPU TF32/JIT isolation rows with structured artifacts. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Conda/Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` |
| TensorFlow | `2.20.0` |
| Device policy | Focused tests ran with `CUDA_VISIBLE_DEVICES=-1` set by the test module; this is CPU-hidden unit coverage, not GPU runtime evidence. |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2a-harness-exception-artifact-repair-subplan-2026-06-26.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2a-harness-exception-artifact-repair-result-2026-06-26.md` |

## Post-Run Red-Team Note

Strongest alternative explanation: the harness repair may correctly serialize
exceptions while the next runtime classification still remains ambiguous if
multiple P04C2 rows produce different exception/nonfinite patterns. That is not
a P04C2A failure; it means P04C2 must classify only the predeclared row pattern.

Weakest part of the evidence: P04C2A tests use synthetic route exceptions and
CPU-hidden unit execution. They validate artifact mechanics, not the real GPU
failure mode. The real GPU evidence must come from the repaired P04C2 rerun.

## Handoff

`P04C2A_PASS_TO_P04C2_RERUN`

Rerun P04C2 rows one at a time with `--capture-route-exceptions` added to the
predeclared commands, parse each JSON artifact before launching the next row,
and keep all P04C/P05/promotion/default/scientific/HMC boundaries closed.
