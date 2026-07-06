# BayesFilter HMC Fixed-Mass Dual-Averaging XLA Probe Review Ledger

Date: 2026-06-20

Repository: `/home/ubuntu/python/BayesFilter`

Subplan:
`docs/plans/bayesfilter_hmc_fixed_mass_dual_averaging_xla_probe_subplan_2026_06_20.md`

## Round 1

Reviewer: Claude Code read-only, path-only bounded review

Command shape:

```text
bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh
  --cwd /home/ubuntu/python/BayesFilter
  --name bayesfilter-hmc-xla-da-plan-review
  "Read-only bounded review ..."
```

Allowed paths:

- `docs/plans/bayesfilter_hmc_fixed_mass_dual_averaging_xla_probe_subplan_2026_06_20.md`
- `bayesfilter/inference/hmc.py`
- `bayesfilter/inference/hmc_tuning.py`
- `tests/test_hmc_fixed_mass_step_tuning.py`
- `tests/test_nonlinear_ssm_phase4_full_chain_hmc.py`

Findings:

1. Required checks did not explicitly include existing full-chain XLA
   authority-boundary tests for unreviewed authority and target-only XLA
   rejection.
2. Required checks named generic dual averaging but did not separately require
   raw-string `adaptation_policy="dual_averaging"` rejection and
   reviewed-but-generic `HMCTuningPolicy.dual_averaging_step_size` rejection.
3. The stated adaptive-trace veto was not fully operationalized in the new XLA
   probe requirement; the probe needed explicit `step_size`,
   `target_accept_prob`, and `num_adaptation_steps` assertions.

Verdict: `REVISE`

Patch applied:

- Added authority-boundary tests to the required-check list.
- Added both raw-string and reviewed-but-generic dual-averaging rejection
  checks.
- Added the three adaptive trace fields to the new XLA probe contract.

## Round 2

Reviewer: Claude Code read-only, focused re-review

Command shape:

```text
bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh
  --cwd /home/ubuntu/python/BayesFilter
  --name bayesfilter-hmc-xla-da-plan-review-r2
  "Read-only bounded re-review ..."
```

Scope:

- Verify only whether the three Round 1 findings were fixed.

Findings:

1. Full-chain XLA authority-boundary checks are now explicitly required at
   subplan lines 50-51.
2. Raw-string and reviewed-but-generic rejection modes are now explicitly
   required at subplan lines 52-54.
3. The new XLA probe now requires adaptive trace fields `step_size`,
   `target_accept_prob`, and `num_adaptation_steps` at subplan lines 55-58.

Verdict: `AGREE`

## Boundary Notes

- Claude was read-only and did not edit files.
- Claude did not authorize scientific, GPU, CCMA, product, funding, or
  posterior-convergence boundaries.
- The review converged after two rounds.
