# Reset Memo: Minimal SSL-LSTM Zhao-Cui Smoke

Date: 2026-07-06

Status: `RESET_MEMO_CURRENT`

## Current State

The minimal scalar SSL-LSTM smoke program completed its stated scope.

The existing `zhaocui_fixed` clean-room fixed adapter now has a dedicated
minimal one-dimensional smoke harness and focused test that preserve a visible
CPU-hidden debug artifact for:

- finite deterministic value/score behavior;
- finite-difference subset agreement;
- explicit primary/comparator role boundaries.

No additional launch-smoke bridge was required for this narrow question.

## Main Files To Know

| File | Note |
| --- | --- |
| `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_smoke_2026_07_06.py` | Minimal scalar smoke harness and artifact writer. |
| `tests/test_minimal_ssl_lstm_zhaocui_smoke.py` | Focused validation of the harness artifact, roles, and CLI output. |
| `docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.json` | Structured minimal smoke artifact. |
| `docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.md` | Human-readable smoke summary. |
| `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase1-harness-result-2026-07-06.md` | Harness implementation/result record. |
| `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase4-closeout-result-2026-07-06.md` | Final closeout result. |

## Review Path Note

The requested external Claude review gate was rejected by the approval reviewer
because it would send private repository context to an external service.
Bounded local Codex substitute reviews were recorded instead. Do not treat this
as equivalent to external Claude review; it is the safer fallback path for this
workspace.

## Evidence Limits

Do not claim:

- source-faithful SSL-LSTM Zhao-Cui parity;
- posterior correctness;
- method superiority or ranking;
- HMC convergence;
- GPU/XLA production readiness;
- default readiness;
- LEDH sufficiency or LEDH evidence.

Current evidence is CPU-hidden minimal debug/smoke evidence only.

## Most Recent Passing Checks

- `python -m compileall -q docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_smoke_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_smoke.py`
  passed.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_minimal_ssl_lstm_zhaocui_smoke.py`
  passed: `3 passed`.
- `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_smoke_2026_07_06.py --output docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.md`
  passed with artifact status `passed`.
- `git diff --check` passed.

## Generated Artifacts

- `docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.md`
- `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_smoke_2026-07-06/compile.log`
- `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_smoke_2026-07-06/pytest.log`
- `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_smoke_2026-07-06/harness.log`

## Worktree Note

The worktree was already dirty before and during this recovery. Preserve
unrelated existing changes from the earlier July 4/5 SSL-LSTM and HMC work.
The minimal-smoke changes are concentrated in the files listed above plus the
July 6 plan/result/review artifacts.

## Next Sensible Work

Future work should start a new plan if needed, for example:

- a broader launch-smoke or longer runtime bridge for a different question;
- longer replicated HMC evidence with predeclared diagnostics;
- reviewed GPU/XLA production-target evidence;
- deeper Zhao-Cui source-route work with explicit source-faithfulness scope.
