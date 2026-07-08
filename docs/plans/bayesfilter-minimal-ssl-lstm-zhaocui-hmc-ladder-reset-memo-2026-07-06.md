# Reset Memo: Minimal SSL-LSTM Zhao-Cui HMC Ladder

Date: 2026-07-06

## Final State

The minimal scalar SSL-LSTM `zhaocui_fixed` HMC ladder completed through Phase
6 closeout.

What was built:

- A minimal internal HMC target adapter harness in
  `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py`
- Focused tests in `tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py`
- Standalone CPU-hidden Phase 2 canary artifact/log
- Standalone CPU-hidden fixed three-seed Phase 4 short-ladder artifact/log

## What Passed

- Phase 1 target-adapter admission passed.
- Phase 2 standalone tiny CPU-hidden canary passed with no hard vetoes.
- Phase 3 required no repair.
- Phase 4 standalone fixed three-seed short debug ladder passed with no hard
  vetoes.
- Phase 5 GPU/XLA bridge was explicitly deferred because there was no remaining
  approved runtime-path question requiring it.

## Important Boundaries

- No claim of posterior correctness.
- No claim of HMC convergence.
- No claim of ranking or superiority.
- No claim of source-faithful Zhao-Cui parity.
- No claim of GPU/XLA production readiness or default readiness.
- No LEDH result.

Acceptance rate was explanatory only. Native divergence was `not_exposed_by_kernel`
in the tiny CPU-hidden runs and was not interpreted as zero divergences.

## Review Path

- External Claude review was denied for private-context transfer risk.
- Local Codex substitute review was used for material gates.
- Phase 2 and Phase 4 both needed executable-artifact repairs before launch.

## Resume Guidance

If work resumes, the next clean branches are:

1. Trusted GPU/XLA runtime-path smoke:
   Only with explicit approval and a narrow question about runtime-path
   behavior, not convergence or readiness.
2. Longer reviewed sampler-diagnostics plan:
   Requires a new plan with explicit evidence bars before any convergence,
   posterior, ranking, or default-readiness language.

## Dirty Worktree Note

This session preserved unrelated dirty worktree state and did not revert
non-owned changes.
