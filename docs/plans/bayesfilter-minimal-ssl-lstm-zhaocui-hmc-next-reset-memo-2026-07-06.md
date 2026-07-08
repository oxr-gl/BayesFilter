# Reset Memo: Minimal SSL-LSTM Zhao-Cui HMC Next Program

Date: 2026-07-06

## Final State

The minimal scalar SSL-LSTM `zhaocui_fixed` HMC next program completed through
Phase 6 closeout.

What was accomplished:

- Extracted the benchmark-only minimal HMC target adapter into internal module
  `bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py`.
- Updated the benchmark harness to consume the internal module.
- Added focused internal-module and ladder tests.
- Ran CPU-hidden regression through the internal surface.
- Ran trusted GPU/XLA launch smoke.
- Designed, reviewed, repaired, and ran a longer trusted GPU/XLA hard-veto
  diagnostic ladder over three predeclared seeds.
- Wrote result, review, reset, and handoff artifacts.

## Key Result

Phase 5 runtime artifact:

- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.json`

Summary:

- Status: `passed`
- Hard vetoes: `[]`
- Seeds: `[20260706, 5101]`, `[20260706, 5102]`, `[20260706, 5103]`
- Sample shape: `[8, 24]` for all seeds
- Samples finite: `true` for all seeds
- GPU: `/physical_device:GPU:0`
- `use_xla=True`, `jit_compile=True`, TF32 enabled
- Native divergence status: `not_exposed_by_kernel`; this is not zero
  divergences
- Acceptance rates: `1.0`, `1.0`, `1.0`; explanatory only

## Review Path

- External Claude review remained blocked by private-context transfer approval.
- Fresh visible Codex substitute review was used.
- Phase 4/5 plan review returned `REVISE` for missing fixed guards on prior
  scale and initial offset scale; the issue was repaired and focused re-review
  returned `AGREE`.
- Phase 5 result review returned `AGREE`.

## Important Boundaries

This program did not establish:

- HMC convergence;
- posterior correctness;
- R-hat/ESS evidence;
- statistical ranking or superiority;
- BayesFilter default readiness;
- GPU/XLA production readiness;
- public API/package readiness;
- source-faithful SSL-LSTM Zhao-Cui parity;
- LEDH result.

The `zhaocui_fixed` path remains a clean-room fixed adaptation / diagnostic
target, not source-faithful Zhao-Cui parity.

## Resume Guidance

Reasonable next plans, each requiring a new reviewed evidence contract:

- longer chains with convergence diagnostics and uncertainty-aware replication;
- posterior/reference checks for the minimal scalar target;
- adaptation/tuning diagnostics for fixed-kernel limitations;
- source-anchor work if the target is source-faithful Zhao-Cui parity;
- LEDH work as a separate route, not implied by this program.

Do not treat the Phase 5 hard-veto pass as convergence, posterior correctness,
ranking, default readiness, or production readiness.

## Dirty Worktree Note

The worktree is intentionally dirty with many existing modified/untracked files
from the larger SSL-LSTM/HMC workstream. This run preserved unrelated changes
and did not revert user or prior-agent work.
